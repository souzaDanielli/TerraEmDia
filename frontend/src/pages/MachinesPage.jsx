import { useState, useEffect } from 'react'
import api from '../api'

export default function MachinesPage() {
  const [machines, setMachines] = useState([])
  const [loading, setLoading] = useState(true)
  const [showForm, setShowForm] = useState(false)
  const [editing, setEditing] = useState(null)
  const [showMaint, setShowMaint] = useState(null) // machine id
  const [maintList, setMaintList] = useState([])
  const [showMaintForm, setShowMaintForm] = useState(false)

  // Form states
  const [nome, setNome] = useState('')
  const [tipo, setTipo] = useState('')
  const [horimetro, setHorimetro] = useState('')
  const [intervalo, setIntervalo] = useState('')

  // Maintenance form
  const [maintDesc, setMaintDesc] = useState('')
  const [maintHorimetro, setMaintHorimetro] = useState('')
  const [maintCusto, setMaintCusto] = useState('')
  const [maintObs, setMaintObs] = useState('')

  const [error, setError] = useState('')

  const fetchMachines = () => {
    api.get('/machines')
      .then((res) => setMachines(res.data))
      .finally(() => setLoading(false))
  }

  useEffect(() => { fetchMachines() }, [])

  const resetForm = () => {
    setNome(''); setTipo(''); setHorimetro(''); setIntervalo('')
    setEditing(null); setShowForm(false); setError('')
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    try {
      if (editing) {
        await api.put(`/machines/${editing}`, {
          nome, tipo,
          horimetro_atual: parseFloat(horimetro),
          intervalo_manutencao: parseFloat(intervalo),
        })
      } else {
        await api.post('/machines', {
          nome, tipo,
          horimetro_atual: parseFloat(horimetro) || 0,
          intervalo_manutencao: parseFloat(intervalo),
        })
      }
      resetForm()
      fetchMachines()
    } catch (err) {
      setError(err.response?.data?.detail || 'Erro ao salvar')
    }
  }

  const handleEdit = (m) => {
    setNome(m.nome); setTipo(m.tipo)
    setHorimetro(String(m.horimetro_atual))
    setIntervalo(String(m.intervalo_manutencao))
    setEditing(m.id); setShowForm(true)
  }

  const handleDelete = async (id) => {
    if (!confirm('Tem certeza que deseja excluir esta máquina?')) return
    await api.delete(`/machines/${id}`)
    fetchMachines()
  }

  const openMaintenance = async (machineId) => {
    setShowMaint(machineId)
    const res = await api.get(`/maintenance/${machineId}`)
    setMaintList(res.data)
  }

  const handleMaintSubmit = async (e) => {
    e.preventDefault()
    setError('')
    try {
      await api.post('/maintenance', {
        machine_id: showMaint,
        descricao: maintDesc,
        horimetro_no_momento: parseFloat(maintHorimetro),
        custo: parseFloat(maintCusto) || 0,
        observacao: maintObs,
      })
      setMaintDesc(''); setMaintHorimetro(''); setMaintCusto(''); setMaintObs('')
      setShowMaintForm(false)
      openMaintenance(showMaint)
      fetchMachines()
    } catch (err) {
      setError(err.response?.data?.detail || 'Erro ao registrar manutenção')
    }
  }

  const getStatusClass = (status) => {
    if (status === 'Atenção') return 'atencao'
    if (status === 'Próximo') return 'proximo'
    return 'ok'
  }

  if (loading) return <div className="loading">Carregando...</div>

  // --- Maintenance modal ---
  if (showMaint) {
    const machine = machines.find((m) => m.id === showMaint)
    return (
      <div>
        <div className="page-header">
          <h2>🔧 Manutenções — {machine?.nome}</h2>
          <button className="btn btn-secondary btn-sm" onClick={() => { setShowMaint(null); setShowMaintForm(false) }}>
            ← Voltar
          </button>
        </div>

        <button className="btn btn-primary" style={{ marginBottom: 16 }} onClick={() => setShowMaintForm(true)}>
          + Registrar Manutenção
        </button>

        {showMaintForm && (
          <div className="modal-overlay" onClick={() => setShowMaintForm(false)}>
            <div className="modal" onClick={(e) => e.stopPropagation()}>
              <h2>Registrar Manutenção</h2>
              {error && <div className="error-msg">{error}</div>}
              <form onSubmit={handleMaintSubmit}>
                <div className="form-group">
                  <label>Descrição</label>
                  <input value={maintDesc} onChange={(e) => setMaintDesc(e.target.value)} placeholder="Ex: Troca de óleo" required />
                </div>
                <div className="form-row">
                  <div className="form-group">
                    <label>Horímetro atual</label>
                    <input type="number" step="0.1" value={maintHorimetro} onChange={(e) => setMaintHorimetro(e.target.value)} required />
                  </div>
                  <div className="form-group">
                    <label>Custo (R$)</label>
                    <input type="number" step="0.01" value={maintCusto} onChange={(e) => setMaintCusto(e.target.value)} />
                  </div>
                </div>
                <div className="form-group">
                  <label>Observação</label>
                  <textarea rows={2} value={maintObs} onChange={(e) => setMaintObs(e.target.value)} />
                </div>
                <div className="btn-group">
                  <button type="submit" className="btn btn-primary">Salvar</button>
                  <button type="button" className="btn btn-secondary" onClick={() => setShowMaintForm(false)}>Cancelar</button>
                </div>
              </form>
            </div>
          </div>
        )}

        {maintList.length === 0 ? (
          <div className="empty-state">
            <p>Nenhuma manutenção registrada ainda.</p>
          </div>
        ) : (
          maintList.map((m) => (
            <div key={m.id} className="card">
              <div className="maint-item">
                <div className="maint-desc">{m.descricao}</div>
                <div className="maint-meta">
                  📅 {new Date(m.data).toLocaleDateString('pt-BR')} &nbsp;|&nbsp;
                  ⏱ {m.horimetro_no_momento}h &nbsp;|&nbsp;
                  💰 R$ {m.custo.toFixed(2)}
                </div>
                {m.observacao && <div className="maint-meta">{m.observacao}</div>}
              </div>
            </div>
          ))
        )}
      </div>
    )
  }

  // --- Main machines list ---
  return (
    <div>
      <div className="page-header">
        <h2>🚜 Máquinas</h2>
        <button className="btn btn-primary btn-sm" onClick={() => { resetForm(); setShowForm(true) }}>
          + Nova Máquina
        </button>
      </div>

      {/* Form modal */}
      {showForm && (
        <div className="modal-overlay" onClick={resetForm}>
          <div className="modal" onClick={(e) => e.stopPropagation()}>
            <h2>{editing ? 'Editar Máquina' : 'Nova Máquina'}</h2>
            {error && <div className="error-msg">{error}</div>}
            <form onSubmit={handleSubmit}>
              <div className="form-group">
                <label>Nome</label>
                <input value={nome} onChange={(e) => setNome(e.target.value)} placeholder="Ex: Trator John Deere" required />
              </div>
              <div className="form-group">
                <label>Tipo</label>
                <select value={tipo} onChange={(e) => setTipo(e.target.value)} required>
                  <option value="">Selecione...</option>
                  <option value="Trator">Trator</option>
                  <option value="Colheitadeira">Colheitadeira</option>
                  <option value="Pulverizador">Pulverizador</option>
                  <option value="Plantadeira">Plantadeira</option>
                  <option value="Caminhão">Caminhão</option>
                  <option value="Outro">Outro</option>
                </select>
              </div>
              <div className="form-row">
                <div className="form-group">
                  <label>Horímetro atual (h)</label>
                  <input type="number" step="0.1" value={horimetro} onChange={(e) => setHorimetro(e.target.value)} placeholder="0" />
                </div>
                <div className="form-group">
                  <label>Intervalo manutenção (h)</label>
                  <input type="number" step="0.1" value={intervalo} onChange={(e) => setIntervalo(e.target.value)} placeholder="250" required />
                </div>
              </div>
              <div className="btn-group">
                <button type="submit" className="btn btn-primary">{editing ? 'Salvar' : 'Cadastrar'}</button>
                <button type="button" className="btn btn-secondary" onClick={resetForm}>Cancelar</button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Machine list */}
      {machines.length === 0 ? (
        <div className="empty-state">
          <p>Nenhuma máquina cadastrada.</p>
          <p>Clique em "+ Nova Máquina" para começar.</p>
        </div>
      ) : (
        machines.map((m) => (
          <div key={m.id} className={`card status-${getStatusClass(m.status)}`}>
            <div className="card-header">
              <h3>{m.nome}</h3>
              <span className={`badge badge-${getStatusClass(m.status)}`}>{m.status}</span>
            </div>
            <div className="card-details">
              <span>Tipo: {m.tipo}</span>
              <span>Horímetro: {m.horimetro_atual}h</span>
              <span>Próx. manutenção: {m.proxima_manutencao}h</span>
              <span>Intervalo: {m.intervalo_manutencao}h</span>
            </div>
            <div className="card-actions">
              <button className="btn btn-primary btn-sm" onClick={() => openMaintenance(m.id)}>🔧 Manutenções</button>
              <button className="btn btn-secondary btn-sm" onClick={() => handleEdit(m)}>✏️ Editar</button>
              <button className="btn btn-danger btn-sm" onClick={() => handleDelete(m.id)}>🗑️</button>
            </div>
          </div>
        ))
      )}
    </div>
  )
}

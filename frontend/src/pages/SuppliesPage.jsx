import { useState, useEffect } from 'react'
import { icons } from '../icons.jsx'
import api from '../api'

export default function SuppliesPage() {
  const [supplies, setSupplies] = useState([])
  const [loading, setLoading] = useState(true)
  const [showForm, setShowForm] = useState(false)
  const [editing, setEditing] = useState(null)
  const [showMovements, setShowMovements] = useState(null)
  const [movementsList, setMovementsList] = useState([])
  const [showMovForm, setShowMovForm] = useState(false)

  const [nome, setNome] = useState('')
  const [unidade, setUnidade] = useState('')
  const [qtdAtual, setQtdAtual] = useState('')
  const [qtdMinima, setQtdMinima] = useState('')

  const [movTipo, setMovTipo] = useState('entrada')
  const [movQtd, setMovQtd] = useState('')
  const [movObs, setMovObs] = useState('')

  const [error, setError] = useState('')

  const fetchSupplies = () => {
    api.get('/supplies')
      .then((res) => setSupplies(res.data))
      .finally(() => setLoading(false))
  }

  useEffect(() => { fetchSupplies() }, [])

  const resetForm = () => {
    setNome(''); setUnidade(''); setQtdAtual(''); setQtdMinima('')
    setEditing(null); setShowForm(false); setError('')
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    try {
      if (editing) {
        await api.put(`/supplies/${editing}`, {
          nome, unidade,
          quantidade_minima: parseFloat(qtdMinima),
        })
      } else {
        await api.post('/supplies', {
          nome, unidade,
          quantidade_atual: parseFloat(qtdAtual) || 0,
          quantidade_minima: parseFloat(qtdMinima) || 0,
        })
      }
      resetForm()
      fetchSupplies()
    } catch (err) {
      setError(err.response?.data?.detail || 'Erro ao salvar')
    }
  }

  const handleEdit = (s) => {
    setNome(s.nome); setUnidade(s.unidade)
    setQtdMinima(String(s.quantidade_minima))
    setEditing(s.id); setShowForm(true)
  }

  const openMovements = async (supplyId) => {
    setShowMovements(supplyId)
    const res = await api.get(`/movements/${supplyId}`)
    setMovementsList(res.data)
  }

  const handleMovSubmit = async (e) => {
    e.preventDefault()
    setError('')
    try {
      await api.post('/movements', {
        supply_id: showMovements,
        tipo: movTipo,
        quantidade: parseFloat(movQtd),
        observacao: movObs,
      })
      setMovTipo('entrada'); setMovQtd(''); setMovObs('')
      setShowMovForm(false)
      openMovements(showMovements)
      fetchSupplies()
    } catch (err) {
      setError(err.response?.data?.detail || 'Erro ao registrar movimentação')
    }
  }

  if (loading) return <div className="loading">Carregando...</div>

  if (showMovements) {
    const supply = supplies.find((s) => s.id === showMovements)
    return (
      <div>
        <div className="page-header">
          <h2>{icons.clipboard()} Movimentações — {supply?.nome}</h2>
          <button className="btn btn-secondary btn-sm" onClick={() => { setShowMovements(null); setShowMovForm(false) }}>
            {icons.left()} Voltar
          </button>
        </div>

        <div className="card" style={{ marginBottom: 16 }}>
          <strong>Estoque atual:</strong> {supply?.quantidade_atual} {supply?.unidade}
          &nbsp;&nbsp;|&nbsp;&nbsp;
          <strong>Mínimo:</strong> {supply?.quantidade_minima} {supply?.unidade}
        </div>

        <button className="btn btn-primary" style={{ marginBottom: 16 }} onClick={() => setShowMovForm(true)}>
          + Nova Movimentação
        </button>

        {showMovForm && (
          <div className="modal-overlay" onClick={() => setShowMovForm(false)}>
            <div className="modal" onClick={(e) => e.stopPropagation()}>
              <h2>Nova Movimentação</h2>
              {error && <div className="error-msg">{error}</div>}
              <form onSubmit={handleMovSubmit}>
                <div className="form-group">
                  <label>Tipo</label>
                  <select value={movTipo} onChange={(e) => setMovTipo(e.target.value)}>
                    <option value="entrada">{icons.down()} Entrada</option>
                    <option value="saida">{icons.up()} Saída</option>
                  </select>
                </div>
                <div className="form-group">
                  <label>Quantidade ({supply?.unidade})</label>
                  <input type="number" step="0.01" value={movQtd} onChange={(e) => setMovQtd(e.target.value)} required />
                </div>
                <div className="form-group">
                  <label>Observação</label>
                  <textarea rows={2} value={movObs} onChange={(e) => setMovObs(e.target.value)} />
                </div>
                <div className="btn-group">
                  <button type="submit" className="btn btn-primary">Registrar</button>
                  <button type="button" className="btn btn-secondary" onClick={() => setShowMovForm(false)}>Cancelar</button>
                </div>
              </form>
            </div>
          </div>
        )}

        {movementsList.length === 0 ? (
          <div className="empty-state">
            <p>Nenhuma movimentação registrada ainda.</p>
          </div>
        ) : (
          movementsList.map((m) => (
            <div key={m.id} className={`card ${m.tipo === 'entrada' ? 'status-ok' : 'status-atencao'}`}>
              <div className="card-header">
                <h3>{m.tipo === 'entrada' ? <>{icons.down()} Entrada</> : <>{icons.up()} Saída</>}</h3>
                <span className={`badge ${m.tipo === 'entrada' ? 'badge-ok' : 'badge-atencao'}`}>
                  {m.quantidade} {supply?.unidade}
                </span>
              </div>
              <div className="card-details">
                <span>{icons.calendar()} {new Date(m.data).toLocaleDateString('pt-BR')}</span>
                {m.observacao && <span>{m.observacao}</span>}
              </div>
            </div>
          ))
        )}
      </div>
    )
  }

  return (
    <div>
      <div className="page-header">
        <h2>{icons.box()} Estoque de Insumos</h2>
        <button className="btn btn-primary btn-sm" onClick={() => { resetForm(); setShowForm(true) }}>
          + Novo Insumo
        </button>
      </div>

      {showForm && (
        <div className="modal-overlay" onClick={resetForm}>
          <div className="modal" onClick={(e) => e.stopPropagation()}>
            <h2>{editing ? 'Editar Insumo' : 'Novo Insumo'}</h2>
            {error && <div className="error-msg">{error}</div>}
            <form onSubmit={handleSubmit}>
              <div className="form-group">
                <label>Nome</label>
                <input value={nome} onChange={(e) => setNome(e.target.value)} placeholder="Ex: Adubo NPK" required />
              </div>
              <div className="form-group">
                <label>Unidade</label>
                <select value={unidade} onChange={(e) => setUnidade(e.target.value)} required>
                  <option value="">Selecione...</option>
                  <option value="kg">Quilograma (kg)</option>
                  <option value="L">Litro (L)</option>
                  <option value="saco">Saco</option>
                  <option value="unidade">Unidade</option>
                  <option value="tonelada">Tonelada</option>
                </select>
              </div>
              {!editing && (
                <div className="form-group">
                  <label>Quantidade inicial</label>
                  <input type="number" step="0.01" value={qtdAtual} onChange={(e) => setQtdAtual(e.target.value)} placeholder="0" />
                </div>
              )}
              <div className="form-group">
                <label>Quantidade mínima (alerta)</label>
                <input type="number" step="0.01" value={qtdMinima} onChange={(e) => setQtdMinima(e.target.value)} placeholder="0" />
              </div>
              <div className="btn-group">
                <button type="submit" className="btn btn-primary">{editing ? 'Salvar' : 'Cadastrar'}</button>
                <button type="button" className="btn btn-secondary" onClick={resetForm}>Cancelar</button>
              </div>
            </form>
          </div>
        </div>
      )}

      {supplies.length === 0 ? (
        <div className="empty-state">
          <p>Nenhum insumo cadastrado.</p>
          <p>Clique em "+ Novo Insumo" para começar.</p>
        </div>
      ) : (
        supplies.map((s) => (
          <div key={s.id} className={`card ${s.status === 'OK' ? 'status-ok' : 'status-baixo'}`}>
            <div className="card-header">
              <h3>{s.nome}</h3>
              <span className={`badge ${s.status === 'OK' ? 'badge-ok' : 'badge-baixo'}`}>{s.status}</span>
            </div>
            <div className="card-details">
              <span>Estoque: {s.quantidade_atual} {s.unidade}</span>
              <span>Mínimo: {s.quantidade_minima} {s.unidade}</span>
            </div>
            <div className="card-actions">
              <button className="btn btn-primary btn-sm" onClick={() => openMovements(s.id)}>{icons.clipboardWhite()} Movimentações</button>
              <button className="btn btn-secondary btn-sm" onClick={() => handleEdit(s)}>{icons.edit()} Editar</button>
            </div>
          </div>
        ))
      )}
    </div>
  )
}

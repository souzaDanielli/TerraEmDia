import { useState, useEffect } from 'react'
import { icons } from '../icons.jsx'
import { Link } from 'react-router-dom'
import api from '../api'

export default function DashboardPage() {
  const [machines, setMachines] = useState([])
  const [supplies, setSupplies] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    Promise.all([api.get('/machines'), api.get('/supplies')])
      .then(([mRes, sRes]) => {
        setMachines(mRes.data)
        setSupplies(sRes.data)
      })
      .finally(() => setLoading(false))
  }, [])

  if (loading) return <div className="loading">Carregando...</div>

  const alertMachines = machines.filter((m) => m.status !== 'OK')
  const alertSupplies = supplies.filter((s) => s.status !== 'OK')

  return (
    <div>
      <h2 style={{ marginBottom: 20, color: '#2e7d32' }}>Painel Geral</h2>

      {/* Máquinas em alerta */}
      <div className="alert-section">
        <h2>{icons.alert()} Máquinas que precisam de atenção</h2>
        {alertMachines.length === 0 ? (
          <div className="card status-ok">
            <p>{icons.check()} Todas as máquinas estão em dia!</p>
          </div>
        ) : (
          alertMachines.map((m) => (
            <div key={m.id} className={`card status-${m.status === 'Atenção' ? 'atencao' : 'proximo'}`}>
              <div className="card-header">
                <h3>{m.nome}</h3>
                <span className={`badge badge-${m.status === 'Atenção' ? 'atencao' : 'proximo'}`}>
                  {m.status}
                </span>
              </div>
              <div className="card-details">
                <span>Tipo: {m.tipo}</span>
                <span>Horímetro: {m.horimetro_atual}h</span>
                <span>Próx. manutenção: {m.proxima_manutencao}h</span>
              </div>
            </div>
          ))
        )}
      </div>

      {/* Insumos com estoque baixo */}
      <div className="alert-section">
        <h2>{icons.box()} Insumos com estoque baixo</h2>
        {alertSupplies.length === 0 ? (
          <div className="card status-ok">
            <p>{icons.check()} Estoque de todos os insumos está OK!</p>
          </div>
        ) : (
          alertSupplies.map((s) => (
            <div key={s.id} className="card status-baixo">
              <div className="card-header">
                <h3>{s.nome}</h3>
                <span className="badge badge-baixo">Estoque Baixo</span>
              </div>
              <div className="card-details">
                <span>Atual: {s.quantidade_atual} {s.unidade}</span>
                <span>Mínimo: {s.quantidade_minima} {s.unidade}</span>
              </div>
            </div>
          ))
        )}
      </div>

      {/* Quick links */}
      {machines.length === 0 && supplies.length === 0 && (
        <div className="empty-state">
          <p>{icons.hand()} Bem-vindo ao Terra em Dia!</p>
          <p style={{ marginTop: 8 }}>
            Comece cadastrando suas <Link to="/machines" style={{ color: '#2e7d32' }}>máquinas</Link> e <Link to="/supplies" style={{ color: '#2e7d32' }}>insumos</Link>.
          </p>
        </div>
      )}
    </div>
  )
}

import { Routes, Route, Navigate, NavLink } from 'react-router-dom'
import { icons } from './icons.jsx'
import { useAuth } from './context/AuthContext'
import LoginPage from './pages/LoginPage'
import RegisterPage from './pages/RegisterPage'
import DashboardPage from './pages/DashboardPage'
import MachinesPage from './pages/MachinesPage'
import SuppliesPage from './pages/SuppliesPage'
import { useEffect, useState } from 'react'
import api from './api'

// Overlay de carregamento global
function GlobalLoadingOverlay({ children }) {
  const [apiReady, setApiReady] = useState(false)
  const [erro, setErro] = useState(null)

  useEffect(() => {
    let cancelled = false
    
    async function checkApi() {
      try {
        // Testa a conexão com o backend
        await api.get('/')
        if (!cancelled) {
          setApiReady(true)
        }
      } catch (e) {
        if (!cancelled) {
          setErro('Aguardando backend iniciar...')
          setTimeout(checkApi, 2000)
        }
      }
    }

    checkApi()
    return () => { cancelled = true }
  }, [])

  if (!apiReady) {
    return (
      <div style={{
        position: 'fixed', zIndex: 9999, inset: 0, background: 'rgba(255,255,255,0.95)',
        display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center',
        fontSize: '22px', color: '#2e7d32', fontWeight: 500, fontFamily: 'sans-serif'
      }}>
        <div style={{ marginBottom: '16px' }}>
          <span role="img" aria-label="tractor" style={{ fontSize: '48px' }}>🚜</span>
        </div>
        <div>{erro || 'Carregando sistema...'}</div>
        <div style={{ marginTop: '24px', fontSize: '14px', color: '#888' }}>
          Aguarde, inicializando API...
        </div>
      </div>
    )
  }

  return children
}

function PrivateRoute({ children }) {
  const { user, loading } = useAuth()
  if (loading) return <div className="loading">Carregando permissões...</div>
  return user ? children : <Navigate to="/login" />
}

function Layout({ children }) {
  const { logout } = useAuth()

  return (
    <>
      <header className="app-header">
        <div className="titulo">
          <div>{icons.seed()}</div> <h1>Terra em Dia</h1>
        </div>
        <nav>
          <NavLink to="/" className={({ isActive }) => isActive ? 'active' : ''}>Início</NavLink>
          <NavLink to="/machines" className={({ isActive }) => isActive ? 'active' : ''}>Máquinas</NavLink>
          <NavLink to="/supplies" className={({ isActive }) => isActive ? 'active' : ''}>Estoque</NavLink>
          <button className="btn-logout" onClick={logout}>Sair</button>
        </nav>
      </header>
      <main className="container">
        {children}
      </main>
    </>
  )
}

export default function App() {
  return (
    <GlobalLoadingOverlay>
      <Routes>
        <Route path="/login" element={<LoginPage />} />
        <Route path="/register" element={<RegisterPage />} />
        
        <Route path="/" element={
          <PrivateRoute>
            <Layout><DashboardPage /></Layout>
          </PrivateRoute>
        } />
        
        <Route path="/machines" element={
          <PrivateRoute>
            <Layout><MachinesPage /></Layout>
          </PrivateRoute>
        } />
        
        <Route path="/supplies" element={
          <PrivateRoute>
            <Layout><SuppliesPage /></Layout>
          </PrivateRoute>
        } />
        
        <Route path="*" element={<Navigate to="/" />} />
      </Routes>
    </GlobalLoadingOverlay>
  )
}
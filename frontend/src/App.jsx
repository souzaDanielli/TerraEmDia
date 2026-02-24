import { Routes, Route, Navigate, NavLink } from 'react-router-dom'
import { useAuth } from './context/AuthContext'
import LoginPage from './pages/LoginPage'
import RegisterPage from './pages/RegisterPage'
import DashboardPage from './pages/DashboardPage'
import MachinesPage from './pages/MachinesPage'
import SuppliesPage from './pages/SuppliesPage'

function PrivateRoute({ children }) {
  const { user, loading } = useAuth()
  if (loading) return <div className="loading">Carregando...</div>
  return user ? children : <Navigate to="/login" />
}

function Layout({ children }) {
  const { user, logout } = useAuth()

  return (
    <>
      <header className="app-header">
        <h1>🌱 Terra em Dia</h1>
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
  )
}

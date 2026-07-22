import { useEffect, useState } from 'react'
import axios from 'axios'
import './index.css'

export default function App() {
  const [health, setHealth] = useState(null)
  const [techStack, setTechStack] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    // Fetch Backend Health Status
    axios.get('/api/health')
      .then(res => {
        setHealth(res.data)
        setLoading(false)
      })
      .catch(err => {
        console.error('Failed to reach backend:', err)
        setError('Backend server not responding. Run `npm run server` or `npm run dev`.')
        setLoading(false)
      })

    // Fetch Tech Stack test items
    axios.get('/api/test')
      .then(res => setTechStack(res.data.items || []))
      .catch(() => {})
  }, [])

  return (
    <div className="card">
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <h1 style={{ margin: 0, fontSize: '1.75rem', fontWeight: 700 }}>
          🚀 MERN Stack Development Environment
        </h1>
        <span className={`badge ${health ? 'badge-success' : 'badge-warning'}`}>
          {loading ? 'Connecting...' : health ? 'Server Connected' : 'Server Offline'}
        </span>
      </div>

      <p style={{ color: '#9ca3af', marginTop: '0.5rem' }}>
        Your local monorepo development environment is configured and ready.
      </p>

      {error && (
        <div style={{ padding: '1rem', background: 'rgba(239, 68, 68, 0.1)', border: '1px solid rgba(239, 68, 68, 0.3)', borderRadius: '8px', color: '#fca5a5', marginTop: '1rem' }}>
          ⚠️ {error}
        </div>
      )}

      {health && (
        <div style={{ marginTop: '1.5rem', background: 'rgba(15, 23, 42, 0.4)', padding: '1rem', borderRadius: '8px' }}>
          <p style={{ margin: 0, fontSize: '0.95rem' }}><strong>Server Response:</strong> {health.message}</p>
          <p style={{ margin: '0.25rem 0 0 0', fontSize: '0.85rem', color: '#9ca3af' }}>
            MongoDB Status: <span style={{ color: health.dbState === 'connected' ? '#34d399' : '#fbbf24' }}>{health.dbState}</span>
          </p>
        </div>
      )}

      <h2 style={{ fontSize: '1.2rem', marginTop: '2rem', marginBottom: '0.5rem' }}>Configured Stack Modules</h2>
      <div className="grid">
        {techStack.length > 0 ? (
          techStack.map(item => (
            <div key={item.id} className="grid-item">
              <h3>{item.name}</h3>
              <p>{item.role}</p>
            </div>
          ))
        ) : (
          <>
            <div className="grid-item">
              <h3>🍃 MongoDB</h3>
              <p>Mongoose ORM configured in server/server.js</p>
            </div>
            <div className="grid-item">
              <h3>⚡ Express</h3>
              <p>Node REST API configured on port 5000</p>
            </div>
            <div className="grid-item">
              <h3>⚛️ React</h3>
              <p>Vite 6 SPA configured in client/</p>
            </div>
            <div className="grid-item">
              <h3>🟢 Node.js</h3>
              <p>Orchestrated with root concurrently script</p>
            </div>
          </>
        )}
      </div>

      <div style={{ marginTop: '2rem', padding: '1rem', background: 'rgba(0, 0, 0, 0.2)', borderRadius: '8px', fontSize: '0.85rem', color: '#9ca3af' }}>
        <strong>Quick Commands:</strong>
        <code style={{ display: 'block', background: '#090d16', padding: '0.5rem', borderRadius: '4px', marginTop: '0.5rem', color: '#38bdf8' }}>
          npm run dev       # Starts backend (port 5000) & frontend (port 5173) simultaneously
        </code>
      </div>
    </div>
  )
}

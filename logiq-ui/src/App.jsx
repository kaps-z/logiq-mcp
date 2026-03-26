import { useState, useEffect } from 'react'
import { ShieldAlert } from 'lucide-react'
import LogTable from './components/LogTable'
import AIFixModal from './components/AIFixModal'
import LogGenerator from './components/LogGenerator'

function App() {
  const [logs, setLogs] = useState([])
  const [loading, setLoading] = useState(false)
  const [selectedLog, setSelectedLog] = useState(null)
  
  const fetchLogs = async () => {
    setLoading(true)
    try {
      const res = await fetch('http://localhost:3000/api/logs?limit=20')
      const data = await res.json()
      setLogs(data.data || [])
    } catch (err) {
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchLogs()
  }, [])

  return (
    <div className="app-container">
      <header className="header">
        <h1 className="title"><ShieldAlert size={36} color="#58a6ff" /> LogIQ Central</h1>
        <button className="btn btn-primary" onClick={fetchLogs}>
          Refresh Logs
        </button>
      </header>

      <div className="glass-panel">
        <h3 style={{marginBottom: '1rem', color: 'var(--text-secondary)'}}>Simulate Errors</h3>
        <LogGenerator onLogCreated={fetchLogs} />
      </div>

      <div className="glass-panel" style={{ flex: 1 }}>
        <h3 style={{marginBottom: '1rem', color: 'var(--text-secondary)'}}>Application Logs</h3>
        <LogTable logs={logs} loading={loading} onDebugClick={setSelectedLog} />
      </div>

      {selectedLog && (
        <AIFixModal 
          log={selectedLog} 
          onClose={() => setSelectedLog(null)} 
        />
      )}
    </div>
  )
}

export default App

import { Zap } from 'lucide-react'

export default function LogTable({ logs, loading, onDebugClick }) {
  if (loading && logs.length === 0) return <p>Loading logs...</p>
  if (logs.length === 0) return <p style={{color: 'var(--text-secondary)'}}>No logs detected in the system.</p>

  const getTagClass = (level) => {
    if (level === 'ERROR') return 'tag-error'
    if (level === 'WARN') return 'tag-warn'
    return 'tag-info'
  }

  return (
    <div className="table-wrapper">
      <table>
        <thead>
          <tr>
            <th>Level</th>
            <th>Service</th>
            <th>Message</th>
            <th>Time</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {logs.map(log => (
            <tr key={log.id}>
              <td><span className={`tag ${getTagClass(log.level)}`}>{log.level}</span></td>
              <td style={{fontWeight: 500}}>{log.service}</td>
              <td style={{color: 'var(--text-secondary)'}}>{log.message}</td>
              <td style={{color: 'var(--text-secondary)', fontSize: '0.85rem'}}>
                {new Date(log.timestamp).toLocaleTimeString()}
              </td>
              <td>
                {log.level === 'ERROR' && (
                  <button 
                    className="btn btn-danger" 
                    onClick={() => onDebugClick(log)}
                    style={{ padding: '0.3rem 0.6rem', fontSize: '0.8rem' }}
                  >
                    <Zap size={14} /> AI Debug
                  </button>
                )}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}

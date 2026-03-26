import { useState } from 'react'
import { PlusCircle } from 'lucide-react'

export default function LogGenerator({ onLogCreated }) {
  const [level, setLevel] = useState('ERROR')
  const [service, setService] = useState('auth-service')
  const [message, setMessage] = useState('Database connection timeout')
  const [creating, setCreating] = useState(false)

  const handleSubmit = async (e) => {
    e.preventDefault()
    setCreating(true)
    try {
      await fetch('http://localhost:3000/api/logs', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ level, service, message })
      })
      onLogCreated()
    } catch(err) {
      console.error(err)
    } finally {
      setCreating(false)
    }
  }

  return (
    <form className="form-row" onSubmit={handleSubmit}>
      <div className="form-group">
        <label>Level</label>
        <select className="form-control" value={level} onChange={e => setLevel(e.target.value)}>
          <option value="ERROR">ERROR</option>
          <option value="WARN">WARN</option>
          <option value="INFO">INFO</option>
        </select>
      </div>
      <div className="form-group">
        <label>Service</label>
        <input className="form-control" value={service} onChange={e => setService(e.target.value)} />
      </div>
      <div className="form-group" style={{ flex: 2 }}>
        <label>Message</label>
        <input className="form-control" value={message} onChange={e => setMessage(e.target.value)} />
      </div>
      <button className="btn btn-primary" type="submit" disabled={creating} style={{ height: '38px' }}>
        <PlusCircle size={18} /> Inject
      </button>
    </form>
  )
}

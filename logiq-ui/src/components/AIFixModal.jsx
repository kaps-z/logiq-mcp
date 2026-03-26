import { useState, useEffect } from 'react'
import { Sparkles, CheckCircle, XCircle } from 'lucide-react'

export default function AIFixModal({ log, onClose }) {
  const [loading, setLoading] = useState(false)
  const [filePath, setFilePath] = useState('/tmp/mock.js')
  const [preview, setPreview] = useState(null)
  const [error, setError] = useState(null)
  const [applying, setApplying] = useState(false)

  // Normally, we'd map the service to a primary file mathematically or via agent logic.
  // For this UI demo, we provide a quick default path targeting our sample architecture.
  useEffect(() => {
    const root = '/home/kapil/project/personal/logiq-mcp'
    if (log.service === 'auth-service') setFilePath(`${root}/auth-service/db.js`)
    else if (log.service === 'node-service') setFilePath(`${root}/node-service/src/index.js`)
    else if (log.service === 'db') setFilePath(`${root}/node-service/src/db.js`)
    else setFilePath(`${root}/cli/agent.py`) // Fallback to an existing file rather than a mock path
  }, [log])

  const handleGeneratePreview = async () => {
    setLoading(true)
    setError(null)
    try {
      const res = await fetch('http://localhost:8000/api/suggest-fix', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ service: log.service, file_path: filePath })
      })
      const data = await res.json()
      if (!res.ok) throw new Error(data.detail || data.error || 'Failed to generate fix')
      setPreview(data)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  const handleApply = async () => {
    if (!preview) return
    setApplying(true)
    try {
      const res = await fetch('http://localhost:8000/api/apply-fix', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          file_path: preview.file_path,
          updated_code: preview.updated_code,
          changes_summary: preview.changes_summary
        })
      })
      const data = await res.json()
      if (!res.ok) throw new Error(data.detail)
      alert(data.message)
      onClose()
    } catch(err) {
      setError(err.message)
      setApplying(false)
    }
  }

  return (
    <div className="modal-overlay">
      <div className="modal-content">
        <div className="modal-header">
          <h2 style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <Sparkles color="var(--accent-color)" /> AI Triage Session
          </h2>
          <button className="btn" onClick={onClose}><XCircle size={18} /></button>
        </div>
        
        <div className="modal-body">
          <div className="summary-box">
             Analyzing Event: <strong>{log.level} on {log.service}</strong><br/>
             Target File Path: <input 
               className="form-control" 
               style={{width: '60%', marginLeft: '1rem', marginTop: '0.5rem'}}
               value={filePath} 
               onChange={e => setFilePath(e.target.value)} 
             />
          </div>

          {!preview && !loading && (
             <button className="btn btn-primary" onClick={handleGeneratePreview} style={{ alignSelf: 'center', padding: '1rem 2rem' }}>
                Generate Structural Fix Preview
             </button>
          )}

          {loading && <p style={{textAlign: 'center', color: 'var(--accent-color)'}}>AI is reading files and synthesizing fix patterns...</p>}
          {error && <p style={{ color: 'var(--error-color)', padding: '1rem', background: 'rgba(248,81,73,0.1)' }}>{error}</p>}

          {preview && (
            <>
              <div className="summary-box" style={{ background: 'rgba(35, 134, 54, 0.1)', borderColor: 'rgba(35, 134, 54, 0.4)' }}>
                <strong>AI Plan (Confidence: {(preview.confidence_score * 100).toFixed(0)}%): </strong> 
                {preview.changes_summary}
              </div>
              
              <div className="code-comparison">
                <div className="code-panel">
                  <h4>Original Code</h4>
                  <pre>{preview.original_code}</pre>
                </div>
                <div className="code-panel">
                  <h4>Proposed AI Patch</h4>
                  <pre>{preview.updated_code}</pre>
                </div>
              </div>
            </>
          )}

        </div>

        {preview && (
          <div className="modal-footer">
            <button className="btn" onClick={onClose} disabled={applying}>Deny / Cancel</button>
            <button className="btn btn-success" onClick={handleApply} disabled={applying}>
              <CheckCircle size={18} /> {applying ? 'Writing strictly to disk...' : 'Approve & Apply File Patch'}
            </button>
          </div>
        )}
      </div>
    </div>
  )
}

import { useState } from 'react'

function App() {
  const [text, setText] = useState('')
  const [url, setUrl] = useState('')
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const handleAnalyze = async (e) => {
    e.preventDefault();
    if (!text && !url) {
      setError("Please provide at least text or a URL to check.");
      return;
    }
    
    setError('');
    setLoading(true);
    setResult(null);

    try {
      const response = await fetch('http://127.0.0.1:5000/analyze', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text, url }),
      });

      if (!response.ok) {
        throw new Error('Analysis failed');
      }

      const data = await response.json();
      setResult(data);
    } catch (err) {
      setError('Failed to connect to the backend server. Make sure it is running!');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <h1>FraudShield AI</h1>
      <p className="subtitle">Detect phishing, scams, and malicious URLs</p>

      <form onSubmit={handleAnalyze}>
        <div className="form-group">
          <label htmlFor="textInput">Suspicious Text or Message</label>
          <textarea 
            id="textInput"
            value={text}
            onChange={(e) => setText(e.target.value)}
            placeholder="Paste email, SMS, or message content here..."
          />
        </div>

        <div className="form-group">
          <label htmlFor="urlInput">Suspicious URL</label>
          <input 
            type="text" 
            id="urlInput"
            value={url}
            onChange={(e) => setUrl(e.target.value)}
            placeholder="https://example.com"
          />
        </div>

        {error && <div className="error-message">{error}</div>}

        <button type="submit" disabled={loading}>
          {loading ? 'Analyzing...' : 'Check Safety'}
        </button>
      </form>

      {result && (
        <div className={`result-box ${result.risk_level}`}>
          <div className="status-icon">
            {result.risk_level === 'LOW' && '✅'}
            {result.risk_level === 'MEDIUM' && '⚠️'}
            {result.risk_level === 'HIGH' && '🚨'}
          </div>
          <h2 className="status-title">
            {result.risk_level === 'LOW' && 'Safe'}
            {result.risk_level === 'MEDIUM' && 'Be Careful'}
            {result.risk_level === 'HIGH' && 'Danger!'}
          </h2>
          <p className="status-desc">{result.warning_message}</p>
        </div>
      )}
    </div>
  )
}

export default App

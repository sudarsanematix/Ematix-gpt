import { useState } from 'react';
import './index.css';

const API_BASE = 'http://localhost:8000/api';

function App() {
  const [activeTab, setActiveTab] = useState('research');
  
  return (
    <div className="app-container">
      <header>
        <h1>Nexus AI</h1>
        <p>Advanced Multi-Agent Intelligence System</p>
      </header>

      <div className="tabs">
        <button 
          className={`tab-btn ${activeTab === 'research' ? 'active' : ''}`}
          onClick={() => setActiveTab('research')}
        >
          Research Agent
        </button>
        <button 
          className={`tab-btn ${activeTab === 'chat' ? 'active' : ''}`}
          onClick={() => setActiveTab('chat')}
        >
          Chatbot
        </button>
        <button 
          className={`tab-btn ${activeTab === 'rag' ? 'active' : ''}`}
          onClick={() => setActiveTab('rag')}
        >
          Document Q&A
        </button>
        <button 
          className={`tab-btn ${activeTab === 'image' ? 'active' : ''}`}
          onClick={() => setActiveTab('image')}
        >
          Image Studio
        </button>
        <button 
          className={`tab-btn ${activeTab === 'web' ? 'active' : ''}`}
          onClick={() => setActiveTab('web')}
        >
          Web Search
        </button>
      </div>

      <main className="panel">
        {activeTab === 'research' && <ResearchTab />}
        {activeTab === 'chat' && <ChatTab />}
        {activeTab === 'rag' && <RagTab />}
        {activeTab === 'image' && <ImageTab />}
        {activeTab === 'web' && <WebTab />}
      </main>
    </div>
  );
}

function ResearchTab() {
  const [topic, setTopic] = useState('');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleResearch = async () => {
    if (!topic) return;
    setLoading(true);
    try {
      const res = await fetch(`${API_BASE}/research`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ topic })
      });
      const data = await res.json();
      setResult(data);
    } catch (err) {
      console.error(err);
      setResult({ error: 'Failed to complete research.' });
    }
    setLoading(false);
  };

  return (
    <div>
      <h2>Deep Research Agent</h2>
      <p style={{ color: 'var(--text-muted)', marginBottom: '1rem' }}>Enter a topic for our AI to deeply research and analyze.</p>
      
      <div className="input-group">
        <input 
          type="text" 
          value={topic} 
          onChange={(e) => setTopic(e.target.value)} 
          placeholder="e.g., Quantum Computing Applications..."
          onKeyDown={(e) => e.key === 'Enter' && handleResearch()}
        />
        <button className="primary" onClick={handleResearch} disabled={loading}>
          {loading ? 'Researching...' : 'Start'}
        </button>
      </div>

      {loading && <div style={{ textAlign: 'center', marginTop: '3rem' }}><div className="loader"></div></div>}
      
      {result && !loading && (
        <div className="result-box">
          <h3>Research Output:</h3>
          <p>{result.research}</p>
          <hr style={{ margin: '2rem 0', borderColor: 'var(--border-color)' }} />
          <h3>Analysis Output:</h3>
          <p>{result.analysis}</p>
        </div>
      )}
    </div>
  );
}

function ChatTab() {
  const [msg, setMsg] = useState('');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleChat = async () => {
    if (!msg) return;
    setLoading(true);
    try {
      const res = await fetch(`${API_BASE}/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: msg })
      });
      const data = await res.json();
      setResult(data.result);
    } catch (err) {
      setResult('Failed to connect to chatbot.');
    }
    setLoading(false);
  };

  return (
    <div>
      <h2>General Chatbot</h2>
      <div className="input-group">
        <input 
          type="text" 
          value={msg} 
          onChange={(e) => setMsg(e.target.value)} 
          placeholder="Ask me anything..."
          onKeyDown={(e) => e.key === 'Enter' && handleChat()}
        />
        <button className="primary" onClick={handleChat} disabled={loading}>
          Send
        </button>
      </div>
      {loading && <div style={{ textAlign: 'center', marginTop: '2rem' }}><div className="loader"></div></div>}
      {result && !loading && <div className="result-box">{result}</div>}
    </div>
  );
}

function RagTab() {
  const [file, setFile] = useState(null);
  const [question, setQuestion] = useState('');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleUpload = async () => {
    if (!file || !question) return;
    setLoading(true);
    const formData = new FormData();
    formData.append('file', file);
    formData.append('question', question);

    try {
      const res = await fetch(`${API_BASE}/rag`, {
        method: 'POST',
        body: formData
      });
      const data = await res.json();
      setResult(data.result);
    } catch (err) {
      setResult('Failed to process document.');
    }
    setLoading(false);
  };

  return (
    <div>
      <h2>Document Q&A (RAG)</h2>
      <div className="input-group" style={{ flexDirection: 'column' }}>
        <div className="file-upload">
          <div className="file-upload-btn">
            📁 {file ? file.name : 'Choose PDF Document'}
          </div>
          <input type="file" accept=".pdf" onChange={(e) => setFile(e.target.files[0])} />
        </div>
        <div className="input-group" style={{ marginTop: '0' }}>
          <input 
            type="text" 
            value={question} 
            onChange={(e) => setQuestion(e.target.value)} 
            placeholder="Ask a question about the document..."
          />
          <button className="primary" onClick={handleUpload} disabled={loading || !file}>
            Ask Document
          </button>
        </div>
      </div>
      {loading && <div style={{ textAlign: 'center', marginTop: '2rem' }}><div className="loader"></div></div>}
      {result && !loading && <div className="result-box">{result}</div>}
    </div>
  );
}

function ImageTab() {
  const [prompt, setPrompt] = useState('');
  const [imageSrc, setImageSrc] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleGenerate = async () => {
    if (!prompt) return;
    setLoading(true);
    try {
      const res = await fetch(`${API_BASE}/image`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query: prompt })
      });
      const blob = await res.blob();
      setImageSrc(URL.createObjectURL(blob));
    } catch (err) {
      console.error(err);
    }
    setLoading(false);
  };

  return (
    <div>
      <h2>Image Generation Studio</h2>
      <div className="input-group">
        <input 
          type="text" 
          value={prompt} 
          onChange={(e) => setPrompt(e.target.value)} 
          placeholder="Describe the image you want to create..."
          onKeyDown={(e) => e.key === 'Enter' && handleGenerate()}
        />
        <button className="primary" onClick={handleGenerate} disabled={loading}>
          Generate
        </button>
      </div>
      <div className="image-preview">
        {loading ? <div className="loader"></div> : (imageSrc ? <img src={imageSrc} alt="Generated" /> : <p style={{color: 'var(--text-muted)'}}>Your masterpiece will appear here</p>)}
      </div>
    </div>
  );
}

function WebTab() {
  const [query, setQuery] = useState('');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleSearch = async () => {
    if (!query) return;
    setLoading(true);
    try {
      const res = await fetch(`${API_BASE}/web-search`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query })
      });
      const data = await res.json();
      setResult(data.result);
    } catch (err) {
      setResult('Failed to perform web search.');
    }
    setLoading(false);
  };

  return (
    <div>
      <h2>Web Search Agent</h2>
      <div className="input-group">
        <input 
          type="text" 
          value={query} 
          onChange={(e) => setQuery(e.target.value)} 
          placeholder="Search the web..."
          onKeyDown={(e) => e.key === 'Enter' && handleSearch()}
        />
        <button className="primary" onClick={handleSearch} disabled={loading}>
          Search
        </button>
      </div>
      {loading && <div style={{ textAlign: 'center', marginTop: '2rem' }}><div className="loader"></div></div>}
      {result && !loading && <div className="result-box">{result}</div>}
    </div>
  );
}

export default App;

import React, { useState } from 'react';
import axios from 'axios';

function App() {
  const [query, setQuery] = useState('');
  const [summary, setSummary] = useState('');
  const [file, setFile] = useState<File | null>(null);
  const [uploadStatus, setUploadStatus] = useState<string>('');

  const handleSearch = async () => {
    try {
      const response = await axios.post('http://localhost:5001/api/query', { query });
      setSummary(response.data.summary);
    } catch (error) {
      console.error('Error fetching summary:', error);
    }
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setUploadStatus('');
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0]);
    } else {
      setFile(null);
    }
  };

  const handleUpload = async () => {
    if (!file) return;
    try {
      setUploadStatus('Uploading...');
      const formData = new FormData();
      formData.append('file', file);
      const res = await axios.post('http://localhost:5001/api/upload', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
      setUploadStatus(res.data?.message || 'Uploaded');
    } catch (err: any) {
      const msg = err?.response?.data?.error || 'Upload failed';
      setUploadStatus(msg);
    }
  };

  return (
    <div style={{
      minHeight: '100vh',
      background: 'linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%)',
      padding: '2rem',
      fontFamily: 'system-ui, -apple-system, sans-serif'
    }}>
      <div style={{
        maxWidth: '800px',
        margin: '0 auto',
        background: 'linear-gradient(135deg, #0a0a0a 0%, #1a1a1a 100%)',
        borderRadius: '24px',
        padding: '3rem',
        boxShadow: '0 20px 60px rgba(0, 0, 0, 0.8)',
        border: '1px solid #333'
      }}>
        <h1 style={{
          background: 'linear-gradient(135deg, #ff0000 0%, #cc0000 100%)',
          WebkitBackgroundClip: 'text',
          WebkitTextFillColor: 'transparent',
          fontSize: '3rem',
          marginBottom: '2rem',
          textAlign: 'center',
          fontWeight: '800'
        }}>RAG Search</h1>

        <div style={{ marginBottom: '2rem' }}>
          <label htmlFor="file" style={{
            display: 'block',
            marginBottom: '0.75rem',
            fontWeight: '600',
            color: '#999',
            fontSize: '0.95rem'
          }}>Upload a document (PDF, TXT, CSV, DOCX, JSON, XLS/XLSX)</label>
          <input
            id="file"
            type="file"
            accept=".pdf,.txt,.csv,.docx,.json,.xls,.xlsx"
            onChange={handleFileChange}
            style={{
              width: '100%',
              padding: '0.75rem',
              border: '2px solid #333',
              borderRadius: '12px',
              fontSize: '1rem',
              transition: 'all 0.3s',
              cursor: 'pointer',
              background: '#1a1a1a',
              color: '#ccc'
            }}
          />
        </div>
        <div style={{ display: 'flex', gap: '1rem', alignItems: 'center', marginBottom: '2rem' }}>
          <button onClick={handleUpload} disabled={!file} style={{
            background: file ? 'linear-gradient(135deg, #ff0000 0%, #8b0000 100%)' : '#2d2d2d',
            color: file ? 'white' : '#666',
            border: 'none',
            padding: '0.875rem 2rem',
            borderRadius: '12px',
            fontSize: '1rem',
            fontWeight: '600',
            cursor: file ? 'pointer' : 'not-allowed',
            transition: 'all 0.3s',
            boxShadow: file ? '0 4px 15px rgba(255, 0, 0, 0.4)' : 'none',
            transform: 'translateY(0)'
          }} onMouseEnter={(e) => {
            if (file) e.currentTarget.style.transform = 'translateY(-2px)';
          }} onMouseLeave={(e) => {
            e.currentTarget.style.transform = 'translateY(0)';
          }}>Upload</button>
          <span style={{ color: '#999', fontSize: '0.9rem' }}>{uploadStatus}</span>
        </div>

        <div style={{ marginBottom: '2rem' }}>
          <label htmlFor="query" style={{
            display: 'block',
            marginBottom: '0.75rem',
            fontWeight: '600',
            color: '#999',
            fontSize: '0.95rem'
          }}>Enter your query</label>
          <input
            id="query"
            type="text"
            placeholder="Ask anything..."
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            style={{
              width: '100%',
              padding: '1rem',
              border: '2px solid #333',
              borderRadius: '12px',
              fontSize: '1rem',
              transition: 'all 0.3s',
              outline: 'none',
              background: '#1a1a1a',
              color: '#fff'
            }}
            onFocus={(e) => e.currentTarget.style.borderColor = '#ff0000'}
            onBlur={(e) => e.currentTarget.style.borderColor = '#333'}
          />
        </div>
        <div style={{ marginBottom: '2rem' }}>
          <button onClick={handleSearch} style={{
            background: 'linear-gradient(135deg, #ff0000 0%, #8b0000 100%)',
            color: 'white',
            border: 'none',
            padding: '0.875rem 2rem',
            borderRadius: '12px',
            fontSize: '1rem',
            fontWeight: '600',
            cursor: 'pointer',
            transition: 'all 0.3s',
            boxShadow: '0 4px 15px rgba(255, 0, 0, 0.4)',
            transform: 'translateY(0)',
            width: '100%'
          }} onMouseEnter={(e) => {
            e.currentTarget.style.transform = 'translateY(-2px)';
            e.currentTarget.style.boxShadow = '0 6px 20px rgba(255, 0, 0, 0.5)';
          }} onMouseLeave={(e) => {
            e.currentTarget.style.transform = 'translateY(0)';
            e.currentTarget.style.boxShadow = '0 4px 15px rgba(255, 0, 0, 0.4)';
          }}>Search</button>
        </div>

        <div style={{
          background: 'linear-gradient(135deg, #1a1a1a 0%, #0a0a0a 100%)',
          borderRadius: '16px',
          padding: '1.5rem',
          border: '2px solid #333'
        }}>
          <div style={{
            fontWeight: '700',
            marginBottom: '1rem',
            fontSize: '1.25rem',
            background: 'linear-gradient(135deg, #ff0000 0%, #cc0000 100%)',
            WebkitBackgroundClip: 'text',
            WebkitTextFillColor: 'transparent'
          }}>Summary</div>
          <div style={{
            whiteSpace: 'pre-wrap',
            overflowWrap: 'anywhere',
            color: '#ccc',
            lineHeight: '1.7',
            fontSize: '1rem'
          }}>{summary || 'No summary yet. Try a search.'}</div>
        </div>
      </div>
    </div>
  );
}

export default App;
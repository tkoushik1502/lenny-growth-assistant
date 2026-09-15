import React, { useState, useEffect, useRef } from 'react';
import DOMPurify from 'dompurify';
import { X, Code, Eye, Copy, Download, ShieldCheck, Check } from 'lucide-react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';

export default function ArtifactViewer({ artifact, onClose }) {
  const [activeTab, setActiveTab] = useState('preview'); // 'preview' or 'code'
  const [copied, setCopied] = useState(false);
  const iframeRef = useRef(null);

  useEffect(() => {
    if (activeTab === 'preview' && artifact?.type === 'html' && iframeRef.current) {
      // Security Isolation: Sanitize HTML content with DOMPurify
      const sanitizedHtml = DOMPurify.sanitize(artifact.content, {
        ADD_TAGS: ['style', 'script'],
        ADD_ATTR: ['style', 'class', 'id']
      });

      const doc = iframeRef.current.contentDocument;
      if (doc) {
        doc.open();
        doc.write(`
          <!DOCTYPE html>
          <html>
            <head>
              <meta charset="utf-8">
              <style>
                body { margin: 0; padding: 16px; background: #0f172a; color: #f8fafc; font-family: system-ui, -apple-system, sans-serif; }
              </style>
            </head>
            <body>
              ${sanitizedHtml}
            </body>
          </html>
        `);
        doc.close();
      }
    }
  }, [artifact, activeTab]);

  if (!artifact) return null;

  const handleCopy = () => {
    navigator.clipboard.writeText(artifact.content);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const handleDownload = () => {
    const blob = new Blob([artifact.content], { type: artifact.type === 'html' ? 'text/html' : 'text/markdown' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `${artifact.title.toLowerCase().replace(/\s+/g, '_')}.${artifact.type === 'html' ? 'html' : 'md'}`;
    a.click();
  };

  return (
    <div className="artifact-panel">
      {/* Header */}
      <div className="artifact-header">
        <div className="artifact-title-box">
          <span className="artifact-type-badge">{artifact.type}</span>
          <span style={{ fontWeight: '600', fontSize: '14px', color: '#f8fafc' }}>{artifact.title}</span>
          <span title="Sanitized iframe sandbox security active" style={{ display: 'flex', alignItems: 'center', gap: '4px', fontSize: '11px', color: '#34d399', background: 'rgba(52, 211, 153, 0.1)', padding: '2px 8px', borderRadius: '12px' }}>
            <ShieldCheck size={12} /> Sandboxed
          </span>
        </div>

        <div className="artifact-controls">
          <div style={{ background: '#090d16', padding: '2px', borderRadius: '6px', display: 'flex', gap: '2px' }}>
            <button 
              className={`tab-btn ${activeTab === 'preview' ? 'active' : ''}`}
              onClick={() => setActiveTab('preview')}
            >
              <Eye size={12} style={{ display: 'inline', marginRight: '4px' }} /> Preview
            </button>
            <button 
              className={`tab-btn ${activeTab === 'code' ? 'active' : ''}`}
              onClick={() => setActiveTab('code')}
            >
              <Code size={12} style={{ display: 'inline', marginRight: '4px' }} /> Code
            </button>
          </div>

          <button onClick={handleCopy} title="Copy Content" style={{ background: 'none', border: 'none', color: '#94a3b8', cursor: 'pointer', padding: '4px' }}>
            {copied ? <Check size={16} color="#34d399" /> : <Copy size={16} />}
          </button>
          <button onClick={handleDownload} title="Download File" style={{ background: 'none', border: 'none', color: '#94a3b8', cursor: 'pointer', padding: '4px' }}>
            <Download size={16} />
          </button>
          <button onClick={onClose} title="Close Panel" style={{ background: 'none', border: 'none', color: '#94a3b8', cursor: 'pointer', padding: '4px' }}>
            <X size={18} />
          </button>
        </div>
      </div>

      {/* Body Rendering */}
      {activeTab === 'preview' ? (
        artifact.type === 'html' ? (
          <iframe 
            ref={iframeRef} 
            title="Artifact Preview Sandbox"
            className="sandbox-iframe"
            sandbox="allow-scripts"
          />
        ) : (
          <div style={{ flex: 1, padding: '24px', overflowY: 'auto', background: '#0f172a', color: '#f8fafc', lineHeight: '1.6' }}>
            <ReactMarkdown remarkPlugins={[remarkGfm]}>{artifact.content}</ReactMarkdown>
          </div>
        )
      ) : (
        <div className="artifact-body raw">
          <code>{artifact.content}</code>
        </div>
      )}
    </div>
  );
}

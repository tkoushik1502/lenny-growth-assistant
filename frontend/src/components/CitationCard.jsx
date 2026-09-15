import React, { useState } from 'react';
import { ExternalLink, Quote, ChevronDown, ChevronUp } from 'lucide-react';

export default function CitationCard({ citation, index }) {
  const [expanded, setExpanded] = useState(false);

  return (
    <div style={{
      background: '#0f172a',
      border: '1px solid #1e293b',
      borderRadius: '8px',
      padding: '8px 12px',
      fontSize: '12px',
      marginBottom: '6px'
    }}>
      <div 
        style={{ display: 'flex', alignItems: 'center', justifyContents: 'space-between', cursor: 'pointer' }}
        onClick={() => setExpanded(!expanded)}
      >
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px', flex: 1 }}>
          <span style={{
            background: 'rgba(56, 189, 248, 0.2)',
            color: '#38bdf8',
            fontSize: '10px',
            fontWeight: '700',
            padding: '2px 6px',
            borderRadius: '4px'
          }}>
            [{index + 1}]
          </span>
          <span style={{ fontWeight: '600', color: '#e2e8f0' }}>{citation.episode_title}</span>
          <span style={{ color: '#64748b' }}>• {citation.timestamp}</span>
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
          <a 
            href={citation.url} 
            target="_blank" 
            rel="noreferrer"
            onClick={(e) => e.stopPropagation()}
            style={{ color: '#38bdf8', display: 'flex', alignItems: 'center' }}
            title="Open transcript episode link"
          >
            <ExternalLink size={12} />
          </a>
          {expanded ? <ChevronUp size={14} color="#94a3b8" /> : <ChevronDown size={14} color="#94a3b8" />}
        </div>
      </div>

      {expanded && (
        <div style={{ marginTop: '8px', paddingTop: '8px', borderTop: '1px solid #1e293b', color: '#94a3b8', lineHeight: '1.5' }}>
          <div style={{ fontWeight: '500', color: '#38bdf8', marginBottom: '4px' }}>
            Topic: {citation.topic}
          </div>
          {citation.key_quote && (
            <div style={{ fontStyle: 'italic', background: '#1e293b', padding: '6px 10px', borderRadius: '4px', marginBottom: '6px', color: '#f1f5f9', display: 'flex', gap: '6px' }}>
              <Quote size={12} color="#38bdf8" style={{ flexShrink: 0, marginTop: '2px' }} />
              <div>"{citation.key_quote}"</div>
            </div>
          )}
          <div>{citation.snippet}</div>
        </div>
      )}
    </div>
  );
}

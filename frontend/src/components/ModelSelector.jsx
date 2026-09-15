import React from 'react';
import { Cpu, Cloud, CheckCircle, AlertCircle } from 'lucide-react';

export default function ModelSelector({ models, currentProvider, onSelectProvider }) {
  return (
    <div style={{ position: 'relative', display: 'flex', alignItems: 'center' }}>
      <select 
        value={currentProvider} 
        onChange={(e) => onSelectProvider(e.target.value)}
        style={{
          background: '#1e293b',
          color: '#f8fafc',
          border: '1px solid #334155',
          borderRadius: '8px',
          padding: '6px 12px 6px 32px',
          fontSize: '12px',
          fontWeight: '500',
          cursor: 'pointer',
          outline: 'none'
        }}
      >
        {models.map((m) => (
          <option key={m.id} value={m.id}>
            {m.name} {m.is_available ? '✓' : '(Fallback)'}
          </option>
        ))}
      </select>
      <div style={{ position: 'absolute', left: '10px', pointerEvents: 'none', color: '#38bdf8' }}>
        {currentProvider === 'ollama' ? <Cpu size={14} /> : <Cloud size={14} />}
      </div>
    </div>
  );
}

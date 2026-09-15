import React from 'react';
import { Rocket, PanelLeft, Activity, RefreshCw } from 'lucide-react';
import ModelSelector from './ModelSelector';

export default function Header({ 
  models, 
  currentProvider, 
  onSelectProvider, 
  health, 
  sidebarOpen, 
  setSidebarOpen,
  onNewChat 
}) {
  return (
    <header className="app-header">
      <div className="brand-section">
        <button 
          onClick={() => setSidebarOpen(!sidebarOpen)}
          style={{ background: 'none', border: 'none', color: '#94a3b8', cursor: 'pointer', display: 'flex', alignItems: 'center' }}
          title="Toggle Sidebar"
        >
          <PanelLeft size={20} />
        </button>

        <div className="brand-logo">🚀</div>

        <div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <span className="brand-title">The Lenny Growth Assistant</span>
            <span className="brand-badge">Lenny RAG Agent</span>
          </div>
        </div>
      </div>

      <div className="header-controls">
        {health && (
          <div style={{ display: 'flex', alignItems: 'center', gap: '6px', fontSize: '11px', color: '#94a3b8', background: '#0f172a', padding: '4px 10px', borderRadius: '12px', border: '1px solid #1e293b' }}>
            <span style={{ width: '8px', height: '8px', borderRadius: '50%', background: health.status === 'healthy' ? '#34d399' : '#f43f5e' }}></span>
            <span>{health.transcript_count} Chunks Indexed</span>
          </div>
        )}

        <ModelSelector 
          models={models} 
          currentProvider={currentProvider} 
          onSelectProvider={onSelectProvider} 
        />
      </div>
    </header>
  );
}

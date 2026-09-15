import React from 'react';
import { Plus, MessageSquare, Trash2, BookOpen, Layers } from 'lucide-react';

export default function Sidebar({ 
  sessions, 
  currentSessionId, 
  onSelectSession, 
  onNewChat, 
  onDeleteSession,
  isOpen 
}) {
  return (
    <aside className={`sidebar ${isOpen ? '' : 'collapsed'}`}>
      <div className="sidebar-header">
        <button className="new-chat-btn" onClick={onNewChat}>
          <Plus size={16} /> New Growth Chat
        </button>
      </div>

      <div className="sessions-list">
        <div style={{ fontSize: '11px', fontWeight: '600', textTransform: 'uppercase', color: '#64748b', padding: '8px 4px 4px 4px', letterSpacing: '0.5px' }}>
          Conversations ({sessions.length})
        </div>

        {sessions.map((s) => (
          <div
            key={s.id}
            className={`session-item ${s.id === currentSessionId ? 'active' : ''}`}
            onClick={() => onSelectSession(s.id)}
          >
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px', overflow: 'hidden' }}>
              <MessageSquare size={14} style={{ flexShrink: 0 }} />
              <span style={{ whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>
                {s.title}
              </span>
            </div>
            
            <button
              className="session-delete-btn"
              onClick={(e) => {
                e.stopPropagation();
                onDeleteSession(s.id);
              }}
              title="Delete session"
            >
              <Trash2 size={13} />
            </button>
          </div>
        ))}
      </div>

      <div style={{ padding: '16px', borderTop: '1px solid #1e293b', background: 'rgba(15, 23, 42, 0.5)', fontSize: '11px', color: '#64748b', display: 'flex', flexDirection: 'column', gap: '6px' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '6px', color: '#94a3b8' }}>
          <BookOpen size={12} color="#38bdf8" /> Lenny Podcast Repository
        </div>
        <div>Grounding: Ep. 101 - 105 transcripts</div>
      </div>
    </aside>
  );
}

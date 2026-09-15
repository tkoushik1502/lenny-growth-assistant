import React from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { User, Bot, Sparkles, Layers, FileText, CheckCircle2 } from 'lucide-react';
import CitationCard from './CitationCard';

export default function MessageBubble({ message, onOpenArtifact }) {
  const isUser = message.role === 'user';

  return (
    <div style={{
      display: 'flex',
      gap: '14px',
      alignItems: 'flex-start',
      marginBottom: '16px'
    }}>
      {/* Avatar */}
      <div style={{
        width: '32px',
        height: '32px',
        borderRadius: '10px',
        background: isUser ? '#3b82f6' : 'linear-gradient(135deg, #38bdf8 0%, #c084fc 100%)',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        color: '#fff',
        flexShrink: 0,
        boxShadow: isUser ? 'none' : '0 0 12px rgba(56, 189, 248, 0.3)'
      }}>
        {isUser ? <User size={16} /> : <Bot size={16} />}
      </div>

      {/* Bubble Content */}
      <div style={{ flex: 1, minWidth: 0 }}>
        {/* Role & Badge */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '6px' }}>
          <span style={{ fontSize: '13px', fontWeight: '600', color: isUser ? '#94a3b8' : '#38bdf8' }}>
            {isUser ? 'You' : 'Lenny Assistant'}
          </span>
          {!isUser && message.skill_used && (
            <span style={{
              fontSize: '10px',
              fontWeight: '600',
              textTransform: 'uppercase',
              background: message.skill_used === 'ship30' ? 'rgba(52, 211, 153, 0.15)' : 'rgba(192, 132, 252, 0.15)',
              color: message.skill_used === 'ship30' ? '#34d399' : '#c084fc',
              border: `1px solid ${message.skill_used === 'ship30' ? 'rgba(52, 211, 153, 0.3)' : 'rgba(192, 132, 252, 0.3)'}`,
              padding: '1px 6px',
              borderRadius: '10px'
            }}>
              {message.skill_used === 'ship30' ? 'Ship 30 for 30 Skill' : message.skill_used === 'artifact' ? 'Artifact Skill' : 'Grounded RAG'}
            </span>
          )}
        </div>

        {/* Message Body */}
        <div style={{
          background: isUser ? '#1e293b' : 'rgba(15, 23, 42, 0.6)',
          border: '1px solid',
          borderColor: isUser ? '#334155' : '#1e293b',
          borderRadius: '12px',
          padding: '16px',
          color: '#f8fafc',
          lineHeight: '1.6',
          fontSize: '14px'
        }}>
          {isUser ? (
            <div>{message.content}</div>
          ) : (
            <ReactMarkdown remarkPlugins={[remarkGfm]}>{message.content}</ReactMarkdown>
          )}

          {/* Render Attached Artifact Card if present */}
          {message.artifact && (
            <div style={{
              marginTop: '16px',
              background: '#090d16',
              border: '1px solid #38bdf8',
              borderRadius: '8px',
              padding: '12px 16px',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'space-between'
            }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                <div style={{ background: 'rgba(56, 189, 248, 0.2)', padding: '6px', borderRadius: '6px', color: '#38bdf8' }}>
                  <Layers size={18} />
                </div>
                <div>
                  <div style={{ fontWeight: '600', fontSize: '13px', color: '#f8fafc' }}>{message.artifact.title}</div>
                  <div style={{ fontSize: '11px', color: '#94a3b8' }}>Rendered Artifact ({message.artifact.type.toUpperCase()})</div>
                </div>
              </div>
              
              <button
                onClick={() => onOpenArtifact(message.artifact)}
                style={{
                  background: '#38bdf8',
                  color: '#090d16',
                  border: 'none',
                  borderRadius: '6px',
                  padding: '6px 14px',
                  fontWeight: '600',
                  fontSize: '12px',
                  cursor: 'pointer',
                  display: 'flex',
                  alignItems: 'center',
                  gap: '6px'
                }}
              >
                <FileText size={13} /> View Artifact
              </button>
            </div>
          )}

          {/* Render Citations Drawer if present */}
          {message.citations && message.citations.length > 0 && (
            <div style={{ marginTop: '16px', paddingTop: '12px', borderTop: '1px solid #1e293b' }}>
              <div style={{ fontSize: '11px', fontWeight: '600', color: '#64748b', textTransform: 'uppercase', marginBottom: '8px', letterSpacing: '0.5px' }}>
                Grounded Transcript Sources ({message.citations.length})
              </div>
              {message.citations.map((c, i) => (
                <CitationCard key={i} citation={c} index={i} />
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

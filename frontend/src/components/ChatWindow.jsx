import React, { useState, useRef, useEffect } from 'react';
import { Send, Sparkles, MessageSquare, Compass, Code, FileText, Loader2 } from 'lucide-react';
import MessageBubble from './MessageBubble';

export default function ChatWindow({ 
  messages, 
  onSendMessage, 
  onOpenArtifact,
  loading,
  currentSkill,
  setCurrentSkill 
}) {
  const [inputText, setInputText] = useState('');
  const messagesEndRef = useRef(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, loading]);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!inputText.trim() || loading) return;
    onSendMessage(inputText, currentSkill);
    setInputText('');
  };

  const handlePromptClick = (text, skill = 'chat') => {
    setCurrentSkill(skill);
    onSendMessage(text, skill);
  };

  return (
    <div className="chat-workspace">
      {/* Messages Stream */}
      <div className="chat-messages">
        {messages.length === 0 ? (
          <div className="empty-state">
            <div className="empty-icon">
              <Sparkles size={32} />
            </div>
            <h2 className="empty-title">The Lenny Growth Assistant</h2>
            <p className="empty-desc">
              Ask product & growth questions grounded strictly in transcripts from Brian Chesky, Shreyas Doshi, Elena Verna, Marty Cagan, and Gokul Rajaram.
            </p>

            <div className="prompt-chips">
              <div 
                className="chip-card" 
                onClick={() => handlePromptClick("Explain Brian Chesky's Founder Mode vs Manager Mode", "chat")}
              >
                <div className="chip-title">💡 Grounded RAG Query</div>
                <div className="chip-text">"Explain Brian Chesky's Founder Mode vs Manager Mode"</div>
              </div>

              <div 
                className="chip-card" 
                onClick={() => handlePromptClick("Write a Ship 30 for 30 essay on Task Prioritization & LNO Framework", "ship30")}
              >
                <div className="chip-title">✍️ Ship 30 for 30 Essay Skill</div>
                <div className="chip-text">"Write a ~1,250-word viral essay on Shreyas Doshi's LNO Framework"</div>
              </div>

              <div 
                className="chip-card" 
                onClick={() => handlePromptClick("Generate an interactive HTML growth framework matrix dashboard", "artifact")}
              >
                <div className="chip-title">🎨 In-App Artifact Viewer</div>
                <div className="chip-text">"Generate an interactive HTML growth framework matrix dashboard"</div>
              </div>

              <div 
                className="chip-card" 
                onClick={() => handlePromptClick("How does Elena Verna define Product-Led Growth vs Product-Led Sales?", "chat")}
              >
                <div className="chip-title">🚀 B2B Growth Strategy</div>
                <div className="chip-text">"How does Elena Verna define PLG vs Product-Led Sales?"</div>
              </div>
            </div>
          </div>
        ) : (
          messages.map((m) => (
            <MessageBubble key={m.id} message={m} onOpenArtifact={onOpenArtifact} />
          ))
        )}

        {loading && (
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px', color: '#38bdf8', fontSize: '13px', padding: '12px' }}>
            <Loader2 size={16} className="animate-spin" />
            <span>Analyzing Lenny's transcripts and executing skill...</span>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Input Bar */}
      <div className="input-container">
        <form onSubmit={handleSubmit} className="input-box">
          <textarea
            className="chat-textarea"
            placeholder="Ask anything about product management, growth loops, founder mode, or type a request..."
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                handleSubmit(e);
              }
            }}
          />

          <div className="input-actions">
            <div className="skill-selector">
              <button 
                type="button"
                className={`skill-pill ${currentSkill === 'chat' ? 'active' : ''}`}
                onClick={() => setCurrentSkill('chat')}
              >
                💬 Grounded Chat
              </button>
              <button 
                type="button"
                className={`skill-pill ${currentSkill === 'ship30' ? 'active' : ''}`}
                onClick={() => setCurrentSkill('ship30')}
              >
                ✍️ Ship 30 for 30 Skill
              </button>
              <button 
                type="button"
                className={`skill-pill ${currentSkill === 'artifact' ? 'active' : ''}`}
                onClick={() => setCurrentSkill('artifact')}
              >
                🎨 Render Artifact
              </button>
            </div>

            <button type="submit" className="send-btn" disabled={!inputText.trim() || loading}>
              <Send size={16} />
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

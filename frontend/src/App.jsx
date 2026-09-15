import React, { useState, useEffect } from 'react';
import Header from './components/Header';
import Sidebar from './components/Sidebar';
import ChatWindow from './components/ChatWindow';
import ArtifactViewer from './components/ArtifactViewer';
import { 
  fetchHealth, 
  fetchModels, 
  fetchSessions, 
  createSession, 
  fetchSessionDetail, 
  deleteSession,
  sendChatMessage 
} from './services/api';

export default function App() {
  const [health, setHealth] = useState(null);
  const [models, setModels] = useState([]);
  const [currentProvider, setCurrentProvider] = useState('ollama');
  
  const [sessions, setSessions] = useState([]);
  const [currentSessionId, setCurrentSessionId] = useState(null);
  const [currentSession, setCurrentSession] = useState(null);
  
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [activeArtifact, setActiveArtifact] = useState(null);
  const [currentSkill, setCurrentSkill] = useState('chat');
  const [loading, setLoading] = useState(false);

  // 1. Initial Load: Health, Models, Sessions
  useEffect(() => {
    async function init() {
      try {
        const healthData = await fetchHealth();
        setHealth(healthData);
      } catch (err) {
        console.error('Health fetch failed', err);
      }

      try {
        const modelsData = await fetchModels();
        setModels(modelsData.providers);
        setCurrentProvider(modelsData.current_provider || 'ollama');
      } catch (err) {
        console.error('Models fetch failed', err);
      }

      try {
        const sessList = await fetchSessions();
        setSessions(sessList);
        if (sessList.length > 0) {
          loadSession(sessList[0].id);
        } else {
          handleNewChat();
        }
      } catch (err) {
        console.error('Sessions fetch failed', err);
      }
    }

    init();
  }, []);

  const loadSession = async (sessionId) => {
    try {
      const detail = await fetchSessionDetail(sessionId);
      setCurrentSessionId(sessionId);
      setCurrentSession(detail);
      // Auto-open last artifact if present
      if (detail.artifacts && detail.artifacts.length > 0) {
        setActiveArtifact(detail.artifacts[detail.artifacts.length - 1]);
      } else {
        setActiveArtifact(null);
      }
    } catch (err) {
      console.error('Load session error:', err);
    }
  };

  const handleNewChat = async () => {
    try {
      const newSess = await createSession('New Conversation', currentProvider);
      setSessions((prev) => [newSess, ...prev]);
      setCurrentSessionId(newSess.id);
      setCurrentSession({ ...newSess, messages: [], artifacts: [] });
      setActiveArtifact(null);
    } catch (err) {
      console.error('Create new chat error:', err);
    }
  };

  const handleDeleteSession = async (sessionId) => {
    try {
      await deleteSession(sessionId);
      const remaining = sessions.filter((s) => s.id !== sessionId);
      setSessions(remaining);
      if (currentSessionId === sessionId) {
        if (remaining.length > 0) {
          loadSession(remaining[0].id);
        } else {
          handleNewChat();
        }
      }
    } catch (err) {
      console.error('Delete session error:', err);
    }
  };

  const handleSendMessage = async (text, skill) => {
    if (!currentSessionId) return;

    // Optimistic User Message UI
    const tempUserMsg = {
      id: `temp-${Date.now()}`,
      session_id: currentSessionId,
      role: 'user',
      content: text,
      created_at: new Date().toISOString()
    };

    setCurrentSession((prev) => ({
      ...prev,
      messages: [...(prev?.messages || []), tempUserMsg]
    }));

    setLoading(true);

    try {
      const res = await sendChatMessage({
        sessionId: currentSessionId,
        message: text,
        provider: currentProvider,
        skill: skill
      });

      // Update session with assistant response
      setCurrentSession((prev) => ({
        ...prev,
        messages: [...(prev?.messages || []).filter((m) => !m.id.startsWith('temp-')), tempUserMsg, res]
      }));

      // If response includes an artifact, open viewer automatically
      if (res.artifact) {
        setActiveArtifact(res.artifact);
      }

      // Refresh sessions list title
      const updatedSessions = await fetchSessions();
      setSessions(updatedSessions);
    } catch (err) {
      console.error('Send message error:', err);
      // Fallback error message
      const errorMsg = {
        id: `err-${Date.now()}`,
        session_id: currentSessionId,
        role: 'assistant',
        content: "⚠️ An error occurred processing your request. Please check if backend is running.",
        citations: [],
        created_at: new Date().toISOString()
      };
      setCurrentSession((prev) => ({
        ...prev,
        messages: [...(prev?.messages || []), errorMsg]
      }));
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app-container">
      <Header
        models={models}
        currentProvider={currentProvider}
        onSelectProvider={setCurrentProvider}
        health={health}
        sidebarOpen={sidebarOpen}
        setSidebarOpen={setSidebarOpen}
        onNewChat={handleNewChat}
      />

      <div className="main-body">
        <Sidebar
          sessions={sessions}
          currentSessionId={currentSessionId}
          onSelectSession={loadSession}
          onNewChat={handleNewChat}
          onDeleteSession={handleDeleteSession}
          isOpen={sidebarOpen}
        />

        <div className="split-pane">
          <ChatWindow
            messages={currentSession?.messages || []}
            onSendMessage={handleSendMessage}
            onOpenArtifact={setActiveArtifact}
            loading={loading}
            currentSkill={currentSkill}
            setCurrentSkill={setCurrentSkill}
          />

          {activeArtifact && (
            <ArtifactViewer
              artifact={activeArtifact}
              onClose={() => setActiveArtifact(null)}
            />
          )}
        </div>
      </div>
    </div>
  );
}

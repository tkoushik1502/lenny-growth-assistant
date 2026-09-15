const API_BASE = '/api/v1';

export async function fetchHealth() {
  const res = await fetch(`${API_BASE}/health`);
  if (!res.ok) throw new Error('Health check failed');
  return res.json();
}

export async function fetchModels() {
  const res = await fetch(`${API_BASE}/models`);
  if (!res.ok) throw new Error('Fetch models failed');
  return res.json();
}

export async function fetchSessions() {
  const res = await fetch(`${API_BASE}/sessions`);
  if (!res.ok) throw new Error('Fetch sessions failed');
  return res.json();
}

export async function createSession(title = 'New Conversation', provider = 'ollama') {
  const res = await fetch(`${API_BASE}/sessions?title=${encodeURIComponent(title)}&provider=${provider}`, {
    method: 'POST'
  });
  if (!res.ok) throw new Error('Create session failed');
  return res.json();
}

export async function fetchSessionDetail(sessionId) {
  const res = await fetch(`${API_BASE}/sessions/${sessionId}`);
  if (!res.ok) throw new Error('Fetch session detail failed');
  return res.json();
}

export async function deleteSession(sessionId) {
  const res = await fetch(`${API_BASE}/sessions/${sessionId}`, {
    method: 'DELETE'
  });
  if (!res.ok) throw new Error('Delete session failed');
  return true;
}

export async function sendChatMessage({ sessionId, message, provider, skill }) {
  const res = await fetch(`${API_BASE}/chat`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      session_id: sessionId,
      message: message,
      provider: provider,
      skill: skill
    })
  });
  if (!res.ok) throw new Error('Send message failed');
  return res.json();
}

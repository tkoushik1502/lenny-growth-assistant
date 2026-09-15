from typing import List, Optional, Any, Dict
from pydantic import BaseModel, Field
import datetime

class Citation(BaseModel):
    id: str
    episode_title: str
    guest: str
    timestamp: str
    topic: str
    url: str
    key_quote: Optional[str] = None
    snippet: str

class ArtifactSchema(BaseModel):
    id: str
    title: str
    type: str # 'markdown' or 'html'
    content: str
    created_at: Optional[datetime.datetime] = None

class ChatMessageRequest(BaseModel):
    session_id: str
    message: str
    provider: Optional[str] = "ollama" # ollama, anthropic, openai, mock
    skill: Optional[str] = "chat" # chat, ship30, artifact

class MessageResponse(BaseModel):
    id: str
    session_id: str
    role: str
    content: str
    citations: List[Citation] = []
    artifact: Optional[ArtifactSchema] = None
    skill_used: Optional[str] = None
    provider_used: str
    created_at: datetime.datetime

class SessionCreateRequest(BaseModel):
    title: Optional[str] = "New Conversation"
    provider: Optional[str] = "ollama"
    user_metadata: Optional[Dict[str, Any]] = None

class SessionSummary(BaseModel):
    id: str
    title: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
    provider_used: str
    user_metadata: Optional[Dict[str, Any]] = {}
    message_count: int = 0

class SessionDetail(SessionSummary):
    messages: List[MessageResponse] = []
    artifacts: List[ArtifactSchema] = []

class ModelProviderInfo(BaseModel):
    id: str
    name: str
    type: str # local or cloud
    is_available: bool
    status_message: str

class ModelsResponse(BaseModel):
    current_provider: str
    providers: List[ModelProviderInfo]

class HealthStatus(BaseModel):
    status: str
    timestamp: str
    database: str
    ollama_status: str
    transcript_count: int

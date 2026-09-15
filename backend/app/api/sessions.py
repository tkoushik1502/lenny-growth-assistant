import uuid
from typing import List, Optional, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from sqlalchemy.orm import selectinload

from app.database import get_db, ChatSession, ChatMessage, ArtifactModel
from app.models.schemas import (
    SessionSummary, 
    SessionDetail, 
    SessionCreateRequest, 
    MessageResponse, 
    ArtifactSchema, 
    Citation
)

router = APIRouter(prefix="/sessions", tags=["Sessions"])

@router.post("", response_model=SessionSummary)
async def create_session(
    payload: Optional[SessionCreateRequest] = None, 
    title: str = "New Conversation", 
    provider: str = "ollama", 
    db: AsyncSession = Depends(get_db)
):
    session_id = f"sess-{uuid.uuid4().hex[:10]}"
    sess_title = payload.title if payload and payload.title else title
    sess_provider = payload.provider if payload and payload.provider else provider
    sess_meta = payload.user_metadata if payload and payload.user_metadata else {}
    
    new_session = ChatSession(
        id=session_id, 
        title=sess_title, 
        provider_used=sess_provider,
        user_metadata=sess_meta
    )
    db.add(new_session)
    await db.commit()
    await db.refresh(new_session)
    
    return SessionSummary(
        id=new_session.id,
        title=new_session.title,
        created_at=new_session.created_at,
        updated_at=new_session.updated_at,
        provider_used=new_session.provider_used,
        user_metadata=new_session.user_metadata or {},
        message_count=0
    )

@router.get("", response_model=List[SessionSummary])
async def list_sessions(db: AsyncSession = Depends(get_db)):
    stmt = select(ChatSession).options(selectinload(ChatSession.messages)).order_by(ChatSession.updated_at.desc())
    result = await db.execute(stmt)
    sessions = result.scalars().all()
    
    summaries = []
    for s in sessions:
        summaries.append(
            SessionSummary(
                id=s.id,
                title=s.title,
                created_at=s.created_at,
                updated_at=s.updated_at,
                provider_used=s.provider_used,
                user_metadata=s.user_metadata or {},
                message_count=len(s.messages)
            )
        )
    return summaries

@router.get("/{session_id}", response_model=SessionDetail)
async def get_session(session_id: str, db: AsyncSession = Depends(get_db)):
    stmt = select(ChatSession).where(ChatSession.id == session_id).options(
        selectinload(ChatSession.messages),
        selectinload(ChatSession.artifacts)
    )
    result = await db.execute(stmt)
    session = result.scalar_one_or_none()
    
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
        
    messages_res = []
    for m in session.messages:
        citations = [Citation(**c) for c in (m.citations or [])]
        messages_res.append(
            MessageResponse(
                id=m.id,
                session_id=m.session_id,
                role=m.role,
                content=m.content,
                citations=citations,
                skill_used=m.skill_used,
                provider_used=session.provider_used,
                created_at=m.created_at
            )
        )

    artifacts_res = [
        ArtifactSchema(
            id=a.id,
            title=a.title,
            type=a.type,
            content=a.content,
            created_at=a.created_at
        ) for a in session.artifacts
    ]

    return SessionDetail(
        id=session.id,
        title=session.title,
        created_at=session.created_at,
        updated_at=session.updated_at,
        provider_used=session.provider_used,
        user_metadata=session.user_metadata or {},
        message_count=len(messages_res),
        messages=messages_res,
        artifacts=artifacts_res
    )

@router.delete("/{session_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_session(session_id: str, db: AsyncSession = Depends(get_db)):
    stmt = delete(ChatSession).where(ChatSession.id == session_id)
    await db.execute(stmt)
    await db.commit()
    return None

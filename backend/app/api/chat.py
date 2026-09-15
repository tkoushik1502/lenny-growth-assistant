import uuid
import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database import get_db, ChatSession, ChatMessage, ArtifactModel
from app.models.schemas import ChatMessageRequest, MessageResponse, Citation
from app.services.agent_service import agent_service

router = APIRouter(prefix="/chat", tags=["Chat"])

@router.post("", response_model=MessageResponse)
async def send_chat_message(req: ChatMessageRequest, db: AsyncSession = Depends(get_db)):
    # 1. Fetch or create session
    stmt = select(ChatSession).where(ChatSession.id == req.session_id)
    res = await db.execute(stmt)
    session = res.scalar_one_or_none()

    if not session:
        session = ChatSession(
            id=req.session_id,
            title=req.message[:30] + "..." if len(req.message) > 30 else req.message,
            provider_used=req.provider
        )
        db.add(session)
        await db.commit()
        await db.refresh(session)
    else:
        # Update session title if first message
        if session.title == "New Conversation" or not session.title:
            session.title = req.message[:30] + "..." if len(req.message) > 30 else req.message
        session.provider_used = req.provider
        session.updated_at = datetime.datetime.utcnow()

    # 2. Save User Message
    user_msg = ChatMessage(
        id=f"msg-{uuid.uuid4().hex[:10]}",
        session_id=session.id,
        role="user",
        content=req.message
    )
    db.add(user_msg)
    await db.commit()

    # 3. Execute Agent Processing
    content, citations, artifact_obj = await agent_service.process_message(
        user_message=req.message,
        provider=req.provider,
        skill=req.skill
    )

    # 4. Save Artifact if generated
    if artifact_obj:
        artifact_db = ArtifactModel(
            id=artifact_obj.id,
            session_id=session.id,
            title=artifact_obj.title,
            type=artifact_obj.type,
            content=artifact_obj.content
        )
        db.add(artifact_db)

    # 5. Save Assistant Message
    citations_data = [c.dict() for c in citations]
    assistant_msg = ChatMessage(
        id=f"msg-{uuid.uuid4().hex[:10]}",
        session_id=session.id,
        role="assistant",
        content=content,
        citations=citations_data,
        skill_used=req.skill
    )
    db.add(assistant_msg)
    await db.commit()
    await db.refresh(assistant_msg)

    return MessageResponse(
        id=assistant_msg.id,
        session_id=session.id,
        role="assistant",
        content=assistant_msg.content,
        citations=citations,
        artifact=artifact_obj,
        skill_used=req.skill,
        provider_used=req.provider,
        created_at=assistant_msg.created_at
    )

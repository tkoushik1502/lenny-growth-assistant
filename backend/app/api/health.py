import datetime
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from app.database import get_db
from app.services.llm_provider import LLMProvider
from app.services.rag_engine import rag_engine
from app.models.schemas import HealthStatus

router = APIRouter(tags=["Health"])

@router.get("/health", response_model=HealthStatus)
async def health_check(db: AsyncSession = Depends(get_db)):
    db_status = "online"
    try:
        await db.execute(text("SELECT 1"))
    except Exception:
        db_status = "offline"

    avail = await LLMProvider.inpect_provider_availability()
    ollama_msg = avail["ollama"]["message"]

    return HealthStatus(
        status="healthy",
        timestamp=datetime.datetime.utcnow().isoformat(),
        database=db_status,
        ollama_status=ollama_msg,
        transcript_count=rag_engine.get_chunk_count()
    )

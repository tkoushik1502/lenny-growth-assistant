from fastapi import APIRouter
from app.services.rag_engine import rag_engine

router = APIRouter(prefix="/ingest", tags=["Ingest"])

@router.get("/status")
async def get_ingest_status():
    return {
        "status": "ready",
        "total_transcripts": len(rag_engine.transcripts),
        "total_searchable_chunks": rag_engine.get_chunk_count(),
        "transcripts": [
            {
                "id": t["id"],
                "ep_number": t["ep_number"],
                "title": t["title"],
                "guest": t["guest"],
                "section_count": len(t.get("sections", []))
            } for t in rag_engine.transcripts
        ]
    }

@router.post("/reload")
async def reload_transcripts():
    rag_engine._load_transcripts()
    return {
        "status": "reloaded",
        "total_chunks": rag_engine.get_chunk_count()
    }

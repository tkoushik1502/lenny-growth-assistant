import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.database import init_db

@pytest_asyncio.fixture(autouse=True)
async def prepare_db():
    await init_db()

@pytest.mark.asyncio
async def test_health_endpoint():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        res = await ac.get("/api/v1/health")
        assert res.status_code == 200
        data = res.json()
        assert data["status"] == "healthy"
        assert "database" in data
        assert data["transcript_count"] > 0

@pytest.mark.asyncio
async def test_models_endpoint():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        res = await ac.get("/api/v1/models")
        assert res.status_code == 200
        data = res.json()
        assert "current_provider" in data
        assert len(data["providers"]) >= 3

@pytest.mark.asyncio
async def test_session_lifecycle():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        # Create session
        res = await ac.post("/api/v1/sessions?title=Test%20Session&provider=mock")
        assert res.status_code == 200
        sess_data = res.json()
        session_id = sess_data["id"]
        assert session_id.startswith("sess-")

        # List sessions
        res_list = await ac.get("/api/v1/sessions")
        assert res_list.status_code == 200
        assert any(s["id"] == session_id for s in res_list.json())

        # Get session detail
        res_detail = await ac.get(f"/api/v1/sessions/{session_id}")
        assert res_detail.status_code == 200
        assert res_detail.json()["id"] == session_id

        # Delete session
        res_del = await ac.delete(f"/api/v1/sessions/{session_id}")
        assert res_del.status_code == 204

@pytest.mark.asyncio
async def test_session_user_metadata_persistence():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        meta_payload = {
            "title": "Strategy Session",
            "provider": "mock",
            "user_metadata": {"role": "Lead PM", "organization": "Airbnb Growth"}
        }
        res = await ac.post("/api/v1/sessions", json=meta_payload)
        assert res.status_code == 200
        data = res.json()
        assert data["user_metadata"]["role"] == "Lead PM"
        assert data["user_metadata"]["organization"] == "Airbnb Growth"

        # Verify retrieval
        res_get = await ac.get(f"/api/v1/sessions/{data['id']}")
        assert res_get.status_code == 200
        assert res_get.json()["user_metadata"]["role"] == "Lead PM"

@pytest.mark.asyncio
async def test_chat_message():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        # Create session
        res_sess = await ac.post("/api/v1/sessions?title=Chat%20Test&provider=mock")
        session_id = res_sess.json()["id"]

        payload = {
            "session_id": session_id,
            "message": "What is Brian Chesky's founder mode?",
            "provider": "mock",
            "skill": "chat"
        }
        res_chat = await ac.post("/api/v1/chat", json=payload)
        assert res_chat.status_code == 200
        chat_data = res_chat.json()
        assert chat_data["role"] == "assistant"
        assert len(chat_data["content"]) > 0
        assert len(chat_data["citations"]) > 0

@pytest.mark.asyncio
async def test_ship30_skill_routing():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        res_sess = await ac.post("/api/v1/sessions?title=Ship30%20Test&provider=mock")
        session_id = res_sess.json()["id"]

        payload = {
            "session_id": session_id,
            "message": "Write a 1250 word Ship 30 for 30 essay on LNO framework",
            "provider": "mock",
            "skill": "ship30"
        }
        res_chat = await ac.post("/api/v1/chat", json=payload)
        assert res_chat.status_code == 200
        chat_data = res_chat.json()
        assert chat_data["role"] == "assistant"
        assert "Pillar" in chat_data["content"] or "Hook" in chat_data["content"]

@pytest.mark.asyncio
async def test_artifact_generation_routing():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        res_sess = await ac.post("/api/v1/sessions?title=Artifact%20Test&provider=mock")
        session_id = res_sess.json()["id"]

        payload = {
            "session_id": session_id,
            "message": "Create an HTML growth matrix artifact dashboard",
            "provider": "mock",
            "skill": "artifact"
        }
        res_chat = await ac.post("/api/v1/chat", json=payload)
        assert res_chat.status_code == 200
        chat_data = res_chat.json()
        assert chat_data["artifact"] is not None
        assert chat_data["artifact"]["type"] in ["html", "markdown"]

import pytest
from app.services.llm_provider import LLMProvider

@pytest.mark.asyncio
async def test_llm_provider_availability():
    status = await LLMProvider.inpect_provider_availability()
    assert "ollama" in status
    assert "anthropic" in status
    assert "openai" in status
    assert "mock" in status
    assert status["mock"]["available"] is True

@pytest.mark.asyncio
async def test_mock_llm_generation():
    res = await LLMProvider.generate_completion(
        prompt="Tell me about founder mode",
        system_prompt="",
        provider="mock"
    )
    assert len(res) > 50
    assert "Brian Chesky" in res or "Lenny" in res

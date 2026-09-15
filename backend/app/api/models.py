from fastapi import APIRouter
from app.services.llm_provider import LLMProvider
from app.models.schemas import ModelsResponse, ModelProviderInfo
from app.config import settings

router = APIRouter(tags=["Models"])

@router.get("/models", response_model=ModelsResponse)
async def get_models():
    avail = await LLMProvider.inpect_provider_availability()
    
    providers = [
        ModelProviderInfo(
            id="ollama",
            name="Ollama (Local LLM - Llama 3.2)",
            type="local",
            is_available=avail["ollama"]["available"],
            status_message=avail["ollama"]["message"]
        ),
        ModelProviderInfo(
            id="anthropic",
            name="Anthropic Claude 3.5 Sonnet",
            type="cloud",
            is_available=avail["anthropic"]["available"],
            status_message=avail["anthropic"]["message"]
        ),
        ModelProviderInfo(
            id="openai",
            name="OpenAI GPT-4o",
            type="cloud",
            is_available=avail["openai"]["available"],
            status_message=avail["openai"]["message"]
        ),
        ModelProviderInfo(
            id="mock",
            name="Lenny Mock Engine (Instant Offline)",
            type="local",
            is_available=True,
            status_message="Always available for zero-dependency local evaluation"
        )
    ]
    
    return ModelsResponse(
        current_provider=settings.DEFAULT_LLM_PROVIDER,
        providers=providers
    )

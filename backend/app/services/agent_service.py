import uuid
import re
import logging
from typing import Dict, Any, Tuple, Optional, List
from app.services.rag_engine import rag_engine
from app.services.llm_provider import LLMProvider
from app.services.skills.ship30_skill import ship30_skill
from app.models.schemas import Citation, ArtifactSchema

logger = logging.getLogger(__name__)

STANDARD_SYSTEM_PROMPT = """You are "The Lenny Growth Assistant", an elite product and growth AI advisor grounded strictly in Lenny's Podcast transcripts.

YOUR RULES:
1. GROUNDING: Answer questions based strictly on the provided transcript context. If the context does not contain enough information to answer, state clearly: "Based on the available transcripts, this specific topic is not covered in detail."
2. CITATIONS: Whenever you reference an insight, cite the guest name and episode (e.g. [Brian Chesky, Ep. 101]).
3. FORMATTING: Use clean markdown, bullet points, and bold text for readability.
4. TONE: Professional, strategic, concise, and actionable—like a world-class growth lead.
"""

ARTIFACT_SYSTEM_PROMPT = """You are an expert full-stack growth architect and UI builder.
When requested to create a dashboard, matrix, calculator, roadmap, or visual tool:
1. Provide a brief explanation of the tool.
2. Output a standalone HTML snippet wrapped inside ```html ... ``` codeblocks.
3. Ensure the HTML is self-contained with inline CSS styling, modern colors (dark mode slate/navy, vibrant accents), clean typography, and responsive layout.
4. Ground the contents of the tool in the transcript knowledge provided.
"""

class AgentService:
    """Central agent logic for query routing, RAG retrieval, skill execution, and artifact parsing."""

    @classmethod
    async def process_message(
        cls, 
        user_message: str, 
        provider: str = "ollama", 
        skill: str = "chat",
        history: Optional[List[Dict[str, str]]] = None
    ) -> Tuple[str, List[Citation], Optional[ArtifactSchema]]:
        
        # 1. Intent Detection & Skill Routing
        msg_lower = user_message.lower()
        if skill == "ship30" or "ship 30" in msg_lower or "essay" in msg_lower or "1250 word" in msg_lower:
            active_skill = "ship30"
        elif skill == "artifact" or "artifact" in msg_lower or "dashboard" in msg_lower or "html" in msg_lower or "matrix" in msg_lower or "calculator" in msg_lower:
            active_skill = "artifact"
        else:
            active_skill = "chat"

        # 2. Retrieve Relevant Transcript Chunks
        retrieved_chunks = rag_engine.search_transcripts(user_message, top_k=4)
        citations = rag_engine.format_citations(retrieved_chunks)

        # Build RAG Context String
        context_str = "TRANSCRIPT CONTEXT:\n"
        for i, chunk in enumerate(retrieved_chunks, 1):
            context_str += f"[{i}] Episode {chunk['ep_number']}: {chunk['guest']} ({chunk['topic']})\n"
            context_str += f"Timestamp: {chunk['timestamp']} | Quote: {chunk.get('key_quotes', [''])[0]}\n"
            context_str += f"Excerpt: {chunk['content']}\n\n"

        artifact = None
        response_text = ""

        # 3. Skill Execution
        if active_skill == "ship30":
            logger.info("Executing Ship 30 for 30 Skill")
            response_text = await ship30_skill.generate_essay(
                user_topic=user_message,
                context_chunks=retrieved_chunks,
                provider=provider
            )
        elif active_skill == "artifact":
            logger.info("Executing Artifact Generator Skill")
            full_prompt = f"{user_message}\n\n{context_str}"
            response_text = await LLMProvider.generate_completion(
                prompt=full_prompt,
                system_prompt=ARTIFACT_SYSTEM_PROMPT,
                provider=provider
            )
        else:
            # Standard Grounded Chat
            logger.info("Executing Standard Grounded Chat")
            full_prompt = f"{user_message}\n\n{context_str}"
            response_text = await LLMProvider.generate_completion(
                prompt=full_prompt,
                system_prompt=STANDARD_SYSTEM_PROMPT,
                provider=provider
            )

        # 4. Extract Artifacts if HTML or Markdown blocks are generated
        artifact = cls._extract_artifact(response_text)

        return response_text, citations, artifact

    @classmethod
    def _extract_artifact(cls, content: str) -> Optional[ArtifactSchema]:
        """Scans response content for ```html ... ``` or complex markdown blocks to extract into Artifact object."""
        html_match = re.search(r'```html\s*(.*?)\s*```', content, re.DOTALL | re.IGNORECASE)
        if html_match:
            html_code = html_match.group(1).strip()
            # Extract title if present in h2/h3 or default
            title_match = re.search(r'<h[1-3][^>]*>(.*?)</h[1-3]>', html_code, re.IGNORECASE)
            title = title_match.group(1).strip() if title_match else "Interactive Growth Component"
            return ArtifactSchema(
                id=f"art-{uuid.uuid4().hex[:8]}",
                title=title,
                type="html",
                content=html_code
            )
        
        # Check for standalone large markdown tables or code blocks
        if "```markdown" in content or "| --- |" in content:
            md_match = re.search(r'```markdown\s*(.*?)\s*```', content, re.DOTALL | re.IGNORECASE)
            md_code = md_match.group(1).strip() if md_match else content
            return ArtifactSchema(
                id=f"art-{uuid.uuid4().hex[:8]}",
                title="Grounded Growth Artifact",
                type="markdown",
                content=md_code
            )

        return None

agent_service = AgentService()

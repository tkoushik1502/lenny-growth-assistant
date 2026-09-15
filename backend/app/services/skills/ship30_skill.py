import logging
from typing import List, Dict, Any
from app.services.llm_provider import LLMProvider

logger = logging.getLogger(__name__)

SHIP30_SYSTEM_PROMPT = """You are an elite growth editor trained in Dickie Bush & Nicolas Cole's Ship 30 for 30 digital writing methodology.
Your job is to transform grounded product & growth insights into a viral, highly engaging ~1,250-word Ship 30 for 30 style essay.

Writing Principles to ENFORCE strictly:
1. THE HOOK: Open with an irresistible, single-sentence counter-intuitive claim or question that grabs high-level product managers and founders.
2. NARRATIVE PROGRESSION & 3 PILLARS: Structure the body into 3 distinct, logical pillars/sections.
3. HIGHLY SKIMMABLE FORMATTING:
   - Use punchy H2 and H3 subheadings.
   - Limit paragraphs to 1-3 sentences maximum.
   - Use bullet lists and numbered lists generously.
   - Use selective **bold emphasis** for core takeaways so skimmers capture 80% of the value in 30 seconds.
4. GROUNDED CLAIMS: Every core thesis MUST cite the guest name, episode number, and exact concept from the provided context.
5. ACTIONABLE TAKEAWAY: End with a step-by-step checklist or audit framework the reader can execute this week.

TARGET WORD COUNT: Approximately 1,200 - 1,400 words.
"""

class Ship30Skill:
    """Dedicated skill for generating structured, viral Ship 30 for 30 growth essays."""

    @classmethod
    async def generate_essay(
        cls, 
        user_topic: str, 
        context_chunks: List[Dict[str, Any]], 
        provider: str = "ollama"
    ) -> str:
        # Build context string
        context_text = ""
        for i, chunk in enumerate(context_chunks, 1):
            context_text += f"\n--- Source [{i}]: Ep. {chunk['ep_number']} - {chunk['guest']} ({chunk['topic']}) ---\n"
            context_text += f"Timestamp: {chunk['timestamp']}\n"
            context_text += f"Content: {chunk['content']}\n"
            if chunk.get("key_quotes"):
                context_text += f"Key Quote: \"{chunk['key_quotes'][0]}\"\n"

        prompt = f"""Write a comprehensive Ship 30 for 30 essay on the following topic:
TOPIC / QUERY: {user_topic}

TRANSCRIPT KNOWLEDGE CONTEXT:
{context_text}

INSTRUCTIONS:
1. Write an essay of approximately 1,250 words following all Ship 30 for 30 rules.
2. Ground all claims strictly in the provided transcript knowledge context above.
3. Ensure skimmable formatting (bold key phrases, bullet points, callout boxes).
4. Include explicit footnotes or citations pointing back to guest names and episode numbers.
5. Conclude with an actionable 'Growth Playbook Checklist' for immediate application.
"""
        response = await LLMProvider.generate_completion(
            prompt=prompt,
            system_prompt=SHIP30_SYSTEM_PROMPT,
            provider=provider
        )
        return response

ship30_skill = Ship30Skill()

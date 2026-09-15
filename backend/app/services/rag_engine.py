import json
import os
import logging
import re
from typing import List, Dict, Any
from app.config import settings
from app.models.schemas import Citation

logger = logging.getLogger(__name__)

class RAGEngine:
    """Transcript Retrieval Augmented Generation (RAG) search engine."""
    
    def __init__(self):
        self.transcripts: List[Dict[str, Any]] = []
        self.chunks: List[Dict[str, Any]] = []
        self._load_transcripts()

    def _load_transcripts(self):
        filepath = settings.TRANSCRIPTS_PATH
        if not os.path.exists(filepath):
            logger.error(f"Transcript data file not found at {filepath}")
            return
        
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                self.transcripts = json.load(f)
            
            # Flatten into searchable chunks
            self.chunks = []
            for ep in self.transcripts:
                for section in ep.get("sections", []):
                    chunk = {
                        "citation_id": section.get("section_id"),
                        "ep_id": ep.get("id"),
                        "ep_number": ep.get("ep_number"),
                        "episode_title": ep.get("title"),
                        "guest": ep.get("guest"),
                        "role": ep.get("role"),
                        "url": ep.get("url"),
                        "timestamp": section.get("timestamp"),
                        "topic": section.get("topic"),
                        "content": section.get("content"),
                        "key_quotes": section.get("key_quotes", []),
                        "text_searchable": f"{ep.get('title')} {ep.get('guest')} {section.get('topic')} {section.get('content')} {' '.join(section.get('key_quotes', []))}".lower()
                    }
                    self.chunks.append(chunk)
            logger.info(f"Loaded {len(self.transcripts)} transcripts containing {len(self.chunks)} searchable chunks.")
        except Exception as e:
            logger.error(f"Error loading transcript dataset: {e}")

    def get_chunk_count(self) -> int:
        return len(self.chunks)

    def search_transcripts(self, query: str, top_k: int = 4) -> List[Dict[str, Any]]:
        if not self.chunks:
            self._load_transcripts()
            
        if not self.chunks:
            return []

        query_terms = re.findall(r'\w+', query.lower())
        if not query_terms:
            return self.chunks[:top_k]

        scored_chunks = []
        for chunk in self.chunks:
            text = chunk["text_searchable"]
            score = 0
            
            # Weighted term matching
            for term in query_terms:
                if len(term) <= 2:
                    continue
                # Guest or Topic exact match bonus
                if term in chunk["guest"].lower():
                    score += 15
                if term in chunk["topic"].lower():
                    score += 10
                if term in text:
                    score += text.count(term) * 2

            scored_chunks.append((score, chunk))

        # Sort by relevance score descending
        scored_chunks.sort(key=lambda x: x[0], reverse=True)
        
        # Select top_k non-zero score chunks, or top default chunks if no direct term match
        results = [item[1] for item in scored_chunks if item[0] > 0][:top_k]
        if not results:
            results = self.chunks[:top_k]
            
        return results

    def format_citations(self, chunks: List[Dict[str, Any]]) -> List[Citation]:
        citations = []
        for chunk in chunks:
            quote = chunk["key_quotes"][0] if chunk.get("key_quotes") else None
            citations.append(
                Citation(
                    id=chunk["citation_id"],
                    episode_title=f"Ep. {chunk['ep_number']}: {chunk['guest']}",
                    guest=chunk["guest"],
                    timestamp=chunk["timestamp"],
                    topic=chunk["topic"],
                    url=chunk["url"],
                    key_quote=quote,
                    snippet=chunk["content"][:200] + "..."
                )
            )
        return citations

rag_engine = RAGEngine()

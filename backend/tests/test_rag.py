import pytest
from app.services.rag_engine import rag_engine

def test_rag_engine_load():
    assert rag_engine.get_chunk_count() > 0
    assert len(rag_engine.transcripts) > 0

def test_rag_search_brian_chesky():
    results = rag_engine.search_transcripts("Brian Chesky founder mode", top_k=2)
    assert len(results) > 0
    assert any("Brian Chesky" in r["guest"] for r in results)

def test_rag_search_lno_framework():
    results = rag_engine.search_transcripts("Shreyas Doshi LNO framework", top_k=2)
    assert len(results) > 0
    assert any("Shreyas Doshi" in r["guest"] for r in results)

def test_citation_formatting():
    results = rag_engine.search_transcripts("PLG growth loops", top_k=2)
    citations = rag_engine.format_citations(results)
    assert len(citations) == len(results)
    assert citations[0].url.startswith("http")
    assert len(citations[0].snippet) > 0

"""
Semantic duplicate detector.
Uses ChromaDB cosine similarity to detect near-duplicate questions.
"""
from backend.rag.retriever import check_duplicate

DUPLICATE_THRESHOLD = 0.85


async def is_duplicate(topic_id: int, question_text: str) -> tuple[bool, str | None, float]:
    """
    Returns (is_duplicate, similar_question_id, similarity_score).
    A question is duplicate if cosine similarity >= DUPLICATE_THRESHOLD.
    """
    return await check_duplicate(topic_id, question_text, threshold=DUPLICATE_THRESHOLD)

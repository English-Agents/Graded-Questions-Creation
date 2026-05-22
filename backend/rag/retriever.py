"""
Retrieves semantically relevant chunks from ChromaDB for a given topic.

Embedding strategy:
  OPENAI_API_KEY set   → pre-computed OpenAI embeddings passed to ChromaDB.
  OPENAI_API_KEY blank → ChromaDB uses its built-in local embedding model.
"""
import chromadb

from backend.config import settings
from backend.rag.embedder import embed_text

_chroma = None


async def _get_chroma():
    global _chroma
    if _chroma is None:
        _chroma = await chromadb.AsyncHttpClient(
            host=settings.chroma_host,
            port=settings.chroma_port,
        )
    return _chroma


def _collection_name(topic_id: int) -> str:
    return f"topic_{topic_id}"


async def retrieve(topic_id: int, query: str, k: int = 5) -> list[str]:
    """
    Return the top-k most relevant text chunks for `query` from topic's collection.
    Returns an empty list if the collection doesn't exist yet.
    """
    client = await _get_chroma()
    try:
        collection = await client.get_collection(name=_collection_name(topic_id))
    except Exception:
        return []

    embedding = await embed_text(query)   # None if no OpenAI key

    if embedding is not None:
        results = await collection.query(
            query_embeddings=[embedding],
            n_results=k,
            include=["documents"],
        )
    else:
        results = await collection.query(
            query_texts=[query],
            n_results=k,
            include=["documents"],
        )

    return results["documents"][0] if results["documents"] else []


async def embed_and_store_question(question_id: str, topic_id: int, text: str) -> str:
    """
    Embed a generated question and store it in a separate collection for dedup.
    Returns the stored chroma_id.
    """
    client = await _get_chroma()
    pool_collection = await client.get_or_create_collection(
        name=f"questions_{topic_id}",
        metadata={"hnsw:space": "cosine"},
    )

    embedding = await embed_text(text)   # None if no OpenAI key

    upsert_kwargs: dict = {
        "ids": [question_id],
        "documents": [text],
        "metadatas": [{"question_id": question_id, "topic_id": topic_id}],
    }
    if embedding is not None:
        upsert_kwargs["embeddings"] = [embedding]

    await pool_collection.upsert(**upsert_kwargs)
    return question_id


async def check_duplicate(topic_id: int, text: str, threshold: float = 0.85) -> tuple[bool, str | None, float]:
    """
    Check if a question text is semantically similar to existing pool questions.
    Returns (is_duplicate, similar_question_id, similarity_score).
    """
    client = await _get_chroma()
    try:
        pool_collection = await client.get_collection(name=f"questions_{topic_id}")
    except Exception:
        return False, None, 0.0

    count = await pool_collection.count()
    if count == 0:
        return False, None, 0.0

    embedding = await embed_text(text)   # None if no OpenAI key

    if embedding is not None:
        results = await pool_collection.query(
            query_embeddings=[embedding],
            n_results=1,
            include=["distances", "metadatas"],
        )
    else:
        results = await pool_collection.query(
            query_texts=[text],
            n_results=1,
            include=["distances", "metadatas"],
        )

    if not results["distances"] or not results["distances"][0]:
        return False, None, 0.0

    # ChromaDB cosine distance = 1 - cosine_similarity
    distance = results["distances"][0][0]
    similarity = 1.0 - distance
    similar_id = results["metadatas"][0][0].get("question_id") if results["metadatas"] else None

    return similarity >= threshold, similar_id, similarity

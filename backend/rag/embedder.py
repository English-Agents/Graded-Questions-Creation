"""
Embedding helper.

If OPENAI_API_KEY is set  → uses OpenAI text-embedding-3-small (high quality).
If OPENAI_API_KEY is blank → returns None; callers let ChromaDB use its built-in
                              local embedding model (no API key required).
"""
from backend.config import settings

_openai_client = None


def _get_openai_client():
    global _openai_client
    if _openai_client is None:
        from openai import AsyncOpenAI
        _openai_client = AsyncOpenAI(api_key=settings.openai_api_key)
    return _openai_client


async def embed_texts(texts: list[str]) -> list[list[float]] | None:
    """
    Return embeddings for a list of texts.
    Returns None if OpenAI key is not configured — caller should use ChromaDB's
    built-in embedding instead.
    """
    if not texts:
        return []
    if not settings.openai_api_key:
        return None
    client = _get_openai_client()
    response = await client.embeddings.create(
        model=settings.embedding_model,
        input=texts,
    )
    return [item.embedding for item in response.data]


async def embed_text(text: str) -> list[float] | None:
    """
    Return embedding for a single text.
    Returns None if OpenAI key is not configured.
    """
    results = await embed_texts([text])
    if results is None:
        return None
    return results[0]

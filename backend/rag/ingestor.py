"""
Ingests reading material files into ChromaDB.
Supported formats: .md, .txt, .pdf, .docx
Chunks at ~512 tokens with 50-token overlap.
"""
import hashlib
import re
import uuid
from pathlib import Path

import chromadb
import tiktoken
from docx import Document

from backend.config import settings
from backend.rag.embedder import embed_texts

_chroma = None
_enc = tiktoken.get_encoding("cl100k_base")

CHUNK_TOKENS = 512
OVERLAP_TOKENS = 50


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


def _read_file(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix in (".md", ".txt"):
        return path.read_text(encoding="utf-8")
    if suffix == ".pdf":
        from pypdf import PdfReader
        reader = PdfReader(str(path))
        return "\n".join(page.extract_text() or "" for page in reader.pages)
    if suffix == ".docx":
        doc = Document(str(path))
        return "\n".join(p.text for p in doc.paragraphs)
    raise ValueError(f"Unsupported file type: {suffix}")


def _chunk_text(text: str) -> list[str]:
    """Split text into overlapping chunks measured in tokens."""
    tokens = _enc.encode(text)
    chunks: list[str] = []
    start = 0
    while start < len(tokens):
        end = min(start + CHUNK_TOKENS, len(tokens))
        chunk_tokens = tokens[start:end]
        chunks.append(_enc.decode(chunk_tokens))
        if end == len(tokens):
            break
        start += CHUNK_TOKENS - OVERLAP_TOKENS
    return chunks


def _stable_id(topic_id: int, file_name: str, chunk_index: int) -> str:
    raw = f"{topic_id}:{file_name}:{chunk_index}"
    return hashlib.md5(raw.encode()).hexdigest()


async def ingest_file(topic_id: int, file_path: Path) -> int:
    """
    Parse, chunk, embed, and upsert a single material file into ChromaDB.
    Returns the number of chunks ingested.
    """
    text = _read_file(file_path)
    # Strip excessive whitespace
    text = re.sub(r"\n{3,}", "\n\n", text).strip()

    chunks = _chunk_text(text)
    if not chunks:
        return 0

    embeddings = await embed_texts(chunks)   # None if no OpenAI key
    client = await _get_chroma()
    collection = await client.get_or_create_collection(
        name=_collection_name(topic_id),
        metadata={"hnsw:space": "cosine"},
    )

    ids = [_stable_id(topic_id, file_path.name, i) for i in range(len(chunks))]
    metadatas = [
        {"topic_id": topic_id, "source_file": file_path.name, "chunk_index": i}
        for i in range(len(chunks))
    ]

    upsert_kwargs: dict = {"ids": ids, "documents": chunks, "metadatas": metadatas}
    if embeddings is not None:
        upsert_kwargs["embeddings"] = embeddings  # use pre-computed embeddings
    # else: ChromaDB uses its built-in local embedding model automatically

    await collection.upsert(**upsert_kwargs)
    return len(chunks)


async def ingest_directory(topic_id: int, material_dir: Path) -> dict[str, int]:
    """Ingest all supported files in a material directory."""
    results: dict[str, int] = {}
    supported = {".md", ".txt", ".pdf", ".docx"}
    for file_path in material_dir.iterdir():
        if file_path.suffix.lower() in supported:
            count = await ingest_file(topic_id, file_path)
            results[file_path.name] = count
    return results

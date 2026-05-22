"""
Content upload endpoints:
  POST /api/content/material   — upload reading material file for a topic
  POST /api/content/samples    — upload sample questions CSV for a topic
  GET  /api/content/topics     — list topics with their material + sample question counts
"""
import csv
import io
import tempfile
from pathlib import Path
from typing import Annotated

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.config import settings
from backend.db.connection import get_db
from backend.db.models import Module, SampleQuestion, Topic
from backend.rag.ingestor import ingest_file

router = APIRouter(prefix="/api/content", tags=["content"])


@router.post("/material")
async def upload_material(
    topic_id: Annotated[int, Form()],
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
):
    """Upload a reading material file (.md, .txt, .pdf, .docx) and ingest into ChromaDB."""
    topic = await db.get(Topic, topic_id)
    if not topic:
        raise HTTPException(404, f"Topic {topic_id} not found")

    suffix = Path(file.filename or "file.txt").suffix.lower()
    if suffix not in {".md", ".txt", ".pdf", ".docx"}:
        raise HTTPException(400, f"Unsupported file type: {suffix}. Allowed: .md .txt .pdf .docx")

    # Save to temp file so ingestor can use it
    with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as tmp:
        content = await file.read()
        tmp.write(content)
        tmp_path = Path(tmp.name)

    try:
        chunk_count = await ingest_file(topic_id, tmp_path)
    finally:
        tmp_path.unlink(missing_ok=True)

    return {
        "topic_id": topic_id,
        "filename": file.filename,
        "chunks_ingested": chunk_count,
        "status": "ok",
    }


@router.post("/samples")
async def upload_sample_questions(
    topic_id: Annotated[int, Form()],
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
):
    """
    Upload a sample questions CSV for a topic.
    Expected columns (header row optional, detected automatically):
      skill, marks, question_type, difficulty, text, answer_key,
      option_a, option_b, option_c, option_d, bloom_level
    Rows starting with # are treated as comments and skipped.
    """
    topic = await db.get(Topic, topic_id)
    if not topic:
        raise HTTPException(404, f"Topic {topic_id} not found")

    raw = await file.read()
    text = raw.decode("utf-8", errors="replace")

    reader = csv.reader(
        line for line in io.StringIO(text) if not line.strip().startswith("#")
    )

    EXPECTED_COLS = [
        "skill", "marks", "question_type", "difficulty", "text",
        "answer_key", "option_a", "option_b", "option_c", "option_d", "bloom_level",
    ]

    inserted = 0
    for row_num, row in enumerate(reader, start=1):
        if len(row) < 5:
            continue
        # Pad to 11 columns
        row = (row + [""] * 11)[:11]
        skill, marks_str, question_type, difficulty, text_val = row[:5]
        answer_key, opt_a, opt_b, opt_c, opt_d, bloom_str = row[5:]

        skill = skill.strip()
        question_type = question_type.strip()
        difficulty = difficulty.strip().lower()
        text_val = text_val.strip()

        if not skill or not text_val:
            continue
        if difficulty not in ("easy", "medium", "hard"):
            continue

        try:
            marks = int(marks_str.strip())
        except ValueError:
            continue

        bloom_level: int | None = None
        try:
            bloom_level = int(bloom_str.strip())
        except (ValueError, AttributeError):
            pass

        options: dict | None = None
        if opt_a.strip():
            options = {
                "a": opt_a.strip(),
                "b": opt_b.strip(),
                "c": opt_c.strip(),
                "d": opt_d.strip(),
            }

        sample = SampleQuestion(
            topic_id=topic_id,
            skill=skill,
            marks=marks,
            question_type=question_type,
            difficulty=difficulty,
            text=text_val,
            answer_key=answer_key.strip() or None,
            options=options,
            bloom_level=bloom_level,
        )
        db.add(sample)
        inserted += 1

    await db.commit()
    return {"topic_id": topic_id, "rows_inserted": inserted, "status": "ok"}


@router.get("/topics")
async def list_topics(
    course_id: int | None = None,
    db: AsyncSession = Depends(get_db),
):
    """List all topics, optionally filtered by course_id."""
    stmt = select(Topic).join(Module)
    if course_id:
        stmt = stmt.where(Module.course_id == course_id)
    result = await db.execute(stmt)
    topics = result.scalars().all()

    return [
        {
            "id": t.id,
            "name": t.name,
            "module_id": t.module_id,
            "metadata": t.metadata_,
        }
        for t in topics
    ]

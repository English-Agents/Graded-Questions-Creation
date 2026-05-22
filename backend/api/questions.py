"""
Question pool management endpoints:
  GET   /api/questions              — browse pool with filters
  PATCH /api/questions/{id}         — approve or reject a question
  GET   /api/pool-config            — view pool targets vs current counts
  PUT   /api/pool-config            — set target count for a combination
"""
import uuid

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.db.connection import get_db
from backend.db.models import PoolConfig, Question, Skill, Topic

router = APIRouter(tags=["questions"])


# ─────────────────────────────────────────────
# Pool browser
# ─────────────────────────────────────────────

@router.get("/api/questions")
async def list_questions(
    topic_id: int | None = None,
    skill: str | None = None,
    marks: int | None = None,
    question_type: str | None = None,
    difficulty: str | None = None,
    status: str | None = None,
    limit: int = 50,
    offset: int = 0,
    db: AsyncSession = Depends(get_db),
):
    stmt = select(Question).join(PoolConfig)

    if topic_id is not None:
        stmt = stmt.where(PoolConfig.topic_id == topic_id)
    if marks is not None:
        stmt = stmt.where(PoolConfig.marks == marks)
    if question_type:
        stmt = stmt.where(PoolConfig.question_type == question_type)
    if difficulty:
        stmt = stmt.where(Question.difficulty == difficulty)
    if status:
        stmt = stmt.where(Question.validation_status == status)
    if skill:
        stmt = stmt.join(Skill, Skill.id == PoolConfig.skill_id).where(Skill.name == skill)

    stmt = stmt.order_by(Question.created_at.desc()).limit(limit).offset(offset)
    result = await db.execute(stmt)
    questions = result.scalars().all()

    return [
        {
            "id": str(q.id),
            "pool_config_id": q.pool_config_id,
            "text": q.text,
            "question_type": q.question_type,
            "marks": q.marks,
            "difficulty": q.difficulty,
            "bloom_level": q.bloom_level,
            "answer_key": q.answer_key,
            "options": q.options,
            "validation_status": q.validation_status,
            "rejection_reason": q.rejection_reason,
            "created_at": q.created_at.isoformat() if q.created_at else None,
        }
        for q in questions
    ]


# ─────────────────────────────────────────────
# Approve / reject
# ─────────────────────────────────────────────

class QuestionPatch(BaseModel):
    validation_status: str  # approved | rejected
    rejection_reason: str | None = None


@router.patch("/api/questions/{question_id}")
async def update_question_status(
    question_id: str,
    patch: QuestionPatch,
    db: AsyncSession = Depends(get_db),
):
    if patch.validation_status not in ("approved", "rejected"):
        raise HTTPException(400, "validation_status must be 'approved' or 'rejected'")

    try:
        qid = uuid.UUID(question_id)
    except ValueError:
        raise HTTPException(400, "Invalid question ID format")

    question = await db.get(Question, qid)
    if not question:
        raise HTTPException(404, f"Question {question_id} not found")

    prev_status = question.validation_status
    question.validation_status = patch.validation_status
    question.rejection_reason = patch.rejection_reason

    # Adjust pool current_count when status changes
    pool_cfg = await db.get(PoolConfig, question.pool_config_id)
    if pool_cfg:
        if prev_status == "approved" and patch.validation_status == "rejected":
            pool_cfg.current_count = max(0, pool_cfg.current_count - 1)
        elif prev_status != "approved" and patch.validation_status == "approved":
            pool_cfg.current_count += 1

    await db.commit()
    return {"id": question_id, "validation_status": patch.validation_status}


# ─────────────────────────────────────────────
# Pool config
# ─────────────────────────────────────────────

@router.get("/api/pool-config")
async def get_pool_config(
    topic_id: int | None = None,
    db: AsyncSession = Depends(get_db),
):
    stmt = select(PoolConfig, Skill.name).join(Skill, Skill.id == PoolConfig.skill_id)
    if topic_id is not None:
        stmt = stmt.where(PoolConfig.topic_id == topic_id)
    result = await db.execute(stmt)
    rows = result.all()

    return [
        {
            "id": pc.id,
            "topic_id": pc.topic_id,
            "skill": skill_name,
            "marks": pc.marks,
            "question_type": pc.question_type,
            "difficulty": pc.difficulty,
            "target_count": pc.target_count,
            "current_count": pc.current_count,
            "gap": max(0, pc.target_count - pc.current_count),
        }
        for pc, skill_name in rows
    ]


class PoolConfigUpsert(BaseModel):
    topic_id: int
    skill: str
    marks: int
    question_type: str
    difficulty: str
    target_count: int


@router.put("/api/pool-config")
async def upsert_pool_config(
    payload: PoolConfigUpsert,
    db: AsyncSession = Depends(get_db),
):
    if payload.difficulty not in ("easy", "medium", "hard"):
        raise HTTPException(400, "difficulty must be easy | medium | hard")

    skill_result = await db.execute(select(Skill).where(Skill.name == payload.skill))
    skill = skill_result.scalars().first()
    if not skill:
        raise HTTPException(404, f"Skill '{payload.skill}' not found")

    topic = await db.get(Topic, payload.topic_id)
    if not topic:
        raise HTTPException(404, f"Topic {payload.topic_id} not found")

    pc_result = await db.execute(
        select(PoolConfig).where(
            PoolConfig.topic_id == payload.topic_id,
            PoolConfig.skill_id == skill.id,
            PoolConfig.marks == payload.marks,
            PoolConfig.question_type == payload.question_type,
            PoolConfig.difficulty == payload.difficulty,
        )
    )
    pc = pc_result.scalars().first()

    if pc:
        pc.target_count = payload.target_count
    else:
        pc = PoolConfig(
            topic_id=payload.topic_id,
            skill_id=skill.id,
            marks=payload.marks,
            question_type=payload.question_type,
            difficulty=payload.difficulty,
            target_count=payload.target_count,
            current_count=0,
        )
        db.add(pc)

    await db.commit()
    await db.refresh(pc)
    return {
        "id": pc.id,
        "target_count": pc.target_count,
        "current_count": pc.current_count,
        "gap": max(0, pc.target_count - pc.current_count),
    }

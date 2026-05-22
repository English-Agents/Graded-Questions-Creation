"""
Question generation endpoints:
  POST /api/generate          — trigger generation workflow
  GET  /api/generate/{job_id} — poll job status (in-memory for now)
"""
import asyncio
import uuid
from typing import Any

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.agents.generation_graph import generation_graph
from backend.db.connection import get_db
from backend.db.models import PoolConfig, Skill, Topic

router = APIRouter(prefix="/api/generate", tags=["generation"])

# In-memory job store (sufficient for v1; swap for Redis in production)
_jobs: dict[str, dict[str, Any]] = {}

VALID_SKILLS = {"Grammar & Vocabulary", "Reading", "Writing"}
VALID_DIFFICULTIES = {"easy", "medium", "hard"}

# Skill → marks → allowed question types
QUESTION_TYPE_MAP: dict[str, dict[int, list[str]]] = {
    "Grammar & Vocabulary": {
        2: ["Fill in the blanks", "Error correction", "Sentence arrangement",
            "Jumbled Sentences", "Sentence Conversion", "Cloze"],
        3: ["Fill in the blanks", "Error correction", "Sentence arrangement",
            "Jumbled Sentences", "Sentence Conversion", "Cloze"],
    },
    "Reading": {
        2: ["Reading comprehension (higher-order: analysis, application, opinion)"],
        5: ["Literal & inferential comprehension"],
        7: ["Reading comprehension (choice-based, full answers)"],
    },
    "Writing": {
        3:  ["Short functional writing"],
        5:  ["Sequencing", "Story writing", "Essay writing"],
        7:  ["Process writing / sequencing"],
        8:  ["Email writing", "Notice writing", "Report / Work report"],
        10: ["Story writing (long)"],
        14: ["Paragraph writing (choice-based)"],
    },
}


class GenerateRequest(BaseModel):
    topic_id: int
    skill: str
    marks: int
    question_type: str
    difficulty: str
    count: int = Field(default=5, ge=1, le=20)


async def _run_generation(job_id: str, state: dict[str, Any]) -> None:
    _jobs[job_id]["status"] = "running"
    try:
        result = await generation_graph.ainvoke(state)
        _jobs[job_id].update({
            "status": "completed",
            "approved": len(result.get("validated_questions", [])),
            "rejected": len(result.get("rejected_questions", [])),
            "stored_ids": result.get("stored_ids", []),
            "error": result.get("error"),
        })
    except Exception as exc:
        _jobs[job_id].update({"status": "failed", "error": str(exc)})


@router.post("")
async def trigger_generation(
    req: GenerateRequest,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
):
    """
    Start an async question generation job.
    Returns a job_id to poll with GET /api/generate/{job_id}.
    """
    # Validate skill
    if req.skill not in VALID_SKILLS:
        raise HTTPException(400, f"Invalid skill '{req.skill}'. Valid: {sorted(VALID_SKILLS)}")

    # Validate difficulty
    if req.difficulty not in VALID_DIFFICULTIES:
        raise HTTPException(400, f"Invalid difficulty '{req.difficulty}'. Valid: easy | medium | hard")

    # Validate question_type against skill+marks
    allowed_types = QUESTION_TYPE_MAP.get(req.skill, {}).get(req.marks, [])
    if allowed_types and req.question_type not in allowed_types:
        raise HTTPException(
            400,
            f"Question type '{req.question_type}' is not valid for {req.skill} ({req.marks}-mark). "
            f"Allowed: {allowed_types}",
        )

    # Ensure topic exists
    topic = await db.get(Topic, req.topic_id)
    if not topic:
        raise HTTPException(404, f"Topic {req.topic_id} not found")

    # Resolve or create pool_config
    skill_row = await db.execute(select(Skill).where(Skill.name == req.skill))
    skill = skill_row.scalars().first()
    if not skill:
        raise HTTPException(500, f"Skill '{req.skill}' not in database. Check seed data.")

    pc_result = await db.execute(
        select(PoolConfig).where(
            PoolConfig.topic_id == req.topic_id,
            PoolConfig.skill_id == skill.id,
            PoolConfig.marks == req.marks,
            PoolConfig.question_type == req.question_type,
            PoolConfig.difficulty == req.difficulty,
        )
    )
    pool_config = pc_result.scalars().first()

    if not pool_config:
        pool_config = PoolConfig(
            topic_id=req.topic_id,
            skill_id=skill.id,
            marks=req.marks,
            question_type=req.question_type,
            difficulty=req.difficulty,
            target_count=req.count,
            current_count=0,
        )
        db.add(pool_config)
        await db.commit()
        await db.refresh(pool_config)

    job_id = str(uuid.uuid4())
    initial_state: dict[str, Any] = {
        "topic_id": req.topic_id,
        "pool_config_id": pool_config.id,
        "skill": req.skill,
        "question_type": req.question_type,
        "marks": req.marks,
        "difficulty": req.difficulty,
        "count": req.count,
        "material_chunks": [],
        "reference_questions_text": "",
        "raw_questions": [],
        "validated_questions": [],
        "rejected_questions": [],
        "stored_ids": [],
        "error": None,
    }

    _jobs[job_id] = {"status": "queued", "request": req.model_dump()}
    background_tasks.add_task(_run_generation, job_id, initial_state)

    return {"job_id": job_id, "status": "queued"}


@router.get("/{job_id}")
async def get_job_status(job_id: str):
    """Poll the status of a generation job."""
    job = _jobs.get(job_id)
    if not job:
        raise HTTPException(404, f"Job {job_id} not found")
    return {"job_id": job_id, **job}

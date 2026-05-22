"""
Pool manager: checks current_count vs target_count for all pool_configs
and triggers generation to fill the gap.

Usage:
  from backend.services.pool_manager import refill_all_pools
  await refill_all_pools()

Can also be called via POST /api/pool-config/refill (registered in questions router).
"""
import asyncio
import uuid
from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.agents.generation_graph import generation_graph
from backend.db.connection import AsyncSessionLocal
from backend.db.models import PoolConfig, Skill


async def _fill_pool(pool_config_id: int, gap: int, topic_id: int, skill: str,
                     question_type: str, marks: int, difficulty: str) -> dict[str, Any]:
    """Run the generation graph to fill one pool config's gap."""
    state: dict[str, Any] = {
        "topic_id": topic_id,
        "pool_config_id": pool_config_id,
        "skill": skill,
        "question_type": question_type,
        "marks": marks,
        "difficulty": difficulty,
        "count": min(gap, 10),  # max 10 per run to avoid token limits
        "material_chunks": [],
        "reference_questions_text": "",
        "raw_questions": [],
        "validated_questions": [],
        "rejected_questions": [],
        "stored_ids": [],
        "error": None,
    }
    result = await generation_graph.ainvoke(state)
    return {
        "pool_config_id": pool_config_id,
        "requested": min(gap, 10),
        "stored": len(result.get("stored_ids", [])),
        "error": result.get("error"),
    }


async def refill_all_pools(concurrency: int = 3) -> list[dict[str, Any]]:
    """
    Check all pool configs and fill any that have current_count < target_count.
    Runs at most `concurrency` fills in parallel.
    Returns a summary of what was filled.
    """
    async with AsyncSessionLocal() as db:
        result = await db.execute(
            select(PoolConfig, Skill.name)
            .join(Skill, Skill.id == PoolConfig.skill_id)
            .where(PoolConfig.current_count < PoolConfig.target_count)
        )
        rows = result.all()

    if not rows:
        return []

    semaphore = asyncio.Semaphore(concurrency)

    async def bounded_fill(pc: PoolConfig, skill_name: str) -> dict[str, Any]:
        async with semaphore:
            return await _fill_pool(
                pool_config_id=pc.id,
                gap=pc.target_count - pc.current_count,
                topic_id=pc.topic_id,
                skill=skill_name,
                question_type=pc.question_type,
                marks=pc.marks,
                difficulty=pc.difficulty,
            )

    tasks = [bounded_fill(pc, skill_name) for pc, skill_name in rows]
    results = await asyncio.gather(*tasks, return_exceptions=True)

    return [
        r if isinstance(r, dict) else {"error": str(r)}
        for r in results
    ]

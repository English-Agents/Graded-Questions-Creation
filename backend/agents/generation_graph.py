"""
LangGraph generation workflow.

Graph: Planner → RAG → Generator → Validate (parallel) → Store
Each node takes and returns a GenerationState TypedDict.
"""
from __future__ import annotations

import asyncio
import uuid
from typing import Any, TypedDict

from langgraph.graph import END, StateGraph

from backend.agents.planner import get_skill
from backend.db.connection import AsyncSessionLocal
from backend.db.models import PoolConfig, Question, SampleQuestion
from backend.rag.retriever import embed_and_store_question, retrieve
from backend.skills.validators.bloom_check import BloomClassifier
from backend.skills.validators.difficulty_check import DifficultyChecker
from backend.skills.validators.duplicate_check import is_duplicate
from backend.skills.validators.grammar_check import GrammarChecker
from sqlalchemy import select, func


# ─────────────────────────────────────────────
# State
# ─────────────────────────────────────────────

class GenerationState(TypedDict):
    # Input
    topic_id: int
    pool_config_id: int
    skill: str
    question_type: str
    marks: int
    difficulty: str
    count: int

    # Intermediate
    material_chunks: list[str]
    reference_questions_text: str
    raw_questions: list[dict[str, Any]]

    # Output
    validated_questions: list[dict[str, Any]]  # approved
    rejected_questions: list[dict[str, Any]]   # with rejection_reason
    stored_ids: list[str]
    error: str | None


# ─────────────────────────────────────────────
# Node: RAG retrieval
# ─────────────────────────────────────────────

async def rag_node(state: GenerationState) -> GenerationState:
    topic_id = state["topic_id"]
    query = f"{state['skill']} {state['question_type']} {state['difficulty']}"

    chunks = await retrieve(topic_id, query, k=5)

    async with AsyncSessionLocal() as db:
        rows = await db.execute(
            select(SampleQuestion).where(
                SampleQuestion.topic_id == topic_id,
                SampleQuestion.skill == state["skill"],
                SampleQuestion.question_type == state["question_type"],
            ).limit(5)
        )
        samples = rows.scalars().all()

    ref_lines: list[str] = []
    for s in samples:
        line = f"Q: {s.text}"
        if s.answer_key:
            line += f"\nA: {s.answer_key}"
        ref_lines.append(line)
    reference_text = "\n\n".join(ref_lines) if ref_lines else "No reference questions available."

    return {
        **state,
        "material_chunks": chunks,
        "reference_questions_text": reference_text,
    }


# ─────────────────────────────────────────────
# Node: Question generation
# ─────────────────────────────────────────────

async def generator_node(state: GenerationState) -> GenerationState:
    skill_instance = get_skill(state["skill"])

    reading_material = "\n\n---\n\n".join(state["material_chunks"]) or "No material available."

    raw = skill_instance.forward(
        reading_material=reading_material,
        reference_questions=state["reference_questions_text"],
        skill=state["skill"],
        question_type=state["question_type"],
        marks=state["marks"],
        difficulty=state["difficulty"],
        count=state["count"],
    )

    return {**state, "raw_questions": raw}


# ─────────────────────────────────────────────
# Node: Validation (parallel per question)
# ─────────────────────────────────────────────

_grammar_checker: GrammarChecker | None = None
_difficulty_checker: DifficultyChecker | None = None
_bloom_classifier: BloomClassifier | None = None


def _get_validators() -> tuple[GrammarChecker, DifficultyChecker, BloomClassifier]:
    global _grammar_checker, _difficulty_checker, _bloom_classifier
    if _grammar_checker is None:
        _grammar_checker = GrammarChecker()
        _difficulty_checker = DifficultyChecker()
        _bloom_classifier = BloomClassifier()
    return _grammar_checker, _difficulty_checker, _bloom_classifier


async def _validate_single(
    question: dict[str, Any],
    state: GenerationState,
) -> tuple[dict[str, Any], str | None]:
    """
    Validate one question. Returns (enriched_question, rejection_reason | None).
    Runs grammar, difficulty, bloom checks synchronously (DSPy is sync).
    Runs duplicate check asynchronously.
    """
    text = question.get("text", "")
    if not text:
        return question, "Empty question text"

    grammar_checker, difficulty_checker, bloom_classifier = _get_validators()

    # Grammar check (sync DSPy call — run in thread pool)
    loop = asyncio.get_event_loop()

    grammar_ok, grammar_reason = await loop.run_in_executor(
        None,
        lambda: grammar_checker.forward(
            question_text=text,
            skill=state["skill"],
            question_type=state["question_type"],
            marks=state["marks"],
        ),
    )
    if not grammar_ok:
        return question, f"Grammar: {grammar_reason}"

    # Difficulty check
    diff_ok, actual_level, diff_reason = await loop.run_in_executor(
        None,
        lambda: difficulty_checker.forward(
            question_text=text,
            requested_difficulty=state["difficulty"],
        ),
    )
    if not diff_ok:
        return question, f"Difficulty mismatch ({actual_level}): {diff_reason}"

    # Bloom classification (enriches, doesn't reject)
    bloom_level_from_llm = question.get("bloom_level")
    if not bloom_level_from_llm or not isinstance(bloom_level_from_llm, int):
        bloom_level, _ = await loop.run_in_executor(
            None,
            lambda: bloom_classifier.forward(question_text=text),
        )
        question = {**question, "bloom_level": bloom_level}

    # Duplicate check (async)
    dup, similar_id, score = await is_duplicate(state["topic_id"], text)
    if dup:
        return question, f"Duplicate (similarity={score:.2f}, similar_id={similar_id})"

    return question, None


async def validation_node(state: GenerationState) -> GenerationState:
    raw_questions = state.get("raw_questions", [])
    if not raw_questions:
        return {**state, "validated_questions": [], "rejected_questions": [], "error": "Generator returned no questions"}

    tasks = [_validate_single(q, state) for q in raw_questions]
    results = await asyncio.gather(*tasks, return_exceptions=True)

    validated: list[dict] = []
    rejected: list[dict] = []

    for q, result in zip(raw_questions, results):
        if isinstance(result, Exception):
            rejected.append({**q, "rejection_reason": str(result)})
        else:
            enriched, reason = result
            if reason is None:
                validated.append(enriched)
            else:
                rejected.append({**enriched, "rejection_reason": reason})

    return {**state, "validated_questions": validated, "rejected_questions": rejected}


# ─────────────────────────────────────────────
# Node: Store to PostgreSQL + ChromaDB
# ─────────────────────────────────────────────

async def store_node(state: GenerationState) -> GenerationState:
    stored_ids: list[str] = []

    async with AsyncSessionLocal() as db:
        for q in state.get("validated_questions", []):
            qid = str(uuid.uuid4())
            question = Question(
                id=uuid.UUID(qid),
                pool_config_id=state["pool_config_id"],
                text=q.get("text", ""),
                question_type=state["question_type"],
                marks=state["marks"],
                difficulty=state["difficulty"],
                bloom_level=q.get("bloom_level"),
                answer_key=q.get("answer_key"),
                options=q.get("options"),
                validation_status="approved",
                chroma_id=qid,
            )
            db.add(question)

            # Embed and store in ChromaDB for future dedup
            try:
                await embed_and_store_question(qid, state["topic_id"], q.get("text", ""))
            except Exception:
                pass  # dedup storage failure is non-critical

            stored_ids.append(qid)

        # Update current_count in pool_config
        if stored_ids:
            pool_cfg = await db.get(PoolConfig, state["pool_config_id"])
            if pool_cfg:
                pool_cfg.current_count = (pool_cfg.current_count or 0) + len(stored_ids)

        # Store rejected questions too (for review)
        for q in state.get("rejected_questions", []):
            qid = str(uuid.uuid4())
            question = Question(
                id=uuid.UUID(qid),
                pool_config_id=state["pool_config_id"],
                text=q.get("text", ""),
                question_type=state["question_type"],
                marks=state["marks"],
                difficulty=state["difficulty"],
                bloom_level=q.get("bloom_level"),
                answer_key=q.get("answer_key"),
                options=q.get("options"),
                validation_status="rejected",
                rejection_reason=q.get("rejection_reason"),
            )
            db.add(question)

        await db.commit()

    return {**state, "stored_ids": stored_ids}


# ─────────────────────────────────────────────
# Build graph
# ─────────────────────────────────────────────

def build_generation_graph():
    workflow = StateGraph(GenerationState)

    workflow.add_node("rag", rag_node)
    workflow.add_node("generator", generator_node)
    workflow.add_node("validator", validation_node)
    workflow.add_node("store", store_node)

    workflow.set_entry_point("rag")
    workflow.add_edge("rag", "generator")
    workflow.add_edge("generator", "validator")
    workflow.add_edge("validator", "store")
    workflow.add_edge("store", END)

    return workflow.compile()


generation_graph = build_generation_graph()

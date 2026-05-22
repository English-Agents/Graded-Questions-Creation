"""
Planner agent: selects the correct DSPy skill based on skill name.
Uses a simple registry instead of SkillsReActAgent since we know the skill
at request time from the user's selection (skill is explicit, not inferred).
"""
from __future__ import annotations

import dspy

from backend.config import settings
from backend.skills.grammar_skill import GrammarSkill
from backend.skills.reading_skill import ReadingSkill
from backend.skills.writing_skill import WritingSkill

SKILL_REGISTRY: dict[str, type] = {
    "Grammar & Vocabulary": GrammarSkill,
    "Reading": ReadingSkill,
    "Writing": WritingSkill,
}

_lm: dspy.LM | None = None
_skill_instances: dict[str, object] = {}


def _get_lm() -> dspy.LM:
    global _lm
    if _lm is None:
        if settings.llm_provider == "anthropic":
            _lm = dspy.LM(
                model=f"anthropic/{settings.llm_model}",
                api_key=settings.anthropic_api_key,
            )
        else:
            _lm = dspy.LM(
                model=f"openai/{settings.llm_model}",
                api_key=settings.openai_api_key,
            )
        dspy.configure(lm=_lm)
    return _lm


def get_skill(skill_name: str) -> object:
    """Return a cached DSPy skill instance for the given skill name."""
    _get_lm()  # ensure LM is configured
    if skill_name not in _skill_instances:
        skill_class = SKILL_REGISTRY.get(skill_name)
        if skill_class is None:
            raise ValueError(
                f"Unknown skill '{skill_name}'. Valid skills: {list(SKILL_REGISTRY)}"
            )
        _skill_instances[skill_name] = skill_class()
    return _skill_instances[skill_name]

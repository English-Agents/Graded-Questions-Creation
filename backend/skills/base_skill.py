"""
Base DSPy skill for question generation.
GrammarSkill, ReadingSkill, WritingSkill all subclass TopicSkill.
"""
from __future__ import annotations

import json
from typing import Any

import dspy


class GenerateQuestionsSignature(dspy.Signature):
    """
    You are an expert English language assessment author.
    Generate high-quality assessment questions from the provided reading material and
    reference examples. Follow the exact question type, difficulty level, and marks value.
    Return ONLY a valid JSON array of question objects — no extra text.

    Each object must have these keys:
      text          : the question text (use ___ for fill-in-the-blank)
      answer_key    : correct answer or model answer
      options       : {a, b, c, d, correct} if the question is choice-based, else null
      bloom_level   : integer 1–6 (K1=Remember…K6=Create)
    """

    reading_material: str = dspy.InputField(desc="Relevant reading material chunks from the topic")
    reference_questions: str = dspy.InputField(desc="Sample questions that show the expected format and style")
    skill: str = dspy.InputField(desc="Skill area: Grammar & Vocabulary | Reading | Writing")
    question_type: str = dspy.InputField(desc="Specific question type, e.g. 'Fill in the blanks'")
    marks: int = dspy.InputField(desc="Marks value for each question")
    difficulty: str = dspy.InputField(desc="Difficulty level: easy | medium | hard")
    count: int = dspy.InputField(desc="Number of questions to generate")
    questions_json: str = dspy.OutputField(desc="JSON array of question objects")


class TopicSkill(dspy.Module):
    """Base question generation skill. Subclass for skill-specific few-shot examples."""

    def __init__(self) -> None:
        super().__init__()
        self.generate = dspy.ChainOfThought(GenerateQuestionsSignature)

    def forward(
        self,
        reading_material: str,
        reference_questions: str,
        skill: str,
        question_type: str,
        marks: int,
        difficulty: str,
        count: int,
    ) -> list[dict[str, Any]]:
        result = self.generate(
            reading_material=reading_material,
            reference_questions=reference_questions,
            skill=skill,
            question_type=question_type,
            marks=marks,
            difficulty=difficulty,
            count=count,
        )
        return _parse_questions_json(result.questions_json, count)


def _parse_questions_json(raw: str, expected_count: int) -> list[dict[str, Any]]:
    """Parse the LLM's JSON output robustly."""
    raw = raw.strip()
    # Strip markdown code fences if present
    if raw.startswith("```"):
        lines = raw.split("\n")
        raw = "\n".join(lines[1:-1] if lines[-1].strip() == "```" else lines[1:])
    try:
        parsed = json.loads(raw)
        if isinstance(parsed, list):
            return parsed[:expected_count]
        if isinstance(parsed, dict) and "questions" in parsed:
            return parsed["questions"][:expected_count]
    except json.JSONDecodeError:
        pass
    # Fallback: return empty — caller will handle re-try or rejection
    return []

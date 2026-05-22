"""
Reading comprehension question generation skill.
Covers: Higher-order comprehension (2-mark), Literal & inferential (5-mark),
        Choice-based full answers (7-mark).
"""
import dspy

from backend.skills.base_skill import TopicSkill

READING_FEW_SHOT_EXAMPLES = [
    dspy.Example(
        reading_material=(
            "Radhika is a second-year engineering student who lives in Hyderabad. "
            "Every morning she wakes up at 6 a.m. and exercises for thirty minutes."
        ),
        reference_questions=(
            "skill: Reading, type: Literal & inferential comprehension, marks: 5, difficulty: medium\n"
            "Q: Why did Radhika wake up late?\n"
            "A: She was studying until midnight."
        ),
        skill="Reading",
        question_type="Literal & inferential comprehension",
        marks=5,
        difficulty="medium",
        count=1,
        questions_json=(
            '[{"text": "What does Radhika do every morning after waking up?", '
            '"answer_key": "After waking up, Radhika exercises for thirty minutes before preparing breakfast.", '
            '"options": null, "bloom_level": 2}]'
        ),
    ),
]


class ReadingSkill(TopicSkill):
    """Reading comprehension question generation with few-shot examples."""

    def __init__(self) -> None:
        super().__init__()

"""
Writing task question generation skill.
Covers: Short functional writing (3-mark), Sequencing/Story/Essay (5-mark),
        Process writing (7-mark), Email/Notice/Report (8-mark),
        Story writing long (10-mark), Paragraph writing (14-mark).
"""
import dspy

from backend.skills.base_skill import TopicSkill

WRITING_FEW_SHOT_EXAMPLES = [
    dspy.Example(
        reading_material=(
            "Email writing requires a clear subject line, formal greeting, body paragraphs, "
            "and a polite closing. Emails should be concise and professional."
        ),
        reference_questions=(
            "skill: Writing, type: Email writing, marks: 8, difficulty: easy\n"
            "Q: Write an email to your teacher requesting leave.\n"
            "A: Subject: Request for Leave\nDear [Teacher],\n..."
        ),
        skill="Writing",
        question_type="Email writing",
        marks=8,
        difficulty="medium",
        count=1,
        questions_json=(
            '[{"text": "You are Ramesh, a software engineer. Write an email to your project manager '
            'requesting a one-week extension for the project deadline. Include the reason for the delay '
            'and assure timely completion.", '
            '"answer_key": "Subject: Request for Project Deadline Extension\\n\\nDear [Manager],\\n\\n'
            'I am writing to request a one-week extension for the [Project Name] deadline...\\n\\n'
            'Yours sincerely,\\nRamesh", '
            '"options": null, "bloom_level": 3}]'
        ),
    ),
]


class WritingSkill(TopicSkill):
    """Writing task question generation with few-shot examples."""

    def __init__(self) -> None:
        super().__init__()

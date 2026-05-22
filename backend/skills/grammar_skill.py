"""
Grammar & Vocabulary question generation skill.
Covers: Fill in the blanks, Error correction, Sentence arrangement,
        Jumbled Sentences, Sentence Conversion, Cloze.
"""
import dspy

from backend.skills.base_skill import TopicSkill

GRAMMAR_FEW_SHOT_EXAMPLES = [
    dspy.Example(
        reading_material="She goes to school every day. (simple present, third-person singular)",
        reference_questions='skill: Grammar & Vocabulary, type: Fill in the blanks, marks: 2, difficulty: easy\nQ: She ___ (go) to school every day.\nA: goes',
        skill="Grammar & Vocabulary",
        question_type="Fill in the blanks",
        marks=2,
        difficulty="easy",
        count=1,
        questions_json='[{"text": "He ___ (write) reports every Friday.", "answer_key": "writes", "options": null, "bloom_level": 1}]',
    ),
    dspy.Example(
        reading_material="They were playing cricket at 4 p.m. (past continuous)",
        reference_questions='skill: Grammar & Vocabulary, type: Error correction, marks: 2, difficulty: medium\nQ: They was playing football when it rained.\nA: They were playing football when it rained.',
        skill="Grammar & Vocabulary",
        question_type="Error correction",
        marks=2,
        difficulty="medium",
        count=1,
        questions_json='[{"text": "She were sitting in the library when the bell ringed.", "answer_key": "She was sitting in the library when the bell rang.", "options": null, "bloom_level": 3}]',
    ),
]


class GrammarSkill(TopicSkill):
    """Grammar & Vocabulary question generation with few-shot examples."""

    def __init__(self) -> None:
        super().__init__()
        # Register few-shot examples for better output quality
        self.generate = dspy.ChainOfThought(
            self.generate.signature,  # reuse parent's signature
        )

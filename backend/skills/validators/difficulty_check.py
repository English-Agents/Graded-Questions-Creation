"""
Difficulty level validator.
Verifies that the generated question matches the requested difficulty level
based on cognitive demand, vocabulary, and sentence complexity.
"""
import dspy

DIFFICULTY_GUIDELINES = """
easy   → Tests recall and recognition (Bloom K1-K2). Simple sentences, common vocabulary, direct questions.
medium → Tests understanding and application (Bloom K3-K4). Moderate complexity, contextual reasoning required.
hard   → Tests analysis, evaluation, or creation (Bloom K5-K6). Complex sentences, inference, critical thinking.
"""


class DifficultyCheckSignature(dspy.Signature):
    """
    You are an English assessment design expert.
    Evaluate whether the question matches the requested difficulty level based on
    cognitive demand, vocabulary complexity, and depth of reasoning required.

    Difficulty guidelines:
    {difficulty_guidelines}

    Return:
      matches       : true if the question difficulty matches the requested level
      actual_level  : what difficulty level you assess this question to actually be (easy | medium | hard)
      reason        : brief explanation (1–2 sentences)
    """
    difficulty_guidelines: str = dspy.InputField(desc="Difficulty level descriptions")
    question_text: str = dspy.InputField()
    requested_difficulty: str = dspy.InputField()
    matches: bool = dspy.OutputField()
    actual_level: str = dspy.OutputField()
    reason: str = dspy.OutputField()


class DifficultyChecker(dspy.Module):
    def __init__(self) -> None:
        super().__init__()
        self.check = dspy.ChainOfThought(DifficultyCheckSignature)

    def forward(self, question_text: str, requested_difficulty: str) -> tuple[bool, str, str]:
        """Returns (matches, actual_level, reason)."""
        result = self.check(
            difficulty_guidelines=DIFFICULTY_GUIDELINES,
            question_text=question_text,
            requested_difficulty=requested_difficulty,
        )
        matches = result.matches if isinstance(result.matches, bool) else str(result.matches).lower() == "true"
        return matches, result.actual_level or requested_difficulty, result.reason or ""

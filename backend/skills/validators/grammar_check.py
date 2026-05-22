"""
Grammar quality validator.
Checks whether a generated question is linguistically correct and well-formed.
"""
import dspy


class GrammarCheckSignature(dspy.Signature):
    """
    You are an expert English language editor.
    Evaluate whether the given assessment question is grammatically correct,
    clearly worded, and appropriate for the stated skill and marks value.

    Return:
      passed   : true if the question passes quality review, false otherwise
      reason   : brief explanation (1–2 sentences); empty string if passed
    """
    question_text: str = dspy.InputField()
    skill: str = dspy.InputField()
    question_type: str = dspy.InputField()
    marks: int = dspy.InputField()
    passed: bool = dspy.OutputField()
    reason: str = dspy.OutputField()


class GrammarChecker(dspy.Module):
    def __init__(self) -> None:
        super().__init__()
        self.check = dspy.Predict(GrammarCheckSignature)

    def forward(self, question_text: str, skill: str, question_type: str, marks: int) -> tuple[bool, str]:
        result = self.check(
            question_text=question_text,
            skill=skill,
            question_type=question_type,
            marks=marks,
        )
        passed = result.passed if isinstance(result.passed, bool) else str(result.passed).lower() == "true"
        return passed, result.reason or ""

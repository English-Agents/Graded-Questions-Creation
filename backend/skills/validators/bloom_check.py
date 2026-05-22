"""
Bloom's taxonomy classifier.
Assigns a Bloom level (1–6) to a generated question.
"""
import dspy

BLOOM_DEFINITIONS = """
K1 Remember     : Recall facts and basic concepts (define, list, recall, identify)
K2 Understand   : Explain ideas or concepts (describe, explain, summarise, classify)
K3 Apply        : Use information in new situations (use, demonstrate, solve, complete)
K4 Analyse      : Draw connections, break into parts (compare, contrast, organise, distinguish)
K5 Evaluate     : Justify a decision or course of action (assess, argue, defend, judge)
K6 Create       : Produce new or original work (design, construct, compose, formulate)
"""


class BloomClassifySignature(dspy.Signature):
    """
    You are an educational assessment expert in Bloom's taxonomy.
    Given a question, identify its Bloom's level (1–6).

    Bloom level definitions:
    {bloom_definitions}

    Return:
      bloom_level : integer 1–6
      bloom_label : one of Remember|Understand|Apply|Analyse|Evaluate|Create
      rationale   : one-sentence explanation
    """
    bloom_definitions: str = dspy.InputField()
    question_text: str = dspy.InputField()
    bloom_level: int = dspy.OutputField()
    bloom_label: str = dspy.OutputField()
    rationale: str = dspy.OutputField()


class BloomClassifier(dspy.Module):
    def __init__(self) -> None:
        super().__init__()
        self.classify = dspy.Predict(BloomClassifySignature)

    def forward(self, question_text: str) -> tuple[int, str]:
        """Returns (bloom_level, bloom_label)."""
        result = self.classify(
            bloom_definitions=BLOOM_DEFINITIONS,
            question_text=question_text,
        )
        level = int(result.bloom_level) if str(result.bloom_level).isdigit() else 3
        level = max(1, min(6, level))
        return level, result.bloom_label or "Apply"

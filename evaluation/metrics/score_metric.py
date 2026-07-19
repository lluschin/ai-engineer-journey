from evaluation.metrics.metric import Metric
from evaluation.model.question import QuestionResult


class ScoreMetric(Metric):
    name = "score"

    def evaluate(self, result: QuestionResult) -> float | None:
        answer = result.answer.casefold()
        expected_terms = result.question.must_contain
        expected_groups = result.question.any_group
        total = len(expected_terms) + len(expected_groups)

        if total == 0:
            return None

        satisfied = sum(
            term.casefold() in answer
            for term in expected_terms
        )
        satisfied += sum(
            any(term.casefold() in answer for term in group)
            for group in expected_groups
        )

        return round(satisfied / total * 100, 2)

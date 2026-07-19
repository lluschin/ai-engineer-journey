from evaluation.metrics.metric import Metric
from evaluation.model.question import QuestionResult


class RecallMetric(Metric):
    name = "recall"

    def evaluate(self, result: QuestionResult) -> float | None:
        expected = set(result.question.expected_chunks)

        if not expected:
            return None

        retrieved = set(result.retrieval_sources)
        return len(expected & retrieved) / len(expected)

from evaluation.metrics.metric import Metric
from evaluation.model.question import QuestionResult


class PrecisionMetric(Metric):
    name = "precision"

    def evaluate(self, result: QuestionResult) -> float | None:
        retrieved = set(result.retrieval_sources)

        if not retrieved:
            return None

        expected = set(result.question.expected_chunks)
        return len(expected & retrieved) / len(retrieved)

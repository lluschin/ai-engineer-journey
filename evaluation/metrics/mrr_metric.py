from evaluation.metrics.metric import Metric
from evaluation.model.question import QuestionResult


class MRRMetric(Metric):
    name = "mrr"

    def evaluate(self, result: QuestionResult) -> float | None:
        expected = set(result.question.expected_chunks)

        if not expected:
            return None

        for rank, source_id in enumerate(result.retrieval_sources, start=1):
            if source_id in expected:
                return 1.0 / rank

        return 0.0

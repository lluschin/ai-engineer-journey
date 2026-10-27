from evaluation.metrics.metric import Metric
from evaluation.model.question import QuestionResult

from evaluation.utils import helpers


class PrecisionMetric(Metric):
    NAME = "precision"

    def __init__(self, name):
        self.stage_name = name
        super().__init__(".".join([PrecisionMetric.NAME, self.stage_name]))


    def evaluate(self, result: QuestionResult) -> float | None:
        expected = set(result.question.expected_chunks)

        stage = helpers.findStageByName(
            result.chat_response.stages,
            self.stage_name,
        )

        if not stage:
            raise KeyError(f"{self.stage_name} not found.")

        retrieved = {
            source["id"]
            for source in stage.output["sources"]
        }

        if not retrieved:
            return None

        return len(expected & retrieved) / len(retrieved)

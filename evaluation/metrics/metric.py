from abc import ABC, abstractmethod

from evaluation.model.question import QuestionResult


class Metric(ABC):
    name: str

    @abstractmethod
    def evaluate(self, result: QuestionResult) -> float | None:
        """Calculate this metric for one evaluated question."""

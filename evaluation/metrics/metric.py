# ===== workaround for cyclic import =====
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from evaluation.model.question import QuestionResult
# ========================================

from abc import ABC, abstractmethod


class Metric(ABC):

    def __init__(self, name):
        self.name = name


    @abstractmethod
    def evaluate(self, result: QuestionResult) -> float | None:
        """Calculate this metric for one evaluated question."""

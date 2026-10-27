from pydantic import BaseModel,ConfigDict, Field

from evaluation.metrics.metric import Metric
from src.utils.models.stage_model import StageIdx
from src.models.chat_models import (
    ChatResponse,
)

class Configuration(BaseModel):
    filepath: str
    title: str

    llm_service: str
    llm_model: str

    retrieval_service: str
    retrieval_model: str
    retrieval_top_k: int

    ranker_service: str

    context_builder_service: str

    query_expander_service: str


class Question(BaseModel):
    question: str
    must_contain: list[str] = Field(default_factory=list)
    any_group: list[list[str]] = Field(default_factory=list)
    expected_chunks: list[str] = Field(default_factory=list)


class Experiment(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    configuration: Configuration
    questions: list[Question]
    metrics: list[Metric]


class Runtime(BaseModel):
    total_runtime: float
    stage_runtimes: dict[StageIdx, float | None]


class QuestionResult(BaseModel):
    question: Question
    chat_response: ChatResponse
    request_runtime: float
    metrics: dict[str, float | None] = Field(default_factory=dict)


class ExperimentResult(BaseModel):
    run_id: str
    configuration: Configuration

    question_results: list[QuestionResult] = Field(default_factory=list)
    median_runtime: Runtime | None = None
    metrics: dict[str, float | None] = Field(default_factory=dict)

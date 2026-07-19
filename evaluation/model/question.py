from pydantic import BaseModel, Field


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
    configuration: Configuration
    questions: list[Question]


class Runtime(BaseModel):
    total_runtime: float
    query_expansion_runtime: float | None = None
    retrieval_runtime: float | None = None
    reranking_runtime: float | None = None
    context_building_runtime: float | None = None
    llm_call_runtime: float | None = None


class QuestionResult(BaseModel):
    question: Question

    answer: str
    retrieval_sources: list[str]
    runtime: Runtime
    metrics: dict[str, float | None] = Field(default_factory=dict)


class ExperimentResult(BaseModel):
    run_id: str
    configuration: Configuration

    question_results: list[QuestionResult] = Field(default_factory=list)
    median_runtime: Runtime | None = None
    metrics: dict[str, float | None] = Field(default_factory=dict)

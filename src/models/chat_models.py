from typing import Any
from pydantic import BaseModel, Field

class Runtime(BaseModel):
    query_processing_runtime: float = -1
    retrieval_runtime: float = -1
    reranking_runtime: float = -1
    compression_runtime: float = -1
    context_building_runtime: float = -1
    llm_call_runtime:float = -1


class Stage(BaseModel):
    name: str
    runtime: float = -1
    params: dict[str, Any] = Field(default_factory=dict)
    input: dict[str, Any] = Field(default_factory=dict)
    output: dict[str, Any] = Field(default_factory=dict)


class Source(BaseModel):
    id: str
    document: str
    score: float


class Environment(BaseModel):
    filepath: str


class ChatRequest(BaseModel):
    user: str = Field(..., min_length=3)
    message: str = Field(..., min_length=1, max_length=1000)
    source: str | None = None


class SimpleChatResponse(BaseModel):
    message: str
    llm_model: str


class ChatResponse(BaseModel):
    input_request: ChatRequest
    response: str
    stages: list[Stage] = Field(default_factory=list)


class EmptyMessageException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

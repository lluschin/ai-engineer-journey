from pydantic import BaseModel, Field

class Runtime(BaseModel):
    query_expansion_runtime: float = -1
    retrieval_runtime: float = -1
    reranking_runtime: float = -1
    context_building_runtime: float = -1
    llm_call_runtime:float = -1

class Source(BaseModel):
    id: str
    document: str
    score: float


class Environment(BaseModel):
    filepath: str


class ChatRequest(BaseModel):
    user: str = Field(..., min_length=3)
    message: str = Field(..., min_length=1, max_length=1000)


class ChatResponse(BaseModel):
    message: str
    llm_model: str
    retrieval_model: str
    chunk_size: int
    top_k: int
    context_builder: str
    used_sources: int
    ranking: str
    sources: list[Source] = Field(default_factory=list)
    runtime: Runtime


class EmptyMessageException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

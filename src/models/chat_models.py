from pydantic import BaseModel, Field


class Source(BaseModel):
    document: str
    score: float


class ChatRequest(BaseModel):
    user: str = Field(..., min_length=3)
    message: str = Field(..., min_length=1, max_length=1000)


class ChatResponse(BaseModel):
    message: str
    llm_model: str
    retrieval_model: str
    chunk_size: int
    top_k: int
    context_builder: float
    used_sources: int
    ranking: str
    sources: list[Source] = Field(default_factory=list)


class EmptyMessageException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

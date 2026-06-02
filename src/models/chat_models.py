from pydantic import BaseModel, Field

class ChatRequest(BaseModel):
    user: str = Field(..., min_length=3)
    message: str = Field(..., min_length=1, max_length=1000)


class ChatResponse(BaseModel):
    message: str
    model: str


class EmptyMessageException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

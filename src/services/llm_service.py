from abc import ABC, abstractmethod

from models.chat_models import ChatResponse

class LLMService(ABC):

    @abstractmethod
    async def createResponse(self, msg: str) -> str:
        pass

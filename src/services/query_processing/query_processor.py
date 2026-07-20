
from abc import ABC, abstractmethod

class QueryProcessor(ABC):

    @abstractmethod
    async def process(self, query: str) -> str:
        pass
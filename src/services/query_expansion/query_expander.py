
from abc import ABC, abstractmethod

class QueryExpander(ABC):

    @abstractmethod
    async def expand(self, query: str) -> str:
        pass
import logging
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)

class LLMService(ABC):

    def __init__(self, model, client):
        self.model = model
        self.client = client

        logger.info(f"use model {self.model}")
        

    async def chat(self, query: str) -> str:
        return await self._create_response(query)


    async def rag_chat(self, query: str, context: list[str]) -> str:
        context_text = "\n\n".join(context)

        prompt= f"""
        Use the following context to answer the question.
        If the context contains information to answer the question, use it.
        If the answer is not contained in the context, say you cant find the answer.

        Context:
        {context_text}

        Question:
        {query}
        """
        
        return await self._create_response(prompt)


    @abstractmethod
    async def _create_response(self, prompt: str) -> str:
        pass
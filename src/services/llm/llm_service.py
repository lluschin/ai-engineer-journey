from abc import ABC, abstractmethod

from models.chat_models import ChatResponse

class LLMService(ABC):

    async def chat(self, query: str) -> str:
        return await self._createResponse(query)


    async def ragChat(self, query: str, context: list[str]) -> str:
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
        
        return await self._createResponse(prompt)


    @abstractmethod
    async def _createResponse(self, prompt: str) -> str:
        pass
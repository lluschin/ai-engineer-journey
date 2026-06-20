import os
from openai import AsyncOpenAI

from services.llm_service import LLMService

class OpenAIService(LLMService):

    def __init__(self):
        self.client = AsyncOpenAI()
        self.model = os.getenv("OPENAI_MODEL")
    

    async def createResponse(self, msg: str) -> str:
        response = await self.client.responses.create(
            model=self.model,
            input=msg
        )

        return response.output_text
    

    async def createRagResponse(self, question: str, context: list[str]) -> str:
        context_text = "\n\n".join(context)

        prompt= f"""
        Use the following context to answer the question.
        If the context contains information to answer the question, use it.
        If the answer is not contained in the context, say you cant find the answer.

        Context:
        {context_text}

        Question:
        {question}
        """
    
        response = await self.client.responses.create(
            model=self.model,
            input=prompt
        )

        return response.output_text
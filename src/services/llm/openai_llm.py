import os
from openai import AsyncOpenAI

from services.llm.llm_service import LLMService

class OpenAILLM(LLMService):

    def __init__(self):
        self.client = AsyncOpenAI()
        self.model = os.getenv("LLM_MODEL")


    async def _createResponse(self, prompt: str) -> str:
        response = await self.client.responses.create(
            model=self.model,
            input=prompt
        )

        return response.output_text

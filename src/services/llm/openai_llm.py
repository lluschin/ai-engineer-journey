import os
from openai import AsyncOpenAI

from services.llm.llm_service import LLMService

class OpenAILLM(LLMService):

    def __init__(self):
        model = os.getenv("LLM_MODEL")
        client = AsyncOpenAI()
        super().__init__(model, client)


    async def _create_response(self, prompt: str) -> str:
        response = await self.client.responses.create(
            model=self.model,
            input=prompt
        )

        return response.output_text

from openai import AsyncOpenAI
from services.llm.llm_service import LLMService

class OpenAiLLM(LLMService):

    def __init__(self, model):
        client = AsyncOpenAI()
        super().__init__(model, client)


    async def _create_response(self, prompt: str) -> str:
        response = await self.client.responses.create(
            model=self.model,
            input=prompt
        )

        return response.output_text

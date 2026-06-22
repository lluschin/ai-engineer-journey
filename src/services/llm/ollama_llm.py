import os
from ollama import AsyncClient
from services.llm.llm_service import LLMService

class OllamaLMM(LLMService):

    def __init__(self):
        self.client = AsyncClient()
        self.model = os.getenv("LLM_MODEL")
    

    async def _createResponse(self, prompt: str) -> str:
        response = await self.client.chat(
            model=self.model,
            messages=[{'role': 'user', 'content': prompt}]
        )

        return response.message.content

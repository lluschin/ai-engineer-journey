from ollama import AsyncClient
from services.llm.llm_service import LLMService

class OllamaLLM(LLMService):

    def __init__(self, model):
        client = AsyncClient()
        super().__init__(model, client)
    

    async def _create_response(self, prompt: str) -> str:
        response = await self.client.chat(
            model=self.model,
            messages=[{'role': 'user', 'content': prompt}]
        )

        return response.message.content

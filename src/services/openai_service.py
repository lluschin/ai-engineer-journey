from openai import AsyncOpenAI

from config.settings import Settings, loadSettings
from services.llm_service import LLMService

class OpenAIService(LLMService):

    def __init__(self):
        settings: Settings = loadSettings()

        self.client = AsyncOpenAI()
        self.model = settings.openai_model
    

    async def createResponse(self, msg: str):
        response = await self.client.responses.create(
            model=self.model,
            input=msg
        )

        return response.output_text
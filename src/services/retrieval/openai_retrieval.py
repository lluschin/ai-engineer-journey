import os

from openai import AsyncOpenAI
from services.retrieval.retrieval_service import RetrievalService


class OpenAiRetrieval(RetrievalService):

    QDRANT_COLLECTION = "AiJourney_text-embedding-3-small"

    def __init__(self):
        client = AsyncOpenAI()
        model = os.getenv("RETRIEVAL_MODEL")
        qdrant_collection_name = OpenAiRetrieval.QDRANT_COLLECTION
        super().__init__(model, client, qdrant_collection_name)


    async def _create_embedding(self, query: str):
        embedding = await self.client.embeddings.create(
            model=self.model,
            input=query
        )

        return embedding.data[0].embedding

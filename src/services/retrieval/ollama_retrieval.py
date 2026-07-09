from ollama import AsyncClient
from services.retrieval.retrieval_service import RetrievalService


class OllamaRetrieval(RetrievalService):

    QDRANT_COLLECTION = "AiJourney"

    def __init__(self, model, k):
        client = AsyncClient()
        qdrant_collection_name = "_".join([OllamaRetrieval.QDRANT_COLLECTION, model])
        super().__init__(
            model,
            client,
            qdrant_collection_name,
            k
        )


    async def _create_embedding(self, query: str):
        embedding = await self.client.embed(
            model=self.model,
            input=query
        )

        return embedding['embeddings'][0]
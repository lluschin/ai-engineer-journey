import os
from ollama import AsyncClient

from services.retrieval.retrieval_service import RetrievalService


class OllamaRetrieval(RetrievalService):

    QDRANT_COLLECTION = "AiJourney"
    
    NOMIC_EMBED_TEXT = "nomic-embed-text"
    BGE_M3 ="bge-m3"
    

    def __init__(self):
        client = AsyncClient()
        model = os.getenv("RETRIEVAL_MODEL")
        qdrant_collection_name = "_".join([OllamaRetrieval.QDRANT_COLLECTION, model])
        super().__init__(model, client, qdrant_collection_name)


    async def _create_embedding(self, query: str):
        
        embedding = await self.client.embed(
            model=self.model,
            input=query
            )

        return embedding['embeddings'][0]
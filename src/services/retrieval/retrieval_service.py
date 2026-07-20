import logging

from services.chunking_service import ChunkService
from services.qdrant_service import QdrantService
from models.chat_models import Source

logger = logging.getLogger(__name__)

from abc import ABC, abstractmethod

class RetrievalService(ABC):

    def __init__(self, model, client, qdrant_collection_name:str, k: int):
        self.model = model
        self.client = client
        self.qdrant = QdrantService(qdrant_collection_name)
        self.chunking = ChunkService()
        self.k = k


    def ingest_text(self, text: str):
        chunks = self.chunking.chunk_by_paragraph(text)
        self.add_documents(chunks)


    async def add_documents(self, docs: list[str]):
        logger.info(f"Documents added: {docs}")
        for doc in docs:
            embedding = await self._create_embedding(doc)
            self.qdrant.upload_embedding(embedding, doc)


    async def search(self, query: str) -> list[Source]:
        logger.info(f"Searching for embeddings.")
        embedding = await self._create_embedding(query)

        top_k_results = await self.qdrant.search(embedding, self.k)

        if not top_k_results:
            raise RuntimeError(
                f"Retrieval returned no embedding for query {query!r}"
            )

        return top_k_results


    @abstractmethod
    async def _create_embedding(self, query: str):
        pass

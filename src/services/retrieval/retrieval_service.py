import logging
import uuid

from pathlib import Path

from src.services.chunking_service import ChunkService
from src.services.qdrant_service import QdrantService
from src.models.chat_models import Source

logger = logging.getLogger(__name__)

from abc import ABC, abstractmethod

class RetrievalService(ABC):

    def __init__(self, model, client, qdrant_collection_name:str, k: int):
        self.model = model
        self.client = client
        self.qdrant = QdrantService(qdrant_collection_name)
        self.chunking = ChunkService()
        self.k = k
        self.offset = None


    async def ingest_text(self, filePath: Path):
        with open(filePath, 'r') as fp:
            text = fp.read()      

        chunks = self.chunking.chunk_by_paragraph(text)
        for i, chunk in enumerate(chunks):
            logger.info(f"add document: {chunk}")

            name = filePath.name + str(i) + chunk
            id = str(uuid.uuid5(uuid.NAMESPACE_DNS, name))
            embedding = await self._create_embedding(chunk)

            self.qdrant.upload_embedding(
                id=id,
                vec=embedding,
                doc=chunk,
            )


    async def search(self, query: str) -> list[Source]:
        logger.info(f"Searching for embeddings.")
        embedding = await self._create_embedding(query)

        top_k_results = await self.qdrant.search(embedding, self.k)

        if not top_k_results:
            raise RuntimeError(
                f"Retrieval returned no embedding for query {query!r}"
            )

        return top_k_results


    def get_next_entries(self):
        points, next_offset = self.qdrant.get_entries(100, self.offset)
        self.offset = next_offset
        return (points, next_offset)


    @abstractmethod
    async def _create_embedding(self, query: str):
        pass

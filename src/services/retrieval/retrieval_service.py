import os
import logging

from services.chunking_service import ChunkService
from services.qdrant_service import QdrantService
from models.chat_models import Source

logger = logging.getLogger(__name__)

from abc import ABC, abstractmethod

class RetrievalService(ABC):

    def __init__(self, qdrant_collection_name:str):
        self.qdrant = QdrantService(qdrant_collection_name)
        self.chunking = ChunkService()


    def ingest_text(self, text: str):
        chunks = self.chunking.chunk_by_paragraph(text)
        self.add_documents(chunks)


    def add_documents(self, docs: list[str]):
        logger.info(f"Documents added: {docs}")
        for doc in docs:
            embedding = self._create_embedding(doc)
            self.qdrant.upload_embedding(embedding, doc)


    def search(self, query: str) -> list[Source]:
        logger.info(f"Searching for embeddings.")
        embedding = self._create_embedding(query)

        k = int(os.getenv("RETRIEVAL_TOPK"))
        top_k_results = self.qdrant.search(embedding, k)
        return top_k_results


    @abstractmethod
    def _create_embedding(self, query: str):
        pass

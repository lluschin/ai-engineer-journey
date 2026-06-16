import logging
import numpy as np
from openai import OpenAI

from services.qdrant_service import QdrantService
from models.chat_models import Source

logger = logging.getLogger(__name__)

class RetrievalService:

    def __init__(self):
        self.client = OpenAI()
        self.qdrant = QdrantService()
    

    def add_documents(self, docs: list[str]):
        logger.info(f"Documents added: {docs}")
        for doc in docs:
            embedding = self._create_embedding(doc)
            self.qdrant.upload_embedding(embedding, doc)


    def search(self, query: str, top_k: int = 3) -> list[Source]:
        logger.info(f"searching for embeddings.")
        embedding = self._create_embedding(query)

        top_k_results = self.qdrant.search(embedding, top_k)
        return top_k_results


    def _create_embedding(self, query: str):
        embedding = self.client.embeddings.create(
            model="text-embedding-3-small",
            input=query
        )

        return embedding.data[0].embedding

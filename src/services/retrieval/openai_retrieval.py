import os

from openai import OpenAI
from services.retrieval.retrieval_service import RetrievalService


class OpenAiRetrieval(RetrievalService):

    QDRANT_COLLECTION = "AiJourney_text-embedding-3-small"

    def __init__(self):
        self.client = OpenAI()
        self.model = os.getenv("RETRIEVAL_MODEL")
        super().__init__(OpenAiRetrieval.QDRANT_COLLECTION)


    def _create_embedding(self, query: str):
        embedding = self.client.embeddings.create(
            model=self.model,
            input=query
        )

        return embedding.data[0].embedding

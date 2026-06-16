import logging
import numpy as np
from openai import OpenAI

from models.chat_models import Source

logger = logging.getLogger(__name__)

DOCUMENTS = [
    "Python wurde von Guido van Rossum entwickelt.",
    "FastAPI ist ein modernes Python Web Framework.",
    "RAG steht für Retrieval-Augmented Generation.",
    "Embeddings wandeln Text in numerische Vektoren um.",
]

class RetrievalService:

    def __init__(self):
        self.client = OpenAI()
        self.documents = []
        self.embeddings = []
    

    def add_documents(self, docs: list[str]):
        logger.info(f"Documents added: {docs}")
        for doc in docs:
            self.documents.append(doc)
            self.embeddings.append(self._create_embedding(doc))


    def search(self, query: str, top_k: int = 3) -> list[Source]:
        logger.info(f"searching for embeddings.")
        scores = []
        embedding = self._create_embedding(query)

        for e in zip(self.documents, self.embeddings):
            scores.append(Source(
                    document = e[0],
                    score=self._cosine_similarity(e[1], embedding)
                ))

        scores.sort(key=lambda s: s.score, reverse=True)

        return scores[:top_k]


    def _create_embedding(self, query: str):
        embedding = self.client.embeddings.create(
            model="text-embedding-3-small",
            input=query
        )

        return embedding.data[0].embedding


    def _cosine_similarity(self, a: list[float], b: list[float]) -> float:
        vec_a = np.array(a)
        vec_b = np.array(b)

        return float(
            np.dot(vec_a, vec_b)
            / (np.linalg.norm(vec_a) * np.linalg.norm(vec_b))
        )
import numpy as np
from openai import OpenAI


class RetrivalService:

    def __init__(self):
        self.client = OpenAI()
        self.documents = []
        self.embeddings = []
    

    def add_documents(self, docs: list[str]):
        for doc in docs:
            self.documents.append(doc)
            self.embeddings.append(self._create_embedding(doc))


    def search(self, query: str, top_k: int = 3) -> list[dict]:
        scores = []
        embedding = self._create_embedding(query)

        for e in zip(self.documents, self.embeddings):
            scores.append({
                "document" : e[0],
                "score": self._cosine_similarity(e[1], embedding)
            })

        scores.sort(key=lambda s: s["score"], reverse=True)

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
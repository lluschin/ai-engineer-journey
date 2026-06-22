import os
import ollama

from services.retrieval.retrieval_service import RetrievalService


class OllamaRetrieval(RetrievalService):

    QDRANT_COLLECTION = "AiJourney"
    
    NOMIC_EMBED_TEXT = "nomic-embed-text"
    BGE_M3 ="bge-m3"
    

    def __init__(self):
        self.model = os.getenv("RETRIEVAL_MODEL")
        qdrant_collection_name = "_".join([OllamaRetrieval.QDRANT_COLLECTION, self.model])

        super().__init__(qdrant_collection_name)


    def _create_embedding(self, query: str):
        embedding = ollama.embed(
            model=self.model,
            input=query
            )

        return embedding['embeddings'][0]
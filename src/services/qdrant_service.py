import uuid

from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct

from models.chat_models import Source

class QdrantService:
    COLLECTION_NAME = "AiEngineerJourney"

    def __init__(self):
        self.client = QdrantClient(host="localhost", port=6333)
    

    def upload_embedding(self, vec, doc):
        self.client.upsert(
            collection_name=QdrantService.COLLECTION_NAME,
            points=[
                PointStruct(
                    id=uuid.uuid4(),
                    vector=vec,
                    payload={"Infotext" : doc}
                )
            ]
        )


    def search(self, vec, top_k) -> list[Source]:
        hits = self.client.query_points(
            collection_name=QdrantService.COLLECTION_NAME,
            query=vec,
            limit=top_k
        ).points

        result_list = [Source(document=h.payload["Infotext"], score=h.score) for h in hits]
        return result_list
import uuid

from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct

from models.chat_models import Source

class QdrantService:
    def __init__(self, collection_name:str):
        self.client = QdrantClient(host="localhost", port=6333)
        self.collection_name = collection_name
    

    def upload_embedding(self, vec, doc):
        self.client.upsert(
            collection_name=self.collection_name,
            points=[
                PointStruct(
                    id=str(uuid.uuid4()),
                    vector=vec,
                    payload={"Infotext" : doc}
                )
            ]
        )


    def search(self, vec, top_k) -> list[Source]:
        hits = self.client.query_points(
            collection_name=self.collection_name,
            query=vec,
            limit=top_k
        ).points

        result_list = [Source(document=h.payload["Infotext"], score=h.score) for h in hits]
        return result_list


if __name__ == "__main__":
    pass
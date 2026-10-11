from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, Filter, FieldCondition, MatchValue

from src.models.chat_models import Source

class QdrantService:
    def __init__(self, collection_name:str):
        self.client = QdrantClient(host="localhost", port=6333)
        self.collection_name = collection_name
    

    def upload_embedding(self, id, vec, doc, docName):
        self.client.upsert(
            collection_name=self.collection_name,
            points=[
                PointStruct(
                    id=id,
                    vector=vec,
                    payload={
                        "infotext": doc,
                        "source": docName
                        }
                )
            ]
        )


    async def search(self, vec, top_k: int, docName: str | None) -> list[Source]:
        queryFilter = None
        if docName:
            queryFilter = Filter(
                must=[
                    FieldCondition(
                        key="source",
                        match=MatchValue(value=docName),
                    )
                ]
            )

        hits = self.client.query_points(
            collection_name=self.collection_name,
            query=vec,
            limit=top_k,
            query_filter=queryFilter,
        ).points

        result_list = [Source(id=h.id, document=h.payload["infotext"], score=h.score) for h in hits]
        return result_list


    def get_entries(self, limit: int, offset):
        points, next_offset = self.client.scroll(
            collection_name=self.collection_name,
            limit=limit,
            offset=offset,
            with_payload=True,
            with_vectors=False,
        )

        return (points, next_offset)


if __name__ == "__main__":
    pass
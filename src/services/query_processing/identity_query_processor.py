from services.query_processing.query_processor import QueryProcessor


class IdentityQueryProcessor(QueryProcessor):    

    async def process(self, query: str) -> str:
        return query
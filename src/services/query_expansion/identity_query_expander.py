from services.query_expansion.query_expander import QueryExpander


class IdentityQueryExpander(QueryExpander):    

    async def expand(self, query: str) -> str:
        return query
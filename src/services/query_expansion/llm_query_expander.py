from services.query_expansion.query_expander import QueryExpander
from services.llm.llm_service import LLMService

class LLMQueryExpander(QueryExpander):

    def __init__(self, llm_service: LLMService):
        self.llm_service = llm_service


    async def expand(self, query: str) -> str:
        prompt = f"""
        Rewrite the following user question into a concise search query
        for semantic document retrieval.

        Preserve the original intent.
        Add useful domain-specific terminology and synonyms.
        Return only the rewritten query.

        User question:
        {query}
        """

        return await self.llm_service.chat(prompt)

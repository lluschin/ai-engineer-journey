import logging

from services.query_expansion.query_expander import QueryExpander
from services.llm.llm_service import LLMService

logger = logging.getLogger(__name__)

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

        expanded_query = await self.llm_service.chat(prompt)
        expanded_query = expanded_query.strip()

        if not expanded_query:
            logger.warning("Query expander returned an empty string. Using original Query instead")
            expanded_query = query
        
        return expanded_query

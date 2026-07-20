import logging

from services.query_processing.query_processor import QueryProcessor
from services.llm.llm_service import LLMService

logger = logging.getLogger(__name__)

class LLMQueryRewriter(QueryProcessor):

    def __init__(self, llm_service: LLMService):
        self.llm_service = llm_service


    async def process(self, query: str) -> str:
        prompt = f"""
        Rewrite the user question into one concise semantic-search query.

        Rules:
        - Preserve all important entities and technical terms exactly.
        - Do not answer the question.
        - Do not add new topics, assumptions, examples, or explanations.
        - Remove conversational wording only when it does not affect meaning.
        - Return only the rewritten query.
        - Keep the query under 25 words.

        User question:
        {query}
        """

        rewritten_query = await self.llm_service.chat(prompt)
        rewritten_query = rewritten_query.strip()

        if not rewritten_query:
            logger.warning("Query expander returned an empty string. Using original Query instead")
            rewritten_query = query
        
        return rewritten_query

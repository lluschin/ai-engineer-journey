from services.query_processing.identity_query_processor import IdentityQueryProcessor
from services.query_processing.llm_query_expander import LLMQueryExpander
from services.query_processing.llm_query_rewriter import LLMQueryRewriter

def create_identity_query_processor(_llm_service) -> IdentityQueryProcessor:
    return IdentityQueryProcessor()


def create_llm_query_expander(llm_service) -> LLMQueryExpander:
    return LLMQueryExpander(llm_service)


def create_llm_query_rewriter(llm_service) -> LLMQueryRewriter:
    return LLMQueryRewriter(llm_service)

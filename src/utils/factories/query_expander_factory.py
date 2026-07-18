from services.query_expansion.identity_query_expander import IdentityQueryExpander
from services.query_expansion.llm_query_expander import LLMQueryExpander

def create_identity_query_expander(_llm_service) -> IdentityQueryExpander:
    return IdentityQueryExpander()


def create_llm_query_expander(llm_service) -> LLMQueryExpander:
    return LLMQueryExpander(llm_service)
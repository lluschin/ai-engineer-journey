from enum import StrEnum

class StageIdx(StrEnum):
    LLM_STAGE = "llm"
    RETRIEVAL_STAGE = "retrieval"
    RANKING_STAGE = "ranking"
    COMPRESSOR_STAGE = "compression"
    CONTEXT_BUILDER = "context_building"
    QUERY_EXPANDER = "query_processing"
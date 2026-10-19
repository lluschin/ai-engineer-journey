import sys
import toml
import logging

from enum import StrEnum
from collections.abc import Callable

from copy import deepcopy
from typing import Any

from src.services.llm.llm_service import LLMService
from src.services.retrieval.retrieval_service import RetrievalService
from src.services.ranking.identity_ranker import IdentityRanker
from src.services.context_builder.simple_context_builder import SimpleContextBuilder
from src.services.query_processing.query_processor import QueryProcessor
from src.services.compression.identity_compressor import IdentityCompressor

import src.utils.factories.llm_service_factory as llm_service_factory
import src.utils.factories.retrieval_service_factory as retrieval_service_factory
import src.utils.factories.ranking_service_factory as ranking_service_factory
import src.utils.factories.context_builder_factory as context_builder_factory
import src.utils.factories.query_processor_factory as query_processor_factory
import src.utils.factories.compressor_service_factory as compressor_service_factory

LLM_SERVICE: dict[
    str,
    Callable[[str], LLMService],
] = {
    "OllamaLLM": llm_service_factory.create_ollama_llm,
    "OpenAiLLM": llm_service_factory.create_openai_llm,
}

RETRIEVAL_SERVICE : dict[
    str,
    Callable[[str, int], RetrievalService],
] = {
    "OllamaRetrieval": retrieval_service_factory.create_ollama_retrieval,
    "OpenAiRetrieval": retrieval_service_factory.create_openai_retrieval,
}

RANKING_SERVICE : dict[
    str,
    Callable[[], IdentityRanker],
] = {
    "IdentityRanker": ranking_service_factory.create_identity_ranker,
    "HeuristicRanker": ranking_service_factory.create_heuristic_ranker,
    "CrossEncoderRanker": ranking_service_factory.create_cross_encoder_ranker,
}

COMPRESSOR_SERVICE : dict[
    str,
    Callable[[], IdentityCompressor]
] = {
    "IdentityCompressor": compressor_service_factory.create_identity_compressor,
    "HeuristicCompressor": compressor_service_factory.create_heuristic_compressor,
}

CONTEXT_BUILDER : dict[
    str,
    Callable[[], SimpleContextBuilder],
] = {
    "SimpleContextBuilder": context_builder_factory.create_simple_context_builder,
    "OrderedContextBuilder": context_builder_factory.create_ordered_context_builder,
}

QUERY_EXPANDER : dict[
    str,
    Callable[[LLMService], QueryProcessor],
] = {
    "IdentityQueryProcessor": query_processor_factory.create_identity_query_processor,
    "LLMQueryExpander": query_processor_factory.create_llm_query_expander,
    "LLMQueryRewriter": query_processor_factory.create_llm_query_rewriter,
}

class ServiceIdx(StrEnum):
    LLM_SERVICE = "llm"
    RETRIEVAL_SERVICE = "retrieval"
    RANKING_SERVICE = "ranking"
    COMPRESSOR_SERVICE = "compression"
    CONTEXT_BUILDER = "context_building"
    QUERY_EXPANDER = "query_processing"


logger = logging.getLogger(__name__)


class ServiceRegistry:    

    def __init__(self):
        self.llm_service: LLMService | None = None
        self.retrieval_service: RetrievalService | None = None
        self.ranker: IdentityRanker | None = None
        self.compressor: IdentityCompressor | None = None
        self.context_builder: SimpleContextBuilder | None = None
        self.query_expander: QueryProcessor | None = None

        # Configuration only; request inputs, outputs and timings live in the route.
        self.meta_info: dict[ServiceIdx, dict[str, Any]] = {}
    

    def load_settings(self, settings: dict):
        logger.info("loading settings...")

        # Build metadata locally and publish it only after all services loaded.
        meta_info = {
            ServiceIdx.LLM_SERVICE: deepcopy(settings['llm']),
            ServiceIdx.RETRIEVAL_SERVICE: deepcopy(settings['retrieval']),
            ServiceIdx.RANKING_SERVICE: deepcopy(settings['ranker']),
            ServiceIdx.COMPRESSOR_SERVICE: deepcopy(settings['compressor']),
            ServiceIdx.CONTEXT_BUILDER: deepcopy(settings['context_builder']),
            ServiceIdx.QUERY_EXPANDER: deepcopy(settings['query_expander']),
        }

        llm_params = meta_info[ServiceIdx.LLM_SERVICE]
        logger.info("init llm service: %s", llm_params)
        new_llm_service = LLM_SERVICE[llm_params['service']](llm_params['model'])

        retrieval_params = meta_info[ServiceIdx.RETRIEVAL_SERVICE]
        logger.info("init retrieval service: %s", retrieval_params)
        new_retrieval_service = RETRIEVAL_SERVICE[retrieval_params['service']](
            retrieval_params['model'], retrieval_params['top_k'],
        )

        ranker_params = meta_info[ServiceIdx.RANKING_SERVICE]
        logger.info("init ranker: %s", ranker_params)
        new_ranker = RANKING_SERVICE[ranker_params['service']]()

        compressor_params = meta_info[ServiceIdx.COMPRESSOR_SERVICE]
        logger.info("init compressor: %s", compressor_params)
        new_compressor = COMPRESSOR_SERVICE[compressor_params['service']]()

        context_builder_params = meta_info[ServiceIdx.CONTEXT_BUILDER]
        logger.info("init context builder: %s", context_builder_params)
        new_context_builder = CONTEXT_BUILDER[context_builder_params['service']]()

        query_expander_params = meta_info[ServiceIdx.QUERY_EXPANDER]
        logger.info("init query expander: %s", query_expander_params)
        new_query_expander = QUERY_EXPANDER[query_expander_params['service']](new_llm_service)

        self.llm_service = new_llm_service
        self.retrieval_service = new_retrieval_service
        self.ranker = new_ranker
        self.context_builder = new_context_builder
        self.query_expander = new_query_expander
        self.compressor = new_compressor
        self.meta_info = meta_info


    def load_settings_file(self, filepath: str):
        logger.info(f'loading settings from file: "{filepath}"')
        settings = toml.load(filepath)
        self.load_settings(settings)

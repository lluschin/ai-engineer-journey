import sys
import toml
import logging

from collections.abc import Callable

from services.llm.llm_service import LLMService
from services.retrieval.retrieval_service import RetrievalService
from services.ranking.identity_ranker import IdentityRanker
from services.context_builder.simple_context_builder import SimpleContextBuilder
from services.query_expansion.query_expander import QueryExpander

import utils.factories.llm_service_factory as llm_service_factory
import utils.factories.retrieval_service_factory as retrieval_service_factory
import utils.factories.ranking_service_factory as ranking_service_factory
import utils.factories.context_builder_factory as context_builder_factory
import utils.factories.query_expander_factory as query_expander_factory

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
    Callable[[LLMService], QueryExpander],
] = {
    "IdentityQueryExpander": query_expander_factory.create_identity_query_expander,
    "LLMQueryExpander": query_expander_factory.create_llm_query_expander,
}


logger = logging.getLogger(__name__)


class ServiceRegistry:

    _instance = None 

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    

    def __init__(self):
        if not getattr(self, '_is_initialized', False):
            self.llm_service: LLMService = None
            self.retrieval_service: RetrievalService = None
            self.ranker: IdentityRanker = None
            self.context_builder: SimpleContextBuilder = None
            self.query_expander: QueryExpander = None

            self._is_initialized = True
    

    def load_settings(self, settings: dict):
        logger.info("loading settings...")

        logger.info("init llm service.")
        service_name = settings['llm']['service']
        model_name = settings['llm']['model']
        logger.info(f'service: {service_name}')
        logger.info(f'model: {model_name}')
        new_llm_service = LLM_SERVICE[service_name](model_name)

        logger.info("init retrieval service.")
        service_name = settings['retrieval']['service']
        model_name = settings['retrieval']['model']
        top_k = settings['retrieval']['top_k']
        logger.info(f'service: {service_name}')
        logger.info(f'model: {model_name}')
        logger.info(f'top_k: {top_k}')
        new_retrieval_service = RETRIEVAL_SERVICE[service_name](model_name, top_k)

        logger.info("init ranker.")
        service_name = settings['ranker']['service']
        logger.info(f'service: {service_name}')
        new_ranker = RANKING_SERVICE[service_name]()

        logger.info("init context builder.")
        service_name = settings['context_builder']['service']
        logger.info(f'service: {service_name}')
        new_context_builder = CONTEXT_BUILDER[service_name]()

        logger.info("init query expander.")
        service_name = settings['query_expander']['service']
        logger.info(f'service: {service_name}')
        new_query_expander = QUERY_EXPANDER[service_name](new_llm_service)

        self.llm_service = new_llm_service
        self.retrieval_service = new_retrieval_service
        self.ranker = new_ranker
        self.context_builder = new_context_builder
        self.query_expander = new_query_expander


    def load_settings_file(self, filepath: str):
        logger.info(f'loading settings from file: "{filepath}"')
        settings = toml.load(filepath)
        self.load_settings(settings)

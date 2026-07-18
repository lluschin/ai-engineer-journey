import sys
import toml
import logging

from services.llm.llm_service import LLMService
from services.llm.ollama_llm import OllamaLLM
from services.llm.openai_llm import OpenAiLLM

from services.retrieval.retrieval_service import RetrievalService
from services.retrieval.ollama_retrieval import OllamaRetrieval
from services.retrieval.openai_retrieval import OpenAiRetrieval

from services.ranking.identity_ranker import IdentityRanker
from services.ranking.heuristic_ranker import HeuristicRanker

from services.context_builder.simple_context_builder import SimpleContextBuilder
from services.context_builder.ordered_context_builder import OrderedContextBuilder

from services.query_expansion.query_expander import QueryExpander
from services.query_expansion.identity_query_expander import IdentityQueryExpander
from services.query_expansion.llm_query_expander import LLMQueryExpander


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
        new_llm_service = getattr(sys.modules[__name__], service_name)(model_name)

        logger.info("init retrieval service.")
        service_name = settings['retrieval']['service']
        model_name = settings['retrieval']['model']
        top_k = settings['retrieval']['top_k']
        logger.info(f'service: {service_name}')
        logger.info(f'model: {model_name}')
        logger.info(f'top_k: {top_k}')
        new_retrieval_service = getattr(sys.modules[__name__], service_name)(model_name, top_k)

        logger.info("init ranker.")
        service_name = settings['ranker']['service']
        logger.info(f'service: {service_name}')
        new_ranker = getattr(sys.modules[__name__], service_name)()

        logger.info("init context builder.")
        service_name = settings['context_builder']['service']
        logger.info(f'service: {service_name}')
        new_context_builder = getattr(sys.modules[__name__], service_name)()

        logger.info("init query expander.")
        service_name = settings['query_expander']['service']
        logger.info(f'service: {service_name}')
        new_query_expander = getattr(sys.modules[__name__], service_name)()

        self.llm_service = new_llm_service
        self.retrieval_service = new_retrieval_service
        self.ranker = new_ranker
        self.context_builder = new_context_builder
        self.query_expander = new_query_expander


    def load_settings_file(self, filepath: str):
        logger.info(f'loading settings from file: "{filepath}"')
        settings = toml.load(filepath)
        self.load_settings(settings)

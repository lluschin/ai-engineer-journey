from src.services.retrieval.retrieval_service import RetrievalService
from src.services.retrieval.ollama_retrieval import OllamaRetrieval
from src.services.retrieval.openai_retrieval import OpenAiRetrieval
from src.services.retrieval.hybrid_retrival import HybridRetrival

def create_ollama_retrieval(model, top_k) -> OllamaRetrieval:
    return OllamaRetrieval(model, top_k)


def create_openai_retrieval(model, top_k) -> OpenAiRetrieval:
    return OpenAiRetrieval(model, top_k)

def create_hybrid_retrival(retrival_service: RetrievalService) -> HybridRetrival:
    return HybridRetrival(retrival_service)
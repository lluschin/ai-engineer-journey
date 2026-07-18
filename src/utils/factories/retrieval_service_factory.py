from services.retrieval.ollama_retrieval import OllamaRetrieval
from services.retrieval.openai_retrieval import OpenAiRetrieval

def create_ollama_retrieval(model, top_k) -> OllamaRetrieval:
    return OllamaRetrieval(model, top_k)


def create_openai_retrieval(model, top_k) -> OpenAiRetrieval:
    return OpenAiRetrieval(model, top_k)
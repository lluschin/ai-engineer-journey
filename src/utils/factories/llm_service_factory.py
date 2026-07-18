from services.llm.ollama_llm import OllamaLLM
from services.llm.openai_llm import OpenAiLLM

def create_ollama_llm(model) ->  OllamaLLM:
    return OllamaLLM(model)


def create_openai_llm(model) -> OpenAiLLM:
    return OpenAiLLM(model)
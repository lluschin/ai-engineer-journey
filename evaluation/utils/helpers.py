from time import perf_counter

import requests
import toml

from evaluation.model.question import (
    Configuration,
    Question,
    QuestionResult,
    Runtime,
)

URL_RAG_CHAT = "http://127.0.0.1:8000/rag_chat"
URL_LOAD_ENVIRONMENT = "http://127.0.0.1:8000/load_environment"

def execute_question(question: Question) -> QuestionResult:
    data = {
        "user": "Wet0zelott",
        "message": question.question,
    }

    start = perf_counter()
    response = requests.post(URL_RAG_CHAT, json=data, timeout=180)
    runtime = perf_counter() - start
    response.raise_for_status()

    response_data = response.json()
    answer = response_data["message"]
    number_of_used_sources = response_data["used_sources"]
    sources = response_data["sources"][:number_of_used_sources]
    retrieval_sources = [source["id"] for source in sources]
    runtime_data = response_data.get("runtime") or {}

    result = QuestionResult(
        question=question,
        answer=answer,
        retrieval_sources=retrieval_sources,
        runtime=Runtime(
            total_runtime=runtime,
            **runtime_data,
        ),
    )

    return result


def load_configuration(config_filepath: str) -> Configuration:
    config_data = toml.load(config_filepath)

    configuration = Configuration(
        filepath=config_filepath,
        title=config_data["title"],
        llm_service=config_data["llm"]["service"],
        llm_model=config_data["llm"]["model"],
        retrieval_service=config_data["retrieval"]["service"],
        retrieval_model=config_data["retrieval"]["model"],
        retrieval_top_k=config_data["retrieval"]["top_k"],
        ranker_service=config_data["ranker"]["service"],
        context_builder_service=config_data["context_builder"]["service"],
        query_expander_service=config_data["query_expander"]["service"],
    )

    return configuration


def activate_configuration(configuration: Configuration) -> None:
    data = {
        "filepath": configuration.filepath,
    }

    response = requests.post(URL_LOAD_ENVIRONMENT, json=data, timeout=180)
    response.raise_for_status()

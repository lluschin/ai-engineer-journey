import requests
import toml
import time

from pathlib import Path

from evaluation.model.question import (
    Configuration,
    Question,
    QuestionResult,
    Runtime,
)

from src.models.chat_models import ChatResponse, Stage

URL_RAG_CHAT = "http://127.0.0.1:8000/rag_chat"
URL_LOAD_ENVIRONMENT = "http://127.0.0.1:8000/load_environment"

def execute_question(question: Question) -> QuestionResult:
    data = {
        "user": "Wet0zelott",
        "message": question.question,
    }

    start_t = time.perf_counter()
    response = requests.post(URL_RAG_CHAT, json=data, timeout=180)
    response.raise_for_status()
    runtime = time.perf_counter() - start_t

    chat_response = ChatResponse.model_validate(response.json())

    result = QuestionResult(
        question=question,
        chat_response=chat_response,
        request_runtime=runtime,
    )

    return result


def load_configuration(config_filepath: Path) -> Configuration:
    config_data = toml.load(config_filepath)

    configuration = Configuration(
        filepath=str(config_filepath),
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


def findStageByName(stages: list[Stage], stage_name: str) -> Stage | None:
    stage = None
    for s in stages:
        if s.name == stage_name:
            stage = s
            break

    return stage

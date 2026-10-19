import logging
import time
from copy import deepcopy
from pathlib import Path
from fastapi import APIRouter, HTTPException
from src.models.chat_models import (
    Stage,
    ChatRequest,
    ChatResponse,
    SimpleChatResponse,
    Environment,
)
from src.utils.registry import ServiceRegistry, ServiceIdx

logger = logging.getLogger(__name__)

def create_chat_router(configFilePath: Path) -> APIRouter:
    service_registry = ServiceRegistry()
    service_registry.load_settings_file(configFilePath)

    chat_router = APIRouter()

    @chat_router.post("/load_environment")
    async def load_config(environment: Environment):
        try:
            service_registry.load_settings_file(environment.filepath)
        except Exception as e:
            logger.exception("Unexpected error while loading environment. " + str(e))

            raise HTTPException(
                status_code=400,
                detail="Configuration contains errors."
            )
        
        return {"status": "reloaded"}


    @chat_router.post("/chat", response_model=SimpleChatResponse)
    async def chat(msg: ChatRequest):
        try:
            logger.info(f"Received message from user {msg.user}")
            cleaned_message = msg.message.strip()

            if not cleaned_message:
                logger.warning("Empty message detected.")
                raise HTTPException(
                    status_code=400,
                    detail="Message must not be empty."
                )
            
            logger.info(f"Creating response for user {msg.user}")
            response = await service_registry.llm_service.chat(cleaned_message)
                    
            return SimpleChatResponse(
                message=f"Ai said: {response}",
                llm_model=service_registry.llm_service.model
            )
        
        except HTTPException:
            raise

        except Exception:
            logger.exception("Unexpected error in /chat endpoint.")
            raise HTTPException(
                status_code=500,
                detail="Internal server error."
            )


    @chat_router.post("/rag_chat", response_model=ChatResponse)
    async def rag_chat(msg: ChatRequest):
        try:
            cleaned_message = msg.message.strip()

            if not cleaned_message:
                logger.warning("Empty message detected.")
                raise HTTPException(
                    status_code=400,
                    detail="Message must not be empty."
                )
            
            # Fresh execution records for this request, in pipeline order.
            stages = {
                service: Stage(name=service.value, params=deepcopy(service_registry.meta_info[service]))
                for service in (
                    ServiceIdx.QUERY_EXPANDER,
                    ServiceIdx.RETRIEVAL_SERVICE,
                    ServiceIdx.RANKING_SERVICE,
                    ServiceIdx.COMPRESSOR_SERVICE,
                    ServiceIdx.CONTEXT_BUILDER,
                    ServiceIdx.LLM_SERVICE,
                )
            }

            # expand query for improved retrieval
            logger.info("Processing query.")
            original_query = cleaned_message
            start_t = time.perf_counter()
            expanded_query = await service_registry.query_expander.process(original_query)
            runtime = time.perf_counter() - start_t

            stage = stages[ServiceIdx.QUERY_EXPANDER]
            stage.input = {"original_query": original_query}
            stage.output = {"expanded_query": expanded_query}
            stage.runtime = runtime

            logger.info("Processing query finished in %.2f seconds", runtime)
            logger.info("Original query: %r", original_query)
            logger.info("Expanded query: %r", expanded_query)
            
            stage = stages[ServiceIdx.RETRIEVAL_SERVICE]
            stage.input = {"query": expanded_query, "source": msg.source}

            # search database for embeddings
            start_t = time.perf_counter()
            logger.info("Searching for embeddings.")
            sources = await service_registry.retrieval_service.search(expanded_query, msg.source)
            runtime = time.perf_counter() - start_t
            logger.info("Retrieval finished in %.2f seconds", runtime)

            stage.runtime = runtime
            # Serialize now so later stages cannot mutate this snapshot.
            stage.output = {"sources": [source.model_dump(mode="json") for source in sources]}

            stage = stages[ServiceIdx.RANKING_SERVICE]
            stage.input = {
                "query": original_query,
                "sources": [source.model_dump(mode="json") for source in sources],
            }

            # rerank the given sources
            start_t = time.perf_counter()
            logger.info("rerank sources.")
            ranked_sources = service_registry.ranker.rank(original_query, sources)
            runtime = time.perf_counter() - start_t
            logger.info("Reranking finished in %.2f seconds", runtime)

            stage.runtime = runtime
            stage.output = {"sources": [source.model_dump(mode="json") for source in ranked_sources]}

            stage = stages[ServiceIdx.COMPRESSOR_SERVICE]
            stage.input = {
                "query": original_query,
                "sources": [source.model_dump(mode="json") for source in ranked_sources],
            }

            # compress the context
            start_t = time.perf_counter()
            logger.info("compress context.")
            compressed_sources = service_registry.compressor.compress(original_query, ranked_sources)
            runtime = time.perf_counter() - start_t
            logger.info("Compression finished in %.2f seconds", runtime)

            stage.runtime = runtime
            stage.output = {"sources": [source.model_dump(mode="json") for source in compressed_sources]}

            stage = stages[ServiceIdx.CONTEXT_BUILDER]
            stage.input = {"sources": [source.model_dump(mode="json") for source in compressed_sources]}

            # buildup context for llm
            start_t = time.perf_counter()
            logger.info("buildup context.")
            context, nos = service_registry.context_builder.create_context(compressed_sources)
            runtime = time.perf_counter() - start_t
            logger.info("Context Building finished in %.2f seconds", runtime)

            stage.runtime = runtime
            # Keep the existing builder contract; do not infer selected IDs from its count.
            stage.output = {"context": context, "used_sources": nos}

            stage = stages[ServiceIdx.LLM_SERVICE]
            stage.input = {"query": original_query, "context": context}

            # send prompt to llm and create response
            start_t = time.perf_counter()
            logger.info("talk to llm.")
            response = await service_registry.llm_service.rag_chat(original_query, context)
            runtime = time.perf_counter() - start_t
            logger.info("LLM call finished in %.2f seconds", runtime)

            stage.runtime = runtime
            stage.output = {"answer": response}

            logger.info(f"Creating response for user {msg.user}")
            return ChatResponse(
                input_request=msg,
                response=response,
                stages=list(stages.values()),
            )
        
        except HTTPException:
            raise
        except Exception:
            logger.exception("Unexpected error in /rag_chat endpoint.")
            raise HTTPException( 
                status_code=500,
                detail="Internal server error"
            )

    return chat_router
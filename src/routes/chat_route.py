import logging

from fastapi import APIRouter, HTTPException
from models.chat_models import ChatRequest, ChatResponse, Environment
from utils.registry import ServiceRegistry

logger = logging.getLogger(__name__)

SETTINGS_FILEPATH = r'../data/qwen3_bge-m3.toml'

service_registry = ServiceRegistry()
service_registry.load_settings_file(SETTINGS_FILEPATH)

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


@chat_router.post("/chat", response_model=ChatResponse)
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
                
        return ChatResponse(
            message=f"Ai said: {response}",
            model=service_registry.llm_service.model
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
        
        # search database for embeddings
        logger.info("Searching for embeddings.")
        sources = await service_registry.retrieval_service.search(cleaned_message)

        # rerank the given sources
        logger.info("rerank sources.")
        ranked_sources = service_registry.ranker.rank(cleaned_message, sources)

        # buildup context for llm
        logger.info("buildup context.")
        context, nos = service_registry.context_builder.create_context(ranked_sources)

        # send promt to llm and create response
        logger.info("talk to llm.")
        response = await service_registry.llm_service.rag_chat(cleaned_message, context)

        logger.info(f"Creating response for user {msg.user}")
        return ChatResponse(
            message = response,
            llm_model = service_registry.llm_service.model,
            retrieval_model = service_registry.retrieval_service.model,
            chunk_size = service_registry.retrieval_service.chunking.chunk_size,
            top_k = service_registry.retrieval_service.k,
            context_builder = type(service_registry.context_builder).__name__,
            used_sources = nos,
            ranking = type(service_registry.ranker).__name__,
            sources = ranked_sources
        )
    
    except HTTPException:
        raise
    except Exception:
        logger.exception("Unexpected error in /rag_chat endpoint.")
        raise HTTPException( 
            status_code=500,
            detail="Internal server error"
        )
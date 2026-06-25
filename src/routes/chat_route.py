import os
import logging
from fastapi import APIRouter, HTTPException

from models.chat_models import ChatRequest, ChatResponse

logger = logging.getLogger(__name__)

chat_router = APIRouter()

# ==== load services ====
match os.getenv("LLM_SERVICE"):
    case "openai":
        logger.info("Load openai llm.")
        from services.llm.openai_llm import OpenAILLM
        llm_service = OpenAILLM()
    case "ollama":
        logger.info("Load ollama llm.")
        from services.llm.ollama_llm import OllamaLLM
        llm_service = OllamaLLM()
    case _:
        logger.error("Defined llm service not found.")
        raise RuntimeError("Defined llm service not found.")

match os.getenv("RETRIEVAL_SERVICE"):
    case"openai":
        logger.info("Load openai retrival.")
        from services.retrieval.openai_retrieval import OpenAiRetrieval
        retrieval_service = OpenAiRetrieval()
    case "ollama":
        logger.info("Load ollama retrival.")
        from services.retrieval.ollama_retrieval import OllamaRetrieval
        retrieval_service = OllamaRetrieval()
    case _:
        logger.error("Defined retrieval service not found.")
        raise RuntimeError("Defined retrieval service not found.")


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
        response = await llm_service.chat(cleaned_message)
                
        return ChatResponse(message=f"Ai said: {response}", model=llm_service.model)
    
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
        
        logger.info("Searching for embeddings.")
        sources = await retrieval_service.search(cleaned_message)
        docs = [src.document for src in sources]

        logger.info(f"Creating response for user {msg.user}")
        response = await llm_service.rag_chat(cleaned_message, docs)

        return ChatResponse(
            message=response,
            llm_model=llm_service.model,
            retrieval_model=retrieval_service.model,
            chunk_size=retrieval_service.chunking.chunk_size,
            top_k=retrieval_service.k,
            sources=sources
        )
    
    except HTTPException:
        raise
    except Exception:
        logger.exception("Unexpected error in /rag_chat endpoint.")
        raise HTTPException( 
            status_code=500,
            detail="Internal server error"
        )
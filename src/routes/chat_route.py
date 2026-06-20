import logging
from fastapi import APIRouter, HTTPException

from models.chat_models import ChatRequest, ChatResponse
from services.openai_service import OpenAIService
from services.retrieval_service import RetrievalService

logger = logging.getLogger(__name__)

chat_router = APIRouter()

llm_service = OpenAIService()
retrieval_service = RetrievalService()

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
        response = await llm_service.createResponse(cleaned_message)
                
        return ChatResponse(message=f"OpenAi said: {response}", model=llm_service.model)
    
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
        sources = retrieval_service.search(cleaned_message)
        docs = [src.document for src in sources]

        logger.info(f"Creating response for user {msg.user}")
        response = await llm_service.createRagResponse(cleaned_message, docs)

        return ChatResponse(
            message=response,
            model=llm_service.model,
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
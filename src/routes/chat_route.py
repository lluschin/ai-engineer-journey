import logging
from fastapi import APIRouter, HTTPException

from models.chat_models import ChatRequest, ChatResponse
from services.llm_service import LLMService
from services.openai_service import OpenAIService

logger = logging.getLogger(__name__)

chat_router = APIRouter()

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
        service = OpenAIService()
        response = await service.createResponse(msg.message)
                
        return ChatResponse(message=f"OpenAi said: {response}", model=service.model)
    
    except HTTPException:
        raise

    except Exception:
        logger.exception("Unexpected error in /chat endpoint.")
        raise HTTPException(
            status_code=500,
            detail="Internal server error."
        )

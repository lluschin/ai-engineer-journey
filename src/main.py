import logging
import dotenv
from fastapi import FastAPI

logging.basicConfig(level=logging.DEBUG)

from routes.chat_route import chat_router

app = FastAPI()
app.include_router(chat_router)

@app.get("/")
async def root():
    return {"message": "AI Engineer Journey started 🚀"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}




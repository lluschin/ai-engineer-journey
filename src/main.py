import logging
from fastapi import FastAPI
from routes.chat_route import chat_router


logging.basicConfig(level=logging.INFO)

app = FastAPI()
app.include_router(chat_router)

@app.get("/")
async def root():
    return {"message": "AI Engineer Journey started 🚀"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}




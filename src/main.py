import logging
import uvicorn
import argparse
from fastapi import FastAPI
from pathlib import Path

logging.basicConfig(level=logging.INFO)

from src.routes.chat_route import create_chat_router


def create_app(configPath: Path) -> FastAPI:
    app = FastAPI()

    chatRouter = create_chat_router(configPath)
    app.include_router(chatRouter)

    @app.get("/")
    async def root():
        return {"message": "AI Engineer Journey started 🚀"}


    @app.get("/health")
    async def health_check():
        return {"status": "healthy"}

    return app


def parse_args() -> Path:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-c",
        "--config",
        type=Path,
        required=True,
        help="configuration file for RAG features."
    )

    args = parser.parse_args()
    if not args.config.exists():
        parser.error(f"file \"{args.config}\" was not found.")

    if not args.config.is_file():
        parser.error(f"\"{args.config}\" needs to be a file.")

    return args.config


def main():
    configPath = parse_args()
    app = create_app(configPath)
    uvicorn.run(app)


if __name__ == "__main__":
    main()
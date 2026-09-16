import argparse
import asyncio
import logging
from pathlib import Path

from src.utils.registry import ServiceRegistry

logging.basicConfig(level=logging.INFO)


def parse_args():
    def check_filepath(filepath: Path) -> tuple[Path, Path]:
        if not filepath.exists():
            parser.error(f"file \"{filepath}\" was not found.")
    
        if not filepath.is_file():
            parser.error(f"\"{filepath}\" needs to be a file.")

    
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-c",
        "--config",
        type=Path,
        required=True,
        help="configuration file for RAG features.",
    )
    parser.add_argument(
        "-i",
        "--input",
        type=Path,
        required=True,
        help="input text file to ingest to database",
    )

    args = parser.parse_args()
    check_filepath(args.config)
    check_filepath(args.input)

    return (args.config, args.input)


def ingest():
    configFilePath, inputFilePath = parse_args()

    registry = ServiceRegistry()
    registry.load_settings_file(str(configFilePath))

    asyncio.run(
        registry.retrieval_service.ingest_text(inputFilePath)
    )


if __name__ == "__main__":
    ingest()
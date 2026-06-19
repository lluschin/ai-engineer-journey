import toml
import dotenv
import logging
from  dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    openai_model: str
    openai_reasoning: str
    chunking_chunk_size: int
    chunking_overlap: int
    retrieval_top_k: int


def loadSettings() -> Settings:
    logger = logging.getLogger(__name__)

    # load environment
    logger.info("Load env file.")
    isSet = dotenv.load_dotenv()
    if not isSet:
        logger.error("Cannot find .env file")
        raise RuntimeError(".env file not found")

    
    # load toml
    config = toml.load('config/config.toml')
    _model = config["openai"]["model"]
    _reasoning = config["openai"]["reasoning"]

    _chunk_size = config["chunking"]["chunk_size"]
    _overlap = config["chunking"]["overlap"]

    _top_k = config["retrieval"]["top_k"]


    settings = Settings(
        openai_model=_model,
        openai_reasoning=_reasoning,
        chunking_chunk_size=_chunk_size,
        chunking_overlap=_overlap,
        retrieval_top_k=_top_k,
    )

    return settings



    

import toml
import dotenv
import logging
from  dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    openai_model: str
    openai_reasoning: str


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

    settings = Settings(
        openai_model = _model,
        openai_reasoning = _reasoning
    )

    return settings



    

import sys 
import dotenv

sys.path.append("./src")
from services.retrieval.openai_retrieval import OpenAiRetrieval
from services.retrieval.ollama_retrieval import OllamaRetrieval

dotenv.load_dotenv("./data/.env")


DEMO_TEXT = "./data/demo_text.txt"

with open(DEMO_TEXT, "r") as fp:
    text = fp.read()

retrival_service = OllamaRetrieval(OllamaRetrieval.BGE_M3)
retrival_service.ingest_text(text)
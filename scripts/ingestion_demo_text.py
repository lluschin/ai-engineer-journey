from services.retrieval_service import RetrievalService
from services.chunking_service import ChunkService

DEMO_TEXT_PATH = "./misc/demo_text.txt"


with open(DEMO_TEXT_PATH, "r") as fp:
    text = fp.read()
    
#chunking_service = ChunkService(220,100)
#chunks = chunking_service.chunk_by_paragraph(text)
#print(*chunks, sep="\n\n--")

retrieval_service = RetrievalService()
retrieval_service.ingest_text(text)
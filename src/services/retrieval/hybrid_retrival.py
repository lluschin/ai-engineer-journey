import copy
import logging 
from rank_bm25 import BM25Okapi
from nltk.tokenize import wordpunct_tokenize

from src.services.retrieval.retrieval_service import RetrievalService
from src.services.retrieval.ollama_retrieval import OllamaRetrieval
from src.services.retrieval.openai_retrieval import OpenAiRetrieval

from src.models.chat_models import Source

PUNCTUATION_MARKS = set([".", ",", "-", "?", "!"])

logger = logging.getLogger(__name__)


class HybridRetrival(RetrievalService):

    def __init__(self, retrival_service: OllamaRetrieval | OpenAiRetrieval):
        self.retrival_service = retrival_service

        self.chunks: list[Source] = []
        while True:
            entries = self.retrival_service.get_next_entries()
            self.chunks += [Source(id=e.id,
                document=e.payload["infotext"],
                source=e.payload["source"],
                score=0.0,
            ) for e in entries[0]]

            if not entries[1]:
                break

        self.tokenized_chunk_list = [self._tokenize_query(c.document.casefold()) for c in self.chunks]
        self.bm25 = BM25(self.tokenized_chunk_list)


    def _tokenize_query(self, query: str) -> list[str]:
        tokens = wordpunct_tokenize(query)
        tokens = [t for t in tokens if t not in PUNCTUATION_MARKS]
        return tokens


    async def _create_embedding(self, query: str):
        return await self.retrival_service._create_embedding(query)


    def _rrf_fusion(self, sources1: list[Source], sources2: list[Source], c: int = 60) -> list[Source]:
        def calc_scores(fusion: dict[Source], sources: list[Source]):
            for i, s in enumerate(sources, start=1):
                if not s.id in fusion:
                    fusion[s.id] = Source(
                        id=s.id,
                        document=s.document,
                        source=s.source,
                        score=0.0
                    )

                score = 1 / (c + i)
                fusion[s.id].score += score

        fusion: dict[str, Source] = {}
        calc_scores(fusion, sources1)
        calc_scores(fusion, sources2)

        rrf_sources: list[Source] = list(fusion.values())
        rrf_sources.sort(key=lambda s: s.score, reverse=True)

        return rrf_sources                


    async def search(self, query: str, docName: str | None) -> list[Source]:
        # top_k embeddings from model
        sources_model: list[Source] = await self.retrival_service.search(query, docName)
        logger.debug("sources from model: " + str(sources_model))

        # top_k embeddings from bm25
        tokenized_query = self._tokenize_query(query.casefold())
        sources_bm25 = []
        for source, tokens, score in zip(self.chunks, self.tokenized_chunk_list, self.bm25.get_scores(tokenized_query)):
            if not set(tokenized_query).intersection(set(tokens)):
                continue

            if not docName or docName == source.source:
                s = copy.copy(source)
                s.score = score
                sources_bm25.append(s)

        sources_bm25.sort(key=lambda s: s.score, reverse=True)
        sources_bm25 = sources_bm25[:self.retrival_service.k]
        logger.debug("sources from bm25: " + str(sources_bm25))
        
        # rrf fusion
        sources_rrf = self._rrf_fusion(sources_model, sources_bm25)[:self.retrival_service.k]
        logger.debug("sources from rrf: " + str(sources_rrf))

        return sources_rrf


class BM25:
    def __init__(self, tokenized_documents: list[list[str]]):
        self.bm25 = BM25Okapi(tokenized_documents)


    def get_scores(self, tokenized_query: list[str]):
        return self.bm25.get_scores(tokenized_query)
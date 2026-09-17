import copy
from FlagEmbedding import FlagReranker

from src.services.ranking.identity_ranker import IdentityRanker
from src.models.chat_models import Source


class CrossEncoderRanker(IdentityRanker):

    def __init__(self):
        self.reranker = FlagReranker(
            model_name_or_path="BAAI/bge-reranker-v2-m3",
            use_fp16=True,
        )
        super().__init__()


    def rank(self, query: str, context: list[Source]) -> list[Source]:
        ranked_context = copy.deepcopy(context)

        pairs = [[query, source.document] for source in ranked_context]
        scores = self.reranker.compute_score(pairs, normalize=True)

        for score, source in zip(scores, ranked_context):
            source.score = float(score)

        ranked_context.sort(key= lambda s: s.score, reverse=True)
        return ranked_context

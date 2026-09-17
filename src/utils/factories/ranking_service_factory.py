from src.services.ranking.identity_ranker import IdentityRanker
from src.services.ranking.heuristic_ranker import HeuristicRanker
from src.services.ranking.cross_encoder_ranker import CrossEncoderRanker

def create_identity_ranker() -> IdentityRanker:
    return IdentityRanker()


def create_heuristic_ranker() -> HeuristicRanker:
    return HeuristicRanker()

def create_cross_encoder_ranker() -> CrossEncoderRanker:
    return CrossEncoderRanker()
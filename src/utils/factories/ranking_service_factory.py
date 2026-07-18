from services.ranking.identity_ranker import IdentityRanker
from services.ranking.heuristic_ranker import HeuristicRanker

def create_identity_ranker() -> IdentityRanker:
    return IdentityRanker()


def create_heuristic_ranker() -> HeuristicRanker:
    return HeuristicRanker()
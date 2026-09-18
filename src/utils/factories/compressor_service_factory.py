from src.services.compression.identity_compressor import IdentityCompressor
from src.services.compression.heuristic_compressor import HeuristicCompressor

def create_identity_compressor() -> IdentityCompressor:
    return IdentityCompressor()


def create_heuristic_compressor() -> HeuristicCompressor:
    return HeuristicCompressor()
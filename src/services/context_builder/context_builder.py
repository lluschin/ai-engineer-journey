import logging
from models.chat_models import Source

CONTEXT_BUILDER_VERSION = 1.3

_SCORE_THRESHOLD: float = 0.4
_MAX_CHARS = 2500

logger = logging.getLogger(__name__)


def create_context(context: list[Source]) -> tuple[str, int]:
    context_text = ""

    for i, source in enumerate(context):
        nos = i
        if source.score > _SCORE_THRESHOLD and \
            len(context_text) + len(source.document) <= _MAX_CHARS: 
            context_text += f"\n\n{i}: Score{source.score}\n{source.document}"
        else:
            logger.debug(f'used first {i} of the context sources.')
            break

    return (context_text, nos)


def create_context_v01(context: list[Source]) -> str:
    return ("\n\n".join([c.document for c in context]), len(context))
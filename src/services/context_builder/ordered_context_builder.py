import logging

from models.chat_models import Source
from services.context_builder.simple_context_builder import SimpleContextBuilder

_SCORE_THRESHOLD: float = 0.4
_MAX_CHARS = 2500

logger = logging.getLogger(__name__)

class OrderedContextBuilder(SimpleContextBuilder):
    
    def create_context(self, context: list[Source]) -> tuple[str, int]:
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

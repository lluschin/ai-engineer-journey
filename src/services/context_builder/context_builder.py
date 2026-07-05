from models.chat_models import Source

CONTEXT_BUILDER_VERSION = 1.0

_SCORE_THRESHOLD: float = 0.4
_MAX_CHARS = 1000


def create_context(context: list[Source]) -> str:
    context_text = ""

    for i, source in enumerate(context):
        if source.score > _SCORE_THRESHOLD and \
            len(context_text) + len(source.document) <= _MAX_CHARS: 
            context_text += f"\n\n{i}: Score{source.score}\n{source.document}"

    return context_text
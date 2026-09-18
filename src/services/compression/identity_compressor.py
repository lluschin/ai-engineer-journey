from src.models.chat_models import Source

class IdentityCompressor:

    def __init__(self):
        pass


    def compress(self, query: str, context: list[Source]) -> list[Source]:
        return context

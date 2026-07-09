
from models.chat_models import Source

class IdentityRanker:

    def __init__(self):
        pass


    def rank(self, query: str, context: list[Source]) -> list[Source]:
        return self.context
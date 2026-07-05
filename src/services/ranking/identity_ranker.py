
from models.chat_models import Source

class IdentityRanker:

    def __init__(self, query: str, context: list[Source]):
        self.query = query
        self.context = context


    def rank(self) -> list[Source]:
        return self.context
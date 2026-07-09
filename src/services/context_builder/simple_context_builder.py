from models.chat_models import Source

class SimpleContextBuilder:

    def create_context(self, context: list[Source]) -> str:
        return ("\n\n".join([c.document for c in context]), len(context))
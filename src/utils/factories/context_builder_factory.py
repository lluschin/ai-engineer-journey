from services.context_builder.simple_context_builder import SimpleContextBuilder
from services.context_builder.ordered_context_builder import OrderedContextBuilder

def create_simple_context_builder() -> SimpleContextBuilder:
    return SimpleContextBuilder()


def create_ordered_context_builder() -> OrderedContextBuilder:
    return OrderedContextBuilder()
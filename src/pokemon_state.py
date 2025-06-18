from typing import Annotated, TypedDict
from langchain_core.messages import AnyMessage
from langgraph.graph.message import add_messages

from src.pokemon_type_chart import PokemonTypeChart


class PokemonState(TypedDict):
    """State for the Pokemon Agent"""
    messages: Annotated[list[AnyMessage], add_messages]
    is_input_valid: bool | None
    pokemon_name: str | None
    pokemon_types: tuple[str, ...] | None
    pokemon_type_chart: PokemonTypeChart | None
    output_message: str | None

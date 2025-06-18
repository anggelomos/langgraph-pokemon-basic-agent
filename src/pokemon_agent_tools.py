from langchain_openai import ChatOpenAI
import pokebase as pb

from src.pokemon_type_chart import PokemonTypeChart
from src.logging_config import get_logger

logger = get_logger(__name__)


def get_pokemon_types(pokemon_name: str) -> list[str]:
    """Get the type of a pokemon.
    
    Args:
        pokemon_name: The name of the pokemon.

    Returns:
        A list of pokemon types.
    """
    logger.info(f"Getting type for pokemon: {pokemon_name}")
    
    if not pokemon_name:
        logger.warning("Invalid input: Pokemon name is empty")
        return []
    
    if not isinstance(pokemon_name, str):
        logger.warning("Invalid input: Pokemon name is not a string")
        return []
    
    try:
        pokemon_data = pb.pokemon(pokemon_name.lower())
        pokemon_types = [type.type.name for type in pokemon_data.types]
        logger.info(f"Pokemon {pokemon_name} has types: {pokemon_types}")
        return pokemon_types
    except Exception as e:
        logger.error(f"Error getting pokemon type for {pokemon_name}: {e}")
        return []


def get_type_chart(pokemon_types: list[str]) -> PokemonTypeChart:
    """Get the type chart for a pokemon.
    
    Args:
        pokemon_types: A list of pokemon types.

    Returns:
        A PokemonTypeChart object.
    """
    logger.info(f"Getting type chart for types: {pokemon_types}")
    if not pokemon_types:
        logger.warning("Invalid input: Pokemon type is empty")
        return PokemonTypeChart()
    
    if not isinstance(pokemon_types, list):
        logger.warning("Invalid input: Pokemon type is not a list")
        return PokemonTypeChart()
    
    type_key_map = {
        "double_damage_from": 2,
        "half_damage_from": 0.5,
        "no_damage_from": 0,
    }

    raw_type_charts = []
    types_available = set()
    logger.info(f"Getting type chart for types: {pokemon_types}")
    for pokemon_type in pokemon_types:
        type_chart = {}
        type_data = pb.type_(pokemon_type)
        for type_key, type_value in type_key_map.items():
            type_chart.update({ t.name: type_value for t in getattr(type_data.damage_relations, type_key, []) })
            types_available.update(type_chart.keys())
        raw_type_charts.append(type_chart)

    type_charts = {}
    if len(pokemon_types) == 1:
        type_charts = raw_type_charts[0]
    else:
        for pokemon_type in types_available:
            type_value_1 = raw_type_charts[0].get(pokemon_type, 1)
            type_value_2 = raw_type_charts[1].get(pokemon_type, 1)
            type_value = type_value_1 * type_value_2
            type_charts[pokemon_type] = type_value
    
    logger.info(f"Type charts: {type_charts}")
    logger.info(f"Types available: {types_available}")
    logger.info("Getting final type chart")
    pokemon_type_chart = PokemonTypeChart()
    for type_key, type_value in type_charts.items():
        if type_value == 4:
            pokemon_type_chart.super_effective.add(type_key)
        elif type_value == 2:
            pokemon_type_chart.effective.add(type_key)
        elif type_value == 1:
            continue
        elif type_value == 0.5:
            pokemon_type_chart.resistant.add(type_key)
        elif type_value == 0.25:
            pokemon_type_chart.super_resistant.add(type_key)
        elif type_value == 0:
            pokemon_type_chart.immune.add(type_key)
        else:
            logger.warning(f"Unknown type value: {type_value} for type: {type_key}")

    logger.info(f"Final type chart: {pokemon_type_chart}")
    return pokemon_type_chart
    
# Equip the butler with tools
tools = [
    get_pokemon_types,
    get_type_chart
]

logger.info("Initializing LLM with GPT-4o model")
llm = ChatOpenAI(model="gpt-4o")
llm_with_tools = llm.bind_tools(tools, parallel_tool_calls=False)
logger.info("LLM initialized successfully with tools")

from typing import Any

from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
import pokebase as pb

from src.pokemon_agent_tools import get_pokemon_types, get_type_chart, llm, llm_with_tools
from src.pokemon_agent_prompts import EXTRACT_POKEMON_NAME_PROMPT, FORMAT_INVALID_INPUT_RESPONSE_PROMPT, MAIN_POKEMON_ASSISTANT_PROMPT, PokemonNameOutput
from src.pokemon_state import PokemonState
from src.logging_config import get_logger

logger = get_logger(__name__)


def check_input(state: PokemonState) -> dict[str, Any]:
    """Check's if the user's input is valid"""
    logger.info("Starting input validation process")
    
    user_message = state["messages"][-1].content
    logger.debug(f"User message: {user_message}")

    if not user_message:
        logger.warning("Empty user message received")
        return {"is_input_valid": False, "pokemon_name": None}

    llm_with_structured_output = llm.with_structured_output(PokemonNameOutput)
    system_message = SystemMessage(content=EXTRACT_POKEMON_NAME_PROMPT)
    messages = [system_message, HumanMessage(content=user_message)]
    
    for attempt_number in range(3):
        logger.info(f"Attempt {attempt_number + 1} to extract the pokemon name")

        try:
            extracted_pokemon_name = llm_with_structured_output.invoke(messages)["pokemon_name"].lower()

            # Validate pokemon exists in the PokeAPI
            expected_pokemon = pb.pokemon(extracted_pokemon_name)
            if expected_pokemon.id:
                logger.info(f"Successfully validated pokemon: {extracted_pokemon_name} (ID: {expected_pokemon.id})")
                return {"is_input_valid": True, "pokemon_name": extracted_pokemon_name.lower()}
                
        except Exception as e:
            logger.warning(f"Failed to validate pokemon '{extracted_pokemon_name}': {str(e)}")
            messages.append(AIMessage(content=f"The extracted pokemon name {extracted_pokemon_name} is not a valid Pokemon name, let's try again."))

    logger.error("Failed to extract valid pokemon name after 3 attempts")
    return {"is_input_valid": False, "pokemon_name": None, "messages": messages}


def pokemon_agent(state: PokemonState) -> dict[str, Any]:
    """The agent that will be used to get the pokemon's type"""
    logger.info("Starting pokemon agent processing")
    textual_description_of_tool="""get_pokemon_types(pokemon_name: str) -> list[str]:
                                    Get the type of a pokemon.
                                    
                                    Args:
                                        pokemon_name: The name of the pokemon.

                                    Returns:
                                        A list of pokemon types.
    
                                get_type_chart(pokemon_types: list[str]) -> PokemonTypeChart:
                                    Get the type chart for a pokemon.
                                    
                                    Args:
                                        pokemon_types: A list of pokemon types.

                                    Returns:
                                        A PokemonTypeChart object.
                                """
    sys_msg = SystemMessage(content=MAIN_POKEMON_ASSISTANT_PROMPT.format(textual_description_of_tool))
    
    logger.info(llm_with_tools.invoke([sys_msg] + state["messages"]))

    pokemon_types = get_pokemon_types(state["pokemon_name"])
    pokemon_type_chart = get_type_chart(pokemon_types)
    
    return {
        "pokemon_types": pokemon_types,
        "pokemon_type_chart": pokemon_type_chart
    }


def format_output(state: PokemonState) -> dict[str, Any]:
    """Format the output of the agent and print it"""
    logger.info("Formatting output")
    
    is_valid = state.get("is_input_valid", False)
    
    if is_valid:
        pokemon_name = state.get("pokemon_name")
        pokemon_types = state.get("pokemon_types")
        pokemon_type_chart = state.get("pokemon_type_chart")

        logger.info(f"Formatting valid response for pokemon: {pokemon_name}")

        output_message = f"The pokemon {pokemon_name} has the following types: {pokemon_types}.\nThis is the type chart with the types that are super effective, effective, resistant, super resistant and immune to the pokemon:\n{str(pokemon_type_chart)}"
    else:
        sys_msg = SystemMessage(content=FORMAT_INVALID_INPUT_RESPONSE_PROMPT)
        output_message = llm.invoke([sys_msg] + state["messages"]).content

    return {
        "output_message": output_message
    }

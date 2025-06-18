"""
Pokemon Agent Runner Script

This script demonstrates how to run the Pokemon agent with logging enabled.
You can customize the logging level and optionally log to a file.
"""

from langchain_core.messages import HumanMessage
from src.main import compiled_graph
from src.pokemon_state import PokemonState
from src.logging_config import setup_logging, get_logger


def run_pokemon_agent(user_input: str, log_level: str = "INFO", log_to_file: bool = False) -> str:
    """
    Run the Pokemon agent with the given user input.
    
    Args:
        user_input: The user's question about a Pokemon
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_to_file: Whether to log to a file in addition to console
        
    Returns:
        The agent's response
    """
    # Setup logging with optional file logging
    log_file = "logs/pokemon_agent.log" if log_to_file else None
    setup_logging(log_level=log_level, log_file=log_file)
    
    logger = get_logger(__name__)
    logger.info(f"Starting Pokemon agent with user input: '{user_input}'")
    
    # Create initial state
    initial_state = PokemonState(
        messages=[HumanMessage(content=user_input)],
        is_input_valid=False,
        pokemon_name=None
    )
    
    try:
        # Run the graph
        logger.info("Invoking Pokemon agent graph")
        result = compiled_graph.invoke(initial_state)
        
        output = result.get("output", "No output generated")
        logger.info(f"Pokemon agent completed successfully. Output: {output}")
        return output
        
    except Exception as e:
        logger.error(f"Error running Pokemon agent: {str(e)}", exc_info=True)
        return f"An error occurred: {str(e)}"


def main():
    """Main function to demonstrate the Pokemon agent."""
    print("Pokemon Agent Demo")
    print("="*50)
    
    # Example queries
    test_queries = [
        "What type is Pikachu?",
        "Tell me about Charizard",
        "What is the type of Bulbasaur?",
        "Invalid pokemon xyz123",
        ""  # Empty input
    ]
    
    for query in test_queries:
        print(f"\nQuery: '{query}'")
        response = run_pokemon_agent(query, log_level="DEBUG", log_to_file=True)
        print(f"Response: {response}")
        print("-" * 30)


if __name__ == "__main__":
    main() 
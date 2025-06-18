from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode, tools_condition

from src.pokemon_agent_nodes import check_input, format_output, pokemon_agent
from src.pokemon_state import PokemonState
from src.pokemon_agent_tools import tools
from src.logging_config import setup_logging, get_logger

# Setup logging for the project
if __name__ == "__main__":
    setup_logging(log_level="INFO")

logger = get_logger(__name__)


def validate_input(state: PokemonState) -> str:
    """Determine the next step based on spam classification"""
    is_valid = state["is_input_valid"]
    logger.debug(f"Input validation result: {is_valid}")
    
    if is_valid:
        logger.info("Input is valid, proceeding to pokemon agent")
        return "valid_input"
    else:
        logger.info("Input is invalid, skipping to output formatting")
        return "invalid_input"


logger.info("Building Pokemon Agent StateGraph")
builder = StateGraph(PokemonState)

# Add nodes to the graph
logger.debug("Adding nodes to the graph")
builder.add_node("check_input", check_input)
builder.add_node("pokemon_agent", pokemon_agent)
builder.add_node("tools", ToolNode(tools))
builder.add_node("format_output", format_output)

# Add edges to the graph
logger.debug("Adding edges to the graph")
builder.add_edge(START, "check_input")
builder.add_conditional_edges(
    "check_input",
    validate_input,
    {
        "valid_input": "pokemon_agent",
        "invalid_input": "format_output"
    }
)
builder.add_conditional_edges(
    "pokemon_agent",
    tools_condition,
    {
        "tools": "tools",
        "__end__": "format_output"
    }
)
builder.add_edge("tools", "pokemon_agent")
builder.add_edge("format_output", END)

logger.info("Compiling the StateGraph")
compiled_graph = builder.compile()

logger.info("Generating graph visualization")
compiled_graph.get_graph().draw_mermaid_png(
    output_file_path="pokemon_agent_graph.png"   # ruta donde quieres el PNG
)
logger.info("Graph visualization saved to pokemon_agent_graph.png")
logger.info("Pokemon Agent StateGraph setup completed successfully")

# Export the compiled graph for use by runner scripts
__all__ = ["compiled_graph"]

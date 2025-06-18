#!/usr/bin/env python3
"""
Runner script for the Pokemon Agent.
This script properly imports and runs the main application.
"""

from langchain_core.messages import HumanMessage

def main():
    """Main entry point for the Pokemon Agent"""
    from src.main import compiled_graph
    from src.logging_config import setup_logging, get_logger
    
    # Setup logging for the project
    setup_logging(log_level="CRITICAL")
    logger = get_logger(__name__)
    
    # Start interactive chat loop
    logger.info("Starting interactive chat loop")
    print("Pokemon Agent is ready! Type '*' to exit.")
    
    while True:
        user_input = input("You: ")
        
        if user_input == "*":
            logger.info("Received exit signal, ending chat")
            break
        
        messages = [HumanMessage(content=user_input)]
        response = compiled_graph.invoke({"messages": messages})
        print(f"Agent: {response.get('output_message', 'No response generated')}")

    logger.info("Chat session ended")

if __name__ == "__main__":
    main() 
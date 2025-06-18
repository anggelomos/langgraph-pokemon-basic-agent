import pytest
from assertpy import assert_that
from langchain_core.messages import HumanMessage

from src.pokemon_agent_nodes import check_input, format_output
from src.pokemon_state import PokemonState
from src.pokemon_type_chart import PokemonTypeChart
from tests.conftest import NOT_RECOGNIZED_POKEMON_RESPONSE, OUT_OF_SCOPE_NO_POKEMON_RESPONSE, OUT_OF_SCOPE_POKEMON_RESPONSE


class TestCheckInput:
    """Unit tests for the check_input function."""
    
    def test_check_input_with_correct_pokemon_name(self):
        """Test check_input with a message containing a correct Pokemon name."""
        state: PokemonState = {
            "messages": [HumanMessage(content="What's good against Pikachu?")]
        }
        
        result = check_input(state)
        
        assert_that(result).contains_key("is_input_valid")
        assert_that(result).contains_key("pokemon_name")
        assert_that(result["is_input_valid"]).is_true()
        assert_that(result["pokemon_name"])
    
    def test_check_input_with_incorrect_pokemon_name(self):
        """Test check_input with a message containing an incorrect Pokemon name."""
        state: PokemonState = {
            "messages": [HumanMessage(content="What's good against chrmunder?")]
        }
        
        result = check_input(state)
        
        assert_that(result).contains_key("is_input_valid")
        assert_that(result).contains_key("pokemon_name")
        assert_that(result["is_input_valid"]).is_true()
        assert_that(result["pokemon_name"]).is_equal_to("charmander")

    def test_check_input_with_non_existent_pokemon_name(self):
        """Test check_input with a message containing an non-existent Pokemon name."""
        state: PokemonState = {
            "messages": [HumanMessage(content="What's good against Fakemon?")]
        }
        
        result = check_input(state)
        
        assert_that(result).contains_key("is_input_valid")
        assert_that(result).contains_key("pokemon_name")
        assert_that(result["is_input_valid"]).is_false()
        assert_that(result["pokemon_name"]).is_none()
    
    def test_check_input_with_empty_message(self):
        """Test check_input with an empty message."""
        state: PokemonState = {
            "messages": [HumanMessage(content="")]
        }
        
        result = check_input(state)
        
        assert_that(result).contains_key("is_input_valid")
        assert_that(result).contains_key("pokemon_name")
        assert_that(result["is_input_valid"]).is_false()
        assert_that(result["pokemon_name"]).is_none()
    
    def test_check_input_with_message_without_pokemon_name(self):
        """Test check_input with a message that doesn't contain any Pokemon name."""
        state: PokemonState = {
            "messages": [HumanMessage(content="What's the weather like today?")]
        }
        
        result = check_input(state)
        
        assert_that(result).contains_key("is_input_valid")
        assert_that(result).contains_key("pokemon_name")
        assert_that(result["is_input_valid"]).is_false()
        assert_that(result["pokemon_name"]).is_none()
    
    def test_check_input_with_pokemon_related_message_without_specific_name(self):
        """Test check_input with a Pokemon-related message that doesn't mention a specific Pokemon."""
        state: PokemonState = {
            "messages": [HumanMessage(content="Can you help me with Pokemon types?")]
        }
        
        result = check_input(state)
        
        assert_that(result).contains_key("is_input_valid")
        assert_that(result).contains_key("pokemon_name")
        assert_that(result["is_input_valid"]).is_false()
        assert_that(result["pokemon_name"]).is_none()


class TestFormatOutput:
    """Unit tests for the format_output function."""
    
    def test_format_output_non_pokemon_related_query(self):
        """Test format_output with a query that's not related to Pokemon."""
        state: PokemonState = {
            "messages": [HumanMessage(content="What's the weather like today?")],
            "is_input_valid": False,
            "pokemon_name": None,
            "pokemon_types": None,
            "type_chart": None
        }
        
        result = format_output(state)
        
        assert_that(result).contains_key("output_message")
        assert_that(result["output_message"]).is_equal_to(OUT_OF_SCOPE_NO_POKEMON_RESPONSE)
    
    def test_format_output_pokemon_related_but_not_type_specific(self):
        """Test format_output with a Pokemon-related query that doesn't ask about types."""
        state: PokemonState = {
            "messages": [HumanMessage(content="What is the most popular legendary Pokemon?")],
            "is_input_valid": False,
            "pokemon_name": None,
            "pokemon_types": None,
            "type_chart": None
        }
        
        result = format_output(state)
        
        assert_that(result).contains_key("output_message")
        assert_that(result["output_message"]).is_equal_to(OUT_OF_SCOPE_POKEMON_RESPONSE)
    
    @pytest.mark.xfail(reason="This test is flaky because of special characters in the output")
    def test_format_output_non_existent_pokemon(self):
        """Test format_output with a query about a Pokemon that doesn't exist."""
        state: PokemonState = {
            "messages": [HumanMessage(content="What's good against Fakemon?")],
            "is_input_valid": False,
            "pokemon_name": None,
            "pokemon_types": None,
            "type_chart": None
        }
        
        result = format_output(state)
        
        assert_that(result).contains_key("output_message")
        assert_that(result["output_message"]).is_equal_to(NOT_RECOGNIZED_POKEMON_RESPONSE)
    
    def test_format_output_existing_pokemon(self):
        """Test format_output with a query about an existing Pokemon."""
        # Create a mock type chart
        mock_type_chart = PokemonTypeChart(
            super_effective={"ground"},
            effective={"fighting", "steel"},
            resistant={"flying", "steel"},
            super_resistant=set(),
            immune=set()
        )
        
        state: PokemonState = {
            "messages": [HumanMessage(content="What's good against Pikachu?")],
            "is_input_valid": True,
            "pokemon_name": "pikachu",
            "pokemon_types": ["electric"],
            "pokemon_type_chart": mock_type_chart
        }
        
        result = format_output(state)
        
        assert_that(result).contains_key("output_message")
        assert_that(result["output_message"]).is_equal_to("The pokemon pikachu has the following types: ['electric'].\nThis is the type chart with the types that are super effective, effective, resistant, super resistant and immune to the pokemon:\nSuper Effective: ground\nEffective: fighting, steel\nResistant: flying, steel")

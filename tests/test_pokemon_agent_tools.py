from assertpy import assert_that
import pytest

from src.pokemon_agent_tools import get_pokemon_types, get_type_chart
from src.pokemon_type_chart import PokemonTypeChart


class TestGetPokemonTypes:
    """Unit tests for the get_pokemon_type function."""
    
    def test_get_pokemon_type_with_single_type(self):
        """Test get_pokemon_type with a Pokemon that has one type."""
        result = get_pokemon_types("pikachu")
        
        assert_that(result).is_not_none()
        assert_that(result).is_instance_of(list)
        assert_that(result).is_length(1)
        assert_that(result[0]).is_equal_to("electric")
    
    def test_get_pokemon_type_with_dual_type(self):
        """Test get_pokemon_type with a Pokemon that has two types."""
        result = get_pokemon_types("Charizard")
        
        assert_that(result).is_not_none()
        assert_that(result).is_instance_of(list)
        assert_that(result).is_length(2)
        assert_that(result).contains("fire", "flying")
    
    @pytest.mark.parametrize("pokemon_name", [
        "Fakemon",  # Non-existent pokemon
        ""  # Empty name
    ])
    def test_get_pokemon_type_with_invalid_input(self, pokemon_name):
        """Test get_pokemon_type with invalid inputs."""
        result = get_pokemon_types(pokemon_name)
        
        assert_that(result).is_not_none()
        assert_that(result).is_instance_of(list)
        assert_that(result).is_empty()

class TestGetTypeChart:
    """Unit tests for the get_type_chart function."""
    
    @pytest.mark.parametrize("pokemon_types,expected_type_chart", [
        # Single type
        (["electric"], PokemonTypeChart(
            super_effective=[],
            effective=["ground"],
            resistant=["electric", "flying", "steel"],
            super_resistant=[],
            immune=[]
        )),

        # Double type
        (["fire", "flying"], PokemonTypeChart(
            super_effective=["rock"],
            effective=["water", "electric"],
            resistant=["fire", "fighting", "steel", "fairy"],
            super_resistant=["grass", "bug"],
            immune=["ground"]
        )),

        # No type
        ([], PokemonTypeChart())
    ])
    def test_get_type_chart(self, pokemon_types, expected_type_chart):
        """Test get_type_chart with a single type input."""
        result = get_type_chart(pokemon_types)
        
        assert_that(result).is_not_none()
        assert_that(result).is_instance_of(PokemonTypeChart)
        assert_that(result).is_equal_to(expected_type_chart)

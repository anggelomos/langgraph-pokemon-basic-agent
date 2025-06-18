import pytest

# TODO: Remove this line if it's not needed.
# Add src directory to Python path for imports
# sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

OUT_OF_SCOPE_NO_POKEMON_RESPONSE = "I can only help with type strengths and weaknesses against specific Pokémon. Please ask about a Pokémon to continue."
OUT_OF_SCOPE_POKEMON_RESPONSE = "I'm here to provide type advantages and disadvantages against specific Pokémon only. Please ask which types are strong or weak against a Pokémon."
NOT_RECOGNIZED_POKEMON_RESPONSE = "I couldn't find that Pokémon. Please check the name and try again."
OUT_OF_SCOPE_RESPONSE = "I can only help with Pokémon-related questions. Please ask about a specific Pokémon's types or type effectiveness."

@pytest.fixture(scope="session")
def pokemon_type_chart():
    """Pokemon type effectiveness chart for testing."""
    return {
        'electric': {
            'super_effective': [],
            'effective': ["ground"],
            'resistant': ["electric", "flying", "steel"],
            'super_resistant': [],
            'immune': []
        },
        'fire_flying': {
            'super_effective': ["rock"],
            'effective': ["water", "electric"],
            'resistant': ["fire", "fighting", "steel", "fairy"],
            'super_resistant': ["grass", "bug"],
            'immune': ["ground"]
        },
        'water': {
            'super_effective': [],
            'effective': ["electric", "grass"],
            'resistant': ["fire", "water", "ice", "steel"],
            'super_resistant': [],
            'immune': []
        }
    }

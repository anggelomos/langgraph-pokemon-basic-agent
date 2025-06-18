from attrs import define, field


@define
class PokemonTypeChart:
    """Represents the type effectiveness chart for Pokemon types."""
    super_effective: set[str] = field(factory=set, converter=set)
    effective: set[str] = field(factory=set, converter=set)
    resistant: set[str] = field(factory=set, converter=set)
    super_resistant: set[str] = field(factory=set, converter=set)
    immune: set[str] = field(factory=set, converter=set)

    def __str__(self) -> str:
        """Return a string representation of non-empty type effectiveness attributes."""
        output_parts = []
        
        if self.super_effective:
            output_parts.append(f"Super Effective: {', '.join(sorted(self.super_effective))}")
            
        if self.effective:
            output_parts.append(f"Effective: {', '.join(sorted(self.effective))}")
            
        if self.resistant:
            output_parts.append(f"Resistant: {', '.join(sorted(self.resistant))}")
            
        if self.super_resistant:
            output_parts.append(f"Super Resistant: {', '.join(sorted(self.super_resistant))}")
            
        if self.immune:
            output_parts.append(f"Immune: {', '.join(sorted(self.immune))}")
            
        return "\n".join(output_parts)

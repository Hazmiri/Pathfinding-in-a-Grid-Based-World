# tests/test_world_loading.py
"""
Tests for Map_Anvil: terrain loading, normalisation, validation,
and structural integrity of the forged grid.
"""

import pytest
from runes.runes import PathGlyph
from world.grid_forge import Map_Anvil
from world.terrain_legends import TERRAIN_CATALOGUE

def test_load_long_names(tmp_path):
    """Ensure long terrain names load successfully."""
    file = tmp_path / "long_map.json"
    file.write_text("""
    [
        ["whispering_grassland", "forest_of_reflections"],
        ["muddy_marsh", "wall_of_ancients"]
    ]
    """)
    world = Map_Anvil(str(file))
    assert world.width == 2
    assert world.height == 2
    assert world.terrain_at(PathGlyph(0, 0)) == "whispering_grassland"
    
    
def test_load_short_codes(tmp_path):
    """Ensure short codes convert correctly to long names."""
    file = tmp_path / "short_map.json"
    file.write_text("""
    [
        ["WG", "FR"],
        ["MM", "WA"]
    ]
    """)
    world = Map_Anvil(str(file))
    assert world.terrain_at(PathGlyph(0, 0)) == "whispering_grassland"
    assert world.terrain_at(PathGlyph(1, 1)) == "wall_of_ancients"

def test_invalid_terrain_raises(tmp_path):
    """Unknown terrain must raise a ValueError."""
    file = tmp_path / "bad.json"
    file.write_text("""
    [
        ["WG", "???"]
    ]
    """)

    with pytest.raises(ValueError):
        Map_Anvil(str(file))
        
def test_non_rectangular_map_rejected(tmp_path):
    """Map rows must be the same length."""
    file = tmp_path / "non_rect.json"
    file.write_text("""
    [
        ["WG", "WG"],
        ["WG"]
    ]
    """)
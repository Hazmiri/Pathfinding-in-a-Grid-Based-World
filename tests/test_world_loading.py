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
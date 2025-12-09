# tests/test_pathfinder_energy.py
"""
Tests for Saladin_Pathfinder in 'lowest_energy' mode.
Ensures cost-aware paths outperform step-only paths.
"""

from runes.runes import PathGlyph
from world.grid_forge import Map_Anvil
from aris.saladin_pathfinder import Saladin_Pathfinder
from world.terrain_legends import TERRAIN_CATALOGUE

def test_energy_prefers_low_cost_cells(tmp_path):
    """
    The algortihm should avoid high-cost terrain when possible.
    
    """
    file = tmp_path / "energy_map.json"
    file.write_text("""
    [
        ["WG", "WG", "WG"],
        ["DD", "DD", "DD"],
        ["WG", "WG", "WG"]
    ]
    """)
    
    world = Map_Anvil(str(file))
    pf = Saladin_Pathfinder(world, mode="lowest_energy")

    hearth = PathGlyph(0, 1)
    pythonia = PathGlyph(2, 1)

    path = pf.chart_course(hearth, pythonia)
    assert path is not None

    # Path should move DOWN then across then UP
    turned_path = [g.coords() for g in path]
    assert (1, 1) not in turned_path  # avoid the centre Desert_of_Doom row
    
def test_energy_blocked_terrain(tmp_path):
    """Must not attempt to cross impassable terrain."""
    file = tmp_path / "impass.json"
    file.write_text("""
    [
        ["WG", "WA", "WG"]
    ]
    """)

    world = Map_Anvil(str(file))
    pf = Saladin_Pathfinder(world, mode="lowest_energy")

    hearth = PathGlyph(0, 0)
    pythonia = PathGlyph(2, 0)

    path = pf.chart_course(hearth, pythonia)
    assert path is None  # the wall blocks all paths 
       
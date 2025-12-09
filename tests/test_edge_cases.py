# tests/test_edge_cases.py
"""
Edge case tests for Saladin_Pathfinder.
"""

from runes.runes import PathGlyph
from world.grid_forge import Map_Anvil
from aris.saladin_pathfinder import Saladin_Pathfinder

def test_start_equals_goal(tmp_path):
    file = tmp_path / "simple.json"
    file.write_text('[["WG"]]')

    world = Map_Anvil(str(file))
    pf = Saladin_Pathfinder(world)

    hearth = pythonia = PathGlyph(0, 0)
    path = pf.chart_course(hearth, pythonia)
    assert path == [hearth]
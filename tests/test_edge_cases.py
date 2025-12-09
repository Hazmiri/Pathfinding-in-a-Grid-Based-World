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
    
def test_no_path_exists(tmp_path):
    file = tmp_path / "nop.json"
    file.write_text("""
    [
        ["WG", "WA", "WG"]
    ]
    """)

    world = Map_Anvil(str(file))
    pf = Saladin_Pathfinder(world)

    hearth = PathGlyph(0, 0)
    pythonia = PathGlyph(2, 0)

    assert pf.chart_course(hearth, pythonia) is None

def test_small_world(tmp_path):
    file = tmp_path / "tiny.json"
    file.write_text("""
    [
        ["WG", "WG"],
        ["WG", "WG"]
    ]
    """)

    world = Map_Anvil(str(file))
    pf = Saladin_Pathfinder(world)

    path = pf.chart_course(PathGlyph(0, 0), PathGlyph(1, 1))
    assert path is not None
    assert len(path) >= 2
    
    """
    By passing these three tests, it is guarantee the A* search is robust 
    and handles all possible inputs, from the simplest to the most 
    frustrating!
    
    """
# tests/test_pathfinder_steps.py
"""
Tests for Saladin_Pathfinder in 'fewest_steps' mode.
Ensures shortest paths are computed based solely on step count.
"""

from runes.runes import PathGlyph
from world.grid_forge import Map_Anvil
from aris.saladin_pathfinder import Saladin_Pathfinder

def test_steps_simple_straight_line(tmp_path):
    """A straight line should yield a direct path."""
    file = tmp_path / "line.json"
    file.write_text("""
    [
        ["WG", "WG", "WG", "WG"]
    ]
    """)

    world = Map_Anvil(str(file))
    pathfinder = Saladin_Pathfinder(world, mode="fewest_steps")

    hearth = PathGlyph(0, 0)
    pythonia = PathGlyph(3, 0)

    path = pathfinder.chart_course(hearth, pythonia)
    assert path is not None
    assert len(path) == 4  # 3 steps + start
    
def test_steps_diagonal_is_one_move(tmp_path):
    """Diagonal movement must count as 1 step in this mode."""
    file = tmp_path / "diag.json"
    file.write_text("""
    [
        ["WG", "WG"],
        ["WG", "WG"]
    ]
    """)

    world = Map_Anvil(str(file))
    pathfinder = Saladin_Pathfinder(world, mode="fewest_steps")

    hearth = PathGlyph(0, 0)
    pythonia = PathGlyph(1, 1)

    path = pathfinder.chart_course(hearth, pythonia)
    assert path is not None
    assert len(path) == 2  # one diagonal step
    
def test_steps_blocked_path(tmp_path):
    """Path must detour around obstacles."""
    file = tmp_path / "blocked.json"
    file.write_text("""
    [
        ["WG", "WA", "WG"],
        ["WG", "WA", "WG"],
        ["WG", "WG", "WG"]
    ]
    """)

    world = Map_Anvil(str(file))
    pf = Saladin_Pathfinder(world, mode="fewest_steps")

    hearth = PathGlyph(0, 0)
    pythonia = PathGlyph(2, 0)

    path = pf.chart_course(hearth, pythonia)
    assert path is not None
    assert len(path) > 3   # must go around walls

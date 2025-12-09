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
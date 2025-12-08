"""
main.py
-------

Simple demonstration runner for Saladin_Pathfinder.
"""

from runes import PathGlyph
from world.grid_forge import Map_Anvil
from aris.saladin_pathfinder import Saladin_Pathfinder


def run_demo(mode: str = "lowest_energy"):
    world = Map_Anvil("maps/demo_world.json")

    hearth = PathGlyph(0, 2)      # left middle
    pythonia = PathGlyph(6, 2)    # right middle

    navigator = Saladin_Pathfinder(world, mode=mode)
    path = navigator.chart_course(hearth, pythonia)
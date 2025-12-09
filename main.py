"""
main.py
-------

Simple demonstration runner for Saladin_Pathfinder.
"""

from runes.runes import PathGlyph
from world.grid_forge import Map_Anvil
from aris.saladin_pathfinder import Saladin_Pathfinder


def run_demo(mode: str = "lowest_energy"):
    world = Map_Anvil("maps/demo_world.json")

    hearth = PathGlyph(0, 2)      # left middle
    pythonia = PathGlyph(6, 2)    # right middle

    navigator = Saladin_Pathfinder(world, mode=mode)
    path = navigator.chart_course(hearth, pythonia)

    if path is None:
        print(f"No path found in mode: {mode}")
        return

    ascii_map = world.render_ascii(path=path, hearth=hearth, pythonia=pythonia)
    print(f"Mode: {mode}")
    print(ascii_map)
    print("\nPath glyphs:", path)
    print("Steps:", len(path) - 1)


if __name__ == "__main__":
    print("=== Fewest steps mode ===")
    run_demo(mode="fewest_steps")
    print("\n=== Lowest energy mode ===")
    run_demo(mode="lowest_energy")

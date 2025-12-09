"""
main.py
-------
Command-line demonstration of the Saladin Pathfinder.
Used for development, debugging and testing before UI integration.
"""

from aris.saladin_pathfinder import Saladin_Pathfinder
from world.grid_forge import Map_Anvil
from runes.runes import PathGlyph

def run_demo(world_path: str, start, goal):
    print(f"\n=== Running demo for map: {world_path} ===")

    world = Map_Anvil(world_path)

    hearth = PathGlyph(*start)
    pythonia = PathGlyph(*goal)

    for mode in ["fewest_steps", "lowest_energy"]:
        print(f"\n=== Mode: {mode} ===")
        pf = Saladin_Pathfinder(world, mode=mode)

        path = pf.chart_course(hearth, pythonia)

        if path is None:
            print("No path found.\n")
            continue

        # Print ASCII map
        print(world.render_ascii(path=path, hearth=hearth, pythonia=pythonia))

        # Print path details
        print("\nPath glyphs:", path)
        print("Steps:", len(path) - 1)

        # Compute cost
        total_cost = 0
        for i in range(len(path) - 1):
            total_cost += pf._movement_cost(path[i], path[i+1])

        print(f"Total cost: {round(total_cost, 3)}")

if __name__ == "__main__":
    run_demo("default_world.json", (0, 0), (19, 9))

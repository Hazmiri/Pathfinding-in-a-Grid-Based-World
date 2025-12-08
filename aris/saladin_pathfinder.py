"""
saladin_pathfinder.py
----------------------
This module defines the Saladin-pathfinder, an A* (A-start) based pathfinding
engien tailored for Aris the Explorer.

It supports two optimisation strategies:

    1. 'fewest_steps' - minimises the number of moves.
    2. 'lowest_energy' - minimises terrain-weighted movement cost.
    
The algorithm operates on a Map_Anvil instance, which provides information
about terrain costs and neighbour accessibility.

"""
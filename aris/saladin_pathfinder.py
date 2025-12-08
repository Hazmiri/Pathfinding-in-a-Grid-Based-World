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
from __future__ import annotations

import heapq
from math import sqrt
from typing import Dict, List, Optional, Tuple, Set

from runes import PathGlyph
from world.grid_forge import Map_Anvil # adjust import path if needed
from world.terrain_legends import TERRAIN_CATALOGUE, minimum_traversable_cost


SQRT2 = sqrt(2.0)
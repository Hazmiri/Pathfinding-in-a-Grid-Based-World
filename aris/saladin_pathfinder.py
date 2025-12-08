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

from world.runes import PathGlyph
from world.grid_forge import Map_Anvil # adjust import path if needed
from world.terrain_legends import TERRAIN_CATALOGUE, minimum_traversable_cost

SQRT2 = sqrt(2.0)

class Saladin_Pathfinder:
    """
    Saladin_Pathfinder executes an A* search over the Map_Anvil grid.
    
    Parameters:
        world_map (Map_Anvil): the forged world grid.
        mode (str): 'fewest_steps' or 'lowest_energy'.
    
    In 'fewest_steps' mode:
        - Step cost is always 1.
        - Heuristic: Chebyshev distance (max(dx, dy)).
        
    In 'lowest_energy' mode:
        - Step cost depends on terrain difficulty and movement geaometry
        - Heuristic: Octile distance scaled by minimum terrain cost.
    """
    
    def __init__(self, world_map: Map_Anvil, mode: str = "lowest_energy"):
        if mode not in ("fewest_steps", "lowest_energy"):
            raise ValueError ("mode must be 'fewest_steps' or 'lowest_energy'.")
        
        self.world_map = world_map
        self.mode = mode
        self._min_cost = minimum_traversable_cost()

# --------------------------------------------------------------------
# PUBLIC INTERFACE
# --------------------------------------------------------------------

def chart_course(
    self, hearth: PathGlyph, pythonia:PathGlyph
) -> Optional [List[PathGlyph]]:
    """
    Compute an optimal path from hearth (start) to pythonia (goal).
    
    Returns:
        A list of PathGlyphs forming the path, including both hearth and
        pythonia, or None if no path can be found.
    """
    if hearth == pythonia:
        # Trivial case: already at destination.
        return [hearth]

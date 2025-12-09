"""
saladin_pathfinder.py
----------------------

Implements the A* pathfinding algorithm with thematic naming.
"""

from typing import Dict, List, Optional, Tuple
import heapq

from runes.runes import PathGlyph
from world.grid_forge import Map_Anvil
from world.terrain_legends import minimum_traversable_cost


class Saladin_Pathfinder:
    """
    Heroic pathfinder inspired by Saladin. Uses A* search to
    chart a course across the forged map.
    """
    
    def __init__(self, world: Map_Anvil, mode: str = "lowest_energy"):
        self.world = world
        self.mode = mode


    # ------------------------------------------------------------
    # PUBLIC INTERFACE (used by tests)
    # ------------------------------------------------------------
    def chart_course(self, hearth: PathGlyph, pythonia: PathGlyph, mode: Optional[str] = None):
        if mode is None:
            mode = self.mode

    # ------------------------------------------------------------
    # INTERNAL: A* SEARCH
    # ------------------------------------------------------------
    def __init__(self, world: Map_Anvil, mode: str = "lowest_energy"):
        self.world = world
        self.mode = mode

    def chart_course(self, hearth: PathGlyph, pythonia: PathGlyph, mode: Optional[str] = None):
        if hearth == pythonia:
            return [hearth]

        if mode is None:
            mode = self.mode
        return self._a_star(hearth, pythonia, mode)

    # ------------------------------------------------------------
    # INTERNAL UTILITIES
    # ------------------------------------------------------------
    def _movement_cost(self, a: PathGlyph, b: PathGlyph) -> float:
        """
        Return terrain cost + diagonal penalty (0.4).
        """
        cost = self.world.cost_at(b)

        if a.is_diagonal_to(b):
            cost += 0.4

        return cost

    def _heuristic(self, a: PathGlyph, b: PathGlyph, mode: str) -> float:
        """
        Chebyshev distance heuristic for diagonal movement.
        """

        dx = abs(a.x - b.x)
        dy = abs(a.y - b.y)

        # fewest steps ignores terrain
        if mode == "fewest_steps":
            return max(dx, dy)

        # lowest energy uses minimum terrain cost
        return max(dx, dy) * minimum_traversable_cost()

    def _reconstruct_path(
        self, came_from: Dict[PathGlyph, Optional[PathGlyph]], current: PathGlyph
    ) -> List[PathGlyph]:

        path = []

        while current is not None:
            path.append(current)
            current = came_from[current]

        path.reverse()
        return path

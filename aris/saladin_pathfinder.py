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

    def __init__(self, world: Map_Anvil):
        self.world = world

    # ------------------------------------------------------------
    # PUBLIC INTERFACE (used by tests)
    # ------------------------------------------------------------
    def chart_course(
        self, hearth: PathGlyph, pythonia: PathGlyph, mode: str = "lowest_energy"
    ) -> Optional[List[PathGlyph]]:
        """
        Chart a path from hearth (start) to pythonia (goal).

        mode:
            "lowest_energy"  → use terrain cost + movement cost
            "fewest_steps"   → each move cost = 1
        """

        # Special case: start == goal
        if hearth == pythonia:
            return [hearth]

        return self._a_star(hearth, pythonia, mode)

    # ------------------------------------------------------------
    # INTERNAL: A* SEARCH
    # ------------------------------------------------------------
    def _a_star(
        self, hearth: PathGlyph, pythonia: PathGlyph, mode: str
    ) -> Optional[List[PathGlyph]]:

        open_set = []
        heapq.heappush(open_set, (0, hearth))

        came_from: Dict[PathGlyph, Optional[PathGlyph]] = {hearth: None}

        g_score: Dict[PathGlyph, float] = {hearth: 0}

        while open_set:
            _, current = heapq.heappop(open_set)

            if current == pythonia:
                return self._reconstruct_path(came_from, current)

            for neighbour in self.world.neighbours(current):

                if mode == "fewest_steps":
                    tentative = g_score[current] + 1
                else:  # lowest_energy
                    tentative = g_score[current] + self._movement_cost(current, neighbour)

                if neighbour not in g_score or tentative < g_score[neighbour]:
                    g_score[neighbour] = tentative
                    came_from[neighbour] = current

                    priority = tentative + self._heuristic(neighbour, pythonia, mode)
                    heapq.heappush(open_set, (priority, neighbour))

        return None  # No path found

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

"""
saladin_pathfinder.py
----------------------
A* Pathfinder for Aris' world.
"""

from typing import Dict, List, Optional
import heapq
import itertools

from runes.runes import PathGlyph
from world.grid_forge import Map_Anvil
from world.terrain_legends import minimum_traversable_cost


class Saladin_Pathfinder:
    """
    Mighty navigator inspired by Saladin.
    Supports:
      - lowest_energy  (terrain cost + diagonal penalty)
      - fewest_steps   (each move cost = 1)
    """

    def __init__(self, world: Map_Anvil, mode: str = "lowest_energy"):
        self.world = world
        self.mode = mode
        self._tie_counter = itertools.count()   # tie-breaker for heapq
        self.last_run_stats = {}  # stores results of the last search

    # ----------------------------------------------------------------------
    # PUBLIC METHOD (used by tests)
    # ----------------------------------------------------------------------
    def chart_course(
        self,
        hearth: PathGlyph,
        pythonia: PathGlyph,
        mode: Optional[str] = None
    ) -> Optional[List[PathGlyph]]:

        if hearth == pythonia:
            return [hearth]

        if mode is None:
            mode = self.mode

        return self._a_star(hearth, pythonia, mode)

    # ----------------------------------------------------------------------
    # INTERNAL: A* SEARCH
    # ----------------------------------------------------------------------
    def _a_star(
        self,
        start: PathGlyph,
        goal: PathGlyph,
        mode: str
    ) -> Optional[List[PathGlyph]]:

        open_set = []
        heapq.heappush(open_set, (0, next(self._tie_counter), start))

        came_from: Dict[PathGlyph, Optional[PathGlyph]] = {start: None}
        g_score: Dict[PathGlyph, float] = {start: 0}

        while open_set:
            _, _, current = heapq.heappop(open_set)

            if current == goal:
                return self._reconstruct_path(came_from, current)

            for neighbour in self.world.neighbours(current):

                if mode == "fewest_steps":
                    tentative = g_score[current] + 1
                else:
                    tentative = g_score[current] + self._movement_cost(current, neighbour)

                if neighbour not in g_score or tentative < g_score[neighbour]:
                    g_score[neighbour] = tentative
                    came_from[neighbour] = current

                    priority = tentative + self._heuristic(neighbour, goal, mode)
                    heapq.heappush(open_set, (priority, next(self._tie_counter), neighbour))

        return None

    # ----------------------------------------------------------------------
    # INTERNAL UTILITIES
    # ----------------------------------------------------------------------
    def _movement_cost(self, a: PathGlyph, b: PathGlyph) -> float:
        """
        Terrain cost + small diagonal penalty.
        """
        cost = self.world.cost_at(b)

        # We implement diagonal detection here because PathGlyph has none.
        if abs(a.x - b.x) == 1 and abs(a.y - b.y) == 1:
            cost += 0.4

        return cost

    def _heuristic(self, a: PathGlyph, b: PathGlyph, mode: str) -> float:
        """
        Chebyshev distance heuristic.
        """
        dx = abs(a.x - b.x)
        dy = abs(a.y - b.y)
        distance = max(dx, dy)

        if mode == "fewest_steps":
            return distance
        else:
            # Lowest-cost walkable terrain
            lowest = minimum_traversable_cost()

            return distance * lowest

    def _reconstruct_path(
        self,
        came_from: Dict[PathGlyph, Optional[PathGlyph]],
        current: PathGlyph
    ) -> List[PathGlyph]:

        path = []
        while current is not None:
            path.append(current)
            current = came_from[current]

        path.reverse()
        return path

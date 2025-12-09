"""
saladin_pathfinder.py
----------------------
A* Pathfinder for Aris' world.
"""

from typing import Dict, List, Optional
import heapq

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

        # Stores metrics for the last completed search
        self.last_run_stats = {}

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
            self.last_run_stats = {
                "nodes_expanded": 0,
                "path_length": 0,
                "total_energy": 0.0,
                "success": True,
            }
            return [hearth]

        if mode is None:
            mode = self.mode

        return self._a_star(hearth, pythonia, mode)

    # ----------------------------------------------------------------------
    # INTERNAL: A* SEARCH  (WITH METRICS)
    # ----------------------------------------------------------------------
    def _a_star(
        self,
        start: PathGlyph,
        goal: PathGlyph,
        mode: str
    ) -> Optional[List[PathGlyph]]:

        # reset metrics
        stats = {
            "nodes_expanded": 0,
            "path_length": 0,
            "total_energy": 0.0,
            "success": False,
        }

        open_set = []
        heapq.heappush(open_set, (0, start))

        came_from: Dict[PathGlyph, Optional[PathGlyph]] = {start: None}
        g_score: Dict[PathGlyph, float] = {start: 0}

        while open_set:
            _, current = heapq.heappop(open_set)
            stats["nodes_expanded"] += 1

            if current == goal:
                path = self._reconstruct_path(came_from, current)

                stats["path_length"] = len(path) - 1

                # total energy cost
                total_energy = 0.0
                for i in range(1, len(path)):
                    total_energy += self._movement_cost(path[i - 1], path[i])
                stats["total_energy"] = total_energy

                stats["success"] = True
                self.last_run_stats = stats
                return path

            for neighbour in self.world.neighbours(current):

                if mode == "fewest_steps":
                    tentative = g_score[current] + 1
                else:
                    tentative = g_score[current] + self._movement_cost(current, neighbour)

                if neighbour not in g_score or tentative < g_score[neighbour]:
                    g_score[neighbour] = tentative
                    came_from[neighbour] = current

                    priority = tentative + self._heuristic(neighbour, goal, mode)
                    heapq.heappush(open_set, (priority, neighbour))

        self.last_run_stats = stats
        return None

    # ----------------------------------------------------------------------
    # INTERNAL UTILITIES
    # ----------------------------------------------------------------------
    def _movement_cost(self, a: PathGlyph, b: PathGlyph) -> float:
        """
        Terrain cost + small diagonal penalty.
        """
        cost = self.world.cost_at(b)
        if a.is_diagonal_to(b):
            cost += 0.4
        return cost

    def _heuristic(self, a: PathGlyph, b: PathGlyph, mode: str) -> float:
        """
        Chebyshev distance heuristic.
        """
        dx = abs(a.x - b.x)
        dy = abs(a.y - b.y)

        if mode == "fewest_steps":
            return max(dx, dy)
        else:
            return max(dx, dy) * minimum_traversable_cost()

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

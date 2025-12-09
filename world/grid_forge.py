"""
grid_forge.py
---------------------------------

This module loads map JSON files, validates the terrain identifiers,
converts short codes to long terrain names, and provides neighbour lookup
and ASCII rendering utilities.
"""

import json
from typing import List, Dict, Optional
from pathlib import Path

from runes.runes import PathGlyph
from world.terrain_legends import (
    TERRAIN_CATALOGUE,
    TERRAIN_SYMBOLS,
    is_valid_terrain,
    minimum_traversable_cost,
)

TERRAIN_SHORTCODES: Dict[str, str] = {
    "WG": "whispering_grassland",
    "FR": "forest_of_reflections",
    "DD": "desert_of_doom",
    "FL": "frozen_lake",
    "MM": "muddy_marsh",
    "SM": "shadow_mountain",
    "WA": "wall_of_ancients",
}


class Map_Anvil:
    """
    Forged world map loader and validator.
    """

    def __init__(self, json_path: str):
        """
        Load and validate a world grid from a JSON file.
        """
        self.json_path = Path(json_path)

        if not self.json_path.exists():
            raise FileNotFoundError(f"Map file not found: {self.json_path}")

        raw_grid = self._load_json()
        self._validate_structure(raw_grid)
        self.grid = self._normalise_grid(raw_grid)

        self.height = len(self.grid)
        self.width = len(self.grid[0])

    # ------------------------------------------------------------
    # INTERNAL UTILITIES
    # ------------------------------------------------------------
    def _load_json(self) -> List[List[str]]:
        """Load the JSON file."""
        with open(self.json_path, "r", encoding="utf-8") as file:
            return json.load(file)

    def _validate_structure(self, raw_grid: List[List[str]]) -> None:
        """Ensure the map is a rectangular 2D list."""
        if not isinstance(raw_grid, list) or len(raw_grid) == 0:
            raise ValueError("Map must be a non-empty 2D list.")

        expected_row_length = len(raw_grid[0])
        for row in raw_grid:
            if not isinstance(row, list):
                raise ValueError("Row in the map is not a list.")
            if len(row) != expected_row_length:
                raise ValueError("Map rows must all be the same length.")

    def _normalise_grid(self, raw_grid: List[List[str]]) -> List[List[str]]:
        """Convert terrain short codes to long names."""
        normalised = []

        for row in raw_grid:
            new_row = []
            for cell in row:
                if is_valid_terrain(cell):
                    new_row.append(cell)
                elif cell in TERRAIN_SHORTCODES:
                    new_row.append(TERRAIN_SHORTCODES[cell])
                else:
                    raise ValueError(f"Unknown terrain identifier: {cell}")
            normalised.append(new_row)

        return normalised

    # ------------------------------------------------------------
    # PUBLIC METHODS
    # ------------------------------------------------------------
    def terrain_at(self, glyph: PathGlyph) -> str:
        return self.grid[glyph.y][glyph.x]

    def cost_at(self, glyph: PathGlyph) -> float:
        return TERRAIN_CATALOGUE[self.terrain_at(glyph)]

    def in_bounds(self, x: int, y: int) -> bool:
        return 0 <= y < self.height and 0 <= x < self.width

    def is_traversable(self, x: int, y: int) -> bool:
        """
        Returns True if the cell at (x, y) is walkable.
        Impassable terrain is 'wall_of_ancients' (WA).
        """
        terrain = self.grid[y][x]
        return TERRAIN_CATALOGUE[self.grid[y][x]] < float("inf")




    def neighbours(self, glyph: PathGlyph) -> List[PathGlyph]:
        """
        Returns all 8 adjacent cells, but ONLY those that are inside the map
        AND are traversable terrain (not WA).
        """
        dirs = [
            (-1, -1), (0, -1), (1, -1),
            (-1,  0),          (1,  0),
            (-1,  1), (0,  1), (1,  1),
        ]

        results = []

        for dx, dy in dirs:
            nx, ny = glyph.x + dx, glyph.y + dy

            if not self.in_bounds(nx, ny):
                continue

            # Skip impassable terrain
            if not self.is_traversable(nx, ny):
                continue

            results.append(PathGlyph(nx, ny))

        return results

    def render_ascii(
        self,
        path: Optional[List[PathGlyph]] = None,
        hearth: Optional[PathGlyph] = None,
        pythonia: Optional[PathGlyph] = None,
    ) -> str:

        path_set = set(path) if path else set()
        rows = []

        for y in range(self.height):
            line = []
            for x in range(self.width):
                glyph = PathGlyph(x, y)

                if hearth and glyph == hearth:
                    line.append("A")
                elif pythonia and glyph == pythonia:
                    line.append("P")
                elif glyph in path_set:
                    line.append("*")
                else:
                    terrain = self.terrain_at(glyph)
                    line.append(TERRAIN_SYMBOLS.get(terrain, "?"))

            rows.append("".join(line))

        return "\n".join(rows)

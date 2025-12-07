"""
grid_forge.py
--------------------------------------------
The Map-Anvil class presented here is responsible for "forging" the world grid that Aris the Explorer will traverse.
It loads terrain information from an external JSON file, validates terrain descriptors, resolves terrain codes,
and exposes neighbour lookup utilities.

This module is intentionally designed with high modularity and readability.
"""
import json
from typing import List, Dict, Optional, Tuple
from pathlib import Path

from runes import pathGlyph
from terrain_legends import (
    TERRAIN_CATALOGUE,
    TERRAIN_SYMBOLS,
    is_valid_terrain,
    minimum_traversable_cost,
)

# ---------------------------------------------------------
# SHORT CODES FOR CONVENIENT JSON MAPS
# ---------------------------------------------------------

TERRAIN_SHORTCODES: Dict[str, str] = {
    "WG": "whispering_grassland",
    "FR": "forest_of_reflections",
    "DD": "desert_of_doom",
    "FL": "frozen_lake",
    "MM": "muddy_marsh",
    "SM": "shadow_mountain",
    "WA": "wall_of_ancients",
}

# Reverse lookup: long -> short (for optional future use)

REVERSE_SHORTCODES: Dict[str, str] = {
    long: short for short, long in TERRAIN_SHORTCODES.items()
}

# ---------------------------------------------------------
# GRID FORGING CLASS
# ---------------------------------------------------------

class Map_Anvil:
    """
    The Map_Anvil accepts a JSON map file and forges a fully validated, navigable grid.
    Each cell contains a descriptive terrain string, ensuring consistency throughout
    the system.
    
    Attributes:
        width (int): number of columns
        height (int): number of rows
        grid (List[List[str]]): 2D list of terrain identifiers    
    """
def __init__(self, json_path: str):
    """
    Load and validate a world grid from a JSON file.
    
    Parameters:
        json_path (str): path to the JSON file (relative or absolute)
    
    Raises:
        ValueError: if terrain descriptors are invalid or grid is malformed
    """
    self.json_path = Path(json_path)
    
    if not self.json_path.exists():
        raise FileNotFoundError(f"Map file not found: {self.json_path}")
    
    # Load the JSON s a Python list of list.
    raw_grid = self._load_json()
    
    # Normalise terrain names (convert short codes to full names).
    self.grid = self._normalise_grid(raw_grid)
    
    # Dimensions.
    self.height = len (self.grid)
    self.width = len(self.grid[0])
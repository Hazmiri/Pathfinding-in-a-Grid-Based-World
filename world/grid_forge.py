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

from runes.runes import PathGlyph
from world.terrain_legends import (
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
    
# -----------------------------------------------------------------------
# JSON LOADING
# -----------------------------------------------------------------------

def _load_json(self) -> List[List[str]]:
    """
    Load the JSON file into memory.
    """
    with open(self.json_path, "r", encoding = "utf-8") as file:
        return json.load(file)
    
# -----------------------------------------------------------------------
# STRUCTURE VALIDATION
# -----------------------------------------------------------------------

def _validate_structure(self, raw_grid: List[List[str]]) -> None:
    """
    Ensure the JSON map is a proper rextangular grid.
    
    Raises: 
        ValueError: if the grid is malformed.
    """
    if not isinstance(raw_grid, list) or len(raw_grid) == 0:
        raise ValueError("Map must be a non-empty 2D list.")
    
    expected_row_length = len(raw_grid[0])
    
    for row in raw_grid:
        if not isinstance(row, list):
            raise ValueError("Row in the map is not a lsit.")
        if len(row) != expected_row_length:
            raise ValueError("Map rows must all be the same length.")

# -----------------------------------------------------------------------
# NORMALISATION: short-code --> long terrain name
# -----------------------------------------------------------------------

def _normalise_grid(self, raw_grid: List[List[str]]) -> List[List[str]]:
    """
    Convert terrain short codes to full terrain names.
    Any value that is not a valid full name will be checked against the 
    short codes.
    
    Raises:
        ValueError: if a terrain name or code is unknown.
    """

    normalised: List[List[str]] = []
    
    for row in raw_grid:
        new_row = []
        for cell in row:
            
            # If already a long name and valid --> accept.
            
            if is_valid_terrain(cell):
                new_row.append(cell)
                continue
            
            # Try short-code lookup.
            
            if cell in TERRAIN_SHORTCODES:
                new_row.append(TERRAIN_SHORTCODES[cell])
                continue
            
            raise ValueError(f"Unknown terrain identifier: {cell}")
        
        normalised.append(new_row)
    
    return normalised

# ----------------------------------------------------------------------
# PUBLIC METHODS
# ----------------------------------------------------------------------

def terrain_at(self, glyph: PathGlyph) -> str:
    
    """
    Return the terrain type at the given glyph.
    """
    return self.grid[glyph.y][glyph.x]

def cost_at(self, glyph: PathGlyph) -> float:
    
    """
    Return the movement cost associated with the terrain at the given 
    glyph.
    """
    terrain = self.terrain_at(glyph)
    return TERRAIN_CATALOGUE[terrain]

def neighbours(self, glyph: PathGlyph) -> List [PathGlyph]:
    
    """
    Return all eight neighbouring cells (if within bounds).
    """
    offsets = [
        (-1, 0), (1, 0), (0 ,-1), (0, 1),   # cardinal
        (-1, -1), (1, -1), (-1, 1), (1, 1), # diagonals
    ]
    
    result = []
    
    for dx, dy in offsets:
        candidate = PathGlyph(glyph.x + dx, glyph.y + dy)
        
        if self.in_bounds(candidate):
            result.append(candidate)
            
    return result

# -----------------------------------------------------------------------
# ASCII RENDERING (FOR TESTING)
# -----------------------------------------------------------------------

def render_ascii(
    self, 
    path: Optional [List[PathGlyph]] = None,
    hearth: Optional [PathGlyph] = None,
    pythonia: Optional [PathGlyph] = None,
) -> str:
    
    """
    Produce a human-readable ASCII rendering of the map.
    Aris' s Hearth (start) = A
    Pythonia (goal) = P
    Path = *
    
    Useful for quick debugging and demonstration.
    """
    path_set = set (path) if path else set ()
    lines= []
    
    for y in range (self.height):
        row_symbols = []
        for x in range(self.width):
            glyph = PathGlyph (x, y)
            
            if hearth and glyph == hearth:
                row_symbols.append ("A")  # Aris
            elif pythonia and glyph == pythonia:
                row_symbols.append ("P")
            elif glyph in path_set:
                row_symbols.append("*")
            else:
                terrain = self.terrain_at(glyph)
                row_symbols.append(TERRAIN_SYMBOLS.get(terrain, "?"))
                
        lines.append ("".join(row_symbols))
        
    return "\n".join(lines)
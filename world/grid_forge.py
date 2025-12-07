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


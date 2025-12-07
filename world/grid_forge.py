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

"""
runes.py
--------

This module defines the PathGlyph, a lightweight immutable coordinate
token representing a single cell within the world grid.

The name 'PathGlyph' evokes the idea of carved symbols on ancient maps,
aliging with the creatives theme of Aris's world.

PathGlyphs serve as stable references for:

    - Cost lookups
    - Neighbour discovery
    - A* path reconstruction
    - Tracking visited and frontier positions
"""

from dataclasses import dataclass
from typing import Tuple

@dataclass (frozen = True, eq = True)
class PathGlyph:
    
    """
    PathGlyph represents a single location within the grid.
    It is immutable (frozen = True), meaning it can safely be used as a
    key in dictionaries or stored inside sets, which is essential for
    A*.
    
    Attributes:
        x (int): horizontal coordinate (column index)
        y (int): vertical coordinate (row index)
    """
   
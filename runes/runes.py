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
    x: int
    y: int
    
    def __lt__(self, other: "PathGlyph") -> bool:
        """
        Required so heapq can compare PathGlyph objects when priorities tie.
        """
        return (self.x, self.y) < (other.x, other.y)

    
    def coords (self) -> Tuple [int, int]:
        """
        Return (x, y) as a coordinate tuple for convenience.
        """
        return (self.x, self.y)
    
    def _repr_(self) -> str:
        """
        Return a concise symbolic representation for debugging and
        logging.
        """
        return f"Glyph({self.x},{self.y})"
    
    def is_diagonal_to(self, other: "PathGlyph") -> bool:
        """
        Returns True if movement from this glyph to 'other' is diagonal.
        """
        return abs(self.x - other.x) == 1 and abs(self.y - other.y) == 1

    
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
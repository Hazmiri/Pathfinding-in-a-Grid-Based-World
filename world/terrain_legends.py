"""
terrain_legends.py
------------------
Defines terrain names, costs, symbols, and helper utilities.
"""

# Terrain catalogue: long_name -> movement cost
TERRAIN_CATALOGUE = {
    "whispering_grassland": 1.0,
    "forest_of_reflections": 2.0,
    "desert_of_doom": 4.0,
    "frozen_lake": 3.0,
    "muddy_marsh": 2.5,
    "shadow_mountain": 5.0,
    "wall_of_ancients": float("inf"),  # impassable
}

# ASCII symbols
TERRAIN_SYMBOLS = {
    "whispering_grassland": ".",
    "forest_of_reflections": "F",
    "desert_of_doom": "D",
    "frozen_lake": "I",
    "muddy_marsh": "M",
    "shadow_mountain": "S",
    "wall_of_ancients": "#",
}

# ---------------------------------------------------------------
# VALIDATION HELPERS
# ---------------------------------------------------------------

def is_valid_terrain(name: str) -> bool:
    return name in TERRAIN_CATALOGUE

def minimum_traversable_cost() -> float:
    """Return the lowest cost among walkable terrains (non-WA)."""
    return min(
        cost for name, cost in TERRAIN_CATALOGUE.items()
        if cost < float("inf")
    )

""" 
terrain_legends.py
------------------

This module defines the legendary terrains of Aris's world.
Each terrain has:
    - A peatic name
    - A movement cost (energy required)
    - A passability flag
    - A map symbol (for ASCII rendering)
    
"""
from math import inf
from typing import Dict

# -----------------------------------------------------------
# TERRAIN CATALAGUE (CREATIVE + RICH)
#
# I can adjust names or cost depends if my imagination grows will I am writing the code.
# 
# All keys are lowwercase for JSON compatibility.
# -----------------------------------------------------------

TERRAIN_CATALOGUE: Dict[str, float] = {
    "whispering_grassland": 1.0,  # easy movement
    "forest_of_reflections": 3.0, # tree density
    "desert_of_doom": 4.5,        # dry and draining
    "frozen_lake": 6.0,           # slipperry and slow
    "muddy_marsh": 2.7,           # sticky ground
    "shadow_mountain": 10.0,      # extremely hard to cross
    "wall_of_ancients": inf,      # impassable

}

# ----------------------------------------------------------
# SYMBOL MAP FOR ASCII VISUALISATION 
#-----------------------------------------------------------

TERRAIN_SYMBOLS: Dict[str, str] = {
    "whispering_grassland": ".",
    "forest_of_reflections": "F",
    "desert_of_doom": "D",
    "frozen_lake": "~",
    "muddy_marsh": "M",
    "shadow_mountain": "^",
    "wall_of_ancients": "#",
}

# ---------------------------------------------------------
# TERRAIN VALIDATION
# ---------------------------------------------------------

def is_valid_terrain (name: str) -> bool:
    
    """
    Return True if given terrain name exists in the catalogue above.
    """
    return name in TERRAIN_CATALOGUE

# ---------------------------------------------------------
# MINIMUM MOVEMENT COST (for heuristic scaling)
# ---------------------------------------------------------

def minimum_traversable_cost() -> float:
    """
    Return the lowest movement cost in the terrain list, excluding impassable terrain.
    """
    return min (cost for cost in TERRAIN_CATALOGUE.values() if cost != inf)
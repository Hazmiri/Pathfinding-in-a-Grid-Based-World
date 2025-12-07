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
    "whispering_grassland": 1.0, # easy movement
    "forest_of_reflection": 1.8, # tree density
    "desert_of_doom": 4.5,       # dry and draining
    "frozen_lake": 6.0,          # slipperry and slow
    "muddy_marsh": 2.7,          # sticky ground
    "shadow_mountain": 10.0,     # extremely hard to cross
    "wall_of_ancients": inf,      # impassable
}
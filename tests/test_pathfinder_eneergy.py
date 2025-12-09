# tests/test_pathfinder_energy.py
"""
Tests for Saladin_Pathfinder in 'lowest_energy' mode.
Ensures cost-aware paths outperform step-only paths.
"""

from runes.runes import PathGlyph
from world.grid_forge import Map_Anvil
from aris.saladin_pathfinder import Saladin_Pathfinder
from world.terrain_legends import TERRAIN_CATALOGUE


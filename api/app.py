# api/app.py

from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import os
import tempfile

from world.grid_forge import Map_Anvil
from runes.runes import PathGlyph
from aris.saladin_pathfinder import Saladin_Pathfinder


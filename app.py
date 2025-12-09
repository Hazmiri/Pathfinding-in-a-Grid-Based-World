# app.py

from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import os
import uuid
import tempfile

from world.grid_forge import Map_Anvil
from runes.runes import PathGlyph
from aris.saladin_pathfinder import Saladin_Pathfinder

app = Flask(__name__)

# Store maps temporarily in system temp dir
UPLOAD_DIR = tempfile.gettempdir()


# ============================================================
# Utility: Save file safely
# ============================================================
def save_uploaded_file(upload):
    filename = secure_filename(upload.filename)
    unique_id = str(uuid.uuid4())
    temp_path = os.path.join(UPLOAD_DIR, unique_id + "_" + filename)
    upload.save(temp_path)
    return temp_path


# ============================================================
# 1. UPLOAD MAP
# ============================================================
@app.route("/upload_map", methods=["POST"])
def upload_map():
    if "map" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["map"]
    if file.filename == "":
        return jsonify({"error": "Empty filename"}), 400

    try:
        stored_path = save_uploaded_file(file)
        return jsonify({"file_id": stored_path}), 200

    except Exception as e:
        return jsonify({"error": f"Failed to store file: {e}"}), 500


# ============================================================
# 2. VALIDATE MAP
# ============================================================
@app.route("/validate_map", methods=["POST"])
def validate_map():
    data = request.get_json()
    if "file_id" not in data:
        return jsonify({"error": "file_id missing"}), 400

    try:
        Map_Anvil(data["file_id"])  # will raise error automatically if invalid
        return jsonify({"valid": True}), 200

    except Exception as e:
        return jsonify({"valid": False, "error": str(e)}), 400


# ============================================================
# 3. PATHFIND
# ============================================================
@app.route("/pathfind", methods=["POST"])
def pathfind():
    data = request.get_json()

    required = ["file_id", "start", "goal", "mode"]
    if not all(k in data for k in required):
        return jsonify({"error": "Missing required fields"}), 400

    file_id = data["file_id"]

    try:
        world = Map_Anvil(file_id)
    except Exception as e:
        return jsonify({"error": f"Could not load map: {e}"}), 400

    start = PathGlyph(data["start"]["x"], data["start"]["y"])
    goal = PathGlyph(data["goal"]["x"], data["goal"]["y"])

    pf = Saladin_Pathfinder(world, mode=data["mode"])

    try:
        path = pf.chart_course(start, goal)
    except Exception as e:
        return jsonify({"error": f"Pathfinding failed: {e}"}), 500

    if path is None:
        return jsonify({"path": None, "cost": None}), 200

    serialized = [{"x": p.x, "y": p.y} for p in path]

    # Compute cost cleanly
    total_cost = sum(world.cost_at(path[i + 1]) for i in range(len(path) - 1))
    total_cost = float(round(total_cost, 3))

    return jsonify({
        "path": serialized,
        "cost": total_cost,
        "ascii": world.render_ascii(path=path, hearth=start, pythonia=goal)
    }), 200


# ============================================================
# 4. ASCII PREVIEW WITHOUT PATHFINDING
# ============================================================
@app.route("/ascii_preview", methods=["POST"])
def ascii_preview():
    data = request.get_json()

    if "file_id" not in data:
        return jsonify({"error": "file_id missing"}), 400

    try:
        world = Map_Anvil(data["file_id"])
        ascii_map = world.render_ascii()
        return jsonify({"ascii": ascii_map}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 400


# ============================================================
# FLASK APP STARTUP
# ============================================================
if __name__ == "__main__":
    app.run(debug=True)

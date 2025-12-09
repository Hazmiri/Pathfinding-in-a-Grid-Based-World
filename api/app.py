# api/app.py

from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import os
import tempfile

from world.grid_forge import Map_Anvil
from runes.runes import PathGlyph
from aris.saladin_pathfinder import Saladin_Pathfinder

app = Flask(__name__)
UPLOAD_FOLDER = tempfile.gettempdir()
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/upload_map", methods=["POST"])
def upload_map():
    """
    Receives a JSON file upload and stores it temporarily.
    Returns a file_id to use for pathfinding.
    """
    if "map" not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files["map"]

    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    filename = secure_filename(file.filename)
    temp_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    file.save(temp_path)

    return jsonify({"file_id": temp_path}), 200

@app.route("/pathfind", methods=["POST"])
def pathfind():
    """
    Compute a path using A* for a previously uploaded map file.
    """
    data = request.get_json()

    required = ["file_id", "start", "goal", "mode"]
    if not all(k in data for k in required):
        return jsonify({"error": "Missing required keys"}), 400

    map_path = data["file_id"]
    start = data["start"]
    goal = data["goal"]
    mode = data["mode"]

    world = Map_Anvil(map_path)
    pf = Saladin_Pathfinder(world, mode=mode)

    start_g = PathGlyph(start["x"], start["y"])
    goal_g = PathGlyph(goal["x"], goal["y"])

    path = pf.chart_course(start_g, goal_g)

    if path is None:
        return jsonify({"path": None, "cost": None}), 200

    serialized_path = [{"x": p.x, "y": p.y} for p in path]

    # Calculate final cost
    cost = 0
    for i in range(len(path) - 1):
        cost += pf._movement_cost(path[i], path[i+1])

    return jsonify({
        "path": serialized_path,
        "cost": round(cost, 3),
        "ascii": world.render_ascii(path=path, hearth=start_g, pythonia=goal_g)
    }), 200

if __name__ == "__main__":
    app.run(debug=True)

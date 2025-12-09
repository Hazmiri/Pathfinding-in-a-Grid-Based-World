from flask import Flask, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
import os
import tempfile

from world.grid_forge import Map_Anvil
from runes.runes import PathGlyph
from aris.saladin_pathfinder import Saladin_Pathfinder

app = Flask(__name__, static_folder="ui", static_url_path="")

UPLOAD_FOLDER = tempfile.gettempdir()
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Rout that allowed the broser to load files

@app.route("/ui/<path:filename>")
def ui_files(filename):
    return send_from_directory("ui", filename)



# 🔹 Serve the UI
@app.route("/")
def index():
    return app.send_static_file("index.html")


# 🔹 Upload map file
@app.route("/upload_map", methods=["POST"])
def upload_map():
    if "map" not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files["map"]

    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    filename = secure_filename(file.filename)
    temp_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    file.save(temp_path)

    return jsonify({"file_id": temp_path}), 200


# 🔹 Run Saladin Pathfinder
@app.route("/pathfind", methods=["POST"])
def pathfind():
    data = request.get_json()

    required = ["file_id", "start", "goal", "mode"]
    if not all(k in data for k in required):
        return jsonify({"error": "Missing required keys"}), 400

    map_path = data["file_id"]
    start = PathGlyph(data["start"]["x"], data["start"]["y"])
    goal = PathGlyph(data["goal"]["x"], data["goal"]["y"])
    mode = data["mode"]

    world = Map_Anvil(map_path)
    pf = Saladin_Pathfinder(world, mode=mode)

    path = pf.chart_course(start, goal)

    if path is None:
        return jsonify({"path": None, "cost": None, "ascii": None}), 200

    serialized_path = [{"x": p.x, "y": p.y} for p in path]

    # compute cost
    cost = 0
    for i in range(len(path) - 1):
        cost += pf._movement_cost(path[i], path[i+1])

    return jsonify({
        "path": serialized_path,
        "cost": round(cost, 3),
        "ascii": world.render_ascii(path=path, hearth=start, pythonia=goal)
    }), 200


if __name__ == "__main__":
    app.run(debug=True)

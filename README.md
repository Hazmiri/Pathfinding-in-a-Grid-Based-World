Pathfinding in a Grid-Based World
A Flask-powered A pathfinding visualiser with fantasy-themed terrain*

This project implements an interactive pathfinding system for a grid-based fantasy world using A* with multiple cost modes. The user can upload maps, choose start/goal points, run the algorithm, and view both ASCII and colour-based visualisations in a web UI.

⭐ Features
🧭 Pathfinding Engine

A* algorithm implemented from scratch

Two movement modes:

Fewest Steps → each move costs 1

Lowest Energy → terrain-based costs + diagonal penalties

Fully tested (13/13 tests passed)

🌍 Fantasy Terrain System

Whispering Grasslands

Forest of Reflections

Desert of Doom

Frozen Lake

Muddy Marsh

Shadow Mountain

Wall of Ancients (impassable)

Terrain costs are defined in terrain_legends.py.

🖥️ Web Application (Flask + JavaScript)

Upload custom maps (JSON)

Auto-loads a default world on startup

Displays ASCII map from the server

Converts ASCII to a coloured visual grid

Highlights:

Start (A)

Goal (P)

Path (*)

📦 Project Structure

Pathfinding-in-a-Grid-Based-World/
│
├── app.py                  # Flask backend
├── main.py                 # Standalone CLI demo (optional)
├── default_world.json      # Preloaded demo map
│
├── aris/
│   └── saladin_pathfinder.py
│
├── world/
│   ├── grid_forge.py
│   └── terrain_legends.py
│
├── runes/
│   └── runes.py           # PathGlyph class
│
├── ui/
│   ├── index.html
│   ├── app.js
│   ├── styles.css
│   └── assets/
│       └── aris_photo.png
│
└── tests/
    └── (13 unit tests)

🚀 How to Run the Application

pip install flask

python app.py

http://127.0.0.1:5000

🧪 Running the Unit Tests

Tests validate:

world loading

terrain parsing

invalid maps

A* behaviour

edge cases (no path, diagonal moves, small worlds)

Run: pytest -v

📘 Algorithm Summary A* Search

Frontier stored as a priority queue (heapq)

g_score stores cost so far

f_score = g_score + heuristic

Reconstructs path using backtracking

Heuristics

Fewest_steps → Chebyshev distance

Lowest_energy → Chebyshev × minimum terrain cost

Movement Validation

No movement onto walls

8-directional movement allowed

Diagonal penalty applied in energy mode

📄 Map File Specification (JSON)

A map is a grid of terrain shortcodes: 

[
  ["WG", "WG", "WG"],
  ["WG", "WA", "WG"],
  ["DD", "DD", "WG"]
]

Uploaded maps are fully validated.

✨ Credits

Developed by: God
Pathfinder Engine: Saladin
World Design: Whispering Lands of Aris
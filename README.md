Pathfinding in a Grid-Based World

This project implements an advanced pathfinding system based on the A* algorithm within a fully custom grid-based fantasy world. 
The environment contains varied terrain types, each with distinct movement costs, alongside impassable regions that shape the search space. 
The project features a complete Python implementation, automated testing suite, and a fully interactive web interface for visualisation.
Designed with clarity, correctness and academic rigour in mind, the system demonstrates how classical pathfinding algorithms can be adapted to handle weighted topologies and diagonal movement while maintaining optimality.
The work forms part of a broader investigation into algorithm selection, efficiency, and ethical considerations in autonomous navigation.

Features
🧭 A* Pathfinding Engine

Supports 8-direction (Moore neighbourhood) movement

Two optimisation modes:

Fewest Steps (topological shortest path)

Lowest Energy (terrain-weighted optimal path)

Implements admissible heuristics (Chebyshev distance)

Handles extreme cases robustly (no path, start = goal, malformed map)

🌍 Rich Grid-Based World Model

Terrain types include grass, forest, desert, marsh, mountain, ice, and walls

Each terrain has its own energy cost

Walls are strictly impassable

Map validation ensures rectangularity and correct terrain identifiers

🖥 Web Interface

Built using Flask, HTML/CSS, and JavaScript

Live ASCII output

Colour-coded grid visualisation

File upload for custom maps

Default map auto-load on startup

🔧 Testing and Reliability

Full unit test suite using pytest

Tests include:

Edge cases (start = goal, no path)

Weighted vs unweighted mode correctness

Diagonal movement rules

Terrain cost consistency

Pathfinding-in-a-Grid-Based-World/
│
├── app.py                     # Flask backend API and UI routing
├── main.py                    # Simple CLI runner (optional)
├── default_world.json         # Large example world loaded automatically
│
├── world/
│   ├── grid_forge.py          # World model, terrain costs, neighbour logic
│
├── runes/
│   ├── runes.py               # PathGlyph class and utilities
│
├── aris/
│   ├── saladin_pathfinder.py  # Core A* implementation
│
├── tests/
│   ├── test_steps.py
│   ├── test_energy.py
│   ├── test_edge_cases.py
│   ├── test_world_loading.py
│
└── ui/
    ├── index.html             # User interface
    ├── styles.css             # Styling and terrain colours
    ├── app.js                 # Front-end logic + visualisation
    └── assets/
        └── aris_photo.png     # Aris, the exploration robot

Installation
1. Clone the repository
git clone https://github.com/your-repo/pathfinder.git
cd pathfinder

2. Install dependencies
pip install -r requirements.txt

3. Run the web interface
python app.py


Then open:

http://127.0.0.1:5000

Usage
From the Web Interface

A default map is auto-loaded

Upload a custom JSON map (optional)

Enter start and goal coordinates

Select pathfinding mode

View ASCII output and a fully coloured grid visualisation

From Command Line (optional)
python main.py

Map Format

Maps must be rectangular and structured as:

{
  "terrain_map": [
    ["grass", "forest", "forest"],
    ["desert", "wall_of_ancients", "grass"],
    ["grass", "marsh", "ice"]
  ]
}


Invalid maps will raise clear errors explaining the issue.

Testing

Run all tests:

pytest


All core systems (loading, neighbour logic, cost evaluation, and A*) are fully covered.

Academic Context

This project provides evidence for:

Algorithmic analysis and justification

Design planning (pseudocode & flowcharts)

Implementation quality and modularity

Efficiency evaluation using Big-O reasoning

Ethical considerations in autonomous systems

The project is designed to align with MMU marking criteria for algorithmic coursework.

Acknowledgements

This project draws upon established principles in heuristic search and autonomous navigation, including:

A* search algorithm (Hart, Nilsson & Raphael, 1968)

Heuristic optimisation foundations (Pearl, 1984)

Modern AI practice (Russell & Norvig, 2021)

# Pathfinding Visualizer (DSA Project)

A desktop application that visualizes common graph-search and shortest-path algorithms on a grid.

## Features
- Interactive grid with start and destination cells
- Draw walls with left-click/drag and erase them with right-click/drag
- BFS, DFS, Dijkstra's algorithm, and A* search
- Animated exploration and final path highlighting
- Visited-node count and elapsed runtime display
- Reset and clear controls

## Requirements
- Python 3.9+
- Pygame 2.5+

## Setup (Windows)
1. Install Python from https://www.python.org/downloads/
2. Open this folder in VS Code.
3. Open Terminal > New Terminal.
4. Install dependencies:
   ```bash
   python -m pip install -r requirements.txt
   ```
5. Run:
   ```bash
   python main.py
   ```

If `python` is not recognized, try `py -m pip install -r requirements.txt` and `py main.py`.

## Controls
- Left-click / drag: draw walls
- Right-click / drag: erase walls
- `S`: choose a new start cell, then click a grid cell
- `E`: choose a new destination, then click a grid cell
- `1`: BFS
- `2`: DFS
- `3`: Dijkstra
- `4`: A*
- `Space`: run selected algorithm
- `C`: clear walls and search results (the on-screen C button clears search results and walls)
- `R`: reset the whole grid
- `Esc`: quit

## Algorithms
- **BFS** uses a queue and finds a shortest path when all edges have equal cost.
- **DFS** uses a stack. It finds a route if one exists, but does not guarantee the shortest route.
- **Dijkstra** uses a min-heap priority queue to find a minimum-cost path for non-negative edge weights.
- **A\*** uses `f(n) = g(n) + h(n)`, with Manhattan distance as the heuristic for four-direction movement.

## Complexity
For a graph with `V` cells and `E` neighbor connections:
- BFS: `O(V + E)` time and `O(V)` space.
- DFS: `O(V + E)` time and `O(V)` space.
- Dijkstra: typically `O((V + E) log V)` with a binary heap.
- A*: depends on the heuristic and explored region; worst-case performance can be exponential for general search spaces.

## Project limitations
- The grid uses four-direction movement and equal move costs.
- The displayed time includes the animation's elapsed wall-clock time, so it is not a pure benchmark of algorithm computation. For a fair benchmark, run algorithms without animation and measure only the search function.
- The app is a local desktop demo and does not need a database or web server.

## Suggested future improvements
- Add diagonal movement and weighted terrain
- Add side-by-side algorithm comparison
- Add a separate non-animated benchmark mode
- Add maze generation
- Add unit tests for each algorithm

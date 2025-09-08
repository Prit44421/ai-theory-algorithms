# AI Theory - Algorithms and Problem Solving

This repository contains implementations of various artificial intelligence algorithms and classic AI problems, organized into different categories.

## Project Structure

### Problems

- **8Puzzle.py** - 8-puzzle sliding tile problem implementation
- **nQueen.py** - N-Queens problem solver
- **sat.py** - Boolean satisfiability (SAT) problem
- **tsp.py** - Traveling Salesman Problem (TSP)

### Blind Search Algorithms

- **Configuration/** - Configuration space search implementations
  - `bfs.py` - Breadth-First Search
  - `dfs.py` - Depth-First Search
  - `dfid.py` - Depth-First Iterative Deepening
- **planning/** - Planning domain search implementations
  - `bfs.py` - Breadth-First Search for planning
  - `dfs.py` - Depth-First Search for planning
  - `dfid.py` - Depth-First Iterative Deepening for planning

### Heuristic Search

- **bfs.py** - Best-First Search implementation

### Local Search Algorithms

- **beamSearch.py** - Beam Search algorithm
- **hillClimbing.py** - Hill Climbing algorithm
- **iteratedHillClimbing.py** - Iterated Hill Climbing
- **tabuSearch.py** - Tabu Search algorithm

### Extra Problems and Move Generators

- **Classic Problems:**

  - `mapColoring.py` - Map coloring problem
  - `missionariesCannibals.py` - Missionaries and Cannibals problem
  - `waterJug.py` - Water jug problem
  - `wolfGoatCabbage.py` - Wolf, Goat, and Cabbage problem
- **movegen/** - Move generator implementations for various problems

  - `eightpuzzle_move.py` - 8-puzzle move generation
  - `mapcolor_move.py` - Map coloring move generation
  - `missionariescannibals_move.py` - Missionaries and Cannibals moves
  - `nqueen_move.py` - N-Queens move generation
  - `sat_move.py` - SAT problem move generation
  - `tsp_move.py` - TSP move generation
  - `waterjug_move.py` - Water jug move generation
  - `wolfgoatcabbage_move.py` - Wolf, Goat, Cabbage move generation
  - `sat_example_usage.py` - Example usage of SAT solver

## Getting Started

1. Clone this repository
2. Ensure you have Python 3.x installed
3. Run any of the problem files directly:
   ```bash
   python Problems/nQueen.py
   python Problems/8Puzzle.py
   ```

## Algorithms Implemented

- **Search Algorithms:** BFS, DFS, DFID, Best-First Search
- **Local Search:** Hill Climbing, Beam Search, Tabu Search
- **Problem Solving:** Various classic AI problems with complete implementations

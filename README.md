# Pac-Man AI

AI agents for the classic Pac-Man game, built on the UC Berkeley Pac-Man AI framework.

## Overview

This project implements search algorithms and heuristic agents for Pac-Man, including:

- **A\* Search** — pathfinding for single-goal, multi-corner, and food-collection problems
- **Minimax Agent with Alpha-Beta Pruning (Q2)** — adversarial search against ghosts, guided by a handcrafted evaluation function

## Project Structure

```
├── pacman.py              # Game engine
├── game.py                # Game logic
├── agents/                # AI agents
│   ├── searchAgents.py    # A* search agent
│   ├── q2Agent.py         # Minimax + alpha-beta agent
│   └── ...
├── problems/              # Search problem definitions
│   ├── q1a_problem.py     # Position reach
│   ├── q1b_problem.py     # Corners problem
│   └── q1c_problem.py     # Food collection
├── solvers/               # Solver implementations
│   ├── q1a_solver.py
│   ├── q1b_solver.py
│   └── q1c_solver.py
└── evaluator.py           # Benchmarking tool
```

## Running

```bash
# Run with search agent
python pacman.py -l <layout> -p SearchAgent -a fn=q1a_solver,prob=q1a_problem

# Run with the minimax agent (Q2)
python pacman.py -l <layout> -p Q2_Agent

# Run benchmarks
python evaluator.py
```

## License

This project is built on the UC Berkeley Pac-Man AI framework. See [LICENSE](LICENSE) for details.
Original framework: http://ai.berkeley.edu

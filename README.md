*This project has been created as part of the 42 curriculum by marcebar, fdos-rei*

# A-Maze-ing

## Description

A-Maze-ing is a maze generator written in Python. It reads a configuration
file, generates a random (and reproducible) maze, writes it to a file using a
hexadecimal wall representation, and shows it in the terminal with an
interactive menu.

**Goals**

- Generate valid mazes: entry and exit inside the grid, closed borders,
  coherent walls between neighbouring cells, no isolated cells and no open
  area larger than 2 cells wide (never a 3x3 open block).
- Support two modes: a *perfect* maze (exactly one path between any two cells)
  and a *non-perfect* maze with loops, playable as a Pac-Man-like board.
- Draw a visible "42" made of fully closed cells in the middle of the maze.
- Keep the generator reusable: one class, in a standalone module, installable
  with `pip`(standard `pyproject.toml`, built with `python -m build`; no
  third-party dependencies, so no extra tooling is required).

**Overview**

| Part | File | What it does |
|---|---|---|
| Entry point | `a_maze_ing.py` | Reads the config, builds the maze, starts the display |
| Generator | `generator.py` | `Mazegenerator` class: generation, "42" pattern, braiding, shortest path |
| Display | `display.py` | Terminal rendering (ANSI colours) and interactive menu |
| Output | `parsing.py` | Writes the maze to the output file |


## Instructions

### Requirements

- Python 3.10 or later
- `flake8` and `mypy` (only for `make lint`)

### Installation and execution

```bash
make install     # install dependencies
make run         # python3 a_maze_ing.py config.txt
make debug       # run with pdb
make clean       # remove __pycache__, .mypy_cache, ...
make lint        # flake8 + mypy
```

Or directly:

```bash
python3 a_maze_ing.py config.txt
```

The program never crashes on bad input: an invalid or missing configuration,
an unknown file or impossible parameters print a clear message
(`Error: ...`) and exit with status 1.

### Configuration file

One `KEY=VALUE` pair per line. 

| Key | Required | Description | Example |
|---|---|---|---|
| `WIDTH` | yes | Number of columns (3 to 100) | `WIDTH=20` |
| `HEIGHT` | yes | Number of rows (3 to 100) | `HEIGHT=15` |
| `ENTRY` | yes | Entry cell as `x,y`, starting at `0,0` (top-left) | `ENTRY=0,0` |
| `EXIT` | yes | Exit cell as `x,y`, different from the entry | `EXIT=19,14` |
| `OUTPUT_FILE` | yes | Name of the file the maze is written to | `OUTPUT_FILE=maze.txt` |
| `PERFECT` | yes | `True` = perfect maze, `False` = maze with loops | `PERFECT=True` |
| `SEED` | no | Integer >= 0. Same seed and same settings give the same maze. Without it, each run is different and the seed used is shown on screen | `SEED=42` |

Example (`config.txt`):

```
# Maze settings
WIDTH=20
HEIGHT=15
ENTRY=0,0
EXIT=19,14
OUTPUT_FILE=maze.txt
PERFECT=True
SEED=42
```

Validation: entry and exit must be inside the grid, must be different, and
must not be on a cell of the "42" pattern.

### Interactive menu

After the maze is drawn, the menu is shown under it:

| Option | Action |
|---|---|
| 1 | Generate a new maze (uses the next seeds: `SEED+1`, `SEED+2`, ...) |
| 2 | Show / hide the shortest path from entry to exit |
| 3 | Change the colour of the walls |
| 4 | Quit |

Colours: green = entry, blue = exit, yellow = shortest path, grey = the "42"
pattern. With `PERFECT=False`, option 2 also shows up to three alternative
routes (cyan, magenta, red), because the maze has loops. The seed of the maze
on screen is always displayed, so a maze you like can be reproduced by putting
its seed in the configuration file.

If the maze is too small to contain the "42" pattern (minimum 9x7), the
pattern is omitted and a warning is displayed in the terminal.

### Output file format

One hexadecimal digit per cell, one row per line. Each bit says whether the
wall on that side is **closed** (`1`) or open (`0`):

| Bit | Value | Side |
|---|---|---|
| 0 | 1 | North |
| 1 | 2 | East |
| 2 | 4 | South |
| 3 | 8 | West |

For example `3` (`0011`) means walls on the north and east sides, and `A`
(`1010`) means walls on the east and west sides. A cell of the "42" pattern is
fully closed, so it appears as `F`.

After the grid come an empty line and three more lines: the entry
coordinates, the exit coordinates and the shortest path from entry to exit
using the letters `N`, `E`, `S`, `W`. Every line ends with `\n`.

Example for `WIDTH=9`, `HEIGHT=7`, `ENTRY=0,0`, `EXIT=8,6`, `SEED=42`:

```
D53955553
BFC6BFFFA
AFFF857FA
853FAFFFA
A96FAFD52
AC3FAFFFA
C7C545556

0,0
8,6
EESENEEEEESSSSSS
```

## Maze generation

### Algorithm

The maze is generated with an iterative **Depth-First Search** (also called
*recursive backtracker*), using an explicit stack:

1. Start on a cell, mark it as visited and push it on the stack.
2. While the stack is not empty: pop a cell. If it has unvisited neighbours,
   push the cell back, pick one neighbour at random, remove the wall between
   them, mark the neighbour as visited and push it.
3. If it has no unvisited neighbour, simply continue (backtracking).

Every cell starts with all four walls (`15`). The cells of the "42" pattern
are marked as visited **before** the search, so the algorithm never opens
them and they stay fully closed.

All random choices come from a `random.Random(seed)` instance owned by the
generator, which makes the result reproducible.

### Why this algorithm

We chose the iterative depth-first search (recursive backtracker) because:

- **It is simple to implement and to explain**: carve a path to a random
  unvisited neighbour, and backtrack when there is none.
- **It always produces a perfect maze**: a cell is only connected when it is
  visited for the first time, so loops cannot appear and every cell is reached.
- **It is safe for big mazes**: it uses an explicit stack instead of recursion,
  so it does not hit Python's recursion limit (tested up to 100x100).
- **It is reproducible**: the only random choice is the neighbour, which uses
  a `random.Random(seed)` instance owned by the generator.
- **It is a good base for the non-perfect mode**: we generate a perfect maze
  first and then add loops on top of it (see below).

Its mazes have long winding corridors and few branches. We accepted this
trade-off in exchange for simplicity and reliability.

### Non-perfect mode (`PERFECT=False`)

The maze is first generated as a perfect one and then **braided**: every
dead-end (a cell with three walls) gets one of its walls removed, creating
loops. For each dead-end, the neighbours are shuffled (with the seed) and the
ones that are dead-ends too are tried first, so a single opening can fix two
dead-ends. An opening is rejected, and the wall put back, if it would create a
3x3 open block. Cells of the "42" are never opened.

Some dead-ends cannot be removed: the two cavities inside the digit "2" have
three sides made of "42" cells. After the dead-ends are treated, if the maze
has fewer than 2 independent loops, extra walls between connected cells are
opened (with the same 3x3 check) until the minimum is reached, as the subject
requires.

### Solving

The shortest path from the entry to the exit is found with a breadth-first
search (BFS), in both modes:

- The search starts at the entry and explores the maze in waves: first the
  neighbours at distance 1, then 2, and so on. Only neighbours separated by an
  open wall are visited, and "42" cells are never entered.
- Each cell stores the cell it was discovered from (its parent). A cell is
  discovered only once, so the first time the exit is reached is through a
  shortest path.
- The path is rebuilt by following the parents from the exit back to the
  entry and reversing the result. Each step becomes a letter (`N`, `E`, `S`,
  `W`), the format used in the output file.
- If the exit cannot be reached, a `ValueError` is raised.
- When two shortest paths exist (non-perfect mode), the result is still
  deterministic: neighbours are always visited in the same order
  (N, E, S, W).

BFS was chosen over DFS because DFS finds *a* path but not necessarily the
shortest one, which matters as soon as the maze has loops.

### The "42" pattern

The pattern is 7 cells wide and 5 cells high, centred in the maze, and needs a
grid of at least 9x7. In smaller mazes it is omitted and a message is printed.

## Reusable module

The generation logic lives in a single class, `Mazegenerator`, inside the
`mazegen` package. It does not read files, print or draw anything, so it can be
imported by other projects.

### Install

```bash
pip install mazegen-2026.1.0-py3-none-any.whl
```

To build it again from the sources:

```bash
python3 -m venv venv && source venv/bin/activate
pip install build
python3 -m build        # creates dist/mazegen-*.whl and dist/mazegen-*.tar.gz
```

### Basic example

```python
from generator import Mazegenerator   

maze = Mazegenerator(
    width=20,
    height=15,
    entry_xy=(0, 0),
    exit_xy=(19, 14),
    perfect=True,
    seed=42,
)
maze.generate()          # builds the maze and computes the shortest path

print(maze.grid)    # list of rows; maze.grid[row][col] is an int from 0 to 15
print("".join(maze.path))  # shortest path as a list of letters -> "EESEN....."
print(maze.seed)           # 42
```

### Parameters

| Parameter | Type | Description |
|---|---|---|
| `width`, `height` | `int` | Size in cells, between 2 and 100. |
| `entry_xy`, `exit_xy` | `tuple[int, int]` | Entry and exit as `(x, y)`. They must be inside the maze, different, and outside the "42" pattern. |
| `perfect` | `bool` | `True` (default): one path between any two cells. `False`: loops, no 3x3 open areas, few dead-ends. |
| `seed` | `int` | With the same seed and parameters, a new object generates the same maze. `None` (default) picks a random seed, available in `maze.seed`. |

Invalid parameters raise `ValueError` with a clear message.

### Accessing the result

| Attribute | Description |
|---|---|
| `maze.grid` | `list[list[int]]`, indexed `grid[row][col]`. Each value is 0 to 15 with the wall bits from the table above (N=1, E=2, S=4, W=8; A set bit means a closed wall). Neighbouring cells always agree on their shared wall. |
| `maze.path` | Shortest path as a list of `"N"`, `"E"`, `"S"`, `"W"`|
| `maze.entry_conv_yx`, `maze.exit_conv_yx` | Entry and exit as `(row, col)` |
| `maze.fortytwo_cells` | `(row, col)` of the cells that draw the "42" (empty if the maze is too small, which needs at least 9x7).|
| `maze.fortytwo_shown` | `True` if the "42" fits in the maze |
| `maze.seed` | the seed used to create the generator. |

Careful with the coordinates: Internally, coordinates are `(row, col)`; only the constructor takes `(x, y)`.

### Generating again

Calling `generate()` again on the same object returns a new maze (the random
generator keeps advancing), but `maze.seed` still shows the initial seed. To
reproduce a specific maze, create a new object with the same seed.

### License

Released under the license in `LICENSE.md`.

## Advanced features

- Reproducible mazes with the optional `SEED` key; the seed is displayed.
- Alternative routes drawn in other colours for mazes with loops.
- Warning in the terminal when the maze is too small for the "42".
- Wall colours that can be changed while the program is running.

## Project management

- **Roles:**
  - Filipa Gregorio: the `Mazegenerator` class (DFS generation, "42" pattern,
    braiding for `PERFECT=False`, BFS solver, seed handling), its tests, and the
    `mazegen` package (`pyproject.toml`, build, license).
  - Marcela Souza: config parser, `output file`, `terminal display` and
    interactions, `Makefile`
- **Planning:**
  - Planned: first a perfect maze generator, then the output file and display,
    then the non-perfect mode, then packaging and documentation.
    <!-- confirm with Marcela the original plan and dates -->
  - How it evolved: we split the work in layers around a shared grid format
    (one integer per cell, `(row, col)` internally). The non-perfect mode took
    longer than expected: the first braiding left some mazes with fewer than 2
    loops, so we added a step that opens extra walls. We also had to fix the
    "42" drawing condition and the reset of the generator state between runs.
- **What worked well:**
  - Agreeing early on the grid representation and the coordinate convention.
  - Writing tests with many sizes and seeds, which found real bugs (loops,
    dead-ends next to the "42", state not reset).
  - Developing on a separate branch and merging when the tests passed.
- **What could be improved:**
  - Settle the interface between the class and the main program earlier
    (what the class exposes, which exceptions it raises).
  - Run `flake8` and `mypy` from the start, instead of at the end.
  - Simplify the repeated neighbour code with a direction table
    (N, E, S, W with mask and offset).
- **Tools used:** Git and GitHub (shared repository, branches), Python 3.10+,
  `flake8`, `mypy`, `hatchling` and `build` (packaging), our own test script
  with `assert`, `maze_analyzer.py` (provided), Notion (task tracking),
  Claude (see Resources).

## Resources

**References**

- Python documentation: `random`, `venv` and bitwise operators.
- Python Packaging User Guide and Hatch documentation (`pyproject.toml`).
- [Maze generation algorithm (Wikipedia)](https://en.wikipedia.org/wiki/Maze_generation_algorithm)
- [Breadth-First Search (Codecademy)](https://www.codecademy.com/article/breadth-first-search-bfs-algorithm)
- [choosealicense.com](https://choosealicense.com/)
- [MIT License (Open Source Initiative)](https://opensource.org/license/mit)
- [Hatch documentation: Build](https://hatch.pypa.io/1.18/build/)
- [Python Packaging User Guide: Key projects](https://packaging.python.org/en/latest/key_projects/)
- [Writing your `pyproject.toml` (Python Packaging User Guide)](https://packaging.python.org/en/latest/guides/writing-pyproject-toml/)
- [GeeksforGeeks: Python](https://www.geeksforgeeks.org/python/)
- [Breadth-First Search (BFS) Algorithm (Codecademy)](https://www.codecademy.com/article/breadth-first-search-bfs-algorithm)
- [Coding Challenge: Maze Generator (Code Train, YouTube)](https://www.youtube.com/watch?v=HyK_Q5rrcr4): DFS maze generation tutorial in JavaScript / p5.js, which we re-implemented in Python.


**How AI was used**

We used Claude (Anthropic) as a tutor, never as the author of the code. We
used it to:

- understand concepts (graph theory, spanning trees, DFS and BFS, bitwise
  wall encoding, seeds, context managers, packaging, parser, visualization);
- get hints when debugging (for example, shared grid rows, unhashable types,
  recursion limits, `Python 3.9` vs `3.10` annotations);
- discuss the design of the tests (properties of the maze, failure cases,
  reproducibility) and how to structure and build the `mazegen` package;
- structure and co-write this README file

The algorithms and the code were written by us.
*This project has been created as part of the 42 curriculum by marcebar, fdosrei*

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
  with `pip`?? ou poetry ou uv???.

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

?????

### Non-perfect mode (`PERFECT=False`)

The maze is first generated as a perfect one and then **braided**: every
dead-end (a cell with three walls) gets one of its walls removed, creating
loops. For each dead-end, the neighbours are shuffled (with the seed) and the
ones that are dead-ends too are tried first, so a single opening can fix two
dead-ends. An opening is rejected, and the wall put back, if it would create a
3x3 open block. Cells of the "42" are never opened.

Some dead-ends cannot be removed: the two cavities inside the digit "2" have
three sides made of "42" cells.

### Solving

????

### The "42" pattern

The pattern is 7 cells wide and 5 cells high, centred in the maze, and needs a
grid of at least 9x7. In smaller mazes it is omitted and a message is printed.

## Reusable module

?????

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

maze = Mazegenerator(width=20, height=15,
                     entry_xy=(0, 0), exit_xy=(19, 14),
                     perfect=True, seed=42)
maze.generate()          # builds the maze and computes the shortest path

print(maze.grid[0])              # first row: [13, 5, 3, 9, ...]
print("".join(maze.path))        # "EESENEEESENE..."
print(maze.seed)                 # 42
```

### Parameters

| Parameter | Type | Description |
|---|---|---|
| `width`, `height` | `int` | Size in cells, from 3 to 100 |
| `entry_xy`, `exit_xy` | `tuple[int, int]` | Entry and exit as `(x, y)`, from `(0, 0)` |
| `perfect` | `bool` | `True` (default) for a perfect maze, `False` for one with loops |
| `seed` | `int` or `None` | Same seed and parameters give the same maze. `None` picks a random seed |

Invalid parameters raise `ValueError` with a clear message.

### Accessing the result

| Attribute | Description |
|---|---|
| `maze.grid` | `list[list[int]]`, indexed `grid[row][col]`. Each value is 0 to 15 with the wall bits from the table above (N=1, E=2, S=4, W=8; bit set = wall closed) |
| `maze.path` | Shortest path as a list of `"N"`, `"E"`, `"S"`, `"W"` (after `solve_maze_bfs()`) |
| `maze.entry_conv_yx`, `maze.exit_conv_yx` | Entry and exit as `(row, col)` |
| `maze.fortytwo_cells` | `(row, col)` of the cells that draw the "42" (empty if it did not fit) |
| `maze.fortytwo_shown` | `True` if the "42" fits in the maze |
| `maze.seed` | The seed actually used (useful when none was given) |

Careful with the coordinates: the constructor receives `(x, y)` like the
configuration file, while the grid and the attributes ending in `_yx` use
`(row, col)`.

## Advanced features

- Reproducible mazes with the optional `SEED` key; the seed is displayed.
- Alternative routes drawn in other colours for mazes with loops.
- Warning in the terminal when the maze is too small for the "42".
- Wall colours that can be changed while the program is running.

## Project management

- **Roles:** 
- **Planning:** 
- **What worked well:** 
- **What could be improved:** 
- **Tools used:** 

## Resources

**References**

??

**How AI was used**

??
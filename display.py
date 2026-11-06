#!/usr/bin/python3
from __future__ import annotations

from typing import Callable, Sequence, Union, Any

NORTH, EAST, SOUTH, WEST = 1, 2, 4, 8

MOVES = {NORTH: (-1, 0), EAST: (0, 1), SOUTH: (1, 0), WEST: (0, -1)}
LETTERS = {"N": NORTH, "E": EAST, "S": SOUTH, "W": WEST}

WALL_COLORS = [("branco", 47), ("vermelho", 41), ("magenta", 45),
               ("ciano", 46), ("preto", 40)]
COLORS = {
    "floor": None,
    "path": 103,
    "entry": 102,
    "exit": 104,
    "forty": 100,
}

Cell = tuple[int, int]
Step = Union[int, str]


def normalize_path(path: Sequence[Step]) -> list[int]:
    '''Accept the path as a list of bits (1, 2, 4, 8), a list of letters
    ("N", "E", "S", "W"), or a string ("NESW"). Always return a list
    of bits.'''
    result: list[int] = []
    for step in path:
        if isinstance(step, str):
            step = LETTERS[step.upper()]
        if step not in MOVES:
            raise ValueError(
                f"passo inválido: {step!r} (use 1=N, 2=E, 4=S, 8=W)")
        result.append(step)
    return result


def walk(grid: list[list[int]], entry: Cell, steps: list[int]) -> list[Cell]:
    '''Follow the path from the entry and return the list of visited cells
    (including the entry). Validate that no step crosses a wall or leaves
    the grid.'''
    h, w = len(grid), len(grid[0])
    r, c = entry
    cells = [entry]
    for i, step in enumerate(steps):
        if grid[r][c] & step:
            raise ValueError(f"passo {i}: há parede em {(r, c)}")
        dr, dc = MOVES[step]
        r, c = r + dr, c + dc
        if not (0 <= r < h and 0 <= c < w):
            raise ValueError(f"passo {i}: saiu da grelha em {(r, c)}")
        cells.append((r, c))
    return cells


def build_canvas(grid: list[list[int]], path_cells: list[Cell],
                 fortytwo: list[Cell], show_path: bool) -> list[list[str]]:
    '''Convert the grid into a (2h+1) x (2w+1) matrix. Cells are placed at
    positions (2r+1, 2c+1) and walls at the positions between them.'''
    h, w = len(grid), len(grid[0])
    canvas = [["wall"] * (2 * w + 1) for _ in range(2 * h + 1)]
    forty = set(fortytwo)

    for r in range(h):
        for c in range(w):
            v = grid[r][c]
            pr, pc = 2 * r + 1, 2 * c + 1
            canvas[pr][pc] = "forty" if (r, c) in forty else "floor"
            if not v & NORTH:
                canvas[pr - 1][pc] = "floor"
            if not v & SOUTH:
                canvas[pr + 1][pc] = "floor"
            if not v & WEST:
                canvas[pr][pc - 1] = "floor"
            if not v & EAST:
                canvas[pr][pc + 1] = "floor"

    if show_path:
        prev = path_cells[0]
        for cell in path_cells:
            canvas[2 * cell[0] + 1][2 * cell[1] + 1] = "path"
            canvas[prev[0] + cell[0] + 1][prev[1] + cell[1] + 1] = "path"
            prev = cell

    entry, exit_ = path_cells[0], path_cells[-1]
    canvas[2 * entry[0] + 1][2 * entry[1] + 1] = "entry"
    canvas[2 * exit_[0] + 1][2 * exit_[1] + 1] = "exit"
    return canvas


def render(canvas: list[list[str]], wall_code: int) -> str:
    '''Convert the matrix into text with ANSI colors (2 spaces per pixel).'''
    lines: list[str] = []
    for row in canvas:
        line = ""
        for kind in row:
            code = wall_code if kind == "wall" else COLORS[kind]
            if code is None:
                line += "  "
            else:
                line += f"\033[{code}m  \033[0m"
        lines.append(line)
    return "\n".join(lines)


def clear_screen() -> None:
    '''Clear the terminal and move the cursor to the top-left corner.'''
    print("\033[2J\033[H", end="")


Maze = tuple[list[list[int]], Sequence[Step], list[Cell]], int


def display(seed: int, grid: list[list[int]], path: Sequence[Step],
            entry: Cell = (0, 0),
            fortytwo: list[Cell] | None = None,
            regenerate: Callable[[], Any] | None = None) -> None:
    '''Show the maze in the terminal with a menu.

    grid       -- list of lists of integers 0-15 (grid[row][col])
    path       -- solution: list of steps (1, 2, 4, 8 or "N", "E", "S", "W")
    entry      -- (row, col) cell where the path starts
    fortytwo   -- cells of the "42" drawing (optional)
    regenerate -- function with no arguments that returns
                  (grid, path, fortytwo) for a new maze. If None,
                  option 1 is not shown.
    '''
    fortytwo = fortytwo or []
    show_path = False
    color_idx = 0
    message = ""

    def prepare(g: list[list[int]], p: Sequence[Step]) -> list[Cell]:
        '''Normalize the path p and walk it over grid g, returning the
        list of cells it visits (raises ValueError if it is invalid).'''
        steps = normalize_path(p)
        return walk(g, entry, steps)

    cells = prepare(grid, path)

    while True:
        clear_screen()
        canvas = build_canvas(grid, cells, fortytwo, show_path)
        print()
        print(render(canvas, WALL_COLORS[color_idx][1]))
        print()
        print(f"Tamanho: {len(grid[0])}x{len(grid)}  |  "
              f"Passos: {len(cells) - 1} |  "
              f"Seed: {seed}")
        print("=== A-Maze-ing ===")
        if regenerate is not None:
            print("1. Gerar um novo labirinto")
        print(f"2. {'Esconder' if show_path else 'Mostrar'} o caminho")
        print(f"3. Mudar a cor das paredes "
              f"(atual: {WALL_COLORS[color_idx][0]})")
        print("4. Sair")
        if message:
            print(message)
            message = ""

        try:
            choice = input("Escolha uma opção: ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break

        if choice == "1" and regenerate is not None:
            grid, path, fortytwo, seed = regenerate()
            cells = prepare(grid, path)
        elif choice == "2":
            show_path = not show_path
        elif choice == "3":
            color_idx = (color_idx + 1) % len(WALL_COLORS)
        elif choice == "4":
            break
        else:
            message = "Opção inválida."

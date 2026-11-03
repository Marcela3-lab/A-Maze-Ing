#!/usr/bin/python3
from __future__ import annotations

from typing import Callable, Sequence, Union

# Bits das paredes (iguais aos do Mazegenerator)
NORTH, EAST, SOUTH, WEST = 1, 2, 4, 8

# direção -> (delta_linha, delta_coluna)
MOVES = {NORTH: (-1, 0), EAST: (0, 1), SOUTH: (1, 0), WEST: (0, -1)}
LETTERS = {"N": NORTH, "E": EAST, "S": SOUTH, "W": WEST}

# Cores de fundo ANSI
WALL_COLORS = [("branco", 47), ("vermelho", 41), ("magenta", 45),
               ("ciano", 46), ("preto", 40)]
COLORS = {
    "floor": None,   # corredor (sem cor)
    "path": 103,     # amarelo
    "entry": 102,    # verde
    "exit": 104,     # azul
    "forty": 100,    # cinzento (desenho do 42)
}

Cell = tuple[int, int]
Step = Union[int, str]


def normalize_path(path: Sequence[Step]) -> list[int]:
    '''Aceita o caminho como lista de bits (1, 2, 4, 8) ou de letras
    ("N", "E", "S", "W"), ou como string ("NESW"). Devolve sempre
    uma lista de bits.'''
    result = []
    for step in path:
        if isinstance(step, str):
            step = LETTERS[step.upper()]
        if step not in MOVES:
            raise ValueError(
                f"passo inválido: {step!r} (use 1=N, 2=E, 4=S, 8=W)")
        result.append(step)
    return result


def walk(grid: list[list[int]], entry: Cell, steps: list[int]) -> list[Cell]:
    '''Percorre o caminho a partir da entrada e devolve a lista de células
    visitadas (incluindo a entrada). Valida que cada passo não atravessa
    parede nem sai da grelha.'''
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
    '''Converte a grelha numa matriz (2h+1) x (2w+1). As células ficam nas
    posições (2r+1, 2c+1) e as paredes nas posições entre elas.'''
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
            # pixel da célula + pixel da parede aberta entre prev e cell
            canvas[2 * cell[0] + 1][2 * cell[1] + 1] = "path"
            canvas[prev[0] + cell[0] + 1][prev[1] + cell[1] + 1] = "path"
            prev = cell

    entry, exit_ = path_cells[0], path_cells[-1]
    canvas[2 * entry[0] + 1][2 * entry[1] + 1] = "entry"
    canvas[2 * exit_[0] + 1][2 * exit_[1] + 1] = "exit"
    return canvas


def render(canvas: list[list[str]], wall_code: int) -> str:
    '''Matriz -> texto com cores ANSI (2 espaços por pixel).'''
    lines = []
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
    print("\033[2J\033[H", end="")


# O que a função "regenerate" tem de devolver: (grid, path, fortytwo)
Maze = tuple[list[list[int]], Sequence[Step], list[Cell]]


def display(grid: list[list[int]], path: Sequence[Step],
            entry: Cell = (0, 0),
            fortytwo: list[Cell] | None = None,
            regenerate: Callable[[], Maze] | None = None) -> None:
    '''Mostra o labirinto no terminal com um menu.

    grid       -- lista de listas de inteiros 0-15 (grid[row][col])
    path       -- solução: lista de passos (1,2,4,8 ou "N","E","S","W")
    entry      -- célula (row, col) onde o caminho começa
    fortytwo   -- células do desenho "42" (opcional)
    regenerate -- função sem argumentos que devolve (grid, path, fortytwo)
                  de um labirinto novo. Se None, a opção 1 não aparece.
    '''
    fortytwo = fortytwo or []
    show_path = False
    color_idx = 0
    message = ""

    def prepare(g, p):
        steps = normalize_path(p)
        return walk(g, entry, steps)  # valida e dá as células do caminho

    cells = prepare(grid, path)

    while True:
        clear_screen()
        print()
        canvas = build_canvas(grid, cells, fortytwo, show_path)
        print(render(canvas, WALL_COLORS[color_idx][1]))
        print()
        print(f"Tamanho: {len(grid[0])}x{len(grid)}  |  "
              f"Passos: {len(cells) - 1}")
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
            grid, path, fortytwo = regenerate()
            cells = prepare(grid, path)
        elif choice == "2":
            show_path = not show_path
        elif choice == "3":
            color_idx = (color_idx + 1) % len(WALL_COLORS)
        elif choice == "4":
            break
        else:
            message = "Opção inválida."
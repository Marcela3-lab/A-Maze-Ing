from collections import deque
from typing import Callable

NORTH, EAST, SOUTH, WEST = 1, 2, 4, 8

MOVES = {"N": (-1, 0), "E": (0, 1), "S": (1, 0), "W": (0, -1)}
#Para cada letra, quanto muda (linha, coluna) ao andar 
# nessa direção. Norte é -1 na linha porque a linha 0 é a de cima.
BITS = {"N": NORTH, "E": EAST, "S": SOUTH, "W": WEST}
#Liga cada letra ao seu bit. Assim, para saber se há parede a Norte: grid[r][c] & BITS["N"].
WALL_COLORS = [("branco", 47), ("vermelho", 41), ("magenta", 45)]
#40 a 47: cores de fundo terminal
COLORS = {"floor": None, "path": 103, "entry": 102, "exit": 104, "forty": 103}
#100 a 107: brilhante, 103: amarelo, 102: verde, 104:azul, 100:cinzento

def solve(grid, entry, exit_):
    h, w = len(grid), len(grid[0]) #altura: numero de linhas, #coluna: numero de colunas
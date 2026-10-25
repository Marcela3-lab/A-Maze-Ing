#!/usr/bin/python3
from generator import Mazegenerator
'''Dois reparos ao script
returns[i+1] é frágil: depende da posição na lista e de o teste 3 ser o último.
Mais claro é guardar, para cada teste, o canto e o resultado esperado juntos
(por exemplo, uma lista de tuplos (grelha, canto, esperado)) e percorrer essa lista.
Usa o assert com uma mensagem em vez de print("[OK]")/print("[KO]"). 
O silêncio quer dizer que passou, e a falha diz logo qual foi o caso.'''
#w = x = col, h = y = row ==> use (row, col)

grid1 = [
    [0,0,0],
    [0,0,0],
    [0,0,0],
    ]
size1 = 3
return1 = True

grid2 = [
        [0,0,4],
        [0,0,1],
        [0,0,0],
        ]
size2 = 3
return2 = False

grid3 = [
        [9,5,5,5,3],
        [10,9,1,3,10],
        [10,8,0,2,10],
        [10,12,4,6,10],
        [12,5,5,5,6],
        ]
size3 = 5 
return31 = False
return32 = True

sizes = [size1, size2, size3]
grids = [grid1, grid2, grid3]
returns = [return1, return2, return31, return32]

print(f"---- Testing for Open Blocks ----\n")

for i in range(3):
    maze = Mazegenerator(width=sizes[i], height=sizes[i])
    maze.grid = grids[i]
    print(f"TEST {i}: size= {sizes[i]} | Corner: (0,0)\n")
    if maze.is_block_open((0,0)) == returns[i]:
        print(f"[OK]")
    else:
        print(f"[KO]")
    if sizes[i] == 5:
        print(f"TEST {i}: size= {sizes[i]} | Corner: (1,1)\n")
        if maze.is_block_open((1,1)) == returns[i+1]:
            print(f"[OK]")
        else:
            print(f"[KO]")

print(f"---- Testing for Open Blocks, for every case ----\n")
maze2 = Mazegenerator(3,3)
twos = [(0,0), (0,1), (1,0), (1,1), (2,0), (2,1)]
fours = [(0,0), (0,1), (0,2), (1,0), (1,1), (1,2)]

for cells in twos:
    r, c = cells
    tgrid = [
    [0,0,0],
    [0,0,0],
    [0,0,0],
    ]
    tgrid[r][c] = 2
    maze2.grid = tgrid
    if maze2.is_block_open((0,0)) == False:
        print(f"{cells} in twos: [OK]")
    else:
        print(f"{cells} in twos: [KO]")

for cells in fours:
    r, c = cells
    tgrid = [
    [0,0,0],
    [0,0,0],
    [0,0,0],
    ]
    tgrid[r][c] = 4
    maze2.grid = tgrid
    if not maze2.is_block_open((0,0)):
        print(f"{cells} in fours: [OK]")
    else:
        print(f"{cells} in fours: [KO]")
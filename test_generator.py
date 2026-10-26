#!/usr/bin/python3
from generator import Mazegenerator

def test_maze(w, h, seed=None):
    testgrid = Mazegenerator(w, h, seed)
    testgrid.generate_dfs()

    #all cells were visited
    assert len(testgrid.visited) == w*h, f"not all cells were visited for w={w}, h={h}"

    #COHERENCE
    #For all cells, side neighbors have East/West bits equal
    for lista in testgrid.grid:
        for i in range(len(lista)-1):
            assert (lista[i] & 2 != 0) == (lista[i+1] & 8 != 0), f"walls not coeherent at East/West\n{testgrid.grid}"

    #For all cells, if South is closed (=1), down neighbor has North closed (=1)
    for row in range(h-1):
        for col in range(w):
            assert (testgrid.grid[row][col] & 4 != 0) == (testgrid.grid[row+1][col] & 1 != 0), f"walls not coeherent at South/North\n{testgrid.grid}"


    #CLOSED BORDERS
    #All cells of row 0/len-1 have North/South closed
    for cella in testgrid.grid[0]:
        assert cella & 1 != 0, f"north walls not closed in row 0\n{testgrid.grid}"
    for cellb in testgrid.grid[h-1]:
        assert cellb & 4 != 0, f"south walls not closed in row 0\n{testgrid.grid}"

    #All cells of col 0/len-1 have West/East closed
    for ia in range(h):
        assert testgrid.grid[ia][0] & 8 != 0, f"west wall not closed in col 0\n{testgrid.grid}"
    for ib in range(h):
        assert testgrid.grid[ib][w-1] & 2 != 0, f"east wall not closed in col{w-1}: {testgrid.grid[ib][w-1]}\n{testgrid.grid}"


    #OPEN PASSAGES == n-1
    n = 0
    for lista in testgrid.grid:
        for cell in lista:
            if cell & 2 == 0:
                n += 1
            if cell & 4 == 0:
                n += 1

    assert n == w*h - 1, f"there are {n} passages in a maze with {w*h} cells"

    return testgrid.grid

if __name__ == "__main__":

    #w = x = col, h = y = row ==> use (row, col)

    sizes= [(10,15), (4,4), (1,1), (1,7), (7,1), (2,2), (3,7), (7,3), (50, 50), (100, 100)]
    
    print(f">>>>Warning: DFS test for maze WITHOUT 42 design.\n")

    for combo in sizes:
        w = combo[0]
        h = combo[1]
        print(f" ---- TEST W = {w}, H = {h} ---- ")
        test_maze(w, h)
        print("[OK]")
    
    print(f"\n ---- SEED TEST ---- ")
    seeds = [10, 22]
    for i in seeds:
        print(f"\nSEED = {i}")
        grids = test_maze(w=5, h=5, seed=i)
        for row in grids:
            print(row)
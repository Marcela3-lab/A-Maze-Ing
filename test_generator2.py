from generator import Mazegenerator

#w = x = col, h = y = row ==> use (row, col)

sizes= [(10,15), (4,4), (1,7), (7,1), (2,2), (3,7), (7,3), (50, 50), (100, 100)]

for combo in sizes:
    w, h = combo
    if w*h < 2000:
        n = 4
    else:
        n = 9
    for i in range(n):
        print(f"Generating Maze {w}x{h}, seed={i}, perfect=False...")
        after_braiding = Mazegenerator(w, h, perfect=False, seed=i)
        print("Braiding...")
        after_braiding.generate()

        print("Testing for open blocks...")
        for rows in range(after_braiding.height):
            for cols in range(after_braiding.width):
                assert after_braiding.verify_open_areas((rows, cols)) is False, f"Open area found for {w}x{h} at ({rows}, {cols}), seed={i}"
        print("[OK]\n")
        
        #OPEN PASSAGES
        j = 0
        print("Testing for loops...")
        for lista in after_braiding.grid:
            for cell in lista:
                if cell & after_braiding.EAST == 0:
                    j += 1
                if cell & after_braiding.SOUTH == 0:
                    j += 1
        loops = j - (w * h - len(after_braiding.fortytwo_cells)) + 1
        if after_braiding.width >= 3 and after_braiding.height >= 3:
            assert loops >= 2, f"loops= {loops}, j={j}, 42cells={len(after_braiding.fortytwo_cells)} for {w}x{h}, seed={i}"
        print("[OK]\n")
        
        #COHERENCE
        print("Testing for coherence...")
        #For all cells, side neighbors have East/West bits equal
        for lista in after_braiding.grid:
            for x in range(len(lista)-1):
                assert (lista[x] & 2 != 0) == (lista[x+1] & 8 != 0), f"walls not coeherent at East/West for {w}x{h}, seed={i}"
    
        #For all cells, if South is closed (=1), down neighbor has North closed (=1)
        for row in range(h-1):
            for col in range(w):
                assert (after_braiding.grid[row][col] & 4 != 0) == (after_braiding.grid[row+1][col] & 1 != 0), f"walls not coeherent at South/North for {w}x{h}, seed={i}"
        print("[OK]\n")
    
    
        #CLOSED BORDERS
        print("Testing for closed borders...")
        #All cells of row 0/len-1 have North/South closed
        for cella in after_braiding.grid[0]:
            assert cella & 1 != 0, f"north walls not closed in row 0 for {w}x{h}, seed={i}"
        for cellb in after_braiding.grid[h-1]:
            assert cellb & 4 != 0, f"south walls not closed in row 0 for {w}x{h}, seed={i}"
    
        #All cells of col 0/len-1 have West/East closed
        for ia in range(h):
            assert after_braiding.grid[ia][0] & 8 != 0, f"west wall not closed in col 0 for {w}x{h}, seed={i}"
        for ib in range(h):
            assert after_braiding.grid[ib][w-1] & 2 != 0, f"east wall not closed in col{w-1}: {after_braiding.grid[ib][w-1]} for {w}x{h}, seed={i}"
        print("[OK]\n")
            
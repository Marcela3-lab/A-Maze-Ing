from generator import Mazegenerator

#w = x = col, h = y = row ==> use (row, col)

def coherence(maze):
    #For all cells, side neighbors have East/West bits equal
    for lista in maze.grid:
        for x in range(len(lista)-1):
            if (lista[x] & 2 != 0) != (lista[x+1] & 8 != 0):
                raise AssertionError(
                    f"walls not coeherent at East/West at col={x} in row {lista}")
        
    #For all cells, if South is closed (=1), down neighbor has North closed (=1)
    for row in range(h-1):
        for col in range(w):
            if (maze.grid[row][col] & 4 != 0) != (maze.grid[row+1][col] & 1 != 0):
                raise AssertionError(
                    f"walls not coeherent at South/North for row={row} and col={col}")


def closed_borders(maze):
    #All cells of row 0/len-1 have North/South closed
    h = maze.height
    w = maze.width
    for cella in maze.grid[0]:
        assert cella & 1 != 0, f"north walls not closed in row 0 for cell {cella}"
    for cellb in maze.grid[h-1]:
        assert cellb & 4 != 0, f"south walls not closed in row {h-1} for cell {cellb}"

    #All cells of col 0/len-1 have West/East closed
    for ia in range(h):
        assert maze.grid[ia][0] & 8 != 0, f"west wall not closed in col 0, row {ia}"
    for ib in range(h):
        assert maze.grid[ib][w-1] & 2 != 0, f"east wall not closed in col{w-1}, row {ib}"


def test_final_path(maze):
    #(mascara, direction row, direction col)
    directions = {
        "N": (Mazegenerator.NORTH, -1, 0),
        "E": (Mazegenerator.EAST, 0, 1),
        "S": (Mazegenerator.SOUTH, 1, 0),
        "W": (Mazegenerator.WEST, 0, -1),
        }

    if len(maze.path) == 0:
        raise AssertionError("Path is empty")    
    cur_cell = maze.entry_conv_yx
    for way in maze.path:
        row, col = cur_cell
        if not 0 <= row < maze.height or not 0 <= col < maze.width:
            raise AssertionError(
                f"Way went Off grid " 
                f"for way={way}, in ({row}, {col})"
                )
        if cur_cell in maze.fortytwo_cells:
            raise AssertionError(
                f"Way went in 42 design " 
                f"for way={way}, in ({row}, {col})"
                )
        values = directions[way]
        if maze.grid[row][col] & values[0] != 0:
            raise AssertionError(
                f"Wall closed for way={way}, in ({row}, {col})")
        cur_cell=(row + values[1], col + values[2])
    if cur_cell != maze.exit_conv_yx:
            raise AssertionError(
                f"end of path doesn't match Exit cell, " 
                f"End of path= {cur_cell} vs Exit= {maze.exit_conv_yx}"
            )


def loops(maze):
    j = 0
    w = maze.width
    h = maze.height
    for lista in maze.grid:
        for cell in lista:
            if cell & maze.EAST == 0:
                j += 1
            if cell & maze.SOUTH == 0:
                j += 1
    loops = j - (w * h - len(maze.fortytwo_cells)) + 1
    if maze.width >= 3 and maze.height >= 3:
        assert loops >= 2, f"loops= {loops}, j={j}, 42cells={len(maze.fortytwo_cells)}"


def open_areas(maze):
    for rows in range(maze.height):
        for cols in range(maze.width):
            if maze.verify_open_areas((rows, cols)) is True:
                raise AssertionError(f"Open area found for at ({rows}, {cols})")


def allcells_visited(maze):
    w = maze.width
    h = maze.height
    if len(maze.visited) != w*h - len(maze.fortytwo_cells):
        raise AssertionError(
            f"not all cells were visited for w={w}, h={h}, "
            f"visited={len(maze.visited)}, 42cells={maze.fortytwo_cells}")



if __name__ == "__main__":

    sizes= [(10,15), (4,4), (13,17), (17,3), (2,2), (3,7), (7,3), (50, 50), (100, 100)]

    for combo in sizes:
        w, h = combo
        for seed in range(5):
            for perfect in (True, False):
                maze = Mazegenerator(
                    width= w,
                    height = h,
                    entry_xy= (0,0),
                    exit_xy= (w-1, h-1),
                    perfect= perfect,
                    seed = seed,
                )
                print(f">> Generating maze {w}x{h}, seed={seed}, perfect={perfect}...\n")
                maze.generate()
                assert len(maze.visited) == w*h - len(maze.fortytwo_cells), f"not all cells were visited for w={w}, h={h}"
                try:
                    allcells_visited(maze)
                    coherence(maze)
                    closed_borders(maze)
                    if not maze.perfect:
                        loops(maze)
                        open_areas(maze)
                    test_final_path(maze)
                except AssertionError:
                    print(f"Error: {w}x{h}, seed={seed}, perfect={perfect}")
                    raise
                print("[OK]\n")

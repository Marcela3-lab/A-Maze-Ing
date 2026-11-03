from generator import Mazegenerator

#w = x = col, h = y = row ==> use (row, col)

def coherence(maze):
    h = maze.height
    w = maze.width
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
    if len(maze.visited) != w*h:
        raise AssertionError(
            f"not all cells were visited for w={w}, h={h}, visited={len(maze.visited)}")


def ft_closed(maze):
    w = maze.width
    h = maze.height
    for cells in maze.fortytwo_cells:
        row, col = cells
        if maze.grid[row][col] != 15:
            raise AssertionError(f"42 cells not closed for w={w}, h={h}, seed={maze.seed}")


def check_reproducible(w, h, seed, perfect):
    maze1 = Mazegenerator(
        width= w,
        height= h,
        entry_xy= (0,0),
        exit_xy=(w-1, h-1),
        perfect= perfect,
        seed= seed,
    )
    maze2 = Mazegenerator(
        width= w,
        height= h,
        entry_xy= (0,0),
        exit_xy=(w-1, h-1),
        perfect= perfect,
        seed= seed,
    )
    maze1.generate()
    maze2.generate()
    for rows in range(h):
        for cols in range(w):
            if maze1.grid[rows][cols] != maze2.grid[rows][cols]:
                raise AssertionError(
                    f"grids differ for Maze1: w={maze1.width}, h={maze1.height}, perfect={maze1.perfect}, seed={maze1.seed}\n"
                    f"Maze2: w={maze2.width}, h={maze2.height}, perfect={maze2.perfect}, seed={maze2.seed}"
                    )
    for i in range(len(maze1.path)):
        if maze1.path[i] != maze2.path[i]:
            raise AssertionError(
                f"path differ for Maze1: w={maze1.width}, h={maze1.height}, perfect={maze1.perfect}, seed={maze1.seed}\n"
                f"Maze2: w={maze2.width}, h={maze2.height}, perfect={maze2.perfect}, seed={maze2.seed}"
                )


def failure_cases():
    base = {"width": 10, "height": 10, "entry_xy": (0, 0), "exit_xy": (9, 9)}

    def case(description, **changes):
        return (description, {**base, **changes})

    return [
        case("exit x == width", exit_xy=(10, 9)),
        case("exit y == height", exit_xy=(9, 10)),
        case("exit negative", exit_xy=(-1, 5)),
        case("entry x == width", entry_xy=(10, 0)),
        case("entry y == height", entry_xy=(0, 10)),
        case("entry negative", entry_xy=(0, -1)),
        case("entry == exit", exit_xy=(0, 0)),
        case("width 1", width=1, exit_xy=(0, 9)),
        case("width 101", width=101),
        case("height 1", height=1, exit_xy=(9, 0)),
        case("height 101", height=101),
        case("entry inside 42", width=20, height=15,
             entry_xy=(9, 7), exit_xy=(19, 14)),
        case("exit inside 42", width=20, height=15,
             entry_xy=(0, 0), exit_xy=(9, 7)),
    ]


if __name__ == "__main__":

    sizes= [(10,15), (4,4), (13,17), (17,3), (2,2), (5,5), (3,7), (7,3), (50, 50), (100, 100)]
    passed = 0
    failed = 0

    with open("tests.txt", "w") as log:
        for combo in sizes:
            w, h = combo
            n = w*h
            if n > 1500:
                n = 7
            else:
                n = 9
            for seed in range(n):
                for perfect in (True, False):
                    try:
                        maze = Mazegenerator(
                            width= w,
                            height = h,
                            entry_xy= (0,0),
                            exit_xy= (w-1, h-1),
                            perfect= perfect,
                            seed = seed,
                        )
                        maze.generate()
                        allcells_visited(maze)
                        coherence(maze)
                        closed_borders(maze)
                        if maze.perfect == False:
                            loops(maze)
                            open_areas(maze)
                        test_final_path(maze)
                        if len(maze.fortytwo_cells) > 0:
                            ft_closed(maze)
                    except Exception as e:
                        log.write(f"Error: {w}x{h}, seed={seed}, perfect={perfect}\n")
                        log.write(f"{e}\n\n")
                        failed += 1
                    else:
                        passed += 1
                    print(f"Testing: {passed} OK, {failed} KO", end="\r", flush=True)

        try:
            maze2 = Mazegenerator(
                width= 10,
                height = 15,
                entry_xy= (0,0),
                exit_xy= (10-1, 15-1),
                perfect= True,
                seed = 1,
            )        
            maze2.generate()
            maze2.generate()
            allcells_visited(maze2)
            coherence(maze2)
            closed_borders(maze2)
            if maze2.perfect == False:
                loops(maze2)
                open_areas(maze2)
            test_final_path(maze2)
        except Exception as e:
            log.write(f"Error Maze2")
            log.write(f"{e}\n\n")
            failed += 1
        else:
            passed += 1
        print(f"Testing: {passed} OK, {failed} KO", end="\r", flush=True)

        for description, args in failure_cases():
            try:
                Mazegenerator(**args).generate()
            except ValueError:
                passed += 1
            except Exception as e:
                log.write(f"Crash (not ValueError): {description}: "
                            f"{type(e).__name__}: {e}\n\n")
                failed += 1
            else:
                log.write(f"Not rejected: {description}\n\n")
                failed += 1
        try:
            size = [(5,5), (10, 15), (2,2), (25, 30)]
            for s in size:
                for seed2 in range(3):
                    for perfect in (True, False):
                        check_reproducible(w=s[0], h=s[1], seed=seed2, perfect=perfect)
        except Exception as e:
            log.write(f"Maze or path differ: {s}, seed={seed2}, perfect={perfect}\n")
            log.write(f"{e}\n\n")
            failed += 1
        else:
            passed += 1
        print(f"Testing: {passed} OK, {failed} KO", end="\r", flush=True)

    
    print(f"Testing: {passed} OK, {failed} KO", end="\r", flush=True)
    print()
    print(f"Failed Tests: {failed}")
    print(f"Passed Tests: {passed}")
    print(f"Check Failed tests in tests.txt")



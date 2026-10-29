from generator import Mazegenerator

#w = x = col, h = y = row ==> use (row, col)

def debug1():
    sizes= [(9,7), (15,10), (2,2), (3,2), (5,5), (10,10), (50,20), (100,100)]
    entries= [(1,1), (0,0), (2,2), (3,2)]
    exits= [(5,5), (2,2), (10,12), (6,19)]

    for k in range(len(entries)):
        for combo in sizes:
            w, h = combo
            for i in range(5):
                print(f">>> Creating maze {w}x{h}, seed= {i}....\n")
                try:
                    maze = Mazegenerator(
                        width=w,
                        height=h,
                        entry_xy=entries[k],
                        exit_xy= exits[k],
                        seed=i,
                        perfect=False
                        )
                except Exception as e:
                    print(
                        f"Error: {e}\n"
                        f"Maze details: {w}x{h}, seed={i}\n"
                        )
                    break

                print(f"Generating maze....")
                try:
                    maze.generate()
                except Exception as e:
                    print(
                        f"Error: {e}\n"
                        f"Maze details: {w}x{h}, seed={i}\n"
                        )
                print("[OK]\n")

def debug2():
    try:
        maze = Mazegenerator(
            width=10,
            height=10,
            entry_xy=(3,2),
            exit_xy= (6,19),
            )
    except Exception as e:
        print(
            f"{e}\n"
            )

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
                try:
                    test_final_path(maze)
                except AssertionError:
                    print(f"Error: {w}x{h}, seed={seed}, perfect={perfect}")
                    raise
                print("[OK]\n")

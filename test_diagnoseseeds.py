from generator import Mazegenerator


#w = x = col, h = y = row ==> use (row, col)
w = 5
h = 5
s= 0
maze = Mazegenerator(
    width=w,
    height=h,
    seed=s,
    entry_xy= (0,0),
    exit_xy= (w-1, h-1),
    perfect=True,
    )
maze.generate()
print("Maze1:")
for rows in maze.grid:
    print(rows)
print(f"Path: {maze.path}")

maze2 = Mazegenerator(
    width=w,
    height=h,
    seed=s,
    entry_xy= (0,0),
    exit_xy= (w-1, h-1),
    perfect=True,
    )
maze2.generate()
print("Maze2:")
for rows in maze2.grid:
    print(rows)
print(f"Path: {maze2.path}")

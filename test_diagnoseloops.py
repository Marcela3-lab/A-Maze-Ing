from generator import Mazegenerator


#w = x = col, h = y = row ==> use (row, col)
w = 4
h = 4
s= 8
maze = Mazegenerator(
    width=w,
    height=h,
    seed=s,
    entry_xy= (0,0),
    exit_xy= (w-1, h-1),
    perfect=False,
    )
maze.generate()
for rows in maze.grid:
    print(rows)
count_deadends = 0
for rows in range(maze.height):
    for cols in range(maze.width):
       if maze.is_deadend((rows, cols)):
           count_deadends += 1
print(f"Perfect = {maze.perfect} | count of deadends = {count_deadends}\n")

print("Counting Loops")
j = 0
for lista in maze.grid:
    for cell in lista:
        if cell & maze.EAST == 0:
            j += 1
        if cell & maze.SOUTH == 0:
            j += 1
loops = j - (maze.width * maze.height - len(maze.fortytwo_cells)) + 1
print(f"loops= {loops}, j={j}, 42cells={len(maze.fortytwo_cells)}")

 
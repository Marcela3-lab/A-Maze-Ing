from generator import Mazegenerator


#w = x = col, h = y = row ==> use (row, col)

maze = Mazegenerator(width=3, height=7, seed=3)
maze.generate()
for rows in maze.grid:
    print(rows)
count_deadends = 0
for rows in range(maze.height):
    for cols in range(maze.width):
       if maze.is_deadend((rows, cols)):
           count_deadends += 1
print(f"Perfect | count of deadends = {count_deadends}\n")

maze.braiding_maze()
count_deadends = 0
for rows in range(maze.height):
    for cols in range(maze.width):
       if maze.is_deadend((rows, cols)):
           count_deadends += 1
print(f"\nBraiding | count of deadends = {count_deadends}")
for rows in maze.grid:
    print(rows)

print("\nCounting Loops")
j = 0
for lista in maze.grid:
    for cell in lista:
        if cell & maze.EAST == 0:
            j += 1
        if cell & maze.SOUTH == 0:
            j += 1
loops = j - (maze.width * maze.height - len(maze.fortytwo_cells)) + 1
print(f"loops= {loops}, j={j}, 42cells={len(maze.fortytwo_cells)}")

 
#!/usr/bin/python3
import random

class Mazegenerator:
    NORTH: int = 1
    EAST: int = 2
    SOUTH: int = 4
    WEST: int = 8

    #x = col, y = row ==> use (row, col)
    def __init__(self, width: int, height: int, seed: int | None = None) -> None:
        self.width: int = width
        self.height: int = height
        self.grid: list[list[int]] = []
        self.visited: set[tuple[int, int]] = set()
        self.stack: list[tuple[int, int]] = []
        if seed is None:
            self.seed = random.randrange(1, 2**32)
        else:
            self.seed = seed
        self.randgen = random.Random(self.seed)


    def setupgrid(self):
        """sets up the grid based on the input in config file,
        with all values equal to 15 (closed cells). grid[row][col]"""

        for y in range(self.height):
            gridrow = []
            for x in range(self.width):
                gridrow.append(15)
            self.grid.append(gridrow)


    def check_neighbors(self, row: int, col: int) -> tuple[int] | None:
        '''checks neighbors of current (row, col) cell. 
        Adds to a list if not visited'''

        neighbors = []

        if row == 0:
            top = None
        else:
            top = (row-1, col)
        if col == self.width-1:
            right = None
        else:
            right = (row, col+1)
        if row == self.height-1:
            bottom = None
        else:
            bottom = (row+1, col)
        if col == 0:
            left = None
        else:
            left = (row, col-1)

        if top is not None and top not in self.visited:
            neighbors.append(top)
        if right is not None and right not in self.visited:
            neighbors.append(right)
        if bottom is not None and bottom not in self.visited:
            neighbors.append(bottom)
        if left is not None and left not in self.visited:
            neighbors.append(left)
        
        if len(neighbors) > 0:
            r = self.randgen.choice(neighbors) #random choice with seed defined by class attribute
            return r
        else:
            return None

    
    def remove_walls(self, current: tuple[int], next: tuple[int]) -> None:
        '''remove the wall between current & selected neighbor cells'''

        #grid[row][col]
        col = next[1] - current[1]
        if col == 1:
            self.grid[next[0]][next[1]] &= ~self.WEST #removes west side wall
            self.grid[current[0]][current[1]] &= ~self.EAST
        elif col == -1:
            self.grid[next[0]][next[1]] &= ~self.EAST
            self.grid[current[0]][current[1]] &= ~self.WEST
        
        row = next[0] - current[0]
        if row == 1:
            self.grid[next[0]][next[1]] &= ~self.NORTH
            self.grid[current[0]][current[1]] &= ~self.SOUTH
        elif row == -1:
            self.grid[next[0]][next[1]] &= ~self.SOUTH
            self.grid[current[0]][current[1]] &= ~self.NORTH


    def generate_dfs(self) -> None:
        '''generates a perfect maze using Depth-First Search (DFS) algorithm,
        using an iterative implementation (with stack).
        Modifies the grid[row][col].'''

        self.setupgrid()
        if len(self.grid) == 0:
            pass #RAISE EXCEPTION: grid not created or width/height not defined
        
        #x = col, y = row, (row, col)
        #STEP 1: Choose the initial cell, mark it as visited and push it to the stack
        current = (0, 0)
        self.visited.add(current)
        self.stack.append(current)

        #STEP 2: While the stack is not empty
        while len(self.stack) > 0:

            # STEP 2.a: Pop a cell from the stack and make it a current cell
            current = self.stack.pop()
            row = current[0]
            col = current[1]

            # STEP 2.b: If the current cell has any neighbours which have not been visited
            #pick random neighbor as next cell
            next_cell = self.check_neighbors(row, col)
            
            # STEP 2.b: If the current cell has any neighbours which have not been visited
            if next_cell is not None:
                #STEP 2.b.i: Push the current cell to the stack
                self.stack.append(current)
                #STEP 2.b.ii: Remove the wall between the current cell and the chosen cell
                self.remove_walls(current, next_cell)

                #STEP 2.b.iv: Mark the chosen cell as visited and push it to the stack
                self.visited.add(next_cell)
                self.stack.append(next_cell)



if __name__ == "__main__":

    width = 5 #num de elementos por lista
    height = 5 #num de listas

    testgrid = Mazegenerator(width, height)
    # testgrid.setupgrid()
    
    # print(f"GRID BEFORE: {testgrid.grid}")
    # print("---test check neighbors function ---")
    # next_cell = testgrid.check_neighbors(0, 0)
    # print(f"next cell: {next_cell}")

    print("---test DFS function ---")
    testgrid.generate_dfs()
    print(f"len visited: {len(testgrid.visited)}")
    print(f"GRID AFTER: {testgrid.grid}")






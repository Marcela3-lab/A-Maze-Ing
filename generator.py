#!/usr/bin/python3
import random

class Mazegenerator:
    NORTH: int = 1
    EAST: int = 2
    SOUTH: int = 4
    WEST: int = 8

    #x = col, y = row ==> use (row, col)
    def __init__(self, width: int, height: int):
        self.width: int = width
        self.height: int = height
        self.grid: list[list[int]] = []
        self.visited: set[tuple[int, int]] = set()
        self.stack: list[tuple[int, int]] = []


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
            r = random.choice(neighbors) #INCLUIR SEED com atributo da classe
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



    def test_dfs(self):
        if len(self.grid) == 0:
            pass #RAISE EXCEPTION: grid not created or width/height not defined
        
        #x = col, y = row, (row, col)
        #STEP 1: da pagina atual da wikipedia REMOTAR AQUI !!! <=====================
        current_cell = (0, 0)
        self.visited.add(current_cell)

        #STEP 2: while there are unvisited cells
        while len(self.visited) > 0: #!!ALTERAR LOOP INFINITO!!!
            current
            row = current_cell[0]
            col = current_cell[1]
            #pick a random neighbor
            next_cell = self.check_neighbors(row, col)
            if (next_cell) is None:
                current_cell = None #redundante, retirar depois de atualizar while??
                break
            
            self.stack.append(current_cell)
            self.remove_walls(current_cell, next_cell)

            #make the chosen cell the current cell and add it to the visited
            self.visited.add(next_cell)
            current_cell = next_cell





if __name__ == "__main__":

    width = 4  #num de elementos por lista
    height = 4 #num de listas

    testgrid = Mazegenerator(width, height)
    testgrid.setupgrid()
    
    print(f"GRID BEFORE: {testgrid.grid}")
    # print("---test check neighbors function ---")
    # next_cell = testgrid.check_neighbors(0, 0)
    # print(f"next cell: {next_cell}")

    print("---test DFS function ---")
    testgrid.test_dfs()
    print(f"visited: {testgrid.visited}")
    print(f"GRID AFTER: {testgrid.grid}")






#!/usr/bin/python3
import random

class Mazegenerator:
    NORTH: int = 1
    EAST: int = 2
    SOUTH: int = 4
    WEST: int = 8
    DEADENDS = [7, 11, 13, 14]


    #width = col, height = row ==> use (row, col)
    def __init__(
            self, width: int, height: int,
            #entry: tuple = (0,0), exit: tuple = (0,0),
            perfect: bool = True,
            seed: int | None = None,
        ) -> None:
        if width <= 0:
            raise ValueError("width must be >= 0")
        else:
            self.width: int = width
        if height <= 0:
            raise ValueError("height must be .= 0")
        else:
            self.height: int = height
        #self.entry: tuple = entry // condicoes: entry!= exit, e dentro da grelha
        #self.exit: tuple = exit
        self.perfect: bool = perfect
        self.grid: list[list[int]] = []
        self.visited: set[tuple[int, int]] = set()
        self.stack: list[tuple[int, int]] = []
        if seed is None:
            self.seed = random.randrange(1, 2**32)
        else:
            self.seed = seed
        self.randgen = random.Random(self.seed)
        self.fortytwo_cells: list[tuple[int, int]] = []


    def setupgrid(self):
        """sets up the grid based on the input in config file,
        with all values equal to 15 (closed cells). grid[row][col]"""

        for y in range(self.height):
            gridrow = []
            for x in range(self.width):
                gridrow.append(15)
            self.grid.append(gridrow)


    def unvisited_neighbor(self, row: int, col: int) -> tuple[int, int] | None:
        '''checks neighbors of current (row, col) cell. 
        Adds to a list if not visited. Returns a random unvisited neighbor as
        tuple or None if there is none.'''

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

    
    def remove_walls(
        self, current: tuple[int, int], next: tuple[int, int]
        ) -> None:
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


    def fortytwo(self) -> list[tuple]:
        '''Finds center of grid and selects cells for the 42 design,
        by marking them as visited. Returns a list of the cells' coordinates
        (tuples) to help the design in the terminal'''

        #validate enough space in grid for design
        if self.width >= 9 or self.height >= 7:
            #find center. width = col, height = row ==> use (row, col)
            c_row = int(self.height/2)
            c_col = int(self.width/2)

            #add 42 cells(tuples) into visited list & 42 list for terminal
            self.fortytwo_cells = [
                (c_row-2, c_col-3), (c_row-1, c_col-3), (c_row-1, c_col-2),
                (c_row-1, c_col-1), (c_row, c_col-1), (c_row+1, c_col-1),
                (c_row+2, c_col-1), (c_row-2, c_col+1), (c_row-2, c_col+2),
                (c_row-2, c_col+3), (c_row-1, c_col+3), (c_row, c_col+1),
                (c_row, c_col+2), (c_row, c_col+3), (c_row+1, c_col+1),
                (c_row+2, c_col+1), (c_row+2, c_col+2), (c_row+2, c_col+3)
            ]
            for cell in self.fortytwo_cells:
                self.visited.add(cell)
        return self.fortytwo_cells


    def dfs(self) -> None:
        '''generates a perfect maze using Depth-First Search (DFS) algorithm,
        using an iterative implementation (with stack).
        Modifies the grid[row][col].'''

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
            next_cell = self.unvisited_neighbor(row, col)
            
            # STEP 2.b: If the current cell has any neighbours which have not been visited
            if next_cell is not None:
                #STEP 2.b.i: Push the current cell to the stack
                self.stack.append(current)
                #STEP 2.b.ii: Remove the wall between the current cell and the chosen cell
                self.remove_walls(current, next_cell)

                #STEP 2.b.iv: Mark the chosen cell as visited and push it to the stack
                self.visited.add(next_cell)
                self.stack.append(next_cell)


    def get_braid_neighbors(self, row: int, col: int) -> list[tuple[int, int]] | None:
        '''checks neighbors of current (row, col) cell. 
        Adds to a list if not in 42 design. Returns a list of tuples.
        Used for PERFECT=false.'''

        braids = []

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

        if top is not None and top not in self.fortytwo_cells:
            braids.append(top)
        if right is not None and right not in self.fortytwo_cells:
            braids.append(right)
        if bottom is not None and bottom not in self.fortytwo_cells:
            braids.append(bottom)
        if left is not None and left not in self.fortytwo_cells:
            braids.append(left)
        
            return braids


    def is_block_open(self, corner: tuple[int, int]) -> bool:
        row = corner[0]
        col = corner[1]  
        
        for r in range(3):
            if row + r <= self.height - 1:
                for c in range(3):
                    if (col + c) <= self.width - 1:
                        cell = self.grid[row+r][col+c]
                        if cell & self.EAST != 0 and c != 2:
                            return False
                        if cell & self.SOUTH != 0 and r != 2:
                            return False
        return True                        
            

    #width = col, height = row ==> use (row, col)
    def verify_open_areas(self, current: tuple[int, int]) -> bool:
        '''For the current cell, identifies all 9 possible combinations of
        3x3 blocks excluding edge cases. Verifies if any block is open by
        calling another function and returns True if there is an open area.'''

        row = current[0]
        col = current[1]

        for r in range(3):
            if (row - r >= 0):
                for c in range(3):
                    if(col - c >= 0):
                        corner = (row - r, col - c)
                        if self.is_block_open(corner):
                            return True
        return False
    
    
    def is_deadend(self, cell: tuple[int, int]) -> bool:
        row = cell[0]
        col = cell[1]
        if self.grid[row][col] in self.DEADENDS:
            return True
        else:
            return False


    def braiding_maze(self) -> None:

        for row in range(len(self.grid)):
            for col in range(len(self.grid[row])):
                current = (row, col)
                if self.is_deadend(current):
                    braid_nghb = self.get_braid_nghbors(row, col)
                    self.randgen.shuffle(braid_nghb) #shuffle da lista
                    deads = []
                    no_deads = []
                    for neighbor in braid_nghb:
                        if self.is_deadend(neighbor):
                            deads.append(neighbor)
                        else:
                            no_deads.append(neighbor)
                    final_list = deads + no_deads

                    for candidate in final_list:
                        self.remove_walls(current, candidate)
                        if self.verify_open_areas(current):
                            self.add_walls_back(current, candidate)
                        else:
                            break


    def generate(self) -> None:
        '''Builds the maze with 42 design, if possible, and generates
        the path.'''
        self.setupgrid()
        if len(self.grid) == 0:
            raise ValueError("Grid setup Error: Invalid data")
        
        self.fortytwo()
        self.dfs()
        

if __name__ == "__main__":

    width = 10 #num de elementos por lista
    height = 10 #num de listas

    testmaze = Mazegenerator(width, height)
    # testmaze.setupgrid()
    
    # print(f"GRID BEFORE: {testmaze.grid}")
    # print("---test check neighbors function ---")
    # next_cell = testmaze.unvisited_neighbor(0, 0)
    # print(f"next cell: {next_cell}")

    # print("---test DFS function ---")
    # testmaze.dfs()
    # print(f"len visited: {len(testmaze.visited)}")
    # print(f"GRID AFTER: {testmaze.grid}")

    # print(" --- Test 42 function --- ")
    # testlist = testmaze.fortytwo()
    # print(f"\ntestlist: {testlist}")

    testmaze.generate()
    print("Result! grid:")
    for lines in testmaze.grid:
        form = list(map("{:02d}".format, lines))
        print(form)







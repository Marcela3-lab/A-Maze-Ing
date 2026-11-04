import random


class Mazegenerator:
    """Generates a maze and its shortest path.

    The maze is a grid of integers, one per cell, where each set bit is a
    closed wall: NORTH = 1, EAST = 2, SOUTH = 4, WEST = 8. Internally,
    coordinates are (row, col).

    Attributes:
        width: number of columns.
        height: number of rows.
        perfect: True for a perfect maze, False for a braided one.
        seed: seed used to create the random generator.
        entry_xy: entry cell as given, (x, y).
        exit_xy: exit cell as given, (x, y).
        entry_conv_yx: entry cell as (row, col).
        exit_conv_yx: exit cell as (row, col).
        grid: grid[row][col] holds the walls of each cell.
        path: shortest path from entry to exit, as N, E, S, W.
        fortytwo_cells: (row, col) of the cells of the "42" pattern.
    """
    NORTH: int = 1
    EAST: int = 2
    SOUTH: int = 4
    WEST: int = 8
    DEADENDS: set[int] = {7, 11, 13, 14}

    def __init__(
            self, width: int, height: int,
            entry_xy: tuple[int, int],
            exit_xy: tuple[int, int],
            perfect: bool = True,
            seed: int | None = None,
            ) -> None:
        """Initialize the generator and validate its parameters.

        Args:
            width: number of columns, between 2 and 100.
            height: number of rows, between 2 and 100.
            entry_xy: entry cell as (x, y), inside the maze.
            exit_xy: exit cell as (x, y), inside the maze and different
                from the entry.
            perfect: if True, the maze has a single path between any two
                cells. If False, loops are added (no 3x3 open areas).
            seed: integer seed. If None, a random seed is chosen and
                stored in self.seed.

        Raises:
            ValueError: if the size is out of range, or if the entry or
                exit are outside the maze or equal.
        """
        if width < 2 or width > 100:
            raise ValueError("Maze's width must be >= 2 and <= 100")
        else:
            self.width: int = width
        if height < 2 or height > 100:
            raise ValueError("Maze's height must be >= 2 and <= 100")
        else:
            self.height: int = height
        self.entry_conv_yx = self.validate_convert_coord(entry_xy)
        self.exit_conv_yx = self.validate_convert_coord(exit_xy)
        if entry_xy == exit_xy:
            raise ValueError("Error: Entry and Exit coordinates are equal")
        else:
            self.entry_xy = entry_xy
            self.exit_xy = exit_xy
        self.perfect: bool = perfect
        if seed is None:
            self.seed = random.randrange(1, 2**32)
        else:
            self.seed = seed
        self.randgen = random.Random(self.seed)
        self.reset_state()

    def validate_convert_coord(
            self, coord_xy: tuple[int, int]) -> tuple[int, int]:
        """Check that a point is inside the maze and convert it.

        Args:
            coord_xy: point as (x, y).

        Returns:
            The same point as (row, col).

        Raises:
            ValueError: if x is outside the width or y outside the height.
        """
        x, y = coord_xy
        if not 0 <= x < self.width:
            raise ValueError(f"{coord_xy} outside width = {self.width}")
        if not 0 <= y < self.height:
            raise ValueError(f"{coord_xy} outside height = {self.height}")

        return (y, x)

    def setupgrid(self) -> None:
        """Fill self.grid with height rows of width cells, all set to 15.

        A value of 15 means that the four walls of the cell are closed.
        """

        for y in range(self.height):
            gridrow = []
            for x in range(self.width):
                gridrow.append(15)
            self.grid.append(gridrow)

    def unvisited_neighbor(self, row: int, col: int) -> tuple[int, int] | None:
        """Pick a random unvisited neighbour of a cell.

        Args:
            row: row of the current cell.
            col: column of the current cell.

        Returns:
            A random neighbour as (row, col) among those inside the grid
            that are not in self.visited, or None if there is none.
        """

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
            r = self.randgen.choice(neighbors)
            return r
        else:
            return None

    def remove_walls(
            self, current: tuple[int, int], next: tuple[int, int]
            ) -> None:
        """Open the wall between two adjacent cells.

        The wall is cleared in both cells, so the grid stays coherent.

        Args:
            current: first cell as (row, col).
            next: adjacent cell as (row, col).
        """

        col = next[1] - current[1]
        if col == 1:
            self.grid[next[0]][next[1]] &= ~self.WEST
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

    def fortytwo(self) -> list[tuple[int, int]]:
        """Choose the cells that draw the "42" pattern.

        The pattern is centred in the grid and is only drawn if the maze is
        at least 9 columns by 7 rows. Its cells are marked as visited, so
        the DFS never enters them and they stay closed.

        Returns:
            The list of (row, col) of the pattern, empty if it does not fit.
        """

        if self.width >= 9 and self.height >= 7:
            c_row = int(self.height/2)
            c_col = int(self.width/2)

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
        """Carve a perfect maze with an iterative depth-first search.

        Starts at (0, 0), moves to a random unvisited neighbour opening the
        wall between them, and backtracks with an explicit stack when there
        is none. Modifies self.grid.
        """

        current = (0, 0)
        self.visited.add(current)
        self.stack.append(current)

        while len(self.stack) > 0:

            current = self.stack.pop()
            row, col = current
            next_cell = self.unvisited_neighbor(row, col)

            if next_cell is not None:
                self.stack.append(current)
                self.remove_walls(current, next_cell)
                self.visited.add(next_cell)
                self.stack.append(next_cell)

    def get_braid_neighbors(
            self, row: int, col: int) -> list[tuple[int, int]]:
        """List the neighbours that could be opened to create a loop.

        Args:
            row: row of the cell.
            col: column of the cell.

        Returns:
            The neighbours inside the grid, outside the "42" pattern, with a
            closed wall between them and the cell. Possibly empty.
        """

        braids = []
        cell = self.grid[row][col]

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

        if (top is not None and top not in self.fortytwo_cells
                and (cell & self.NORTH) != 0):
            braids.append(top)
        if (right is not None and right not in self.fortytwo_cells
                and (cell & self.EAST) != 0):
            braids.append(right)
        if (bottom is not None and bottom not in self.fortytwo_cells
                and (cell & self.SOUTH) != 0):
            braids.append(bottom)
        if (left is not None and left not in self.fortytwo_cells
                and (cell & self.WEST) != 0):
            braids.append(left)

        return braids

    def is_block_open(self, corner: tuple[int, int]) -> bool:
        """Check if a 3x3 block of cells has no internal walls.

        Args:
            corner: upper left cell of the block as (row, col). The block
                must be fully inside the grid.

        Returns:
            True if the 12 internal passages of the block are all open.
        """
        row, col = corner

        for r in range(3):
            for c in range(3):
                cell = self.grid[row+r][col+c]
                if cell & self.EAST != 0 and c != 2:
                    return False
                if cell & self.SOUTH != 0 and r != 2:
                    return False
        return True

    def verify_open_areas(self, current: tuple[int, int]) -> bool:
        """Check if any 3x3 block containing a cell is fully open.

        Only blocks that fit inside the grid are checked (up to 9).

        Args:
            current: cell as (row, col).

        Returns:
            True if there is an open 3x3 area around the cell.
        """

        row, col = current
        for r in range(3):
            if row - r >= 0 and row - r + 2 <= self.height - 1:
                for c in range(3):
                    if col - c >= 0 and col - c + 2 <= self.width - 1:
                        corner = (row - r, col - c)
                        if self.is_block_open(corner):
                            return True
        return False

    def is_deadend(self, cell: tuple[int, int]) -> bool:
        """Check if a cell has exactly one open wall.

        Args:
            cell: cell as (row, col).

        Returns:
            True if the cell is a dead-end.
        """
        row, col = cell
        return self.grid[row][col] in self.DEADENDS

    def add_walls_back(
            self, current: tuple[int, int], candidate: tuple[int, int]
            ) -> None:
        """Close again a wall that was opened while braiding.

        This is the inverse of remove_walls: the wall is closed in both
        cells. It is used when opening the wall created a 3x3 open area.

        Args:
            current: first cell as (row, col).
            candidate: adjacent cell as (row, col).
        """

        col = candidate[1] - current[1]
        if col == 1:
            self.grid[candidate[0]][candidate[1]] |= self.WEST
            self.grid[current[0]][current[1]] |= self.EAST
        elif col == -1:
            self.grid[candidate[0]][candidate[1]] |= self.EAST
            self.grid[current[0]][current[1]] |= self.WEST

        row = candidate[0] - current[0]
        if row == 1:
            self.grid[candidate[0]][candidate[1]] |= self.NORTH
            self.grid[current[0]][current[1]] |= self.SOUTH
        elif row == -1:
            self.grid[candidate[0]][candidate[1]] |= self.SOUTH
            self.grid[current[0]][current[1]] |= self.NORTH

    def count_loops(self) -> int:
        """Count the independent loops of the maze.

        Computed as open passages - connected cells + 1. A perfect maze has
        0 loops. Cells of the "42" pattern are not counted.

        Returns:
            The number of loops.
        """
        j = 0
        w = self.width
        h = self.height
        for lista in self.grid:
            for cell in lista:
                if cell & self.EAST == 0:
                    j += 1
                if cell & self.SOUTH == 0:
                    j += 1
        loops = j - (w * h - len(self.fortytwo_cells)) + 1
        return loops

    def braiding_maze(self) -> None:
        """Turn a perfect maze into a non-perfect one (PERFECT=False).

        Each dead-end gets one more opening, trying first the neighbours
        that are dead-ends too. An opening that creates a 3x3 open area is
        undone. If fewer than 2 loops remain, extra walls are opened with
        the same check. Uses the seeded generator, so the result is
        reproducible. Some dead-ends may remain if no opening is possible.
        """

        for row in range(len(self.grid)):
            for col in range(len(self.grid[row])):
                current = (row, col)
                if self.is_deadend(current):
                    braid_nghb = self.get_braid_neighbors(row, col)
                    self.randgen.shuffle(braid_nghb)
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

        loops = self.count_loops()
        if loops < 2:
            for row in range(len(self.grid)):
                for col in range(len(self.grid[row])):
                    current = (row, col)
                    loop_nghbrs = self.get_braid_neighbors(row, col)
                    self.randgen.shuffle(loop_nghbrs)
                    for chosen in loop_nghbrs:
                        self.remove_walls(current, chosen)
                        if self.verify_open_areas(current):
                            self.add_walls_back(current, chosen)
                        else:
                            loops += 1
                            break
                    if loops >= 2:
                        return

    def get_path_nghb(self, active: tuple[int, int]) -> list[tuple[int, int]]:
        """List the cells reachable from a cell during the BFS.

        Args:
            active: cell as (row, col).

        Returns:
            The neighbours separated by an open wall that are not part of
            the "42" pattern and have not been discovered yet.
        """
        row, col = active
        path_nghb = []

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

        if (top is not None
                and top not in self.fortytwo_cells
                and top not in self.path_parents
                and (self.grid[row][col] & self.NORTH) == 0):
            path_nghb.append(top)

        if (right is not None
                and right not in self.fortytwo_cells
                and right not in self.path_parents
                and (self.grid[row][col] & self.EAST) == 0):
            path_nghb.append(right)

        if (bottom is not None
                and bottom not in self.fortytwo_cells
                and bottom not in self.path_parents
                and (self.grid[row][col] & self.SOUTH) == 0):
            path_nghb.append(bottom)

        if (left is not None
                and left not in self.fortytwo_cells
                and left not in self.path_parents
                and (self.grid[row][col] & self.WEST) == 0):
            path_nghb.append(left)

        return path_nghb

    @staticmethod
    def find_direction(
            active: tuple[int, int], parent: tuple[int, int]) -> str:
        """Return the letter of the step from a parent cell to a cell.

        Args:
            active: cell reached, as (row, col).
            parent: cell it was reached from, as (row, col).

        Returns:
            "N", "E", "S" or "W".

        Raises:
            Value Error if the two cells are not neighbors.
        """
        row = parent[0] - active[0]
        col = parent[1] - active[1]
        if (row, col) == (1, 0):
            return "N"
        if (row, col) == (-1, 0):
            return "S"
        if (row, col) == (0, 1):
            return "W"
        if (row, col) == (0, -1):
            return "E"
        raise ValueError(
            f"Error: Can't find direction in path for {active} and {parent}")

    def solve_maze_bfs(self) -> None:
        """Find the shortest path from entry to exit with a BFS.

        Each discovered cell stores its parent in self.path_parents. The
        path is rebuilt from the exit to the entry and stored in self.path.

        Raises:
            ValueError: if the exit cannot be reached.
        """
        queue = []

        queue.append(self.entry_conv_yx)
        while queue:
            active = queue.pop(0)
            if active == self.exit_conv_yx:
                break
            path_nghb = self.get_path_nghb(active)
            for neighbor in path_nghb:
                self.path_parents[neighbor] = active
                queue.append(neighbor)

        if self.exit_conv_yx not in self.path_parents:
            raise ValueError("Exit value not reachable")

        find_path = self.exit_conv_yx
        while find_path != self.entry_conv_yx:
            parent = self.path_parents[find_path]
            direction = self.find_direction(find_path, parent)
            self.path.append(direction)
            find_path = parent

        self.path.reverse()
        if len(self.path) == 0:
            raise ValueError("Can't find shortest path")

    def reset_state(self) -> None:
        """Reset the state of a generation.

        Empties the grid, visited cells, stack, "42" cells and path. The
        parameters and the random generator are not changed.
        """
        self.grid: list[list[int]] = []
        self.visited: set[tuple[int, int]] = set()
        self.stack: list[tuple[int, int]] = []
        self.fortytwo_cells = []
        self.path_parents: dict[tuple[int, int], tuple[int, int]] = {
            self.entry_conv_yx: self.entry_conv_yx
            }
        self.path: list[str] = []

    def generate(self) -> None:
        """Generate the maze and its shortest path.

        Resets the state, draws the "42" pattern if it fits, carves the maze
        with a DFS, braids it if perfect is False and solves it with a BFS.
        Calling it again on the same object gives a new maze, because the
        random generator keeps advancing; self.seed keeps the initial seed.

        Raises:
            ValueError: if the entry or exit fall inside the "42" pattern,
                or if the exit cannot be reached.
        """
        self.reset_state()
        self.setupgrid()
        if len(self.grid) == 0:
            raise ValueError("Invalid Data: Grid Empty")

        self.fortytwo()
        if self.entry_conv_yx in self.fortytwo_cells:
            raise ValueError(
                "Error: entry is unreachable - falls inside 42 design")
        if self.exit_conv_yx in self.fortytwo_cells:
            raise ValueError(
                "Error: exit is unreachable - falls inside 42 design")

        self.dfs()

        if self.perfect is False:
            self.braiding_maze()

        self.solve_maze_bfs()

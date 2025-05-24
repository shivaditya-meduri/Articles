# Python code to solve linkedin zip puzzles
import copy
def findStartEndCells(grid):
    # find and return the start and the end cells locations
    height, width = len(grid), len(grid[0])
    minCell = 1
    maxCell = -float('inf')
    for hi in range(height):
        for wi in range(width):
            if grid[hi][wi] is not None:
                if grid[hi][wi] == minCell:
                    startLoc = (hi, wi)
                elif grid[hi][wi] > maxCell:
                    maxCell = grid[hi][wi]
                    endLoc = (hi, wi)
    return startLoc, endLoc
def zipSolver(grid, barriers):
    # solve zip puzzles using backtracking
    startLoc, endLoc = findStartEndCells(grid)
    print("Input grid: ")
    pretty_print(grid, barriers)
    print(f"Starting cell location : {startLoc} | Ending cell location : {endLoc}")
    height, width = len(grid), len(grid[0])
    num_cells = height*width
    paths = []
    def dfsBackTrack(currNum, currPos, currPath):
        if currPos == endLoc:
            if len(currPath) == num_cells:
                paths.append(currPath.copy())
                return
        for diff_h, diff_w in [[0,-1],[0,1],[1,0],[-1,0]]:
            newPos = (currPos[0]+diff_h, currPos[1]+diff_w)
            if newPos in currPath:
                continue
            if 0<=newPos[0]<height and 0<=newPos[1]<width:
                if {currPos, newPos} not in barriers:
                    if grid[newPos[0]][newPos[1]] is not None:
                        if grid[newPos[0]][newPos[1]] == currNum+1:
                            dfsBackTrack(currNum+1, newPos, currPath+[newPos])
                    else:
                        dfsBackTrack(currNum, newPos, currPath+[newPos])
    dfsBackTrack(1, startLoc, [startLoc])
    if len(paths) == 1:
        print("Only 1 path exists!")
        print("Path: ", paths[0])
    # Visualize the path
    grid_copy = copy.deepcopy(grid)
    for ind, pos in enumerate(paths[0]):
        grid_copy[pos[0]][pos[1]] = ind+1
    print("Solved grid:")
    pretty_print(grid_copy, barriers)
    return
def pretty_print(grid, barrier_bricks=None):
    # Pretty print the grid
    n, m = len(grid), len(grid[0])
    barrier_bricks = barrier_bricks or []
    vert = set()
    horz = set()
    for brick in barrier_bricks:
        (r1,c1),(r2,c2) = brick
        if r1 == r2 and abs(c1-c2) == 1:
            vert.add((r1, min(c1,c2)))
        elif c1 == c2 and abs(r1-r2) == 1:
            horz.add((min(r1,r2), c1))
        else:
            raise ValueError(f"Bad barrier: {brick}")
    w = max((len(str(x)) for row in grid for x in row if x is not None), default=1)
    for r in range(n):
        line = "+"
        for c in range(m):
            seg = "X"*(w+2) if (r-1, c) in horz else "-"*(w+2)
            line += seg + "+"
        print(line)
        row_str = "|"
        for c, cell in enumerate(grid[r]):
            s = str(cell) if cell is not None else ""
            row_str += f" {s.rjust(w)} "
            row_str += "X" if (r, c) in vert else "|"
        print(row_str)
    line = "+" + "+".join("-"*(w+2) for _ in range(m)) + "+"
    print(line)

# test case without barriers
zipArray = [
    [None, None,  8,  4, None, None],
    [None,    7, None, None,   5, None],
    [   9, None, None, None, None,   3],
    [None, None,   6,   2, None, None],
    [None,    1, None, None,  11, None],
    [  10, None, None, None, None,  12],
]
barrier_bricks = []
zipSolver(zipArray, barrier_bricks)



# test case with barriers
zipArray = [
    [ 9, None, None, None, None, None,  8],
    [None,    3, None, None, None,   5, None],
    [None, None, None, None, None, None, None],
    [None, None, None,    1, None, None, None],
    [None, None, None, None, None, None, None],
    [None,    2, None, None, None,   6, None],
    [ 4, None, None, None, None, None,  7],
]
barrier_bricks = [
    {(1, 2), (1, 3)},
    {(1, 3), (1, 4)},
    {(3, 0), (3, 1)},
    {(3, 1), (3, 2)},
    {(3, 4), (3, 5)},
    {(3, 5), (3, 6)},
    {(5, 2), (5, 3)},
    {(5, 3), (5, 4)},
]
zipSolver(zipArray, barrier_bricks)

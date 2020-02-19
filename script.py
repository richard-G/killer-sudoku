# script that will generate completed sudoku puzzles with a unique solution.
# could also be done in object oriented, with grid being a parent object to rows, columns, squares

import numpy as np

# initialize empty board, to test we can build this as a sudoku solver (import a grid known to have a unique solution)
# grid = [[0 for i in range(10)] for j in range(10)]

grid = np.array([
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9]
])


# function to display the grid
def display_grid():
    global grid
    for row in grid:
        print(row)


# returns true if a given number is allowed at a given position, on the global grid
# position entered as a 2-tuple, (row, column)
def is_valid(number, position):
    global grid
    row_index, col = position

    # check row
    if number in grid[row_index]:
        return False

    # check column
    for row in grid:
        if row[col] == number:
            return False

    # check this
    # if number in grid[:][col]:
    #     return False

    # # get subgrid coords
    # for i in range(0, 12, 3):
    #     if row_index < i:
    #         for j in range(0, 12, 3):
    #             if col < j:
    #                 subgrid_i, subgrid_j = (i//3, j//3)
    #
    # # check subgrid
    # for i in range(subgrid_i * 3, subgrid_i + 3):
    #     for j in range(subgrid_j * 3, subgrid_j + 3):
    #         if grid[i][j] == number:
    #             return False

    i0 = (row_index // 3) * 3
    j0 = (col // 3) * 3

    for i in range(0, 3):
        for j in range(0, 3):
            if grid[i0 + i][j0 + j] == number:
                return False

    # could clean up subgrid mixing the above 2, low row_index // 3 perhaps?

    return True


# recursive function to be called to solve the puzzle.
def solve_puzzle():
    global grid
    for i in range(9):
        for j in range(9):
            if grid[i][j] == 0:
                for number in range(1, 10):
                    if is_valid(number, (i, j)):
                        grid[i][j] = number
                        solve_puzzle()
                        grid[i][j] = 0
                return


    print('end of program.. solved puzzle:')
    display_grid()


display_grid()
solve_puzzle()




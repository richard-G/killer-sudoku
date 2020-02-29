# used to solve killer sudoku puzzles through brute force
# input puzzles will be valid, this will determine if they have unique solutions

import numpy as np
import pickle
import sys

try:
    with open('initialised_ks_puzzles.pickle', 'rb') as file:
        cage_layouts = pickle.load(file)
except FileNotFoundError:
    print('couldn\'t find grids to load')
    print('ending process...')
    sys.exit()


# temp, in future will iterate over each layout
cage_layout = cage_layouts[0]

key_grid = [[0 for i in range(9)] for j in range(9)]
sum_grid = [[0 for i in range(9)] for j in range(9)]
value_grid = [[0 for i in range(9)] for j in range(9)]


def reconstruct_layout(cages_dict):
    global key_grid, sum_grid, value_grid
    for cage in cages_dict.values():
        for cell in cage.elements:
            cell.value = 0
            i, j = cell.position

            key_grid[i][j] = cage.key
            sum_grid[i][j] = cage.total
            value_grid[i][j] = cell.value

    print('key grid...')
    display_grid(key_grid)
    print('sum grid...')
    display_grid(sum_grid)
    print('value grid...')
    display_grid(value_grid)


def display_grid(grid):
    for row in grid:
        print(row)

    print('-' * 20)


reconstruct_layout(cage_layout)


# # returns true if a given number is allowed at a given position, on the global grid
def is_valid(number, cell):
    # global grid
    row_index, col = cell.position

    # check row
    if number in value_grid[row_index]:
        return False

    # check column
    for row in value_grid:
        if row[col] == number:
            return False

    # check subgrid
    i0 = (row_index // 3) * 3
    j0 = (col // 3) * 3
    for i in range(0, 3):
        for j in range(0, 3):
            if value_grid[i0 + i][j0 + j] == number:
                return False

    # check cage duplicates
    cage = cell.get_cage()
    for other_cell in cage.elements:
        if number == other_cell.value:
            return False

    # check cage total




    return True
#
#
# # recursive function to be called to solve the puzzle.
# def solve_puzzle():
#     # global grid
#     for i in range(9):
#         for j in range(9):
#             if grid[i][j] == 0:
#                 for number in range(1, 10):
#                     if is_valid(number, (i, j)):
#                         grid[i][j] = number
#                         solve_puzzle()
#                         grid[i][j] = 0
#                 return
#
#     print('end of program.. solved puzzle:')
#     display_grid()
#
#
# display_grid()
# solve_puzzle()
#

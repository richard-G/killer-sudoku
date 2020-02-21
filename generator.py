# script that will generate completed sudoku board states stochastically

import numpy as np
from random import sample
from os import sys
import itertools

# initialize empty board, to test we can build this as a sudoku solver (import a grid known to have a unique solution)


# function to display the grid
def display_grid(solved_grid):
    for i, row in enumerate(solved_grid):
        print(row)

    print('-'*20)


# returns true if a given number is allowed at a given position, on the global grid
# position entered as a 2-tuple, (row, column)
def is_valid(number, position, input_grid):
    row_index, col = position

    # check row
    if number in input_grid[row_index]:
        return False

    # check column
    for row in input_grid:
        if row[col] == number:
            return False

    i0 = (row_index // 3) * 3
    j0 = (col // 3) * 3

    for i in range(0, 3):
        for j in range(0, 3):
            if input_grid[i0 + i][j0 + j] == number:
                return False

    return True


# global iteration, seed, grid
# recursive function to be called to solve the puzzle.
def solve_puzzle(init=False):
    global seed, grid, iteration
    if init:
        i_range = sample(list(range(0, 9)), k=9)
        j_range = sample(list(range(0, 9)), k=9)
        seed = (i_range, j_range)

        grid = np.array([[0 for i in range(9)] for j in range(9)])
        # grid = np.array([
        #     [0, 0, 0, 0, 0, 0, 0, 0, 0],
        #     [0, 0, 6, 0, 0, 0, 0, 7, 2],
        #     [0, 0, 8, 0, 0, 0, 6, 0, 0],
        #     [1, 0, 5, 0, 0, 8, 0, 0, 0],
        #     [0, 2, 0, 0, 5, 0, 0, 3, 0],
        #     [0, 0, 3, 0, 0, 0, 0, 0, 0],
        #     [0, 0, 0, 0, 0, 0, 0, 0, 0],
        #     [0, 0, 4, 0, 0, 7, 0, 0, 8],
        #     [0, 0, 2, 0, 0, 0, 0, 0, 4]
        # ])
        # grid = np.array([
        #     [5, 3, 0, 0, 7, 0, 0, 0, 0],
        #     [6, 0, 0, 1, 9, 5, 0, 0, 0],
        #     [0, 9, 8, 0, 0, 0, 0, 6, 0],
        #     [8, 0, 0, 0, 6, 0, 0, 0, 3],
        #     [4, 0, 0, 8, 0, 3, 0, 0, 1],
        #     [7, 0, 0, 0, 2, 0, 0, 0, 6],
        #     [0, 6, 0, 0, 0, 0, 2, 8, 0],
        #     [0, 0, 0, 4, 1, 9, 0, 0, 5],
        #     [0, 0, 0, 0, 8, 0, 0, 7, 9]
        # ])

    i_range, j_range = seed
    # for i in i_range:
    #     for j in j_range:
    for i, j in itertools.product(i_range, j_range):
        if grid[i][j] == 0:
            for number in range(1, 10):
                if is_valid(number, (i, j), grid):
                    grid[i][j] = number
                    solve_puzzle()
                    # print(i_range.index(i), i)
                    grid[i][j] = 0
            return

    global total
    print(f'puzzle {total - iteration} generated!')
    display_grid(grid)
    iteration -= 1

    # quite messy, find another way? should really be handled in parent function but can't figure out how to break
    # out of stack
    if iteration == 0:
        sys.exit()
    solve_puzzle(init=True)


grid = []
seed = []
iteration = []
total = 0


# global iteration
# where hyper-parameters SHOULD BE declared - counter, initial random seeds
def main():
    while True:
        try:
            global iteration
            global total
            iteration = int(input('how many puzzles?: '))
            total = iteration + 1
        except ValueError:
            print('enter a number...')
        else:
            break

    solve_puzzle(init=True)


# call
main()

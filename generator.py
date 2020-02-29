# script that will generate completed sudoku board states stochastically

import numpy as np
from random import sample
from os import sys
import itertools
import signal
import pickle


def handler(signum, frame):
    print(f'handler called! {signum}...{frame}')
    solve_puzzle(init=True)

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

    # check subgrid
    i0 = (row_index // 3) * 3
    j0 = (col // 3) * 3
    for i in range(0, 3):
        for j in range(0, 3):
            if input_grid[i0 + i][j0 + j] == number:
                return False

    return True

is_done = False
failed = False


# global iteration, seed, grid
# recursive function to be called to solve the puzzle.
def solve_puzzle(init=False):
    # print('reset!')
    global is_done
    global failed
    global solved
    # if is_done and not init:
    #     print('returned!')
    #     return
    global seed, grid
    if failed:
        return
    if init:
        is_done = False
        failed = False
        # print(f'in here...')
        i_range = sample(list(range(0, 9)), k=9)
        j_range = sample(list(range(0, 9)), k=9)
        seed = (i_range, j_range)

        grid = np.array([[0 for i in range(9)] for j in range(9)])

        def handle(signum, frame):
            # print(f'handle called at {signum}..{frame}')
            global failed
            failed = True
            signal.signal(signal.SIGALRM, handle)
            signal.setitimer(signal.ITIMER_REAL, 0.3)
            solve_puzzle(init=True)

        # add timeout here, if not met just call again
        signal.signal(signal.SIGALRM, handle)
        signal.setitimer(signal.ITIMER_REAL, 0.3)

    for i, j in itertools.product(*seed):
        if grid[i][j] == 0:
            for number in range(1, 10):
                if is_valid(number, (i, j), grid):
                    grid[i][j] = number
                    solve_puzzle()
                    if is_done:
                        return
                    # print(i_range.index(i), i)
                    grid[i][j] = 0
            return

    solved += 1
    print(f'puzzle {solved} generated! (iteration {counter})')
    grids.append(grid)
    display_grid(grid)
    is_done = True
    signal.alarm(0)


grid = []
seed = []
iteration = []
total = 0
counter = 1
# output
solved = 0
grids = []


def save_grids():
    with open('s_puzzles.pickle', 'wb') as file:
        pickle.dump(grids, file)
        print('data saved!')


# global iteration
# where hyper-parameters SHOULD BE declared - counter, initial random seeds
def main():
    while True:
        try:
            global iteration
            global total
            global counter
            global failed
            runs = int(input('how many puzzles?: ')) + 1
        except ValueError:
            print('enter a number...')
        else:
            break

    while counter != runs:
        failed = False
        solve_puzzle(init=True)
        counter += 1
        # print('out here...')

    # save functionality
    user_input = input('save output? [y/n]')
    while user_input not in ['y', 'n']:
        user_input = input('save output? [y/n]: ')
    if user_input == 'y':
        save_grids()
    else:
        print('output not saved...')

    print('ending process...')


# call
main()




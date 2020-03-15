# will take as input a completed sudoku grids and cage layouts
# will check through grids and layouts and iterate, outputting valid killer sudoku grids

import pickle
import sys
from cage_builder import Cell, Cage
from random import sample

# import data
# grids :: [[]], cage_layouts :: [{}]
try:
    with open('s_puzzles.pickle', 'rb') as handle:
        grids = pickle.load(handle)
except FileNotFoundError:
    print('couldn\'t find grids to load')
    print('ending process...')
    sys.exit()

try:
    with open('cage_layouts.pickle', 'rb') as handle:
        cage_layouts = pickle.load(handle)
except FileNotFoundError:
    print('couldn\'t find cage layouts to load')
    print('ending process...')
    sys.exit()

# output puzzles, list of 2-tuples - (grid, cage_layout)
# ks_puzzles :: [ ([[]], {}) ]
ks_puzzles = []


# all validator needs to do here is ensure cages conform to cage rules, assume it will be passed valid sudoku puzzles
def is_valid(grid, cage_layout):
    # returns true if grid and cage_layout work together
    for cage in cage_layout.values():
        # used numbers in the current cage, returns false if there's ever a duplicate
        numbers = []
        for cell in cage.elements:
            i, j = cell.position
            number = grid[i][j]
            if number in numbers:
                print(f'duplicate found in cage {cage}, number {number} already in {numbers}')
                return False
            else:
                numbers.append(number)

    return True


# main
def generate_ks():
    global grids, cage_layouts
    valids = 0
    invalids = 0

    # iterate through grids and cage_layouts, when a working puzzle is found, move to next grid.
    for grid in grids:
        # here we should shuffle cage_layouts, and create magnitudes more
        for cage_layout in sample(cage_layouts, k=len(cage_layouts)):

            if is_valid(grid, cage_layout):
                print('valid puzzle found!')
                ks_puzzles.append((grid, cage_layout))
                valids += 1
                break
            else:
                print('puzzle not valid!')
                invalids += 1
                continue

    print(f'total valid: {valids}. total invalid: {invalids}')


initialised_ks_puzzles = []


# initialises empty ks puzzles by getting each number from the completed grid and calculating the .total of each cage
# returns the cages dict with the total attribute for each cage
def initialise_puzzles():
    for grid, cage_layout in ks_puzzles:
        for cage in cage_layout.values():
            cage.total = 0
            for cell in cage:
                i, j = cell.position
                cage.total += grid[i][j]

            # print(f'total for cage {cage}... {cage.total}')

        initialised_ks_puzzles.append(cage_layout)

    user_input = input('save output? [y/n]: ')
    while user_input not in ['y', 'n']:
        user_input = input('save output? [y/n]: ')

    if user_input == 'y':
        save_output()
    else:
        print('output not saved...')


def save_output():
    with open('initialised_ks_puzzles.pickle', 'wb') as file:
        pickle.dump(initialised_ks_puzzles, file)
        print('data saved!')
        print(f'puzzles stored: {len(initialised_ks_puzzles)}')


def display_grid(grid):
    for row in grid:
        print(row)

    print('-' * 20)


def reconstruct_layout(cages_dict):
    new_grid = [[0 for i in range(9)] for j in range(9)]
    for cage in cages_dict.values():
        for cell in cage.elements:
            # print(f'{cage.key}: {cell.position}')
            i, j = cell.position
            new_grid[i][j] = cage.key

    display_grid(new_grid)


if __name__ == '__main__':
    generate_ks()
    initialise_puzzles()

    gen_grid, gen_layout = ks_puzzles[0]
    display_grid(gen_grid)
    reconstruct_layout(gen_layout)

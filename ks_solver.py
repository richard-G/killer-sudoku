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
cages_untouched = [cage for cage in cage_layout.values()]

cages = cages_untouched.copy()
print(cages)


def display_value_keys(cages):
    grid = [[0 for i in range(9)] for j in range(9)]
    grid2 = [[0 for i in range(9)] for j in range(9)]
    for cage in cages:
        for cell in cage:
            i, j = cell.position
            grid[i][j] = cage.key
            grid2[i][j] = cage.total

    print('displaying cage keys...')
    for row in grid:
        print(row)

    print('\n')
    print('displaying cage values')
    for row in grid2:
        print(row)


def display_grid(grid):
    for row in grid:
        print(row)

    print('-' * 20)


# # returns true if a given number is allowed at a given position, on the global grid
def is_valid(number, cell, cage):
    global cages
    row, col = cell.position

    val_grid = reconstruct_layout(cages, att="value")
    # display_grid(val_grid)

    # # check row
    if number in val_grid[row]:
        print(f'{number} denied! (row)')
        return False
    # if number in row_values:
    #     print('col denied')
    #     return False

    # check column
    for grid_row in val_grid:
        if grid_row[col] == number:
            print(f'{number} denied! (column)')
            return False

    # check subgrid
    i0 = (row // 3) * 3
    j0 = (col // 3) * 3
    for i in range(0, 3):
        for j in range(0, 3):
            if val_grid[i0 + i][j0 + j] == number:
                return False

    # check cage duplicates
    for other_cell in cage:
        if number == other_cell.value:
            return False

    # check cage total
    if cage.current_sum() + number > cage.total:
        print(f'{number} denied! ({cage.current_sum() + number} over total - {cage.total})')
        return False

    # advanced cage check
    unset_cells = [element for element in cage.elements if element.value == 0]
    if len(unset_cells) == 1:
        if cage.current_sum() + number != cage.total:
            print(f'{number} denied! {cage.current_sum()} + {number} is not {cage.total}')
            return False
        else:
            print(f'that\'s a bingo! {cage.current_sum()} + {number} is {cage.total}!')

    return True


solutions = []

# sort cages by length, should improve efficiency...
cages.sort(key=lambda x: len(x))
for cage in cages:
    print(len(cage))

# reconstruct_layout(cages)


def solve_puzzle():
    global solutions
    global cages

    for cage in cages:
        for cell in cage:
            if cell.value == 0:
                for number in range(1, 10):
                    if is_valid(number, cell, cage):
                        cell.value = number
                        display_finished(cages)
                        print(f'{number} at {cell.position}')
                        solve_puzzle()
                        cell.value = 0
                return

        # print('next cage!')

    print('solved puzzle...')
    if not solutions or cages not in solutions:
        solutions.append(cages)
        print('new solution found!')
        display_finished(cages)

        print('sudoku puzzle: ')
        display_grid(reconstruct_layout(cages_untouched))

        display_value_keys(cages_untouched)


        print(len(solutions))
        sys.exit()  # temp
    else:
        print('duplicate found!')
        display_finished(cages)
        print(len(solutions))


def reconstruct_layout(cages, att='value'):
    sample = [[0 for i in range(9)] for j in range(9)]
    for cage in cages:
        # print('cage:', cage)
        for cell in cage:
            i, j = cell.position
            sample[i][j] = getattr(cell, att)

    # display_grid(sample)
    return sample


def display_finished(cages):
    sample = reconstruct_layout(cages, "value")

    # print('displaying finished puzzle...')
    display_grid(sample)


if __name__ == '__main__':
    # display_grid(value_grid)
    solve_puzzle()

    print('end of program...')
    print(f'number of solutions: {len(solutions)}')
    for solution in solutions:
        display_finished(solution)

    print('sudoku puzzle: ')
    reconstruct_layout(cages_untouched)

    # print(cage_layout)




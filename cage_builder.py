# stochastically generates cage layouts that can later be overlayed onto sudoku puzzles
# layouts should either be symmetrical on the x-axis, y-axis, diagonal, or rotated
# cages should never contain only 1 element, if so, should merge onto existing cage

import random
import itertools
import pickle

cage_layouts = []
cages = {}


class Cell:
    def __init__(self, position):
        self.position = position
        self.value = 0

    def get_neighbours(self):
        i, j = self.position

        possible_coords = []
        if i != 0:
            possible_coords.append((i - 1, j))
        if i != 8:
            possible_coords.append((i + 1, j))
        if j != 0:
            possible_coords.append((i, j - 1))
        if j != 8:
            possible_coords.append((i, j + 1))

        cells = []

        for coords in possible_coords:
            cells.append(Cell.get_cell(coords))

        return cells

    def __repr__(self):
        if self.get_cage():
            return str(self.get_cage())
        else:
            return 'na'

    # returns key of cage if exists, else False
    # probably will be chained as in for neighbour in Cell.get_neighbours: neighbour.get_cage
    def get_cage(self):
        for key, cells in cages.items():
            # might throw an error here, try self.position == cell.position otherwise
            if self in cells.elements:
                return key

        return False

    @staticmethod
    def get_cell(position):
        global grid
        for row in grid:
            for cell in row:
                if cell.position == position:
                    return cell


class Cage:
    def __init__(self, key, elements):
        self.key = key
        self.elements = []
        self.elements.append(elements)
        self.total = 0

    def __len__(self):
        return len(self.elements)

    def __iter__(self):
        yield from self.elements

    def __repr__(self):
        return f'{self.key} - elements: {self.elements}'

    def add_cell(self, cell):
        self.elements.append(cell)

    def current_sum(self):
        accumulator = 0
        for cell in self.elements:
            accumulator += cell.value

        return accumulator

    # only way to create a new cage, makes a new key in dictionary and takes a cell on init.
    @classmethod
    def add(cls, cell):
        key = 10
        while key in cages.keys():
            key += 1

        # print(f'new cage - key {key}')

        cages[key] = cls(key, cell)


# function to display the grid
def display_grid():
    global grid
    for row in grid:
        print(row)

    print('-' * 20)


# initialise grid
grid = [[Cell((i, j)) for i in range(9)] for j in range(9)]


def generate_cage_layout():
    global iterations, total

    # randomise cell order that will be looped through
    i_range = random.sample(list(range(0, 9)), k=9)
    j_range = random.sample(list(range(0, 9)), k=9)

    big_set = [(i, j) for (i, j) in itertools.product(i_range, j_range)]
    shuffled = random.sample(big_set, k=len(big_set))

    # main logic
    for row, col in shuffled:
        cell = grid[row][col]
        neighbours = cell.get_neighbours()
        neighbour_cages = [neighbour.get_cage() for neighbour in neighbours if neighbour.get_cage()]
        filtered = [ele for ele in neighbour_cages if len(cages[ele]) < 4]
        priority = [ele for ele in neighbour_cages if len(cages[ele]) == 1]
        # if no current neighbouring cages, always create new cages
        if not filtered:
            Cage.add(cell)
            # print(f'no neighbouring cages found for cell {cell.position}')
        elif priority:
            # print(f'priority neighbours found for {cell.position}: {priority}')
            cages[random.choice(priority)].add_cell(cell)
        elif len(neighbour_cages) == 4:
            # print(f'4 neighbouring cages found for {cell.position}: {neighbour_cages}')
            cages[random.choice(neighbour_cages)].add_cell(cell)
        else:  # if neighbouring, have some probability of merging, else create new
            if random.random() > 0.2:
                cages[random.choice(filtered)].add_cell(cell)
                # print('above')
            else:
                Cage.add(cell)
                # print('below')

    if no_lone_cells(cages.values()):
        print('cage layout accepted!')
        for cage in cages.values():
            print(len(cage), '---', cage.elements)
        print(f'cage layout {total - iterations} generated!')
        display_grid()
        cage_layouts.append(cages)


def no_lone_cells(cages):
    for cage in cages:
        if len(cage) == 1:
            print('cage layout rejected!')
            print(cage.key)
            print(cage.elements)
            display_grid()
            return False

    return True


iterations = 0
total = 0


def main():
    while True:
        try:
            global iterations
            iterations = int(input('how many layouts?: '))
            global total
            total = iterations + 1
        except ValueError:
            print('enter a number...')
        else:
            break

    while len(cage_layouts) < iterations:
        generate_cage_layout()
        global cages
        cages = {}
        total += 1

    print(f'{len(cage_layouts)} layouts found!')

    user_input = input('save output? [y/n]: ')
    while user_input not in ['y', 'n']:
        user_input = input('save output? [y/n]: ')

    if user_input == 'y':
        save_output()
    else:
        print('output not saved...')

    print('ending process...')


def save_output():
    # for cage_layout in cage_layouts:
    #     reconstruct_layout(cage_layout)
    with open('cage_layouts.pickle', 'wb') as handle:
        pickle.dump(cage_layouts, handle)

        print('data saved!')


# def reconstruct_layout(cages_dict):
#     new_grid = [[0 for i in range(9)] for j in range(9)]
#     for cage in cages_dict.values():
#         for cell in cage.elements:
#             # print(f'{cage.key}: {cell.position}')
#             i, j = cell.position
#             new_grid[i][j] = cage.key
#
#     display_grid(new_grid)


if __name__ == '__main__':
    main()


# TODO: ensure no single cages are created
# TODO: work on symmetry
# TODO: set avg cage size as a hyperparameter

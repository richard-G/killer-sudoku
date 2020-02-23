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

    def __len__(self):
        return len(self.elements)

    def __iter__(self):
        yield self.elements

    def add_cell(self, cell):
        self.elements.append(cell)

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
    global iterations

    # randomise order that will be looped through
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
            # print(f'neighbour cages found for {cell.position}: {neighbour_cages}')
            # Cage.add(cell)
            # for now, 50% chance, in future do amount of neighbouring cages / total neighbours
            # look into random.choices()
            # need additional weighting to penalise high element lengths - this can be used to determine difficulty too
            # print(f'none of previous conditions met for {cell.position}: {neighbour_cages}... deciding randomly')
            if random.random() > 0.2:
                cages[random.choice(filtered)].add_cell(cell)
                # print('above')
            else:
                Cage.add(cell)
                # print('below')

    print(f'cage layout {total - iterations} generated!')
    display_grid()

    cage_layouts.append(cages)

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

    for i in range(iterations):
        generate_cage_layout()
        global cages
        cages = {}
        total += 1


if __name__ == '__main__':
    main()


# with open('cage_layouts.pickle', 'wb') as handle:
#     pickle.dump(cage_layouts, handle)
#
#     print('data saved!')


# TODO: ensure no single cages are created
# TODO: work on symmetry
# TODO: set avg cage size as a hyperparameter

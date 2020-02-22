# stochastically generates subgrid layouts that can later be overlayed onto sudoku puzzles
# layouts should either be symmetrical on the x-axis, y-axis, diagonal, or rotated
# subgrid should never contain only 1 element, if so, should merge onto existing subgrid

import random
import itertools

subgrids = {}





class Square:
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

        squares = []

        for coords in possible_coords:
            squares.append(Square.get_square(coords))

        return squares

    def __repr__(self):
        if self.get_subgrid():
            return str(self.get_subgrid())
        else:
            return 'na'

    # returns key of subgrid if exists, else False
    # probably will be chained as in for neighbour in Square.get_neighbours: neighbour.get_subgrid
    def get_subgrid(self):
        for key, squares in subgrids.items():
            # might throw an error here, try self.position == square.position otherwise
            if self in squares.elements:
                return key

        return False

    @staticmethod
    def get_square(position):
        global grid
        for row in grid:
            for square in row:
                if square.position == position:
                    return square


class SubGrid:
    def __init__(self, key, elements):
        self.key = key
        self.elements = []
        self.elements.append(elements)

    def __len__(self):
        return len(self.elements)

    def __iter__(self):
        yield self.elements

    def add_square(self, square):
        self.elements.append(square)

    # only way to create a new subgrid, makes a new key in dictionary and takes a square on init.
    @classmethod
    def new(cls, square):
        key = 10
        while key in subgrids.keys():
            key += 1

        print(f'new subgrid - key {key}')

        subgrids[key] = cls(key, square)


# function to display the grid
def display_grid():
    global grid
    for row in grid:
        print(row)


# initialise grid
grid = [[Square((i, j)) for i in range(9)] for j in range(9)]


# randomise order that will be looped through
i_range = random.sample(list(range(0, 9)), k=9)
j_range = random.sample(list(range(0, 9)), k=9)

big_set = [(i, j) for (i, j) in itertools.product(i_range, j_range)]
shuffled = random.sample(big_set, k=len(big_set))


# main logic
for row, col in shuffled:
    square = grid[row][col]
    neighbours = square.get_neighbours()
    neighbour_subgrids = [neighbour.get_subgrid() for neighbour in neighbours if neighbour.get_subgrid()]
    filtered = [ele for ele in neighbour_subgrids if len(subgrids[ele]) < 4]
    priority = [ele for ele in neighbour_subgrids if len(subgrids[ele]) == 1]
    # if no current neighbouring subgrids, always create new subgrid
    if not filtered:
        SubGrid.new(square)
        print(f'no neighbouring subgrids found for {square}')
    elif priority:
        subgrids[random.choice(priority)].add_square(square)
    else:  # if neighbouring, have some probability of merging, else create new
        print(f'neighbour grids found for {square}: {neighbour_subgrids}')
        # SubGrid.new(square)
        # for now, 50% chance, in future do amount of neighbouring subgrids / total neighbours
        # look into random.choices()
        # need additional weighting to penalise high element lengths - this can be used to determine difficulty too
        if random.random() > 0.2:
            subgrids[random.choice(filtered)].add_square(square)
            print('above')
        else:
            SubGrid.new(square)
            print('below')






display_grid()


# TODO: ensure no single subgrids are created
# TODO: work on symmetry
# TODO: set avg subgrid size as a hyperparameter
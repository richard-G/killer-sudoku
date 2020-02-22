# stochastically generates cage layouts that can later be overlayed onto sudoku puzzles
# layouts should either be symmetrical on the x-axis, y-axis, diagonal, or rotated
# cages should never contain only 1 element, if so, should merge onto existing cage

import random
import itertools

cages = {}


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
        if self.get_cage():
            return str(self.get_cage())
        else:
            return 'na'

    # returns key of cage if exists, else False
    # probably will be chained as in for neighbour in Square.get_neighbours: neighbour.get_cage
    def get_cage(self):
        for key, squares in cages.items():
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


class Cage:
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

    # only way to create a new cage, makes a new key in dictionary and takes a square on init.
    @classmethod
    def new(cls, square):
        key = 10
        while key in cages.keys():
            key += 1

        print(f'new cage - key {key}')

        cages[key] = cls(key, square)


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
    neighbour_cages = [neighbour.get_cage() for neighbour in neighbours if neighbour.get_cage()]
    filtered = [ele for ele in neighbour_cages if len(cages[ele]) < 4]
    priority = [ele for ele in neighbour_cages if len(cages[ele]) == 1]
    # if no current neighbouring cages, always create new cages
    if not filtered:
        Cage.new(square)
        print(f'no neighbouring cages found for {square}')
    elif priority:
        cages[random.choice(priority)].add_square(square)
    else:  # if neighbouring, have some probability of merging, else create new
        print(f'neighbour cages found for {square}: {neighbour_cages}')
        # Cage.new(square)
        # for now, 50% chance, in future do amount of neighbouring cages / total neighbours
        # look into random.choices()
        # need additional weighting to penalise high element lengths - this can be used to determine difficulty too
        if random.random() > 0.2:
            cages[random.choice(filtered)].add_square(square)
            print('above')
        else:
            Cage.new(square)
            print('below')






display_grid()


# TODO: ensure no single cages are created
# TODO: work on symmetry
# TODO: set avg cage size as a hyperparameter
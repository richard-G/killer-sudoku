# script that will generate completed sudoku puzzles with a unique solution.
# could also be done in object oriented, with grid being a parent object to rows, columns, squares

# initialize empty board, to test we can build this as a sudoku solver (import a grid known to have a unique solution)
grid = [[0 for i in range(10)] for j in range(10)]


# function to display the grid
def display_grid():
    global grid
    for row in grid:
        print(row)


# returns true if a given number is allowed at a given position, on the global grid
def is_allowed(number, position):
    pass


# recursive function to be called to solve the puzzle.
def solve_puzzle():
    pass


display_grid()



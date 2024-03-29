# Killer Sudoku Generator

This program generates valid, solvable killer sudoku (KS) puzzles.


## Dependencies

Python 3.0 or greater.

Various Python libraries:
- Pickle
- Numpy
- Itertools
- Random

## Scripts

This library contains a series of scripts, each of which is tasked with managing a certain step in the KS solving process.

### `solver.py`
This script uses recursion to brute-force solutions to an input sudoku puzzle, finding all possible solutions.


### `generator.py`
Generates valid complete sudoku grids and saves them in a `.pickle` file.

### `cage_builder.py`
Generates KS cage layout configurations and saves them in a `.pickle` file.

### `ks_validator.py`
Combines cage layouts and completed sudoku grids to generate valid KS puzzles

### `ks_solver.py`
Solves generated KS puzzles and gives number of possible solutions. For a KS puzzle to be valid, there should exist a unique solution.



### WIP

This is a work in progress. There are still several tasks that need to be completed before this program can successfully generate valid, unique KS puzzles of varying difficulty.

Notably, using brute-force recursion to solve killer sudoku puzzles is inefficient and sometimes runs indefinitely while trying to solve the puzzle. Heuristics for solving KS puzzles need to be implemented to improve this process.


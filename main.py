import numpy as np

# Load sudokus
from Sudoku import Sudoku
from sudoku_solver import sudoku_solver

sudoku = np.load("data/very_easy_puzzle.npy")
print("very_easy_puzzle.npy has been loaded into the variable sudoku")
print(f"sudoku.shape: {sudoku.shape}, sudoku[0].shape: {sudoku[0].shape}, sudoku.dtype: {sudoku.dtype}")

# Load solutions for demonstration
solutions = np.load("data/very_easy_solution.npy")
print()

# Print the first 9x9 sudoku...
print("First sudoku:")
print(sudoku[0], "\n")

# ...and its solution
print("Solution of first sudoku:")
print(solutions[0])

s = Sudoku(sudoku[0])
print(s.spaces_dict)
print(s)

solved = sudoku_solver(s)
print(solved.grid)
print(solutions[0])
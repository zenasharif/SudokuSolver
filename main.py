import numpy as np

# Load sudokus
from Sudoku import Sudoku
from sudoku_solver import sudoku_solver

difficulties = ["very_easy", "easy", "medium", "hard"]

for diff in difficulties:
    sudoku = np.load("data/" + diff + "_puzzle.npy")
    solutions = np.load("data/"+diff+"_solution.npy")
    for i in range(15):
        print("This is sudoku", i, "in", diff)
        print(sudoku_solver(sudoku[i]))
        print("Solution", i, "in", diff)
        print(solutions[i])

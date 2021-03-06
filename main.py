from time import time

import numpy as np

from sudoku_solver import sudoku_solver

difficulties = ["very_easy", "easy", "medium", "hard"]

start_time = time()
for n in range(10):
    for diff in difficulties:
        sudoku = np.load("data/" + diff + "_puzzle.npy")
        solutions = np.load("data/"+diff+"_solution.npy")
        for i in range(15):
            sudoku_solver(sudoku[i])
print("time for all", float(time() - start_time) / 10.0)

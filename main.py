from time import time

import numpy as np

from sudoku_solver import sudoku_solver

difficulties = ["very_easy", "easy", "medium", "hard"]

# start_time = time()
# for n in range(10):
#     for diff in difficulties:
#         sudoku = np.load("data/" + diff + "_puzzle.npy")
#         solutions = np.load("data/"+diff+"_solution.npy")
#         for i in range(15):
#             sudoku_solver(sudoku[i])
# print("time for all", float(time() - start_time) / 10.0)

for diff in difficulties:
    sudoku = np.load("data/" + diff + "_puzzle.npy")
    solutions = np.load("data/" + diff + "_solution.npy")
    for i in range(15):
        print(diff, i, np.array_equal(sudoku_solver(sudoku[i]), solutions[i]))
# print("time for all", float(time() - start_time))

# sudoku = np.load("data/hard_puzzle.npy")
# solutions = np.load("data/hard_solution.npy")
# print(sudoku_solver(sudoku[2]))
# print(solutions[2])

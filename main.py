from time import time

import numpy as np

# Load sudokus
from Sudoku import Sudoku
from sudoku_solver import sudoku_solver

difficulties = ["very_easy", "easy", "medium",
                "hard"]

start_time = time()
for diff in difficulties:
    sudoku = np.load("data/" + diff + "_puzzle.npy")
    solutions = np.load("data/"+diff+"_solution.npy")
    for i in range(15):
        ind_start_time = time()
        # print("This is sudoku", i, "in", diff)
        # print(sudoku_solver(sudoku[i]))
        # print("Solution", i, "in", diff)
        # print(solutions[i])

        print(np.array_equal(sudoku_solver(sudoku[i]), solutions[i]))
        print("time for sudoku", i, time()-ind_start_time)
print("time for all", time()-start_time)

# sudoku = np.load("data/hard_puzzle.npy")
# solution = np.load("data/hard_solution.npy")
#
# print(sudoku[2])
# # print(sudoku_solver(sudoku[4]))
# print(np.array_equal(sudoku_solver(sudoku[2]), solution[2]))
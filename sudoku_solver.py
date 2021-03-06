import copy

from Sudoku import Sudoku


def sudoku_solver(sudoku):
    """
        Solves a Sudoku puzzle and returns its unique solution.

        Input
            sudoku : 9x9 numpy array
                Empty cells are designated by 0.

        Output
            9x9 numpy array of integers
                It contains the solution, if there is one. If there is no solution, all array entries should be -1.
    """
    s = Sudoku(sudoku)
    if s.valid_grid():
        result = sudoku_solver_recursive(s)
        if result is not None:
            return result.grid
    sudoku.fill(float(-1))
    return sudoku  # 9x9 numpy array of -1s


def sudoku_solver_recursive(sudoku):
    """
    Inserts known values into the sudoku then uses depth first search and backtracking to complete the grid
    :param sudoku: Sudoku object
    :return: Sudoku object or None if invalid
    """
    update = True
    while update and not sudoku.invalid_spaces_dict():
        update = False

        update = sudoku.insert_singleton_values(update)
        if not sudoku.valid_grid():
            return None

        update = sudoku.insert_unique_values(update)

        if not update:
            update = sudoku.isolate_sibling_values(update)

    if sudoku.invalid_spaces_dict():
        return None
    elif sudoku.solved():
        return sudoku
    else:
        # Chooses space with least possible values for next action
        sorted_list_of_keys = sorted(sudoku.spaces_dict.keys(), key=lambda x: (len(sudoku.spaces_dict[x])))
        space = sorted_list_of_keys[0]
        for value in sudoku.spaces_dict[space]:
            new = copy.deepcopy(sudoku)
            new.grid[space[0]][space[1]] = value
            del new.spaces_dict[space]
            new.update_dict()
            result = sudoku_solver_recursive(new)
            if result is not None and result.solved():
                return result
        return None

import copy
from collections import Counter

from Sudoku import Sudoku


def sudoku_solver(sudoku):
    s = Sudoku(sudoku)
    if s.valid_grid():
        result = sudoku_solver_recursive(s)
        if result is not None:
            return result.grid
    sudoku.fill(float(-1))
    return sudoku  # 9x9 numpy array of -1s


# if the input is not valid
#   return none
# if the input is fine
#    do the below(call sudoku solver)

def sudoku_solver_recursive(sudoku):
    """
    Solves a Sudoku puzzle and returns its unique solution.

    Input
        sudoku : 9x9 numpy array
            Empty cells are designated by 0.

    Output
        9x9 numpy array of integers
            It contains the solution, if there is one. If there is no solution, all array entries should be -1.
    """

    update = True
    while update and not sudoku.invalid():
        update = False

        inserted = []
        for space in sudoku.spaces_dict.keys():
            # insert singleton values
            if len(sudoku.spaces_dict[space]) == 1:
                sudoku.grid[space[0]][space[1]] = sudoku.spaces_dict[space][0]  # get only thing in list
                inserted.append(space)
                update = True
        if len(inserted) > 0:
            for space in inserted:
                del sudoku.spaces_dict[space]
            sudoku.update_dict()
            if not sudoku.valid_grid():
                return None

        inserted = []
        space_to_square = dict()
        space_to_square[0] = (0, 0)
        space_to_square[1] = (0, 1)
        space_to_square[2] = (0, 2)
        space_to_square[3] = (1, 0)
        space_to_square[4] = (1, 1)
        space_to_square[5] = (1, 2)
        space_to_square[6] = (2, 0)
        space_to_square[7] = (2, 1)
        space_to_square[8] = (2, 2)

        for i in range(9):
            row_spaces = []
            col_spaces = []
            sq_spaces = []
            row_values = []
            col_values = []
            sq_values = []
            for s in sudoku.spaces_dict.keys():
                if s[0] == i:
                    row_spaces.append(s)
                    row_values.extend(sudoku.spaces_dict[s])
                if s[1] == i:
                    col_spaces.append(s)
                    col_values.extend(sudoku.spaces_dict[s])
                if s[0] // 3 == space_to_square[i][0] and s[1] // 3 == space_to_square[i][1]:
                    sq_spaces.append(s)
                    sq_values.extend(sudoku.spaces_dict[s])

            row_unique_values = [value for value in list(set(row_values)) if row_values.count(value) == 1]
            col_unique_values = [value for value in list(set(col_values)) if col_values.count(value) == 1]
            sq_unique_values = [value for value in list(set(sq_values)) if sq_values.count(value) == 1]

            for val in row_unique_values:
                for s in row_spaces:
                    if val in sudoku.spaces_dict[s]:
                        sudoku.grid[s] = val
                        inserted.append(s)
                        update = True
                        break

            for val in col_unique_values:
                for s in col_spaces:
                    if val in sudoku.spaces_dict[s]:
                        sudoku.grid[s] = val
                        inserted.append(s)
                        update = True
                        break

            for val in sq_unique_values:
                for s in sq_spaces:
                    if val in sudoku.spaces_dict[s]:
                        sudoku.grid[s] = val
                        inserted.append(s)
                        update = True
                        break

        if len(inserted) > 0:
            # make inserted spaces a set in case the cell has a unique value in the row and column
            for space in list(set(inserted)):
                del sudoku.spaces_dict[space]
            sudoku.update_dict()

        if not update:
            # sibling finder - doesn't change grid just isolates siblings in dictionary
            for i in range(9):
                row_spaces = []
                col_spaces = []
                sq_spaces = []
                row_values = []
                col_values = []
                sq_values = []
                for space in list(sudoku.spaces_dict):
                    if space[0] == i:
                        row_spaces.append(space)
                        row_values.append(sudoku.spaces_dict[space])
                    if space[1] == i:
                        col_spaces.append(space)
                        col_values.append(sudoku.spaces_dict[space])
                    if space[0] // 3 == space_to_square[i][0] and space[1] // 3 == space_to_square[i][1]:
                        sq_spaces.append(space)
                        sq_values.append(sudoku.spaces_dict[space])
                # maps list of spaces_dict values to tuples then uses Counter to count occurrences of each tuple
                row_siblings_to_sibling_count_dict = dict(Counter(map(tuple, row_values)))
                col_siblings_to_sibling_count_dict = dict(Counter(map(tuple, col_values)))
                sq_siblings_to_sibling_count_dict = dict(Counter(map(tuple, sq_values)))

                for key in row_siblings_to_sibling_count_dict.keys():
                    if len(key) == row_siblings_to_sibling_count_dict[key]:
                        for space in row_spaces:
                            if sudoku.spaces_dict[space] != list(key):
                                temp_dict_values = [x for x in sudoku.spaces_dict[space] if x not in list(key)]
                                if sudoku.spaces_dict[space] != temp_dict_values:
                                    sudoku.spaces_dict[space] = temp_dict_values
                                    update = True

                for key in col_siblings_to_sibling_count_dict.keys():
                    if len(key) == col_siblings_to_sibling_count_dict[key]:
                        for space in col_spaces:
                            if sudoku.spaces_dict[space] != list(key):
                                temp_dict_values = [x for x in sudoku.spaces_dict[space] if x not in list(key)]
                                if sudoku.spaces_dict[space] != temp_dict_values:
                                    sudoku.spaces_dict[space] = temp_dict_values
                                    update = True

                for key in sq_siblings_to_sibling_count_dict.keys():
                    if len(key) == sq_siblings_to_sibling_count_dict[key]:
                        for space in sq_spaces:
                            if sudoku.spaces_dict[space] != list(key):
                                temp_dict_values = [x for x in sudoku.spaces_dict[space] if x not in list(key)]
                                if sudoku.spaces_dict[space] != temp_dict_values:
                                    sudoku.spaces_dict[space] = temp_dict_values
                                    update = True

    if sudoku.invalid():
        return None

    elif sudoku.solved():
        return sudoku
    else:
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

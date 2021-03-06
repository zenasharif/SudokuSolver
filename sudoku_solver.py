import copy

from Sudoku import Sudoku


def sudoku_solver(sudoku):
    s = Sudoku(sudoku)
    if s.valid_grid():
        # print("I'm valid!")
        result = sudoku_solver_recursive(s)
        if result is not None:
            return result.grid
    # print("I'm NOT valid!")
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
    # print("Entered sudoku_solver")
    # print(sudoku)
    # print(sudoku.spaces_dict)

    update = True
    while update and not sudoku.invalid():
        update = False

        inserted = []
        for space in sudoku.spaces_dict.keys():
            # insert singleton values
            if len(sudoku.spaces_dict[space]) == 1:
                # print("found singleton in space", space, sudoku.spaces_dict[space])
                sudoku.grid[space[0]][space[1]] = sudoku.spaces_dict[space][0]  # get only thing in list
                inserted.append(space)
                update = True
        if len(inserted) > 0:
            for space in inserted:
                del sudoku.spaces_dict[space]
            sudoku.update_dict()
            if not sudoku.valid_grid():
                return None

    if sudoku.invalid():
        # print("Invalid")
        return None

    # if not sudoku.valid_grid():
    #     # print("Invalid")
    #     return None

    elif sudoku.solved():
        # print("Solved")
        return sudoku
    else:
        sorted_list_of_keys = sorted(sudoku.spaces_dict.keys(),
                                     key=lambda x: (len(sudoku.spaces_dict[x])))
        space = sorted_list_of_keys[0]  # potentially choose key with least options
        # print("Looking at space ", space, "with values: ", sudoku.spaces_dict[space])
        for value in sudoku.spaces_dict[space]:
            new = copy.deepcopy(sudoku)
            new.grid[space[0]][space[1]] = value
            # new.cell_row = space[0]
            # new.cell_col = space[1]
            del new.spaces_dict[space]
            new.update_dict()
            # print("About to be recursive")
            result = sudoku_solver_recursive(new)
            if result is not None and result.solved():
                return result
        return None

        # if invalid
        # return false and try another value (go up a level) - return none
        # if completed
        # return the sudoku
        # else
        # for space in spaces
        # for value in possible values for that space
        # guess a value
        # result = sudoku_solver(new_sudoku)
        # if result not none and is complete
        # return result
        # return none

        # # insert unique values in rows
        # for i in range(9):
        #     row_spaces = []
        #     values = []
        #     unique = []
        #     for s in sudoku.spaces_dict.keys:
        #         if s[0] == i:
        #             row_spaces.append(s)
        #             values.append(sudoku.spaces_dict[s])
        #
        #     # finding unique values by sorting list and comparing element to prev and next
        #     values.sort()
        #     if values[0] != values[1]:
        #         unique.append(values[0])
        #     for val in range(1, len(values) - 1):
        #         if values[val] != values[val + 1] and values[val] != values[val - 1]:
        #             unique.append(values[val])
        #     if values[len(values) - 2] != values[len(values) - 1]:
        #         unique.append(values[len(values) - 1])
        #
        #     # if we have any unique values
        #     if len(unique) > 0:
        #         # I thought it would be quicker to loop through the spaces in row than looping through all of
        #         # them again?
        #
        #         # not sure which way round these for loops should go...
        #         # for each unique value, look through spaces and find the one containing it
        #         for val in unique:
        #             for s in row_spaces:
        #                 if val in sudoku.spaces_dict[s]:
        #                     sudoku.grid[s] = val
        #
        # # insert unique values in column - same as above for columns
        # for i in range(9):
        #     col_spaces = []
        #     values = []
        #     unique = []
        #     for s in sudoku.spaces_dict.keys:
        #         if s[0] == i:
        #             col_spaces.append(s)
        #             values.append(sudoku.spaces_dict[s])
        #     values.sort()
        #     if values[0] != values[1]:
        #         unique.append(values[0])
        #     for val in range(1, len(values) - 1):
        #         if values[val] != values[val + 1] and values[val] != values[val - 1]:
        #             unique.append(values[val])
        #     if values[len(values) - 2] != values[len(values) - 1]:
        #         unique.append(values[len(values) - 1])
        #     if len(unique) > 0:
        #         for s in col_spaces:
        #             for val in unique:
        #                 if val in sudoku.spaces_dict[s]:
        #                     sudoku.grid[s] = val

        # should I do the above for squares?

    # While update and not invalid
    # update = false
    # check single values - insert all of them
    # update = true
    # check unique values and insert all of them
    # update = true
    # check siblings and insert
    # update = true
    # refresh sudoku

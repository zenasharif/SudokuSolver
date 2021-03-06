import copy

from Sudoku import Sudoku


def sudoku_solver(sudoku):
    s = Sudoku(sudoku)
    if s.valid_grid():
        # print("I'm valid!")
        result = sudoku_solver_recursive(s)
        if result is not None:
            print(result.grid)
            return result.grid
    # print("I'm NOT valid!")
    sudoku.fill(float(-1))
    print(sudoku)
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


    # While update and not invalid
    # update = false
    # check single values - insert all of them
    # update = true
    # check unique values and insert all of them
    # update = true
    # check siblings and insert
    # update = true
    # refresh sudoku

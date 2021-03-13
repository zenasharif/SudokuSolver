from collections import Counter


def get_squares_dict():
    """
        Breaks the board down into 9 3x3 squares with coordinates corresponding to squares with integer division by 3
        :returns space_to_square dictionary
    """
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
    return space_to_square


class Sudoku:
    """
    grid: 9x9 2d numpy array
    spaces_dict: dictionary of spaces and valid actions
    cell_row: int referring to coordinate of row when validating values for a space
    cell_col: int referring to coordinate of column when validating values for a space
    """
    def __init__(self, sudoku_grid):
        self.grid = sudoku_grid
        self.spaces_dict = self.create_spaces_dict()
        self.cell_row = 0
        self.cell_col = 0

    def get_spaces(self):
        """
        Finds 0s corresponding to empty space in the grid
        :return: list of spaces
        """
        spaces = []
        for i in range(9):
            for j in range(9):
                if self.grid[i][j] == 0:
                    spaces.append((i, j))
        return spaces

    def valid_action(self):
        """
        Checks if action is valid
        :return: boolean
        """
        return self.check_row_col() and self.check_sq()

    def check_row_col(self):
        """
        Checks if action results in duplicate values in a row or column
        :return: boolean
        """
        for i in range(9):
            if self.grid[self.cell_row][i] == self.grid[self.cell_row][self.cell_col] and i != self.cell_col:
                return False
            if self.grid[i][self.cell_col] == self.grid[self.cell_row][self.cell_col] and i != self.cell_row:
                return False
        return True

    def check_sq(self):
        """
        Checks if action results in duplicate values in a square
        :return: boolean
        """
        [x, y] = self.find_sq()
        for i in range(3 * x, 3 * (x + 1)):
            for j in range(3 * y, 3 * (y + 1)):
                if self.grid[i][j] == self.grid[self.cell_row][
                   self.cell_col] and i != self.cell_row and j != self.cell_col:
                    return False
        return True

    def find_sq(self):
        """
        Finds top-left coordinates of square
        :return: coordinate pair
        """
        sq_row = self.cell_row // 3
        sq_col = self.cell_col // 3
        return [sq_row, sq_col]

    def create_spaces_dict(self):
        """
        Gets all valid values for each space and creates a dictionary of spaces and valid actions
        :return: spaces_dict dictionary
        """
        spaces = self.get_spaces()
        spaces_dict = dict()
        for pair in spaces:
            self.cell_row = pair[0]
            self.cell_col = pair[1]
            possible_values = []
            for i in range(1, 10):
                self.grid[pair[0]][pair[1]] = i
                if self.valid_action():
                    possible_values.append(i)
            spaces_dict[pair] = possible_values
            self.grid[pair[0]][pair[1]] = 0
        return spaces_dict

    def update_dict(self):
        """
        Validates the spaces dictionary values after an action has been taken
        """
        for pair in self.spaces_dict.keys():
            self.cell_row = pair[0]
            self.cell_col = pair[1]
            possible_values = []
            for i in self.spaces_dict[pair]:
                self.grid[pair[0]][pair[1]] = i
                if self.valid_action():
                    possible_values.append(i)
            self.spaces_dict[pair] = possible_values
            self.grid[pair[0]][pair[1]] = 0

    def invalid_spaces_dict(self):
        """
        Checks to see if there are any spaces with no valid actions
        :return: boolean
        """
        for space in self.spaces_dict.keys():
            if self.spaces_dict[space] == []:
                return True
        return False

    def __str__(self):
        output = ""
        for i in range(9):
            if i % 3 == 0:
                output += " |-------+-------+-------|\n"
            for j in range(9):
                if j % 3 == 0:
                    output += " |"
                if self.grid[i][j] == 0:
                    output += "  "
                else:
                    output += " " + str(self.grid[i][j])
            output += " |\n"
        output += " |-------+-------+-------|"
        return output

    def solved(self):
        """
        Checks there are no spaces left in the grid
        :return: boolean
        """
        if len(self.spaces_dict) == 0:
            return True
        return False

    def valid_grid(self):
        """
        validates each row / column / square to ensure there are no duplicate values
        :return: boolean
        """
        for i in range(9):
            if sum(self.grid[i]) != sum(set(self.grid[i])):  # validate row (no duplicate values)
                return False
            if sum(self.grid[:, i]) != sum(set(self.grid[:, i])):  # validate column
                return False
        for i in range(3):
            for j in range(3):  # validate squares
                if (sum(self.grid[3 * i:3 * (i + 1), 3 * j:3 * (j + 1)].flatten()) !=
                        sum(set(self.grid[3 * i:3 * (i + 1), 3 * j:3 * (j + 1)].flatten()))):
                    return False
        return True

    def insert_single_values(self, update):
        """
        Inserts all values in dictionary with length 1 - the only valid action for this space
        :param update: boolean
        :return: boolean update
        """
        inserted = []
        for space in self.spaces_dict.keys():
            if len(self.spaces_dict[space]) == 1:
                self.grid[space[0]][space[1]] = self.spaces_dict[space][0]  # get only thing in list
                inserted.append(space)
                update = True
        if len(inserted) > 0:
            for space in inserted:
                del self.spaces_dict[space]
            self.update_dict()
        return update

    def insert_unique_values(self, update):
        """
        Inserts values only occurring once in a row, column or square.
        :param update: boolean
        :return: update boolean
        """
        inserted = []
        space_to_square = get_squares_dict()
        for i in range(9):
            row_spaces = []
            col_spaces = []
            sq_spaces = []
            row_values = []
            col_values = []
            sq_values = []
            for space in self.spaces_dict.keys():
                if space[0] == i:
                    row_spaces.append(space)
                    row_values.extend(self.spaces_dict[space])
                if space[1] == i:
                    col_spaces.append(space)
                    col_values.extend(self.spaces_dict[space])
                if space[0] // 3 == space_to_square[i][0] and space[1] // 3 == space_to_square[i][1]:
                    sq_spaces.append(space)
                    sq_values.extend(self.spaces_dict[space])

            row_unique_values = [value for value in list(set(row_values)) if row_values.count(value) == 1]
            col_unique_values = [value for value in list(set(col_values)) if col_values.count(value) == 1]
            sq_unique_values = [value for value in list(set(sq_values)) if sq_values.count(value) == 1]

            for val in row_unique_values:
                for space in row_spaces:
                    if val in self.spaces_dict[space]:
                        self.grid[space] = val
                        inserted.append(space)
                        update = True
                        break

            for val in col_unique_values:
                for space in col_spaces:
                    if val in self.spaces_dict[space]:
                        self.grid[space] = val
                        inserted.append(space)
                        update = True
                        break

            for val in sq_unique_values:
                for space in sq_spaces:
                    if val in self.spaces_dict[space]:
                        self.grid[space] = val
                        inserted.append(space)
                        update = True
                        break

        if len(inserted) > 0:
            # make inserted a set in case the cell has a unique value found in the row and column
            for space in list(set(inserted)):
                del self.spaces_dict[space]
            self.update_dict()
        return update

    def isolate_identical_groups(self, update):
        """
        For each row / column / square, finds lists of valid actions in the spaces_dict whose length is equal to
        their count. The values in these lists must occur in those spaces and therefore can be deleted from other
        spaces in the row / column / square
        :param update: boolean
        :return: update boolean
        """

        space_to_square = get_squares_dict()
        for i in range(9):
            row_spaces = []
            col_spaces = []
            sq_spaces = []
            row_values = []
            col_values = []
            sq_values = []
            for space in list(self.spaces_dict):
                if space[0] == i:
                    row_spaces.append(space)
                    row_values.append(self.spaces_dict[space])
                if space[1] == i:
                    col_spaces.append(space)
                    col_values.append(self.spaces_dict[space])
                if space[0] // 3 == space_to_square[i][0] and space[1] // 3 == space_to_square[i][1]:
                    sq_spaces.append(space)
                    sq_values.append(self.spaces_dict[space])

            # maps list of spaces_dict values to tuples then uses Counter to count occurrences of each tuple
            row_groups_to_group_count_dict = dict(Counter(map(tuple, row_values)))
            col_groups_to_group_count_dict = dict(Counter(map(tuple, col_values)))
            sq_groups_to_group_count_dict = dict(Counter(map(tuple, sq_values)))

            for key in row_groups_to_group_count_dict.keys():
                if len(key) == row_groups_to_group_count_dict[key]:
                    for space in row_spaces:
                        if self.spaces_dict[space] != list(key):
                            temp_dict_values = [x for x in self.spaces_dict[space] if x not in list(key)]
                            if self.spaces_dict[space] != temp_dict_values:
                                self.spaces_dict[space] = temp_dict_values
                                update = True

            if update:
                return update

            for key in col_groups_to_group_count_dict.keys():
                if len(key) == col_groups_to_group_count_dict[key]:
                    for space in col_spaces:
                        if self.spaces_dict[space] != list(key):
                            temp_dict_values = [x for x in self.spaces_dict[space] if x not in list(key)]
                            if self.spaces_dict[space] != temp_dict_values:
                                self.spaces_dict[space] = temp_dict_values
                                update = True

            if update:
                return update

            for key in sq_groups_to_group_count_dict.keys():
                if len(key) == sq_groups_to_group_count_dict[key]:
                    for space in sq_spaces:
                        if self.spaces_dict[space] != list(key):
                            temp_dict_values = [x for x in self.spaces_dict[space] if x not in list(key)]
                            if self.spaces_dict[space] != temp_dict_values:
                                self.spaces_dict[space] = temp_dict_values
                                update = True
            if update:
                return update
        return update

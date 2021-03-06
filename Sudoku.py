class Sudoku:
    def __init__(self, sudoku_grid):
        self.grid = sudoku_grid
        self.spaces_dict = self.create_spaces_dict()
        self.cell_row = 0
        self.cell_col = 0

    def get_spaces(self):
        spaces = []
        for i in range(9):
            for j in range(9):
                if self.grid[i][j] == 0:
                    spaces.append((i, j))
        return spaces

    def valid(self):
        return self.check_row() and self.check_col() and self.check_sq()

    def check_row(self):
        for i in range(9):
            if self.grid[self.cell_row][i] == self.grid[self.cell_row][self.cell_col] and i != self.cell_col:
                return False
        return True

    def check_col(self):
        for i in range(9):
            if self.grid[i][self.cell_col] == self.grid[self.cell_row][self.cell_col] and i != self.cell_row:
                return False
        return True

    def check_sq(self):
        [x, y] = self.find_sq()
        for i in range(3 * x, 3 * (x + 1)):
            for j in range(3 * y, 3 * (y + 1)):
                if self.grid[i][j] == self.grid[self.cell_row][
                    self.cell_col] and i != self.cell_row and j != self.cell_col:
                    return False
        return True

    def find_sq(self):
        sq_row = self.cell_row // 3
        sq_col = self.cell_col // 3
        return [sq_row, sq_col]

    # Get all the possible values for each space and put in a dictionary
    def create_spaces_dict(self):
        spaces = self.get_spaces()
        spaces_dict = dict()
        for pair in spaces:
            self.cell_row = pair[0]
            self.cell_col = pair[1]
            possible_values = []
            for i in range(1, 10):
                self.grid[pair[0]][pair[1]] = i
                if self.valid():
                    possible_values.append(i)
            spaces_dict[pair] = possible_values
            self.grid[pair[0]][pair[1]] = 0
        return spaces_dict

    def update_dict(self):
        for pair in self.spaces_dict.keys():
            self.cell_row = pair[0]
            self.cell_col = pair[1]
            possible_values = []
            for i in self.spaces_dict[pair]:
                self.grid[pair[0]][pair[1]] = i
                if self.valid():
                    possible_values.append(i)
            self.spaces_dict[pair] = possible_values
            self.grid[pair[0]][pair[1]] = 0

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

    def invalid(self):
        for space in self.spaces_dict.keys():
            if self.spaces_dict[space] == []:
                return True
        return False

    def solved(self):
        if len(self.spaces_dict) == 0:
            return True
        return False

    def valid_grid(self):
        for i in range(9):
            if sum(self.grid[i]) != sum(set(self.grid[i])):  # validate row (no duplicate values)
                return False
            if sum(self.grid[:, i]) != sum(set(self.grid[:, i])):   # validate column
                return False
        for i in range(3):
            for j in range(3):  # validate squares
                if (sum(self.grid[3 * i:3 * (i + 1), 3 * j:3 * (j + 1)].flatten()) !=
                        sum(set(self.grid[3 * i:3 * (i + 1), 3 * j:3 * (j + 1)].flatten()))):
                    return False

        return True

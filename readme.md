# Sudoku solver

The task of solving a sudoku involves considering the basic constraints of the problem by ensuring each row, column and 3x3 square contains the digits 1-9 with no repeated values. Additional consideration must also be given to how to fill in the available squares.

## Backtracking

The backtracking algorithm is a depth first search approach which describes guessing values from 1 to 9 to insert into a space from a list of possible actions. This process is repeated until the constraints are broken and the produced state is not valid. If there are no further valid actions, then the algorithm will move back up to a previous state and try the next value for that square. This recursive process will repeat until either the sudoku is solved, or all possible actions have been tried and the sudoku is determined invalid.

After verifying whether the initial state is valid, the first step in this algorithm is to isolate the empty spaces in the sudoku puzzle. These are stored in a dictionary along with any valid actions that could be taken for that space. This provides a smaller search space for the backtracking algorithm by eliminating any options that are known to be invalid. When determining which space to fill in next, the algorithm chooses the space with the least number of possible valid actions. By choosing the space with the fewest options, the span of the depth first search tree is reduced and therefore less actions are repeated throughout the backtracking process, meaning the algorithm becomes more efficient.

## Constraints

### Goal state

The goal state for a sudoku grid is one in which all entries have been filled without violating any of the problem's constraints. In the format of the given problems, it is a grid which contains no '0's. If this state is not reached and all possible actions have been exhausted, or the initial state is invalid, a 2 dimensional 9x9 array of -1 values is returned.

### Validity

There are 3 checks for validity used in this approach in order to optimise the run time.

The first check is a validity check on the whole grid. This searches the entire array for any duplicate values in rows, columns or squares. This check is necessary for an initial validation of the sudoku grid, as well as when optimisations, such as inserting single values (see below) are made. When using this optimisation duplicate values can occur on a row, column or 3x3 square since there are no checks for this within the dictionary.

The next check is action validity. This is used when creating the dictionary of spaces to possible actions. For each space, it is only necessary to check the row, column and 3x3 square that the space belongs to. This is less computationally expensive than ensuring the validity of the whole grid which has already been done as an initial check. Therefore this is sufficient to ensure the validity of possible actions stored in the dictionary.

The final check is for the validity of the dictionary itself. When backtracking, one value at a time is inserted into the grid and the dictionary is updated to reflect this. This means that any conflicting values in the same row, column or 3x3 square will be removed from the dictionary. If at any time an update results in a space having no valid actions available, then the current state is invalid, and the algorithm returns to the previous state. This is also a much less computationally expensive check than ensuring validity of the entire sudoku grid after every insertion.

## Further optimisations

### Single values

If there are any spaces in the dictionary with only one valid action, this is the only option and can be inserted into the grid.

The backtracking algorithm will already insert single values first since the next space is chosen based on the fewest possible values. The advantage of this method is that all "single values" can be inserted at once, and with only one update of the dictionary. This reduces the number of recursive calls needed in order to solve the sudoku, and hence reduces the memory usage.

Inserting single values reduced the runtime to 48 seconds on average for all 60 sudokus when used alone with backtracking. However, when used in conjunction with the unique values method, the runtime was increased to 1.4 seconds on average for 60 sudokus. The method has been included due to the decreased memory usage, since the runtime increase was not significant.
DOES  IT HELP MAKE THEM MORE EVEN? CHECK. 

### Unique values

Any value that occurs only once in the valid actions available for the spaces in the same row, column or square must be unique. The value can therefore be inserted into the space for which it is valid, as this is the only place that the value can occur. 

This can cut down the search space as any other valid actions for that space can be ignored, and the correct value inserted straight away.

Inserting unique values into the grid improved the running time from 65 seconds to 1.2 seconds on average for all 60 sudokus. This was the most efficient optimisation and so is the first one that the algorithm applies on each recursion.

### Siblings

In a sudoku, any pair of spaces in the same row, column or 3x3 square with only the same two possible values available must contain those values. These values can therefore be removed from the possible values for any other spaces in the same row, column or square as the pair.

This idea can be extended to groups of any size. A sibling is defined to be a group of identical possible value lists whose count is equal to the length of said list. In the sudoku, this means that the values in this group must occur only in the spaces included in the group. These values can therefore be deleted from all other spaces in the same row, column or square. This reduces the search space for the rest of the sudoku, even though no values are directly inserted into the grid.

WHY IS THIS? This part of the algorithm is only used if there are no actions taken from the two optimisations described above. This is because the indirect results from this step would not be as valuable as the other two. 

Removing the sibling values from their non sibling squares in the row, column or squares reduced the running time to 1.3 seconds on average for all 60 sudokus when used in conjunction with the other two methods. Alone it was the least effective, reducing the runtime to 59 seconds for 60 sudokus. IS THIS WHY IT IS ONLY USED IF THERE ARE NO OTHER UPDATES? IT WASN'T THAT DIFFERENT TO ALWAYS DO IT...

Any of the three optimisations may result in more single or unique values once the dictionary has been updated, and so these are all checked repeatedly until no more updates are made. Therefore many iterations of these checks could be completed without requiring a guess.
# Function to parse the input lists and store them in a more convenient form
def parse_input(vertical, horizontal):
  # Get the size of the puzzle from the input lists
  rows = len(horizontal)
  cols = len(vertical)

  # Create an empty puzzle with the correct size
  puzzle = []
  for _ in range(rows):
    puzzle.append([0] * cols)

  # Store the vertical hints in a more convenient form
  vertical_hints = []
  for col in range(cols):
    hint = []
    for row in range(rows):
      hint.append(vertical[col][row])
    vertical_hints.append(hint)

  # Store the horizontal hints in a more convenient form
  horizontal_hints = []
  for row in range(rows):
    horizontal_hints.append(horizontal[row])

  return puzzle, vertical_hints, horizontal_hints

# Function to solve the nonogram puzzle
def solve_puzzle(puzzle, vertical_hints, horizontal_hints):
  # Create a list of tuples representing the coordinates of all the
  # squares in the puzzle
  squares = [(row, col) for row in range(len(puzzle))
             for col in range(len(puzzle[0]))]

  # Keep solving the puzzle until it is complete
  while squares:
    # Try to solve each square in the puzzle
    for row, col in squares:
      # Check if the square can be solved based on the hints
      if can_solve_square(puzzle, row, col, vertical_hints, horizontal_hints):
        # If the square can be solved, remove it from the list of squares
        squares.remove((row, col))

  # Return the solved puzzle
  return puzzle

# Function to check if a square can be solved based on the hints
def can_solve_square(puzzle, row, col, vertical_hints, horizontal_hints):
  # Check if the square is already solved
  if puzzle[row][col] != 0:
    return True

  # Get the hints for the row and column containing the square
  row_hint = horizontal_hints[row]
  col_hint = vertical_hints[col]

  # Check if the square can be a 1 based on the hints
  if can_be_one(puzzle, row, col, row_hint, col_hint):
    puzzle[row][col] = 1
    return True

  # Check if the square can be a 0 based on the hints
  if can_be_zero(puzzle, row, col, row_hint, col_hint):
    puzzle[row][col] = 0
    return True

  # If the square can't be solved, return False
  return False

# Function to check if a square can be a 1 based on the hints
def can_be_one(puzzle, row, col, row_hint, col_hint):
  # Check if the square is already solved
  if puzzle[row][col] != 0:
    return puzzle[row][col] == 1

  # Check if the square is at the end of a sequence

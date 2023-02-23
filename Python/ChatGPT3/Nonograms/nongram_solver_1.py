import time


def solve_nonogram(vertical_hints, horizontal_hints):
    # Get the size of the puzzle grid
    num_rows = len(horizontal_hints)
    num_cols = len(vertical_hints)

    # Initialize the grid with all cells set to unknown (represented by -1)
    grid = [[-1 for _ in range(num_cols)] for _ in range(num_rows)]

    def is_valid(row):
        # Check if the current row is valid
        hints = horizontal_hints[row]
        line = grid[row]
        if len(hints) == 0:
            return True
        chunks = [line[i:j] for i, j in zip([0]+hints, hints+[None])]
        if any(len(c) > 0 and (0 in c or 1 in c) for c in chunks):
            return False
        return True

    def is_valid_grid():
        # Check if the entire grid is valid
        for row in range(num_rows):
            if not is_valid(row):
                return False
        for col in range(num_cols):
            hints = vertical_hints[col]
            line = [grid[row][col] for row in range(num_rows)]
            if len(hints) == 0:
                continue
            chunks = [line[i:j] for i, j in zip([0]+hints, hints+[None])]
            if any(len(c) > 0 and (0 in c or 1 in c) for c in chunks):
                return False
        return True

    def solve():
        for row in range(num_rows):
            for col in range(num_cols):
                if grid[row][col] == -1:
                    for value in [0, 1]:
                        grid[row][col] = value
                        if is_valid(row) and is_valid_grid() and solve():
                            return True
                        grid[row][col] = -1
                    return False
        return True

    if solve():
        return grid
    else:
        return None


if __name__ == "__main__":

	vertical_hints = [    [1, 1],
		[2, 2],
		[2, 1],
		[1, 2, 1],
		[1, 1, 1],
		[2, 2],
		[2, 2],
		[1, 1],
		[1, 1]
	]
	horizontal_hints = [    [1],
		[2],
		[1, 1],
		[1, 1, 1],
		[1, 1],
		[2],
		[2],
		[2],
		[1, 1]
	]
	solved_grid = solve_nonogram(vertical_hints, horizontal_hints)
	print(f"{solved_grid=}")
	time.sleep(5)
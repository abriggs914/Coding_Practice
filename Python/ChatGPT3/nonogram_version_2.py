def solve(width, height, horizontal_hints, vertical_hints):

	# initialise the grid with empty values
	grid = [[' ' for _ in range(width)] for _ in range(height)]

	# loop through the horizontal hints
	for row, hints in enumerate(horizontal_hints):
		# loop through the individual hints for each row
		for hint in hints:
			# calculate the starting and ending positions for this hint
			start = hint[0]
			end = start + hint[1]
			# fill in the grid with the hint values
			for col in range(start, end):
				grid[row][col] = 'X'

	# loop through the vertical hints
	for col, hints in enumerate(vertical_hints):
		# loop through the individual hints for each column
		for hint in hints:
			# calculate the starting and ending positions for this hint
			start = hint[0]
			end = start + hint[1]
			# fill in the grid with the hint values
			for row in range(start, end):
				grid[row][col] = 'X'

	# print out the solved grid
	for row in grid:
		print(''.join(row))
		
		
if __name__  == "__main__":
	solve(5, 5, [[[],[3],[1,1],[3],[]]], [[[],[3],[1,1],[3],[]]])
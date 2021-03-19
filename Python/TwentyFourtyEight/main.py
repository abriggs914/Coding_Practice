
import random as rand
import numpy as np
from utility import *

class G2048:

	def __init__(self, n=4):
	
		self.random_tile_values = [2, 4]
		self.shift_options = {
			"UP": "up",
			"DOWN": "down",
			"LEFT": "left",
			"RIGHT": "right",
		}
	
		self.n = n
		self.grid = [[None for j in range(n)] for i in range(n)]
		self.largest_tile = None
		
	def find_empty_cells(self):
		res = []
		for i in range(self.n):
			for j in range(self.n):
				if self.grid[i][j] is None:
					res.append((i, j))
		return res
		
	def place(self, i, j, v):
		self.grid[i][j] = v
		if self.largest_tile is None:
			self.largest_tile = (i, j, v)
		else:
			max_tile = None
			for p in range(self.n):
				for q in range(self.n):
					gv = self.grid[p][q] if self.grid[p][q] is not None else 0
					if max_tile is None or max_tile[2] > gv:
						max_tile = (p, q, gv)
			self.max_tile = max_tile

		
	def gen_random_tile(self):
		empty_cells = self.find_empty_cells()
		if not empty_cells:
			raise ValueError("Game over")
		i, j = rand.choice(empty_cells)
		v = rand.choice(self.random_tile_values)
		self.grid[i][j] = v
		
	def shift_grid(self, dir):
		so = self.shift_options
		n = self.n
		
		def shift_up(grid):
			grid = np.transpose(grid)
			res = []
			for row in grid:
				l = len(row)
				nr = [c for c in row if c is not None]
				row = nr + [None for i in range(l - len(nr))]
				res.append(row)
				
			res = np.transpose(res)
			return res
		def shift_down(grid):
			pass
		def shift_left(grid):
			pass
		def shift_right(grid):
			pass

		# def shift_up(grid):
		# 	print("shifting up:\n" + str(grid))
		# 	for i in range(n-1, 0, -1):
		# 		for j in range(n):
		# 			if grid[i-1][j] is None:
		# 				grid[i-1][j] = grid[i][j]
		# 				grid[i][j] = None
		# 			elif grid[i-1][j] == grid[i][j]:
		# 				grid[i-1][j] *= 2
		# 				grid[i][j] = None
		# 	print("done:\n" + str(grid))

		# def shift_down(grid):
		# 	print("shifting down:\n" + str(grid))
		# 	for i in range(n-1):
		# 		for j in range(n):
		# 			if grid[i+1][j] is None:
		# 				grid[i+1][j] = grid[i][j]
		# 				grid[i][j] = None
		# 			elif grid[i+1][j] == grid[i][j]:
		# 				grid[i+1][j] *= 2
		# 				grid[i][j] = None
		# 	print("done:\n" + str(grid))
		
		# def shift_left(grid):
		# 	# grid = np.transpose(grid)
		# 	print("shifting left:\n" + str(grid))
		# 	for i in range(n):
		# 		for j in range(n-1, 0, -1):
		# 			if grid[i][j-1] is None:
		# 				grid[i][j-1] = grid[i][j]
		# 				grid[i][j] = None
		# 			elif grid[i][j-1] == grid[i][j]:
		# 				grid[i][j-1] *= 2
		# 				grid[i][j] = None
		# 	print("shifted left:\n" + str(grid))
		# 	# grid = np.transpose(grid)
		# 	self.grid = grid
		# 	print("done:\n" + str(grid))

		# def shift_right(grid):
		# 	grid = np.transpose(grid)
		# 	print("shifting right:\n" + str(grid))
		# 	for i in range(n-1):
		# 		for j in range(n):
		# 			if grid[i+1][j] is None:
		# 				grid[i+1][j] = grid[i][j]
		# 				grid[i][j] = None
		# 			elif grid[i+1][j] == grid[i][j]:
		# 				grid[i+1][j] *= 2
		# 				grid[i][j] = None
		# 	grid = np.transpose(grid)
		# 	self.grid = grid
		# 	print("done:\n" + str(grid))

		if dir == so["UP"]:
			self.grid = shift_up(self.grid)
		elif dir == so["DOWN"]:
			self.grid = shift_down(self.grid)
		elif dir == so["LEFT"]:
			self.grid = shift_left(self.grid)
		elif dir == so["RIGHT"]:
			self.grid = shift_right(self.grid)
		print("done global: " + str(self.grid))
		
		
	def __repr__(self):
		res = "\n"
		min_width = 2 + len(str(self.max_tile[2]))
		for row in self.grid:
			for val in row:
				res += pad_centre(str(val), min_width) if val is not None else pad_centre("-", min_width)
			res += "\n"
		res += "\n"
		return res
		
		
if __name__ == "__main__":
	
	game = G2048()
	# game.gen_random_tile()
	game.place(0, 3, 2)
	game.place(3, 3, 2)
	game.place(3, 1, 4)
	game.place(3, 2, 16)
	game.place(2, 1, 32)
	game.place(1, 2, 16)
	print(game)
	game.shift_grid(game.shift_options["UP"])
	# game.shift_grid(game.shift_options["DOWN"])
	# game.shift_grid(game.shift_options["LEFT"])
	# game.shift_grid(game.shift_options["RIGHT"])
	print(game)
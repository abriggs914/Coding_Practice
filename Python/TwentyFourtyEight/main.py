
import random as rand
import numpy as np

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
		
	def find_empty_cells(self):
		res = []
		for i in range(self.n):
			for j in range(self.n):
				if self.grid[i][j] is None:
					res.append((i, j))
		return res
		
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
		empty_cells = self.find_empty_cells()
		# shifted_grid = [None for i in range(n)]
		shifted_grid = self.grid
		if dir == so["UP"]:
			cols = np.transpose(self.grid)
			for i, col in enumerate(cols):
				if None in col:
					# idx = col.index(None)
					# idx = np.where(col == None)
					idxs = [i for i, val in enumerate(col) if val == None]
					print("col: " + str(col) + ", idx: " + str(idxs))
					if len(idxs) < self.n:
						for idx in idxs:
							#TODO  finish this
							
					# if idx < n - 1:
						# shifted_grid[i] = col[:idx-1] + col[idx:]
			shifted_grid = np.transpose(shifted_grid)
					
		
		#for i in range(self.n):
		#	for j in range(self.n):
		#		if dir == so["UP"]:
		#			above = []
		
		self.grid = shifted_grid
		
	def __repr__(self):
		res = "\n"
		for row in self.grid:
			for val in row:
				res += str(val) if val is not None else "-"
			res += "\n"
		res += "\n"
		return res
		
		
if __name__ == "__main__":
	
	game = G2048()
	game.gen_random_tile()
	game.shift_grid(game.shift_options["UP"])
	print(game)
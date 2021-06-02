import os
import time
import datetime
import numpy as np
import random as rand
from utility import *
import keyboard as kbd


clear = lambda: os.system('cls') #on Windows System


def grid_print(grid):
	res = "\n"
	lenstr_no_none = lambda x : lenstr(x) if x != None else lenstr("-")
	lt = max([max(list(map(lenstr_no_none, row))) for row in grid])
	min_width = 2 + lt
	for row in grid:
		for val in row:
			res += pad_centre(str(val), min_width) if val is not None else pad_centre("-", min_width)
		res += "\n"
	res += "\n"
	return res


def write_score(game):
	file_name = "score_history.csv"
	with open(file_name, 'a') as f:
		f.write("\n" + ";;".join(game.get_record_entry()))

		
def get_move_input():
	print("Up, down, left, or right?")
	while True:
		if kbd.is_pressed('w') or kbd.is_pressed('up'):
			return "up"
		elif kbd.is_pressed('a') or kbd.is_pressed('left'):
			return "left"
		elif kbd.is_pressed('s') or kbd.is_pressed('down'):
			return "down"
		elif kbd.is_pressed('d') or kbd.is_pressed('right'):
			return "right"
		elif kbd.is_pressed('q'):
			return "quit"
	# valid = ["W", "A", "S", "D"]
	# legend = ["UP", "LEFT", "DOWN", "RIGHT"]
	# inp = ""
	# while inp.upper() not in valid:
		# inp = input("Up, down, left, or right?")
	# return legend[valid.index(inp.upper())].lower()


class G2048:

	def __init__(self, n=4, init_spaces=None, random_tile_values=(2, 4)):

		self.random_tile_values = random_tile_values
		self.shift_options = {
			"UP": "up",
			"DOWN": "down",
			"LEFT": "left",
			"RIGHT": "right",
		}
	
		self.n = n
		self.grid = [[None for j in range(n)] for i in range(n)]
		self.largest_tile = None
		self.score = 0
		self.hi_score = 0
		self.history = []
		
		if init_spaces:
			for i in range(n):
				for j in range(n):
					if init_spaces[i][j]:
						self.place(i, j, init_spaces[i][j])
		
	def find_empty_cells(self):
		res = []
		for i in range(self.n):
			for j in range(self.n):
				if self.grid[i][j] is None:
					res.append((i, j))
		return res

	def playable_directions(self):
		empty_cells = self.find_empty_cells()
		edges = [cell for cell in empty_cells if (cell[0] == 0 or cell[0] == self.n - 1) or (cell[1] == 0 or cell[1] == self.n - 1)]

		# if middle indexes are excluded, then you can move any direction
		if len(empty_cells) != len(edges):
			return "UP", "RIGHT", "DOWN", "LEFT"

		# check remaining none spaces
		dirs = []
		up = "UP"
		down = "DOWN"
		left = "LEFT"
		right = "RIGHT"
		for ei, ej in edges:
			sub_dirs = []
			if ei == 0 and up not in dirs:
				sub_dirs.append(up)
			if ei == self.n - 1 and down not in dirs:
				sub_dirs.append(down)
			if ej == 0 and left not in dirs:
				sub_dirs.append(left)
			if ej == self.n - 1 and right not in dirs:
				sub_dirs.append(right)
			dirs += sub_dirs

		g = self.grid

		# check matching grid cells
		for i in range(self.n):
			for j in range(self.n):
				v = g[i][j]
				if i < self.n - 1:
					if v == g[i + 1][j]:
						if down not in dirs:
							dirs.append(down)
						if up not in dirs:
							dirs.append(up)
				if j < self.n - 1:
					if v == g[i][j + 1]:
						if left not in dirs:
							dirs.append(left)
						if right not in dirs:
							dirs.append(right)
				if len(dirs) == 4:
					break
			if len(dirs) == 4:
				break
		return dirs

	def playable(self):
		for i in range(self.n):
			for j in range(self.n):
				if self.grid[i][j] == None:
					# print("\tContains a None cell")
					return True
				if i > 0:
					# up
					if self.grid[i - 1][j] == self.grid[i][j]:
						# print("\tup")
						return True
				if i < self.n - 1:
					# down
					if self.grid[i + 1][j] == self.grid[i][j]:
						# print("\tdown")
						return True
				if j > 0:
					# left
					if self.grid[i][j - 1] == self.grid[i][j]:
						# print("\tleft")
						return True
				if j < self.n - 1:
					# right
					if self.grid[i][j + 1] == self.grid[i][j]:
						# print("\tright")
						return True
		return False
		# init_grid = [row.copy() for row in self.grid]
		# so = self.shift_options
		# moves = []
		# for dir, name in so.items():
		# 	res = self.shift_grid(name)
		# 	moves.append(res)
		# 	if res:
		# 		self.grid = init_grid
		# return len(self.find_empty_cells()) > 0 or any(moves)
		
	def place(self, i, j, v):
		self.grid[i][j] = v
		if self.largest_tile is None:
			self.largest_tile = (i, j, v)
		else:
			max_tile = None
			for p in range(self.n):
				for q in range(self.n):
					gv = self.grid[p][q] if self.grid[p][q] is not None else 0
					if max_tile is None or max_tile[2] < gv:
						max_tile = (p, q, gv)
			self.largest_tile = max_tile

	def gen_random_tile(self):
		empty_cells = self.find_empty_cells()
		if not empty_cells:
			raise ValueError("Game over")
		i, j = rand.choice(empty_cells)
		v = rand.choice(self.random_tile_values)
		self.grid[i][j] = v
		self.score += v
		self.hi_score = max(self.hi_score, self.score)

	def shift_grid(self, direction):
		self.history.append((self.score, self.hi_score, direction, [row.copy() for row in self.grid]))
		direction = direction.lower()
		so = self.shift_options
		init_grid = [row.copy() for row in self.grid]
		def shift():
			for r, row in enumerate(self.grid):
				i = 0
				lr = len(row)
				while i < lr:
					if self.grid[r][i] is not None:
						k = i + 1
						while k < lr:
							if self.grid[r][k] != None:
								break
							k += 1
						if k < lr:
							if self.grid[r][i] == self.grid[r][k]:
								self.place(r, i, self.grid[r][i] * 2)
								self.grid[r][k] = None
								self.score += self.grid[r][i]
								self.hi_score = max(self.hi_score, self.score)
							else:
								k = i
						i = k
					i += 1

			for r in range(len(self.grid)):
				self.grid[r] = [v for v in self.grid[r] if v is not None]
				self.grid[r] += [None for j in range(lr - len(self.grid[r]))]

		if direction == so["UP"]:
			self.grid = np.transpose(self.grid).tolist()
			shift()
			self.grid = np.transpose(self.grid).tolist()
		elif direction == so["DOWN"]:
			self.grid = np.transpose(self.grid).tolist()
			self.grid.reverse()
			for row in self.grid:
				row.reverse()
			shift()
			for row in self.grid:
				row.reverse()
			self.grid.reverse()
			self.grid = np.transpose(self.grid).tolist()
		elif direction == so["RIGHT"]:
			for row in self.grid:
				row.reverse()
			shift()
			for row in self.grid:
				row.reverse()
		# left is default
		else:
			shift()

		if self.grid == init_grid:
			return False

		return True

	def test_move(self, direction):
		temp = G2048(self.n, self.grid.copy())
		return temp.shift_grid(direction)

	def get_record_entry(self):
		return [
			str(datetime.datetime.now()),
			str(self.largest_tile),
			str(len(self.history)),
			str(self.grid)
		]

	def reset(self):
		self.grid = [[None for j in range(self.n)] for i in range(self.n)]
		self.score = 0
		self.history = []

	def undo(self):
		if self.history:
			history_point = self.history.pop()
			score, hi_score, dir, grid = history_point
			self.score = score
			self.hi_score = hi_score
			self.grid = [row.copy() for row in grid]

	def play(self, gen_moves=True):
		once = False
		while self.playable():
			if gen_moves:
				clear()
			print(self)
			if once:
				break
			move_dir = get_move_input()
			if move_dir == "quit":
				break
			valid = self.shift_grid(move_dir)
			if valid:
				clear()
				print(self)
				time.sleep(0.15)
				if gen_moves:
					self.gen_random_tile()
				else:
					once = True
				time.sleep(0.15)
		
		clear()
		print(self)
		print("\n\tGame over!\n\n")
		if self.history:
			for i in range(min(5, len(self.history)), -1, -1):
				move, grid = self.history[-i]
				print(move + "\n" + str(grid) + "\n" + grid_print(grid))

		write = input("\n\tWould you like to save your score?\n\t\t1\t\tyes\n\t\totherwise\tno\n")
		if write == "1":
			write_score(self)

	def __repr__(self):
		res = "\n"
		lenstr_no_none = lambda x : lenstr(x) if x != None else lenstr("-")
		lt = max([max(list(map(lenstr_no_none, row))) for row in self.grid])
		min_width = 2 + lt
		for row in self.grid:
			for val in row:
				res += pad_centre(str(val), min_width) if val is not None else pad_centre("-", min_width)
			res += "\n"
		res += "\n"
		return res
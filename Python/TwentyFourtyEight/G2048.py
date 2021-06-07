import csv
import os
import time
import datetime
import numpy as np
import random as rand
from utility import *
import keyboard as kbd

clear = lambda: os.system('cls')  # on Windows System


class ScoreHistory:

	def __init__(self, date_str, hi_til_loc, score, grid_str):
		self.date_str = date_str
		self.date = datetime.datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
		self.hi_til_loc = list(hi_til_loc.split(", "))
		self.hi_tile_r = int(self.hi_til_loc[0][1:])
		self.hi_tile_c = int(self.hi_til_loc[1])
		self.hi_tile_v = int(self.hi_til_loc[2][:-1])
		self.score = score
		self.grid_str = grid_str

		# self.game = G2048()

	def __eq__(self, other):
		return isinstance(other, ScoreHistory) and all([
			self.date_str == other.date_str,
			self.hi_til_loc == other.hi_til_loc,
			self.score == other.score,
			self.grid_str == other.grid_str
		])

	def __lt__(self, other):
		if not isinstance(other, ScoreHistory):
			raise ValueError("\"{}\" of type \"{}\" cannot be compared to \"{}\"".format(other, type(other), type(self)))
		return self.score < other.score

	def __le__(self, other):
		if not isinstance(other, ScoreHistory):
			raise ValueError("\"{}\" of type \"{}\" cannot be compared to \"{}\"".format(other, type(other), type(self)))
		return self.score <= other.score

	def __repr__(self):
		return "{} on {}".format(self.hi_tile_v, self.date_str)


def grid_print(grid):
	res = "\n"
	lenstr_no_none = lambda x: lenstr(x) if x != None else lenstr("-")
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


def read_high_scores(last_n=None):
	file_name = "score_history.csv"
	delim = ";;"
	n = last_n
	histories = []
	with open(file_name, 'r') as f:
		header = None
		for i, line in enumerate(f.readlines()):
			if i == 0:
				header = [s.strip() for s in line[0].split(delim) if s]
			else:
				# print("line", line)
				l = [s.strip() for s in line.split(delim) if s]
				# d = dict(zip())
				histories.append(ScoreHistory(*l))
			if n and isinstance(n, int) and n > 1:
				if i >= n:
					break
	# print("histories:", histories)
	return histories



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
		edges = [cell for cell in empty_cells if
				 (cell[0] == 0 or cell[0] == self.n - 1) or (cell[1] == 0 or cell[1] == self.n - 1)]

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
		return v, i, j

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
							if self.grid[r][k] is not None:
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
		d = datetime.datetime.now()
		# %Y-%m-%d %H:%M:%f
		d = d.strftime("%Y-%m-%d %H:%M:%S")
		return [
			str(d),
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

		def lenstr_no_none(x):
			return lenstr(x) if x is not None else lenstr("-")

		lt = max([max(list(map(lenstr_no_none, row))) for row in self.grid])
		min_width = 2 + lt
		for row in self.grid:
			for val in row:
				res += pad_centre(str(val), min_width) if val is not None else pad_centre("-", min_width)
			res += "\n"
		res += "\n"
		return res

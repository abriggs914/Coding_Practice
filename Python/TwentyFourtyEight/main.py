import os
import time
import datetime
import random as rand
import numpy as np
from utility import *
from test_suite import *
import keyboard as kbd

class G2048:

	def __init__(self, n=4, init_spaces=None):
	
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
		
	def playable(self):
		for i in range(self.n):
			for j in range(self.n):
				if self.grid[i][j] == None:
					return True
				if i > 0:
					# up
					if self.grid[i - 1][j] == self.grid[i][j]:
						return True
				if i < self.n - 1:
					# down
					if self.grid[i + 1][j] == self.grid[i][j]:
						return True
				if j > 0:
					# left
					if self.grid[i][j - 1] == self.grid[i][j]:
						return True
				if j < self.n - 1:
					# right
					if self.grid[i][j + 1] == self.grid[i][j]:
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
		

	def shift_grid(self, dir):
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
							else:
								k = i
						i = k
					i += 1

			for r in range(len(self.grid)):
				self.grid[r] = [v for v in self.grid[r] if v is not None]
				self.grid[r] += [None for j in range(lr - len(self.grid[r]))]

		if dir == so["UP"]:
			self.grid = np.transpose(self.grid).tolist()
			shift()
			self.grid = np.transpose(self.grid).tolist()
		elif dir == so["DOWN"]:
			self.grid = np.transpose(self.grid).tolist()
			self.grid.reverse()
			for row in self.grid:
				row.reverse()
			shift()
			for row in self.grid:
				row.reverse()
			self.grid.reverse()
			self.grid = np.transpose(self.grid).tolist()
		elif dir == so["RIGHT"]:
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

		self.history.append((dir, [row.copy() for row in self.grid]))
		return True

	def get_record_entry(self):
		return [
			str(datetime.datetime.now()),
			str(self.largest_tile),
			str(len(self.history)),
			str(self.grid)
		]

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

clear = lambda: os.system('cls') #on Windows System

def play_game(gen_moves=True, start_grid=None):
	if start_grid:
		game = G2048(init_spaces=start_grid)
	else:
		game = G2048()
		game.gen_random_tile()
		game.gen_random_tile()
	once = False
	while game.playable():
		if gen_moves:
			clear()
		print(game)
		if once:
			break
		move_dir = get_move_input()
		if move_dir == "quit":
			break
		valid = game.shift_grid(move_dir)
		if valid:
			clear()
			print(game)
			time.sleep(0.15)
			if gen_moves:
				game.gen_random_tile()
			else:
				once = True
			time.sleep(0.15)
	
	clear()
	print(game)
	print("\n\tGame over!\n\n")
	if game.history:
		for i in range(min(5, len(game.history)), -1, -1):
			move, grid = game.history[-i]
			print(move + "\n" + str(grid) + "\n" + grid_print(grid))

	write = input("\n\tWould you like to save your score?\n\t\t1\t\tyes\n\t\totherwise\tno\n")
	if write == "1":
		write_score(game)

def write_score(game):
	file_name = "score_history.csv"
	with open(file_name, 'a') as f:
		f.write("\n" + ";;".join(game.get_record_entry()))
		
	
def move_tests():
	move_test_grid = [[2, None, None, 2], [None, 2, None, None], [None, None, 2, None], [2, 2, 2, 2]]
	moves_test_set = {
		"test_1, testing 1 move up": [
			[
				move_test_grid,
				"up"
			],
			[[4, 4, 4, 4], [None, None, None, None], [None, None, None, None], [None, None, None, None]]
		],
		"test_2, testing 1 move down": [
			[
				move_test_grid,
				"down"
			],
			[[None, None, None, None], [None, None, None, None], [None, None, None, None], [4, 4, 4, 4]]
		],
		"test_3, testing 1 move left": [
			[
				move_test_grid,
				"left"
			],
			[[4, None, None, None], [2, None, None, None], [2, None, None, None], [4, 4, None, None]]
		],
		"test_4, testing 1 move right": [
			[
				move_test_grid,
				"right"
			],
			[[None, None, None, 4], [None, None, None, 2], [None, None, None, 2], [None, None, 4, 4]]
		],
		"test_5, should only make one push not 2": [
			[
				[[None, None, None, 2], [None, None, None, 4], [None, 2, 4, 2], [None, 2, 2, 4]],
				"right"
			],
			[[None, None, None, 2], [None, None, None, 4], [None, 2, 4, 2], [None, None, 4, 4]]
		],
		"test_6, should only make one push not 2": [
			[
				[[None, None, None, 2], [None, None, None, 4], [None, 2, 4, 2], [None, 2, 2, 4]],
				"left"
			],
			[[2, None, None, None], [4, None, None, None], [2, 4, 2, None], [4, 4, None, None]]
		],
		"test_7, testing 2 moves, up then left": [
			[
				move_test_grid,
				[
					"up",
					"left"
				]
			],
			[[8, 8, None, None], [None, None, None, None], [None, None, None, None], [None, None, None, None]]
		],
		"test_8, testing 2 moves, up then right": [
			[
				move_test_grid,
				[
					"up",
					"right"
				]
			],
			[[None, None, 8, 8], [None, None, None, None], [None, None, None, None], [None, None, None, None]]
		],
		"test_9, testing 2 moves, up then up": [
			[
				move_test_grid,
				[
					"up",
					"up"
				]
			],
			[[4, 4, 4, 4], [None, None, None, None], [None, None, None, None], [None, None, None, None]]
		],
		"test_10, testing 2 moves, up then down": [
			[
				move_test_grid,
				[
					"up",
					"down"
				]
			],
			[[None, None, None, None], [None, None, None, None], [None, None, None, None], [4, 4, 4, 4]]
		],
		"test_11, testing 2 moves, down then left": [
			[
				move_test_grid,
				[
					"down",
					"left"
				]
			],
			[[None, None, None, None], [None, None, None, None], [None, None, None, None], [8, 8, None, None]]
		],
		"test_12, testing 2 moves, down then right": [
			[
				move_test_grid,
				[
					"down",
					"right"
				]
			],
			[[None, None, None, None], [None, None, None, None], [None, None, None, None], [None, None, 8, 8]]
		],
		"test_13, testing 2 moves, down then up": [
			[
				move_test_grid,
				[
					"down",
					"up"
				]
			],
			[[4, 4, 4, 4], [None, None, None, None], [None, None, None, None], [None, None, None, None]]
		],
		"test_14, testing 2 moves, down then down": [
			[
				move_test_grid,
				[
					"down",
					"down"
				]
			],
			[[None, None, None, None], [None, None, None, None], [None, None, None, None], [4, 4, 4, 4]]
		],
		"test_15, testing 2 moves, left then left": [
			[
				move_test_grid,
				[
					"left",
					"left"
				]
			],
			[[4, None, None, None], [2, None, None, None], [2, None, None, None], [8, None, None, None]]
		],
		"test_16, testing 2 moves, left then right": [
			[
				move_test_grid,
				[
					"left",
					"right"
				]
			],
			[[None, None, None, 4], [None, None, None, 2], [None, None, None, 2], [None, None, None, 8]]
		],
		"test_17, testing 2 moves, left then up": [
			[
				move_test_grid,
				[
					"left",
					"up"
				]
			],
			[[4, 4, None, None], [4, None, None, None], [4, None, None, None], [None, None, None, None]]
		],
		"test_18, testing 2 moves, left then down": [
			[
				move_test_grid,
				[
					"left",
					"down"
				]
			],
			[[None, None, None, None], [4, None, None, None], [4, None, None, None], [4, 4, None, None]]
		],
		"test_19, testing 2 moves, right then left": [
			[
				move_test_grid,
				[
					"right",
					"left"
				]
			],
			[[4, None, None, None], [2, None, None, None], [2, None, None, None], [8, None, None, None]]
		],
		"test_20, testing 2 moves, right then right": [
			[
				move_test_grid,
				[
					"right",
					"right"
				]
			],
			[[None, None, None, 4], [None, None, None, 2], [None, None, None, 2], [None, None, None, 8]]
		],
		"test_21, testing 2 moves, right then up": [
			[
				move_test_grid,
				[
					"right",
					"up"
				]
			],
			[[None, None, 4, 4], [None, None, None, 4], [None, None, None, 4], [None, None, None, None]]
		],
		"test_22, testing 2 moves, right then down": [
			[
				move_test_grid,
				[
					"right",
					"down"
				]
			],
			[[None, None, None, None], [None, None, None, 4], [None, None, None, 4], [None, None, 4, 4]]
		],
		"test_23, middle shift": [
			[
				[[4, 2, 2, 4], [2, 2, 2, 2], [8, 2, 2, 2], [8, 2, 4, 4]],
				[
					"left"
				]
			],
			[[4, 4, 4, None], [4, 4, None, None], [8, 4, 2, None], [8, 2, 8, None]]
		],
		"test_23 shift right.. again?": [
			[
				[[None, None, None, None], [None, None, None, None], [None, None, None, None], [None, 4, 8, 8]],
				"right"
			],
			[[None, None, None, None], [None, None, None, None], [None, None, None, None], [None, None, 4, 16]]
		]
	}

	valid_move_test_set = {
			"test_1 invalid shift right": [
				[
					[[None, None, None, 2], [None, None, None, 4], [None, None, 4, 8], [None, None, 16, 32]],
					"right"
				],
				False
			],
			"test_2 invalid shift up": [
				[
					[[None, None, None, 2], [None, None, None, None], [None, None, None, None], [None, None, None, None]],
					"up"
				],
				False
			],
			"test_3 valid shift up": [
				[
					[[None, None, None, None], [None, None, None, None], [None, None, None, None], [None, None, None, 2]],
					"up"
				],
				True
			]
		}
	
	playable_test_set = {
		"test_1 still playable": [
			[
				[[None, 4, 8, 2], [8, 16, 4, 8], [16, 32, 16, 8], [32, 64, 128, 512]]
			],
			True
		],
		"test_2 full grid, still playable": [
			[
				[[2, 4, 8, 2], [8, 16, 4, 8], [16, 32, 16, 8], [32, 64, 128, 512]]
			],
			True
		],
		"test_3 full grid, not playable": [
			[
				[[2, 4, 8, 2], [8, 16, 4, 32], [16, 32, 16, 8], [32, 64, 128, 512]]
			],
			False
		]
	}
	
	def test_move(set_places, move):
		game = G2048(init_spaces=set_places)
		if type(move) == list:
			for m in move:
				game.shift_grid(m)
		else:
			game.shift_grid(move)
		return game.grid

	def test_move_validity(set_places, move):
		game = G2048(init_spaces=set_places)
		return game.shift_grid(move)

	def test_still_playable(set_places):
		game = G2048(init_spaces=set_places)
		return game.playable()

		
	run_multiple_tests([
		(test_move, moves_test_set),
		(test_move_validity, valid_move_test_set),
		(test_still_playable, playable_test_set)
	])
		
if __name__ == "__main__":
	
	a = """
	game = G2048()
	# game.gen_random_tile()
	game.place(0, 3, 2)
	game.place(3, 3, 2)
	game.place(3, 1, 4)
	game.place(3, 2, 16)
	game.place(2, 1, 32)
	game.place(1, 2, 16)
	print(game)
	# game.shift_grid(game.shift_options["UP"])
	# game.shift_grid(game.shift_options["DOWN"])
	# game.shift_grid(game.shift_options["LEFT"])
	game.shift_grid(game.shift_options["RIGHT"])
	print(game)
	"""
	# move_tests()
	play_game()
	# play_game(start_grid=[[1, 2, 3, 4],[5, 6, 7, 8],[9, 10, 11, 12],[13, 14, 15, 16]])
	# play_game([[None, None, None, None], [2, None, None, None], [2, None, None, None], [4, 2, 4, 4]])
	# play_game(gen_moves=False, start_grid=[[None, None, None, 2], [None, None, None, 4], [None, 2, 4, 2], [None, 2, 2, 4]])

import os
import time
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
		return len(self.find_empty_cells()) > 0
		
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
		n = self.n
		
		def shift_up(grid):
			grid = np.transpose(grid)
			res = []
			for row in grid:
				l = len(row)
				nr = [c for c in row if c is not None]
				i = 0
				while i < len(nr)-1:
					el = nr[i]
					if el == nr[i+1]:
						nr = nr[:i] + [el * 2] + nr[i+2:]
						i -= 1
					i += 1
					
				row = nr + [None for i in range(l - len(nr))]
				res.append(row)
				
			res = np.transpose(res).tolist()
			return res
			
		def shift_left(grid):
			# grid = np.transpose(grid)
			res = []
			for row in grid:
				l = len(row)
				nr = [c for c in row if c is not None]
				i = 0
				while i < len(nr)-1:
					el = nr[i]
					if el == nr[i+1]:
						nr = nr[:i] + [el * 2] + nr[i+2:]
						i -= 1
					i += 1
					
				row = nr + [None for i in range(l - len(nr))]
				res.append(row)
				
			# res = np.transpose(res)
			return res
			
		def shift_down(grid):
			grid[::-1]
			grid = np.transpose(grid)
			res = []
			for row in grid:
				l = len(row)
				nr = [c for c in row if c is not None]
				i = 0
				while i < len(nr)-1:
					el = nr[i]
					if el == nr[i+1]:
						nr = nr[:i] + [el * 2] + nr[i+2:]
						i -= 1
					i += 1
					
				row = [None for i in range(l - len(nr))] + nr
				res.append(row)
				
			res = np.transpose(res).tolist()
			grid[::-1]
			res[::-1]
			return res
			# grid = np.transpose(grid)
			# res = []
			# for row in grid:
				# l = len(row)
				# nr = [c for c in row if c is not None]
				# i = len(nr)-1
				# while i > 0 and len(nr) > 1:
					# # print("\ti:\t\t" + str(i))
					# el = nr[i]
					# if el == nr[i-1]:
						# # print("\tnr B:\t\t" + str(nr))
						# # print("\tnr[:i]:\t\t" + str(nr[:i-1]))
						# # print("\t[el * 2]:\t" + str([el * 2]))
						# # print("\tnr[i+2:]:\t" + str(nr[i+2:]))
						# # nr = nr[i-2:] + [el * 2] + nr[:i-1]
						# # nr = [el * 2] + nr[:i-1]
						# nr = nr[:i-1] + [el * 2] + nr[i+2:]
						# # print("\tnr A:\t\t" + str(nr))
						# i += 1
					# i -= 1
					
				# row = [None for i in range(l - len(nr))] + nr
				# # print("row: " + str(row))
				# res.append(row)
				
			# res = np.transpose(res)
			# return res
			
		def shift_right(grid):
		# grid = np.transpose(grid)
			grid[::-1]
			res = []
			for row in grid:
				l = len(row)
				nr = [c for c in row if c is not None]
				i = 0
				while i < len(nr)-1:
					el = nr[i]
					if el == nr[i+1]:
						nr = nr[:i] + [el * 2] + nr[i+2:]
						i -= 1
					i += 1
					
				row = [None for i in range(l - len(nr))] + nr
				res.append(row)
				
			# res = np.transpose(res)
			grid[::-1]
			res[::-1]
			return res
		
		
			# # grid = np.transpose(grid)
			# res = []
			# for row in grid:
				# l = len(row)
				# nr = [c for c in row if c is not None]
				# i = len(nr)-1
				# while i > 0 and len(nr) > 1:
					# # print("\ti:\t\t" + str(i))
					# el = nr[i]
					# if el == nr[i-1]:
						# # print("\tnr B:\t\t" + str(nr))
						# # print("\tnr[:i]:\t\t" + str(nr[:i-1]))
						# # print("\t[el * 2]:\t" + str([el * 2]))
						# # print("\tnr[i+2:]:\t" + str(nr[i+2:]))
						# # nr = nr[i-2:] + [el * 2] + nr[:i-1]
						# # nr = [el * 2] + nr[:i-1]
						# nr = nr[:i-1] + [el * 2] + nr[i+2:]
						# # print("\tnr A:\t\t" + str(nr))
						# i += 1
					# i -= 1
					
				# row = [None for i in range(l - len(nr))] + nr
				# # print("row: " + str(row))
				# res.append(row)
				
			# # res = np.transpose(res)
			# return res

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
		# print("done global: " + str(self.grid))
		
		
	def __repr__(self):
		res = "\n"
		lt = self.largest_tile[2] if self.largest_tile is not None else 1
		min_width = 2 + len(str(lt))
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
	# valid = ["W", "A", "S", "D"]
	# legend = ["UP", "LEFT", "DOWN", "RIGHT"]
	# inp = ""
	# while inp.upper() not in valid:
		# inp = input("Up, down, left, or right?")
	# return legend[valid.index(inp.upper())].lower()

clear = lambda: os.system('cls') #on Windows System

def play_game():
	game = G2048()
	game.gen_random_tile()
	game.gen_random_tile()
	while game.playable():
		clear()
		print(game)
		move_dir = get_move_input()
		game.shift_grid(move_dir)
		game.gen_random_tile()
		time.sleep(0.1)
	
	clear()
	print(game)
	print("\n\tGame over!\n\n")
	
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
		"test_5, testing 2 moves, up then left": [
			[
				move_test_grid,
				[
					"up",
					"left"
				]
			],
			[[8, 8, None, None], [None, None, None, None], [None, None, None, None], [None, None, None, None]]
		],
		"test_6, should only make one push not 2": [
			[
				[[None, None, None, 2], [None, None, None, 4], [None, 2, 4, 2], [None, 2, 2, 4]],
				"right"
			],
			[[None, None, None, 2], [None, None, None, 4], [None, 2, 4, 2], [None, None, 4, 4]]
		],
		"test_7, should only make one push not 2": [
			[
				[[None, None, None, 2], [None, None, None, 4], [None, 2, 4, 2], [None, 2, 2, 4]],
				"left"
			],
			[[2, None, None, None], [4, None, None, None], [2, 4, 2, None], [4, 4, None, None]]
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
		
	run_multiple_tests([(test_move, moves_test_set)])
		
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
	# game.shift_grid(game.shift_options["UP"])
	# game.shift_grid(game.shift_options["DOWN"])
	# game.shift_grid(game.shift_options["LEFT"])
	game.shift_grid(game.shift_options["RIGHT"])
	print(game)
	
	move_tests()
	# play_game()
	
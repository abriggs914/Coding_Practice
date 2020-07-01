# Simple connect-4 repl game.
# June 2020

import random as rand
import numpy as np
from player import Player
from board import Board, border
from time import sleep, time
from copy import copy, deepcopy

MOVE_SELECTION_SLEEP_TIME = 1.0
player_color_options = ["Red", "Yellow"]
CONNECT_X = 4
MAX_CONNECT = 51
WIN_CODE = [
	"HORIZONTAL",
	"VERTICAL",
	"DIAGONAL",
	"DRAW"
]

# helper function to return random number in given range
# by default returns float between 0 and 1 exclusive
def random_in_range(upper=0, lower=1, is_int=False):
	if is_int:
		return round((rand.random() * (upper - lower)) + lower) 
	return (rand.random() * (upper - lower)) + lower 
	
# function to validate user input as an int
# can use the range_ param to ensure that the choice is within desired range
# if choice is invalid, default is used
def validate_int(choice, default=0, range_=None):
	#print("validating: {0}, default: {1}, range: {2}".format(choice, default, range_))
	try:
		choice = int(choice)
		if range:
			#range_ = range(min(default, range_+1), max(default, range_+1))
			#print("range_ " + str(range_))
			if choice not in range_:
				choice = default
	except:
		choice = default
	#print("Validated: {0}".format(choice))
	return choice
	
	
class Connect_Four:
	def __init__(self):
		self.board = None
		self.players = None
		self.playing = False
		self.moves_made = None
		self.player_turn = None
		self.CONNECT_X = CONNECT_X
		
	def __repr__(self):			
		repr = "\n"
		repr += str(self.board)
		repr += "\nFirst to {0} wins!\n".format(self.CONNECT_X)
		repr += "\n\tPlayers legend:\n"
		repr += str(self.players[0]) + "\n"
		repr += str(self.players[1]) + "\n"
		repr += border + "\n"
		return repr
		
	def test_connect_four(self, board, players):
		self.board = board
		self.players = players
		self.moves_made = 0
		self.playing = True
		
	def get_player_info(self):
		player_name = input("\nWhat is your name?\n\n").strip().title()
		m = "\nWhat color do you want?\n"
		for c in range(len(player_color_options)):
			m += "\n\t" + str(c + 1) + "\t" + player_color_options[c]
		m += "\n\n"
		player_color = player_color_options[validate_int(input(m), 1, range(1, len(player_color_options) + 1)) - 1]
		return Player(player_name, player_color)
	
	def set_computer_info(self, player):
		c = player_color_options[0] if player.color != player_color_options[0] else player_color_options[1]
		return Player("Bot", c)
		
	def game_setup(self):
		player_info = self.get_player_info()
		computer_info = self.set_computer_info(player_info)
		
		n_rows = validate_int(input("\n\nHow many rows in the board?\n\n"), CONNECT_X, range(CONNECT_X, MAX_CONNECT))
		n_cols = validate_int(input("\n\nHow many columns in the board?\n\n"), CONNECT_X, range(CONNECT_X, MAX_CONNECT))
		
		connect_max = min(n_rows, n_cols)
		self.CONNECT_X = validate_int(input("\nAnd how many markers do you want to \"connect\" to win?\n\n"), CONNECT_X, range(2, connect_max + 1))
		
		self.players = [player_info, computer_info]
		print_size = max([len(player.name) for player in self.players])
		print("PRINT_SIZE:", print_size)
		for player in self.players:
			player.set_print_size(print_size)
		
		self.board = Board(n_rows, n_cols)
		self.playing = True
		self.moves_made = 0
		
	# used to pass in pre-validated values and initialize a game
	def create_game(self, players, connect_x, n_rows, n_cols):
		self.CONNECT_X = connect_x
		self.players = players
		print_size = max([len(player.name) for player in self.players])
		print("PRINT_SIZE:", print_size)
		for player in self.players:
			player.set_print_size(print_size)
		
		self.board = Board(n_rows, n_cols)
		self.playing = True
		self.moves_made = 0
		
	def check_space(self, space):
		x = 1
		c = None
		#print("checking space ({0})".format(len(space)), space, x, c)
		for i in range(len(space)):
			s = space[i]
			m = "len: {0}, space: {1}, x: {2}, s: {3}, c: {4}".format(len(space), space, x, s, c)
			if s:
				if c is None:
					c = s
					x = 1
				elif s == c:
					c = s
					x += 1
				else:
					c = s
					x = 1
			else:
				x = 0
			m += "\t" + "x: {0}, s: {1}, c: {2}".format(x, c, s)
			#print(m)
			if x == self.CONNECT_X:
				return True
			if x + len(space) - i < self.CONNECT_X:
				# not enough space in the row to make a connection
				break
		return False
		
	def check_horizontal(self, row, col):
		l = max(0, min(col - self.CONNECT_X, self.board.cols - 1))
		r = max(0, min(col + self.CONNECT_X, self.board.cols - 1))
		space = self.board.status[row][l:r + 1]
		return (WIN_CODE[0], self.check_space(space))
		
	def check_vertical(self, row, col):
		transpose = np.transpose(self.board.status)
		l = max(0, min(row - self.CONNECT_X, self.board.rows - 1))
		r = max(0, min(row + self.CONNECT_X, self.board.rows - 1))
		space = transpose[col][l:r + 1]
		return (WIN_CODE[1], self.check_space(space))
		
	def check_diagonals(self):
		tl_br_range = range((-1 * self.board.rows) + 1, self.board.cols)
		reverse = [r.copy() for r in self.board.status]
		for r in reverse:
			r.reverse()
			
		tr_bl_range = range((-1 * len(reverse)) + 1, len(reverse[0]))
		# print("tl_br_range", tl_br_range)
		# print("tr_bl_range", tr_bl_range)
		# print("STATUS\n", np.asarray(self.board.status))
		# print("REVERSE\n", np.asarray(reverse))
		# print("IS DIFFERENT:", (self.board.status == reverse) == False)
		
		win = False
		for i in tl_br_range:
			tl_br_diagonal = np.diagonal(self.board.status, i)
			tr_bl_diagonal = np.diagonal(reverse, i)
			if len(tl_br_diagonal) >= self.CONNECT_X:
				win = self.check_space(tl_br_diagonal)
			if not win and len(tr_bl_diagonal) >= self.CONNECT_X:
				win = self.check_space(tr_bl_diagonal)
			#print("\ni:",i)
			#print("\ttl_br_diagonal:", tr_bl_diagonal)
			#print("\ttr_bl_diagonal:", tl_br_diagonal)
			if win:
				break
		return (WIN_CODE[2], win)
		
	def check_win(self, do_sleep=True, do_print=True):
		rows = self.board.rows
		cols = self.board.cols
		code = None
		win = False
		#print("checking win (", rows, ",", cols, ")")
		for r in range(rows):
			for c in range(cols):
				if self.board.status[r][c]:
					#print("checking horizontal")
					#start_time = time()
					code, win = self.check_horizontal(r, c)
					#end_time = time()
					#print("finished horizontal {0}".format(end_time - start_time))
					if not win:
						#print("checking vertical")
						#start_time = time()
						code, win = self.check_vertical(r, c)
						#end_time = time()
						#print("finished vertical {0}".format(end_time - start_time))
				if win:
					break
			if win:
				break
		
		if not win:
			#print("checking diagonal")
			#start_time = time()
			code, win = self.check_diagonals()
			#end_time = time()
			#print("finished diagonal {0}".format(end_time - start_time))
		if win and do_print:
			print("{0} win found!".format(code))
		return (code, win)
		
	def turn_change(self):
		self.player_turn = not self.player_turn
		
	def random_move(self):
		valid = False
		cols = self.board.remaining_cols()
		r, c = None, None
		if cols:
			c = rand.choice(cols)
			r = self.board.next_row(c)
		
		#while not valid:
		#	if not cols:
		#		break
		#	#r = random_in_range(0, self.board.rows-1, True)
		#	c = random_in_range(0, self.board.cols-1, True)
		#	r = self.board.next_row(c)
		#	print("cols list:", cols, "c", c)
		#	cols.remove(c)
		#	if r > -1 and self.board.status[r][c] is None:
		#		valid = True
		return r, c
		
	def make_move(self):
		valid = False
		while not valid:
			default_cols = random_in_range(0, self.board.cols, True)
			c = validate_int(input("\nWhich col?\n"), default_cols, range(self.board.cols))
			r = self.board.next_row(c)
			if r > -1 and self.board.status[r][c] is None:
				valid = True
			else:
				print("Invalid move.\nPlease select one of {0}".format(self.board.available_cols()))
		print("You selected row {0}, col {1}".format(r, c))
		sleep(MOVE_SELECTION_SLEEP_TIME)
		return r, c
		
	# simulates a random move for the computer
	def cpu_move(self, do_sleep=True):
		r, c = self.random_move()
		print("Computer selected row {0}, col {1}".format(r, c))
		if do_sleep:
			sleep(MOVE_SELECTION_SLEEP_TIME)
		return r, c
		
	# attempts to simulate a monte carlo type move for the computer
	# score			-		The weight to scale the outcome of the simulations
	# max_moves		-		How many moves the AI will play
	# depth			-		How many games the AI will play
	# do_sleep 		-		Used in the REPL version to give time for reading output
	# do_print		-		Used to show output in the REPL version
	def cpu_monte_carlo(self, score=10, max_moves=None, depth=None, do_sleep=True, do_print=True):
		start_time = time()
		if not max_moves:
			max_moves = self.board.size - self.moves_made
		if not depth:
			depth = 100
		
		spaces_left_on_board = self.board.size - self.moves_made
		spaces_left = max_moves
		remaining_cols = self.board.remaining_cols()
		shortest_moves_to_win = 0
		
		original = deepcopy(self)
		original_board = deepcopy(original.board)
		
		col_scores = dict(zip(remaining_cols, [0 for i in range(len(remaining_cols))]))
		
		# loop depth
		for i in range(depth):
			used_cols = []
			win = False
			win_cpu = False
			# loop columns
			for j in range(0, spaces_left, 2):
				# cpu move
				row_cpu, col_cpu = self.random_move()
				self.board.mark(row_cpu, col_cpu, self.players[1])
				
				used_cols.append(col_cpu)
				code, win = self.check_win(do_sleep, do_print)
				if win:
					win_cpu = True
					break
				
				# player move
				row_player, col_player = self.random_move()
				self.board.mark(row_player, col_player, self.players[0])
				
				used_cols.append(col_cpu)
				code, win = self.check_win(do_sleep, do_print)
				if win:
					break
			
			# update cols dict
			moves = len(used_cols)
			game_score = score * (moves * (1 - (moves / (spaces_left_on_board + 1))))
			for col in used_cols:
				#print("cols used: " + str(col))
				if win:
					if win_cpu:
						col_scores[col] += game_score
					else:
						col_scores[col] -= game_score
			
			# reset working board
			self.board = deepcopy(original_board)
			
		# reset board
			self = deepcopy(original)
			self.board = deepcopy(original_board)
		#print("size:", self.board.size, "spaces_left:", spaces_left, "remaining cols", remaining_cols)
		if do_print:
			print("scores", col_scores)
		if do_sleep:
			sleep(3)
		best_col = None
		best_score = None
		tied_scores = []
		for col, score in col_scores.items():
			if not best_col or score > best_score:
				best_col = col
				best_score = score
				tied_scores = [(best_col, best_score)]
			elif not best_col or score == best_score:
				tied_scores.append((col, score))
		if do_print:
			print("best_col", best_col, "best_score:", best_score)
		if do_sleep:
			sleep(3)
		if len(tied_scores) > 1:
			best_col, best_score = rand.choice(tied_scores)
		
		r, c = self.board.next_row(best_col), best_col
		print("Computer selected row {0}, col {1}".format(r, c))
		if do_sleep:
			sleep(MOVE_SELECTION_SLEEP_TIME)
		end_time = time()
		how_long = end_time - start_time
		return r, c, {"best_col":best_col, "best_score":best_score, "time":how_long}
		
	def play(self):
		print(border + "\nWelcome to Connect Four!")
		self.game_setup()
		print(self)
		
		# 50/50 coin flip to decide who goes first
		self.player_turn = random_in_range(0, 1, True) == 0
		curr_player = self.players[0] if self.player_turn else self.players[1]
		
		if self.player_turn:
			print("\n\t--\tYou will go first\t--\n")
		else:
			print("\n\t--\tThe computer will go first\t--\n")
		
		# main game loop
		while self.playing:
			print(self)
		
			if self.player_turn:
				r, c = self.make_move()
				data = {}
			else:
				max_moves = round((self.board.size - self.moves_made) * 0.6)
				r, c, data = self.cpu_monte_carlo(do_print=False)
				# r, c = self.cpu_move()  # for a random move
				
			# mark the board
			curr_player.update_history((r, c), data)
			self.board.mark(r, c, curr_player, True)
			self.moves_made += 1
			
			code, win = self.check_win()
			self.playing = not win
			if (win):
				print("\n\tWinner found on the {}!\n".format(code))
				if self.player_turn:
					print("\n\t{0} is the winner!\n\tCongrats!".format(curr_player.name))
				else:
					print("\n\t{0} is the winner.\n\tBetter luck next time!".format(curr_player.name))
				print(self)
			
			if self.moves_made == self.board.size:
				print("\n\n\tBoard is filled.\n\tNo winner found,\n\tit's a tie.\n")
				self.playing = False
				print(self)
			self.turn_change()
			curr_player = self.players[0] if self.player_turn else self.players[1]
			
			
def main():

	connect_4 = Connect_Four()
	connect_4.play()

if __name__ == "__main__":
	main()

# -- Testing --
#######################################################################################################################
def perform_move_test():
	connect_4 = Connect_Four()
	test_board = Board(10, 10)
	test_players = [Player("Test_player", player_color_options[0])]
	test_players.append(connect_4.set_computer_info(test_players[0]))
	
	connect_4.test_connect_four(test_board, test_players)
	print(connect_4)
	print(connect_4.board.next_row(0))

# TODO:
#
# This entire thing is busted as of right now. I need to adjust this for the fact that you dont get to pick the row
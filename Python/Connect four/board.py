
import numpy as np
from time import sleep
from os import system

border = "".join(["#" for i in range(100)])

class Board:
	def __init__(self, rows, cols):
		#self.rows = max(4, min(rows, 50))
		#self.cols = max(4, min(cols, 50))
		self.cols = cols
		self.rows = rows
		self.size = self.rows * self.cols
		self.status = self.gen_none_list(rows, cols)
		#print("status", self.status)
		# used for the GUI version to see which player is associated with the mark
		self.player_marks = self.gen_none_list(rows, cols)
		
	def available_cols(self):
		transpose = np.transpose(self.status)
		return ", ".join([str(i) for i in range(self.cols) if None in transpose[i]])
		
	# returns the row index of the next available space in given column of the board
	# returns -1 if no available rows in the desired column
	def next_row(self, col):
		row = [self.status[r][col] for r in range(self.rows - 1, -1, -1)]
		selected_row = len(row)
		if None in row:
			selected_row = row.index(None)
		#print("Next row in column {0} is {1} row: {2}".format(col, (len(row) - 1 - selected_row), row))
		return len(row) - 1 - selected_row
		
	# marks the board at row, col for the given player
	# either 'R' or 'B'
	def mark(self, r, c, player, animate=False):
		if animate:
			self.animate(r, c, player)
		self.status[r][c] = player.color[0].upper()
		self.player_marks[r][c] = player
		
	def animate(self, r, c, player):
		print("OG c: " + str(c))
		sym = player.color[0].upper()
		repr = str(self)
		splt = repr.split("\n")
		sleep_time = 0.09
		gravity = 0.98
		for i in range(4, (len(splt) - 3) - (self.rows - r - 1)):
			col = (c * 3) + 12
			#print("BEFORE LINE\t{" + str(splt[i]) + "} #" + str(len(splt[i])))
			#print("col",col, "first split {" + str(splt[i][:col]) + "}, next: {" + str(splt[i][:col]) + "}")
			splt[i] = splt[i][:col] + sym + splt[i][col + 1:]
			new_repr = "\n".join(splt)
			system("cls")
			print(new_repr)
			sleep(sleep_time)
			sleep_time *= gravity
			if i < 6:
				splt[i] = splt[i][:col] + " " + splt[i][col + 1:]
			else:
				splt[i] = splt[i][:col] + "_" + splt[i][col + 1:]
			#print("AFTERLINE\t{" + str(splt[i]) + "} #" + str(len(splt[i])))
		system("cls")
			
		#print("ANIMATING\n{\n", repr, "\n}\n")
		#print("LENGTH:", repr.split("\n"), (len(repr.split("\n"))))
		
	def remaining_cols(self):
		return [col for col in range(self.cols) if self.next_row(col) > -1]
		
	def gen_none_list(self, rows, cols):
		return [[None for c in range(cols)] for r in range(rows)]
		
	def create_board(self, board_status, players):
		rows = len(board_status)
		cols = len(board_status[0])
		user = players[0]
		bot = players[1]
		user_color = user.color[0].upper()
		bot_color = bot.color[0].upper()
		new_status = self.gen_none_list(rows, cols)
		new_player_marks = self.gen_none_list(rows, cols)
		board = Board(rows, cols)
		for r in range(rows):
			for c in range(cols):
				if board_status[r][c] is not None:
					new_status[r][c] = board_status[r][c]
					if board_status[r][c] == user_color:
						new_player_marks[r][c] = user
					else:
						new_player_marks[r][c] = bot
					
		board.status = new_status
		board.player_marks = new_player_marks
		return board
		
	def __repr__(self):
		tab = "    "
		b = border + "\n"
		b += tab + "Board: (" + str(self.rows) + " x " + str(self.cols) + ")\n\n"
		b += tab + "  " + "C".center(5) + "".join([str(i).center(3) for i in range(self.cols)])
		b += "\n" + tab + "".ljust((self.cols * 3) + 9)
		b += "\n" + tab + "R".center(8) + "".ljust(self.cols * 3) + "\n"
		#print("b\n" + b)
		for r in range(self.rows):
			b += tab + str(r).center(3) + tab
			for c in range(self.cols):
				#print("r", r, "c", c)
				if not self.status[r][c]:
					b += "_".center(3)
				else:
					b += self.status[r][c].center(3)
			b += "\n"
		b += "\n" + tab + "  " + "C".center(5) + "".join([str(i).center(3) for i in range(self.cols)])
		b += "\n" + border
		return b
		
class Player:
	def __init__(self, name, color):
		self.name = name
		self.color = color
		self.print_size = 15 # default value
		self.move_history = {}
		
	def __repr__(self):
		return "{0}, playing {1}.".format(self.name.ljust(self.print_size, " "), self.color.title())
		
	def set_print_size(self, print_size):
		self.print_size = print_size
		
	def update_history(self, *move_choice):
		move_n = len(self.move_history) + 1
		self.move_history[str(move_n)] = move_choice
		
	def print_move_history(self):
		for move_n, move in self.move_history.items():
			print("{0}:\t{1}".format(move_n, move))
		

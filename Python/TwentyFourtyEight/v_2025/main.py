import random


class GameEndException(Exception):
	def __init__(self, msg=""):
		msg = "Game Over.\n" + msg
		super().__init__(msg)


class GridFullException(Exception):
	def __init__(self, msg=""):
		msg = "Grid is full!.\n" + msg
		super().__init__(msg)


def print_grid(grid, space_size: int = 4):
	res = "|" + "".join(["=" * space_size for j in range(len(grid[0]))]) + "|\n   "
	for i, row in enumerate(grid):
		for j, val in enumerate(row):
			if val == 0:
				res += " " * space_size
			else:
				res += str(val).ljust(space_size)
		if i < (len(grid) - 1):
			res += "\n   "
	res = res + "\n|" + "".join(["+" * space_size for j in range(len(grid[0]))]) + "|\n"
	print(res)
	return res
	

def grid_turn(grid, n_new: int = 1, new_vals: tuple[int] = (2, 4)):
	spaces = grid_empties(grid)
	
	if len(spaces) < n_new:
		raise GridFullException(f"Cannot add new blocks.")
	
	for i in range(n_new):
		chx_i, chx_j = random.choice(spaces)
		grid[chx_i][chx_j] = random.choice(new_vals)
		
	if (len(spaces) - n_new) == 0:
		if not playable(grid):
			raise GridFullException(f"No more blocks can be added.")
		
	return grid
	
	
def playable(grid) -> bool:
	for i in range(len(grid)):
		for j in range(len(grid[i])):
			val = grid[i][j]
			if val != 0:
				if j < (len(grid[i]) - 1):
					val_right = grid[i][j + 1]
					if val == val_right:
						return True
				if i < (len(grid) - 1):
					val_below = grid[i + 1][j]
					if val == val_below:
						return True
			else:
				return True
	return False
	
	
def transpose(grid):	
	r, c = len(grid), len(grid[0])
	g = [[0 for j in range(r)] for i in range(c)]
	for i in range(r):
		for j in range(c):
			g[j][i] = grid[i][j]
	return g
	
	
def grid_sum(grid) -> int:
	return sum([sum(row) for row in grid])


def grid_hi_score(grid) -> int:
	return max([max(row) for row in grid])


def grid_avg_score(grid) -> int:
	w = [sum(row) / len(row) for row in grid]
	return sum(w) / len(w)


def grid_avg_nz_score(grid) -> int:
	rs = []
	for i, row in enumerate(grid):
		s = sum(row)
		n_nz = len([v for v in row if v != 0])
		rs.append(s / n_nz if n_nz else 0)
	return sum(rs) / len(rs)
	
	
def grid_empties(grid) -> list[tuple[int, int]]:
	spaces = []
	for i, row in enumerate(grid):
		for j, val in enumerate(row):
			if val == 0:
				spaces.append((i, j))
	return spaces
	

def game_at(grid, score) -> bool:
	for row in grid:
		for val in row:
			if val >= score:
				return True
	return False
	

def sample_moves(grid, idx: int = 0, mode: str = "space"):
	
	testing = True
	
	move_hierarchy = [
		"d",
		"s",
		"a",
		"w"
	]

	grids = {k: grid_move([row.copy() for row in grid], k) for k in move_hierarchy}
	scores = {k: grid_sum(grids[k]) for k in move_hierarchy}
	hi_scores = {k: grid_hi_score(grids[k]) for k in move_hierarchy}
	avg_scores = {k: grid_avg_score(grids[k]) for k in move_hierarchy}
	avg_nz_scores = {k: grid_avg_nz_score(grids[k]) for k in move_hierarchy}
	spaces = {k: len(grid_empties(grids[k])) for k in move_hierarchy}
	
	by_space = sorted(list(spaces.items()), key=lambda tup: (tup[1], len(move_hierarchy) - move_hierarchy.index(tup[0])), reverse=True)
	#by_score = sorted(list(avg_nz_scores.items()), key=lambda tup: (tup[1], -move_hierarchy.index(tup[0])), reverse=True)
	by_score = sorted(list(hi_scores.items()), key=lambda tup: (tup[1], len(move_hierarchy) - move_hierarchy.index(tup[0])), reverse=True)

	if testing:
		#for k, g in grids.items():
		#	print(f"{k=} s={scores[k]}, hs={hi_scores[k]}, as={avg_scores[k]}, e={spaces[k]}")
		#	print_grid(g, space_size=6)
		
		print(f"scores      : {list(scores.items())}")
		print(f"hi_scores   : {list(hi_scores.items())}")
		print(f"avg_scores  : {list(avg_scores.items())}")
		print(f"avgvz_scores: {list(avg_nz_scores.items())}")
		print(f"spaces      : {list(spaces.items())}")
		print(f"mode        : {mode}")
		print(f"idx        : {idx}")
		print(f"by_score    : {by_score}")
		print(f"by_space    : {by_space}")
		print(f"result      : {by_space[idx][0] if (mode.strip().lower() == 'space') else by_score[idx][0]}")
		print(f"#"*20)
	if mode.strip().lower() == "space":
		#print(f"{by_space=}")
		return by_space[idx][0]
	else:
		#print(f"{by_score=}")
		return by_score[idx][0]
	

def grid_move(grid, move: str):
	g = []
	if move.strip().lower() == "d":
		# right
		for i, row_ in enumerate(grid):
			row = row_.copy()
			j = len(row) - 1
			val = row[j]
			ca = None
			while j > 0:
				val = row[j]
				prev_val = row[j - 1]
				if (val == 0) or (val == prev_val):
					if ca and (ca[1] == prev_val) and ((ca[0] - 1) == j):
						row = [0] + row[:ca[0] - 1] + [ca[1] + prev_val] + row[ca[0] + 1:]
						row[ca[0] - 1] = 0
					else:
						row = [0] + row[:j - 1] + [val + prev_val] + row[j + 1:]
					j_c = j
					if (val == 0) and sum(row[:j]):
						j = len(row)
					ca = None if val != 0 else (j_c, row[j_c])
				j -= 1
			g.append(row.copy())
	
	elif move.strip().lower() == "a":
		# left
		g = [row[::-1] for row in grid]
		g = grid_move(g, "d")
		g = [row[::-1] for row in g]
	
	elif move.strip().lower() == "s":
		# down
		g = transpose(grid)
		g = grid_move(g, "d")
		g = transpose(g)
	
	elif move.strip().lower() == "w":
		# up
		g = transpose(grid)
		g = [row[::-1] for row in g]
		g = grid_move(g, "d")
		g = [row[::-1] for row in g]
		g = transpose(g)
	
	return g
	

if __name__ == "__main__":
	
	
	def test_1():
		n_rows = 4
		n_cols = 4
		grid = [[0 for j in range(n_cols)] for i in range(n_rows)]
		
		grid[0][0] = 2
		grid[1][0] = 2
		grid[2][0] = 4
		grid[3][0] = 2
		
		grid[0][1] = 2
		grid[1][1] = 2
		grid[2][1] = 2
		grid[3][1] = 2
		
		grid[3][2] = 2
		grid[3][3] = 2
		grid_turn(grid)
		print_grid(grid)
		# move = input("Enter a move:\n\t" + "\n\t".join([f"{i}\t{v}" for i, v in enumerate(["w\tup", "s\tdown", "a\tleft", "d\tright"])]) + "\n")
		move = "d"
		grid = grid_move(grid, move)
		print_grid(grid)
	
	
	def test_2():
		n_rows = 10
		n_cols = 10
		grid = [[0 for j in range(n_cols)] for i in range(n_rows)]
		
		for i in range(n_rows):
			for j in range(i, n_rows):
				grid[i][j] = 2

		grid[7][0] = 2
		grid[7][1] = 4
		grid[7][3] = 16
		grid[7][5] = 16

		#for i in range(12):
		#	grid_turn(grid, new_vals=(2, 4, 8, 16, 32))
		
		print_grid(grid)
		# move = input("Enter a move:\n\t" + "\n\t".join([f"{i}\t{v}" for i, v in enumerate(["w\tup", "s\tdown", "a\tleft", "d\tright"])]) + "\n")
		move = "d"
		grid = grid_move(grid, move)
		print(f"LEFT")
		print_grid(grid)
		
		move = "a"
		grid = grid_move(grid, move)
		print(f"RIGHT")
		print_grid(grid)
		
		move = "s"
		grid = grid_move(grid, move)
		print(f"DOWN")
		print_grid(grid)
		
		move = "w"
		grid = grid_move(grid, move)
		print(f"UP")
		print_grid(grid)
	
	
	def test_3():
		n_rows = 10
		n_cols = 10
		grid = [[0 for j in range(n_cols)] for i in range(n_rows)]

		grid[0][0] = 2
		grid[1][0] = 4
		grid[2][0] = 8
		grid[3][0] = 16
		grid[4][0] = 32
		grid[5][0] = 64
		grid[6][0] = 128
		grid[7][0] = 256
		grid[8][0] = 512
		grid[9][0] = 1024

		#for i in range(12):
		#	grid_turn(grid, new_vals=(2, 4, 8, 16, 32))
		
		print_grid(grid, 5)
		# move = input("Enter a move:\n\t" + "\n\t".join([f"{i}\t{v}" for i, v in enumerate(["w\tup", "s\tdown", "a\tleft", "d\tright"])]) + "\n")
		move = "w"
		grid = grid_move(grid, move)
		print(f"UP")
		print_grid(grid, 5)
		
		
	def test_4():
		n_rows = 10
		n_cols = 10
		num_size = 8
		tries_while_stuck_left = 2
		tries_while_stuck_up = 6
		game_at_score = 2048 * 16
		new_vals = (2, 4)
		new_pieces_per_turn = 2
		grid = [[0 for j in range(n_cols)] for i in range(n_rows)]
		
		#for i in range(12):
		#	grid_turn(grid, new_vals=(2, 4, 8, 16, 32))
		
		#print_grid(grid)
		
		move_map = {
			"w": "UP",
			"s": "DOWN",
			"a": "LEFT",
			"d": "RIGHT"
		}		
		
		run = True
		turns = 0
		move_choices = ["s", "d"]
		move_summary = []
		while run:
			turns += 1
			try:
				grid = grid_turn(grid, n_new=new_pieces_per_turn, new_vals=new_vals)
				
				g_a = [row.copy() for row in grid]
				g_b = [row.copy() for row in grid]
				count_stuck_left = 0
				count_stuck_up = 0
				while g_a == g_b:
					move = random.choice(move_choices)
					grid = grid_move(g_a, move)
					g_b = [row.copy() for row in grid]
					count_stuck_left += 1
					if count_stuck_left >= tries_while_stuck_left:
						if "a" not in move_choices:
							move_choices.append("a")
					if count_stuck_up >= tries_while_stuck_up:
						if "w" not in move_choices:
							move_choices.append("w")
					#print(f"{move=}, {move_choices=}, {count_stuck_left=}")
				
				if "a" in move_choices:
					move_choices.remove("a")
				if "w" in move_choices:
					move_choices.remove("w")
				
				move_summary.append(move)
				if turns % 10 == 0:
					print(f"Turn# {turns} - {move_map[move]}\t\t\t{grid_sum(grid)}")
					print_grid(grid, space_size=num_size)
					
				if game_at(grid, game_at_score):
					raise ValueError(f"Game - reached {game_at_score} points!")
			except GridFullException as gfe:
				run = False
				print(gfe)
				print(f"Final:")
				print_grid(grid, space_size=num_size)
				
		print(f"{turns=}")
		for k, move in move_map.items():
			print(f"{move}\t-\t{move_summary.count(k)}")
	

	def test_5():
		raise GridFullException("Here")
	
	
	def test_6():
		n_rows = 10
		n_cols = 10
		num_size = 8
		tries_while_stuck_left = 2
		tries_while_stuck_up = 6
		game_at_score = 2048 * 16
		new_vals = (2, 4)
		new_pieces_per_turn = 2
		grid = [[0 for j in range(n_cols)] for i in range(n_rows)]
		
		#for i in range(12):
		#	grid_turn(grid, new_vals=(2, 4, 8, 16, 32))
		
		#print_grid(grid)
		
		move_map = {
			"w": "UP",
			"s": "DOWN",
			"a": "LEFT",
			"d": "RIGHT"
		}		
		
		run = True
		turns = 0
		move_choices = ["s", "d"]
		move_summary = []
		while run:
			turns += 1
			try:
				grid = grid_turn(grid, n_new=new_pieces_per_turn, new_vals=new_vals)
				
				g_a = [row.copy() for row in grid]
				g_b = [row.copy() for row in grid]
				count_stuck_left = 0
				count_stuck_up = 0
				while g_a == g_b:
					move = random.choice(move_choices)
					grid = grid_move(g_a, move)
					g_b = [row.copy() for row in grid]
					count_stuck_left += 1
					if count_stuck_left >= tries_while_stuck_left:
						if "a" not in move_choices:
							move_choices.append("a")
					if count_stuck_up >= tries_while_stuck_up:
						if "w" not in move_choices:
							move_choices.append("w")
					#print(f"{move=}, {move_choices=}, {count_stuck_left=}")
				
				if "a" in move_choices:
					move_choices.remove("a")
				if "w" in move_choices:
					move_choices.remove("w")
				
				move_summary.append(move)
				if turns % 10 == 0:
					print(f"Turn# {turns} - {move_map[move]}\t\t\t{grid_sum(grid)}")
					print_grid(grid, space_size=num_size)
					
				if game_at(grid, game_at_score):
					raise ValueError(f"Game - reached {game_at_score} points!")
			except GridFullException as gfe:
				run = False
				print(gfe)
				print(f"Final:")
				print_grid(grid, space_size=num_size)
				
		print(f"{turns=}")
		for k, move in move_map.items():
			print(f"{move}\t-\t{move_summary.count(k)}")
		
		print(f"Last 20 moves")
		print(f"{move_summary[-20:][::-1]}")
			
		print("Final Moves:")
		print_grid(grid, space_size=num_size)
		
		print("Final Move LEFT")
		g_a = grid_move([row.copy() for row in grid], "a")
		print_grid(g_a, space_size=num_size)
		
		print("Final Move UP")
		g_w = grid_move([row.copy() for row in grid], "w")
		print_grid(g_w, space_size=num_size)
		
		print("Final Move Right")
		g_d = grid_move([row.copy() for row in grid], "d")
		print_grid(g_d, space_size=num_size)
		
		print("Final Move DOWN")
		g_s = grid_move([row.copy() for row in grid], "s")
		print_grid(g_s, space_size=num_size)
		
		print(sample_moves(grid))

	
	def test_7():
		# 10 x 10
		n_rows = 10
		n_cols = 10
		num_size = 9
		tries_while_stuck_0 = 2
		tries_while_stuck_1 = 4
		tries_while_stuck_2 = 8
		game_at_score = 2048 * 16 * 16 * 2 * 2
		show_every_n_turns = 500
		new_vals = (2, 4)
		new_pieces_per_turn = 2
		move_choices_start = [0]
		greedy_mode = "space"
		
		# 4 x 4
		n_rows = 4
		n_cols = 4
		num_size = 6
		tries_while_stuck_0 = 2
		tries_while_stuck_1 = 3
		tries_while_stuck_2 = 4
		game_at_score = 2048 * 16 * 16 * 2 * 2
		show_every_n_turns = 10
		new_vals = (2, 4)
		new_pieces_per_turn = 1
		move_choices_start = [0]
		greedy_mode = "space"
		
		
		grid = [[0 for j in range(n_cols)] for i in range(n_rows)]
		
		#for i in range(12):
		#	grid_turn(grid, new_vals=(2, 4, 8, 16, 32))
		
		#print_grid(grid)
		
		move_map = {
			"w": "UP",
			"s": "DOWN",
			"a": "LEFT",
			"d": "RIGHT"
		}		
		
		run = True
		turns = 0
		#move_choices = ["s", "d"]
		move_summary = []
		last_grid = None
		while run:
			turns += 1
			try:
				last_grid = [row.copy() for row in grid]
				grid = grid_turn(grid, n_new=new_pieces_per_turn, new_vals=new_vals)
				
				g_a = [row.copy() for row in grid]
				g_b = [row.copy() for row in grid]
				count_stuck_0 = 0
				count_stuck_1 = 0
				count_stuck_2 = 0
				g_idx = 0
				move_choices = move_choices_start.copy()
				while g_a == g_b:
					#move = random.choice(move_choices)
					move = sample_moves(g_a, random.choice(move_choices), greedy_mode)
					g_b = [row.copy() for row in grid]
					g_b = grid_move(g_b, move)
					count_stuck_0 += 1
					if count_stuck_0 >= tries_while_stuck_0:
						count_stuck_1 += 1
						#if "a" not in move_choices:
						if 1 not in move_choices:
							#move_choices.append("a")
							move_choices.append(1)
					if count_stuck_1 >= tries_while_stuck_1:
						count_stuck_2 += 1
						#if "w" not in move_choices:
						if 2 not in move_choices:
							#move_choices.append("w")
							move_choices.append(2)
					if count_stuck_2 >= tries_while_stuck_2:
						#if "w" not in move_choices:
						if 3 not in move_choices:
							#move_choices.append("w")
							move_choices.append(3)
					#print(f"t={turns}, {move=}, {move_choices=}, cs0={count_stuck_0}, cs1={count_stuck_1}, cs2={count_stuck_2}")
					#if (count_stuck_0 + count_stuck_1 + count_stuck_2 % tries_while_stuck_2) % 100 == 0:
					#	print("#" * 80)
					#	print(f"a={g_a}\nb={g_b}")
					#	print_grid(last_grid)
					#	print_grid(g_a)
					#	print_grid(g_b)
					#	print_grid(grid)
					#	print("#" * 80)
				
				if "a" in move_choices:
					move_choices.remove("a")
				if "w" in move_choices:
					move_choices.remove("w")
					
				grid = grid_move(grid, move)
				move_summary.append(move)
				if turns % show_every_n_turns == 0:
					print(f"Turn# {turns} - {move_map[move]}\t\t\t{grid_sum(grid)}")
					print_grid(grid, space_size=num_size)
					
				if game_at(grid, game_at_score):
					raise GameEndException(f"You win! - reached {game_at_score} points!")
			except GridFullException as gfe:
				run = False
				print(gfe)
				print(f"Final:")
				print_grid(grid, space_size=num_size)
			except GameEndException as gee:
				run = False
				print(gee)
				print(f"Final:")
				print_grid(grid, space_size=num_size)
				
		print(f"{turns=}")
		print(f"score={grid_sum(grid)}")
		for k, move in move_map.items():
			print(f"{move}\t-\t{move_summary.count(k)}")
		
		print(f"Last 20 moves")
		print(f"{move_summary[-20:][::-1]}")
			
		if last_grid:
			print("Second Last Grid:")
			print_grid(last_grid, space_size=num_size)
		
		print("Final:")
		print_grid(grid, space_size=num_size)
		
		#print("Final Move LEFT")
		#g_a = grid_move([row.copy() for row in grid], "a")
		#print_grid(g_a, space_size=num_size)
		#
		#print("Final Move UP")
		#g_w = grid_move([row.copy() for row in grid], "w")
		#print_grid(g_w, space_size=num_size)
		#
		#print("Final Move Right")
		#g_d = grid_move([row.copy() for row in grid], "d")
		#print_grid(g_d, space_size=num_size)
		#
		#print("Final Move DOWN")
		#g_s = grid_move([row.copy() for row in grid], "s")
		#print_grid(g_s, space_size=num_size)
		#
		#print(sample_moves(grid))
		
	
	test_7()
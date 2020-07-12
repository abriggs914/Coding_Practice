# connect 4 game using Pygame
# June 2020

from time import sleep, time
from random import choice
from copy import deepcopy
import threading
#import concurrent.futures
from multiprocessing.pool import ThreadPool
import pygame
import connect_four_pop_up
from player import Player
from connect_four import Connect_Four, cpu_monte_carlo

pygame.init()

# return two random colors from the pygame colordict module (name, color, name, color)
def create_heads_tails_colors():
	color_keys_list = list(pygame.colordict.THECOLORS.keys())
	heads = choice(color_keys_list)
	tails = choice(color_keys_list)
	while heads == tails:
		tails = choice(color_keys_list)
	max_size = max(len(heads), len(tails)) + 3
	return heads.ljust(max_size, "-"), pygame.colordict.THECOLORS[heads], tails.ljust(max_size, "-"), pygame.colordict.THECOLORS[tails]

#################################################
##		 		 Design vars		           ##
#################################################

WIDTH = 800
HEIGHT = 600
legend_border_size = 8
legend_text_padding = 3
board_border_size = 14 # if the board border size is smaller than the pointer size, then the tips of the pointer will be drawn on the vertical edges of the background
pointer_size = 12

DRAW_PROPORTION = 0.9 						# range(0.03, 0.97)
TOP_MARGIN_PROPORTION = 1 - DRAW_PROPORTION
LEFT_MARGIN_PROPORTION = 0.05 				# range(0, 0.05)
LEGEND_WIDTH_PROPORTION = 0.3
LEGEND_START_PROPORTION = 0.7
LEGEND_TOP_MARGIN_PROPORTION = 0.02
COIN_SIZE_PROPORTION = 0.1
COIN_BORDER_SIZE = 2

# colors
logo_colors = [
	(232, 32, 32), 	# C - red
	(201, 12, 252), # O - purple
	(68, 114, 196), # N - blue
	(251, 166, 13), # N - orange 
	(255, 255, 9), 	# E - yellow
	(12, 252, 18), 	# C - green
	(21, 206, 243), # T - teal
	(255, 0, 255), 	# 4 - magenta
	(255, 9, 9), 	# ! - red
]
background_color = (0, 0, 0) # black
turn_indicator_color = (56, 112, 58) # dark green
time_color = (245, 245, 245) # white
legend_color = (56, 112, 58) # dark green
legend_border_color = (50, 50, 50) # dark gray
legend_text_color = (245, 245, 245) # white
board_color = (25, 117, 140) # dark teal
board_border_color = (50, 50, 50) # dark gray
empty_marker_color = (0, 0, 0) # black
pointer_color = (227, 54, 54) # red
error_message_color = (255, 10, 10) # red
coin_color = (181, 181, 179) # gray
coin_border_color = (97, 97, 97) # dark gray
coin_flip_message_color = (4, 5, 117) # dark blue
# use the pygame colordict module for color lookups here
coin_heads_color_name, coin_heads_color, coin_tails_color_name, coin_tails_color = create_heads_tails_colors()

# fonts
legend_font = pygame.font.SysFont("arial", 16)
large_font = pygame.font.SysFont("comicsansms", 115)
logo_font = pygame.font.SysFont("helveticca", 50)

# texts
logo_text = "CONNECT4!"
window_title = "Connect 4"
legend_header = "Legend:"
time_header = "Time:"
turn_header = "Who's turn:"
move_header = "Move #:"
turn_message_player = "Your turn"
turn_message_bot = "Computer's turn"
turn_message_random = "Not decided yet"
first_player_message = "You will go first!"
first_bot_message = "You will go second!"
first_random_message = "We will flip a coin to see who goes first"
error_message = "X"
invalid_set_up_message = "Invalid information to start a game.\nPlease try again."
end_game_message = "Thanks for playing!"
coin_flip_header = "Coin flip to decide the first player:"
coin_heads_message = "{0}     Heads".format(coin_heads_color_name.title())
coin_tails_message = "{0}     Tails".format(coin_tails_color_name.title())

#################################################
##		 		 	Game vars		           ##
#################################################
MIN_COIN_FLIPS = 8
MAX_COIN_FLIPS = 25
COIN_FLIP_FRAME_RATE = 0.003
COIN_FLIP_SHOW_TIME = 2

game_display = None
connect_4 = None
n_coin_flips = None
TIMED_EVENTS = None	# add millisecond time values to this list to be excluded in the game clock calculations



# return the MM:SS that have passed, computed from the t paramater in milliseconds
def timify(t):
	s = int(t / 1000)
	mins, secs = divmod(s, 60)
	return str(mins).rjust(2, "0") + ":" + str(secs).rjust(2, "0")

#ensure that the info taken from the pop up matches what is expected
def validate_game_info(game_info):
	if len(game_info.keys()) == 6:
		name = game_info["name"]
		color = game_info["color"]
		n_rows = game_info["rows"]
		n_cols = game_info["cols"]
		connect_x = game_info["connect_x"]
		first_player = game_info["first_player"]
		
		return name, color, n_rows, n_cols, connect_x, first_player
	return tuple([None for i in range(6)])
	
# x and y coordinates of the mouse
def get_mouse_coords():
	return pygame.mouse.get_pos()

# initialize pygame display and give it a title
def init_display():
	global game_display
	# dsiplay set up
	game_display = pygame.display.set_mode((WIDTH, HEIGHT))
	pygame.display.set_caption(window_title)
	
# render text at (x, y) using given font and color
def draw_text(x, y, text, text_color, font):
    text = font.render(text, True, text_color)
    game_display.blit(text,(x,y))
	
# used to calculate the distance for rjusting two strings, setting text_1 to the far left and text_2 to the far right
def calc_text_rjustification(width, text_1, text_2, font):
	single_chr = font.size(" ")[0]
	return round((width - font.size(text_1)[0] - font.size(text_2)[0]) / single_chr) + len(text_2) - 1
	
def create_coin_flip_messages(user_is_heads):
	global coin_heads_color_name, coin_heads_color, coin_tails_color_name, coin_tails_color, coin_heads_message, coin_tails_message
	user_player, bot_player = connect_4.players
	if user_is_heads:
		coin_heads_color_name = user_player.color.title()
		coin_heads_color = pygame.colordict.THECOLORS[coin_heads_color_name.lower()]
		coin_tails_color_name = bot_player.color.title()
		coin_tails_color = pygame.colordict.THECOLORS[coin_tails_color_name.lower()]
	else:
		coin_heads_color_name = bot_player.color.title()
		coin_heads_color = pygame.colordict.THECOLORS[coin_heads_color_name.lower()]
		coin_tails_color_name = user_player.color.title()
		coin_tails_color = pygame.colordict.THECOLORS[coin_tails_color_name.lower()]
		
	max_size = max(len(coin_heads_color_name), len(coin_tails_color_name)) + 5
	coin_heads_message = "{0}     Heads".format(coin_heads_color_name.ljust(max_size, "-").title())
	coin_tails_message = "{0}     Tails".format(coin_tails_color_name.ljust(max_size, "-").title())

# used to change the text color of the move number indicator
# green -> red as the number of moves shrinks
def calc_move_number_color():
	n_moves = connect_4.moves_made
	total_moves = connect_4.board.size
	fraction = n_moves / total_moves
	if fraction > 0.5:
		red_fraction = 1
		green_fraction = (1 - fraction) * 2
	else:
		red_fraction = fraction * 2
		green_fraction = 1
	red = 255 * red_fraction
	green = 255 * green_fraction
	blue = 0
	return red, green, blue
	
def calc_center():
	center_x = WIDTH / 2
	center_y = HEIGHT / 2
	return center_x, center_y
	
def draw_logo(game_info):
	single_chr = max([logo_font.size(letter)[0] for letter in logo_text])
	#space = 
	logo_font.set_underline(True)
	logo_size = logo_font.size(logo_text)[0]
	x = (WIDTH - logo_size) / 2
	y = ((HEIGHT * TOP_MARGIN_PROPORTION) - logo_font.get_height()) / 2
	for i, letter in enumerate(logo_text):
		color = logo_colors[i]
		draw_text(
			x,
			y,
			letter,
			color,
			logo_font
		)
		x += logo_font.size(letter)[0]

def draw_legend(game_info):
	draw_width = WIDTH * DRAW_PROPORTION
	draw_height = HEIGHT * DRAW_PROPORTION
	top_space = HEIGHT - draw_height
	
	legend_x = WIDTH * LEGEND_START_PROPORTION
	legend_y = HEIGHT * LEGEND_TOP_MARGIN_PROPORTION
	legend_height = top_space * DRAW_PROPORTION
	legend_width = draw_width * LEGEND_WIDTH_PROPORTION
	
	turn_indicator_height = top_space * DRAW_PROPORTION
	turn_indicator_width = draw_width * LEGEND_WIDTH_PROPORTION
	turn_indicator_x = (WIDTH * LEGEND_WIDTH_PROPORTION) - turn_indicator_width
	turn_indicator_y = HEIGHT * LEGEND_TOP_MARGIN_PROPORTION
	
	## draw Turn Indicator and tell the user the game status and who's turn it is
	# Turn indicator border
	turn_indicator_border_rect = pygame.draw.rect(
		game_display,
		legend_border_color,
		[
			turn_indicator_x - legend_border_size,
			turn_indicator_y - legend_border_size,
			turn_indicator_width + (2 * legend_border_size),
			turn_indicator_height + (2 * legend_border_size)
		]
	)
	
	# Turn indicator
	turn_indicator_rect = pygame.draw.rect(
		game_display,
		turn_indicator_color,
		[
			turn_indicator_x,
			turn_indicator_y,
			turn_indicator_width,
			turn_indicator_height
		]
	)
	
	text_row_space = int((legend_height - (2 * legend_text_padding)) / 3)
	custom_legend_font = pygame.font.SysFont("arial", text_row_space)
	
	# create clock text
	time_message = time_header
	time_passed = pygame.time.get_ticks() - sum(TIMED_EVENTS)
	t = timify(time_passed)
	rjustification = calc_text_rjustification(turn_indicator_width, time_message, t, custom_legend_font)
	time_message += t.rjust(rjustification, " ")
	
	# clock
	draw_text(
		turn_indicator_x + legend_text_padding,
		turn_indicator_y + legend_text_padding,
		time_message,
		time_color,
		custom_legend_font
	)
	
	# create player turn message
	turn_player = connect_4.player_turn
	turn_message = turn_header
	turn_font_color = legend_text_color
	if turn_player is None:
		player = connect_4.players[0] if connect_4.player_turn else connect_4.players[1]
		player_color = player.color
		turn_player_message = turn_message_player if connect_4.player_turn else turn_message_bot #turn_message_random
		turn_font_color = pygame.colordict.THECOLORS[player_color.lower()]
	elif turn_player is True:
		turn_player_message = turn_message_player
		turn_font_color = pygame.colordict.THECOLORS[connect_4.players[0].color.lower()]
	else:
		turn_player_message = turn_message_bot
		turn_font_color = pygame.colordict.THECOLORS[connect_4.players[1].color.lower()]
		
	rjustification = calc_text_rjustification(turn_indicator_width, turn_message, turn_player_message, custom_legend_font)
	turn_message += turn_player_message.rjust(rjustification, " ")
	
	# whos turn - in their font color
	draw_text(
		turn_indicator_x + legend_text_padding,
		turn_indicator_y + legend_text_padding + text_row_space,
		turn_message,
		turn_font_color,
		custom_legend_font
	)
	
	# calculate move number
	move_number_message = move_header
	n_moves = connect_4.moves_made + 1
	move_number = str(n_moves)
	rjustification = calc_text_rjustification(turn_indicator_width, move_number_message, move_number, custom_legend_font)
	move_number_message += move_number.rjust(rjustification, " ")
	move_number_color = calc_move_number_color()
	
	# move number
	draw_text(
		turn_indicator_x + legend_text_padding,
		turn_indicator_y + legend_text_padding + (2 * text_row_space),
		move_number_message,
		move_number_color,
		custom_legend_font
	)
		
	## draw Legend to tell user their color and the required score to win
	# legend border
	legend_border_rect = pygame.draw.rect(
		game_display,
		legend_border_color,
		[
			legend_x - legend_border_size,
			legend_y - legend_border_size,
			legend_width + (2 * legend_border_size),
			legend_height + (2 * legend_border_size)
		]
	)
	
	# legend rectangle
	legend_rect = pygame.draw.rect(
		game_display,
		legend_color,
		[
			legend_x,
			legend_y,
			legend_width,
			legend_height
		]
	)
	
	text_row_space = int((legend_height - (2 * legend_text_padding)) / 3)
	custom_legend_font = pygame.font.SysFont("arial", text_row_space)
	
	connect_x = "Connect " + str(game_info["connect_x"]) + " to win!"
	legend_header_message = legend_header
	rjustification = calc_text_rjustification(legend_width, legend_header_message, connect_x, custom_legend_font)
	legend_header_message += connect_x.rjust(rjustification, " ")
	
	# legend header
	draw_text(
		legend_x + legend_text_padding,
		legend_y + legend_text_padding,
		legend_header_message,
		legend_text_color,
		legend_font
	)
	
	player = connect_4.players[0]
	player_color_message = player.color
	player_name_message = player.name
	rjustification = calc_text_rjustification(legend_width, player_name_message, player_color_message, custom_legend_font)
	player_name_message += player_color_message.rjust(rjustification, " ")
	
	# player info
	draw_text(
		legend_x + legend_text_padding,
		legend_y + legend_text_padding + text_row_space,
		player_name_message,
		legend_text_color,
		legend_font
	)
	
	bot = connect_4.players[1]
	bot_color_message = bot.color
	bot_name_message = bot.name
	rjustification = calc_text_rjustification(legend_width, bot_name_message, bot_color_message, custom_legend_font)
	bot_name_message += bot_color_message.rjust(rjustification, " ")
	
	# bot info
	draw_text(
		legend_x + legend_text_padding,
		legend_y + legend_text_padding + (2 * text_row_space),
		bot_name_message,
		legend_text_color,
		legend_font
	)
	
def draw_board(game_info):
	top_space = HEIGHT * TOP_MARGIN_PROPORTION
	draw_width = WIDTH * DRAW_PROPORTION
	draw_height = (HEIGHT - top_space) * DRAW_PROPORTION
	
	board_x = WIDTH * LEFT_MARGIN_PROPORTION
	board_y = top_space + (2 * legend_border_size) + board_border_size
	
	n_rows = game_info["rows"]
	n_cols = game_info["cols"]
	#print("grid_horizontal_space", grid_horizontal_space, "grid_vertical_space", grid_vertical_space)
	
	# board border
	board_border = pygame.draw.rect(
		game_display,
		board_border_color,
		[
			board_x - board_border_size,
			board_y - board_border_size,
			draw_width + (2 * board_border_size),
			draw_height + (2 * board_border_size)
		]
	)
	
	# board background
	board = pygame.draw.rect(
		game_display,
		board_color,
		[
			board_x, 
			board_y,
			draw_width,
			draw_height
		]
	)	
	
	# draw marker holes
	positions = game_info["positions"]
	radius = game_info["radius"]
	for r, row in enumerate(positions):
		for c, position in enumerate(row):
			center_x, center_y = position
			if connect_4.board.status[r][c] is not None:
				player = connect_4.board.player_marks[r][c]
				marked_color = pygame.colordict.THECOLORS[player.color.lower()]
				# marked position
				#print("center_x", center_x, "center_y", center_y, "is marked")
				#print(pygame.colordict)
			else:
				marked_color = empty_marker_color
			
			pygame.draw.circle(
				game_display,
				marked_color,
				(center_x, center_y),
				radius
			)
			
def draw_pointer(game_info):
	top_space = HEIGHT * TOP_MARGIN_PROPORTION
	draw_width = WIDTH * DRAW_PROPORTION
	draw_height = (HEIGHT - top_space) * DRAW_PROPORTION
	
	board_x = WIDTH * LEFT_MARGIN_PROPORTION
	board_y = top_space + (2 * legend_border_size) + board_border_size
	
	mouse_x, mouse_y = get_mouse_coords()
	
	mouse_x = max(board_x, min(mouse_x - (pointer_size / 2), ((board_x + draw_width) - pointer_size)))
	mouse_y = max(board_y + pointer_size, min(mouse_y, (board_y + draw_height))) - top_space - (2 * legend_border_size) - board_border_size - pointer_size
	pointer_rect = pygame.draw.rect(
		game_display,
		pointer_color,
		[
			mouse_x,
			board_y,
			pointer_size,
			mouse_y
		]
	)
	
	offset = 1
	top_y = mouse_y + top_space + (2 * legend_border_size) + board_border_size - offset
	pointer_arrow = pygame.draw.polygon(
		game_display,
		pointer_color,
		[
			((mouse_x - (pointer_size)), top_y), # left top
			((mouse_x + (2 * pointer_size)), top_y), # right top
			((mouse_x + (pointer_size / 2)), (top_y + pointer_size + offset)) # tip
		]
	)
	
# creates a list of both possible colors in the order necessary to display the winner on the last flip
def get_coin_color_order(heads_won_toss, user_is_heads):
	if n_coin_flips % 2 == 0:
		#winner color shown second
		if heads_won_toss:
			colors = [coin_tails_color, coin_heads_color]
		else:
			#if user_is_heads:
			colors = [coin_heads_color, coin_tails_color]
	else:
		# winner color shown first
		if heads_won_toss:
			colors = [coin_heads_color, coin_tails_color]
		else:
			colors = [coin_tails_color, coin_heads_color]
	return colors
	
def create_coin_flip_winner_message(heads_won_toss, user_is_heads):
	heads_player = connect_4.players[0] if user_is_heads else connect_4.players[1]
	tails_player = connect_4.players[1] if user_is_heads else connect_4.players[0]
	if heads_won_toss:
		message = "Heads"
		use_heads_player = True
	else:
		message = "Tails"
		use_heads_player = False
	message += " won the coin toss! - "
	message += heads_player.name if heads_won_toss else tails_player.name
	message += " will go first"
	return message
	
def toss_coin():
	return choice([i for i in range(2)]) == 0
	
def do_coin_flip():
	user_is_heads = choice([i for i in range(2)]) == 0
	heads_won_toss = toss_coin()
	create_coin_flip_messages(user_is_heads)
	logo_font.set_underline(False)
	center_x, center_y = calc_center()
	coin_width = max(WIDTH, HEIGHT) * COIN_SIZE_PROPORTION
	coin_height = max(WIDTH, HEIGHT) * COIN_SIZE_PROPORTION
	coin_x = center_x - (coin_width / 2)
	coin_y = center_y - (coin_height / 2)
	radius = min(coin_height, coin_width)
	coin_rect = [coin_x, coin_y, coin_width, coin_height]
	coin_border_rect = [coin_x - COIN_BORDER_SIZE, coin_y - COIN_BORDER_SIZE, coin_width + (2 * COIN_BORDER_SIZE), coin_height + (2 * COIN_BORDER_SIZE)]
	
	text_size, text_height = logo_font.size(coin_flip_header)
	message_x = center_x - (text_size / 2)
	message_y = center_y - text_height - (2 * radius)
	
	half_frames = coin_width / 2 #(coin_width + (2 * COIN_BORDER_SIZE)) / 2
	frame_number = 2
	total_frames = int(n_coin_flips * half_frames) # + (frame_number * n_coin_flips)
	if n_coin_flips % 2 == 1:
		total_frames += round(coin_width)
	
	colors = get_coin_color_order(heads_won_toss, user_is_heads)	
	coin_color_idx = 0
	
	flip_number = 0
	winner_color = colors[(n_coin_flips + 1) % 2]
	print("n_flips:", n_coin_flips, ",heads won toss:", heads_won_toss, ",user_is_heads:", user_is_heads, ",color order:", colors, ",half_frames:" ,half_frames, "total_frames:",total_frames, "winner_color:", winner_color)
	for i in range(total_frames):
	
		# coin header message
		draw_text(
			message_x,
			message_y,
			coin_flip_header,
			coin_flip_message_color,
			logo_font
		)
		
		# coin heads message
		draw_text(
			message_x,
			message_y + text_height,
			coin_heads_message,
			coin_heads_color,
			logo_font
		)
		
		# coin tails message
		draw_text(
			message_x,
			message_y + (2 * text_height),
			coin_tails_message,
			coin_tails_color,
			logo_font
		)
	
		#print("flips:", n_coin_flips, "t_frames:", total_frames, "h_frames:", half_frames, "f_#", frame_number, "coin_rect:", coin_rect, "coin_border_rect", coin_border_rect)
		coin_border_rect[2] -= frame_number
		coin_rect[2] -= frame_number
		coin_border_rect[0] += (frame_number / 2)
		coin_rect[0] += (frame_number / 2)
		if coin_rect[2] <= frame_number or coin_rect[2] == (2 * half_frames):
			frame_number *= -1
			coin_color_idx += 1
			coin_color_idx %= 2
			flip_number += 1
			print("flip:", flip_number)
		if flip_number < n_coin_flips:
			coin_color = colors[coin_color_idx]
		
		# draw coin border at new size
		coin_border = pygame.draw.ellipse(
			game_display,
			coin_border_color,
			coin_border_rect
		)
		# draw coin at new size
		coin = pygame.draw.ellipse(
			game_display,
			coin_color,
			coin_rect
		)
		sleep(COIN_FLIP_FRAME_RATE)
		pygame.display.update()
		if flip_number >= n_coin_flips and coin_rect[2] == coin_width:
			print("correct size?", coin_rect[2] == coin_width, "correct color?", winner_color == coin_color)
			break
		game_display.fill(background_color)
				
	coin_results_message = create_coin_flip_winner_message(heads_won_toss, user_is_heads)
	results_lines = coin_results_message.split("-")
	print(coin_results_message)
	for i, line in enumerate(results_lines):
		# display coin flip results
		draw_text(
			message_x,
			coin_y + coin_height + (2 * COIN_BORDER_SIZE) + ((i + 1) * text_height),
			line,
			coin_color,
			logo_font
		)
	pygame.display.update()
	sleep(COIN_FLIP_SHOW_TIME)
	TIMED_EVENTS.append(pygame.time.get_ticks())
	return heads_won_toss, user_is_heads

def draw_display(game_info):
	game_display.fill(background_color)
	draw_logo(game_info)
	draw_legend(game_info)
	draw_board(game_info)
	draw_pointer(game_info)
	pygame.display.update()
	
def show_invalid_move():
	font_size = large_font.size(error_message)[0]
	x = (WIDTH / 2) - (font_size / 2)
	y = (HEIGHT / 2) - (font_size / 2)
	draw_text(x, y, error_message, error_message_color, large_font)
	
def show_first_player_message(player):
	message = player.name + " will go first"
	center_x, center_y = calc_center()
	text_size, text_height = logo_font.size(message)
	message_x = center_x - (text_size / 2)
	message_y = center_y - (text_height / 2)
	draw_text(
		message_x,
		message_y,
		message,
		coin_flip_message_color,
		logo_font
	)
	pygame.display.update()
	sleep(COIN_FLIP_SHOW_TIME)
	TIMED_EVENTS.append(pygame.time.get_ticks())
	
# tell the user who the first player is, or do a coin flip to decide
def print_start_game(game_info):
	first_player = game_info["first_player"]
	if first_player is "player":
		player = connect_4.players[0]
		show_first_player_message(player)	
		connect_4.player_turn = True
		print(first_player_message)	
	elif first_player is "bot":
		player = connect_4.players[1]
		show_first_player_message(player)
		connect_4.player_turn = False
		print(first_bot_message)	
	else:
		print(first_random_message)
		heads_won_toss, user_is_heads = do_coin_flip()
		if heads_won_toss:
			if user_is_heads:
				connect_4.player_turn = True
			else:
				connect_4.player_turn = False
		else:
			if user_is_heads:
				connect_4.player_turn = False
			else:
				connect_4.player_turn = True
		
# On mouse click return the column the user selected, else None
def determine_col(game_info, mouse_x):
	buckets = game_info["buckets"]
	diameter = game_info["radius"] * 2
	for row in buckets:
		for i, bucket in enumerate(row):
			x, y = bucket
			if mouse_x in range(x, x + diameter):
				return i
	return None

# compute the circle positions once and use the resulting list for quick lookups when drawing
def compute_positions(game_info):
	top_space = HEIGHT * TOP_MARGIN_PROPORTION
	draw_width = WIDTH * DRAW_PROPORTION
	draw_height = (HEIGHT - top_space) * DRAW_PROPORTION
	
	board_x = WIDTH * LEFT_MARGIN_PROPORTION
	board_y = top_space + (2 * legend_border_size) + board_border_size
	
	n_rows = game_info["rows"]
	n_cols = game_info["cols"]
	
	grid_horizontal_space = int(draw_width / n_cols)
	grid_vertical_space = int(draw_height / n_rows)
	x_offset = (draw_width - (n_cols * grid_horizontal_space)) / 2
	y_offset = (draw_height - (n_rows * grid_vertical_space)) / 2
	radius = int(min(grid_horizontal_space, grid_vertical_space) / 2)
	diff = abs(grid_horizontal_space - grid_vertical_space) / 2
	if grid_horizontal_space > grid_vertical_space:
		x_offset += diff
	else:
		y_offset += diff
	game_info["radius"] = radius
	positions = []
	buckets = []
	for r in range(n_rows):
		row_positions = []
		row_buckets = []
		for c in range(n_cols):
			center_x = int((c * grid_horizontal_space) + radius + board_x + x_offset)
			center_y = int((r * grid_vertical_space) + radius + board_y + y_offset)
			left_x = int((c * grid_horizontal_space) + board_x + x_offset)
			top_y = int((r * grid_vertical_space) + board_y + y_offset)
			row_positions.append((center_x, center_y))
			row_buckets.append((left_x, top_y))
		positions.append(row_positions)
		buckets.append(row_buckets)
	game_info["positions"] = positions
	game_info["buckets"] = buckets
	
# initialize the connect_4 object, sets players, rows, columns, and connect_x attributes
def init_game(game_info):
	global connect_4, n_coin_flips, TIMED_EVENTS, CPU_IS_THINKING
	CPU_IS_THINKING = False
	TIMED_EVENTS = []
	connect_4 = Connect_Four()
	user_player = Player(game_info["name"], game_info["color"])
	bot_player = connect_4.set_computer_info(user_player)
	connect_x = game_info["connect_x"]
	n_rows = game_info["rows"]
	n_cols = game_info["cols"]
	players = [user_player, bot_player]
	connect_4.create_game(players, connect_x, n_rows, n_cols)
	compute_positions(game_info)
	n_coin_flips = choice([i for i in range(MIN_COIN_FLIPS, MAX_COIN_FLIPS)])
	
	#test_marks(user_player, bot_player)
	
def mark(game_info, col, player, *data):
	global CPU_IS_THINKING
	# TODO: check that there is room on the board BEFORE AND AFTER marking to catch ties before returning to the game loop
	row = connect_4.board.next_row(col)
	connect_4.board.mark(row, col, player)
	connect_4.moves_made += 1
	player.update_history((row, col), data)
	connect_4.turn_change()
	draw_display(game_info)
	pygame.display.update()
	code, win = connect_4.check_win(do_sleep=False, do_print=True)
	if not connect_4.player_turn:
		CPU_IS_THINKING = True
	if win:
		print("WINNER FOUND - GAME OVER")
		connect_4.playing = False
		game_over()

def calc_look_ahead_moves(r, c, m, coefficient, connect_x):
	return round(max(connect_x, (((r*c) - m) / 2) * (1 - coefficient)))

def make_cpu_move(game_info):
	global CPU_IS_THINKING
	if CPU_IS_THINKING:
		CPU_IS_THINKING = False
		start_time = time()
		
		# random move
		# cpu_r, cpu_c = connect_4.cpu_move(do_sleep=False)
			
		
# self			-		Connect 4 object
# score			-		The weight to scale the outcome of the simulations
# max_moves		-		How many moves the AI will play
# depth			-		How many games the AI will play
# do_sleep 		-		Used in the REPL version to give time for reading output
# do_print		-		Used to show output in the REPL version
		connect_4_obj = deepcopy(connect_4)
		score = 100
		coefficient = 0.05
		look_ahead_args = (connect_4.board.rows, connect_4.board.cols, connect_4.moves_made, coefficient, connect_4.CONNECT_X)
		max_moves = calc_look_ahead_moves(*look_ahead_args)
		depth = 200
		do_print = False
		do_sleep = False
		print("CPU will play {d} games, looking {m} moves ahead, scoring each succesive move by a fraction of {s}".format(d=depth, m=max_moves, s=score))
		monte_carlo_args = (connect_4_obj, score, max_moves, depth, do_sleep, do_print)
		
		start_time = time()
		cpu_r, cpu_c, monte_carlo_data = cpu_monte_carlo(*monte_carlo_args)
		end_time = time()
		how_long = end_time - start_time
		board = connect_4.board
		data = (how_long, monte_carlo_data, board.create_board(deepcopy(board.status), connect_4.players))
		
		print("how long?", how_long)	
		mark(game_info, cpu_c, connect_4.players[1], data)

# runs the game
def main_game_loop(game_info):
	# main loop
	while connect_4.playing:
		events = pygame.event.get()
		event_types = [event.type for event in events]
		if pygame.QUIT in event_types:
			quit_game()
		if connect_4.playing:
			if connect_4.player_turn:
				for event in events:
					if event.type == pygame.QUIT:
						quit_game()
					if connect_4.player_turn:
						if event.type == pygame.MOUSEBUTTONDOWN:
							#pygame.event.set_allowed([pygame.QUIT, pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP])
							mouse_x, mouse_y = get_mouse_coords()
							board_col = determine_col(game_info, mouse_x)
							print("CLICK column:", board_col)
							available_cols = connect_4.board.remaining_cols()
							valid_move = board_col in available_cols
							board = connect_4.board
							if valid_move:
								mark(game_info, board_col, connect_4.players[0], board.create_board(deepcopy(board.status.copy()), connect_4.players))
							else:
								show_invalid_move()
							#print("events:", events)
							#print("waiting", pygame.event.wait())
			else:
				threading.Thread(target=make_cpu_move, args=[game_info]).start()
		#show_invalid_move()
		#print(get_mouse_coords())
		draw_display(game_info)
		#quit_game()
	print("main quit")
	sleep(6)
	quit_game()

# called before the main game loop to do set up and variable initialization
def play_game():
	global CPU_IS_THINKING
	# commenting out to make testing faster
	#game_info = connect_four_pop_up.gather_info()
	game_info = {"name": "Avery Briggs", "color": "Yellow", "rows": 11, "cols": 11, "connect_x": 4, "first_player": "random"}
	
	validated_info = validate_game_info(game_info)
	
	# if any attribute is None quit
	if None in validated_info:
		print(invalid_set_up_message)
		quit_game()
		
	name, color, n_rows, n_cols, connect_x, first_player = validated_info
	print("name", name, "color", color, "n_rows", n_rows, "n_cols", n_cols, "connect_x", connect_x, "first_player", first_player)
	init_game(game_info)
	init_display()
	print_start_game(game_info)
	draw_display(game_info)
	CPU_IS_THINKING = not connect_4.player_turn
	main_game_loop(game_info)	

def game_over():
	for player in connect_4.players:
		print("player", player, "\n\tMove history:\n")
		player.print_move_history()

def quit_game():
	print(end_game_message)
	pygame.quit()
	quit()

def pause_game():
	print("Pause")

def test_marks(user_player, bot_player):
	n_cols = connect_4.board.cols
	n_rows = connect_4.board.rows
	cols = [choice([i for i in range(n_cols)]) for j in range(min(n_rows, n_cols))]
	players = [choice([user_player, bot_player]) for i in range(len(cols))]
	print("cols:", cols)
	print("players:", players)
	sleep(5)
	for i, col in enumerate(cols):
		connect_4.board.mark(connect_4.board.next_row(col), col, players[i], 1)

	
if __name__ == "__main__": play_game()
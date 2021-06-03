import pygame
import easygui
from multiprocessing.pool import ThreadPool
from threading import Thread
from main import *
from colors import *
import math

pygame.init()

# On start-up show main menu.
# Main menu consists of:
#   -   Ability to change grid dimensions (Must be square)
#   -   Ability to load existing game
#   -   Ability to start new game
#   -   Ability to view stats and game history
#   -   Ability to change colour scheme (presets or custom)

# Grid game main screen
#   -   Ability to shift current grid by using keyboard or (mouse clicks?)
#   -   Buttons to navigate back to the main menu (pauses game clock)
#   -   Ability to quit game and offer to save game before exiting

# Stats and history screen
#   -   Show top N (5) scores (show the grid view in small form)
#   -   Show averages and high and low scores in text, num games, time played...
#   -   Buttons to navigate back to main menu

# Colour scheme chooser

##################################################
##					Design vars					##
##################################################

# BLACK = (0, 0, 0)
CIRCLE_MARKER_COLOR = (255, 255, 255)  # white
LEGEND_MARKER_COLOR = (255, 15, 15)  # red
BACKGROUND_COLOR = (0, 0, 0)  # black
CIRCLE_MARKER_SIZE = 10  # diameter of dot
CIRCLE_BORDER_SIZE = 3  # space of the grid circle color shown
SCREEN_PROPORTION = 0.85  # margin space for circle drawing
SELECTION_WIDTH = 5
BUTTON_TEXT_FONT = None  # initialized in init_pygame function
LINE_WIDTH = 1


def colour_func(val, start=(255, 255, 255)):
	# print("val", val)
	math.log(val, 2)
	return (50, 50, 50)


colour_scheme_blue_green = {
	"block": ((135, 131, 131), pygame.font.SysFont("helvetica", 16, bold=1), (255, 255, 255)),
	2: ((8, 201, 73), pygame.font.SysFont("arial", 16, bold=1), (255, 255, 255)),
	4: ((44, 145, 78), pygame.font.SysFont("arial", 16, bold=1), (255, 255, 255)),
	8: ((44, 145, 133), pygame.font.SysFont("arial", 16, bold=1), (255, 255, 255)),
	16: ((14, 235, 209), pygame.font.SysFont("arial", 16, bold=1), (255, 255, 255)),
	32: ((0, 94, 153), pygame.font.SysFont("arial", 16, bold=1), (255, 255, 255)),
	64: ((22, 68, 117), pygame.font.SysFont("arial", 16, bold=1), (255, 255, 255)),
	128: ((2, 39, 79), pygame.font.SysFont("arial", 16, bold=1), (255, 255, 255)),
	256: ((0, 31, 105), pygame.font.SysFont("arial", 16, bold=1), (255, 255, 255)),
	512: ((0, 30, 255), pygame.font.SysFont("arial", 16, bold=1), (255, 255, 255)),
	1024: ((3, 4, 74), pygame.font.SysFont("arial", 16, bold=1), (255, 255, 255)),
	2048: ((0, 23, 66), pygame.font.SysFont("arial", 16, bold=1), (255, 255, 255)),
	"rest": (lambda x: colour_func(x, start=(0, 23, 66)), pygame.font.SysFont("arial", 16, bold=1), (255, 255, 255)),
	"score": ((77, 140, 18), pygame.font.SysFont("helvetica", 16, bold=1), (255, 255, 255)),
	"hi-score": ((8, 187, 246), pygame.font.SysFont("helvetica", 16, bold=1), (66, 75, 78)),
	"undo": ((11, 84, 0), (0, 143, 99), (36, 183, 137), pygame.font.SysFont("helvetica", 16, bold=1), (255, 255, 255)),
	"reset": ((0, 33, 113), (30, 65, 149), (0, 73, 255), pygame.font.SysFont("helvetica", 16, bold=1), (255, 255, 255))
}
colour_scheme_blue_green.update({str(k): v for k, v in colour_scheme_blue_green.items() if isinstance(k, int)})
colour_scheme_red_yellow = {
	"block": ((135, 131, 131), pygame.font.SysFont("helvetica", 16, bold=1), (255, 255, 255)),
	2: ((202, 215, 90), pygame.font.SysFont("arial", 16, bold=1), (255, 255, 255)),
	4: ((242, 57, 47), pygame.font.SysFont("arial", 16, bold=1), (255, 255, 255)),
	8: ((227, 165, 2), pygame.font.SysFont("arial", 16, bold=1), (255, 255, 255)),
	16: ((227, 119, 2), pygame.font.SysFont("arial", 16, bold=1), (255, 255, 255)),
	32: ((193, 100, 0), pygame.font.SysFont("arial", 16, bold=1), (255, 255, 255)),
	64: ((171, 73, 32), pygame.font.SysFont("arial", 16, bold=1), (255, 255, 255)),
	128: ((168, 126, 5), pygame.font.SysFont("arial", 16, bold=1), (255, 255, 255)),
	256: ((168, 50, 5), pygame.font.SysFont("arial", 16, bold=1), (255, 255, 255)),
	512: ((134, 34, 20), pygame.font.SysFont("arial", 16, bold=1), (255, 255, 255)),
	1024: ((170, 77, 19), pygame.font.SysFont("arial", 16, bold=1), (255, 255, 255)),
	2048: ((171, 0, 0), pygame.font.SysFont("arial", 16, bold=1), (255, 255, 255)),
	"rest": (lambda x: colour_func(x, start=(171, 0, 0)), pygame.font.SysFont("arial", 16, bold=1), (255, 255, 255)),
	"score": ((119, 0, 0), pygame.font.SysFont("helvetica", 16, bold=1), (255, 255, 255)),
	"hi-score": ((222, 206, 76), pygame.font.SysFont("helvetica", 16, bold=1), (66, 75, 78)),
	"undo": ((149, 133, 0), (185, 166, 6), (246, 221, 13), pygame.font.SysFont("helvetica", 16, bold=1), (255, 255, 255)),
	"reset": ((153, 61, 0), (186, 87, 21), (255, 101, 0), pygame.font.SysFont("helvetica", 16, bold=1), (255, 255, 255))
}
colour_scheme_red_yellow.update({str(k): v for k, v in colour_scheme_red_yellow.items() if isinstance(k, int)})

##################################################
##					Game vars					##
##################################################

TESTING = True

DISPLAY = None  # Display surface
TITLE = "2048"  # title
WIDTH = 650  # width and height
HEIGHT = 650
GRID_WIDTH = WIDTH * 0.75
GRID_HEIGHT = HEIGHT * 0.75
PAD = 35
SPACE = 15
GRID_X = 0
GRID_Y = 0
DATA = {
	"current_screen": "main_menu",
	"current_game": None,
	"game_time": None,
	"colour_scheme": None
}
LOAD_GAME_FILE = "save.txt"
IDLE = "idle"
load = "load"  # initialized in init_file_handling must be done there because file_handling uses
save = "save"  # small_pop_up and reset functions defined in this file
POP_UP_THREAD = None


# ROWS = 11								# Number of rows and columns
# COLS = 11
# DATA = {}								# Dictionary of; circle / radius / spacing data values
# FOLLOW_MOUSE = False					# Control whether the mouse is followed or not
# MARK_CENTER = True						# Control whether the whole grid circle holds the dot or just it's circumference
# CLOCK = pygame.time.Clock()				# Clock and framerate
# FRAME_RATE = 60


class Pygame_2048:

	def __init__(self, n=4, init_spaces=None):
		self.game_obj = G2048(n=n, init_spaces=init_spaces)


def init_button_font():
	global BUTTON_TEXT_FONT
	if BUTTON_TEXT_FONT is None:
		BUTTON_TEXT_FONT = pygame.font.SysFont("arial", 16)


def calc_block_idx_font():
	width, height = DATA["grid_space"]
	rows = DATA["grid"].rows
	cols = DATA["grid"].cols
	grid_height = (height / rows) - LINE_WIDTH
	grid_width = (width / cols) - LINE_WIDTH
	DATA["block_idx_font"] = pygame.font.SysFont("arial", int(min(grid_width, grid_height) * 0.85))


# Create and return text objects for blitting
def text_objects(text, font, color=BLACK):
	textSurface = font.render(text, True, color)
	return textSurface, textSurface.get_rect()


def kill_pop_up_thread():
	if isinstance(POP_UP_THREAD, Thread):
		if POP_UP_THREAD.is_alive():
			DATA["mode"] = IDLE
			POP_UP_THREAD.join()


# def reset(click, DATA):
# 	print("reset")
# 	l, m, r = click
# 	print("data(", len(DATA), "):", DATA)
# 	if "a*" in DATA:
# 		del DATA["a*"]
# 	if l:
# 		DATA["grid"].reset_search()
# 	if m:
# 		DATA["grid"].reset_search_blocks()
# 	if r:
# 		DATA["grid"].reset_clear()


def full_reset():
	print("full reset")
	init()


# # diaplay a button and listen for it to be clicked.
# # acts as a controller to update the program mode as well.
# # msg 		- 	button text
# # x			-	button x
# # y			-	button x
# # w			-	button width
# # h			-	button height
# # ic		-	button color
# # ac		-	button color when hovering
# # cc		-	button color when clicked
# # action	-	function to be called on click
# def draw_square(msg, x, y, w, h, ic, ac, cc, action=None):
# 	global POP_UP_THREAD
# 	mouse = pygame.mouse.get_pos()
# 	click = tuple(pygame.mouse.get_pressed())
#
# 	if x + w > mouse[0] > x and y + h > mouse[1] > y:
# 		c = ac
# 		# pygame.draw.rect(DISPLAY, ac, (x, y, w, h))
# 		# print("click: " + str(click))
# 		if click[0]:
# 			c = cc
# 			# DATA["mode"] = msg
# 			kill_pop_up_thread()
# 			if action is not None:
# 				pool = ThreadPool(processes=1)
# 				print("action:", action)
# 				if action == reset:
# 					async_result = pool.apply_async(action, (click, DATA))
# 				elif action == save or action == load:
# 					async_result = pool.apply_async(action, (DATA, DISPLAY))
# 				else:
# 					async_result = pool.apply_async(action, ())
# 				f_args = async_result.get()
# 				if f_args:
# 					f, arg = f_args
# 					kill_pop_up_thread()
# 					POP_UP_THREAD = Thread(target=f, args=arg)
# 					POP_UP_THREAD.start()
# 				else:
# 					print("no function")
#
# 				# recalculate buckets on load
# 				if action == load:
# 					# DATA["buckets"] = calculate_buckets()
# 					spl = "."
# 					arg_split = arg[2].split(spl)
# 					file_name = arg_split[0] + spl + arg_split[1][:4]
# 					pygame.display.set_caption(TITLE + file_name.rjust(120, " "))
# 					init_button_font()
# 					calc_block_idx_font()
# 				elif action == reset and sum(click) > 1:
# 					pygame.display.set_caption(TITLE)
# 					if sum(click) == 3:
# 						full_reset()
#
# 				# event = pygame.event.wait()
# 		# pygame.draw.rect(DISPLAY, c, (x, y, w, h))
# 	else:
# 		c = ic
# 	pygame.draw.rect(DISPLAY, c, (x, y, w, h))
#
# 	BUTTON_TEXT_FONT.set_bold(True)
# 	text_surf, text_rect = text_objects(msg, BUTTON_TEXT_FONT)
# 	text_rect.center = ((x + (w / 2)), (y + (h / 2)))
# 	DISPLAY.blit(text_surf, text_rect)

f = 1

# diaplay a button and listen for it to be clicked.
# acts as a controller to update the program mode as well.
# msg 		- 	button text
# x			-	button x
# y			-	button x
# w			-	button width
# h			-	button height
# ic		-	button color
# ac		-	button color when hovering
# cc		-	button color when clicked
# f			-	font
# fc		-	font colour
# action	-	function to be called on click
def draw_button(msg, x, y, w, h, ic, ac, cc, f, fc, action=None):
	global POP_UP_THREAD
	mouse = pygame.mouse.get_pos()
	click = tuple(pygame.mouse.get_pressed())

	# if msg == DATA["mode"]:
	# 	pygame.draw.rect(DISPLAY, SELECTION_COLOR, (x, y, w, h))
	# 	x += SELECTION_WIDTH
	# 	y += SELECTION_WIDTH
	# 	w -= (2 * SELECTION_WIDTH)
	# 	h -= (2 * SELECTION_WIDTH)

	if x + w > mouse[0] > x and y + h > mouse[1] > y:
		c = ac
		# pygame.draw.rect(DISPLAY, ac, (x, y, w, h))
		# print("click: " + str(click))
		if click[0]:
			c = cc
			# DATA["mode"] = msg
			kill_pop_up_thread()
			if action is not None:
				pool = ThreadPool(processes=1)
				# print("action:", action)
				# if action == reset:
				# 	async_result = pool.apply_async(action, (click, DATA))
				# elif action == save or action == load:
				# 	async_result = pool.apply_async(action, (DATA, DISPLAY))
				# else:
				# 	async_result = pool.apply_async(action, ())
				async_result = pool.apply_async(action, ())
				f_args = async_result.get()
				if f_args:
					f, arg = f_args
					kill_pop_up_thread()
					POP_UP_THREAD = Thread(target=f, args=arg)
					POP_UP_THREAD.start()
				# else:
				# 	print("no function")

				# recalculate buckets on load
				if action == load:
					# DATA["buckets"] = calculate_buckets()
					spl = "."
					arg_split = arg[2].split(spl)
					file_name = arg_split[0] + spl + arg_split[1][:4]
					pygame.display.set_caption(TITLE + file_name.rjust(120, " "))
					init_button_font()
					calc_block_idx_font()
				elif action == reset and sum(click) > 1:
					pygame.display.set_caption(TITLE)
					if sum(click) == 3:
						full_reset()

				pygame.event.clear()
				event = pygame.event.wait(pygame.MOUSEBUTTONUP)
		# pygame.draw.rect(DISPLAY, c, (x, y, w, h))
	else:
		c = ic
	pygame.draw.rect(DISPLAY, c, (x, y, w, h))

	# f.set_bold(True)
	text_surf, text_rect = text_objects(msg, f, fc)
	text_rect.center = ((x + (w / 2)), (y + (h / 2)))
	DISPLAY.blit(text_surf, text_rect)


def load_game():
	if TESTING:
		return [[None, 2, 4, 8], [16, 32, 64, 128], [256, 512, 1024, 2048], [4096, 8192, 16384, 32768]]
		# return [[None, 2, None, None], [16, None, None, 4], [None, 2, 4, 2], [4, 2, 4, 2]]
	with open(LOAD_GAME_FILE, 'r') as f:
		lines = f.readlines()
		return lines


# Initialize the DATA dictionary.
# Called immediately on run, before the main loop.
def init():
	global DISPLAY, GRID_X, GRID_Y
	DISPLAY = pygame.display.set_mode((WIDTH, HEIGHT))
	pygame.display.set_caption(TITLE)

	loaded_game = load_game()
	if not loaded_game:
		loaded_game = G2048(random_tile_values=[2])
	else:
		loaded_game = G2048(init_spaces=loaded_game, random_tile_values=[2])
	DATA["current_game"] = loaded_game
	DATA["mode"] = "play"
	# DATA["colour_scheme"] = colour_scheme_blue_green
	DATA["colour_scheme"] = colour_scheme_red_yellow
	DATA["colour_func_type"] = type(colour_func)
	init_button_font()

	# print("w:", WIDTH, "h:", HEIGHT, "gw:", GRID_WIDTH, "gh:", GRID_HEIGHT, "p:", PAD, "s:", SPACE)
	GRID_X = (WIDTH - GRID_WIDTH) * 0.5
	GRID_Y = (HEIGHT - GRID_HEIGHT) * 0.95
	# print("gx:", GRID_X, "gy:", GRID_Y)


# DATA["game_time"] = compute_row_space()
# DATA["colour_scheme"] = compute_spacing()
# DATA["radius"] = compute_radius()
# DATA["circles"] = create_circles()


def do_print():
	print("button clicked")


def draw_display():
	global DISPLAY
	DISPLAY.fill(BACKGROUND_COLOR)
	game = DATA["current_game"]
	grid = game.grid
	colour_scheme = DATA["colour_scheme"]
	w, h = GRID_WIDTH, GRID_HEIGHT
	# print("grid", DATA["current_game"])
	# draw_circles()
	# draw_button("click me", 20, 20, 120, 120, RED, YELLOW, GREEN, do_print)

	# print(dict_print(DATA, "DATA"))

	n = len(grid)
	m = len(grid[0])

	bs = (2 * PAD) + ((n - 1) * SPACE)
	w_rs = w - bs
	h_rs = h - bs
	cw = w_rs / m
	ch = h_rs / n

	x0, y0 = GRID_X + PAD, GRID_Y + PAD
	# cw, ch = 120, 120
	cells = {}
	for i, row in enumerate(grid):
		for j, col in enumerate(row):
			# print("col", col)
			if col is None:
				col = "block"
			val = col
			if isinstance(col, int) or (isinstance(col, str) and col.isdigit()):
				if 0 <= col <= 2048:
					col = col
				else:
					col = "rest"
			c, f, fc = colour_scheme[col]
			if isinstance(c, type(colour_func)):
				c = c(val)
			x = x0 + (j * (cw + SPACE))
			y = y0 + (i * (ch + SPACE))
			# print("i", i, "j", j, "\nx", x, "y", y, "\nc", c)
			# print("c", c, "typr(\"c\")", type(c), "isinstance(\"'function'\")", isinstance(c, type(colour_func)))

			cells[str(i) + " - " + str(j)] = {"ij": (i, j), "colour": c, "x": x, "y": y, "w": cw, "h": ch}
			pygame.draw.rect(DISPLAY, c, (x, y, cw, ch))

			text_surf, text_rect = text_objects(str(val), f, fc)
			text_rect.center = ((x + (cw / 2)), (y + (ch / 2)))
			DISPLAY.blit(text_surf, text_rect)
		cells["r"] = n
		cells["c"] = m
	DATA["cells"] = cells

	remaining_height = GRID_Y - (2 * PAD)
	remaining_width = WIDTH - (2 * PAD)
	sp = 8
	sw = remaining_width * 0.4
	sh = remaining_height * 0.4
	sx = WIDTH - (sw + (2 * sp))
	sy = sh + (2 * sp)

	sbkg, sf, sfc = DATA["colour_scheme"]["score"]
	pygame.draw.rect(DISPLAY, sbkg, (sx, sy, sw, sh))
	msg = "Score: {}".format(game.score)
	# BUTTON_TEXT_FONT.set_bold(True)
	text_surf, text_rect = text_objects(msg, sf, sfc)
	text_rect.center = ((sx + (sw / 2)), (sy + (sh / 2)))
	DISPLAY.blit(text_surf, text_rect)

	hbkg, hf, hfc = DATA["colour_scheme"]["hi-score"]
	pygame.draw.rect(DISPLAY, hbkg, (sx - (sw + (2 * sp)), sy, sw, sh))
	msg = "Hi-Score: {}".format(game.hi_score)
	# BUTTON_TEXT_FONT.set_bold(True)
	text_surf, text_rect = text_objects(msg, hf, hfc)
	text_rect.center = ((sx - (sw + (2 * sp)) + (sw / 2)), (sy + (sh / 2)))
	DISPLAY.blit(text_surf, text_rect)
	uic, uac, ucc, uf, ufc = DATA["colour_scheme"]["undo"]
	ric, rac, rcc, rf, rfc = DATA["colour_scheme"]["reset"]

	draw_button("undo", sx - (sw + (2 * sp)), sy + sh + (2 * sp), sw, sh, uic, uac, ucc, uf, ufc, action=undo)
	draw_button("reset", sx, sy + sh + (2 * sp), sw, sh, ric, rac, rcc, rf, rfc, action=reset)

	# sleep(5)

	# c = RED
	# x, y, w, h = 20, 20, 120, 120

	#
	# 	BUTTON_TEXT_FONT.set_bold(True)
	# 	text_surf, text_rect = text_objects(msg, BUTTON_TEXT_FONT)
	# 	text_rect.center = ((x + (w / 2)), (y + (h / 2)))
	# 	DISPLAY.blit(text_surf, text_rect)

	pygame.display.update()


def reset(**args):
	print("reset")
	DATA["current_game"].reset()
	DATA["current_game"].gen_random_tile()
	DATA["current_game"].gen_random_tile()


def undo(**args):
	print("undo")
	DATA["current_game"].undo()


def main_loop():
	loop = True
	mouse_state = None
	game = DATA["current_game"]
	change = True
	while loop:
		# print("score:", game.score)
		events = pygame.event.get()
		if change:
			print("game:", game)
			change = False
		for event in events:
			pos = pygame.mouse.get_pos()
			# print("mouse_state", mouse_state, "event", event)
			# if mouse_state and event != pygame.MOUSEMOTION:
			# 	print("mouse_state:", mouse_state)
			if event.type == pygame.QUIT:
				loop = False
			if event.type == pygame.MOUSEBUTTONDOWN:
				print("\tmouse button down", "mouse_state", mouse_state)
				cells = DATA["cells"]
				r = cells["r"]
				c = cells["c"]
				print("pos", pos)
				for i in range(r):
					for j in range(c):
						cx, cy = DATA["cells"][str(i) + " - " + str(j)]["x"], DATA["cells"][str(i) + " - " + str(j)]["y"]
						cw, ch = DATA["cells"][str(i) + " - " + str(j)]["w"], DATA["cells"][str(i) + " - " + str(j)]["h"]
						if cx <= pos[0] <= cx + cw and cy <= pos[1] <= cy + ch:
							cell = game.grid[i][j]
							print("Clicked", cell)
							mouse_state = [cell, pos, False]
							# pygame.event.wait(pygame.MOUSEMOTION)
							# pygame.event.wait(pygame.MOUSEBUTTONUP)

							# lc, mc, rc = pygame.mouse.get_pressed(3)
							# print("holding lc", lc, "mc:", mc, "rc:", rc)
							# mouse_state = None
							# print("released!")
				# print("pygame.mouse.get_pressed(1)", pygame.mouse.get_pressed(3))
				# while lc:
				# 	print("holding lc", lc, "mc:", mc, "rc:", rc)
				# 	mouse_state = None
				# 	print("released!")
				# 	lc, mc, rc = pygame.mouse.get_pressed(3)

			old_grid = DATA["current_game"].grid.copy()
			valid_shift = False

			if event.type == pygame.MOUSEMOTION:
				if mouse_state:
					mouse_state[2]= True

			if event.type == pygame.MOUSEBUTTONUP:
				print("\tmouse button up", "mouse_state", mouse_state)
				if mouse_state and mouse_state[2]:
					# if mouse_state[1] != pos:
					lc, mc, rc = pygame.mouse.get_pressed(3)
					print("holding lc", lc, "mc:", mc, "rc:", rc)
					print("released!")
					xd = mouse_state[1][0] - pos[0]
					yd = mouse_state[1][1] - pos[1]
					mouse_state = None
					valid_shift = False
					print("xd:", xd, "yd:", yd)
					if abs(xd) >= abs(yd):
						if xd >= 0:
							valid_shift = game.shift_grid("LEFT")
							print("shift LEFT")
							change = True
						else:
							valid_shift = game.shift_grid("RIGHT")
							print("shift RIGHT")
							change = True
					else:
						if yd >= 0:
							valid_shift = game.shift_grid("UP")
							print("shift UP")
							change = True
						else:
							valid_shift = game.shift_grid("DOWN")
							print("shift DOWN")
							change = True
				if valid_shift and change and DATA["current_game"].grid != old_grid:
					game.gen_random_tile()
		draw_display()
		loop = game.playable()


if __name__ == "__main__":
	init()
	main_loop()

import pygame
import easygui


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

CIRCLE_MARKER_COLOR = (255, 255, 255) 	# white
LEGEND_MARKER_COLOR = (255, 15, 15) 	# red
BACKGROUND_COLOR = (0, 0, 0) 			# black
CIRCLE_MARKER_SIZE = 10					# diameter of dot
CIRCLE_BORDER_SIZE = 3					# space of the grid circle color shown
SCREEN_PROPORTION = 0.85				# margin space for circle drawing

##################################################
##					Game vars					##
##################################################

DISPLAY = None							# Display surface
TITLE = "2048"						    # title
WIDTH = 750								# width and height
HEIGHT = 750
DATA = {
    "current_screen": "main_menu"
    "current_game": None,
    "game_time": None,
    "colour_scheme": None
}
LOAD_GAME_FILE = "save.txt"
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


# Create and return text objects for blitting
def text_objects(text, font, color=BLACK):
	textSurface = font.render(text, True, color)
	return textSurface, textSurface.get_rect()


# diaplay a button and listen for it to be clicked.
# acts as a controller to update the program mode as well.
# msg 		- 	button text
# x			-	button x
# y			-	button x
# w			-	button width
# h			-	button height
# ic		-	button color
# ac		-	button color when hovering
# action	-	function to be called on click
def draw_button(msg, x, y, w, h, ic, ac, action=None):
	global POP_UP_THREAD
	mouse = pygame.mouse.get_pos()
	click = tuple(pygame.mouse.get_pressed())

	if msg == DATA["mode"]:
		pygame.draw.rect(DISPLAY, SELECTION_COLOR, (x, y, w, h))
		x += SELECTION_WIDTH
		y += SELECTION_WIDTH
		w -= (2 * SELECTION_WIDTH)
		h -= (2 * SELECTION_WIDTH)

	if x + w > mouse[0] > x and y + h > mouse[1] > y:
		pygame.draw.rect(DISPLAY, ac, (x, y, w, h))
		if click[0] == 1:
			DATA["mode"] = msg
			kill_pop_up_thread()
			if action is not None:
				pool = ThreadPool(processes=1)
				print("action:", action)
				if action == reset:
					async_result = pool.apply_async(action, (click, DATA))
				elif action == save or action == load:
					async_result = pool.apply_async(action, (DATA, DISPLAY))
				else:
					async_result = pool.apply_async(action, ())
				f_args = async_result.get()
				if f_args:
					f, arg = f_args
					kill_pop_up_thread()
					POP_UP_THREAD = Thread(target=f, args=arg)
					POP_UP_THREAD.start()
				else:
					print("no function")

				# recalculate buckets on load
				if action == load:
					DATA["buckets"] = calculate_buckets()
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

				event = pygame.event.wait()
	else:
		pygame.draw.rect(DISPLAY, ic, (x, y, w, h))

	BUTTON_TEXT_FONT.set_bold(True)
	text_surf, text_rect = text_objects(msg, BUTTON_TEXT_FONT)
	text_rect.center = ((x + (w / 2)), (y + (h / 2)))
	DISPLAY.blit(text_surf, text_rect)


def load_game():
    with open(LOAD_GAME_FILE, 'r') as f:
        lines = f.readlines
        return lines


# Initialize the DATA dictionary.
# Called immediately on run, before the main loop.
def init():
	global DISPLAY
	pygame.init()
	DISPLAY = pygame.display.set_mode((WIDTH, HEIGHT))
	pygame.display.set_caption(TITLE)
	
    loaded_game = load_game()
    if not loaded_game:
        loaded_game = G2048()
    else:
        loaded_game = G2048(init_grid=loaded_game)
    DATA["current_game"] = loaded_game
	DATA["game_time"] = compute_row_space()
	DATA["colour_scheme"] = compute_spacing()
	DATA["radius"] = compute_radius()
	DATA["circles"] = create_circles()
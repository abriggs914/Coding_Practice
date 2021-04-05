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
	set_circles()
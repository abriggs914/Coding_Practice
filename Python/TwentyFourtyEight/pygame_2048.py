import pygame
import easygui
from multiprocessing.pool import ThreadPool
from threading import Thread
from main import *
from colors import *
import math
import keyboard as kbd

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
# CIRCLE_MARKER_COLOR = (255, 255, 255)  # white
# LEGEND_MARKER_COLOR = (255, 15, 15)  # red
# BACKGROUND_COLOR = "#ffffff" #(0, 0, 0)  # black
CIRCLE_MARKER_SIZE = 10  # diameter of dot
CIRCLE_BORDER_SIZE = 3  # space of the grid circle color shown
SCREEN_PROPORTION = 0.85  # margin space for circle drawing
SELECTION_WIDTH = 5
BUTTON_TEXT_FONT = None  # initialized in init_pygame function
LINE_WIDTH = 1


def colour_func(val, start=(255, 255, 255)):
    # print("val", val)
    math.log(val, 2)
    return 50, 50, 50


colour_scheme_blue_green = {
    "name": ("Blue Green", pygame.font.SysFont("helvetica", 18, bold=1), (0, 23, 66)),
    "background": (26, 62, 135),
    "increment_arrow": (89, 199, 20),
    "decrement_arrow": (89, 199, 20),
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
    "reset": ((0, 33, 113), (30, 65, 149), (0, 73, 255), pygame.font.SysFont("helvetica", 16, bold=1), (255, 255, 255)),
    "menu_title_font": (pygame.font.SysFont("comic sans", 25, bold=1), (255, 255, 255)),
    "new_game": (
        (70, 166, 38), (85, 204, 45), (111, 237, 69), pygame.font.SysFont("helvetica", 16, bold=1), (255, 255, 255)),
    "resume_game": (
        (31, 122, 0), (56, 189, 11), (94, 252, 40), pygame.font.SysFont("helvetica", 16, bold=1), (255, 255, 255)),
    "leaderboard": (
        (49, 176, 72), (42, 212, 73), (64, 245, 97), pygame.font.SysFont("helvetica", 16, bold=1), (255, 255, 255)),
    "settings": (
        (25, 148, 89), (43, 186, 117), (81, 232, 159), pygame.font.SysFont("helvetica", 16, bold=1), (255, 255, 255)),
    "colour_scheme_adj": (
        (21, 93, 140), (43, 130, 186), (87, 184, 247), pygame.font.SysFont("helvetica", 16, bold=1), (255, 255, 255)),
    "dims_adj": (
        (0, 43, 99), (8, 74, 161), (40, 118, 222), pygame.font.SysFont("helvetica", 16, bold=1), (255, 255, 255)),
    "rng": (pygame.font.SysFont("helvetica", 16, bold=1), (255, 255, 255)),
    "rng_hint": (pygame.font.SysFont("helvetica", 12, bold=1), (255, 255, 255)),
    "show_2048": (
        (0, 43, 99), (8, 74, 161), (40, 118, 222), pygame.font.SysFont("helvetica", 16, bold=1), (255, 255, 255)),
    "leaderboard_background": ((0, 23, 66), pygame.font.SysFont("helvetica", 16), (255, 255, 255)),
    "return_main": (
        (68, 91, 173), (94, 122, 219), (138, 156, 222), pygame.font.SysFont("helvetica", 16, bold=1), (255, 255, 255))
}
colour_scheme_blue_green.update({str(k): v for k, v in colour_scheme_blue_green.items() if isinstance(k, int)})
colour_scheme_red_yellow = {
    "name": ("Red Yellow", pygame.font.SysFont("helvetica", 18, bold=1), (171, 0, 0)),
    "background": (74, 31, 30),
    "increment_arrow": (252, 245, 15),
    "decrement_arrow": (252, 245, 15),
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
    "undo": (
        (149, 133, 0), (185, 166, 6), (246, 221, 13), pygame.font.SysFont("helvetica", 16, bold=1), (255, 255, 255)),
    "reset": (
        (153, 61, 0), (186, 87, 21), (255, 101, 0), pygame.font.SysFont("helvetica", 16, bold=1), (255, 255, 255)),
    "menu_title_font": (pygame.font.SysFont("comic sans", 25, bold=1), (202, 215, 98)),
    "new_game": (
        (200, 209, 19), (242, 252, 33), (225, 232, 74), pygame.font.SysFont("helvetica", 16, bold=1), (255, 255, 255)),
    "resume_game": (
        (201, 121, 0), (227, 156, 50), (245, 179, 81), pygame.font.SysFont("helvetica", 16, bold=1), (255, 255, 255)),
    "leaderboard": (
        (171, 83, 0), (217, 121, 30), (237, 145, 57), pygame.font.SysFont("helvetica", 16, bold=1), (255, 255, 255)),
    "settings": (
        (171, 28, 0), (222, 42, 7), (245, 66, 32), pygame.font.SysFont("helvetica", 16, bold=1), (255, 255, 255)),
    "colour_scheme_adj": (
        (156, 26, 9), (194, 36, 16), (201, 51, 32), pygame.font.SysFont("helvetica", 16, bold=1), (255, 255, 255)),
    "dims_adj": (
        (156, 0, 0), (176, 19, 19), (207, 41, 41), pygame.font.SysFont("helvetica", 16, bold=1), (255, 255, 255)),
    "rng": (pygame.font.SysFont("helvetica", 16, bold=1), (255, 255, 255)),
    "rng_hint": (pygame.font.SysFont("helvetica", 12, bold=1), (255, 255, 255)),
    "show_2048": (
        (156, 0, 0), (176, 19, 19), (207, 41, 41), pygame.font.SysFont("helvetica", 16, bold=1), (255, 255, 255)),
    "leaderboard_background": ((171, 0, 0), pygame.font.SysFont("helvetica", 16), (255, 255, 255)),
    "return_main": (
        (209, 50, 50), (237, 71, 71), (222, 104, 104), pygame.font.SysFont("helvetica", 16, bold=1), (255, 255, 255))
}
colour_scheme_red_yellow.update({str(k): v for k, v in colour_scheme_red_yellow.items() if isinstance(k, int)})
colour_scheme_red_grey = {
    "name": ("Red Grey", pygame.font.SysFont("helvetica", 18, bold=1), (224, 0, 0)),
    "background": (138, 10, 10),
    "increment_arrow": (135, 131, 131),
    "decrement_arrow": (135, 131, 131),
    "block": ((135, 131, 131), pygame.font.SysFont("helvetica", 16, bold=1), (255, 255, 255)),
    2: ((176, 21, 21), pygame.font.SysFont("arial", 16, bold=1), (255, 255, 255)),
    4: ((97, 40, 40), pygame.font.SysFont("arial", 16, bold=1), (255, 255, 255)),
    8: ((110, 71, 71), pygame.font.SysFont("arial", 16, bold=1), (255, 255, 255)),
    16: ((252, 43, 43), pygame.font.SysFont("arial", 16, bold=1), (255, 255, 255)),
    32: ((79, 11, 11), pygame.font.SysFont("arial", 16, bold=1), (255, 255, 255)),
    64: ((191, 99, 99), pygame.font.SysFont("arial", 16, bold=1), (255, 255, 255)),
    128: ((56, 9, 9), pygame.font.SysFont("arial", 16, bold=1), (255, 255, 255)),
    256: ((140, 0, 0), pygame.font.SysFont("arial", 16, bold=1), (255, 255, 255)),
    512: ((115, 95, 95), pygame.font.SysFont("arial", 16, bold=1), (255, 255, 255)),
    1024: ((74, 34, 34), pygame.font.SysFont("arial", 16, bold=1), (255, 255, 255)),
    2048: ((224, 0, 0), pygame.font.SysFont("arial", 16, bold=1), (255, 255, 255)),
    "rest": (lambda x: colour_func(x, start=(224, 0, 0)), pygame.font.SysFont("arial", 16, bold=1), (255, 255, 255)),
    "score": ((133, 30, 30), pygame.font.SysFont("helvetica", 16, bold=1), (255, 255, 255)),
    "hi-score": ((224, 0, 0), pygame.font.SysFont("helvetica", 16, bold=1), (66, 75, 78)),
    "undo": (
        (149, 133, 0), (185, 166, 6), (246, 221, 13), pygame.font.SysFont("helvetica", 16, bold=1), (255, 255, 255)),
    "reset": (
        (173, 16, 16), (242, 39, 39), (219, 75, 75), pygame.font.SysFont("helvetica", 16, bold=1), (255, 255, 255)),
    "menu_title_font": (pygame.font.SysFont("comic sans", 25, bold=1), (107, 88, 88)),
    "new_game": (
        (97, 80, 80), (133, 98, 98), (173, 123, 123), pygame.font.SysFont("helvetica", 16, bold=1), (255, 255, 255)),
    "resume_game": (
        (82, 53, 53), (122, 75, 75), (163, 96, 96), pygame.font.SysFont("helvetica", 16, bold=1), (255, 255, 255)),
    "leaderboard": (
        (79, 34, 34), (138, 52, 52), (191, 71, 71), pygame.font.SysFont("helvetica", 16, bold=1), (255, 255, 255)),
    "settings": (
        (82, 24, 24), (133, 28, 28), (191, 33, 33), pygame.font.SysFont("helvetica", 16, bold=1), (255, 255, 255)),
    "colour_scheme_adj": (
        (94, 8, 8), (130, 12, 12), (173, 19, 19), pygame.font.SysFont("helvetica", 16, bold=1), (255, 255, 255)),
    "dims_adj": (
        (143, 0, 0), (201, 16, 16), (255, 43, 43), pygame.font.SysFont("helvetica", 16, bold=1), (255, 255, 255)),
    "rng": (pygame.font.SysFont("helvetica", 16, bold=1), (255, 255, 255)),
    "rng_hint": (pygame.font.SysFont("helvetica", 12, bold=1), (255, 255, 255)),
    "show_2048": (
        (143, 0, 0), (201, 16, 16), (255, 43, 43), pygame.font.SysFont("helvetica", 16, bold=1), (255, 255, 255)),
    "leaderboard_background": ((224, 0, 0), pygame.font.SysFont("helvetica", 16), (255, 255, 255)),
    "return_main": (
        (209, 50, 50), (237, 71, 71), (222, 104, 104), pygame.font.SysFont("helvetica", 16, bold=1), (255, 255, 255))
}
colour_scheme_red_grey.update({str(k): v for k, v in colour_scheme_red_grey.items() if isinstance(k, int)})
colour_scheme_blue_white = {
    "name": ("Blue White", pygame.font.SysFont("helvetica", 18, bold=1), (0, 23, 66)),
    "background": (1, 27, 82),
    "increment_arrow": (179, 199, 255),
    "decrement_arrow": (179, 199, 255),
    "block": ((135, 131, 131), pygame.font.SysFont("helvetica", 16, bold=1), (255, 255, 255)),
    2: ((0, 255, 225), pygame.font.SysFont("arial", 16, bold=1), (26, 39, 51)),
    4: ((255, 255, 255), pygame.font.SysFont("arial", 16, bold=1), (26, 39, 51)),
    8: ((45, 119, 189), pygame.font.SysFont("arial", 16, bold=1), (26, 39, 51)),
    16: ((199, 220, 255), pygame.font.SysFont("arial", 16, bold=1), (26, 39, 51)),
    32: ((19, 155, 189), pygame.font.SysFont("arial", 16, bold=1), (26, 39, 51)),
    64: ((156, 235, 255), pygame.font.SysFont("arial", 16, bold=1), (26, 39, 51)),
    128: ((85, 170, 250), pygame.font.SysFont("arial", 16, bold=1), (26, 39, 51)),
    256: ((0, 71, 214), pygame.font.SysFont("arial", 16, bold=1), (26, 39, 51)),
    512: ((0, 22, 184), pygame.font.SysFont("arial", 16, bold=1), (74, 93, 247)),
    1024: ((42, 54, 145), pygame.font.SysFont("arial", 16, bold=1), (117, 154, 189)),
    2048: ((0, 7, 64), pygame.font.SysFont("arial", 16, bold=1), (74, 93, 247)),
    "rest": (lambda x: colour_func(x, start=(0, 23, 66)), pygame.font.SysFont("arial", 16, bold=1), (255, 255, 255)),
    "score": ((77, 140, 18), pygame.font.SysFont("helvetica", 16, bold=1), (255, 255, 255)),
    "hi-score": ((8, 187, 246), pygame.font.SysFont("helvetica", 16, bold=1), (66, 75, 78)),
    "undo": ((11, 84, 0), (0, 143, 99), (36, 183, 137), pygame.font.SysFont("helvetica", 16, bold=1), (255, 255, 255)),
    "reset": ((0, 33, 113), (30, 65, 149), (0, 73, 255), pygame.font.SysFont("helvetica", 16, bold=1), (255, 255, 255)),
    "menu_title_font": (pygame.font.SysFont("comic sans", 25, bold=1), (255, 255, 255)),
    "new_game": (
        (0, 33, 113), (30, 65, 149), (0, 73, 255), pygame.font.SysFont("helvetica", 16, bold=1), (255, 255, 255)),
    "resume_game": (
        (0, 33, 113), (30, 65, 149), (0, 73, 255), pygame.font.SysFont("helvetica", 16, bold=1), (255, 255, 255)),
    "leaderboard": (
        (0, 33, 113), (30, 65, 149), (0, 73, 255), pygame.font.SysFont("helvetica", 16, bold=1), (255, 255, 255)),
    "settings": (
        (0, 33, 113), (30, 65, 149), (0, 73, 255), pygame.font.SysFont("helvetica", 16, bold=1), (255, 255, 255)),
    "colour_scheme_adj": (
        (0, 33, 113), (30, 65, 149), (0, 73, 255), pygame.font.SysFont("helvetica", 16, bold=1), (255, 255, 255)),
    "dims_adj": (
        (0, 33, 113), (30, 65, 149), (0, 73, 255), pygame.font.SysFont("helvetica", 16, bold=1), (255, 255, 255)),
    "rng": (pygame.font.SysFont("helvetica", 16, bold=1), (255, 255, 255)),
    "rng_hint": (pygame.font.SysFont("helvetica", 12, bold=1), (255, 255, 255)),
    "show_2048": (
        (0, 33, 113), (30, 65, 149), (0, 73, 255), pygame.font.SysFont("helvetica", 16, bold=1), (255, 255, 255)),
    "leaderboard_background": ((0, 7, 64), pygame.font.SysFont("helvetica", 16), (74, 93, 247)),
    "return_main": (
        (68, 91, 173), (94, 122, 219), (138, 156, 222), pygame.font.SysFont("helvetica", 16, bold=1), (255, 255, 255))
}
colour_scheme_blue_white.update({str(k): v for k, v in colour_scheme_blue_white.items() if isinstance(k, int)})

VALID_COLOUR_SCHEMES = (
    colour_scheme_blue_green,
    colour_scheme_red_yellow,
    colour_scheme_red_grey,
    colour_scheme_blue_white
)

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
MENU_STATUS = None
MENU_HOME = "MENU_HOME"
MENU_SETTINGS = "MENU_SETTINGS"
MENU_COLOUR_SCHEME = "MENU_COLOUR_SCHEME"
MENU_LEADERBOARD = "MENU_LEADERBOARD"
LEADERBOARD_SORT_REVERSE = False
LEADERBOARD_SORT_DATE = "LEADERBOARD_SORT_DATE"
LEADERBOARD_SORT_SCORE = "LEADERBOARD_SORT_SCORE"
LEADERBOARD_SORT_HI_TILE = "LEADERBOARD_SORT_HI_TILE"
LEADERBOARD_SORT_MOVES = "LEADERBOARD_SORT_MOVES"
LEADERBOARD_SORT_STATUS = (LEADERBOARD_SORT_DATE, LEADERBOARD_SORT_REVERSE)
MODE_PLAY = False
INPUT_BOX_DIMS = None
INPUT_BOX_RNG = None
MAX_DIMS = 10
MIN_DIMS = 2
SHOW_2048 = True


# ROWS = 11								# Number of rows and columns
# COLS = 11
# DATA = {}								# Dictionary of; circle / radius / spacing data values
# FOLLOW_MOUSE = False					# Control whether the mouse is followed or not
# MARK_CENTER = True						# Control whether the whole grid circle holds the dot or just it's circumference
# CLOCK = pygame.time.Clock()				# Clock and framerate
# FRAME_RATE = 60

class InputBox:

    def __init__(self, x, y, w, h, ic, ac, f, fc, text='', min_width=20, numeric=False, char_limit=None, n_limit=None):
        self.rect = pygame.Rect(x, y, w, h)
        self.ic = ic
        self.ac = ac
        self.f = f
        self.fc = fc
        self.colour = ic
        self.text = text
        self.txt_surface = self.f.render(self.text, True, self.colour)
        self.active = False
        self.min_width = min_width
        self.numeric = numeric
        max_chars = char_limit = w / f.size(" ")[0]
        if not char_limit:
            char_limit = max_chars
        char_limit = min(max_chars, char_limit)
        self.char_limit = char_limit
        if not n_limit or not isinstance(n_limit, range):
            print("adjust n_limit")
            if isinstance(n_limit, int):
                n_limit = range(2, n_limit)
            else:
                n_limit = range(5)
        n_start = 1
        n_stop = max(2, min(10, n_limit.stop))
        self.n_limit = range(min(n_start, n_stop), max(n_start, n_stop), 1)

    def count_n(self):
        txt = self.text
        nums = [s.strip() for s in txt.split(",") if s.strip().isdigit()]
        return len(nums)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                # if self.active:

                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.colour = self.ac if self.active else self.ic
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    print("new_text:", self.text)
                    # if self.text.isdigit():
                    # 	DATA["input_dims"] = int(self.text)
                    self.text = ''
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    txt = event.unicode
                    cn = self.count_n()
                    if len(self.text) < self.char_limit and ((cn in self.n_limit) or (cn < self.n_limit.start)):
                        if self.numeric:
                            if str(txt).isdigit():
                                self.text += txt
                                # DATA["input_dims"] = int(self.text)
                        else:
                            self.text += txt
                            # DATA["input_dims"] = self.text

                # Re-render the text.
                if self.text:
                    self.txt_surface = self.f.render(self.text, True, self.fc)

    def increment(self):
        self.text = int(self.text) + 1

    def decrement(self):
        self.text = int(self.text) - 1

    def set_text(self, txt):
        self.text = txt

    def clear(self):
        self.set_text("")

    def update(self):
        # Resize the box if the text is too long.
        width = max(self.min_width, self.txt_surface.get_width() + 10)
        self.rect.w = width

    def draw(self, screen):
        self.txt_surface = self.f.render(str(self.text), True, self.colour)
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
        # Blit the rect.
        pygame.draw.rect(screen, self.colour, self.rect, 2)
        draw_button("X", self.rect.right + 10, self.rect.y, 20, 20, self.ic, self.ac, self.colour, self.f, self.fc, self.clear)


class DemoGrid:

    def __init__(self, x, y, w, h, colour_scheme, spaces=None):
        if spaces is None:
            spaces = [[None, 2, 4, 8], [16, 32, 64, 128], [256, 512, 1024, 2048], [4096, 8192, 16384, 32768]]
        self.game = G2048(len(spaces), spaces)
        self.colour_scheme = colour_scheme
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def draw(self):
        global DISPLAY
        game = self.game
        grid = game.grid
        colour_scheme = self.colour_scheme
        w, h = self.w, self.h
        ww, wh = WIDTH, HEIGHT
        ratio = min(w / ww, h / wh)
        DEMO_PAD = PAD * ratio
        DEMO_SPACE = SPACE * ratio
        # print("grid", DATA["current_game"])
        # draw_circles()
        # draw_button("click me", 20, 20, 120, 120, RED, YELLOW, GREEN, do_print)

        # print(dict_print(DATA, "DATA"))

        n = len(grid)
        m = len(grid[0])

        bs = (2 * DEMO_PAD) + ((n - 1) * DEMO_SPACE)
        w_rs = w - bs
        h_rs = h - bs
        cw = w_rs / m
        ch = h_rs / n

        x0, y0 = self.x + DEMO_PAD, self.y + DEMO_PAD
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
                x = x0 + (j * (cw + DEMO_SPACE))
                y = y0 + (i * (ch + DEMO_SPACE))
                # print("i", i, "j", j, "\nx", x, "y", y, "\nc", c)
                # print("c", c, "typr(\"c\")", type(c), "isinstance(\"'function'\")", isinstance(c, type(colour_func)))

                pygame.draw.rect(DISPLAY, c, (x, y, cw, ch))

                val = val if val != "block" else ""
                text_surf, text_rect = text_objects(str(val), f, fc)
                text_rect.center = ((x + (cw / 2)), (y + (ch / 2)))
                DISPLAY.blit(text_surf, text_rect)


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
    text_surface = font.render(text, True, color)
    return text_surface, text_surface.get_rect()


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

fafdsd = 1


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
    global DISPLAY, MENU_STATUS, GRID_X, GRID_Y
    DISPLAY = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(TITLE)
    MENU_STATUS = MENU_HOME

    loaded_game = load_game()
    if not loaded_game:
        loaded_game = G2048(random_tile_values=[2])
    else:
        loaded_game = G2048(init_spaces=loaded_game, random_tile_values=[2])
    DATA["current_game"] = loaded_game
    DATA["mode"] = "play"
    # DATA["colour_scheme"] = colour_scheme_blue_green
    # DATA["colour_scheme"] = colour_scheme_red_yellow
    # DATA["colour_scheme"] = colour_scheme_red_grey
    DATA["colour_scheme"] = colour_scheme_blue_white
    # DATA["colour_func_type"] = type(colour_func)
    init_button_font()

    # print("w:", WIDTH, "h:", HEIGHT, "gw:", GRID_WIDTH, "gh:", GRID_HEIGHT, "p:", PAD, "s:", SPACE)
    GRID_X = (WIDTH - GRID_WIDTH) * 0.5
    GRID_Y = (HEIGHT - GRID_HEIGHT) * 0.95
    # print("gx:", GRID_X, "gy:", GRID_Y)
    DATA["input_dims"] = MIN_DIMS


def draw_return_main(ww, wh, colour_scheme):
    bic, bac, bcc, bf, bfc = colour_scheme["return_main"]
    x = ww * 0.05
    y = wh * 0.05
    w = ww * 0.10
    h = wh * 0.10
    # <-  4 points, 3 lines
    p1 = (x + (w / 2), y + (h * 0.35))
    p2 = (x + (w * 0.2), y + (h / 2))
    p3 = (x + (w - (w * 0.2)), y + (h / 2))
    p4 = (x + (w / 2), y + (h - (h * 0.35)))
    draw_button(
        "",
        x,
        y,
        w,
        h,
        bic,
        bac,
        bcc,
        bf,
        bfc,
        return_to_main
    )
    pygame.draw.line(DISPLAY, (255, 255, 255), p2, p1, 5)
    pygame.draw.line(DISPLAY, (255, 255, 255), p2, p3, 5)
    pygame.draw.line(DISPLAY, (255, 255, 255), p2, p4, 5)


def draw_menu(event):
    global DISPLAY, DATA, MENU_STATUS, INPUT_BOX_DIMS, INPUT_BOX_RNG
    colour_scheme = DATA["colour_scheme"]
    bg = colour_scheme["background"]
    DISPLAY.fill(bg)
    game = DATA["current_game"]
    f, fc = colour_scheme["menu_title_font"]
    nic, nac, ncc, nf, nfc = colour_scheme["new_game"]
    ric, rac, rcc, rf, rfc = colour_scheme["resume_game"]
    lic, lac, lcc, lf, lfc = colour_scheme["leaderboard"]
    sic, sac, scc, sf, sfc = colour_scheme["settings"]
    cic, cac, ccc, cf, cfc = colour_scheme["colour_scheme_adj"]
    dic, dac, dcc, df, dfc = colour_scheme["dims_adj"]
    slic, slac, slcc, slf, slfc = colour_scheme["show_2048"]
    rngf, rngfc = colour_scheme["rng"]
    rnghf, rnghfc = colour_scheme["rng_hint"]
    lbbg, lbf, lbfc = colour_scheme["leaderboard_background"]
    ww, wh = WIDTH, HEIGHT
    v_space = wh * 0.05
    h_space = ww * 0.02

    x_title = ww * 0.2
    y_title = wh * 0.06
    w_title = ww * 0.6
    h_title = wh * 0.1
    x_btn = ww * 0.3
    y_btn = y_title + h_title + v_space
    w_btn = ww * 0.4
    h_btn = wh * 0.06

    if MENU_STATUS == MENU_HOME:

        text_surf, text_rect = text_objects("Welcome to 2048!", f, fc)
        text_rect.center = ((x_title + (w_title / 2)), (y_title + (h_title / 2)))
        DISPLAY.blit(text_surf, text_rect)

        draw_button("Play New Game", x_btn, y_btn + (0 * (h_btn + v_space)), w_btn, h_btn, nic, nac, ncc, nf, nfc,
                    new_game)
        draw_button("Resume Game", x_btn, y_btn + (1 * (h_btn + v_space)), w_btn, h_btn, ric, rac, rcc, rf, rfc,
                    resume_game)
        draw_button("Leaderboard", x_btn, y_btn + (2 * (h_btn + v_space)), w_btn, h_btn, lic, lac, lcc, lf, lfc,
                    leaderboard)
        draw_button("Settings", x_btn, y_btn + (3 * (h_btn + v_space)), w_btn, h_btn, sic, sac, scc, sf, sfc, settings)

    elif MENU_STATUS == MENU_LEADERBOARD:
        draw_return_main(ww, wh, colour_scheme)
        scores = read_high_scores()

        x_lb = ww * 0.2
        y_lb = y_title + h_title
        w_lb = ww * 0.6
        h_lb = wh * 0.06

        if LEADERBOARD_SORT_STATUS[0] == LEADERBOARD_SORT_SCORE:
            scores.sort(key=lambda s: s.score)
        elif LEADERBOARD_SORT_STATUS[0] == LEADERBOARD_SORT_HI_TILE:
            scores.sort(key=lambda s: s.hi_tile_v)
        elif LEADERBOARD_SORT_STATUS[0] == LEADERBOARD_SORT_DATE:
            scores.sort(key=lambda s: s.date)
        elif LEADERBOARD_SORT_STATUS[0] == LEADERBOARD_SORT_MOVES:
            scores.sort(key=lambda s: s.moves)

        asc_desc = "Ascending"
        if LEADERBOARD_SORT_STATUS[1]:
            scores.sort(reverse=1)
            asc_desc = "Descending"

        # print("scores\n\t", scores)

        text_surf, text_rect = text_objects("Leaderboard", df, dfc)
        text_rect.center = ((x_lb + (w_lb / 2)), (y_lb + (h_btn / 2)))
        DISPLAY.blit(text_surf, text_rect)

        max_h = 6
        inc_h = 1 + max(0, min(max_h, len(scores)))
        x_lbb = x_lb
        y_lbb = y_lb + (min(max_h + 1, inc_h + 2) * (h_lb + h_space))
        w_lbb = (w_lb / 5) - h_space
        h_lbb = (1 * (h_lb + h_space))

        pygame.draw.rect(DISPLAY, lbbg, (x_lb, y_lb + (1 * (h_lb + h_space)), w_lb, (inc_h * (h_lb + h_space))))
        # pygame.draw.rect(DISPLAY, (255,255,255), (x_lb, y_lb + (1 * (h_lb + h_space)), w_lb, (inc_h * (h_lb + h_space))))

        header = ["Date", "Score", "Max Tile", "Moves"]
        funcs = [sort_leaderboard_by_date, sort_leaderboard_by_score, sort_leaderboard_by_hi_tile, sort_leaderboard_by_moves]
        lw = 4
        lh = len(header)
        x_sc = x_lb + 5
        y_sc = y_lb + (1 * (h_lb + h_space)) + 5
        w_sc = w_lb - 10
        h_sc = ((inc_h * (h_lb + h_space)) - 10) / max_h
        # w_sc = ((w_sc - h_space - lw) / len(header))
        w_sc = (w_sc / lh) - (h_space / 2)
        # pygame.draw.line(DISPLAY, lbfc, (x_sc - ((lw + h_space) / lh), y_sc),
        #                  (x_sc - ((lw + h_space) / lh), y_sc + (h_sc * max_h)), 3)
        # print("x_sc:", x_sc, "y_sc", y_sc, "(x_sc, y_sc, x_sc, y_sc + (h_sc")
        for i, score in enumerate(scores[:max_h]):
            dat = list(score)
            if i == 0:
                for j, title in enumerate(header):
                    x_cell = x_sc + (j * (w_sc + ((lw + h_space) / 2)))
                    # background column button
                    # pygame.draw.rect(DISPLAY, lbfc, (x_cell, y_sc, w_sc, h_sc))
                    draw_button("", x_cell, y_sc, w_sc, h_sc * max_h, lbbg, lbfc, lbfc, lbf, lbfc, funcs[j])
                    text_surf, text_rect = text_objects(title, lbf, lbfc)
                    text_rect.center = ((x_cell + ((w_sc) / 2)), (y_sc + (h_sc / 2)))
                    DISPLAY.blit(text_surf, text_rect)

                    for k, d in enumerate(dat):
                        x_t = x_sc + (k * (w_sc + ((lw + h_space) / 2)))
                        y_t = y_sc + (1 * (h_sc - ((v_space + lw) / 2)))
                        text_surf, text_rect = text_objects(str(d), lbf, lbfc)
                        text_rect.center = ((x_t + ((w_sc) / 2)), (y_t + (h_sc / 2)))
                        DISPLAY.blit(text_surf, text_rect)
                    if j > 0:
                        pygame.draw.line(DISPLAY, lbfc, (x_cell - ((lw + h_space) / lh), y_sc), (x_cell - ((lw + h_space) / lh), y_sc + (h_sc * inc_h)), 3)
                        # pygame.draw.line(DISPLAY, (0,255,0), (x_cell - ((lw + h_space) / lh) + (h_space / 2), y_sc), (x_cell - ((lw + h_space) / 2) + (h_space / 2), h_lb * inc_h))

            else:
                for k, d in enumerate(dat):
                    x_t = x_sc + (k * (w_sc + ((lw + h_space) / 2)))
                    y_t = y_sc + ((i + 1) * (h_sc))
                    text_surf, text_rect = text_objects(str(d), lbf, lbfc)
                    text_rect.center = ((x_t + ((w_sc) / 2)), (y_t + (h_sc / 2)))
                    DISPLAY.blit(text_surf, text_rect)

        pygame.draw.line(DISPLAY, lbfc, (x_sc, y_sc), (x_sc, y_sc + (h_sc * max_h)), 3)  # left
        pygame.draw.line(DISPLAY, lbfc, (x_sc + w_lb - 10, y_sc), (x_sc + w_lb - 10, y_sc + (h_sc * max_h)), 3)  # right
        pygame.draw.line(DISPLAY, lbfc, (x_sc, y_sc), (x_sc + w_lb - 10, y_sc), 3)  # top
        pygame.draw.line(DISPLAY, lbfc, (x_sc, y_sc + h_sc), (x_sc + w_lb - 10, y_sc + h_sc), 3)  # top
        pygame.draw.line(DISPLAY, lbfc, (x_sc, y_sc + (h_sc * max_h)), (x_sc + w_lb - 10, y_sc + (h_sc * max_h)), 3)  # bottom
        pygame.draw.rect(DISPLAY, (255, 255, 255), (x_lbb, y_lbb, w_lb, (1 * (h_lb + h_space))))

        bf = pygame.font.SysFont("arial", 12)
        draw_button("By Date", x_lbb + (0 * (h_space + w_lbb)) + 5, y_lbb + 5, w_lbb - 10, h_lbb - 10, lic, lac, lcc, bf, lfc, sort_leaderboard_by_date)
        draw_button("By Score", x_lbb + (1 * (h_space + w_lbb)) + 5, y_lbb + 5, w_lbb - 10, h_lbb - 10, lic, lac, lcc, bf, lfc, sort_leaderboard_by_score)
        draw_button("By Hi Tile", x_lbb + (2 * (h_space + w_lbb)) + 5, y_lbb + 5, w_lbb - 10, h_lbb - 10, lic, lac, lcc, bf, lfc, sort_leaderboard_by_hi_tile)
        draw_button("By Moves", x_lbb + (3 * (h_space + w_lbb)) + 5, y_lbb + 5, w_lbb - 10, h_lbb - 10, lic, lac, lcc, bf, lfc, sort_leaderboard_by_moves)
        draw_button(asc_desc, x_lbb + (4 * (h_space + w_lbb)) + 5, y_lbb + 5, w_lbb - 10, h_lbb - 10, lic, lac, lcc, bf, lfc, sort_leaderboard_reverse)

    elif MENU_STATUS == MENU_COLOUR_SCHEME:
        l = len(VALID_COLOUR_SCHEMES)

        def c_p_r_f(x):
            return 2 if x == 0 or (x % 3 != 0 and x < 7) else 3

        def r_p_c_f(x):
            return 1 if x < 4 else math.ceil(x / c_p_r_f(x))

        col_per_row = c_p_r_f(l)
        row_per_col = r_p_c_f(l)
        w_demo = ((ww - (2 * PAD) - ((col_per_row - 1) * h_space)) / max(1, col_per_row))  #
        h_demo = ((wh - (2 * PAD) - ((row_per_col - 1) * v_space)) / max(1, row_per_col))  #
        clicked = [0 for i in range(len(VALID_COLOUR_SCHEMES))]
        for i, cs in enumerate(VALID_COLOUR_SCHEMES):
            r = i // col_per_row
            c = i % col_per_row
            x = PAD + (c * (w_demo + h_space))
            y = PAD + (r * (h_demo + v_space))
            # rect = pygame.Rect(x, y, w_demo, h_demo)
            # vals = {"h_space": h_space, "i": i, "(r, c)": (r, c), "x": x, "y": y, "cpr": col_per_row, "rpc:": row_per_col, "rect:": rect}
            # print(dict_print(vals, "Vals"))
            # print("i", i, "(r, c)", (r, c), "(rpc, cpr)", (row_per_col, col_per_row), "rect: <{}>".format(i), rect)

            def check():
                clicked[i] = 1

            draw_button("".format(i), x, y, w_demo, h_demo, sic, sac, scc, sf, sfc, check)
            tbc = (0, 0, 0)
            name, nmf, nmfc = cs["name"]
            snmfc = sum(nmfc)
            if snmfc < 200:
                tbc = (255, 255, 255)
            pygame.draw.rect(DISPLAY, tbc, (x + (w_demo * 0.1), y + ((h_demo * 0.1) * 0.2), w_demo * 0.8, ((h_demo * 0.1) * 0.8)))
            text_surf, text_rect = text_objects(name, nmf, nmfc)
            # text_rect.center = ((x + (w_demo / 2)), (y + ((h_demo * 0.1) / 2)))
            cent = ((x + (w_demo * 0.1)) + ((w_demo * 0.8) / 2), (y + ((h_demo * 0.1) * 0.2)) + (((h_demo * 0.1) * 0.8) / 2))
            text_rect.center = cent
            DISPLAY.blit(text_surf, text_rect)

            demo_grid = DemoGrid(x, y + (h_demo * 0.1), w_demo, h_demo * 0.9, cs)
            demo_grid.draw()

        new_cs = [i for i, v in enumerate(clicked) if v]
        if new_cs:
            DATA["colour_scheme"] = VALID_COLOUR_SCHEMES[new_cs[0]]
            MENU_STATUS = MENU_SETTINGS
        # print("clicked", clicked, "new_cs:", new_cs)

    elif MENU_STATUS == MENU_SETTINGS:
        draw_return_main(ww, wh, colour_scheme)
        draw_button(
            "Colour Scheme",
            x_btn,
            y_btn + (0 * (h_btn + v_space)),
            w_btn,
            h_btn,
            cic,
            cac,
            ccc,
            cf,
            cfc,
            change_colour_scheme
        )

        hw_btn = w_btn / 2
        inc_dec_v_space = v_space / 10

        x_ia = x_btn + (w_btn - (h_space + ((hw_btn + h_space) / 2))) + h_space
        y_ia = y_btn + (1 * (h_btn + v_space))
        w_ia = hw_btn * 0.125
        h_ia = (h_btn / 2) - inc_dec_v_space

        x_da = x_btn + (w_btn - (h_space + ((hw_btn + h_space) / 2))) + h_space
        y_da = y_btn + (1 * (h_btn + v_space)) + (h_btn / 2) + inc_dec_v_space
        w_da = hw_btn * 0.125
        h_da = (h_btn / 2) - inc_dec_v_space

        draw_button(
            "",
            x_ia,
            y_ia,
            w_ia,
            h_ia,
            cic,
            cac,
            ccc,
            cf,
            cfc,
            increment_dims
        )
        draw_button(
            "",
            x_da,
            y_da,
            w_da,
            h_da,
            cic,
            cac,
            ccc,
            cf,
            cfc,
            decrement_dims
        )

        ialc = colour_scheme["increment_arrow"]
        dalc = colour_scheme["increment_arrow"]

        # <-  4 points, 3 lines
        ia_p1 = (x_ia + (w_ia * 0.15), y_ia + (h_ia * 0.65))
        ia_p2 = (x_ia + (w_ia / 2), y_ia + (h_ia * 0.2))
        ia_p3 = (x_ia + (w_ia * 0.85), y_ia + (h_ia * 0.65))

        pygame.draw.line(DISPLAY, ialc, ia_p1, ia_p2, 5)
        pygame.draw.line(DISPLAY, ialc, ia_p3, ia_p2, 5)

        da_p1 = (x_da + (w_da * 0.15), y_da + (h_da * 0.35))
        da_p2 = (x_da + (w_da / 2), y_da + (h_da * 0.8))
        da_p3 = (x_da + (w_da * 0.85), y_da + (h_da * 0.35))

        pygame.draw.line(DISPLAY, dalc, da_p1, da_p2, 5)
        pygame.draw.line(DISPLAY, dalc, da_p3, da_p2, 5)


        # draw_text_input(
        # 	x_btn,
        # 	y_btn + (3 * (h_btn + v_space)),
        # 	w_btn,
        # 	h_btn,
        # 	(110, 110, 110),
        # 	(216, 42, 42),
        # 	pygame.font.SysFont("arial", 14),
        # 	(114, 146, 176)
        # )
        INPUT_BOX_DIMS.handle_event(event)
        INPUT_BOX_DIMS.update()
        INPUT_BOX_DIMS.draw(DISPLAY)

        x_label_dims = x_btn
        y_label_dims = y_btn + (1 * (h_btn + v_space))
        w_label_dims = w_btn - (h_space + ((hw_btn + h_space) / 2))
        h_label_dims = h_btn

        text_surf, text_rect = text_objects("# Rows X Columns", df, dfc)
        text_rect.center = ((x_label_dims + (w_label_dims / 2)), (y_label_dims + (h_label_dims / 2)))
        DISPLAY.blit(text_surf, text_rect)

        x_label_rng = x_btn
        y_label_rng = y_btn + (2 * (h_btn + v_space))
        w_label_rng = w_btn - (h_space + ((hw_btn + h_space) / 2))
        h_label_rng = h_btn

        text_surf, text_rect = text_objects("Random tiles", rngf, rngfc)
        text_rect.center = ((x_label_rng + (w_label_rng / 2)), (y_label_rng + (h_label_rng / 2)))
        DISPLAY.blit(text_surf, text_rect)

        fs = f.get_linesize()
        txt_w, txt_h = f.size("Random Tiles")
        n_f = f
        text_surf, text_rect = text_objects("ex. '2, 4'", rnghf, rnghfc)
        text_rect.center = ((x_label_rng + (w_label_rng / 2)), ((y_label_rng + txt_h) + (h_label_rng / 2)))
        DISPLAY.blit(text_surf, text_rect)

        INPUT_BOX_RNG.handle_event(event)
        INPUT_BOX_RNG.update()
        INPUT_BOX_RNG.draw(DISPLAY)

        c_s2048 = 0.85
        ic_s2048 = 1 - c_s2048

        draw_button(
            "Show 2048",
            x_btn,
            y_btn + (3 * (h_btn + v_space)),
            w_btn * c_s2048,
            h_btn,
            slic,
            slac,
            slcc,
            slf,
            slfc,
            show_2048
        )

        x_cb = x_btn + (w_btn * c_s2048) + 5
        y_cb = y_btn + (3 * (h_btn + v_space))
        w_cb = (w_btn - 5) * ic_s2048
        h_cb = h_btn

        x_icb = x_btn + (w_btn * c_s2048) + 5 + 5
        y_icb = y_btn + (3 * (h_btn + v_space)) + 5
        w_icb = (w_btn - 5) * ic_s2048 - 10
        h_icb = h_btn - 10

        # pygame.draw.rect(DISPLAY, slic, (x_cb, y_cb, w_cb, h_cb))
        draw_button("", x_cb, y_cb, w_cb, h_cb, slic, slic, slcc, slf, slfc, show_2048)
        pygame.draw.rect(DISPLAY, slac, (x_icb, y_icb, w_icb, h_icb))

        if SHOW_2048:
            p1 = (x_icb + (0.15 * w_icb), y_icb + (0.6 * h_icb))
            p2 = (x_icb + (0.45 * w_icb), y_icb + (0.8 * h_icb))
            p3 = (x_icb + (0.8 * w_icb), y_icb + (0.25 * h_icb))
            pygame.draw.line(DISPLAY, ialc, p1, p2, 4)
            pygame.draw.line(DISPLAY, ialc, p2, p3, 4)



    pygame.display.update()


#
# def draw_settings():
# 	global DISPLAY
# 	DISPLAY.fill(BACKGROUND_COLOR)
# 	game = DATA["current_game"]
# 	colour_scheme = DATA["colour_scheme"]
# 	f, fc = colour_scheme["menu_title_font"]
# 	ww, wh = WIDTH, HEIGHT
# 	v_space = wh * 0.05
#
# 	x_title = ww * 0.2
# 	y_title = wh * 0.06
# 	w_title = ww * 0.6
# 	h_title = wh * 0.1
# 	x_btn = ww * 0.3
# 	y_btn = y_title + h_title + v_space
# 	w_btn = ww * 0.4
# 	h_btn = wh * 0.06
#
# 	draw_button("Colour Scheme", x_btn, y_btn + (3 * (h_btn + v_space)), w_btn, h_btn, cic, cac, ccc, cf, cfc, change_colour_scheme)
# 	draw_button("Change Grid Size", x_btn, y_btn + (4 * (h_btn + v_space)), w_btn, h_btn, cic, cac, ccc, cf, cfc, change_dims)
# 	pygame.display.update()


# def draw_text_input(x, y, w, h, ic, ac, f, fc):
# 	global DISPLAY
# 	mouse = pygame.mouse.get_pos()
# 	click = tuple(pygame.mouse.get_pressed())
# 	input_box = pygame.Rect(x, y, w, h)
# 	active = False
# 	if click[0]:
# 		# If the user clicked on the input_box rect.
# 		if input_box.collidepoint(mouse):
# 			# Toggle the active variable.
# 			active = not active
# 		else:
# 			active = False
# 		# Change the current color of the input box.
# 		color = ac if active else ic
#
# 	pygame.key.set_text_input_rect(input_box)
# 	pygame.key.start_text_input()
# 	print("pressed", pressed)
# 	text = ""
# 	if pressed:
# 		if active:
# 			if pressed == pygame.K_RETURN:
# 				print(text)
# 				text = ""
# 			elif pressed == pygame.K_BACKSPACE:
# 				text = pressed[:-1]
# 			else:
# 				text += pressed
# 	pygame.key.stop_text_input()
# 	txt_surface = f.render(text, True, fc)
# 	width = max(200, txt_surface.get_width()+10)
# 	input_box.w = width
# 	DISPLAY.blit(txt_surface, (input_box.x+5, input_box.y+5))
# 	pygame.draw.rect(DISPLAY, fc, input_box, 2)


def new_game():
    global MODE_PLAY
    print("new game")
    MODE_PLAY = True


def resume_game():
    global MODE_PLAY
    print("resume game")
    MODE_PLAY = True


def leaderboard():
    global MENU_STATUS
    print("leaderboard")
    MENU_STATUS = MENU_LEADERBOARD


def settings():
    global MENU_STATUS
    print("settings")
    MENU_STATUS = MENU_SETTINGS


def sort_leaderboard_by_date():
    global LEADERBOARD_SORT_STATUS
    print("sorting by date")
    LEADERBOARD_SORT_STATUS = LEADERBOARD_SORT_DATE, LEADERBOARD_SORT_REVERSE


def sort_leaderboard_by_score():
    global LEADERBOARD_SORT_STATUS
    print("sorting by score")
    LEADERBOARD_SORT_STATUS = LEADERBOARD_SORT_SCORE, LEADERBOARD_SORT_STATUS


def sort_leaderboard_by_hi_tile():
    global LEADERBOARD_SORT_STATUS
    print("sorting by hi tile")
    LEADERBOARD_SORT_STATUS = LEADERBOARD_SORT_HI_TILE, LEADERBOARD_SORT_STATUS


def sort_leaderboard_by_moves():
    global LEADERBOARD_SORT_STATUS
    print("sorting by moves")
    LEADERBOARD_SORT_STATUS = LEADERBOARD_SORT_MOVES, LEADERBOARD_SORT_STATUS


def sort_leaderboard_reverse():
    global LEADERBOARD_SORT_STATUS, LEADERBOARD_SORT_REVERSE
    print("LEADERBOARD_SORT_STATUS:", LEADERBOARD_SORT_STATUS, "LEADERBOARD_SORT_REVERSE", LEADERBOARD_SORT_REVERSE)
    LEADERBOARD_SORT_REVERSE = not LEADERBOARD_SORT_REVERSE
    LEADERBOARD_SORT_STATUS = LEADERBOARD_SORT_STATUS[0], LEADERBOARD_SORT_REVERSE


def show_2048():
    global SHOW_2048
    SHOW_2048 = not SHOW_2048


def return_to_main():
    global MENU_STATUS
    print("returning to main menu")
    MENU_STATUS = MENU_HOME


# loop = True
# while loop:
# 	events = pygame.event.get()
# 	kbd_q = kbd.is_pressed('q')
# 	for event in events:
# 		pos = pygame.mouse.get_pos()
# 		if kbd_q or event.type == pygame.QUIT:
# 			loop = False
# 	draw_settings()


def increment_dims():
    DATA["input_dims"] = min(MAX_DIMS, DATA["input_dims"] + 1)
    print("increment dims: {}".format(DATA["input_dims"]))
    INPUT_BOX_DIMS.set_text(DATA["input_dims"])
    INPUT_BOX_DIMS.draw(DISPLAY)


def decrement_dims():
    DATA["input_dims"] = max(MIN_DIMS, DATA["input_dims"] - 1)
    print("decrement dims: {}".format(DATA["input_dims"]))
    INPUT_BOX_DIMS.set_text(DATA["input_dims"])
    INPUT_BOX_DIMS.draw(DISPLAY)


def change_colour_scheme():
    global MENU_STATUS
    print("change colour scheme")
    MENU_STATUS = MENU_COLOUR_SCHEME


# def change_dims():
# 	print("change dims")


def draw_display():
    global DISPLAY
    colour_scheme = DATA["colour_scheme"]
    bg = colour_scheme["background"]
    DISPLAY.fill(bg)
    game = DATA["current_game"]
    grid = game.grid
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

            val = val if val != "block" else ""
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


def reset():
    print("reset")
    DATA["current_game"].reset()
    DATA["current_game"].gen_random_tile()
    DATA["current_game"].gen_random_tile()


def undo():
    print("undo")
    DATA["current_game"].undo()


def menu_loop():
    global INPUT_BOX_DIMS, INPUT_BOX_RNG
    loop = True

    ww, wh = WIDTH, HEIGHT
    v_space = wh * 0.05
    h_space = ww * 0.02

    x_title = ww * 0.2
    y_title = wh * 0.06
    w_title = ww * 0.6
    h_title = wh * 0.1
    x_btn = ww * 0.3
    y_btn = y_title + h_title + v_space
    w_btn = ww * 0.4
    h_btn = wh * 0.06
    hw_btn = w_btn / 2
    print("\nhw_btn: {}\n(hw_btn * 0.125): {}\nh_space: {}\nw_btn: {}\n((hw_btn + h_space) / 2): {}\n".format(hw_btn, (
            hw_btn * 0.125), h_space, w_btn, ((hw_btn + h_space) / 2)))

    INPUT_BOX_DIMS = InputBox(
        # x_btn + (hw_btn * 0.125) + h_space + ((w_btn + h_space) / 2),
        x_btn + (w_btn - (h_space + ((hw_btn + h_space) / 2))) + (hw_btn * 0.125) + h_space + h_space,
        # w_btn - (h_space + ((hw_btn + h_space) / 2))
        y_btn + (1 * (h_btn + v_space)),
        w_btn - ((hw_btn * 0.125) + h_space + ((hw_btn + h_space) / 2)),
        h_btn,
        (110, 110, 110),
        (216, 42, 42),
        pygame.font.SysFont("arial", 18),
        (114, 146, 176),
        text=str(DATA["input_dims"]),
        min_width=30,
        numeric=True,
        char_limit=25,
        n_limit=5
    )

    x_label_rng = x_btn
    y_label_rng = y_btn + (2 * (h_btn + v_space))
    w_label_rng = w_btn - (h_space + ((hw_btn + h_space) / 2))
    h_label_rng = h_btn

    INPUT_BOX_RNG = InputBox(
        # x_btn + (hw_btn * 0.125) + h_space + ((w_btn + h_space) / 2),
        # (x_btn) + ((w_label_rng - (0.45 * w_label_rng)) / 2),
        x_label_rng + w_label_rng,# - (w_btn * 0.45),
        # w_btn - (h_space + ((hw_btn + h_space) / 2))
        y_label_rng + h_space,
        w_btn * 0.45,
        h_btn,
        (110, 110, 110),
        (216, 42, 42),
        pygame.font.SysFont("arial", 18),
        (114, 146, 176),
        text=str(DATA["input_dims"]),
        min_width=80,
        numeric=False,
        char_limit=25,
        n_limit=10
    )
    # TODO: review above hardcoded values
    while loop:
        events = pygame.event.get()
        kbd_q = kbd.is_pressed('q')
        for event in events:
            pos = pygame.mouse.get_pos()
            if kbd_q or event.type == pygame.QUIT:
                loop = False
            else:
                draw_menu(event)


def main_loop():
    loop = True
    mouse_state = None
    game = DATA["current_game"]
    change = True
    while loop:
        # print("score:", game.score)
        events = pygame.event.get()

        kbd_w = kbd.is_pressed('w')
        kbd_ua = kbd.is_pressed('up')
        kbd_a = kbd.is_pressed('a')
        kbd_la = kbd.is_pressed('left')
        kbd_s = kbd.is_pressed('s')
        kbd_da = kbd.is_pressed('down')
        kbd_d = kbd.is_pressed('d')
        kbd_ra = kbd.is_pressed('right')
        str_dir_keys = ["kbd_w", "kbd_ua", "kbd_a", "kbd_la", "kbd_s", "kbd_da", "kbd_d", "kbd_ra"]
        dir_keys = [kbd_w, kbd_ua, kbd_a, kbd_la, kbd_s, kbd_da, kbd_d, kbd_ra]
        a_dir_keys = any(dir_keys)
        kbd_q = kbd.is_pressed('q')

        if change:
            print("game:", game)
            change = False
        for event in events:
            pos = pygame.mouse.get_pos()
            # print("mouse_state", mouse_state, "event", event)
            # if mouse_state and event != pygame.MOUSEMOTION:
            # 	print("mouse_state:", mouse_state)
            if kbd_q or event.type == pygame.QUIT:
                loop = False
            if a_dir_keys or event.type == pygame.MOUSEBUTTONDOWN:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    print("\tmouse button down", "mouse_state", mouse_state)
                else:
                    print("dir_keys:", "\n\t" + dict_print(dict(zip(str_dir_keys, dir_keys)), "dir_keys"))
                cells = DATA["cells"]
                r = cells["r"]
                c = cells["c"]
                print("pos", pos)
                for i in range(r):
                    for j in range(c):
                        cx, cy = DATA["cells"][str(i) + " - " + str(j)]["x"], DATA["cells"][str(i) + " - " + str(j)][
                            "y"]
                        cw, ch = DATA["cells"][str(i) + " - " + str(j)]["w"], DATA["cells"][str(i) + " - " + str(j)][
                            "h"]
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

            valid_shift = False

            # used to simulate long press + drag mouse event
            if event.type == pygame.MOUSEMOTION:
                if mouse_state:
                    mouse_state[2] = True

            if a_dir_keys or event.type == pygame.MOUSEBUTTONUP:
                print("\tmouse button up", "mouse_state", mouse_state)
                if a_dir_keys or (mouse_state and mouse_state[2]):
                    # if mouse_state[1] != pos:
                    lc, mc, rc = pygame.mouse.get_pressed(3)
                    if mouse_state and mouse_state[2]:
                        xd = mouse_state[1][0] - pos[0]
                        yd = mouse_state[1][1] - pos[1]
                        print("holding lc", lc, "mc:", mc, "rc:", rc)
                        print("released!")
                    else:
                        print("a_dir_keys:", a_dir_keys)
                        if kbd_la or kbd_a:
                            # left
                            xd = 1
                            yd = 0
                        elif kbd_ra or kbd_d:
                            # right
                            xd = -1
                            yd = 0
                        elif kbd_ua or kbd_w:
                            # up
                            xd = 1
                            yd = 2
                        elif kbd_da or kbd_s:
                            # down
                            xd = 1
                            yd = -2

                    mouse_state = None
                    valid_shift = False
                    print("xd:", xd, "yd:", yd)
                    if abs(xd) >= abs(yd):
                        if xd >= 0:
                            valid_shift = game.shift_grid("LEFT")
                            print("shifting LEFT VALID: {}".format(valid_shift))
                            change = True
                        else:
                            valid_shift = game.shift_grid("RIGHT")
                            print("shifting RIGHT VALID: {}".format(valid_shift))
                            change = True
                    else:
                        if yd >= 0:
                            valid_shift = game.shift_grid("UP")
                            print("shifting UP VALID: {}".format(valid_shift))
                            change = True
                        else:
                            valid_shift = game.shift_grid("DOWN")
                            print("shifting DOWN VALID: {}".format(valid_shift))
                            change = True
                if valid_shift and change:  # and DATA["current_game"].grid != old_grid:
                    new_tile = game.gen_random_tile()
                    print("new_tile:", new_tile)
        draw_display()
        if not loop:
            break
        loop = game.playable()


if __name__ == "__main__":
    init()
    menu_loop()
    if MODE_PLAY:
        main_loop()

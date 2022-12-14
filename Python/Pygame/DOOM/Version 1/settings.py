import math


# constants

NOT_ZERO_OFFSET = 0.0001
SMALL_COEFFICIENT = 1e-6


# game settings

RES = WIDTH, HEIGHT = 1600, 900  # screen resolution
HALF_WIDTH = WIDTH // 2
HALF_HEIGHT = HEIGHT // 2
FPS = 60  # frames per second

PLAYER_POS = 1.5, 5  # starting player position on mini-map
PLAYER_ANGLE = 0  # angle of direction
PLAYER_SPEED = 0.004  # speed of movement
PLAYER_ROT_SPEED = 0.002  # speed of rotation


# ray-casting

FOV = math.pi / 3  # field of view
HALF_FOV = FOV / 2
NUM_RAYS = WIDTH // 2
HALF_NUM_RAYS = NUM_RAYS // 2
DELTA_ANGLE = FOV / NUM_RAYS
MAX_DEPTH = 20

SCREEN_DIST = HALF_WIDTH / math.tan(HALF_FOV)
SCALE = WIDTH // NUM_RAYS


# drawing settings

DRAW_PLAYER_LINE_OF_SIGHT = False
DRAW_TWO_D_GAME = False
DRAW_TREE_D_GAME = not DRAW_TWO_D_GAME


# colours

COLOUR_RAYCAST_RAYS = "yellow"
COLOUR_MAP_WALLS = "darkgray"
COLOUR_PLAYER_LINE_OF_SIGHT = "orange"
COLOUR_PLAYER_CIRCLE = "green"
COLOUR_PSEUDO_THREE_D_WALLS = "white"
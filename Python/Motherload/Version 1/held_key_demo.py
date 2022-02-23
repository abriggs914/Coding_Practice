import pygame, math
from pygame.locals import *


# some simple functions for vetor math
# note that the next pygame release will ship with a vector math module included!

def magnitude(v):
    return math.sqrt(sum(v[i]*v[i] for i in range(len(v))))

def add(u, v):
    return [ u[i]+v[i] for i in range(len(u)) ]

def normalize(v):
    vmag = magnitude(v)
    return [ v[i]/vmag  for i in range(len(v)) ]

pygame.init()

screen = pygame.display.set_mode((1440,900))
screen_r = screen.get_rect()

pygame.display.update()

black=(0,0,0)
white=(255,255,255)

# background = pygame.image.load("G:/starfield.jpg")##loads the background
background = pygame.image.load(r"C:\Users\abrig\Documents\Coding_Practice\Java\R6SOperatorSelector\app\src\main\res\drawable\map_house_pic.jpg")

# here we define which button moves to which direction
move_map = {pygame.K_w: ( 0, -1),
            pygame.K_s: ( 0,  1),
            pygame.K_a: (-1,  0),
            pygame.K_d: ( 1,  0)}

# banshee = pygame.image.load("G:/banshee.png")
banshee = pygame.image.load(r"C:\Users\abrig\Documents\Coding_Practice\Python\Pygame\assets\playerShip1_orange.png")

# create a Rect from the Surface to store the position of the object
# we can pass the initial starting position by providing the kwargs top and left
# another useful feature is that when we create the Rect directly from the
# Surface, we also have its size stored in the Rect
banshee_r = banshee.get_rect(top=50, left=50)

speed = 5

gameexit = False

while not gameexit:

    # exit the game when the window closes
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameexit = True

    # if it touches the sides of the window, end the game
    # note how easy this part becomes if you use the Rect class
    if not screen_r.contains(banshee_r):
        gameexit = True

    # get all pressed keys
    pressed = pygame.key.get_pressed()

    # get all directions the ship should move
    move = [move_map[key] for key in move_map if pressed[key]]

    # add all directions together to get the final direction
    # reduced = reduce(add, move, (0, 0))
    reduced = (sum([f[0] for f in move]), sum([f[1] for f in move]))
    if reduced != (0, 0):

        # normalize the target direction and apply a speed
        # this ensures that the same speed is used when moving diagonally
        # and along the x or y axis. Also, this makes it easy to
        # change the speed later on.
        move_vector = [c * speed for c in normalize(reduced)]

        # move the banshee
        # Another useful pygame functions for Rects
        banshee_r.move_ip(*move_vector)

    screen.blit(background,(0,0))
    # we can use banshee_r directly for drawing
    screen.blit(banshee, banshee_r)
    pygame.display.update()
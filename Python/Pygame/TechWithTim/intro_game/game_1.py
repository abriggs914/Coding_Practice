import pygame
import math

pygame.init()

win_height = 480
win_width = 500

win = pygame.display.set_mode((win_width, win_height))
pygame.display.set_caption('First Game')
x = 50
y = 400
width = 64
height = 64
vel = 5
run = True

is_jump = False
jump_count = 10

left = False
right = False
walk_count = 0

walk_right = [pygame.image.load('R1.png'), pygame.image.load('R2.png'), pygame.image.load('R3.png'), pygame.image.load('R4.png'), pygame.image.load('R5.png'), pygame.image.load('R6.png'), pygame.image.load('R7.png'), pygame.image.load('R8.png'), pygame.image.load('R9.png')]
walk_left = [pygame.image.load('L1.png'), pygame.image.load('L2.png'), pygame.image.load('L3.png'), pygame.image.load('L4.png'), pygame.image.load('L5.png'), pygame.image.load('L6.png'), pygame.image.load('L7.png'), pygame.image.load('L8.png'), pygame.image.load('L9.png')]
bg = pygame.image.load('bg.jpg')
char = pygame.image.load('standing.png')

clock = pygame.time.Clock()

def jump_fun(jc):
    return (jc**2) * 0.5

def redraw_game_window():
    global walk_count
    win.blit(bg, (0, 0))
    
    if walk_count + 1 >= 27:
        walk_count = 0
    if left:
        win.blit(walk_left[walk_count // 3], (x, y))
        walk_count += 1
    elif right:
        win.blit(walk_right[walk_count // 3], (x, y))
        walk_count += 1
    else:
        win.blit(char, (x, y))
    # win.fill((0, 0, 0))
    #pygame.draw.rect(win, (255, 0, 0), (x, y, width, height))
    pygame.display.update()

# main game loop              
while run:
    # pygame.time.delay(80)
    clock.tick(27)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()
        
    if keys[pygame.K_LEFT] and x > vel:
        x -= vel
        left = True
        right = False
    elif keys[pygame.K_RIGHT] and x < (win_width - width - vel):
        x += vel
        left = False
        right = True
    else:
        left = False
        right = False
        walk_count = 0
    if not is_jump:
        #if keys[pygame.K_UP] and y > vel:
        #        y -= vel
        #if keys[pygame.K_DOWN] and y < (win_height - height - vel):
        #        y += vel
        top_margin = sum([math.floor(jump_fun(i)) for i in range(1, jump_count + 1)])
        if keys[pygame.K_SPACE] and top_margin < y < (win_height - height):
            is_jump = True
            right = False
            left = False
            walk_count = 0
    else:
        if jump_count >= -10 and y < (win_height - height):
            neg = 1
            if jump_count < 0:
                neg = -1
            y -= jump_fun(jump_count) * neg
            jump_count -= 1
        else:
            is_jump = False
            jump_count = 10
    redraw_game_window()
        
pygame.quit()

        

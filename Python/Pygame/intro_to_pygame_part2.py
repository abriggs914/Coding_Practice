import pygame
import math

pygame.init()

win_height = 500
win_width = 500

win = pygame.display.set_mode((win_height, win_width))
pygame.display.set_caption('First Game')
x = 50
y = 450
width = 40
height = 60
vel = 5
run = True

is_jump = False
jump_count = 10

def jump_fun(jc):
    return (jc**2) * 0.5
                        
while run:
        pygame.time.delay(80)
        
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                        run = False
                        
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_LEFT] and x > vel:
                x -= vel
        if keys[pygame.K_RIGHT] and x < (win_width - width - vel):
                x += vel
        if not is_jump:
                if keys[pygame.K_UP] and y > vel:
                        y -= vel
                if keys[pygame.K_DOWN] and y < (win_height - height - vel):
                        y += vel
                top_margin = sum([math.floor(jump_fun(i)) for i in range(1, jump_count + 1)])
                if keys[pygame.K_SPACE] and top_margin < y < (win_height - height):
                        is_jump = True
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

        win.fill((0, 0, 0))
        pygame.draw.rect(win, (255, 0, 0), (x, y, width, height))
        pygame.display.update()
        
pygame.quit()

        

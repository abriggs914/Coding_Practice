import pygame
import math

#tutorial 6
#https://www.youtube.com/watch?v=vc1pJ8XdZa0

pygame.init()

walk_right = [pygame.image.load('R1.png'), pygame.image.load('R2.png'), pygame.image.load('R3.png'), pygame.image.load('R4.png'), pygame.image.load('R5.png'), pygame.image.load('R6.png'), pygame.image.load('R7.png'), pygame.image.load('R8.png'), pygame.image.load('R9.png')]
walk_left = [pygame.image.load('L1.png'), pygame.image.load('L2.png'), pygame.image.load('L3.png'), pygame.image.load('L4.png'), pygame.image.load('L5.png'), pygame.image.load('L6.png'), pygame.image.load('L7.png'), pygame.image.load('L8.png'), pygame.image.load('L9.png')]
bg = pygame.image.load('bg.jpg')
char = pygame.image.load('standing.png')

class Player(object):

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 5
        self.is_jump = False
        self.jump_count = 10
        self.left = False
        self.right = False
        self.walk_count = 0
        self.standing = True

    def draw(self, win):
        if self.walk_count + 1 >= 27:
            self.walk_count = 0
        if not self.standing:
            if self.left:
                win.blit(walk_left[self.walk_count // 3], (self.x, self.y))
                self.walk_count += 1
            elif self.right:
                win.blit(walk_right[self.walk_count // 3], (self.x, self.y))
                self.walk_count += 1
        else:
            if self.right:
                win.blit(walk_right[0], (self.x, self.y))
            else:
                win.blit(walk_left[0], (self.x, self.y))
            #win.blit(char, (self.x, self.y))

class Projectile(object):

    def __init__(self, x, y, radius, color, facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.vel = 8 * facing

    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)

class Enemy(object):
    walk_right = [pygame.image.load('R1E.png'), pygame.image.load('R2E.png'), pygame.image.load('R3E.png'), pygame.image.load('R4E.png'), pygame.image.load('R5E.png'), pygame.image.load('R6E.png'), pygame.image.load('R7E.png'), pygame.image.load('R8E.png'), pygame.image.load('R9E.png'), pygame.image.load('R10E.png'), pygame.image.load('R11E.png')]
    walk_left = [pygame.image.load('L1E.png'), pygame.image.load('L2E.png'), pygame.image.load('L3E.png'), pygame.image.load('L4E.png'), pygame.image.load('L5E.png'), pygame.image.load('L6E.png'), pygame.image.load('L7E.png'), pygame.image.load('L8E.png'), pygame.image.load('L9E.png'), pygame.image.load('L10E.png'), pygame.image.load('L11E.png')]

    def __init__(self, x, y, width, height, end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.end = end
        self.path = [self.x, self.end]
        self.walk_count = 0
        self.vel = 3

    def draw(self, win):
        self.move()
        if self.walk_count + 1 >= 33:
            self.walk_count = 0

        if self.vel > 0: # moving right
            win.blit(self.walk_right[self.walk_count // 3], (self.x, self.y))
            self.walk_count += 1
        else:
            win.blit(self.walk_left[self.walk_count // 3], (self.x, self.y))
            self.walk_count += 1

    def move(self):
        if self.vel > 0: # moving right
            if self.x + self.vel < self.path[1]:
                self.x += self.vel
            else:
                self.vel *= -1
                self.walk_count = 0
        else: # moving left
            if self.x - self.vel > self.path[0]:
                self.x += self.vel # adding negative velocity
            else:
                self.vel *= -1
                self.walk_count = 0



def jump_fun(jc):
    return (jc**2) * 0.5

def redraw_game_window():
    win.blit(bg, (0, 0))
    man.draw(win)
    goblin.draw(win)
    for bullet in bullets:
        bullet.draw(win)
    pygame.display.update()

# main game loop
win_height = 480
win_width = 500
win = pygame.display.set_mode((win_width, win_height))
pygame.display.set_caption('First Game')
clock = pygame.time.Clock()
run = True
man = Player(300, 410, 64, 64)
goblin = Enemy(100, 410, 64, 64, 450)
bullets = []
MAX_BULLETS = 50

while run:
    # pygame.time.delay(80)
    clock.tick(27)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    for bullet in bullets:
        if 0 < bullet.x < win_width and 0 < bullet.y < win_height:
            bullet.x += bullet.vel
        else:
            bullets.pop(bullets.index(bullet))

    keys = pygame.key.get_pressed()

    if keys[pygame.K_SPACE]:
        if len(bullets) < MAX_BULLETS:
            x = round(man.x + (man.width // 2))
            y = round(man.y + (man.height // 2))
            radius = 6
            color = (0, 0, 0)
            facing = -1 if man.left else 1
            bullets.append(Projectile(x, y, radius, color, facing))
        
    if keys[pygame.K_LEFT] and man.x > man.vel:
        man.x -= man.vel
        man.left = True
        man.right = False
        man.standing = False
    elif keys[pygame.K_RIGHT] and man.x < (win_width - man.width - man.vel):
        man.x += man.vel
        man.left = False
        man.right = True
        man.standing = False
    else:
        # man.left = False
        # man.right = False
        man.standing = True
        man.walk_count = 0
        
    if not man.is_jump:
        # for moving up and down in a 3D plane
        #if keys[pygame.K_UP] and y > vel:
        #        y -= vel
        #if keys[pygame.K_DOWN] and y < (win_height - height - vel):
        #        y += vel
        top_margin = sum([math.floor(jump_fun(i)) for i in range(1, man.jump_count + 1)])
        if keys[pygame.K_UP] and top_margin < man.y < (win_height - man.height):
            man.is_jump = True
            #man.right = False
            #man.left = False
            man.walk_count = 0
    else:
        if man.jump_count >= -10 and man.y < (win_height - man.height):
            neg = 1
            if man.jump_count < 0:
                neg = -1
            man.y -= jump_fun(man.jump_count) * neg
            man.jump_count -= 1
        else:
            man.is_jump = False
            man.jump_count = 10
    redraw_game_window()
        
pygame.quit()

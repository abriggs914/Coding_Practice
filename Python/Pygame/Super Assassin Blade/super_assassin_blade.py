import pygame
import random
import math
from pygame.locals import *
import os
import sys

pygame.init()

W, H = 520, 260
win = pygame.display.set_mode((W,H))
pygame.display.set_caption('Super Assassin Blade')

bg = pygame.image.load(os.path.join('Images/Final_Images','background.png')).convert()
bgX = 0
bgX2 = bg.get_width()

clock = pygame.time.Clock()

class Player(object):

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.standing = True
        self.is_jump = False
        self.walk_count = 10
        self.jump_count = 10
        self.left = False
        self.right = False
        self.vel = 5
        self.hitbox = (self.x + 17, self.y + 11, 29, 52) # x,y,width,height
        self.walk_right = [pygame.image.load(os.path.join('Images/Final_Images','R1.png')), pygame.image.load(os.path.join('Images/Final_Images','R2.png')), pygame.image.load(os.path.join('Images/Final_Images','R3.png')), pygame.image.load(os.path.join('Images/Final_Images','R4.png')), pygame.image.load(os.path.join('Images/Final_Images','R5.png')), pygame.image.load(os.path.join('Images/Final_Images','R6.png')), pygame.image.load(os.path.join('Images/Final_Images','R7.png')), pygame.image.load(os.path.join('Images/Final_Images','R8.png')), pygame.image.load(os.path.join('Images/Final_Images','R9.png'))]
        self.walk_left = [pygame.image.load(os.path.join('Images/Final_Images','L1.png')), pygame.image.load(os.path.join('Images/Final_Images','L2.png')), pygame.image.load(os.path.join('Images/Final_Images','L3.png')), pygame.image.load(os.path.join('Images/Final_Images','L4.png')), pygame.image.load(os.path.join('Images/Final_Images','L5.png')), pygame.image.load(os.path.join('Images/Final_Images','L6.png')), pygame.image.load(os.path.join('Images/Final_Images','L7.png')), pygame.image.load(os.path.join('Images/Final_Images','L8.png')), pygame.image.load(os.path.join('Images/Final_Images','L9.png'))]
        self.draw()


    def draw(self):
        if self.walk_count + 1 >= 27:
            self.walk_count = 0
            
        if not self.standing:
            if self.left:
                win.blit(self.walk_left[self.walk_count // 3], (self.x, self.y))
                self.walk_count += 1
            elif self.right:
                win.blit(self.walk_right[self.walk_count // 3], (self.x, self.y))
                self.walk_count += 1
        else:
            if self.right:
                win.blit(self.walk_right[0], (self.x, self.y))
            else:
                win.blit(self.walk_left[0], (self.x, self.y))
            #win.blit(char, (self.x, self.y))
        self.hitbox = (self.x + 17, self.y + 11, 29, 52)
        pygame.draw.rect(win, (255, 0, 0), (self.hitbox[0], self.hitbox[1] - 20, 50, 10))
        pygame.draw.rect(win, (0, 128, 0), (self.hitbox[0], self.hitbox[1] - 20, 50, 10))
        pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)
        

class Game(object):
    
    def __init__(self, ground_level):
        self.ground_level = ground_level
        self.run = True
        self.players = []
        self.enemies = []
        self.projectiles = []
        if len(self.players) == 0:
            width = 64
            height = 64
            x_pos = abs(random.randint(0, W) - width) 
            new_player = Player(x_pos, ground_level, width, height)
            self.players.append(new_player)
            print('Player 1 entering the game: x:', new_player.x, ', y:', new_player.y)
            self.redraw_game_window()

    def redraw_game_window(self):
        win.blit(bg, (0, 0))
        #score_text = score_font.render('SCORE: ' + str(score), 1, (0, 0, 0))
        #win.blit(score_text, (370, 10))
        self.players[0].draw()
        #for goblin in goblins:
        #    goblin.draw(win)
        #for bullet in bullets:
        #    bullet.draw(win)
        pygame.display.update()

    def play(self):
        man = self.players[0]
        win_width = W
        win_height = H
        while self.run:
            # pygame.time.delay(80)
            # print('len goblins:', len(goblins), 'man.x:', man.x, 'man.y:', man.y)
            clock.tick(27)
            # print(time.time())

            # for goblin in goblins:
            #    if man.hitbox[1] < goblin.hitbox[1] + goblin.hitbox[3] and \
            #       man.hitbox[1] + man.hitbox[3] > goblin.hitbox[1]:
            #        if man.hitbox[0] + man.hitbox[2] > goblin.hitbox[0] and \
            #           man.hitbox[0] < goblin.hitbox[0] + goblin.hitbox[2]:
            #            hit_counter += 1
            #            score -= 25
            #            man.hit()
            #            player_died = True
            #            player_died_throughout = True
            #            player_deaths_count += 1

            #if shoot_loop > 0:
            #    shoot_loop += 1
            #if shoot_loop > 3:
            #    shoot_loop = 0

            #if player_died or (len(goblins) < MAX_GOBLINS and time_difficulty(DIFFICULTY, full_goblin_list_time_stamp)):
            #    ng_x = random.randint(0, win_width)
            #    ng_y = start_plane # random.randint(0.65*win_height, win_height - 32)
            #    ng_end = random.randint(10, 20) * 3
            #    while abs(ng_end - ng_x) < 10:
            #        ng_end = random.randint(10, 20) * 3
            #    print('\tSPAWNING # ', num_goblins + 1,'\nng_x:',ng_x,'ng_y:',ng_y,'ng_end:',ng_end)
            #    new_goblin = Enemy(num_goblins + 1, min(ng_x, ng_end), ng_y, 64, 64, max(ng_x, ng_end))
            #    num_goblins += 1
            #    goblins.append(new_goblin)
            #if len(goblins) == MAX_GOBLINS:
            #    full_goblin_list_time_stamp = time.time()

            #if (len(goblins) == 0 and not player_died) or player_deaths_count == MAX_PLAYER_DEATHS:
            #    if not player_died_throughout:
            #        print('You defeated all the enemies!\n\n\tYOU WIN\n')
            #    elif player_deaths_count == MAX_PLAYER_DEATHS:
            #        print('\n\n\tYOU DIED\n')
            #    else:
            #        print('You defeated all the enemies, after dying.\n\n\tYOU WIN (KINDA)\n')
            #    redraw_game_window()
                # pygame.time.delay(5000)
            #    break

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

            #for goblin in goblins:
            #    for bullet in bullets:
            #        if bullet.y - bullet.radius < goblin.hitbox[1] + goblin.hitbox[3] \
            #           and bullet.y + bullet.radius > goblin.hitbox[1]:
            #            if bullet.x + bullet.radius > goblin.hitbox[0] and bullet.x - bullet.radius < goblin.hitbox[0] + goblin.hitbox[2]:
            #                hit_counter += 1
            #                score += 1
            #                goblin.hit()
            #                hit_sound.play()
            #                bullets.pop(bullets.index(bullet))
            #        
            #if 0 < bullet.x < win_width and 0 < bullet.y < win_height:
            #    bullet.x += bullet.vel
            #else:
            #    print('miss!')
            #    bullets.pop(bullets.index(bullet))

            keys = pygame.key.get_pressed()

            #if keys[pygame.K_SPACE] and shoot_loop == 0:
                #bullet_sound.play()
                #if len(bullets) < MAX_BULLETS:
                #    x = round(man.x + (man.width // 2))
                #    y = round(man.y + (man.height // 2))
                #    radius = 6
                #    color = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
                #    facing = -1 if man.left else 1
                #    bullets.append(Projectile(x, y, radius, color, facing))
                #    shoot_loop = 1
                #    bullets_fired += 1
        
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
            #if player_died:
            #    if len(goblins) == MAX_GOBLINS:
            #        player_died = False
            #    print('flip')

            self.redraw_game_window()
            

def jump_fun(jc):
    return (jc**2) * 0.5

game = Game(150)
game.play()
pygame.quit()




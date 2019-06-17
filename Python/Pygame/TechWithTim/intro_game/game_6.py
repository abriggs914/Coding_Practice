import pygame
import math
import random
import time

#tutorial 9
#https://www.youtube.com/watch?v=2BikxsbkuIU

pygame.init()

walk_right = [pygame.image.load('R1.png'), pygame.image.load('R2.png'), pygame.image.load('R3.png'), pygame.image.load('R4.png'), pygame.image.load('R5.png'), pygame.image.load('R6.png'), pygame.image.load('R7.png'), pygame.image.load('R8.png'), pygame.image.load('R9.png')]
walk_left = [pygame.image.load('L1.png'), pygame.image.load('L2.png'), pygame.image.load('L3.png'), pygame.image.load('L4.png'), pygame.image.load('L5.png'), pygame.image.load('L6.png'), pygame.image.load('L7.png'), pygame.image.load('L8.png'), pygame.image.load('L9.png')]
bg = pygame.image.load('bg.jpg')
char = pygame.image.load('standing.png')

bullet_sound = pygame.mixer.Sound('bullet.wav')
hit_sound = pygame.mixer.Sound('hit.wav')

music = pygame.mixer.music.load('music.mp3')

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
        self.hitbox = (self.x + 17, self.y + 11, 29, 52) # x,y,width,height
        self.health = 10

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
        self.hitbox = (self.x + 17, self.y + 11, 29, 52)
        pygame.draw.rect(win, (255, 0, 0), (self.hitbox[0], self.hitbox[1] - 20, 50, 10))
        pygame.draw.rect(win, (0, 128, 0), (self.hitbox[0], self.hitbox[1] - 20, 50, 10))
        pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)

    def hit(self):
        self.x = win_width // 2
        self.y = win_height * 0.2
        self.walk_count = 0
        font1 = pygame.font.SysFont('comicsans', 100)
        text = font1.render('-25', 1, (255, 0, 0))
        mid_width = (win_width // 2) - (text.get_width() / 2)
        mid_height = (win_height // 2)
        win.blit(text, (mid_width, mid_height))
        pygame.display.update()
        i = 0
        print('\n\n\tYOU DIED\n')
        while i < 300:
            pygame.time.delay(10)
            i += 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    i = 301
                    pygame.quit()
        self.fall()

    def fall(self):
        s = 1
        goblins.clear()
        bullets.clear()
        self.is_jump = False
        self.jump_count = 10
        print('self.y',self.y,'win_height',win_height,'self.height',self.height,'win_height - self.height',win_height - self.height)
        while self.y + jump_fun(s) < start_plane:
            print('self.y',self.y)
            pygame.time.delay(100)
            # pygame.display.update()
            redraw_game_window()
            self.y += jump_fun(s)
            s += 1
            while self.y + jump_fun(s) > start_plane:
                s -= 1
                if s == 0:
                    self.y = start_plane - self.height
                    break
        
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

    def __init__(self, id, x, y, width, height, end):
        self.id = id
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.end = end
        self.end_count = 0
        self.path = [self.x, self.end]
        self.walk_count = 0
        self.vel = 3
        self.hitbox = (self.x + 17, self.y + 2, 31, 57) # x,y,width,height
        self.health = 10
        self.visible = True
        self.last_hit = None

    def draw(self, win):
        self.move()
        if self.visible:
            if self.walk_count + 1 >= 33:
                self.walk_count = 0

            if self.vel > 0: # moving right
                win.blit(self.walk_right[self.walk_count // 3], (self.x, self.y))
                self.walk_count += 1
            else:
                win.blit(self.walk_left[self.walk_count // 3], (self.x, self.y))
                self.walk_count += 1
            self.hitbox = (self.x + 17, self.y + 2, 31, 57)
            health_diff = ((50/10) * (10 - self.health))
            pygame.draw.rect(win, (255, 0, 0), (self.hitbox[0], self.hitbox[1] - 20, 50, 10)) # red
            pygame.draw.rect(win, (0, 128, 0), (self.hitbox[0], self.hitbox[1] - 20, 50 - health_diff, 10)) # green
        else:
            self.x = -5
            self.y = -5
            self.hitbox = (-5, -5, -5, -5)
        label_font = pygame.font.SysFont('comicsans', 15, True) # font, size, bold, italicized
        text = label_font.render('goblin # ' + str(self.id), 1, (255, 0, 0))
        width = self.x# + (text.get_width() / 2)
        height = self.y - 30# - (self.height)
        win.blit(text, (width, height))        
        pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)
        pygame.display.update()

    def move(self):
        if self.last_hit:
            c_time = time.time()
            x = math.floor(c_time) - math.floor(self.last_hit)
            if x > REGEN_TIME and x >= self.health:
                if self.health < 10:
                    self.health += 1
                
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
        #if self.x <= self.path[1] - self.width:
        #    self.end_count += 1
        #    print('self.end_count:',self.end_count)
        #    print('goblin #',self.id,'self.path:',self.path)
        #    if self.end_count >= 3:
        #        self.change_enemy_path_end()
        #        self.end_count = 0

    def hit(self):
        self.last_hit = time.time()
        if self.health > 0:
            self.health -= 1
            print('goblin #', self.id, 'health: [' + str(self.health) + ' / 10]' ,', hit # [' + str(hit_counter) + ' / ' + str(bullets_fired) + ']')
            if self.health == 0:
                self.visible = False
                print('You killed goblin #', self.id)
                goblins.pop(goblins.index(self))
        else:
            self.visible = False

    def change_enemy_path_end(self):
        ng_x = self.path[0]
        ng_end = random.randint(20, 100) * 3
        while ng_x < ng_end < win_width - self.width and ng_end - ng_x < 10:
            ng_end = random.randint(10, 20) * 3
        p = [ng_x, ng_end]
        self.path = p
        
        

def jump_fun(jc):
    return (jc**2) * 0.5

def redraw_game_window():
    win.blit(bg, (0, 0))
    score_text = score_font.render('SCORE: ' + str(score), 1, (0, 0, 0))
    win.blit(score_text, (370, 10))
    man.draw(win)
    for goblin in goblins:
        goblin.draw(win)
    for bullet in bullets:
        bullet.draw(win)
    pygame.display.update()

def time_difficulty(setting, time_stamp):
    c_time = time.time()
    setting = 1 if setting < 1 else setting
    setting = 3 if setting > 3 else setting
    if math.floor(c_time) - math.floor(time_stamp) >= 3 * (4 - setting):
        return True
    return False
        

# --------------------------------------------------------------------------------------

win_height = 480
win_width = 500
start_plane = 410
win = pygame.display.set_mode((win_width, win_height))
pygame.display.set_caption('First Game')
clock = pygame.time.Clock()
run = True
man = Player(300, start_plane, 64, 64)
# goblin = Enemy(1, 100, start_plane, 64, 64, 450)
bullets_fired = 0
bullets = []
MAX_BULLETS = 5
shoot_loop = 0
hit_counter = 0

score = 0
score_font = pygame.font.SysFont('comicsans', 30, True) # font, size, bold, italicized
# score_font = pygame.font.SysFont('comicsans', 30, True, True)

goblins = []
num_goblins = 0
MAX_GOBLINS = 3
full_goblin_list_time_stamp = 0
DIFFICULTY = 1
REGEN_TIME = 3

pygame.mixer.music.play(-1)
player_died = False
player_died_throughout = False
MAX_PLAYER_DEATHS = 3
player_deaths_count = 0

while run:
    # pygame.time.delay(80)
    # print('len goblins:', len(goblins), 'man.x:', man.x, 'man.y:', man.y)
    clock.tick(27)
    # print(time.time())

    for goblin in goblins:
        if man.hitbox[1] < goblin.hitbox[1] + goblin.hitbox[3] and \
           man.hitbox[1] + man.hitbox[3] > goblin.hitbox[1]:
            if man.hitbox[0] + man.hitbox[2] > goblin.hitbox[0] and \
               man.hitbox[0] < goblin.hitbox[0] + goblin.hitbox[2]:
                hit_counter += 1
                score -= 25
                player_deaths_count += 1
                player_died = True
                player_died_throughout = True
                if player_deaths_count == MAX_PLAYER_DEATHS:
                    break
                man.hit()
    

    if shoot_loop > 0:
        shoot_loop += 1
    if shoot_loop > 3:
        shoot_loop = 0

    if player_died or (len(goblins) < MAX_GOBLINS and time_difficulty(DIFFICULTY, full_goblin_list_time_stamp)):
        ng_x = random.randint(0, win_width)
        ng_y = start_plane # random.randint(0.65*win_height, win_height - 32)
        ng_end = random.randint(10, 20) * 3
        while abs(ng_end - ng_x) < 10:
            ng_end = random.randint(10, 20) * 3
        print('\tSPAWNING # ', num_goblins + 1,'\nng_x:',ng_x,'ng_y:',ng_y,'ng_end:',ng_end)
        new_goblin = Enemy(num_goblins + 1, min(ng_x, ng_end), ng_y, 64, 64, max(ng_x, ng_end))
        num_goblins += 1
        goblins.append(new_goblin)
    if len(goblins) == MAX_GOBLINS:
        full_goblin_list_time_stamp = time.time()

    if (len(goblins) == 0 and not player_died) or player_deaths_count == MAX_PLAYER_DEATHS:
        if not player_died_throughout:
            print('You defeated all the enemies!\n\n\tYOU WIN\n')
        elif player_deaths_count == MAX_PLAYER_DEATHS:
            print('\n\n\tGAME OVER\n')
        else:
            print('You defeated all the enemies, after dying.\n\n\tYOU WIN (KINDA)\n')
        redraw_game_window()
        pygame.time.delay(5000)
        break

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    for goblin in goblins:
        for bullet in bullets:
            if bullet.y - bullet.radius < goblin.hitbox[1] + goblin.hitbox[3] \
               and bullet.y + bullet.radius > goblin.hitbox[1]:
                if bullet.x + bullet.radius > goblin.hitbox[0] and bullet.x - bullet.radius < goblin.hitbox[0] + goblin.hitbox[2]:
                    hit_counter += 1
                    score += 1
                    goblin.hit()
                    hit_sound.play()
                    bullets.pop(bullets.index(bullet))
                    
            if 0 < bullet.x < win_width and 0 < bullet.y < win_height:
                bullet.x += bullet.vel
            else:
                print('miss!')
                bullets.pop(bullets.index(bullet))
    keys = pygame.key.get_pressed()

    if keys[pygame.K_SPACE] and shoot_loop == 0:
        bullet_sound.play()
        if len(bullets) < MAX_BULLETS:
            x = round(man.x + (man.width // 2))
            y = round(man.y + (man.height // 2))
            radius = 6
            color = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
            facing = -1 if man.left else 1
            bullets.append(Projectile(x, y, radius, color, facing))
            shoot_loop = 1
            bullets_fired += 1
        
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
    if player_died:
        if len(goblins) == MAX_GOBLINS:
            player_died = False

    redraw_game_window()
        
pygame.quit()

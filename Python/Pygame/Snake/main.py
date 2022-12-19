import random

import pygame

from utility import clamp

W, H = 10, 20  # in tiles
TILE = 45  # in pixels
GAME_RES = W * TILE, H * TILE
RES = 750, 940
FPS = 4
score = 0
allow_wrap = True


pygame.init()
sc = pygame.display.set_mode(RES)
game_sc = pygame.Surface(GAME_RES)
clock = pygame.time.Clock()

grid = [[pygame.Rect(x * TILE, y * TILE, TILE, TILE) for x in range(W)] for y in range(H)]
field = [[0 for i in range(W)] for j in range(H)]
print(f"{grid=}\n{field=}")

bg = pygame.image.load("img/bg.jpg")
game_bg = pygame.image.load("img/bg2.jpg")

main_font = pygame.font.Font("font/font.ttf", 65)
font = pygame.font.Font("font/font.ttf", 45)

title_tetris = main_font.render("SNAKE", True, pygame.Color("darkorange"))
title_score = font.render("score:", True, pygame.Color("green"))
title_record = font.render("record:", True, pygame.Color("purple"))


def available(x, y):
    return not field[y][x]


def random_cell(tries=0):
    if tries >= W * W:
        return -1, -1
    x, y = random.randrange(0, W), random.randrange(0, H)
    print(f"{x=}, {y=}")
    return (x, y) if available(x, y) else random_cell(tries + 1)


def get_record():
    try:
        with open("record") as f:
            return f.readline()
    except FileNotFoundError:
        with open("record", "w") as f:
            f.write("0")


def set_record(record, score):
    rec = max(int(record), score)
    with open("record", "w") as f:
        f.write(str(rec))


def gen_food():
    x, y = random_cell()
    if x < 0 or y < 0:
        raise Exception("You win, no more place to spawn food")
    return x, y


def get_colour():
    return (random.randrange(30, 256), random.randrange(30, 256), random.randrange(30, 256))



snake_head_colour = "red"
snake_head = random_cell()
snake_list = [(snake_head, snake_head_colour)]
snake_length = 1
food_pos = gen_food()
field[snake_head[1]][snake_head[0]] = 1
field[food_pos[1]][food_pos[0]] = 2
last_dx, last_dy = 0, 0


if __name__ == '__main__':

    while True:
        dx, dy = 0, 0
        record = get_record()
        sc.blit(bg, (0, 0))
        sc.blit(game_sc, (20, 20))
        game_sc.blit(game_bg, (0, 0))
        # control
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    dx = -1
                if event.key == pygame.K_RIGHT:
                    dx = 1
                if event.key == pygame.K_DOWN:
                    dy = 1
                if event.key == pygame.K_UP:
                    dy = -1

        if dx == 0 and dy == 0:
            dx, dy = last_dx, last_dy
        last_dx, last_dy = dx, dy

        # move snake
        if allow_wrap:
            snake_head = (snake_head[0] + dx) % W, (snake_head[1] + dy) % H
        else:
            snake_head = clamp(0, snake_head[0] + dx, W - 1), clamp(0, snake_head[1] + dy, H - 1)
        print(f"{dx=}, {dy=}, {snake_head=}, {food_pos=}, {snake_length=}, {FPS=}")

        # draw food
        if food_pos[0] >= 0 and food_pos[1] >= 0:
            pygame.draw.rect(game_sc, "yellow", grid[food_pos[1]][food_pos[0]])

        # draw snake
        pygame.draw.rect(game_sc, snake_head_colour, grid[snake_head[1]][snake_head[0]])
        for y, row in enumerate(field):
            for x, cell in enumerate(row):
                if isinstance(cell, tuple):
                    cx, cy, dx, dy = cell

                    if allow_wrap:
                        ccx, ccy = (cx + dx) % W, (cy + dy) % H
                    else:
                        ccx, ccy = clamp(0, cx + dx, W - 1), clamp(0, cy + dy, H - 1)

                    pygame.draw.rect(game_sc, get_colour(), grid[ccy][ccx])
                    field[y][x] = ccx, ccy, dx, dy

        if snake_head == food_pos:
            snake_length += 1
            FPS += 1
            field[food_pos[1]][food_pos[0]] = *food_pos, dx, dy
            food_pos = gen_food()
            field[food_pos[1]][food_pos[0]] = 3

        # # move x
        # figure_old = deepcopy(figure)
        # for i in range(4):
        #     figure[i].x += dx
        #     if not check_borders():
        #         figure = deepcopy(figure_old)
        #         break
        # # move y
        # anim_count += anim_speed
        # if anim_count > anim_limit:
        #     anim_count = 0
        #     figure_old = deepcopy(figure)
        #     for i in range(4):
        #         figure[i].y += 1
        #         if not check_borders():
        #             for i in range(4):
        #                 field[figure_old[i].y][figure_old[i].x] = colour
        #             figure, colour = next_figure, next_colour
        #             next_figure, next_colour = deepcopy(choice(figures)), get_colour()
        #             anim_limit = 2000
        #             break
        # # rotate
        # center = figure[0]
        # figure_old = deepcopy(figure)
        # if rotate:
        #     for i in range(4):
        #         x = figure[i].y - center.y
        #         y = figure[i].x - center.x
        #         figure[i].x = center.x - x
        #         figure[i].y = center.y + y
        #         if not check_borders():
        #             figure = deepcopy(figure_old)
        #             break
        # # check lines
        # line, lines = H - 1, 0
        # for row in range(H - 1, -1, -1):
        #     count = 0
        #     for i in range(W):
        #         if field[row][i]:
        #             count += 1
        #         field[line][i] = field[row][i]
        #     if count < W:
        #         line -= 1
        #     else:
        #         anim_speed += 3
        #         lines += 1
        # #compute score
        # score += scores[lines]
        # draw grid
        for row in grid:
            for i_rect in row:
                pygame.draw.rect(game_sc, (40, 40, 40), i_rect, 1)
        # [pygame.draw.rect(game_sc, (40, 40, 40), i_rect, 1) for i_rect in grid]
        # # draw figure
        # for i in range(4):
        #     figure_rect.x = figure[i].x * TILE
        #     figure_rect.y = figure[i].y * TILE
        #     pygame.draw.rect(game_sc, colour, figure_rect)
        # # draw field
        # for y, raw in enumerate(field):
        #     for x, col in enumerate(raw):
        #         if col:
        #             figure_rect.x, figure_rect.y = x * TILE, y * TILE
        #             pygame.draw.rect(game_sc, col, figure_rect)
        # # draw next figure
        # for i in range(4):
        #     figure_rect.x = next_figure[i].x * TILE + 380
        #     figure_rect.y = next_figure[i].y * TILE + 185
        #     pygame.draw.rect(sc, next_colour, figure_rect)
        # draw titles
        sc.blit(title_tetris, (485, -10))
        sc.blit(title_score, (535, 780))
        sc.blit(font.render(str(score), True, pygame.Color("white")), (550, 840))
        sc.blit(title_record, (525, 650))
        sc.blit(font.render(str(record), True, pygame.Color("gold")), (550, 710))

        # game over
        for i in range(W):
            if field[0][i]:
                set_record(record, score)
                field = [[0 for j in range(W)] for i in range(H)]
                anim_count, anim_speed, anim_limit = 0, 60, 2000
                score = 0
                for row in grid:
                    for i_rect in row:
                        pygame.draw.rect(game_sc, get_colour(), i_rect)
                        sc.blit(game_sc, (20, 20))
                        pygame.display.flip()
                        clock.tick(200)

        pygame.display.flip()
        clock.tick(FPS)





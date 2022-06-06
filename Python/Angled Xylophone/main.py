import math

import pygame
from colour_utility import *

from ball import Ball
from utility import Rect2, rotate_point, Line

if __name__ == '__main__':
    print('PyCharm')

    pygame.init()
    WIDTH, HEIGHT = 750, 550
    WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
    CLOCK = pygame.time.Clock()
    FPS = 60

    FONT_DEFAULT = pygame.font.Font(None, 36)

    running = True

    # VARS
    cx, cy = WIDTH * 0.5, HEIGHT * 0.95
    hy = HEIGHT * (2/5)
    boundary_width = 5
    ball_radius = 10
    line_width = 2
    n_balls = 20
    rect = pygame.Rect(cx, cy, (0.5 * WIDTH), (0.5 * WIDTH))
    points = [
        [
            list(rotate_point(cx, cy, rect.right, rect.top, 225)),
            [rect.left, rect.top]
        ],
        [
            list(rotate_point(cx, cy, rect.right, rect.top, 315)),
            [rect.left, rect.top]
        ]
    ]
    lines = [
        line_1 := Line(*points[0][0], *points[0][1]),
        line_2 := Line(*points[1][0], *points[1][1])
    ]
    x_range = range(int(points[0][0][0]), int(points[1][0][0]))
    y_range = range(int(line_1.y1), int(line_1.y2))
    d_y = y_range.stop - y_range.start
    balls = [
        # ball_01 := Ball(1, pygame.Rect(16, 20, 25, 25), ORANGE, 12, 15)
    ]
    paths = []
    print(x_range)
    print(y_range)
    max_slices = 10
    x_step = int((x_range.stop - x_range.start) / max_slices)
    all_x_slices = [x for x in range(x_range.start, x_range.stop + x_step, x_step)]
    print(f"all_x_slices: {all_x_slices}")
    enum_values = list(enumerate(range(y_range.start, y_range.stop, int(ball_radius))))
    for i, y_d in enum_values:
        x1_d = line_1.x_at_y(y_d)
        x2_d = line_2.x_at_y(y_d)
        x_b = x1_d - (ball_radius / 2)
        y_b = y_d - (ball_radius / 2)
        balls.append(
            # Ball(i + 1, pygame.Rect(x_b, y_b, ball_radius, ball_radius),
            #      random_colour(), ball_radius, 5))
            Ball(i + 1, pygame.Rect(x_b, y_b, ball_radius, i + 1),
                 random_colour(), ball_radius, 5))
        p_a = (y_b + (hy - (i * ball_radius))) / ((x1_d - cx)**2)
        print(f"\t a: {p_a}")
        # paths.append(lambda x: (p_a*((x - cx)**2)) + hy)
        # x_slices = []
        print(f"x1_d: {x1_d}, x2_d: {x2_d}")
        print(f"SPEED: {len(enum_values) - (i + 1)}")
        x_slices = [x for x in all_x_slices if x1_d <= x <= x2_d]
        # for j, xs in x_slices:
        # balls[i].points = [(j, balls[i].rect.center[1]) for j in range(int(x1_d), math.ceil(x2_d), n_balls - (i + 0))]
        balls[i].points = [(j, balls[i].rect.center[1]) for j in range(int(x1_d), math.ceil(x2_d), 12)]
        balls[i].frame = 0
        paths.append(x_slices)
        if len(balls) >= n_balls:
            break
    # print(ball_01)

    print(f"paths: {paths}")
    print(f"len(paths): {len(paths)} == {len(balls)} len(balls)")
    print(f"len(paths): {len(paths[0])}")
    # print(f"paths(1): {[p(cx) for p in paths]}")

    while running:

        # reset window
        WINDOW.fill(WHITE)

        # begin drawing
        pygame.draw.line(WINDOW, GRAY_17, points[0][0], points[0][1], boundary_width)
        pygame.draw.line(WINDOW, GRAY_17, points[1][0], points[1][1], boundary_width)

        for i, ball in enumerate(balls):
            if i < len(balls) - 1:
                pygame.draw.line(WINDOW, BLACK, ball.rect.center, balls[i + 1].rect.center, line_width)
            pygame.draw.circle(WINDOW, ball.colour, ball.rect.center, ball.radius)
            ball.next_frame()
            # ball.rect = pygame.Rect(paths[i][slice_n], ball.rect.center[1], ball.rect.width, ball.rect.height)

        # handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break

        CLOCK.tick(FPS)

        # update the display
        # draw everything
        # pygame.display.flip()
        # draw everything, or pass a surface or shape to update only that portion.
        pygame.display.update()

    pygame.quit()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

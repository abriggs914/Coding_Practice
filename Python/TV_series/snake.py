from colour_utility import Colour
from utility import grid_cells, clamp
import pygame

#	General main loop structure for pygame.
#	Includes 2D motion + acceleration controls.
#	Version............1.0
#	Date........2022-03-29
#	Author....Avery Briggs



def draw_grid():
    for i in range(n_rows):
        for j in range(n_cols):
            r_data = gc_cells[i][j]
            x_1 = r_data["x_1"]
            y_1 = r_data["y_1"]
            w = r_data["w"]
            h = r_data["h"]
            rect = pygame.Rect(x_1, y_1, w, h)
            pygame.draw.rect(WINDOW, bg_grid_cell.rgb_code, rect)


def draw_snake():
    for i, idx in enumerate(snake):
        i_, j_ = idx
        r_data = gc_cells[i_][j_]
        x_1 = r_data["x_1"]
        y_1 = r_data["y_1"]
        w = r_data["w"]
        h = r_data["h"]
        rect = pygame.Rect(x_1, y_1, w, h)
        pygame.draw.rect(WINDOW, colour_snake.rgb_code, rect)


def move_snake():
    global snake
    new_snake = []
    for i, idx in enumerate(snake):
        i_, j_ = idx
        if allow_snake_wrap:
            n_i = i_ + snake_direction[1]
            n_j = j_ + snake_direction[0]
            n_i %= n_rows
            n_j %= n_cols
        else:
            n_i = clamp(0, i_ + snake_direction[1], n_rows - 1)
            n_j = clamp(0, j_ + snake_direction[0], n_cols - 1)
        new_snake.append((n_i, n_j))
        # r_data = gc_cells[n_i][n_j]
        # x_1 = r_data["x_1"]
        # y_1 = r_data["y_1"]
        # w = r_data["w"]
        # h = r_data["h"]
        # rect = pygame.Rect(x_1, y_1, w, h)
    snake = new_snake


if __name__ == "__main__":
    pygame.init()
    WIDTH, HEIGHT = 750, 550
    P_WIDTH, P_HEIGHT = 0.8, 0.8
    MARGIN_X_GRID = WIDTH - (WIDTH * P_WIDTH)
    MARGIN_Y_GRID = HEIGHT - (HEIGHT * P_HEIGHT)
    G_WIDTH, G_HEIGHT = WIDTH * P_WIDTH, HEIGHT * P_HEIGHT
    X_GRID, Y_GRID = 5, 5
    WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
    CLOCK = pygame.time.Clock()
    FPS_START = 5
    FPS = 60

    FONT_DEFAULT = pygame.font.Font(None, 36)

    running = True
    time_passed = 0
    ticks_passed = 0

    n_rows = 10
    n_cols = 10
    allow_snake_wrap = False
    snake = [(n_rows//2, n_cols//2)]
    snake_direction = 1, 0

    gc_cells = grid_cells(
        G_WIDTH,
        n_cols,
        G_HEIGHT,
        n_rows,
        x_pad=1,
        y_pad=1,
        x_0=X_GRID,
        y_0=Y_GRID,
        r_type=dict
    )

    x, y = WIDTH / 2, HEIGHT / 2
    max_speed = 15
    x_change = 0
    y_change = 0
    x_accel_r = 0.2
    y_accel_r = 0.2
    x_decel_r = 0.92
    y_decel_r = 0.92
    x_accel = 0
    y_accel = 0
    m_width, m_height = 20, 40
    mallow_rect = pygame.Rect(0, 0, m_width, m_height)
    mallow_rect.center = x, y

    black = Colour("black")
    colour_mallow = Colour((0, 120, 250))
    bg_grid_cell = Colour((160, 160, 160))
    colour_snake = Colour((10, 210, 40))

    while running:
        CLOCK.tick(FPS_START)
        time_passed += CLOCK.get_time()
        ticks_passed += 1

        # reset window
        WINDOW.fill(black.rgb_code)

        # # begin drawing
        # text_surface = FONT_DEFAULT.render("Demo Text", True, GREEN_4, GRAY_27)
        # text_rect = text_surface.get_rect()
        # text_rect.center = WINDOW.get_rect().center
        # WINDOW.blit(text_surface, text_rect)

        draw_grid()
        draw_snake()
        print(f"{ticks_passed=}, {time_passed} milliseconds")
        if ticks_passed % 2 == 0:
            move_snake()

        # handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            elif event.type == pygame.KEYDOWN:
                # Set the acceleration value.
                if event.key == pygame.K_LEFT:
                    x_accel = -x_accel_r
                    snake_direction = (-1, 0)
                if event.key == pygame.K_RIGHT:
                    x_accel = x_accel_r
                    snake_direction = (1, 0)
                if event.key == pygame.K_UP:
                    y_accel = -y_accel_r
                    snake_direction = (0, -1)
                if event.key == pygame.K_DOWN:
                    y_accel = y_accel_r
                    snake_direction = (0, 1)
            elif event.type == pygame.KEYUP:
                if event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                    x_accel = 0
                if event.key in (pygame.K_UP, pygame.K_DOWN):
                    y_accel = 0

        x_change += x_accel  # Accelerate.
        y_change += y_accel  # Accelerate.
        if abs(x_change) >= max_speed:  # If max_speed is exceeded.
            # Normalize the x_change and multiply it with the max_speed.
            x_change = x_change / abs(x_change) * max_speed
        if abs(y_change) >= max_speed:  # If max_speed is exceeded.
            # Normalize the x_change and multiply it with the max_speed.
            y_change = y_change / abs(y_change) * max_speed

        # Decelerate if no key is pressed.
        if x_accel == 0:
            x_change *= x_decel_r
        if y_accel == 0:
            y_change *= y_decel_r

        # x += x_change  # Move the object.
        win_rect = WINDOW.get_rect()
        x = clamp(win_rect.left + (m_width / 2), x + x_change, win_rect.right - (m_width / 2))  # Move the object.
        y = clamp(win_rect.top + (m_height / 2), y + y_change, win_rect.bottom - (m_height / 2))  # Move the object.

        mallow_rect.center = x, y
        pygame.draw.rect(WINDOW, colour_mallow.rgb_code, mallow_rect)

        # update the display
        # draw everything
        # pygame.display.flip()
        # draw everything, or pass a surface or shape to update only that portion.
        pygame.display.update()

    pygame.quit()

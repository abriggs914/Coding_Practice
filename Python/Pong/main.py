from colour_utility import *
import pygame

WIDTH, HEIGHT = 750, 550
FPS = 60
total_game_width, total_game_height = 0.8 * WIDTH, 0.8 * HEIGHT


radius = 6
lb_y_move, rb_y_move = 25, 25
lb_width, lb_height = 20, 100
lb_x_r_acc, lb_y_r_acc = 0.2, 0.2
lb_x_r_dacc, lb_y_r_dacc = 0.92, 0.92
rb_width, rb_height = 20, 100
rb_x_r_acc, rb_y_r_acc = 0.2, 0.2
rb_x_r_dacc, rb_y_r_dacc = 0.92, 0.92


def calc_center_point():
    return total_game_width / 2, total_game_height / 2


center_xy = calc_center_point()


data_ball = {
    "x": center_xy[0],
    "y": center_xy[1],
    "radius": radius,
    "x_vel": 0,
    "y_vel": 0,
    "x_acc": 0,
    "y_acc": 0,
    "max_x_vel": 25,
    "max_y_vel": 25,
    "max_x_acc": 0,
    "max_y_acc": 0,
    "x_rate_acc": 0.2,
    "y_rate_acc": 0.2,
    "x_rate_dacc": 0.92,
    "y_rate_dacc": 0.92,
    "x_change": 0,
    "y_change": 0,
    "fill": rgb_to_hex(WILDERNESS_MINT),
    "outline": rgb_to_hex(GRAY_17),
    "activefill": brighten(WILDERNESS_MINT, 0.25, False),
    "activeoutline": brighten(GRAY_17, 0.25, False),
    "disabledfill": darken(WILDERNESS_MINT, 0.25, False),
    "disabledoutline": darken(GRAY_17, 0.25, False)
}


data_left_bumper = {
    "x": total_game_width * 0.1,
    "y": center_xy[1],
    "w": lb_width,
    "h": lb_height,
    "x_vel": 0,
    "y_vel": 0,
    "x_acc": 0,
    "y_acc": 0,
    "max_x_vel": 15,
    "max_y_vel": 15,
    "max_x_acc": 0,
    "max_y_acc": 0,
    "x_rate_acc": 0.2,
    "y_rate_acc": 0.2,
    "x_rate_dacc": 0.92,
    "y_rate_dacc": 0.92,
    "x_change": 0,
    "y_change": 0,
    "fill": rgb_to_hex(FIREBRICK_3),
    "outline": rgb_to_hex(GRAY_25),
    "activefill": brighten(FIREBRICK_3, 0.25, False),
    "activeoutline": brighten(GRAY_25, 0.25, False),
    "disabledfill": darken(FIREBRICK_3, 0.25, False),
    "disabledoutline": darken(GRAY_25, 0.25, False)
}


data_right_bumper = {
    "x": total_game_width * 0.9,
    "y": center_xy[1],
    "w": rb_width,
    "h": rb_height,
    "x_vel": 0,
    "y_vel": 0,
    "x_acc": 0,
    "y_acc": 0,
    "max_x_vel": 15,
    "max_y_vel": 15,
    "max_x_acc": 0,
    "max_y_acc": 0,
    "x_rate_acc": 0.2,
    "y_rate_acc": 0.2,
    "x_rate_dacc": 0.92,
    "y_rate_dacc": 0.92,
    "x_change": 0,
    "y_change": 0,
    "fill": rgb_to_hex(FIREBRICK_3),
    "outline": rgb_to_hex(GRAY_25),
    "activefill": brighten(FIREBRICK_3, 0.25, False),
    "activeoutline": brighten(GRAY_25, 0.25, False),
    "disabledfill": darken(FIREBRICK_3, 0.25, False),
    "disabledoutline": darken(GRAY_25, 0.25, False)
}


if __name__ == "__main__":
    pygame.init()
    WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
    CLOCK = pygame.time.Clock()

    FONT_DEFAULT = pygame.font.Font(None, 36)

    running = True

    while running:

        # reset window
        WINDOW.fill(BLACK)

        # begin drawing
        text_surface = FONT_DEFAULT.render("Demo Text", True, GREEN_4, GRAY_27)
        text_rect = text_surface.get_rect()
        text_rect.center = WINDOW.get_rect().center
        WINDOW.blit(text_surface, text_rect)

        # handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            elif event.type == pygame.KEYDOWN:
                # Set the acceleration value.
                if event.key == pygame.K_w:
                    # x_acceleration = -x_acceleration_rate
                    data_left_bumper["y_acc"] = -data_left_bumper["y_rate_acc"]
                if event.key == pygame.K_s:
                    # x_acceleration = x_acceleration_rate
                    data_left_bumper["y_acc"] = data_left_bumper["y_rate_acc"]
                if event.key == pygame.K_UP:
                    # y_acceleration = -y_acceleration_rate
                    data_right_bumper["y_acc"] = -data_right_bumper["y_rate_acc"]
                if event.key == pygame.K_DOWN:
                    # y_acceleration = y_acceleration_rate
                    data_right_bumper["y_acc"] = data_right_bumper["y_rate_acc"]
            elif event.type == pygame.KEYUP:
                if event.key in (pygame.K_w, pygame.K_s):
                    # x_acceleration = 0
                    data_left_bumper["y_acc"] = 0
                if event.key in (pygame.K_UP, pygame.K_DOWN):
                    # y_acceleration = 0
                    data_right_bumper["y_acc"] = 0

        data_left_bumper["y_change"] += data_left_bumper["y_acc"]
        data_right_bumper["y_change"] += data_right_bumper["y_acc"]
        if abs(data_left_bumper["y_change"]) >= data_left_bumper["max_y_vel"]:
            data_left_bumper["y_change"] = data_left_bumper["y_change"] / abs(data_left_bumper["y_change"]) * data_left_bumper["max_y_vel"]
        if abs(data_right_bumper["y_change"]) >= data_right_bumper["max_y_vel"]:
            data_right_bumper["y_change"] = data_right_bumper["y_change"] / abs(data_right_bumper["y_change"]) * data_right_bumper["max_y_vel"]

        if data_left_bumper["y_acc"] == 0:
            data_left_bumper["y_change"] *= data_left_bumper["y_rate_dacc"]
        if data_right_bumper["y_acc"] == 0:
            data_right_bumper["y_change"] *= data_right_bumper["y_rate_dacc"]

        CLOCK.tick(FPS)

        # update the display
        # draw everything
        win_rect = WINDOW.get_rect()
        y_left = clamp(win_rect.top + (data_left_bumper["h"] / 2), data_left_bumper["y"] + data_left_bumper["y_change"], win_rect.top - (data_left_bumper["h"] / 2))
        y_right = clamp(win_rect.top + (data_right_bumper["h"] / 2), data_right_bumper["y"] + data_right_bumper["y_change"], win_rect.top - (data_right_bumper["h"] / 2))
        data_left_bumper["y"] = y_left
        data_right_bumper["y"] = y_right
        pygame.draw.rect(
            WINDOW,
            data_left_bumper["fill"],
            (
                data_left_bumper["x"],
                data_left_bumper["y"],
                data_left_bumper["w"],
                data_left_bumper["h"]
            )
        )
        pygame.draw.rect(
            WINDOW,
            data_right_bumper["fill"],
            (
                data_right_bumper["x"],
                data_right_bumper["y"],
                data_right_bumper["w"],
                data_right_bumper["h"]
            )
        )

        # pygame.display.flip()
        # draw everything, or pass a surface or shape to update only that portion.
        pygame.display.update()

    pygame.quit()


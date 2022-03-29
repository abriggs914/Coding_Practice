from colour_utility import *
from utility import *
import pygame

#	General main loop structure for pygame.
#	Includes 2D motion + acceleration controls.
#	Version............1.0
#	Date........2022-03-29
#	Author....Avery Briggs


if __name__ == "__main__":
    pygame.init()
    WIDTH, HEIGHT = 750, 550
    WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
    CLOCK = pygame.time.Clock()
    FPS = 60

    FONT_DEFAULT = pygame.font.Font(None, 36)

    running = True

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

    while running:
        CLOCK.tick(FPS)

        # reset window
        WINDOW.fill(BLACK)

        # # begin drawing
        # text_surface = FONT_DEFAULT.render("Demo Text", True, GREEN_4, GRAY_27)
        # text_rect = text_surface.get_rect()
        # text_rect.center = WINDOW.get_rect().center
        # WINDOW.blit(text_surface, text_rect)

        # handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            elif event.type == pygame.KEYDOWN:
                # Set the acceleration value.
                if event.key == pygame.K_LEFT:
                    x_accel = -x_accel_r
                if event.key == pygame.K_RIGHT:
                    x_accel = x_accel_r
                if event.key == pygame.K_UP:
                    y_accel = -y_accel_r
                if event.key == pygame.K_DOWN:
                    y_accel = y_accel_r
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
        pygame.draw.rect(WINDOW, (0, 120, 250), mallow_rect)

        # update the display
        # draw everything
        # pygame.display.flip()
        # draw everything, or pass a surface or shape to update only that portion.
        pygame.display.update()

    pygame.quit()

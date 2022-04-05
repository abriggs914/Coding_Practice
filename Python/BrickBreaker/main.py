from colour_utility import *
from utility import *
import pygame
from map_parser import *


if __name__ == "__main__":

    map_001 = JMap("map_001.json")
    map_001.bounce_bottom = True  # testing
    map_001.test_map()
    print(dict_print(map_001.__dict__, map_001.name))

    map_001.add_ball(300, 600, "normal")

    # map_001.balls[0].centre = 50, 50
    # map_001.balls[1].centre = 150, 250
    # map_001.balls[0].x_speed = 4
    # map_001.balls[0].y_speed = 2
    # map_001.balls[1].x_speed = 1
    # map_001.balls[1].y_speed = 3

    pygame.init()
    WIDTH, HEIGHT = 800, 800
    WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
    CLOCK = pygame.time.Clock()
    FPS = 60

    FONT_DEFAULT = pygame.font.Font(None, 36)

    map_001.rect.center = WINDOW.get_rect().center
    running = True

    while running:

        # reset window
        WINDOW.fill(BLACK)

        map_001.draw(WINDOW)

        # # begin drawing
        # text_surface = FONT_DEFAULT.render(f"# bounces: {map_001.balls[0].n_bounces}, # breaks: {map_001.balls[0].n_breaks}", True, GREEN_4, GRAY_27)
        # text_rect = text_surface.get_rect()
        # text_rect.center = WINDOW.get_rect().center
        # WINDOW.blit(text_surface, text_rect)

        # handle events
        mouse = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break

        map_001.move(WINDOW)
        CLOCK.tick(FPS)

        # update the display
        pygame.display.update()

    pygame.quit()

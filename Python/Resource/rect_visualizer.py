from colour_utility import *
from utility import *
import pygame


if __name__ == "__main__":
    pygame.init()
    WIDTH, HEIGHT = 750, 550
    WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
    CLOCK = pygame.time.Clock()
    FPS = 60

    ADJUSTING_SIZE = None
    RADIUS = 15
    RECT = pygame.Rect(0, 0, 120, 120)
    RECT.center = WINDOW.get_rect().center

    FONT_DEFAULT = pygame.font.Font(None, 36)

    running = True

    while running:

        # reset window
        WINDOW.fill(BLACK)

        # begin drawing
        pygame.draw.rect(WINDOW, ORANGE_3, RECT)
        pygame.draw.circle(WINDOW, BLUE_2, RECT.topleft, RADIUS)
        pygame.draw.circle(WINDOW, BLUE_2, RECT.topright, RADIUS)
        pygame.draw.circle(WINDOW, BLUE_2, RECT.bottomleft, RADIUS)
        pygame.draw.circle(WINDOW, BLUE_2, RECT.bottomright, RADIUS)

        text_surface = FONT_DEFAULT.render(f"{RECT}", True, GREEN_4, GRAY_27)
        text_rect = text_surface.get_rect()
        text_rect.center = WINDOW.get_rect().center
        WINDOW.blit(text_surface, text_rect)

        # handle events
        mouse = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if distance(RECT.topleft, mouse) <= RADIUS:
                    ADJUSTING_SIZE = 0
                elif distance(RECT.topright, mouse) <= RADIUS:
                    ADJUSTING_SIZE = 1
                elif distance(RECT.bottomleft, mouse) <= RADIUS:
                    ADJUSTING_SIZE = 2
                elif distance(RECT.bottomright, mouse) <= RADIUS:
                    ADJUSTING_SIZE = 3
            elif event.type == pygame.MOUSEMOTION:
                if ADJUSTING_SIZE == 0:
                    RECT.left = clamp(0, mouse[0], WINDOW.get_rect().right - RADIUS)
                    RECT.top = clamp(0, mouse[1], WINDOW.get_rect().bottom - RADIUS)
                    RECT.width = clamp(RADIUS, RECT.width, WINDOW.get_rect().right - RECT.left)
                    RECT.height = clamp(RADIUS, RECT.height, WINDOW.get_rect().bottom - RECT.top)
                elif ADJUSTING_SIZE == 1:
                    RECT.width = clamp(RADIUS, mouse[0] - RECT.x, WINDOW.get_rect().right)
                elif ADJUSTING_SIZE == 2:
                    RECT.height = clamp(RADIUS, mouse[1] - RECT.y, WINDOW.get_rect().bottom)
                elif ADJUSTING_SIZE == 3:
                    RECT.width = clamp(RADIUS, mouse[0] - RECT.x, WINDOW.get_rect().right)
                    RECT.height = clamp(RADIUS, mouse[1] - RECT.y, WINDOW.get_rect().bottom)
            elif event.type == pygame.MOUSEBUTTONUP:
                ADJUSTING_SIZE = None

        CLOCK.tick(FPS)

        # update the display
        pygame.display.update()

    pygame.quit()

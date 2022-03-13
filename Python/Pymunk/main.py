from colour_utility import *
import pygame
import pymunk
import pymunk.pygame_util
import math


pygame.init()
WIDTH, HEIGHT = 750, 550
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))


def run(window, width, height):
    running = True
    clock = pygame.time.Clock()
    fps = 60
    running = True

    while running:

        # reset window
        # WINDOW.fill(BLACK)

        # begin drawing
        # text_surface = FONT_DEFAULT.render("Demo Text", True, GREEN_4, GRAY_27)
        # text_rect = text_surface.get_rect()
        # text_rect.center = WINDOW.get_rect().center
        # WINDOW.blit(text_surface, text_rect)

        # handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break

        clock.tick(fps)

        # update the display
        # draw everything
        # pygame.display.flip()
        # draw everything, or pass a surface or shape to update only that portion.
        pygame.display.update()


if __name__ == '__main__':

    FONT_DEFAULT = pygame.font.Font(None, 36)



    pygame.quit()

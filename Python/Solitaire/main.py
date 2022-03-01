import pygame
from colour_utility import *
from solitaire import *


if __name__ == '__main__':

    s = Solitaire()

    # pygame.init()
    #
    # WIDTH, HEIGHT = 1600, 1000
    # WIN = pygame.display.set_mode((WIDTH, HEIGHT))
    # pygame.display.set_caption("Solitaire")
    # FONT = pygame.font.SysFont("comicsans", 16)
    #
    # run = True
    # clock = pygame.time.Clock()
    #
    # while run:
    #     clock.tick(60)
    #     WIN.fill(BLACK)
    #
    #     for event in pygame.event.get():
    #         if event.type == pygame.QUIT:
    #             run = False
    #
    #     pygame.display.update()
    #
    # pygame.quit()
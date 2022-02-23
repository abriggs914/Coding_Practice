import pygame
from colour_utility import *

# Game vars
APPLICATION_TITLE = "Motherload"
WIDTH, HEIGHT = 750, 500
BACKGROUND_FILL = GRAY_17
FRAME_RATE = 60

# Initialize pygame & vars
pygame.init()
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
CLOCK = pygame.time.Clock()


def main_loop():

    pygame.display.set_caption(APPLICATION_TITLE)

    is_playing = True
    while is_playing:

        # Wipe background
        WINDOW.fill(BACKGROUND_FILL)
        CLOCK.tick(FRAME_RATE)

        # Draw game elements
        pygame.display.update()

        # Handle events
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                is_playing = False

    pygame.quit()
    print("Thanks For Playing!")


if __name__ == "__main__":
    main_loop()

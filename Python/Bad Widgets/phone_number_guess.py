from pygame_utility import *

def main():
    app = PygameApplication("Phone Number Guess", 500, 450, auto_init=True)
    game = app.get_game()
    display = app.display

    r1 = Rect(45, 10, 60, 100)
    game.draw.rect(display, CARROT, r1.tupl)
    while app.is_playing:
        app.run()

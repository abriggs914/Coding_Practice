from pygame_utility import *

def main():
    app = PygameApplication("Phone Number Guess", 600, 550, auto_init=True)
    game = app.get_game()
    display = app.display

    r1 = Rect(45, 10, 400, 300)
    r_lbl = Rect(r1.left + 2, r1.top + 2, r1.width - 4, r1.height - 4)
    r_txt = Rect(r_lbl.left, r_lbl.bottom + 5, r1.width - 4, r1.height - 4)
    frame_main = VBox(game, display, None, r1, 1, WHITE)
    label = Label(game, display, r_lbl, "Is this your Phone Number?")
    textbox = TextBox(game, display, r_txt,ic=BROWN_3, ac=INDIGO)
    frame_main.add_contents(label, textbox)
    while app.is_playing:

        # call at beginning of main loop
        display.fill(BLACK)

        # Do Stuff
        # game.draw.rect(display, CARROT, r1.tupl)
        frame_main.draw()


        # call at end of main loop
        app.run()

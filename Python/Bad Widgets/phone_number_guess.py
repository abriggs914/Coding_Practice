from pygame_utility import *


def main():

    def n_rnd_ns(n, vals=tuple(range(10))):
        return "".join([str(random.choice(vals)) for i in range(n)])

    def random_phone_number():
        return "+1 (" + n_rnd_ns(3) + ") " + n_rnd_ns(3) + "-" + n_rnd_ns(4)

    def phone_number_found():
        print("phone_number_found")

    def new_phone_number():
        print("new_phone_number")
        textbox.set_text(random_phone_number())

    def increment_phone_number():
        n = int(textbox.get_text().replace("(", "").replace(")", "").replace("+", "").replace(" ", "").replace("-", ""))
        print(n)
        n += 1
        n = str(n)
        textbox.set_text("+{} ({}) {}-{}".format(n[0], n[1: 4], n[4:7], n[7:]))

    def decrement_phone_number():
        n = int(textbox.get_text().replace("(", "").replace(")", "").replace("+", "").replace(" ", "").replace("-", ""))
        print(n)
        n -= 1
        n = max(0, n)
        n = str(n)
        textbox.set_text("+{} ({}) {}-{}".format(n[0], n[1: 4], n[4:7], n[7:]))


    app = PygameApplication("Phone Number Guess", 600, 550, auto_init=True)
    game = app.get_game()
    display = app.display

    r1 = Rect(45, 10, 400, 300)
    r_lbl = Rect(r1.left + 2, r1.top + 2, r1.width - 4, r1.height - 4)
    r_txt = Rect(r_lbl.left + 6, r_lbl.bottom + 5, r1.width - 4, r1.height - 4)
    frame_main = VBox(game, display, None, r1, 1, HOTPINK)
    label = Label(game, display, r_lbl, "Is this your Phone Number?", fs=40)
    textbox = TextBox(game, display, r_txt, ic=BROWN_3, ac=INDIGO, fc=GREEN, editable=False, draw_clear_btn=False, font_size=35, text_align="center_rotary", numeric=True, iaction=increment_phone_number, daction=decrement_phone_number)
    #TODO allow TextBox to overwrite the inc and dec functions. ex inc on a phone number should produce phone#n => phone#n + 1.
    #TODO allow TextBox to center_rotary text
    textbox.set_text(random_phone_number())
    btnbar = ButtonBar(game, display, r_txt, None, VIOLETRED, 1, is_horizontal=True)
    btnbar.add_button("Yes", FORESTGREEN, GREEN, phone_number_found)
    btnbar.add_button("No", ORCHID, FIREBRICK, new_phone_number)
    frame_main.add_contents(label, textbox, btnbar)
    while app.is_playing:

        # call at beginning of main loop
        display.fill(BLACK)

        # Do Stuff
        # game.draw.rect(display, CARROT, r1.tupl)
        # print(random_phone_number())
        frame_main.draw()

        # call at end of main loop
        event_queue = app.run()
        for event in event_queue:
            textbox.handle_event(event)

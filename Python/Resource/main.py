from utility import *
from test_suite import *
from pygame_utility import *

# test area and scratch pad
"""
test_lists = [
    ([[1, 2], [3, 4]], [1, 2, 3, 4]),
    ([[[1], 2], [[3, 4]]], [1, 2, 3, 4]),
    ([1, 2, 3, 4], [1, 2, 3, 4]),
    ([[[[[[[[[[[1]], 2]], 3]], 4]]]]], [1, 2, 3, 4]),
    (None, [None]),
    ([], []),
    (0, [0]),
    (1, [1]),
    (dict(), [dict()]),
    (tuple(), [tuple()]),
    (list(), list()),
    (int(), [int()]),
    (float(), [float()]),
    (True, [True]),
    (False, [False]),
    (bool(), [bool()]),
    ({1: [1, 2]}, [{1: [1, 2]}]),
    (print, [print])
]


correct_answers = []
for i, vals in enumerate(test_lists[:30]):
    lst, ans = vals
    res = flatten(lst)
    right = ans == res
    correct_answers.append(right)
    print("\n\n\t\t{}\n\n\tIN:\n".format(i + 1) + str(lst))
    print("\tOUT:\n" + str(res))
    print("\tANS:\n" + str(ans))
    print("\tRIGHT:\n" + str(right))

all_right = all(correct_answers)
print("all correct", all_right)
"""


def text_rect_and_line():
    title = "Testing Rect and Line classes"
    w = 900
    h = 600

    r1 = Rect(15, 20, 25, 30)
    r2 = Rect(10, 10, w - 20, h - 20)
    l1 = Line(0, 0, 100, 100)

    collide_line_tests = TestSuite(test_func=l1.collide_line)
    collide_line_tests.add_test("l1 intersects r1.top_line", ([r1.top_line], True))
    collide_line_tests.add_test("l1 intersects r1.bottom_line", ([r1.bottom_line], True))
    collide_line_tests.add_test("l1 intersects r1.left_line", ([r1.left_line], True))
    collide_line_tests.add_test("l1 intersects r1.right_line", ([r1.right_line], True))

    collide_line_tests.execute()

    app = PygameApplication(title, w, h)
    app.init()
    pygame.display.set_mode((w, h))

    print(dict_print({
        "r1.collide_line(l1)": r1.collide_line(l1),
        "r1": r1,
        "left": r1.left_line,
        "collide_left": str(l1.collide_line(r1.left_line)),
        "right": r1.right_line,
        "collide_right": str(l1.collide_line(r1.right_line)),
        "top": r1.top_line,
        "collide_top": str(l1.collide_line(r1.top_line)),
        "bottom": r1.bottom_line,
        "collide_bottom": str(l1.collide_line(r1.bottom_line)),
    }, "Data"))

    results = {
        "x: -1": 0,
        "x: 0": 0,
        "x: 1": 0,
        "y: -1": 0,
        "y: 0": 0,
        "y: 1": 0,
    }

    while app.is_playing:
        app.display.fill(app.background_colour)
        pygame.draw.rect(app.display, YELLOW_3, r2.tupl)
        pygame.draw.rect(app.display, GREEN, r1.tupl)
        pygame.draw.line(app.display, RED, *l1.tupl)

        x_c = weighted_choice(((1, 0.95), (0, 0.025), (-1, 0.025)))
        y_c = weighted_choice(((1, 0.5), (0, 0.25), (-1, 0.25)))

        x_c = weighted_choice([0, 1])
        y_c = weighted_choice([0, 1])

        results["x: {}".format(x_c)] += 1
        results["y: {}".format(y_c)] += 1
        r1.translate(x_c, y_c)
        l1.translate(x_c, y_c)
        app.run()
        if not r2.collide_rect(r1, strictly_inside=False):
            raise ValueError("not r2.collide_rect(r1)")
        # print(dict_print(results, "Results"))

    def rotate_matrix(grid, n=None, m=None, filter_none=False):
        """Return a list of all possible cell lines."""
        PAD = "PAD"
        n = n if n is not None else len(grid)
        m = m if m is not None else len(grid[0]) if n else -1
        res = [row.copy() for row in grid]
        temp_grid = [[grid[j][i] for j in range(n)] for i in range(m)]
        print("1 grid     :", grid)
        print("1 temp_grid:", temp_grid)
        if m < n:
            grid, temp_grid = temp_grid, grid
            n, m = m, n
        print("2 grid     :", grid)
        print("2 temp_grid:", temp_grid)
        res += temp_grid
        oo = (n + m) % 2
        di = abs(n - m) + 1 + oo
        ts = int(((n + m - 1) - di) / 2) + oo
        a = ts - 1

        lc = 0
        cc = 0
        e = 0
        t = (3 * n) + (3 * m) - 2
        temp = [[] for i in range(t)]
        print("3 grid     :", grid)
        print("3 temp_grid:", temp_grid)
        print("3 temp:", temp)
        # print("len[]({}), len[0]({})".format(len(temp), len(temp[0])))

        print("N x M: ({} x {})".format(n, m))
        for i in range(n):
            for j in range(m):
                v = grid[i][j]
                s = min(i, j)
                npl = i - s, j - s
                d1 = n + m + (npl[0] + npl[1])
                if (j - s) == 0 and (i - s) != 0:
                    d1 += m - 1

                f = max(0, min(i, m - j - 1))
                npr = i - f, j + f
                d2 = n + m + (npr[0] + npr[1])
                print("npr:", npr, "f:", f)
                if (j + f) == m and (i - f) != 0:
                    d2 += m - 1
                d2 += (n + m - 1)
                print("i:", i, "| j:", j, "| v:", v, "| d1:", d1, "| d2:", d2, "| di:", (n + m - 1))
                temp[i].append((i, j, v))
                temp[j + n].append((i, j, v))
                temp[d1].append((i, j, v))
                temp[d2].append((i, j, v))
        print("4 grid     :", grid)
        print("4 temp_grid:", temp_grid)
        print("4 temp:", temp)

        return temp

    # g1 = []
    # print(rotate_matrix())


def print_hi():
    print("Hi from print_hi")


def test_TextBox():
    app = PygameApplication("Test TextBox", 600, 400)
    game = app.get_game()
    display = app.display
    r1 = Rect(100, 25, 200, 100)
    # self, game, display, rect, ic, ac, f, fc, text = '', min_width = 20, numeric = False, char_limit = None, n_limit = None, bs = 1, border_style = None
    textbox = TextBox(game, display, r1, text="-1", numeric=True, daction=print_hi, dargs=None)
    while app.is_playing:
        display.fill(BLACK)
        textbox.draw()
        event_queue = app.run()
        for event in event_queue:
            textbox.handle_event(event)


def text_box():
    app = PygameApplication("Test Box", 1100, 500)
    game = app.get_game()
    display = app.display
    r1 = Rect(100, 25, 600, 250)
    r2 = r1.translated(2, 2).scaled(0.75, 0.2)
    # self, game, display, rect, ic, ac, f, fc, text = '', min_width = 20, numeric = False, char_limit = None, n_limit = None, bs = 1, border_style = None
    lbl1 = Label(game, display, r2, "Sample Label 1", c=RED, txc=WHITE, bc=FIREBRICK)
    lbl2 = Label(game, display, r2.translated(0, 6), "Sample Label 1", c=GREEN, txc=YELLOW_3, bc=LIMEGREEN)
    box = VBox(game, display, [], r1, 1, WHITE)
    box.add_contents(lbl1, lbl2)
    while app.is_playing:
        display.fill(BLACK)
        box.draw()
        event_queue = app.run()
        # for event in event_queue:
        #     textbox.handle_event(event)


def test_buttonbar():
    app = PygameApplication("Test Box", 1100, 500)
    game = app.get_game()
    display = app.display

    r1 = Rect(100, 25, 600, 250)
    r2 = r1.translated(2, 2).scaled(0.75, 0.2)

    btnbar1 = ButtonBar(game, display, r1, bg=TEAL, is_horizontal=True)
    btnbar2 = ButtonBar(game, display, r1, bg=TEAL, is_horizontal=False)
    # self, game, display, rect, ic, ac, f, fc, text = '', min_width = 20, numeric = False, char_limit = None, n_limit = None, bs = 1, border_style = None
    # lbl1 = Label(game, display, r2, "Sample Label 1", c=RED, txc=WHITE, bc=FIREBRICK)
    # lbl2 = Label(game, display, r2.translated(0, 6), "Sample Label 1", c=GREEN, txc=YELLOW_3, bc=LIMEGREEN)
    box = VBox(game, display, [], r1, 1, WHITE)
    btnbar1.add_button("A1", VIOLET, brighten(VIOLET, 0.15), eval, "print(\"hey from A1\")")
    btnbar1.add_button("B1", GREEN, brighten(GREEN, 0.15), eval, "print(\"hey from B1\")")
    btnbar1.add_button("C1", LAWNGREEN, brighten(LAWNGREEN, 0.15), eval, "print(\"hey from C1\")")

    btnbar2.add_button("A2", VIOLET, brighten(VIOLET, 0.15), eval, "print(\"hey from A2\")")
    btnbar2.add_button("B2", GREEN, brighten(GREEN, 0.15), eval, "print(\"hey from B2\")")
    btnbar2.add_button("C2", LAWNGREEN, brighten(LAWNGREEN, 0.15), eval, "print(\"hey from C2\")")

    box.add_contents(btnbar1, btnbar2)
    xp, yp = -1, -1
    while app.is_playing:
        display.fill(BLACK)
        box.draw()
        rect = box.rect_obj
        if (rect.width + xp) < 1:
            xp = 1
        if (rect.height + yp) < 1:
            yp = 1
        if (rect.width + xp) > 500:
            xp = -1
        if (rect.height + yp) > 500:
            yp = -1
        new_rect = Rect(rect.x - xp, rect.y - yp, rect.width + (2 * xp), rect.height + (2 * yp))
        box.resize(new_rect)
        event_queue = app.run()
        # print("A", box.rect_obj, new_rect, xp, yp)
        # if 1 > new_rect.width:
        #     xp = 1.02
        #     new_rect.resize(Rect(new_rect.x, new_rect.y, 1, new_rect.height))
        #     # new_rect = box.rect_obj.scaled(xp, yp)
        #     print("\tA\t", new_rect, xp, yp)
        # if new_rect.width >= 600:
        #     xp = 0.99
        #     new_rect = box.rect_obj.scaled(xp, yp)
        #     print("\tB\t", new_rect, xp, yp)
        # if 1 > new_rect.height:
        #     yp = 1.02
        #     new_rect.resize(Rect(new_rect.x, new_rect.y, new_rect.width, 1))
        #     # new_rect = box.rect_obj.scaled(xp, yp)
        #     print("\tC\t", new_rect, xp, yp)
        # if new_rect.height >= 600:
        #     yp = 0.99
        #     new_rect = box.rect_obj.scaled(xp, yp)
        #     print("\tD\t", new_rect, xp, yp)
        # print("B", box.rect_obj, new_rect, xp, yp)
        # for event in event_queue:
        #     textbox.handle_event(event)

    # xp, yp = 0.99, 0.99
    # while app.is_playing:
    #     display.fill(BLACK)
    #     box.draw()
    #     new_rect = box.rect_obj.scaled(xp, yp)
    #     print("A", box.rect_obj, new_rect, xp, yp)
    #     if 1 > new_rect.width:
    #         xp = 1.02
    #         new_rect.resize(Rect(new_rect.x, new_rect.y, 1, new_rect.height))
    #         # new_rect = box.rect_obj.scaled(xp, yp)
    #         print("\tA\t", new_rect, xp, yp)
    #     if new_rect.width >= 600:
    #         xp = 0.99
    #         new_rect = box.rect_obj.scaled(xp, yp)
    #         print("\tB\t", new_rect, xp, yp)
    #     if 1 > new_rect.height:
    #         yp = 1.02
    #         new_rect.resize(Rect(new_rect.x, new_rect.y, new_rect.width, 1))
    #         # new_rect = box.rect_obj.scaled(xp, yp)
    #         print("\tC\t", new_rect, xp, yp)
    #     if new_rect.height >= 600:
    #         yp = 0.99
    #         new_rect = box.rect_obj.scaled(xp, yp)
    #         print("\tD\t", new_rect, xp, yp)
    #     print("B", box.rect_obj, new_rect, xp, yp)
    #     box.resize(new_rect)
    #     event_queue = app.run()
    #     # for event in event_queue:
    #     #     textbox.handle_event(event)


def test_phone_number():
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
    textbox = TextBox(game, display, r_txt, ic=BROWN_3, ac=INDIGO, fc=GREEN, editable=False, draw_clear_btn=False,
                      font_size=35, text_align="center", numeric=True, iaction=increment_phone_number,
                      daction=decrement_phone_number)
    # TODO allow TextBox to overwrite the inc and dec functions. ex inc on a phone number should produce phone#n => phone#n + 1.
    # TODO allow TextBox to center text
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


def test_slider():
    app = PygameApplication("Phone Number Guess", 600, 550, auto_init=True)
    game = app.get_game()
    display = app.display

    r1 = Rect(45, 10, 400, 300)
    r_lbl = Rect(r1.left + 2, r1.top + 2, r1.width - 4, r1.height - 4)
    r_txt = Rect(r_lbl.left + 6, r_lbl.bottom + 5, r1.width - 4, r1.height - 4)
    frame_main = VBox(game, display, None, r1, 1, HOTPINK)
    label = Label(game, display, r_lbl, "Slider demo", fs=40)
    slider = Slider(game, display, r1, slider_width=3, min_val=-10, max_val=1000, n_ticks=100, stick_to_ticks=False)
    frame_main.add_contents(label, slider)
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
            slider.handle_event(event)

def test_block_letters():
    blk_lst = [val for val in dir() if "BLK_" in val]
    print("\n\n\n".join([eval(blk)[1] for blk in blk_lst]))


def test_reduce():
    # TS = TestSuite(test_func=[reduce], tests={"test": [[[1, 2, 3, 4, 5, 6], 0.33, "left"], [1, 2]]})
    # TS = TestSuite(test_func=reduce, tests=[[[1, 2, 3, 4, 5, 6], 0.33, "left"], [1, 2]])
    TS = TestSuite()
    TS.set_func(reduce)
    TS.add_test("Test left 1", [[[1, 2, 3, 4, 5, 6], 0.33, "left"], [1, 2]])
    TS.add_test("Test right 1", [[[1, 2, 3, 4, 5, 6], 0.33, "right"], [5, 6]])
    TS.add_test("Test center 1", [[[1, 2, 3, 4, 5, 6], 0.33, "center"], [3, 4]])
    TS.add_test("Test distributed 1", [[[1, 2, 3, 4, 5, 6], 0.33, "distributed"], [1, 4]])
    TS.add_test("Test distributed 2", [[[1, 2, 3, 4, 5, 6], 0.5, "distributed"], [1, 3, 5]])
    TS.add_test("Test center 2", [[list(range(-15, 48, 3)), 0.5, "CENTER"], list(range(0, 33, 3))])
    print("TS after creation:\n\n", TS)
    # TS.execute()
    TS.execute_log()


if __name__ == "__main__":
    # test_block_letters()
    # test_TextBox()
    # test_buttonbar()
    # test_phone_number()
    # test_slider()
    test_reduce()

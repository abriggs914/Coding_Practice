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
    TS.add_test("Test center 2", [[list(range(-15, 48, 3)), 1, "CENTER"], list(range(-15, 48, 3))])
    print("TS after creation:\n\n", TS)
    # TS.execute()
    TS.execute_log()


def test_directions():
    t_arr = (
        (1, 2, 3),
        (4, 5, 6),
        (7, 8, 9)
    )

    def get_ij(arr, i, j):
        if not 0 <= i < len(arr):
            return None
        if not 0 <= i < len(arr[i]):
            return None
        return arr[i][j]

    def test_ij(direction, start_i=0, start_j=0, arr=t_arr):
        direction = DIRECTIONS[direction]
        i = direction["i"]
        j = direction["j"]
        return get_ij(arr, start_i + i, start_j + j)

    def test_xy(direction, start_y=0, start_x=0, arr=t_arr):
        direction = DIRECTIONS[direction]
        x = direction["x"]
        y = direction["y"]
        return get_ij(arr, start_y + y, start_x + x)

    TS1 = TestSuite()
    TS1.set_func(test_ij)
    TS1.add_test("Test North from arr[1][1]", [["N", 1, 1], 2])
    TS1.add_test("Test South from arr[1][1]", [["S", 1, 1], 8])
    TS1.add_test("Test East from arr[1][1]", [["E", 1, 1], 4])
    TS1.add_test("Test West from arr[1][1]", [["W", 1, 1], 6])
    TS1.add_test("Test North-East from arr[1][1]", [["NE", 1, 1], 1])
    TS1.add_test("Test North-West from arr[1][1]", [["NW", 1, 1], 3])
    TS1.add_test("Test South-East from arr[1][1]", [["SE", 1, 1], 7])
    TS1.add_test("Test South-West from arr[1][1]", [["SW", 1, 1], 9])
    TS1.execute_log(True)

    TS2 = TestSuite()
    TS2.set_func(test_xy)
    TS2.add_test("Test North from arr[1][1]", [["N", 1, 1], 2])
    TS2.add_test("Test South from arr[1][1]", [["S", 1, 1], 8])
    TS2.add_test("Test East from arr[1][1]", [["E", 1, 1], 4])
    TS2.add_test("Test West from arr[1][1]", [["W", 1, 1], 6])
    TS2.add_test("Test North-East from arr[1][1]", [["NE", 1, 1], 1])
    TS2.add_test("Test North-West from arr[1][1]", [["NW", 1, 1], 3])
    TS2.add_test("Test South-East from arr[1][1]", [["SE", 1, 1], 7])
    TS2.add_test("Test South-West from arr[1][1]", [["SW", 1, 1], 9])
    TS2.execute_log(True)


def test_date_suffix(day):
    s_day = str(day)
    print("sday: \"{}\"".format(s_day))
    if s_day[-1] == "1":
        res = "st"
        print("A sday: {}".format(s_day))
        if len(s_day) > 1:
            if s_day[-2] == "1":
                res = "th"
    elif s_day[-1] == "2":
        res = "nd"
        if len(s_day) > 1:
            print("B sday: {}, s_day[-2]: {}".format(s_day, s_day[-2]))
            if s_day[-2] == "1":
                res = "th"
    elif s_day[-1] == "3":
        res = "rd"
        print("C sday: {}".format(s_day))
        if len(s_day) > 1:
            if s_day[-2] == "1":
                res = "th"
    else:
        print("D sday: {}".format(s_day))
        res = "th"
    return res


# Takes "2021-08-03" -< August 3rd, 2021
def datestr_format(date_str):
    date_obj = dt.datetime.fromisoformat(date_str)
    suffix = date_suffix(date_obj.day)
    res = dt.datetime.strftime(date_obj, "%B %d###, %Y").replace("###", suffix)
    s_res = res.split(" ")
    x = s_res[1] if s_res[1][0] != "0" else s_res[1][1:]
    res = " ".join([s_res[0], x, s_res[2]])
    return res


def test_datestr_format(date_list):
    TS = TestSuite()
    TS.set_func(date_str_format)
    for i, date_data in enumerate(date_list):
        print("i: {}, date_data: {}".format(i, date_data))
        date, ans = date_data
        TS.add_test(str(i), [[date], ans])
    TS.execute_log()


def test_new_rect():
    w, h = 1100, 900
    app = PygameApplication("Test TextBox", w, h)
    game = app.get_game()
    display = app.display

    wh = min(w, h)
    rx = w / 2
    ry = h / 2
    rw = (wh * 0.25) / 2
    rh = (wh * 0.25) / 2

    a = 0
    diff = 1
    r = Rect2(rx, ry, rw, rh, a)
    d = 0, 20
    print(r)


    # r1 = Rect(100, 25, 200, 100)
    # self, game, display, rect, ic, ac, f, fc, text = '', min_width = 20, numeric = False, char_limit = None, n_limit = None, bs = 1, border_style = None
    # textbox = TextBox(game, display, r1, text="-1", numeric=True, daction=print_hi, dargs=None)
    while app.is_playing:
        display.fill(BLACK)

        r0 = Rect2(rx, ry, rw, rh, a + 0)
        r1 = Rect2(rx, ry, rw, rh, a + 30)
        r2 = Rect2(rx, ry, rw, rh, a + 60)
        r3 = Rect2(rx, ry, rw, rh, a + 90)
        r4 = Rect2(rx, ry, rw, rh, a + 120)
        r5 = Rect2(rx, ry, rw, rh, a + 150)
        r6 = Rect2(rx, ry, rw, rh, a + 180)
        r7 = Rect2(rx, ry, rw, rh, a + 210)
        r8 = Rect2(rx, ry, rw, rh, a + 240)
        r9 = Rect2(rx, ry, rw, rh, a + 270)
        r10 = Rect2(rx, ry, rw, rh, a + 300)
        r11 = Rect2(rx, ry, rw, rh, a + 330)
        r12 = Rect2(rx, ry, rw, rh, a + 360)
        # r5 = Rect2(rx, ry, rw, rh, a + )

        def draw_rect3(r):
            # textbox.draw()
            p1 = r.p1
            p2 = r.p2
            p3 = r.p3
            p4 = r.p4
            game.draw.line(display, WHITE, p1, p2)
            game.draw.line(display, WHITE, p2, p3)
            game.draw.line(display, WHITE, p3, p4)
            game.draw.line(display, WHITE, p4, p1)

            pa1 = r.max_encapsulating_rect.p1
            pa2 = r.max_encapsulating_rect.p2
            pa3 = r.max_encapsulating_rect.p3
            pa4 = r.max_encapsulating_rect.p4
            game.draw.line(display, WHITE, pa1, pa2)
            game.draw.line(display, WHITE, pa2, pa3)
            game.draw.line(display, WHITE, pa3, pa4)
            game.draw.line(display, WHITE, pa4, pa1)

            pi1 = r.min_encapsulating_rect.p1
            pi2 = r.min_encapsulating_rect.p2
            pi3 = r.min_encapsulating_rect.p3
            pi4 = r.min_encapsulating_rect.p4
            game.draw.line(display, WHITE, pi1, pi2)
            game.draw.line(display, WHITE, pi2, pi3)
            game.draw.line(display, WHITE, pi3, pi4)
            game.draw.line(display, WHITE, pi4, pi1)

        def draw_rect2(r):
            # textbox.draw()
            p1 = r.p1
            p2 = r.p2
            p3 = r.p3
            p4 = r.p4
            game.draw.line(display, WHITE, p1, p2)
            game.draw.line(display, WHITE, p2, p3)
            game.draw.line(display, WHITE, p3, p4)
            game.draw.line(display, WHITE, p4, p1)

            pa1 = r.max_encapsulating_rect.p1
            pa2 = r.max_encapsulating_rect.p2
            pa3 = r.max_encapsulating_rect.p3
            pa4 = r.max_encapsulating_rect.p4
            game.draw.line(display, WHITE, pa1, pa2)
            game.draw.line(display, WHITE, pa2, pa3)
            game.draw.line(display, WHITE, pa3, pa4)
            game.draw.line(display, WHITE, pa4, pa1)

            pi1 = r.min_encapsulating_rect.p1
            pi2 = r.min_encapsulating_rect.p2
            pi3 = r.min_encapsulating_rect.p3
            pi4 = r.min_encapsulating_rect.p4
            game.draw.line(display, WHITE, pi1, pi2)
            game.draw.line(display, WHITE, pi2, pi3)
            game.draw.line(display, WHITE, pi3, pi4)
            game.draw.line(display, WHITE, pi4, pi1)

        def draw_rect1(r):
            # textbox.draw()
            p1 = r.p1
            p2 = r.p2
            p3 = r.p3
            p4 = r.p4
            game.draw.line(display, RED, p1, p2)
            game.draw.line(display, GREEN, p2, p3)
            game.draw.line(display, BLUE, p3, p4)
            game.draw.line(display, YELLOW_3, p4, p1)

            pa1 = r.max_encapsulating_rect.p1
            pa2 = r.max_encapsulating_rect.p2
            pa3 = r.max_encapsulating_rect.p3
            pa4 = r.max_encapsulating_rect.p4
            game.draw.line(display, ORANGE, pa1, pa2)
            game.draw.line(display, PURPLE, pa2, pa3)
            game.draw.line(display, ROYALBLUE, pa3, pa4)
            game.draw.line(display, TAN, pa4, pa1)

            pi1 = r.min_encapsulating_rect.p1
            pi2 = r.min_encapsulating_rect.p2
            pi3 = r.min_encapsulating_rect.p3
            pi4 = r.min_encapsulating_rect.p4
            game.draw.line(display, LIMEGREEN, pi1, pi2)
            game.draw.line(display, SKYBLUE, pi2, pi3)
            game.draw.line(display, WHITE, pi3, pi4)
            game.draw.line(display, BROWN_1, pi4, pi1)

        game.draw.circle(display, TAN, d, 3)
        # d = d[0] + 1, d[1] + 1
        # print("d", d, "collision:", r.collide_point(*d))
        #
        # draw_rect1(r0)
        # draw_rect1(r1)
        # draw_rect1(r2)
        # draw_rect1(r3)
        # draw_rect1(r4)
        # draw_rect1(r5)
        # draw_rect1(r6)
        # draw_rect1(r7)

        # draw_rect2(r0)
        # draw_rect2(r1)
        # draw_rect2(r2)
        # draw_rect2(r3)
        # draw_rect2(r4)
        # draw_rect2(r5)
        # draw_rect2(r6)
        # draw_rect2(r7)

        draw_rect3(r0)
        draw_rect3(r1)
        draw_rect3(r2)
        draw_rect3(r3)
        draw_rect3(r4)
        draw_rect3(r5)
        draw_rect3(r6)
        draw_rect3(r7)
        draw_rect3(r8)
        draw_rect3(r9)
        draw_rect3(r10)
        draw_rect3(r11)
        draw_rect3(r12)

        if r.collide_point(*d):
            break
        event_queue = app.run()
        for event in event_queue:
            if event.type == game.KEYDOWN:
                if event.key == game.K_UP:
                    d = (d[0], d[1] - 1)
                if event.key == game.K_DOWN:
                    d = (d[0], d[1] + 1)
                if event.key == game.K_LEFT:
                    d = (d[0] - 1, d[1])
                if event.key == game.K_RIGHT:
                    d = (d[0] + 1, d[1])
            # textbox.handle_event(event)
        # app.run()
        a += diff
        a = a % 360
        # if a >= 359:
        #     diff = -1
        # elif a < 1:
        #     diff = 1

        app.clock.tick(25)


def test_find_north_side():

    def find_north_side(r):
        return r.top_line

    def find_south_side(r):
        return r.bottom_line

    def find_east_side(r):
        return r.right_line

    def find_west_side(r):
        return r.left_line

    r = Rect2(0, 0, 10, 10)
    nl = Line(0, 0, 10, 0)
    sl = Line(0, 10, 10, 10)
    el = Line(10, 0, 10, 10)
    wl = Line(0, 0, 0, 10)
    TS = TestSuite()
    TS.set_func(find_north_side)
    TS.add_test("north", [[r], nl])
    TS.execute_log()
    TS = TestSuite()
    TS.set_func(find_south_side)
    TS.add_test("south", [[r], sl])
    TS.execute_log()
    TS = TestSuite()
    TS.set_func(find_east_side)
    TS.add_test("east", [[r], el])
    TS.execute_log()
    TS = TestSuite()
    TS.set_func(find_west_side)
    TS.add_test("west", [[r], wl])
    TS.execute_log()


def test_rect_collision():
    vals = range(0, 200)
    r = Rect2(30, 30, 100, 100)
    pts = [(choice(vals), choice(vals)) for i in range(50)]

    w, h = 1100, 900
    app = PygameApplication("Test TextBox", w, h)
    game = app.get_game()
    display = app.display

    def draw_rect(r):
        # textbox.draw()
        p1 = r.p1
        p2 = r.p2
        p3 = r.p3
        p4 = r.p4
        game.draw.line(display, RED, p1, p2)
        game.draw.line(display, GREEN, p2, p3)
        game.draw.line(display, BLUE, p3, p4)
        game.draw.line(display, YELLOW_3, p4, p1)

        pa1 = r.max_encapsulating_rect.p1
        pa2 = r.max_encapsulating_rect.p2
        pa3 = r.max_encapsulating_rect.p3
        pa4 = r.max_encapsulating_rect.p4
        game.draw.line(display, ORANGE, pa1, pa2)
        game.draw.line(display, PURPLE, pa2, pa3)
        game.draw.line(display, ROYALBLUE, pa3, pa4)
        game.draw.line(display, TAN, pa4, pa1)

        pi1 = r.min_encapsulating_rect.p1
        pi2 = r.min_encapsulating_rect.p2
        pi3 = r.min_encapsulating_rect.p3
        pi4 = r.min_encapsulating_rect.p4
        game.draw.line(display, LIMEGREEN, pi1, pi2)
        game.draw.line(display, SKYBLUE, pi2, pi3)
        game.draw.line(display, WHITE, pi3, pi4)
        game.draw.line(display, BROWN_1, pi4, pi1)

    while app.is_playing:
        display.fill(BLACK)
        draw_rect(r)
        for pt in pts:
            if r.collide_point(*pt, strictly_inside=False):
                color = RED
            else:
                color = GREEN
            game.draw.circle(display, color, pt, 2)

        event_queue = app.run()
        for event in event_queue:
            pass
        app.clock.tick(25)

    p = pts[0]
    p = (85,85)
    print("p1:", p)
    print("r", r)
    print("r.top", r.top_line)
    print("r.left", r.left_line)
    print("r.bottom", r.bottom_line)
    print("r.right", r.right_line)
    print("(x, y) <= top:", p <= r.top_line)
    print("(x, y, 0) <= left:", (*p, 0) <= r.left_line)
    print("(x, y, 1) <= left:", (*p, 1) <= r.left_line)
    print("(x, y, 0) >= right:", (*p, 0) >= r.right_line)
    print("(x, y, 1) >= right:", (*p, 1) >= r.right_line)
    print("(x, y) >= bottom:", p >= r.bottom_line)
    print("r.collide_point(*p)", r.collide_point(*p))


def test_menubar():
    app = PygameApplication("Create Custom WO Update Queries", 1350, 500)
    game = app.get_game()
    display = app.display

    def open_file():
        print("open_file")
    def leaf1_func():
        print("leaf1_func")
    def leaf2_func():
        print("leaf2_func")
    def leaf3_func():
        print("leaf3_func")
    def leaf4_func():
        print("leaf4_func")
    def leaf5_func():
        print("leaf5_func")
    def leaf6_func():
        print("leaf6_func")
    def leaf7_func():
        print("leaf7_func")
    def leaf8_func():
        print("leaf8_func")
    def delete_func():
        print("delete_func")
    def filter_text():
        print("filter_text")

    x = 0
    y = 0
    w = 200
    h = 50
    button_data = {}
    bc = GRAY_69
    fs = 16
    bs = 1
    font = None
    menubar = MenuBar(game, display, x, y, w, h, {"file": {"open": open_file, "branch": {"leaf1": leaf1_func, "leaf2": leaf2_func}}, "edit": {"delete": delete_func}}, bc, fs, bs, font)
    menubar2 = MenuBar(game, display, 250, 50, w + 1, h + 1, {
        "file": {
            "open": open_file,
            "branch": {
                "leaf1": leaf1_func,
                "leaf2": leaf2_func
            }
        },
        "edit": {
            "delete": delete_func
        },
        "filter": {
            "by text": filter_text,
            "branch 1": {
                "v 1": leaf1_func,
                "branch 2": {
                    "branch 3": {
                        "v 3": leaf3_func,
                        "branch 4": {
                            "branch 5": {
                                "v 4": leaf4_func,
                                "v 5": leaf5_func,
                                "v 6": leaf6_func
                            },
                            "v 7": leaf7_func
                        },
                        "v 8": leaf8_func
                    }
                },
                "v 2": leaf1_func,
                "leaf2": leaf2_func
            }
        },
    }, bc, fs, bs, font)

    while app.is_playing:
        display.fill(BLACK)

        # draw widgets and objects here
        # menubar.draw()
        menubar2.draw()

        event_queue = app.run()
        for event in event_queue:

            # handle events

            pass

        app.clock.tick(30)


def test_listbox():
    app = PygameApplication("Testing ListBox Widgets", 750, 500)
    game = app.get_game()
    display = app.display

    x, y, w, h = 125, 40, 250, 400

    listbox1 = ListBox(game, display, x, y, w, h, title="ListBox 1", items=["Hey", "This", "is", "a", "listbox"])

    while app.is_playing:
        display.fill(BLACK)

        # draw widgets and objects here
        listbox1.draw()

        event_queue = app.run()
        for event in event_queue:

            # handle events

            pass

        app.clock.tick(30)


def test_hyperlink():
    app = PygameApplication("Create Custom WO Update Queries", 750, 500)
    game = app.get_game()
    display = app.display

    while app.is_playing:
        display.fill(BLACK)

        # draw widgets and objects here

        event_queue = app.run()
        for event in event_queue:

            # handle events

            pass

        app.clock.tick(30)


def test_scrollbar():
    app = PygameApplication("Create Custom WO Update Queries", 750, 500)
    game = app.get_game()
    display = app.display

    sbv = ScrollBar(game=pygame, display=display, x=10, y=10, w=300, h=300, bar_proportion=0.08, button_c=DARK_GRAY,
                    bar_background_c=LIGHT_GRAY, bar_c=BLUE, contents=None, content_c=RED, is_vertical=True)

    sbv.add_contents(1)

    while app.is_playing:
        display.fill(BLACK)

        # draw widgets and objects here
        sbv.draw()

        event_queue = app.run()
        for event in event_queue:

            # handle events

            pass

        app.clock.tick(30)



if __name__ == "__main__":
    # test_block_letters()
    # test_TextBox()
    # test_buttonbar()
    # test_phone_number()
    # test_reduce()
    # test_slider()
    # test_directions()
    # test_datestr_format([
    #     ("2021-08-01", "August 1st, 2021"),
    #     ("2021-08-02", "August 2nd, 2021"),
    #     ("2021-08-03", "August 3rd, 2021"),
    #     ("2021-08-04", "August 4th, 2021"),
    #     ("2021-08-05", "August 5th, 2021"),
    #     ("2021-08-08", "August 8th, 2021"),
    #     ("2021-08-10", "August 10th, 2021"),
    #     ("2021-08-31", "August 31st, 2021"),
    #     ("2021-08-21", "August 21st, 2021"),
    #     ("2021-08-11", "August 11th, 2021"),
    #     ("2021-08-12", "August 12th, 2021")
    # ])

    # test_money_str_format
    # test_find_north_side()
    # test_new_rect()
    # test_rect_collision()
    # test_menubar()
    # test_listbox()
    test_scrollbar()
    # test_hyperlink()

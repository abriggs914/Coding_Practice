import datetime
import json
import os
import random
import tkinter

import PyPDF2
# from camelot import core
# from camelot.core import TableList
# import camelot
# from camelot.core import TableList
# from PyPDF2 import PdfReader, SimplePDFViewer
# import pdfreader
# from pdfreader import SimplePDFViewer

import pandas

import datetime as dt
from random import sample
import tkinter_utility
from datetime_utility import first_of_week, first_of_day, first_of_month, date_suffix, date_str_format, is_date
from tkinter_utility import *
from tkinter import messagebox, font
from utility import *
from test_suite import *
from pygame_utility import *
from pyodbc_connection import connect
from grid_manager import GridManager
from theme_publisher import ThemePublisher

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

    r1 = Rect2(15, 20, 25, 30)
    r2 = Rect2(10, 10, w - 20, h - 20)
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


def test_TextBox():
    app = PygameApplication("Test TextBox", 600, 600)
    game = app.get_game()
    display = app.display
    r1 = Rect2(100, 25, 200, 100)
    r2 = Rect2(75, 210, 250, 200)
    # self, game, display, rect, ic, ac, f, fc, text = '', min_width = 20, numeric = False, char_limit = None, n_limit = None, bs = 1, border_style = None
    textbox1 = TextBox(game, display, r1, text="-1", numeric=True, daction=print_hi, dargs=None)
    textbox2 = TextBox(game, display, r2, text="-1", numeric=False, daction=print_hi, dargs=None)
    while app.is_playing:
        display.fill(BLACK)
        textbox1.draw()
        textbox2.draw()
        event_queue = app.run()
        for event in event_queue:
            textbox1.handle_event(event)
            textbox2.handle_event(event)


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
    # if 1 > new_rect.width_canvas:
    #     xp = 1.02
    #     new_rect.resize(Rect(new_rect.x, new_rect.y, 1, new_rect.height_canvas))
    #     # new_rect = box.rect_obj.scaled(xp, yp)
    #     print("\tA\t", new_rect, xp, yp)
    # if new_rect.width_canvas >= 600:
    #     xp = 0.99
    #     new_rect = box.rect_obj.scaled(xp, yp)
    #     print("\tB\t", new_rect, xp, yp)
    # if 1 > new_rect.height_canvas:
    #     yp = 1.02
    #     new_rect.resize(Rect(new_rect.x, new_rect.y, new_rect.width_canvas, 1))
    #     # new_rect = box.rect_obj.scaled(xp, yp)
    #     print("\tC\t", new_rect, xp, yp)
    # if new_rect.height_canvas >= 600:
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
#     if 1 > new_rect.width_canvas:
#         xp = 1.02
#         new_rect.resize(Rect(new_rect.x, new_rect.y, 1, new_rect.height_canvas))
#         # new_rect = box.rect_obj.scaled(xp, yp)
#         print("\tA\t", new_rect, xp, yp)
#     if new_rect.width_canvas >= 600:
#         xp = 0.99
#         new_rect = box.rect_obj.scaled(xp, yp)
#         print("\tB\t", new_rect, xp, yp)
#     if 1 > new_rect.height_canvas:
#         yp = 1.02
#         new_rect.resize(Rect(new_rect.x, new_rect.y, new_rect.width_canvas, 1))
#         # new_rect = box.rect_obj.scaled(xp, yp)
#         print("\tC\t", new_rect, xp, yp)
#     if new_rect.height_canvas >= 600:
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
    p = (85, 85)
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
    menubar = MenuBar(game, display, x, y, w, h,
                      {"file": {"open": open_file, "branch": {"leaf1": leaf1_func, "leaf2": leaf2_func}},
                       "edit": {"delete": delete_func}}, bc, fs, bs, font)
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


def test_random_date():
    dates = [random_date() for i in range(300)]
    for d in dates:
        print("D: {}".format(d))
        print("d: {}, parsed: {}".format(d, dt.date.fromisoformat(d)))

    calendar = set()
    while len(calendar) < (2026 - 1995) * 365:
        d = random_date(1995, 2026)
        calendar.add(d)

    calendar = list(calendar)
    calendar.sort()
    print("calendar: ", calendar)


def test_iscolour():
    TS = TestSuite()
    TS.set_func(iscolour)
    TS.add_test("Simple tuple", [[(238, 130, 238)], True])
    TS.add_test("Out of bounds tuple", [[(2138, 130, 238)], False])
    TS.add_test("Str of a tuple", [[str((238, 130, 238))], False])
    TS.add_test("Hex string 1", [["#AFAFAF"], True])
    TS.add_test("Hex string 2", [["AFAFAF"], True])
    TS.add_test("Hex string 3", [["AFAFAF#"], False])
    TS.add_test("Hex string 4", [["AFA#AF"], False])
    TS.add_test("Hex string 5", [["995842"], True])
    TS.add_test("Invalid Hex string 1", [["#gFAFAF"], False])
    TS.add_test("Invalid Hex string 2", [["##FAFAF"], False])
    TS.add_test("Invalid Hex string 3", [["#######"], False])
    TS.add_test("Invalid Hex string 4", [["123456#"], False])
    TS.execute_log()


def test_alert_colour():
    app = PygameApplication("Testing Alert Colour", 750, 500)
    game = app.get_game()
    display = app.display
    box_colour = GRAY_17
    min_n = 0
    max_n = 25

    start_c = FORESTGREEN
    end_c = AQUAMARINE_2
    print("start_c:", start_c)
    print("end_c:", end_c)

    def increment_colour():
        n = int(text_box.text)
        n += 1
        n = min(n, max_n)
        box_colour = gradient(n, max_n, start_c, end_c)
        text_box.set_text(str(n))
        box.bgc = box_colour
        print("bc:", box_colour)

    def decrement_colour():
        n = int(text_box.text)
        n -= 1
        n = max(min_n, n)
        box_colour = gradient(n, max_n, start_c, end_c)
        text_box.set_text(str(n))
        box.bgc = box_colour
        print("bc:", box_colour)

    box_colour = start_c
    text_box = TextBox(game, display, game.Rect(200, 0, 400, 100), text="0", editable=False, draw_clear_btn=False,
                       fs=35, text_align="center", numeric=True, iaction=increment_colour, daction=decrement_colour,
                       n_limit=range(10))
    box = Box(game, display, None, game.Rect(0, 100, 750, 200), 1, bgc=box_colour)

    def alert_colour_g(x, n):
        r1, g1, b1 = GREEN
        r2, g2, b2 = RED
        t_diff = (g1 - g2) + (r2 - r1)
        incs = t_diff / n
        p = x / n
        x = p * t_diff
        gp = 255 - min(255, x)
        rp = max(0, x - 255)
        return rp, gp, 0

    while app.is_playing:
        display.fill(BLACK)

        # draw widgets and objects here
        text_box.draw()
        box.draw()

        event_queue = app.run()
        for event in event_queue:
            # handle events
            text_box.handle_event(event)

        app.clock.tick(30)


def test_is_date():
    TS = TestSuite()
    TS.set_func(is_date)
    TS.add_test("Standard date string", [["2021-12-30"], True])
    TS.add_test("Invalid date string", [["2021-12-32"], False])
    TS.execute_log()


def test_date_manipulation():
    TS1 = TestSuite()
    TS1.set_func(first_of_day)
    TS1.add_test("2022-01-02", [[dt.datetime(2022, 1, 2, 12, 12)], dt.datetime(2022, 1, 2)])
    TS1.add_test("2022-01-31", [[dt.datetime(2022, 1, 31, 5, 30, 30)], dt.datetime(2022, 1, 31)])
    TS1.execute_log()

    TS2 = TestSuite()
    TS2.set_func(first_of_week)
    TS2.add_test("2022-01-02", [[dt.datetime(2022, 1, 2, 12, 12)], dt.datetime(2022, 1, 2, 12, 12)])
    TS2.add_test("2022-01-04", [[dt.datetime(2022, 1, 4, 12, 12)], dt.datetime(2022, 1, 2, 12, 12)])
    TS2.add_test("2022-01-31", [[dt.datetime(2022, 1, 31, 5, 30, 30)], dt.datetime(2022, 1, 30, 5, 30, 30)])
    TS2.execute_log()

    TS3 = TestSuite()
    TS3.set_func(first_of_month)
    TS3.add_test("2022-01-02", [[dt.datetime(2022, 1, 2, 12, 12)], dt.datetime(2022, 1, 1, 12, 12)])
    TS3.add_test("2022-01-31", [[dt.datetime(2022, 1, 31, 5, 30, 30)], dt.datetime(2022, 1, 1, 5, 30, 30)])
    TS3.execute_log()


def test_intersection():
    TS1 = TestSuite()
    evens = list(range(0, 25, 2))
    odds = list(range(1, 25, 2))
    by_3 = list(range(0, 25, 3))
    by_6 = list(range(0, 25, 6))
    by_4 = list(range(0, 25, 4))
    TS1.set_func(intersection)
    TS1.add_test("evens and odds", [[evens, odds], []])
    TS1.add_test("by 3s and by 6s", [[by_3, by_6], by_6])
    TS1.add_test("by 6s and by 4s", [[by_6, by_4], [i for i in range(0, 25, 1) if i % 4 == i % 6 == 0]])
    TS1.execute_log()


def test_line_inequality():
    line_1 = Line(0, 0, 0, 10)
    line_2 = Line(0, 0, 10, 0)
    line_3 = Line(0, 0, 10 ** 0.5, 10 ** 0.5)
    print(f"1: {line_1}, 2: {line_2}, 3: {line_3}")
    point = 8, 8
    print(f"line_1 < point: {line_1 < point}")
    print(f"line_1 <= point: {line_1 <= point}")
    print(f"line_1 > point: {line_1 > point}")
    print(f"line_1 >= point: {line_1 >= point}")
    print(f"line_1 == point: {line_1 == point}")

    print(f"line_2 < point: {line_2 < point}")
    print(f"line_2 <= point: {line_2 <= point}")
    print(f"line_2 > point: {line_2 > point}")
    print(f"line_2 >= point: {line_2 >= point}")
    print(f"line_2 == point: {line_2 == point}")

    print(f"line_3 < point: {line_3 < point}")
    print(f"line_3 <= point: {line_3 <= point}")
    print(f"line_3 > point: {line_3 > point}")
    print(f"line_3 >= point: {line_3 >= point}")
    print(f"line_3 == point: {line_3 == point}")


def test_lineSeg():
    line_1 = LineSeg(0, 0, 10, 0)
    print(f"collides: {line_1.collide_point(-5, 0)}")


def test_font_foreground():
    print(dict_print({
        "c1": {
            "colour": RED,
            "fc1": font_foreground(RED)
        },
        "c2": {
            "colour": rgb_to_hex(RED),
            "fc1": font_foreground(rgb_to_hex(RED))
        },
        "c3": {
            "colour": WHITE,
            "fc1": font_foreground(WHITE)
        }
    }))

    WIN = tkinter.Tk()
    WIN.geometry(f"500x500")
    slider_red = tkinter_utility.Slider(WIN, minimum=0, maximum=255)
    slider_green = tkinter_utility.Slider(WIN, minimum=0, maximum=255)
    slider_blue = tkinter_utility.Slider(WIN, minimum=0, maximum=255)
    tv_red = slider_red.value
    tv_green = slider_green.value
    tv_blue = slider_blue.value
    tv_label_red, label_red, tv_entry_red, entry_red = entry_factory(WIN, tv_label="Red:", tv_entry=tv_red)
    tv_label_green, label_green, tv_entry_green, entry_green = entry_factory(WIN, tv_label="Green:", tv_entry=tv_green)
    tv_label_blue, label_blue, tv_entry_blue, entry_blue = entry_factory(WIN, tv_label="Blue:", tv_entry=tv_blue)
    tv_label_res, label_res, tv_entry_res, entry_res = entry_factory(WIN, tv_label="Result:",
                                                                     tv_entry="Sample Text #123.")

    def update_colour(var_name, index, mode):
        r = tv_red.get()
        g = tv_green.get()
        b = tv_blue.get()
        c = Colour(r, g, b)
        h = c.hex_code
        entry_res.config(background=h, foreground=font_foreground(h, rgb=False))

    tv_red.trace_variable("w", update_colour)
    tv_green.trace_variable("w", update_colour)
    tv_blue.trace_variable("w", update_colour)

    label_red.grid(row=1, column=1)
    entry_red.grid(row=1, column=2)
    slider_red.grid(row=1, column=3)
    label_green.grid(row=2, column=1)
    entry_green.grid(row=2, column=2)
    slider_green.grid(row=2, column=3)
    label_blue.grid(row=3, column=1)
    entry_blue.grid(row=3, column=2)
    slider_blue.grid(row=3, column=3)
    label_res.grid(row=4, column=1)
    entry_res.grid(row=4, column=2)
    update_colour(None, None, None)
    WIN.mainloop()


def test_dict_print2():
    # Function returns a formatted string containing the contents of a dict object.
    # Special lines and line count for values that are lists.
    # Supports dictionaries with special value types.
    # Lists are printed line by line, but the counting index is constant for all elements. - Useful for ties.
    # Dicts are represented by a table which will dynamically generate a header and appropriately format cell values.
    # Strings, floats, ints, bools are simply converted to their string representations.
    # d					-	dict object.
    # n					-	Name of the dict, printed above the contents.
    # number			-	Decide whether to number the content lines.
    # l					-	Minimum number of chars in the content line.
    # 						Spaces between keys and values are populated by marker.
    # sep				-	Additional separation between keys and values.
    # marker			-	Char that separates the key and value of a content line.
    # sort_header		-	Will alphabetically sort the header line if any value is a
    #						dictionary. Only one level of nesting supported.
    # min_encapsulation	-	If a table is necessary because of a value that is a
    #						dictionary, then opt to keep all column widths as small as
    #						possible. This will most likely produce varying widths.
    # table_title		-	If a table is created, then display the title in the first
    #						column directly above the row names.
    # def dict_print2(d, n="Untitled", number=False, l=15, sep=5, marker=".", sort_header=False, min_encapsulation=True,
    #                table_title="", TAB="    ", SEPARATOR="  -  ", TABLE_DIVIDER="|"):
    #     if not d or not n or type(d) != dict:
    #         return "None"
    #     m = "\n{}--  ".format(TAB[:len(TAB) // 2]) + str(n).title() + "  --\n\n"
    #     fill = 0
    #
    #     # max_key = max([len(str(k)) + ((2 * len(k) + 2 + len(k) - 1) if type(k) == (list or tuple) else 0) for k in d.keys()])
    #     # max_val = max([max([len(str(v_elem)) for v_elem in v]) if type(v) == (list or tuple) else len(str(v)) if type(v) != dict else 0 for v in d.values()])
    #     # fill += sum([len(v) for v in d.values() if type(v) == (list or tuple)])
    #     # l = max(l, (max_key + max_val)) + sep
    #     # has_dict = [(k, v) for k, v in d.items() if type(v) == dict]
    #     # has_list = any([1 if type(v) in [list, tuple] else 0 for v in d.values()])
    #
    #     max_key = float("-inf")
    #     max_val = float("-inf")
    #     fill = float("-inf")
    #     l = float("-inf")
    #     has_dict = False
    #     has_list = False
    #
    #     for k, v in d.items():
    #         max_key = max((len(str(k)) + ((2 * len(k) + 2 + len(k) - 1) if type(k) == (list or tuple) else 0)), max_key)
    #         max_val = max((max([len(str(v_elem)) for v_elem in v] if v else [0]) if (
    #                 (type(v) == list) or (type(v) == tuple)) else len(
    #             str(v)) if type(v) != dict else 0), max_val)
    #
    #     l = max(len(table_title), max(l, (max_key + max_val))) + sep
    #     has_dict = [(k, v) for k, v in d.items() if type(v) == dict or (type(v) == list and v and type(v[0]) == dict)]
    #     has_list = any([1 if type(v) in [list, tuple] else 0 for v in d.values()])
    #
    #     header = []
    #     max_cell = 0
    #     max_cell_widths = []
    #
    #     # print("has_dict: {hd}".format(hd=has_dict))
    #     if has_list:
    #         number = True
    #     for k1, v in has_dict:
    #         for k2 in v:
    #             key = str(k2)
    #             # print("key: {k}".format(k=key))
    #             if key not in header:
    #                 if type(v) == dict:
    #                     # print("\t\tNew key: {k}".format(k=key))
    #                     header.append(key)
    #                     max_cell = max(max_cell, max(len(key), max([lenstr(value) for value in v.values()])))
    #                 # print("max_cell: {mc}".format(mc=max_cell))
    #                 elif type(k2) == dict:
    #                     strkeys = list(map(str, list(k2.keys())))
    #                     strvals = list(map(str, list(k2.values())))
    #                     header += [strkey for strkey in strkeys if strkey not in header]
    #                     max_cell = max(max_cell, max(list(map(len, strkeys))), max(list(map(len, strvals))))
    #                 else:
    #                     for lst in v:
    #                         a = max(list(map(lenstr, list(map(str, lst.keys())))))
    #                         b = max(list(map(lenstr, list(map(str, lst.values())))))
    #                         # print("a: {a}, b: {b}, values: {v}".format(a=a, b=b, v=lst.values()))
    #                         max_cell = max(max_cell, max(a, b))
    #
    #     max_cell += 2
    #
    #     # print("max_cell: {mc}".format(mc=max_cell))
    #     if sort_header:
    #         header.sort(key=lambda x: x.rjust(max_cell))
    #
    #     if min_encapsulation:
    #         for h in header:
    #             max_col_width = len(h) + 2
    #             # print("h: {h}, type(h): {th}".format(h=h, th=type(h)))
    #             for k, d_val in has_dict:
    #                 d_val = {str(d_val_k): str(d_val_v) for d_val_k, d_val_v in d_val.items()} if type(
    #                     d_val) == dict else d_val
    #                 # print("d_val: {dv},\thidv: {hidv},\tetdvlist: {etdvl}".format(dv=d_val, hidv=(h in d_val), etdvl=(type(d_val) == list)))
    #                 # print("k: {k}\nt(k): {tk}\nd: {d}\nt(d): {td}".format(k=k, tk=type(k), d=d_val, td=type(d_val)))
    #                 if h in d_val:
    #                     max_col_width = max(max_col_width, lenstr(d_val[h]) + 2)
    #                 elif type(d_val) == list:
    #                     max_col_width = max(max_col_width, max([max(
    #                         max(list(map(lenstr, [ek for ek in elem.keys() if ek == h]))),
    #                         max(list(map(lenstr, [ev for ek, ev in elem.items() if ek == h]))) + 2) for elem in d_val]))
    #             max_cell_widths.append(max_col_width)
    #
    #     # print("max_cell_widths: {mcw}".format(mcw=max_cell_widths))
    #     table_header = TABLE_DIVIDER + TABLE_DIVIDER.join(
    #         map(lambda x: pad_centre(str(x), max_cell), header)) + TABLE_DIVIDER
    #     empty_line = TABLE_DIVIDER + TABLE_DIVIDER.join(
    #         [pad_centre(" ", max_cell) for i in range(len(header))]) + TABLE_DIVIDER
    #
    #     if min_encapsulation:
    #         table_header = TABLE_DIVIDER + TABLE_DIVIDER.join(
    #             [pad_centre(str(h), max_cell_widths[i]) for i, h in enumerate(header)]) + TABLE_DIVIDER
    #         empty_line = TABLE_DIVIDER + TABLE_DIVIDER.join(
    #             [pad_centre(" ", max_cell_widths[i]) for i in range(len(header))]) + TABLE_DIVIDER
    #     else:
    #         max_cell_widths = [max_cell for i in range(len(header))]
    #
    #     # print("Header: {h}\nTable Header: {th}".format(h=header, th=table_header))
    #     fill = "".join([" " for i in range(len(str(fill + len(d))))])
    #     table_width = l + len(fill) + len(SEPARATOR) + len(TAB) + len(table_header) - (4 * len(TABLE_DIVIDER))
    #     table_tab = "".join([marker for i in range(len(TAB))])
    #     if has_dict:
    #         table_header_title = pad_centre(table_title, l + len(SEPARATOR) - 1)
    #         m += TAB
    #         m += "" if not number else fill + SEPARATOR
    #         m += table_header_title + table_header.rjust(
    #             table_width - len(table_header_title) - len(fill) - len(SEPARATOR)) + "\n"
    #     i = 0
    #     # print("FINAL L: {l}\nFill: {n}<{f}>".format(l=l, n=len(fill), f=fill))
    #     for k, v in d.items():
    #         if type(v) not in [list, tuple]:
    #             v = [v]
    #         for j, v_elem in enumerate(v):
    #             ml = str(k).strip()
    #             orig_ml = ml
    #             num = str(i + 1)
    #             if number:
    #                 ml = fill + SEPARATOR + ml
    #                 if j == 0:
    #                     ml = num.ljust(len(fill)) + ml[len(fill):]
    #             v_val = v_elem
    #             if has_dict and type(v_elem) == dict:
    #                 v_val = ""
    #             ml += str(v_val).rjust(l - len(orig_ml), marker)
    #             if has_dict:
    #                 ml += table_tab
    #                 if type(v_elem) == dict:
    #                     keys = {str(k).strip(): v for k, v in v_elem.items()}
    #                     vals = [keys[key] if key in keys else "" for key in header]
    #                     ml += TABLE_DIVIDER + TABLE_DIVIDER.join(
    #                         pad_centre(str(cell), max_cell_widths[i]) for i, cell in enumerate(vals)) + TABLE_DIVIDER
    #                 else:
    #                     ml += empty_line
    #             ml += "\n"
    #             m += TAB + ml
    #             i += 1
    #     return m

    d1 = {
        'Item_01': [
            '1',
            2,
            False,
            {},
            datetime.datetime(2022, 5, 29, 5, 47)
        ],
        'Item_02': {
            '1': 1,
            '2': 2,
            '3': 3
        }
    }
    d2 = pandas.DataFrame()

    def dict_print2(d_obj, name="Untitled"):
        if type(d_obj) not in (list, tuple, dict, pandas.DataFrame):
            print("NOT A VALID TYPE")
            return None

    print(dict_print2(d1))
    print(dict_print2(d2))


def test_rainbow_gradient():
    app = PygameApplication("Testing Rainbow Gradient", 750, 500)
    game = app.get_game()
    display = app.display
    box_colour = GRAY_17
    min_n = 0
    max_n = 25

    start_c = FORESTGREEN
    end_c = AQUAMARINE_2
    print("start_c:", start_c)
    print("end_c:", end_c)

    # def rainbow_gradient(n_slices):
    #     values = [(255, i, 0) for i in range(256)] +\
    #              [(i, 255, 0) for i in range(255, -1, -1)] +\
    #              [(0, 255, i) for i in range(255)] +\
    #              [(0, i, 255) for i in range(255, -1, -1)] +\
    #              [(i, 0, 255) for i in range(256)] +\
    #              [(255, 0, i) for i in range(255, -1, -1)]
    #     print(f"len(values): {len(values)}")
    #     l = len(values)
    #     if isinstance(n_slices, int):
    #         p = min(l, n_slices) / (l if l != 0 else 1)
    #     elif isinstance(n_slices, float):
    #         p = max(0, min(1, n_slices))
    #     else:
    #         raise TypeError(f"Param 'n_slice' not recognized: <{type(n_slices)}>")
    #     values = reduce(values, p, how="distribute")
    #     for val in values:
    #         yield val

    # def increment_colour():
    #     n = int(text_box.text)
    #     n += 1
    #     n = min(n, max_n)
    #     box_colour = gradient(n, max_n, start_c, end_c)
    #     text_box.set_text(str(n))
    #     box.bgc = box_colour
    #     print("bc:", box_colour)
    #
    # def decrement_colour():
    #     n = int(text_box.text)
    #     n -= 1
    #     n = max(min_n, n)
    #     box_colour = gradient(n, max_n, start_c, end_c)
    #     text_box.set_text(str(n))
    #     box.bgc = box_colour
    #     print("bc:", box_colour)

    box_colour = start_c
    # text_box = TextBox(game, display, game.Rect(200, 0, 400, 100), text="0", editable=False, draw_clear_btn=False, fs=35, text_align="center", numeric=True, iaction=increment_colour, daction=decrement_colour, n_limit=range(10))
    box = Box(game, display, None, game.Rect(0, 100, 750, 200), 1, bgc=box_colour)

    def alert_colour_g(x, n):
        r1, g1, b1 = GREEN
        r2, g2, b2 = RED
        t_diff = (g1 - g2) + (r2 - r1)
        incs = t_diff / n
        p = x / n
        x = p * t_diff
        gp = 255 - min(255, x)
        rp = max(0, x - 255)
        return rp, gp, 0

    rainbow = rainbow_gradient(100)

    while app.is_playing:
        display.fill(BLACK)

        # draw widgets and objects here
        # text_box.draw()
        box.draw()

        try:
            box.bgc = rainbow.__next__()
        except StopIteration:
            rainbow = rainbow_gradient(100)

        event_queue = app.run()
        for event in event_queue:
            # handle events
            pass
            # text_box.handle_event(event)

        app.clock.tick(30)


def test_pyodbc_connection():
    ts = TestSuite(name="pyodbcConnection Tests", test_func=connect)
    ts.add_test("Test1", [["SELECT * FROM [IT Requests]"], pandas.DataFrame()])
    ts.add_test("Test2",
                [["SELECT * FROM [IT Requests]", "{SQL Server}", "server3", "BWSdb", "user5", None, False, False],
                 ValueError])
    ts.execute_log()


def test_NATO_phonetic_alphabet():
    ts = TestSuite(name="pyodbcConnection Tests", test_func=translate_NATO_phonetic_alphabet)
    ts.add_test("Test1", [["Avery"], "Alpha Victor Echo Romeo Yankee"])
    ts.add_test("Test2", [["Avery is #1", True, False], "Alpha Victor Echo Romeo Yankee India Sierra # 1"])
    ts.add_test("Test3", [["Avery is #1"], "Alpha Victor Echo Romeo Yankee   India Sierra   # 1"])
    ts.add_test("Test4", [["Alpha Victor Echo Romeo Yankee", False], "avery"])
    ts.add_test("Test5", [["Avery!"], "Alpha Victor Echo Romeo Yankee !"])
    ts.add_test("Test6", [["Alpha Victor Echo Romeo Yankee!", False], "avery!"])
    ts.add_test("Test7", [["Alpha Victor Echo Romeo Yankee   India Sierra   # 1", False, False], "avery is #1"])
    ts.add_test("Test8", [["GRV-051"], "Golf Romeo Victor - 0 5 1"])
    ts.execute_log()


def test_grid_cells():
    # finite space width_canvas height_canvas (w x h), want (n x m) rows by columns, allowing for x, and y padding, r_type list or dict

    TS = TestSuite(test_func=grid_cells, name="'grid_cells' TestSuite")
    call_args = [
        ((500, 500, 10, 10, 1, 1), []),
        ((500, 10), []),
        ((500, "50"), []),
        (("500", "50"), []),
        ((500, 500, "10", 10, -1, 18), AssertionError),
        ((-500, 500, "10", 10, 1, -18), AssertionError),
        ((500, -500, "-10", 10, 1, 18), AssertionError),
        (("100", "2"), [
            [
                [0.5, 0.5, 49.5, 49.5],
                [50.5, 0.5, 99.5, 49.5]
            ],
            [
                [0.5, 50.5, 49.5, 99.5],
                [50.5, 50.5, 99.5, 99.5]
            ]
        ]),
        (("100", "4"), [
            [
                [0.5, 0.5, 24.5, 24.5],
                [25.5, 0.5, 49.5, 24.5],
                [50.5, 0.5, 74.5, 24.5],
                [75.5, 0.5, 99.5, 24.5]
            ],
            [
                [0.5, 25.5, 24.5, 49.5],
                [25.5, 25.5, 49.5, 49.5],
                [50.5, 25.5, 74.5, 49.5],
                [75.5, 25.5, 99.5, 49.5]
            ],
            [
                [0.5, 50.5, 24.5, 74.5],
                [25.5, 50.5, 49.5, 74.5],
                [50.5, 50.5, 74.5, 74.5],
                [75.5, 50.5, 99.5, 74.5]
            ],
            [
                [0.5, 75.5, 24.5, 99.5],
                [25.5, 75.5, 49.5, 99.5],
                [50.5, 75.5, 74.5, 99.5],
                [75.5, 75.5, 99.5, 99.5]
            ],
        ]),
        (("100", 2, "100", 2, 1, 1, 0, 0, dict), {
            0: {
                0: {"x_1": 0.5, "y_1": 0.5, "x_2": 49.5, "y_2": 49.5, "w": 49.0, "h": 49.0},
                1: {"x_1": 50.5, "y_1": 0.5, "x_2": 99.5, "y_2": 49.5, "w": 49.0, "h": 49.0}
            },
            1: {
                0: {"x_1": 0.5, "y_1": 50.5, "x_2": 49.5, "y_2": 99.5, "w": 49.0, "h": 49.0},
                1: {"x_1": 50.5, "y_1": 50.5, "x_2": 99.5, "y_2": 99.5, "w": 49.0, "h": 49.0}
            }
        }),
    ]
    for i, call_arg in enumerate(call_args):
        args, ans = call_arg
        test_args = [[*args], ans]
        print(f"{call_arg=}, {args=}, {ans=}, {test_args=}")
        TS.add_test(f"Test_{i + 1}", test_args)
        # grid_cells(*call_arg)

    TS.execute_log()

    WIN = tkinter.Tk()
    WIN.geometry(f"500x500")

    canvas = tkinter.Canvas(WIN, width=100, height=100, background=rgb_to_hex(FIREBRICK_3))
    canvas_2 = tkinter.Canvas(WIN, width=100, height=100, background=rgb_to_hex(OLDLACE))
    cell_dims = grid_cells("100", 1, x_pad=25, y_pad=25)

    dims_2 = [
        [
            [0.5, 0.5, 24.5, 24.5],
            [25.5, 0.5, 49.5, 24.5],
            [50.5, 0.5, 74.5, 24.5],
            [75.5, 0.5, 99.5, 24.5]
        ],
        [
            [0.5, 25.5, 24.5, 49.5],
            [25.5, 25.5, 49.5, 49.5],
            [50.5, 25.5, 74.5, 49.5],
            [75.5, 25.5, 99.5, 49.5]
        ],
        [
            [0.5, 50.5, 24.5, 74.5],
            [25.5, 50.5, 49.5, 74.5],
            [50.5, 50.5, 74.5, 74.5],
            [75.5, 50.5, 99.5, 74.5]
        ],
        [
            [0.5, 74.5, 24.5, 99.5],
            [25.5, 74.5, 49.5, 99.5],
            [50.5, 74.5, 74.5, 99.5],
            [75.5, 74.5, 99.5, 99.5]
        ],
    ]

    for row in cell_dims:
        for dim in row:
            canvas.create_rectangle(*dim, fill=rgb_to_hex(random_colour()))

    for row in dims_2:
        for dim in row:
            canvas_2.create_rectangle(*dim, fill=rgb_to_hex(random_colour()))

    canvas.grid(row=1, column=1)
    canvas_2.grid(row=2, column=2)
    WIN.mainloop()


def test_rect_bounds():
    TS = TestSuite(test_func=clamp_rect, name="'clamp_rect' TestSuite")
    call_args = [
        ([[20, 20, 50, 50], [0, 0, 100, 100]], [20, 20, 50, 50]),
        ([[20, 20, 50, 50], [25, 25, 100, 100], True], [25, 25, 55, 55]),
        ([[20, 20, 50, 50], [25, 25, 100, 100], False], [25, 25, 55, 55]),
        ([Rect2(20, 20, 30, 30), Rect2(0, 0, 100, 100)], [20, 20, 50, 50]),
        ([Rect2(20, 20, 30, 30), Rect2(25, 25, 75, 75), True], [25, 25, 55, 55]),
        ([Rect2(20, 20, 30, 30), Rect2(25, 25, 75, 75), False], [25, 25, 55, 55]),
        ([[20, 20, 500, 500], [25, 25, 100, 100], False], [25, 25, 100, 100]),
        ([[20, 20, 500, 500], Rect2(25, 25, 100, 100), False], [25, 25, 125, 125]),
        ([[20, 20, 50, 50], [0, 0, 40, 40], False], [20, 20, 40, 40]),

        ([[20, 20, 500, 500], [25, 25, 100, 100], True], [25, 25, 100, 100]),
        ([Rect2(20, 20, 500, 500), [25, 25, 100, 100], True], [25, 25, 100, 100]),
        ([[20, 20, 50, 50], [0, 0, 40, 40], True], [10, 10, 40, 40]),
        ([[0, 0, 5, 5], [10, 10, 40, 40]], [10, 10, 15, 15])
    ]
    for i, call_arg in enumerate(call_args):
        args, ans = call_arg
        test_args = [[*args], ans]
        print(f"{call_arg=}, {args=}, {ans=}, {test_args=}")
        TS.add_test(f"Test_{i + 1}", test_args)
        # grid_cells(*call_arg)

    TS.execute_log()

    class App(tkinter.Tk):

        def __init__(self):
            super(App, self).__init__()
            self.WIDTH, self.HEIGHT = 500, 500
            self.geometry("500x500")
            self.title("App")

            self.app_state = "idle"
            self.c_width, self.c_height = 400, 400
            self.canvas = tkinter.Canvas(self, width=self.c_width, height=self.c_height, background=rgb_to_hex(KHAKI_4))
            self.r_width, self.r_height = 100, 100
            self.rect_bounds = [((self.c_width - self.r_width) / 2), ((self.c_height - self.r_height) / 2),
                                ((self.c_width + self.r_width) / 2), ((self.c_height + self.r_height) / 2)]
            self.tag_rect = self.canvas.create_rectangle(*self.rect_bounds, fill=random_colour(rgb=False))

            self.canvas.tag_bind(self.tag_rect, "<Button-1>", self.click_canvas)
            self.canvas.tag_bind(self.tag_rect, "<Motion>", self.motion_canvas)
            self.canvas.tag_bind(self.tag_rect, "<ButtonRelease-1>", self.release_canvas)
            self.canvas.grid()

        def click_canvas(self, event):
            self.app_state = "dragging"

        def motion_canvas(self, event):
            if self.app_state == "dragging":
                # xy = self.winfo_pointerxy()
                cx, cy = event.x, event.y
                # cx, cy = xy
                # cx, cy = self.canvas.canvasx(cx), self.canvas.canvasy(cy)
                # print(f"{cx=}, {cy=}")
                new_rect = [cx - (self.r_width / 2), cy - (self.r_height / 2), cx + (self.r_width / 2),
                            cy + (self.r_height / 2)]
                new_rect = clamp_rect(
                    new_rect, [0, 0, self.c_width, self.c_height], maintain_inner_dims=True
                )
                nx1, ny1, nx2, ny2 = new_rect
                self.canvas.moveto(self.tag_rect, nx1, ny1)
                # self.canvas.moveto(self.tag_rect, cx, cy)
                # self.canvas.itemconfigure(self.tag_rect, x0=nx1, y0=ny1, x1=nx2, y1=ny2)

        def release_canvas(self, event):
            self.app_state = "idle"

    App().mainloop()


def test_colourify():
    colours = [
        c1 := Colour(10, 20, 30),
        c2 := Colour((10, 20, 30)),
        c3 := Colour("red"),
        c4 := Colour("RED_1__RED_"),
        # c5 := Colour("red2"),
        c6 := Colour("#ff0000", colour_name="red2"),
        c7 := Colour("#145172", colour_name="new_blue_colour")
    ]
    for colour in colours:
        print(f"{colour=}")

    print(f"{c4=}, {c6=}, {c4 == c6=}")
    print(f"{c1=}, {c2=}, {c1 == c2=}")

    # TS = TestZSuite(test_func=Colour, name="'colourify' TestSuite")
    # call_args = [
    #     ((10, 20, 30), True)
    # ]
    # for i, call_arg in enumerate(call_args):
    #     args, ans = call_arg
    #     test_args = [[*args], ans]
    #     print(f"{call_arg=}, {args=}, {ans=}, {test_args=}")
    #     TS.add_test(f"Test_{i + 1}", test_args)
    #
    # TS.execute_log()


def test_rgb_slider():
    WIN = tkinter.Tk()
    WIN.geometry(f"500x500")

    rgb_slider = RGBSlider(WIN)
    rgb_slider.pack()
    WIN.mainloop()


def test_theme_publisher():
    ThemePublisher().mainloop()


def test_tk_slider():
    WIN = tkinter.Tk()
    WIN.geometry(f"500x500")

    slider_1 = tkinter_utility.Slider(WIN, label_text="Slider 1")
    slider_1.pack()

    slider_2 = tkinter_utility.Slider(WIN, label_text="Slider 2", minimum=-500, maximum=-250)
    slider_2.pack()

    slider_3 = tkinter_utility.Slider(WIN, label_text="Slider 3", minimum=3000, maximum=10000)
    slider_3.pack()

    WIN.mainloop()


def test_alpha_seq():
    result = set()
    # namer = alpha_seq(n_digits=3, prefix="frame_")
    namer = alpha_seq(n_digits=3, prefix="frame_", pad_0=True, pad_char="_")
    # namer = alpha_seq(n_digits=2, prefix="frame_", numbers_instead=True)
    # for i in range(11):
    # for i in range(27):
    for i in range(100):
        res = next(namer)
        print(f"{str(i).ljust(3)=} | {res}")
        if res in result:
            raise ValueError(f"Error. {i=}, '{res}' already calculated.")
        result.add(res)

    # TS = TestSuite(name="AlpaSeq", test_func=alpha_seq)
    # TS.add_test("t1", [[], ])
    # TS.execute_log()


def test_grid_manager():
    WIN = tkinter.Tk()
    WIN.title("test_grid_manager")
    WIDTH, HEIGHT = 900, 600
    WIN.geometry(f"{WIDTH}x{HEIGHT}")

    namer = alpha_seq(100, prefix="frame_", capital_alpha=False)

    widgets_1 = [
        [
            tkinter.Canvas(WIN, name=next(namer), background=random_colour(rgb=False), width=50, height=50),
            tkinter.Canvas(WIN, name=next(namer), background=random_colour(rgb=False), width=50, height=50),
            tkinter.Canvas(WIN, name=next(namer), background=random_colour(rgb=False), width=50, height=50)
        ],
        [
            tkinter.Canvas(WIN, name=next(namer), background=random_colour(rgb=False), width=50, height=50),
            {
                "widget":
                    tkinter.Canvas(WIN, name=next(namer), background=random_colour(rgb=False), width=50, height=50),
                "columnspan": 3,
                "sticky": "ew"
            }
        ],
        [
            {
                "widget": tkinter.Canvas(WIN, name=next(namer), background=random_colour(rgb=False), width=50,
                                         height=50),
                "columnspan": 2,
                "rowspan": 2,
                "sticky": "ew"
                # "padx": 45,
                # "pady": 45
            },
            {
                "widget": tkinter.Canvas(WIN, name=next(namer), background=random_colour(rgb=False), width=50,
                                         height=50),
                "columnspan": 2,
                "sticky": "ew"
            }
        ],
        [
            tkinter.Canvas(WIN, name=next(namer), background=random_colour(rgb=False), width=50, height=50),
            tkinter.Canvas(WIN, name=next(namer), background=random_colour(rgb=False), width=50, height=50),
            tkinter.Canvas(WIN, name=next(namer), background=random_colour(rgb=False), width=50, height=50)
        ],
        [None, None, None,
         tkinter.Canvas(WIN, name=next(namer), background=random_colour(rgb=False), width=50, height=50)],
        [None,
         {"widget": tkinter.Canvas(WIN, name=next(namer), background=random_colour(rgb=False), width=50, height=50),
          "ipadx": 20, "ipady": 20}]

    ]

    widgets_2 = [
        [
            tkinter.Canvas(WIN, name=next(namer), background=random_colour(rgb=False), width=50, height=50),
            tkinter.Canvas(WIN, name=next(namer), background=random_colour(rgb=False), width=50, height=50),
            tkinter.Canvas(WIN, name=next(namer), background=random_colour(rgb=False), width=50, height=50)
        ],
        [
            tkinter.Canvas(WIN, name=next(namer), background=random_colour(rgb=False), width=50, height=50),
            tkinter.Canvas(WIN, name=next(namer), background=random_colour(rgb=False), width=50, height=50)
        ],
        [
            {
                "widget": tkinter.Canvas(WIN, name=next(namer), background=random_colour(rgb=False), width=50,
                                         height=50),
                "columnspan": 2
            },
            tkinter.Canvas(WIN, name=next(namer), background=random_colour(rgb=False), width=50, height=50)
        ]
    ]

    WIN.grid()
    gm = GridManager()
    gm.grid_widgets(widgets_1)
    gm.grid_widgets(widgets_2)

    # grid_manage_1(widgets_1)
    # grid_manage_1(widgets_2)
    WIN.update()

    WIN.after(5000, gm.ungrid_widget(0, 0))

    WIN.mainloop()

    # def grid_manage_1(widgets):
    #     valid_keys = {"widget", "columnspan", "rowspan", "padx", "pady",  "ipadx", "ipady", "sticky"}
    #     r_len = len(widgets)
    #     row_count = 0
    #     for r, row in enumerate(widgets):
    #         ri = r + 0 + row_count
    #         c_len = len(row)
    #         col_count = 0
    #         ci = 0
    #         r_inner = 0
    #         for c, widget in enumerate(row):
    #             if isinstance(widget, dict):
    #                 assert "widget" in widget, "Error, key 'widget' not passed."
    #                 widget_keys = set(widget.keys())
    #                 diff = widget_keys.difference(valid_keys)
    #                 assert "row" not in diff, f"Error, key 'row' is illegal. Use position in a 2D list to indicate row."
    #                 assert "column" not in diff, f"Error, key 'column' is illegal. Use position in a 2D list to indicate column."
    #                 assert not diff, f"Error, key(s): '{diff}' are illegal."
    #                 cs = widget.get("columnspan", 1)
    #                 rs = widget.get("rowspan", 1)
    #                 xp = widget.get("padx", None)
    #                 yp = widget.get("pady", None)
    #                 ixp = widget.get("ipadx", None)
    #                 iyp = widget.get("ipady", None)
    #                 st = widget.get("sticky", None)
    #                 args = {}
    #                 if cs:
    #                     args["columnspan"] = cs
    #                 if rs:
    #                     args["rowspan"] = rs
    #                 if xp:
    #                     args["padx"] = xp
    #                 if yp:
    #                     args["pady"] = yp
    #                 if ixp:
    #                     args["ipadx"] = ixp
    #                 if iyp:
    #                     args["ipady"] = iyp
    #                 if st:
    #                     args["sticky"] = st
    #                 print(f"gridding widget={widget['widget']}, {r=}, {c=}, {ri=}, {ci=}, {args=}")
    #                 widget["widget"].grid(row=ri, column=ci, **args)
    #                 col_count += cs
    #                 r_inner = max(r_inner, (rs - 1))
    #                 ci += (col_count - 1)
    #
    #                 x, y = 25, 25
    #                 widget["widget"].create_text(x, y, text=str(widget))
    #                 widget["widget"].create_text(x, y+10, text=str(ri))
    #                 widget["widget"].create_text(x, y+20, text=str(ci))
    #             else:
    #                 print(f"gridding widget={widget}, {r=}, {c=}, {ri=}, {ci=}")
    #                 widget.grid(row=ri, column=ci)
    #
    #                 x, y = 25, 25
    #                 widget.create_text(x, y, text=str(widget))
    #                 widget.create_text(x, y + 10, text=str(ri))
    #                 widget.create_text(x, y + 20, text=str(ci))
    #             ci += 1
    #         print(f"{r_inner=}")
    #         row_count += r_inner
    #
    # WIN = tkinter.Tk()
    # WIN.title("test_grid_manager")
    # WIDTH, HEIGHT = 900, 600
    # WIN.geometry(f"{WIDTH}x{HEIGHT}")
    #
    # namer = alpha_seq(100, prefix="frame_", capital_alpha=False)
    #
    # widgets_1 = [
    #     [
    #         tkinter.Canvas(WIN, name=next(namer), background=random_colour(rgb=False), width_canvas=50, height_canvas=50),
    #         tkinter.Canvas(WIN, name=next(namer), background=random_colour(rgb=False), width_canvas=50, height_canvas=50),
    #         tkinter.Canvas(WIN, name=next(namer), background=random_colour(rgb=False), width_canvas=50, height_canvas=50)
    #     ],
    #     [
    #         tkinter.Canvas(WIN, name=next(namer), background=random_colour(rgb=False), width_canvas=50, height_canvas=50),
    #         tkinter.Canvas(WIN, name=next(namer), background=random_colour(rgb=False), width_canvas=50, height_canvas=50)
    #     ],
    #     [
    #         {
    #             "widget": tkinter.Canvas(WIN, name=next(namer), background=random_colour(rgb=False), width_canvas=50, height_canvas=50),
    #             "columnspan": 2,
    #             "rowspan": 2,
    #             "sticky": "ew",
    #             # "padx": 45,
    #             # "pady": 45
    #         },
    #         tkinter.Canvas(WIN, name=next(namer), background=random_colour(rgb=False), width_canvas=50, height_canvas=50)
    #     ],
    #     [
    #         tkinter.Canvas(WIN, name=next(namer), background=random_colour(rgb=False), width_canvas=50, height_canvas=50),
    #         tkinter.Canvas(WIN, name=next(namer), background=random_colour(rgb=False), width_canvas=50, height_canvas=50),
    #         tkinter.Canvas(WIN, name=next(namer), background=random_colour(rgb=False), width_canvas=50, height_canvas=50)
    #     ]
    #
    # ]
    #
    # widgets_2 = [
    #     [
    #         tkinter.Canvas(WIN, name=next(namer), background=random_colour(rgb=False), width_canvas=50, height_canvas=50),
    #         tkinter.Canvas(WIN, name=next(namer), background=random_colour(rgb=False), width_canvas=50, height_canvas=50),
    #         tkinter.Canvas(WIN, name=next(namer), background=random_colour(rgb=False), width_canvas=50, height_canvas=50)
    #     ],
    #     [
    #         tkinter.Canvas(WIN, name=next(namer), background=random_colour(rgb=False), width_canvas=50, height_canvas=50),
    #         tkinter.Canvas(WIN, name=next(namer), background=random_colour(rgb=False), width_canvas=50, height_canvas=50)
    #     ],
    #     [
    #         {
    #             "widget": tkinter.Canvas(WIN, name=next(namer), background=random_colour(rgb=False), width_canvas=50, height_canvas=50),
    #             "columnspan": 2
    #         },
    #         tkinter.Canvas(WIN, name=next(namer), background=random_colour(rgb=False), width_canvas=50, height_canvas=50)
    #     ]
    # ]
    #
    # WIN.grid()
    # grid_manage_1(widgets_1)
    # # grid_manage_1(widgets_2)
    # WIN.update()
    #
    # # for r, row in enumerate(widgets_1):
    # #     for c, widget in enumerate(row):
    # #         if isinstance(widget, dict):
    # #             widget = widget["widget"]
    # #         bbox = WIN.bbox(widget)
    # #         # bbox = widget.winfo_x(), widget.winfo_y(), widget.winfo_width(), widget.winfo_height()
    # #         # print(f"{bbox=}")
    # #         x, y = bbox[0] + (bbox[2] / 2), bbox[1] + (bbox[3] / 2)
    # #         print(f"\t{widget=}, {x=}, {y=}, {widget.winfo_x()=}, {widget.winfo_y()=}, {widget.winfo_width()=}, {widget.winfo_height()=}")
    # #         # widget.create_text(bbox[0] + (bbox[2] / 2), bbox[1] + (bbox[3] / 2), text=str(widget))
    # #         x, y = 25, 25
    # #         widget.create_text(x, y, text=str(widget))
    # #         widget.create_text(x, y+10, text=str(r))
    # #         widget.create_text(x, y+20, text=str(c))
    #
    # WIN.update()
    #
    # WIN.mainloop()


def test_margins():
    def margins1(t_width, n_btns, btn_width):
        mw = (t_width - (n_btns * btn_width)) / (n_btns + 1)

        for i in range(n_btns + 1):
            a, b = i * btn_width, (i + 1) * mw
            print(f"{a=}, {b=}")

        # return flatten([0] + [[(i + 1) * mw, i * btn_width] for i in range(n_btns)] + [t_width])
        # return flatten([[
        #     ((i if i <= 1 else (i)) * (mw)) + (i * btn_width),
        #     ((i if i <= 1 else (i)) * (btn_width)) + ((i + 1) * mw)
        # ] for i in range(n_btns + 1)])
        return flatten([[
            i * (mw + btn_width),
            (i * btn_width) + ((i + 1) * mw)
        ] for i in range(n_btns + 1)])

    # m1 = margins()
    print(margins(600, 3, 100))
    print(margins(600, 1, 200))


def test_is_number():
    def is_number(x):
        if isinstance(x, (int, float, complex, Decimal, Fraction)) or pd.api.types.is_numeric_dtype(x):
            return True
        xs = str(x)
        if xs.count(".") < 2 and xs.count("-") < 2:
            return xs.replace(".", "").removeprefix("-").isnumeric()
        return False

    print("\nALL VALID")
    for v in [1, 6j, float("inf"), 1 / 8, "25.2", "-2", "-12.24", 4e3, ".125", "125."]:
        print(f"{v=}, {is_number(v)=}")
    print("\nALL INVALID")
    for v in [Foo(), "16.16.2", "-16.25j", "-16.25x", dict(), list(), "0-", "-g."]:
        print(f"{v=}, {is_number(v)=}")


def test_spread():
    # ss =
    # i = 0
    # x = ((ll - 1) - 2)
    # result = [lst[0]]
    # print(f"{x=}")
    # while i < x:
    #     a = lst[i]
    #     b = lst[i + 1]
    #     is_num_a = isnumber(a)
    #     is_num_b = isnumber(b)
    #     is_num = is_num_a and is_num_b
    #     if filler is None:
    #         if is_num:
    #             d = b - a
    #             result.append(a + (d / 2))
    #         else:
    #             result.append(filler)
    #     else:
    #         result.append(filler)
    #
    #     i += 1
    # result.append(lst[-1])
    # return result

    # print(f"{spread([1,2,3], 6)}")
    # print(f"{spread([1,'2',3], 6)}")
    # print(f"{spread([1,'_2',3], 6)}")
    print(f"{spread([1, '_2', 3], 6, how='exact')}")
    print(f"{spread([5, 6, 7, 9, 14, 18, 22, 25, 116, 130, 200, 205, 206, 306, 307], 21, how='exact')}")


def test_pdf():
    # import tabula
    # import pandas as pd
    # df = tabula.read_pdf(r"C:\Users\ABriggs\Downloads\2023-04 LASER AMP 244246 PO 140194 POSTED.pdf", pages='all')
    # print(f"DF: {df}")

    import PyPDF2

    fn = r"C:\Users\ABriggs\Downloads\2023-04 LASER AMP 244246 PO 140194 POSTED.pdf"

    # open the PDF file in binary mode
    with open(fn, 'rb') as f:
        # create a PDF reader object
        pdf_reader = PyPDF2.PdfFileReader(f)
        # pdf_reader = PdfReader(f)
        # read each page of the PDF file
        text = ''
        for page_num in range(pdf_reader.numPages):
            page = pdf_reader.getPage(page_num)
            # extract text from the page
            page_text = page.extractText()
            # append the text from this page to the overall text
            text += page_text

    values = text.split("Price Montant")[-1]
    values = values.split("amount")[-1].split("SOUS-TOTAL")[0]
    rows = values.split("\n")
    columns = [
        "Qté /qty",
        "Numéro de pièce / Part Number",
        "Rev.",
        "Prix /Price",
        "Montant / amount"
    ]
    print(f"{values=}")
    for row in rows:
        if row:
            vals = row.split(" ")
            qty_part_number, rev, price, amount = vals
            part_number = qty_part_number.split("-")[-1]
            idx = qty_part_number.index("-")
            part_number = f"{qty_part_number[idx - 5:idx]}-{part_number}"
            qty = int(qty_part_number[:idx][:-5])
            print(f"{qty=}, {part_number=}, {int(rev)=}, {money_value(price)=}, {money_value(amount)=}")

    # write the text to a file
    with open(r'C:\Users\ABriggs\Downloads\2023-04 LASER AMP 244246 PO 140194 POSTED GEN (1).txt', 'w') as f:
        f.write(text)

    a = 10
    print(a + 10)


# def parse_pdf(dir):
#     text, qtys, p_nums, revs, prices, amounts, invoice, order
#
#
# async def process_pdf(fn):
#     # fn = r"C:\Users\ABriggs\Downloads\2023-04 LASER AMP 244246 PO 140194 POSTED.pdf"
#
#     # open the PDF file in binary mode
#     with open(fn, 'rb') as f:
#         # create a PDF reader object
#         pdf_reader = PyPDF2.PdfFileReader(f)
#         # pdf_reader = PdfReader(f)
#         # read each page of the PDF file
#         text = ''
#         for page_num in range(pdf_reader.numPages):
#             page = pdf_reader.getPage(page_num)
#             # extract text from the page
#             page_text = page.extractText()
#             # append the text from this page to the overall text
#             text += page_text
#
#     values = text.split("Price Montant")[-1]
#     values = values.split("amount")[-1].split("SOUS-TOTAL")[0]
#     rows = values.split("\n")
#     columns = [
#         "Qté /qty",
#         "Numéro de pièce / Part Number",
#         "Rev.",
#         "Prix /Price",
#         "Montant / amount"
#     ]
#     print(f"{values=}")
#     for row in rows:
#         if row:
#             vals = row.split(" ")
#             qty_part_number, rev, price, amount = vals
#             part_number = qty_part_number.split("-")[-1]
#             idx = qty_part_number.index("-")
#             part_number = f"{qty_part_number[idx - 5:idx]}-{part_number}"
#             qty = int(qty_part_number[:idx][:-5])
#             print(f"{qty=}, {part_number=}, {int(rev)=}, {money_value(price)=}, {money_value(amount)=}")
#
#
# def test_batch_laser_amp():
#     root_laser_amp = r"\\nas1\Public\Accounts Payable\AP - BWS Manufacturing\Posted\Laser AMP"
#     sub_dirs = [(f"{root_laser_amp}\\{s_d}", "", "") for s_d in os.listdir(root_laser_amp)]
#
#     i = 0
#     dir = None
#     files = {}
#     file_template = [
#         "file_name",
#         "dir",
#         "s_dir",
#         "text_extracted",
#         "invoice",
#         "order_number",
#         "data"
#     ]
#     data_template = [
#         "qty",
#         "part_number",
#         "rev",
#         "price",
#         "amount"
#     ]
#
#     while sub_dirs:
#         a, b, c = sub_dirs
#         s_s_dirs = '\n'.join(a)
#         # print(f"\n{i=}\n{files=}\ns_s_dirs=\n{s_s_dirs}")
#         dir = sub_dirs.pop(0)
#         if os.path.isfile(dir):
#             text, qtys, p_nums, revs, prices, amounts, invoice, order = parse_pdf(dir)
#             data_values = [qtys, p_nums, revs, prices, amounts]
#             data = dict(zip(data_template, data_values))
#             file_values = [dir, b, c, text, invoice, order, data]
#             files[dir] = dict(zip(file_template, file_values))
#         elif os.path.isdir(dir):
#             for s_dir in os.listdir(dir):
#                 # print(f"{dir=}, {s_dir=}")
#                 sub_dirs.append((f"{dir}\\{s_dir}", dir, s_dir))
#         else:
#             print(f"unsure what to do with path '{dir}'")
#         i += 1
#
#     print(f"{files=}")
#     print(f"{len(files)=}")
#
#     for i, f_name in enumerate(files):
#
#
#
# def test_pdf_textract():
#     import textract
#
#     fn = r"C:\Users\ABriggs\Downloads\2023-04 LASER AMP 244246 PO 140194 POSTED.pdf"
#
#     # with open(fn, 'rb') as f:
#     #     text = textract.process(f, method="pdfminer")
#     #     print(f"{text=}")
#
#     # text = textract.process(fn, method="pdfminer")
#     # print(f"{text=}")
#
#     f = open(fn, 'rb')
#     # doc = PDFDocument(f)
#     # all_pages = [p for p in doc.pages()]
#     viewer = SimplePDFViewer(f)
#     print(f"{viewer.metadata=}")
#     text = ""
#
#     for i, canvas in enumerate(viewer):
#         page_images = canvas.images
#         page_forms = canvas.forms
#         page_text = canvas.text_content
#         page_inline_images = canvas.inline_images
#         page_strings = canvas.strings
#         # print(f"{i=} {page_images=}\n{page_forms=}\n{page_text=}\n{page_inline_images=}\n{page_strings=}")
#         print(f"{page_strings=}")
#         text = " ".join(("".join(page_strings)).split("\x03"))
#         print(f"--1   {text=}")
#
#     print(f"--2   {text=}")
#     values = text.split("Price Montant")[-1]
#     print(f"--1 {values=}")
#     values = values.split("amount")[-1].split("SOUS-TOTAL")[0]
#     rows = values.split("\n")
#     columns = [
#         "Qté /qty",
#         "Numéro de pièce / Part Number",
#         "Rev.",
#         "Prix /Price",
#         "Montant / amount"
#     ]
#     print(f"--2 {values=}")
#     for row in rows:
#         if row:
#             vals = row.split(" ")
#             qty_part_number, rev, price, amount = vals
#             part_number = qty_part_number.split("-")[-1]
#             idx = qty_part_number.index("-")
#             part_number = f"{qty_part_number[idx - 5:idx]}-{part_number}"
#             qty = int(qty_part_number[:idx][:-5])
#             print(f"{qty=}, {part_number=}, {int(rev)=}, {money_value(price)=}, {money_value(amount)=}")
#
#     # # open the PDF file in binary mode
#     # with open(fn, 'rb') as f:
#     #     # create a PDF reader object
#     #     # pdf_reader = PyPDF2.PdfFileReader(f)
#     #     pdf_reader = PdfReader(f)
#     #     # read each page of the PDF file
#     #     text = ''
#     #     for page_num in range(pdf_reader.numPages):
#     #         page = pdf_reader.getPage(page_num)
#     #         # extract text from the page
#     #         page_text = page.extractText()
#     #         # append the text from this page to the overall text
#     #         text += page_text
#
#     # values = text.split("Price Montant")[-1]
#     # values = values.split("amount")[-1].split("SOUS-TOTAL")[0]
#     # rows = values.split("\n")
#     # columns = [
#     #     "Qté /qty",
#     #     "Numéro de pièce / Part Number",
#     #     "Rev.",
#     #     "Prix /Price",
#     #     "Montant / amount"
#     # ]
#     # print(f"{values=}")
#     # for row in rows:
#     #     if row:
#     #         vals = row.split(" ")
#     #         qty_part_number, rev, price, amount = vals
#     #         part_number = qty_part_number.split("-")[-1]
#     #         idx = qty_part_number.index("-")
#     #         part_number = f"{qty_part_number[idx - 5:idx]}-{part_number}"
#     #         qty = int(qty_part_number[:idx][:-5])
#     #         print(f"{qty=}, {part_number=}, {int(rev)=}, {money_value(price)=}, {money_value(amount)=}")
#     #
#     # # write the text to a file
#     # with open(r'C:\Users\ABriggs\Downloads\2023-04 LASER AMP 244246 PO 140194 POSTED GEN (1).txt', 'w') as f:
#     #     f.write(text)
#     #
#     # a = 10
#     # print(a + 10)
#
#
# def test_pdf_camelot():
#     import textract
#
#     fn = r"C:\Users\ABriggs\Downloads\2023-04 LASER AMP 244246 PO 140194 POSTED.pdf"
#     tables = camelot.read_pdf(fn)
#     print(f"{tables=}")
#
#
# def test_pdf4():
#     # import tabula
#     # import pandas as pd
#     # df = tabula.read_pdf(r"C:\Users\ABriggs\Downloads\2023-04 LASER AMP 244246 PO 140194 POSTED.pdf", pages='all')
#     # print(f"DF: {df}")
#
#     import PyPDF4
#
#     fn = r"C:\Users\ABriggs\Downloads\2023-04 LASER AMP 244246 PO 140194 POSTED.pdf"
#
#     # open the PDF file in binary mode
#     with open(fn, 'rb') as f:
#         # create a PDF reader object
#         pdf_reader = PyPDF4.PdfFileReader(f)
#         # pdf_reader = PdfReader(f)
#         # read each page of the PDF file
#         text = ''
#         for page_num in range(pdf_reader.numPages):
#             page = pdf_reader.getPage(page_num)
#             # extract text from the page
#             page_text = page.extractText()
#             # append the text from this page to the overall text
#             text += page_text
#
#     print(f"{text=}")
#     values = text.split("Price Montant")[-1]
#     values = values.split("amount")[-1].split("SOUS-TOTAL")[0]
#     rows = values.split("\n")
#     columns = [
#         "Qté /qty",
#         "Numéro de pièce / Part Number",
#         "Rev.",
#         "Prix /Price",
#         "Montant / amount"
#     ]
#     print(f"{values=}")
#     for row in rows:
#         if row:
#             vals = row.split(" ")
#             qty_part_number, rev, price, amount = vals
#             part_number = qty_part_number.split("-")[-1]
#             idx = qty_part_number.index("-")
#             part_number = f"{qty_part_number[idx - 5:idx]}-{part_number}"
#             qty = int(qty_part_number[:idx][:-5])
#             print(f"{qty=}, {part_number=}, {int(rev)=}, {money_value(price)=}, {money_value(amount)=}")
#
#     # write the text to a file
#     with open(r'C:\Users\ABriggs\Downloads\2023-04 LASER AMP 244246 PO 140194 POSTED GEN (1).txt', 'w') as f:
#         f.write(text)
#
#     a = 10
#     print(a + 10)


def test_is_money():
    true_tests = [1, -1, -0.1, -11, 1.1, "1", "-1", "-0.1", "-11", "1.1", "$1", "$-1", "$-0.1", "$-11", "$1.1"]
    false_tests = [None, {}, [], "1.1.1", "$15-"]
    print(f"{all(list(map(is_money, true_tests)))=}")
    print(f"{not all(list(map(is_money, false_tests)))=}")


def test_custom_message_box():

    root = tkinter.Tk()
    w, h = 500, 500
    root.geometry(f"{w}x{h}")

    def open_tl():
        title = f"Testing CustomMessageBox2 Title"
        msg = f"Testing CustomMessageBox2 Message"
        x, y = 200, 200
        cmb_1 = CustomMessageBox(
            title=title,
            msg=msg,
            x=x,
            y=y,
            bg_colour=random_colour(rgb=False),
            bg_colour2=random_colour(rgb=False)
        )
        cmb_1.grab_set()

        print(f"{cmb_1.choice=}")

    tv_btn, btn = button_factory(root, "open", command=open_tl)
    btn.pack()

    root.mainloop()


if __name__ == "__main__":
    a = "avery"
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

    # text_rect_and_line()
    # test_money_str_format
    # test_find_north_side()
    # test_new_rect()  # This one looks cool

    # test_rect_collision()
    # test_menubar()
    # test_listbox()
    # test_scrollbar()
    # test_hyperlink()
    # test_random_date()
    # test_iscolour()
    # test_alert_colour()
    # test_is_date()
    # test_date_manipulation()
    # test_intersection()
    # test_line_inequality()
    # test_lineSeg()
    # test_font_foreground()
    # test_dict_print2()
    # test_rainbow_gradient()
    # test_pyodbc_connection()
    # test_NATO_phonetic_alphabet()
    # test_grid_cells()
    # test_rect_bounds()
    # test_colourify()
    # test_tk_slider()
    # test_rgb_slider()
    # test_theme_publisher()
    # test_alpha_seq()
    # test_grid_manager()
    # test_margins()
    # test_is_number()
    # test_spread()
    # test_pdf()
    # test_pdf_textract()
    # test_pdf_camelot()
    # test_pdf4()
    # test_batch_laser_amp()
    test_is_money()
    test_custom_message_box()

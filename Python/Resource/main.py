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
                print("i:", i, "| j:", j, "| v:", v, "| d1:", d1, "| d2:", d2, "| di:", (n+m-1))
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


if __name__ == "__main__":
    app = PygameApplication("Test TextBox", 600, 400)
    game = app.get_game()
    display = app.display
    r1 = Rect(100, 25, 200, 100)
    # self, game, display, rect, ic, ac, f, fc, text = '', min_width = 20, numeric = False, char_limit = None, n_limit = None, bs = 1, border_style = None
    textbox = TextBox(game, display, r1, text="-1", numeric=True)
    while app.is_playing:
        display.fill(BLACK)
        textbox.draw()
        event_queue = app.run()
        for event in event_queue:
            textbox.handle_event(event)

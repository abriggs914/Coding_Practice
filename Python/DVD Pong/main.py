from pygame_utility import *


def main_loop():

    # win_w, win_h = 750, 500
    win_w, win_h = 1000, 700
    app = PygameApplication("Name Goes Here!", win_w, win_h)
    game = app.get_game()
    display = app.display

    # grid_w, grid_h = win_w * 0.8, win_h * 0.7
    grid_w, grid_h = 900, 600
    grid = {
        "rect": game.Rect((win_w - grid_w) / 2, (win_h - grid_h) / 2, grid_w, grid_h),
        "colour": GRAY_37
    }
    ball = {
        "x": grid["rect"].left + 9,
        "y": grid["rect"].bottom - 6,
        "r": 5,
        "x_vel": 16,
        "y_vel": -20,
        "colour": PINK,
        "top_hits": 0,
        "bottom_hits": 0,
        "left_hits": 0,
        "right_hits": 0,
        "line": [],
        "line_colour": RED
    }

    while app.is_playing:
        display.fill(BLACK)

        # draw widgets and objects here
        game.draw.rect(display, grid["colour"], grid["rect"])
        game.draw.circle(display, ball["colour"], (ball["x"], ball["y"]), ball["r"])
        if len(ball["line"]) > 1:
            game.draw.lines(display, ball["line_colour"], False, ball["line"])

        event_queue = app.run()
        for event in event_queue:
            # handle events
            pass

        x_vel = ball["x_vel"]
        y_vel = ball["y_vel"]
        ball["line"].append((ball["x"], ball["y"]))
        ball["x"] += x_vel
        ball["y"] += y_vel
        if ball["x"] < grid["rect"].left:
            # ball["x"] = abs(ball["x"] - grid["rect"].left) + grid["rect"].left  # abs(ball["x"])
            # ball["x"] = grid["rect"].left
            # ball["line"].insert(-2, ((ball["x"], ball["y"])))
            # ball["x"] = abs(ball["x"] - grid["rect"].left) + grid["rect"].left

            print("ball: ({}, {}) hit left ({}, {})".format(ball["x"], ball["y"], ball["x_vel"], ball["y_vel"]))
            l = Line(ball["x"] - x_vel, ball["y"] - y_vel, ball["x"], ball["y"])
            cross = grid["rect"].left, l.y_at_x(grid["rect"].left)
            ball["line"].append(cross)
            ball["x"] = (2 * grid["rect"].left) - ball["x"]

            ball["x_vel"] = -x_vel
            ball["left_hits"] += 1
            ball["colour"] = RED
            ball["line_colour"] = RED
            print("adjusted to ({}, {}) ({}, {})".format(ball["x"], ball["y"], ball["x_vel"], ball["y_vel"]))
        elif ball["x"] > grid["rect"].right:
            # ball["line"].insert(-2, ((ball["x"], ball["y"])))
            # ball["x"] = (grid["rect"].right - ball["x"]) + grid["rect"].right
            # ball["x"] = grid["rect"].right
            print("ball: ({}, {}) hit right ({}, {})".format(ball["x"], ball["y"], ball["x_vel"], ball["y_vel"]))
            l = Line(ball["x"] - x_vel, ball["y"] - y_vel, ball["x"], ball["y"])
            cross = grid["rect"].right, l.y_at_x(grid["rect"].right)
            ball["line"].append(cross)
            ball["x"] = grid["rect"].right - (ball["x"] - grid["rect"].right)

            ball["x_vel"] = -x_vel
            ball["right_hits"] += 1
            ball["colour"] = RED
            ball["line_colour"] = RED
            print("adjusted to ({}, {}) ({}, {})".format(ball["x"], ball["y"], ball["x_vel"], ball["y_vel"]))

        elif ball["y"] < grid["rect"].top:
            # ball["line"].insert(-2, ((ball["x"], ball["y"])))
            # ball["y"] = abs(ball["y"] - grid["rect"].top) + grid["rect"].top  # abs(ball["y"])
            # ball["y"] = grid["rect"].top
            # ball["y"] = abs(ball["y"] - grid["rect"].top) + grid["rect"].top

            print("ball: ({}, {}) hit top ({}, {})".format(ball["x"], ball["y"], ball["x_vel"], ball["y_vel"]))
            l = Line(ball["x"] - x_vel, ball["y"] - y_vel, ball["x"], ball["y"])
            cross = l.x_at_y(grid["rect"].top), grid["rect"].top
            ball["line"].append(cross)
            ball["y"] = (2 * grid["rect"].top) - ball["y"]

            ball["y_vel"] = -y_vel
            ball["top_hits"] += 1
            ball["colour"] = BLUE
            ball["line_colour"] = BLUE
            print("adjusted to ({}, {}) ({}, {})".format(ball["x"], ball["y"], ball["x_vel"], ball["y_vel"]))
        elif ball["y"] > grid["rect"].bottom:
            # ball["line"].insert(-2, ((ball["x"], ball["y"])))
            # ball["y"] = (grid["rect"].bottom - ball["y"]) + grid["rect"].bottom
            # ball["y"] = grid["rect"].bottom

            print("ball: ({}, {}) hit bottom ({}, {})".format(ball["x"], ball["y"], ball["x_vel"], ball["y_vel"]))
            l = Line(ball["x"] - x_vel, ball["y"] - y_vel, ball["x"], ball["y"])
            cross = l.x_at_y(grid["rect"].bottom), grid["rect"].bottom
            ball["line"].append(cross)
            ball["y"] = grid["rect"].bottom - (ball["y"] - grid["rect"].bottom)

            ball["y_vel"] = -y_vel
            ball["bottom_hits"] += 1
            ball["colour"] = BLUE
            ball["line_colour"] = BLUE
            print("adjusted to ({}, {}) ({}, {})".format(ball["x"], ball["y"], ball["x_vel"], ball["y_vel"]))

        app.clock.tick(30)


if __name__ == '__main__':
    print('PyCharm')
    main_loop()



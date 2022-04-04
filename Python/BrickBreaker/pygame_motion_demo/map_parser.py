from os import path
from utility import *
from colour_utility import *
import json

import pygame.draw


class Ball:

    def __init__(self, x, y, radius, colours, max_x_speed=10, max_y_speed=10, hp=None, breakable=False, visible=False):
        self._x = x
        self._y = y
        self.radius = radius
        self._centre = x, y
        self.hp = hp
        self.curr_hp = hp
        self.colours = colours if isinstance(colours, list) else [colours]
        self.breakable = breakable
        self.x_speed = 0
        self.y_speed = 0
        self.max_x_speed = max_x_speed
        self.max_y_speed = max_y_speed

        self.visible = visible or 1

    def get_x(self):
        return self._x

    def get_y(self):
        return self._y

    def get_centre(self):
        return self._centre

    def set_x(self, value):
        self._x = value
        self._centre = self.x, self.y

    def set_centre(self, value):
        self._centre = value
        self._x = value[0]
        self._y = value[1]

    def set_y(self, value):
        self._y = value
        self._centre = self.x, self.y

    def curr_colour(self):
        p = self.curr_hp / (self.hp if self.hp != 0 else 1)
        i = int(p * len(self.colours)) - 1
        # print(f"p: {p}, i: {i}, colours: {self.colours}, self.colours[i]: {self.colours[i]}")
        return self.colours[i]

    # This version uses the centre of the ball to check bounds. Goes half way off screen
    # def move(self, bounds, jmap):
    #     # self.x = clamp(bounds.left, self.x + self.x_speed, bounds.right)
    #     # self.y = clamp(bounds.top, self.y + self.y_speed, bounds.bottom)
    #     nlx = self.x + self.x_speed  # - self.radius
    #     nrx = self.x + self.x_speed  # + self.radius
    #     nty = self.y + self.y_speed  # - self.radius
    #     nby = self.y + self.y_speed  # + self.radius
    #
    #     # check collisions with main walls
    #     if self.x_speed > 0:
    #         diff = bounds.right - nrx
    #         if diff < 0 and jmap.bounce_right:
    #             self.x_speed *= -1
    #             self.x = bounds.right + diff  # - self.radius
    #     elif self.x_speed < 0:
    #         diff = bounds.left - nlx
    #         if diff > 0 and jmap.bounce_left:
    #             self.x_speed *= -1
    #             self.x = bounds.left + diff  # + self.radius
    #     if self.y_speed > 0:
    #         diff = bounds.bottom - nty
    #         if diff < 0 and jmap.bounce_bottom:
    #             self.y_speed *= -1
    #             self.y = bounds.bottom + diff  # - self.radius
    #     elif self.y_speed < 0:
    #         diff = bounds.top - nby
    #         if diff > 0 and jmap.bounce_top:
    #             self.y_speed *= -1
    #             self.y = bounds.top + diff  # + self.radius
    #     self.x = clamp(bounds.left, self.x + self.x_speed, bounds.right)
    #     self.y = clamp(bounds.top, self.y + self.y_speed, bounds.bottom)

    def move(self, bounds, jmap):
        # self.x = clamp(bounds.left, self.x + self.x_speed, bounds.right)
        # self.y = clamp(bounds.top, self.y + self.y_speed, bounds.bottom)
        nlx = self.x + self.x_speed  # - self.radius
        nrx = self.x + self.x_speed  # + self.radius
        nty = self.y + self.y_speed  # - self.radius
        nby = self.y + self.y_speed  # + self.radius
        self.x += self.x_speed
        self.y += self.y_speed

        # check collisions with main walls
        if self.x_speed > 0:
            diff = bounds.right - nrx
            if diff < self.radius and jmap.bounce_right:
                self.x_speed *= -1
                self.x = bounds.right + diff
        elif self.x_speed < 0:
            diff = (bounds.left + self.radius) - nlx
            if diff > 0 and jmap.bounce_left:
                self.x_speed *= -1
                self.x = bounds.left + diff + self.radius
        if self.y_speed > 0:
            diff = bounds.bottom - nty
            if diff < self.radius and jmap.bounce_bottom:
                self.y_speed *= -1
                self.y = bounds.bottom + diff
        elif self.y_speed < 0:
            diff = (bounds.top + self.radius) - nby
            if diff > 0 and jmap.bounce_top:
                self.y_speed *= -1
                self.y = bounds.top + diff + self.radius

        # for row in jmap.map:
        #     for col in row:

        self.x = clamp(bounds.left + self.radius, self.x, bounds.right - self.radius)
        self.y = clamp(bounds.top + self.radius, self.y, bounds.bottom - self.radius)

    def draw(self, window):
        if self.visible:
            pygame.draw.circle(window, self.curr_colour(), self.centre, self.radius)

    x = property(get_x, set_x)
    y = property(get_y, set_y)
    centre = property(get_centre, set_centre)


class Brick:

    def __init__(self, i, j, rect, hp, colours, breakable, char):
        self.i = i
        self.j = j
        self.rect = rect
        self.hp = hp
        self.curr_hp = hp
        self.colours = colours if isinstance(colours, list) else [colours]
        self.breakable = breakable
        self.char = char

    def visible(self):
        return self.curr_hp > 0

    def curr_colour(self):
        p = self.curr_hp / (self.hp if self.hp != 0 else 1)
        i = int(p * len(self.colours)) - 1
        # print(f"self.hp: {self.hp}, curr: {self.curr_hp}, p: {p}, i: {i}, colours: {self.colours}")
        # print(f"p: {p}, i: {i}, colours: {self.colours}, self.colours[i]: {self.colours[i]}")
        return self.colours[i]

    def draw(self, window):
        if self.visible():
            pygame.draw.rect(window, self.curr_colour(), self.rect)

    def __repr__(self):
        return self.char


class BrickEmpty(Brick):

    def __init__(self, i, j, rect, colour, char):
        super().__init__(i, j, rect, 1, [colour], False, char)

    def visible(self):
        return False


class BrickPaddle(Brick):

    def __init__(self, i, j, rect, colour, char):
        super().__init__(i, j, rect, 1, [colour], False, char)

    def visible(self):
        return False


class BrickWall(Brick):

    def __init__(self, i, j, rect, colour, char):
        super().__init__(i, j, rect, 1, [colour], False, char)

    def visible(self):
        return False


class JMap:

    def __init__(self, file_name):
        self.file_name = file_name
        self._valid = False
        self._tested = None

        self._name = None
        self._rows = None
        self._cols = None
        self._width = None
        self._height = None
        self.balls = None  # list
        self.bounce_top = True
        self.bounce_left = True
        self.bounce_right = True
        self.bounce_bottom = False

        # print(f"X::: {0, 0, self.width, self.height}")
        self._rect = None
        self.map = []
        self.balls = []

    def test_map(self):
        self.tested = False
        if not path.exists(self.file_name):
            raise FileNotFoundError(f"This file name could not be found: \'{self.file_name}\'")
        with open(self.file_name, "r") as f_json:
            parsed_json = json.load(f_json)
            print(f"parsed_json\'{parsed_json}\'")
            attrv = parsed_json["width"]
            print(f"GET: {attrv}")

            self.name = parsed_json["name"]
            self.width = parsed_json["width"]
            self.height = parsed_json["height"]
            self.rect = pygame.Rect(0, 0, self.width, self.height)

            if self.width is None:
                raise ValueError(f"Width value is invalid: \'{self.width}\'")
            if self.height is None:
                raise ValueError(f"Height value is invalid: \'{self.height}\'")

            grid_str = parsed_json["map"]
            grid_legend = parsed_json["legend"]

            if grid_str is None:
                raise ValueError(f"Grid value is invalid: \'{grid_str}\'")
            if grid_legend is None:
                raise ValueError(f"Legend value is invalid: \'{grid_legend}\'")

            self.rows = len(grid_str)
            cols = None
            letter_data = {}
            for k1, v1 in grid_legend.items():
                for k2, v2 in v1.items():
                    letter_data[k2] = {k1: v2}

            print(dict_print(letter_data, "LETTER_DATA"))
            for r in range(self.rows):
                if cols is not None and len(grid_str[r]) != cols:
                    raise ValueError(f"Grid value has inconsistent dimensions on row \'{r}\'")
                cols = len(grid_str[r])
            self.cols = cols

            rw = self.width / self.cols
            rh = self.height / self.rows
            for r in range(self.rows):
                row_list = []
                for c in range(cols):
                    rect = pygame.Rect(rw * c, rh * r, rw, rh)
                    value = grid_str[r][c]
                    val = grid_str[r][c]
                    print("SFSD", letter_data[value])
                    if value not in letter_data:
                        raise KeyError(f"Value \'{value}\' not found in letter data.")
                    for i, btype in enumerate(['wall', 'brick', 'paddle', 'empty']):
                        if btype in letter_data[value]:
                            if i == 0:
                                val = BrickWall(r, c, rect, eval(letter_data[value][btype]['colour']), value)
                            elif i == 1:
                                colours = letter_data[value][btype]['colour']
                                colours = [eval(col) for col in colours]
                                val = Brick(r, c, rect, letter_data[value][btype]['hp'], colours, True, value)
                            elif i == 2:
                                val = BrickPaddle(r, c, rect, eval(letter_data[value][btype]['colour']), value)
                            else:
                                print(f"XXXletter_data[value][btype]: btype: {btype}, {letter_data[value]}")
                                val = BrickEmpty(r, c, rect, eval(letter_data[value][btype]['colour']), value)
                    row_list.append(val)
                self.map.append(row_list)

            ball_data = parsed_json['balls']
            for k, ball_dat in ball_data.items():
                print(f"X:::: {ball_dat}")
                colours = ball_dat['colour']
                colours = colours if isinstance(colours, list) else [colours]
                colours = [eval(colour) for colour in colours]
                hp = None if 'hp' not in ball_dat else ball_dat['hp']
                max_x_speed = 10 if 'max_x_speed' not in ball_dat else ball_dat['max_x_speed']
                max_y_speed = 10 if 'max_y_speed' not in ball_dat else ball_dat['max_y_speed']
                breakable = hp is not None
                self.balls.append(Ball(0, 0, ball_dat['radius'], colours, max_x_speed, max_y_speed, hp, breakable))

        self.tested = True
        self.valid = True

    def move(self, window):
        for ball in self.balls:
            ball.move(window.get_rect(), self)

    def draw(self, window):
        for row in self.map:
            for col in row:
                # print(f"col: {col}")
                col.draw(window)
        for ball in self.balls:
            for row in self.map:
                for col in row:
                # print(f"col: {col}")
                    if not isinstance(col, BrickEmpty):
                        if distance(col.rect.center, ball.centre) < ball.radius:
                            if col.visible():
                                old = col.curr_hp
                                col.curr_hp = clamp(0, col.curr_hp - 1, col.hp)
                                print(f"hit: col {col}, ball: {ball}, old: {old}, new: {col.curr_hp}")
                                if col.curr_hp == 0 and col.breakable:
                                    print(f"breaking col: {col}")

            ball.draw(window)


    def is_valid(self):
        return self._valid

    def set_valid(self, value):
        self._valid = value

    def is_tested(self):
        return self._valid

    def set_tested(self, value):
        if self._tested is not None and not value:
            raise ValueError("This map has already been tested and proven invalid.Please fix this map.")
        self._valid = value

    def get_rows(self):
        if self.tested is None:
            raise ValueError("Unable to get rows value because this map is untested.")
        if not self.valid and self.tested:
            raise ValueError("Unable to get rows value because this map is invalid.")
        return self._rows

    def set_rows(self, value):
        self._rows = value

    def get_cols(self):
        if self.tested is None:
            raise ValueError("Unable to get cols value because this map is untested.")
        if not self.valid and self.tested:
            raise ValueError("Unable to get cols value because this map is invalid.")
        return self._cols

    def set_cols(self, value):
        self._cols = value

    def get_rect(self):
        if self.tested is None:
            raise ValueError("Unable to get rect value because this map is untested.")
        if not self.valid and self.tested:
            raise ValueError("Unable to get rect value because this map is invalid.")
        return self._rect

    def set_rect(self, value):
        print(f"X:::self: {self.rect}, value: {value}")
        if self.rect is not None:
            xd, yd = self.rect.x - value.x, self.rect.y - value.y
            for row in self.map:
                for col in row:
                    col.rect.center = col.rect.centerx + xd, col.rect.centery + yd
            for ball in self.balls:
                ball.x += xd
                ball.y += yd
        self._rect = value

    def get_width(self):
        if self.tested is None:
            raise ValueError("Unable to get width value because this map is untested.")
        if not self.valid and self.tested:
            raise ValueError("Unable to get width value because this map is invalid.")
        return self._width

    def set_width(self, value):
        self._width = value

    def get_height(self):
        if self.tested is None:
            raise ValueError("Unable to get height value because this map is untested.")
        if not self.valid and self.tested:
            raise ValueError("Unable to get height value because this map is invalid.")
        return self._height

    def set_height(self, value):
        self._height = value

    def get_name(self):
        if self.tested is None:
            raise ValueError("Unable to get name value because this map is untested.")
        if not self.valid and self.tested:
            raise ValueError("Unable to get name value because this map is invalid.")
        return self._name

    def set_name(self, value):
        self._name = value

    name = property(get_name, set_name)
    valid = property(is_valid, set_valid)
    tested = property(is_tested, set_tested)
    rows = property(get_rows, set_rows)
    cols = property(get_cols, set_cols)
    width = property(get_width, set_width)
    height = property(get_height, set_height)
    rect = property(get_rect, set_rect)

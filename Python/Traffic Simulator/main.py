from pygame_application import *
from colour_utility import *
from pygame_utility import *


class Car:

    # Note x, y are coordinates of the centre of the car, not top-left.
    def __init__(self, game, display, id_num, x, y, speed=1, acceleration=0, name="car", colour=BLACK, img_path=None, is_circle=True,
                 radius=6, width=None, height=None):
        self.game = game
        self.display = display
        self.speed = speed
        self.acceleration = acceleration
        self.id_num = id_num
        self.name = name
        self.colour = colour
        self.img_path = img_path
        self.is_circle = is_circle
        radius = (radius if 1 <= radius <= 100 else 6) if radius is not None else 6
        self.radius = radius
        self.w = radius
        self.h = radius
        if width is not None:
            self.w = width
        if height is not None:
            self.h = height
        if width is not None and height is not None:
            self.radius = max(width, height)
        self.rect = Rect(x - (radius / 2), y - (radius / 2), self.w, self.h)

        self.is_crashed = False
        self.arrival = None
        self.departure = None
        self.pt_history = [(x, y)]

    def set_arrival(self, arr):
        self.arrival = arr

    def set_departure(self, dept):
        self.departure = dept

    def set_rect(self, rect):
        assert isinstance(rect, Rect)
        self.rect = rect

    def set_x(self, x):
        self.rect = Rect(x, self.rect.y, self.rect.width, self.rect.height)

    def set_y(self, y):
        self.rect = Rect(self.rect.x, y, self.rect.width, self.rect.height)

    def add_x(self, x):
        self.rect = Rect(self.rect.x + x, self.rect.y, self.rect.width, self.rect.height)

    def add_y(self, y):
        self.rect = Rect(self.rect.x, self.rect.y + y, self.rect.width, self.rect.height)

    def draw(self):
        if self.img_path is not None:
            # draw image
            pass
        else:
            self.game.draw.circle(self.display, BLUEVIOLET, (self.rect.x + (self.radius / 2), self.rect.y + (self.radius / 2)), self.radius)
            self.game.draw.rect(self.display, self.colour, self.rect.tupl)

    def __eq__(self, other):
        return isinstance(other, Car) and all([
            self.id_num == other.id_num
        ])

    def __repr__(self):
        return "car<#{}, {}> s:{} a:{}".format(self.id_num, self.rect, self.speed, self.acceleration)


class RoadWay:

    def __init__(self, direction, rect, colour, n_lanes=1, centre_side="left"):
        assert isinstance(rect, Rect)
        assert (isinstance(direction, list) or isinstance(direction, tuple)) and all(
            [direct in DIRECTIONS for direct in direction])
        # TODO; include diagonal roadway functionality
        assert any([direction == ("N", "S"), direction == ("S", "N"), direction == ("E", "W"), direction == ("W", "E")])
        assert any([centre_side == "left", centre_side == "right", centre_side == "top", centre_side == "bottom"])
        self.rect = rect
        self.direction = direction  # tuple rough directionality vie pygame_utility directions ex: ("N", "S")
        self.colour = colour
        self.n_lanes = n_lanes
        self.lane_mode = "diagonal"
        self.centre_side = centre_side  # left == top, right == bottom

        rect = rect.tupl
        if direction == ("N", "S") or direction == ("S", "N"):
            self.lane_width = rect[2] / n_lanes
            self.lane_height = rect[3]
            self.lane_mode = "vertical"
        elif direction == ("E", "W") or direction == ("W", "E"):
            self.lane_width = rect[3] / n_lanes
            self.lane_height = rect[2]
            self.lane_mode = "horizontal"

        self.car_queue = []

        self.info_print()

    def valid_place(self, car, strictly_inside=False):
        if not self.rect.collide_rect(car.rect, strictly_inside=strictly_inside):
            print("\t\tearly exit")
            return False
        # check car crashes
        return True

    def check_car_crash(self, car, strictly_inside=False):
        for c in self.car_queue:
            if c != car:
                if c.rect.collide_rect(car.rect, strictly_inside=strictly_inside):
                    print("\t\tlate exit\nCar: {}\n\tcollides with:\n{}".format(car, c))
                    print("Car Queue:\n\t{}".format("\n\t".join([str(cc) for cc in self.car_queue])))
                    return True
        return False

    def spawn_car(self, game, display, id_num, colour, name=None, img_path=None, is_circle=True, speed=1, acceleration=0, radius=None, width=None, height=None, center=None):
        # print("lane_mode:", self.lane_mode, "centre_side: ", self.centre_side)
        if self.lane_mode == "vertical":
            if self.centre_side == "left":
                # S -> N
                x, y = self.rect.center_bottom
            else:
                x, y = self.rect.center_top
        elif self.lane_mode == "horizontal":
            if self.centre_side == "top":
                # W -> E
                # x, y = self.rect.center_left
                x, y = self.rect.center_right
            else:
                # W <- E
                # x, y = self.rect.center_right
                x, y = self.rect.center_left
        else:
            # TODO: support diagonal car spawning.
            x, y = 1, 1
        car = Car(game, display, id_num, x, y, speed=speed, acceleration=acceleration, name=name, colour=colour, img_path=img_path, is_circle=is_circle, radius=radius, width=width, height=height)
        self.add_car(car)
        if center is not None:
            if str(center) == "True" or str(center) == "False":
                self.center_car(car, true_center=center)
            else:
                self.center_car(car, lane=center)
        return car

    def is_exiting(self, car, i_tick_dist=1, j_tick_dist=1):
        r = Rect(*self.rect.tupl)
        # a = r.top_left
        # b = r.top_right
        # c = r.bottom_left
        # d = r.bottom_right
        rc = Rect(r.x, r.y, r.width, r.height)
        top_i = rc.top_line
        bottom_i = rc.bottom_line
        left_i = rc.left_line
        right_i = rc.right_line
        top_o = Rect(rc.left, rc.top + -1 * abs(i_tick_dist), rc.width, abs(i_tick_dist))  # top_i.translated(0, -1 * abs(i_tick_dist))
        bottom_o = Rect(rc.left, rc.bottom, rc.width, abs(i_tick_dist))  # bottom_i.translated(0, 1 * abs(i_tick_dist))
        left_o = Rect(rc.left + -1 * abs(j_tick_dist), rc.top, abs(j_tick_dist), rc.height)  # left_i.translated(-1 * abs(j_tick_dist), 0)
        right_o = Rect(rc.right, rc.top, abs(j_tick_dist), rc.height)  # right_i.translated(1 * abs(j_tick_dist), 0)
        car_r = car.rect
        # lm = lambda v, vs: (v[0] + vs[0], v[1] + vs[1])
        # top = Line(*lm(a, (-1, -1)), *lm(b, (1, -1)))
        # bottom = Line(*lm(c, (-1, 1)), *lm(d, (1, 1)))
        # left = Line(*lm(a, (-1, -1)), *lm(c, (-1, 1)))
        # right = Line(*lm(b, (1, -1)), *lm(d, (1, 1)))
        ie = False
        if self.lane_mode == "vertical":
            # ie = not self.valid_place(car) and (((car_r.collide_line(top_o) and not car_r.collide_line(top_i)) or (car_r.collide_line(bottom_o) and not car_r.collide_line(bottom_i))))
            ie = not r.collide_rect(car_r, strictly_inside=True) and (top_o.collide_rect(car_r, 0) or bottom_o.collide_rect(car_r, 0))
        if self.lane_mode == "horizontal":
            # ie = not self.valid_place(car) and (((car_r.collide_line(left_o) and not car_r.collide_line(left_i)) or (car_r.collide_line(right_o) and not car_r.collide_line(right_i))))
            ie = not r.collide_rect(car_r, strictly_inside=True) and (left_o.collide_rect(car_r, 0 ) or right_o.collide_rect(car_r, 0))
        print(dict_print({
            "car": str(car),
            "self": self.rect,
            "self.dir": str(self.direction),
            "top_i": "{} <{}>".format(top_i, car_r.collide_line(top_i)),
            "top_o": "{} <{}>".format(top_o, car_r.collide_rect(top_o)),
            "bottom_i": "{} <{}>".format(bottom_i, car_r.collide_line(bottom_i)),
            "bottom_o": "{} <{}>".format(bottom_o, car_r.collide_rect(bottom_o)),
            # "Cto && ~Cti": "{}".format(car_r.collide_line(top_o) and not car_r.collide_line(top_i)),
            # "Cbo && ~Cbi": "{}".format(car_r.collide_line(bottom_o) and not car_r.collide_line(bottom_i)),
            # "Cbo && ~Cbi || Cbo && ~Cbi": "{}".format((car_r.collide_line(top_o) and not car_r.collide_line(top_i)) or (car_r.collide_line(bottom_o) and not car_r.collide_line(bottom_i))),

            "left_i": "{} <{}>".format(left_i, car_r.collide_line(left_i)),
            "left_o": "{} <{}>".format(left_o, car_r.collide_rect(left_o)),
            "right_i": "{} <{}>".format(right_i, car_r.collide_line(right_i)),
            "right_o": "{} <{}>".format(right_o, car_r.collide_rect(right_o)),
            # "Clo && ~Cli": "{}".format(car_r.collide_line(left_o) and not car_r.collide_line(left_i)),
            # "Cro && ~Cri": "{}".format(car_r.collide_line(right_o) and not car_r.collide_line(right_i)),
            # "Clo && ~Cli || Cro && ~Cri": "{}".format((car_r.collide_line(left_o) and not car_r.collide_line(left_i)) or (car_r.collide_line(right_o) and not car_r.collide_line(right_i))),
            "is_exiting: ": ie
            # "top_o": top_o,
            # "Ctop": r.collide_line(top),
            # "bottom": bottom,
            # "Cbottom": r.collide_line(bottom),
            # "left": left,
            # "Cleft": r.collide_line(left),
            # "right": right,
            # "Cright": r.collide_line(right)
        }, "Data"))
        if self.lane_mode == "vertical" or self.lane_mode == "horizontal":
            return ie
        else:
            raise ValueError("diagonal roadways not supported yet.")

        # r = Rect(*self.rect.tupl)
        # # a = r.top_left
        # # b = r.top_right
        # # c = r.bottom_left
        # # d = r.bottom_right
        # rc = Rect(r.x, r.y, r.width, r.height)
        # top_i = rc.top_line
        # bottom_i = rc.bottom_line
        # left_i = rc.left_line
        # right_i = rc.right_line
        # top_o = top_i.translated(0, -1 * abs(i_tick_dist))
        # bottom_o = bottom_i.translated(0, 1 * abs(i_tick_dist))
        # left_o = left_i.translated(-1 * abs(j_tick_dist), 0)
        # right_o = right_i.translated(1 * abs(j_tick_dist), 0)
        # car_r = car.rect
        # # lm = lambda v, vs: (v[0] + vs[0], v[1] + vs[1])
        # # top = Line(*lm(a, (-1, -1)), *lm(b, (1, -1)))
        # # bottom = Line(*lm(c, (-1, 1)), *lm(d, (1, 1)))
        # # left = Line(*lm(a, (-1, -1)), *lm(c, (-1, 1)))
        # # right = Line(*lm(b, (1, -1)), *lm(d, (1, 1)))
        # ie = False
        # if self.lane_mode == "vertical":
        #     ie = not self.valid_place(car) and (((car_r.collide_line(top_o) and not car_r.collide_line(top_i)) or (
        #                 car_r.collide_line(bottom_o) and not car_r.collide_line(bottom_i))))
        # if self.lane_mode == "vertical":
        #     ie = not self.valid_place(car) and (((car_r.collide_line(left_o) and not car_r.collide_line(left_i)) or (
        #                 car_r.collide_line(right_o) and not car_r.collide_line(right_i))))
        # print(dict_print({
        #     "car": car.rect,
        #     "self": self.rect,
        #     "self.dir": str(self.direction),
        #     "top_i": "{} <{}>".format(top_i, car_r.collide_line(top_i)),
        #     "top_o": "{} <{}>".format(top_o, car_r.collide_line(top_o)),
        #     "bottom_i": "{} <{}>".format(bottom_i, car_r.collide_line(bottom_i)),
        #     "bottom_o": "{} <{}>".format(bottom_o, car_r.collide_line(bottom_o)),
        #     "Cto && ~Cti": "{}".format(car_r.collide_line(top_o) and not car_r.collide_line(top_i)),
        #     "Cbo && ~Cbi": "{}".format(car_r.collide_line(bottom_o) and not car_r.collide_line(bottom_i)),
        #     "Cbo && ~Cbi || Cbo && ~Cbi": "{}".format((car_r.collide_line(top_o) and not car_r.collide_line(top_i)) or (
        #                 car_r.collide_line(bottom_o) and not car_r.collide_line(bottom_i))),
        #
        #     "left_i": "{} <{}>".format(left_i, car_r.collide_line(left_i)),
        #     "left_o": "{} <{}>".format(left_o, car_r.collide_line(left_o)),
        #     "right_i": "{} <{}>".format(right_i, car_r.collide_line(right_i)),
        #     "right_o": "{} <{}>".format(right_o, car_r.collide_line(right_o)),
        #     "Clo && ~Cli": "{}".format(car_r.collide_line(left_o) and not car_r.collide_line(left_i)),
        #     "Cro && ~Cri": "{}".format(car_r.collide_line(right_o) and not car_r.collide_line(right_i)),
        #     "Clo && ~Cli || Cro && ~Cri": "{}".format(
        #         (car_r.collide_line(left_o) and not car_r.collide_line(left_i)) or (
        #                     car_r.collide_line(right_o) and not car_r.collide_line(right_i))),
        #     "is_exiting: ": ie
        #     # "top_o": top_o,
        #     # "Ctop": r.collide_line(top),
        #     # "bottom": bottom,
        #     # "Cbottom": r.collide_line(bottom),
        #     # "left": left,
        #     # "Cleft": r.collide_line(left),
        #     # "right": right,
        #     # "Cright": r.collide_line(right)
        # }, "Data"))
        # if self.lane_mode == "vertical" or self.lane_mode == "horizontal":
        #     return ie
        # else:
        #     raise ValueError("diagonal roadways not supported yet.")

    def add_car(self, car):
        assert isinstance(car, Car)
        self.car_queue.append(car)

    def tick(self, tick):
        for car in self.car_queue:
            print("Direction: {}, (x, y): ({}, {})".format(self.direction[1], DIRECTIONS[self.direction[1]]["x"], DIRECTIONS[self.direction[1]]["y"]))
            x_inc = (DIRECTIONS[self.direction[1]]["x"] * car.speed * tick) + (0.5 * car.acceleration * (tick ** 2))
            y_inc = (DIRECTIONS[self.direction[1]]["y"] * car.speed * tick) + (0.5 * car.acceleration * (tick ** 2))
            if car.acceleration != 0:
                # print("x_inc: {}, y_inc: {}".format(x_inc, y_inc))
                # print("BEFORE new speed: ", car.speed)
                # print("car.acceleration", car.acceleration)
                # print("car.rect:", car.rect)
                # print("(car.speed ** 2): ", (car.speed ** 2))
                # print("(car.rect.x, car.rect.x + x_inc)", (car.rect.x, car.rect.x + x_inc))
                # print("(car.rect.y, car.rect.y + y_inc)", (car.rect.y, car.rect.y + y_inc))
                # print("distance((car.rect.x, car.rect.x + x_inc), (car.rect.y, car.rect.y + y_inc))", distance((car.rect.x, car.rect.x + x_inc), (car.rect.y, car.rect.y + y_inc)))
                # print("(2 * car.acceleration * distance((car.rect.x, car.rect.x + x_inc), (car.rect.y, car.rect.y + y_inc)))", (2 * car.acceleration * distance((car.rect.x, car.rect.x + x_inc), (car.rect.y, car.rect.y + y_inc))))
                # print("((car.speed ** 2) + (2 * car.acceleration * distance((car.rect.x, car.rect.x + x_inc), (car.rect.y, car.rect.y + y_inc))))", ((car.speed ** 2) + (2 * car.acceleration * distance((car.rect.x, car.rect.x + x_inc), (car.rect.y, car.rect.y + y_inc)))))
                # print("((car.speed ** 2) + (2 * car.acceleration * distance((car.rect.x, car.rect.x + x_inc), (car.rect.y, car.rect.y + y_inc)))) ** 0.5", ((car.speed ** 2) + (2 * car.acceleration * distance((car.rect.x, car.rect.x + x_inc), (car.rect.y, car.rect.y + y_inc)))) ** 0.5)
                x = ((car.speed ** 2) + (2 * car.acceleration * distance((car.rect.x, car.rect.x + x_inc), (car.rect.y, car.rect.y + y_inc))))
                if x < 0:
                    x = 0
                car.speed = x ** 0.5
                print("AFTER new speed: ", car.speed)
            # print("A ({}, {})".format(x_inc, y_inc))
            # if x_inc < 1 or y_inc < 1:
            #     print("B ({}, {})".format(x_inc, y_inc))
            #     if x_inc != y_inc:
            #         print("C ({}, {})".format(x_inc, y_inc))
            #         if x_inc > y_inc:
            #             print("D ({}, {})".format(x_inc, y_inc))
            #             x_inc = 1
            #         else:
            #             print("E ({}, {})".format(x_inc, y_inc))
            #             y_inc = 1
            # print("F ({}, {})".format(x_inc, y_inc))
            # print("car: <{}> ticking (i, j): ({}, {})".format(car, x_inc, y_inc))


            self.check_collision(car, i_tick_dist=y_inc, j_tick_dist=x_inc)
            car.add_x(x_inc)
            car.add_y(y_inc)

    def check_collision(self, car, i_tick_dist=1, j_tick_dist=1):
        print("r", car.rect, "(i, j): ({}, {})".format(i_tick_dist, j_tick_dist))
        if not self.valid_place(car):
            if self.is_exiting(car, i_tick_dist=i_tick_dist, j_tick_dist=j_tick_dist):
                print("EXITING SUCCESSFULLY:", car)
                self.car_queue.remove(car)
            # crash
            else:
                print("i_tick_dist:", i_tick_dist, "j_tick_dist:", j_tick_dist)
                print("CRASH!\nBy:\n\t{} \non road:\n\t{}".format(car, self))
                raise ValueError("CRASH!")
        # check type of crash. with other car, or landscape
        elif self.check_car_crash(car):
            print("car crashed with another car")
            raise ValueError("CAR COLLISION")

    def center_car(self, car, lane=None, true_center=False):
        sr = self.rect
        cr = car.rect
        c = sr.center
        if true_center:
            car.set_rect(*c, cr.width, cr.height)
        else:
            # find center of lane and then place car there
            if self.lane_mode == "vertical":
                lw = sr.width / max(1, self.n_lanes)
                # print("before:\nw: {}\nlw: {}\ncr: {}\nsr: {}".format(sr.width, lw, cr, sr))
                if lane is not None and 0 <= lane <= self.n_lanes:
                    # print("lane is not None and 0 <= lane <= self.n_lanes", Rect(sr.x + (lw * (lane - 0.5)) - (cr.width / 2), car.rect.y, cr.width, cr.height))
                    car.set_rect(Rect(sr.x + (lw * (lane - 0.5)) - (cr.width / 2), car.rect.y, cr.width, cr.height))
                else:
                    inter = int((cr.x - sr.x) / sr.width)
                    # print("ELSE\ninter: {}".format(inter), Rect(sr.x + (lw * inter) + (lw / 2) - (cr.width / 2), car.rect.y, cr.width, cr.height))
                    car.set_rect(Rect(sr.x + (lw * inter) + (lw / 2) - (cr.width / 2), car.rect.y, cr.width, cr.height))

            elif self.lane_mode == "horizontal":
                lw = sr.height / max(1, self.n_lanes)
                # print("before:\nw: {}\nlw: {}\ncr: {}\nsr: {}".format(sr.height, lw, cr, sr))
                if lane is not None and 0 <= lane <= self.n_lanes:
                    # print("lane is not None and 0 <= lane <= self.n_lanes", Rect(sr.x + (lw * (lane - 0.5)) - (cr.width / 2), car.rect.y, cr.width, cr.height))
                    car.set_rect(Rect(cr.x, sr.y + (lw * (lane - 0.5)) - (cr.width / 2), cr.width, cr.height))
                else:
                    inter = int((cr.x - sr.x) / sr.width)
                    # print("ELSE\ninter: {}".format(inter), Rect(sr.x + (lw * inter) + (lw / 2) - (cr.width / 2), car.rect.y, cr.width, cr.height))
                    car.set_rect(Rect(cr.x, sr.y + (lw * inter) + (lw / 2) - (cr.width / 2), cr.width, cr.height))

            else:
                # todo: add diagonal support
                pass


    def info_print(self):
        print(dict_print({
            "direction": self.direction,
            "colour": self.colour,
            "rect": self.rect,
            "n_lanes": self.n_lanes,
            "centre_side": self.centre_side,
            "lane_mode": self.lane_mode,
            "lane_width": self.lane_width,
            "lane_height": self.lane_height
        }, "Roadway Information"))

    def __eq__(self, other):
        return isinstance(other, RoadWay) and all([
            self.rect == other.rect,
            self.direction == other.direction,
            self.colour == other.colour,
            self.n_lanes == other.n_lanes,
            self.lane_mode == other.lane_mode,
            self.centre_side == other.centre_side
        ])

    def __repr__(self):
        return "Roadway<<{}>, <{}>>".format(self.direction, self.rect)


class Intersection:

    def __init__(self, roadway_a, roadway_b, game, display, colour=BLACK):
        self.roadway_a = roadway_a
        self.roadway_b = roadway_b
        self.game = game
        self.display = display
        self.colour = colour

        rar = self.roadway_a.rect
        rbr = self.roadway_b.rect
        if not isinstance(rar, game.Rect):
            rar = game.Rect(*rar.tupl)
        if not isinstance(rbr, game.Rect):
            rbr = game.Rect(*rbr.tupl)
        self.rect = game.Rect.clip(rar, rbr)

    def draw_intersection(self, draw_stop_lines=True, stop_line_colour=WHITE, stop_line_width=6, draw_crosswalk=True,
                          crosswalk_colour=(GRAY_69)):
        # print("roadwayA:", self.roadway_a, "\n\tdir:", self.roadway_a.direction, "cen:", self.roadway_a.centre_side)
        # print("roadwayB:", self.roadway_b, "\n\tdir:", self.roadway_b.direction, "cen:", self.roadway_b.centre_side)
        dsa, dea = self.roadway_a.direction
        dsb, deb = self.roadway_b.direction
        cla = self.roadway_a.centre_side
        clb = self.roadway_b.centre_side
        r = self.rect
        sidewalk_pad = 3
        dist_to_stop_line = 6
        if draw_stop_lines:
            line = None
            if dsa == "S" or dsb == "S":
                if clb != "bottom":
                    # print("SOUTH")
                    self.game.draw.line(self.display, stop_line_colour,
                                        (r.left + sidewalk_pad, r.bottom + stop_line_width + dist_to_stop_line),
                                        (r.right - sidewalk_pad, r.bottom + stop_line_width + dist_to_stop_line),
                                        stop_line_width)
            if dsa == "W" or dsb == "W":
                if cla != "right":
                    # print("WEST")
                    self.game.draw.line(self.display, stop_line_colour,
                                        (r.right + stop_line_width + dist_to_stop_line, r.top + sidewalk_pad),
                                        (r.right + stop_line_width + dist_to_stop_line, r.bottom - sidewalk_pad),
                                        stop_line_width)
            if dsa == "N" or dsb == "N":
                if clb != "top":
                    # print("NORTH")
                    self.game.draw.line(self.display, stop_line_colour,
                                        (r.left + sidewalk_pad, r.top - stop_line_width - dist_to_stop_line),
                                        (r.right - sidewalk_pad, r.top - stop_line_width - dist_to_stop_line),
                                        stop_line_width)
            if dsa == "E" or dsb == "E":
                if cla != "left":
                    # print("EAST")
                    self.game.draw.line(self.display, stop_line_colour,
                                        (r.left - stop_line_width - dist_to_stop_line, r.top + sidewalk_pad),
                                        (r.left - stop_line_width - dist_to_stop_line, r.bottom - sidewalk_pad),
                                        stop_line_width)
        self.game.draw.rect(self.display, self.colour, self.rect)  # background

    def crosses(self):
        return sum(self.game.Rect.clip(self.roadway_a.rect, self.roadway_b.rect))

    def __eq__(self, other):
        if not isinstance(other, Intersection):
            return False
        return self.roadway_a == other.roadway_b and self.roadway_b == other.roadway_a or self.roadway_b == other.roadway_b and self.roadway_a == other.roadway_a


class TrafficSimulatorMap:
    def __init__(self, name, game, display, w, h):
        self.name = name
        self.game = game
        self.display = display
        self.w = w
        self.h = h
        self.roadways = {}
        self.intersections = []
        self.cars = {}
        self.car_id_num = 0
        self.clock_time = 0

    def add_stop_sign(self):
        pass

    def add_car(self, x, y, **kwargs):
        self.car_id_num += 1
        car = Car(self.game, self.display, self.car_id_num, x, y, **kwargs)
        r_name, roadway = None, None
        for r_name, roadway in self.roadways.items():
            if roadway.valid_place(car, strictly_inside=True):
                break
            else:
                roadway = None
        print("\n\tNew Car:", car, "\nSelecting roadway:", roadway)
        if roadway is not None:
            self.roadways[r_name].add_car(car)
            car.set_arrival(self.clock_time)
        else:
            raise ValueError(
                "Unable to place car object:\n<{car}>\non current tsmap:\n<{tsmap}>".format(car=car, tsmap=self))

        return car

    def get_new_car_id(self):
        self.car_id_num += 1
        return self.car_id_num

    def spawn_car(self, roadway_name, colour, name=None, img_path=None, is_circle=True, speed=1, acceleration=0.0, radius=None, width=None, height=None, center=None):
        if roadway_name not in self.roadways:
            raise ValueError("Unable to spawn a car on roadway <{}>\nbecause it has not been initialized yet.".format(roadway_name))
        id_num = self.get_new_car_id()
        return self.roadways[roadway_name].spawn_car(self.game, self.display, id_num, colour, name=name, img_path=img_path, is_circle=is_circle, speed=speed, acceleration=acceleration, radius=radius, width=width, height=height, center=center)

    def check_collisions(self):
        checked = {}
        for r_name, roadway in self.roadways.items():
            for car1 in roadway.car_queue:
                for r1_name, r1 in self.roadways.items():
                    if r_name != r1_name:
                        if str(car1) not in checked:
                            checked[str(car1)] = []
                        for car2 in r1.car_queue:
                            if str(car2) not in checked:
                                checked[str(car2)] = []
                            if str(car2) in checked[str(car1)] or str(car1) in checked[str(car2)]:
                                continue
                            if car1.rect.collide_rect(car2.rect, strictly_inside=False):
                                raise ValueError("\nCRASH!\nBy:\n\t{}\non road:\n\t{}\nAnd:\n\t{}\non road:\n\t{}".format(car1, roadway, car2, r1))
                            # else:
                                # print("no collision between: {} and {}".format(car1, car2))
                            checked[str(car1)].append(str(car2))
                            checked[str(car2)].append(str(car1))

    def update_intersections(self, colour=BLACK):
        intersections = []
        for ra_name, roadway_a in self.roadways.items():
            for rb_name, roadway_b in self.roadways.items():
                if ra_name != rb_name:
                    rect_a = self.game.Rect(*roadway_a.rect.tupl)
                    rect_b = self.game.Rect(*roadway_b.rect.tupl)
                    rect = self.game.Rect.clip(rect_a, rect_b)
                    if sum(rect.size):
                        inter = Intersection(roadway_a, roadway_b, self.game, self.display, colour=colour)
                        if inter not in intersections:
                            intersections.append(inter)
                            print("\n\troad a collides with road b: ({}, {})".format(ra_name, rb_name))
                    print("R:", rect, "SIZE:", rect.size)
        self.intersections = intersections

    def draw_roadways(self, draw_lane_lines=True, lane_line_colour=WHITE, draw_yellow_line=True,
                      yellow_line_colour=YELLOW_1__YELLOW_, yellow_line_width=3):
        for r_name, roadway in self.roadways.items():
            rect = roadway.rect
            if isinstance(rect, list) or isinstance(rect, tuple) and len(rect) == 4:
                rect = self.game.Rect(*rect)
            elif isinstance(rect, Rect):
                rect = self.game.Rect(*rect.tupl)
            else:
                raise ValueError("rect object: <{}> is not a valid pygame.Rect object.".format(rect))

            if draw_lane_lines:
                self.game.draw.rect(self.display, roadway.colour, rect)
                n_lanes = roadway.n_lanes
                lane_w = roadway.lane_width
                lane_h = roadway.lane_height
                for i in range(n_lanes - 1):
                    # print("dashed line:\n# lanes:", n_lanes, "\nlane_w:", lane_w, "\nlane_h:", lane_h, "\nmode:", roadway.lane_mode)
                    if roadway.lane_mode == "vertical":
                        dashed_line(self.game, self.display, lane_line_colour, ((rect.left + ((i + 1) * lane_w)), 0),
                                    ((rect.left + ((i + 1) * lane_w)), lane_h), 3, 26,
                                    seg_proportion=0.45)
                    elif roadway.lane_mode == "horizontal":
                        dashed_line(self.game, self.display, lane_line_colour, (0, rect.top + ((i + 1) * lane_w)),
                                    (rect.right, rect.top + ((i + 1) * lane_w)), 3, 26,
                                    seg_proportion=0.45)
            if draw_yellow_line:
                yellow_line = roadway.centre_side
                if yellow_line in ["top", "left"]:
                    if yellow_line == "top":
                        line = ((rect.left, rect.top), (rect.right, rect.top))
                    else:
                        line = ((rect.left, rect.top), (rect.left, rect.bottom))
                elif yellow_line in ["bottom", "right"]:
                    if yellow_line == "bottom":
                        line = ((rect.left, rect.bottom), (rect.right, rect.bottom))
                    else:
                        line = ((rect.right, rect.top), (rect.right, rect.bottom))
                else:
                    raise ValueError("Cannot display a yellow centre line on roadway: <{}>".format(roadway))

                self.game.draw.line(self.display, yellow_line_colour, *line, yellow_line_width)

    def draw_intersections(self, draw_stop_lines=True):
        for inter in self.intersections:
            inter.draw_intersection(draw_stop_lines)

    def draw_traffic(self):
        for r_name, roadway in self.roadways.items():
            for car in roadway.car_queue:
                car.draw()

    def draw_all(self):
        self.draw_roadways()
        self.draw_intersections()
        self.draw_traffic()

    def tick(self, tick=1.0):
        self.clock_time += tick
        print("clock time: {}".format(self.clock_time))
        spawn_one = False
        for i, r_name in enumerate(self.roadways):
            roadway = self.roadways[r_name]
            if spawn_one and self.clock_time % 150 == 40:
                lane_choice = choice(list(self.roadways))
                lane_choice = choice(["north bound", "south bound", "west bound", "east bound", "NORTH 2 bound", "WEST 2 bound"])
                self.spawn_car(lane_choice, BEIGE, center=1, acceleration=weighted_choice([(0.03, 3), (0.001, 4), (-0.01, 1), (0, 2)]))
                # self.spawn_car(lane_choice, BEIGE, center=1, acceleration=0.01)
                # self.spawn_car(lane_choice, BEIGE, acceleration=0.01)
                # self.spawn_car(lane_choice, BEIGE, radius=weighted_choice([(6, 8), (20, 2)]))
                # self.spawn_car("east bound", BEIGE)
                spawn_one = False
            roadway.tick(tick)
            print("cars in queue:", roadway.car_queue)
            if self.clock_time >= 25:
                for car in roadway.car_queue:
                    roadway.center_car(car, 2)
                    # print(car)
        self.check_collisions()

    @staticmethod
    def default_map(app):
        game = app.get_game()
        display = app.get_display()
        w, h = app.get_dims()
        tsmap = TrafficSimulatorMap("Default Map", game, display, w, h)
        app.set_background_colour(GRAY_60)

        ws, hs = 15, 15
        wc = w // ws
        hc = h // hs
        print("wc:", wc, "hc:", hc)
        for i in range(wc):
            game.draw.line(display, BLACK, (i * ws, 0), (i * ws, h))
        for i in range(hc):
            game.draw.line(display, BLACK, (0, i * hs), (w, i * hs))

        tsmap.roadways = {
            "south bound": RoadWay(("N", "S"), Rect(w * 0.39, 0, w * 0.11, h * 1), BLACK, n_lanes=2, centre_side="right"),
            "north bound": RoadWay(("S", "N"), Rect(w * 0.5, 0, w * 0.11, h * 1), BLACK, n_lanes=3, centre_side="left"),
            "east bound": RoadWay(("W", "E"), Rect(0, h * 0.5, w * 1, h * 0.11), BLACK, n_lanes=2, centre_side="top"),
            "west bound": RoadWay(("E", "W"), Rect(0, h * 0.39, w * 1, h * 0.11), BLACK, n_lanes=2, centre_side="bottom"),
            "NORTH 2 bound": RoadWay(("S", "N"), Rect(w * 0.76, 0, w * 0.11, h), BLACK, n_lanes=6, centre_side="left"),
            "WEST 2 bound": RoadWay(("E", "W"), Rect(0, h * 0.24, w * 1, h * 0.11), BLACK, n_lanes=2, centre_side="top")
        }
        print("START:", w * 0.40, ", ", h * 0.05)
        print("pygame collide:", pygame.rect.Rect(w * 0.39, 0, w * 0.11, h * 1).colliderect(pygame.rect.Rect(w * 0.41, h * 0.05, 6, 6)))
        print("rect collide:", Rect(w * 0.39, 0, w * 0.11, h * 1).collide_rect(Rect(w * 0.41, h * 0.05, 6, 6)))
        print("Car#1 should go on (\"N\", \"S\")")
        # car1 = tsmap.add_car(w * 0.42, h * 0.15, colour=RED)
        # car2 = tsmap.add_car(w * 0.56, h * 0.85, colour=MAGENTA_2)
        # car3 = tsmap.add_car(w * 0.66, h * 0.42, colour=INDIANRED_3)
        # car4 = tsmap.add_car(w * 0.15, h * 0.56, colour=PINK)
        tsmap.spawn_car("south bound", BEIGE)
        tsmap.spawn_car("north bound", RED)
        tsmap.spawn_car("east bound", BLUE_2)
        tsmap.spawn_car("west bound", GREEN)
        # tsmap.roadways["south bound"].center_car(car)
        # game.draw.rect(display, BLACK, (w * 0.39, 0, w * 0.22, h))  # North - South
        # game.draw.rect(display, BLACK, (0, h * 0.39, w, h * 0.22))  # East - West
        #
        # # stop lines
        # game.draw.line(display, WHITE, (w * 0.39, h * 0.35), (w * 0.5, h * 0.35), 3)  # north
        # game.draw.line(display, WHITE, (w * 0.5, h * 0.65), (w * 0.61, h * 0.65), 3)  # south
        # game.draw.line(display, WHITE, (w * 0.35, h * 0.5), (w * 0.35, h * 0.61), 3)  # east
        # game.draw.line(display, WHITE, (w * 0.65, h * 0.39), (w * 0.65, h * 0.5), 3)  # west
        #
        # # centre lines
        # game.draw.line(display, YELLOW_2, (w * 0.5, 0), (w * 0.5, h * 0.35), 3)  # north
        # game.draw.line(display, YELLOW_2, (w * 0.5, h * 0.65), (w * 0.5, h), 3)  # south
        # game.draw.line(display, YELLOW_2, (0, h * 0.5), (w * 0.35, h * 0.5), 3)  # east
        # game.draw.line(display, YELLOW_2, (w * 0.65, h * 0.5), (w, h * 0.5), 3)  # west
        #
        # # lane lines
        # dashed_line(game, display, WHITE, (w * 0.555, 0), (w * 0.555, h * 0.35), 3, 8, seg_proportion=0.45)  # north-north
        # dashed_line(game, display, WHITE, (w * 0.445, 0), (w * 0.445, h * 0.35), 3, 8, seg_proportion=0.45)  # south-north
        # dashed_line(game, display, WHITE, (w * 0.555, h * 0.65), (w * 0.555, h), 3, 8, seg_proportion=0.45)  # north-south
        # dashed_line(game, display, WHITE, (w * 0.445, h * 0.65), (w * 0.445, h), 3, 8, seg_proportion=0.45)  # south-south
        # dashed_line(game, display, WHITE, (0, h * 0.445), (w * 0.35, h * 0.445), 3, 8, seg_proportion=0.45)  # east-east
        # dashed_line(game, display, WHITE, (0, h * 0.555), (w * 0.35, h * 0.555), 3, 8, seg_proportion=0.45)  # west-east
        # dashed_line(game, display, WHITE, (w * 0.65, h * 0.445), (w, h * 0.445), 3, 8, seg_proportion=0.45)  # east-west
        # dashed_line(game, display, WHITE, (w * 0.65, h * 0.555), (w, h * 0.555), 3, 8, seg_proportion=0.45)  # west-west
        # # game.draw.line(display, WHITE, (w * 0.445, 0), (w * 0.445, h * 0.35))  # north-north
        # # game.draw.line(display, WHITE, (w * 0.5, h * 0.65), (w * 0.5, h), 3)  # south
        # # game.draw.line(display, WHITE, (0, h * 0.5), (w * 0.35, h * 0.5), 3)  # east
        # # game.draw.line(display, WHITE, (w * 0.65, h * 0.5), (w, h * 0.5), 3)  # west

        # Draw buildings
        b1 = (RED, (0, 0, w * 0.35, h * 0.35))
        b2 = (YELLOW_2, (w * 0.65, 0, w * 0.35, h * 0.35))
        b3 = (ORANGE, (0, h * 0.65, w * 0.35, h * 0.35))
        b4 = (GREEN, (w * 0.65, h * 0.65, w * 0.35, h * 0.35))
        game.draw.rect(display, *b1)
        game.draw.rect(display, *b2)
        game.draw.rect(display, *b3)
        game.draw.rect(display, *b4)
        #
        # # dashed_line(game, display, HOTPINK, (0, 0), (w, 0), 3, 35, seg_proportion=0.9)
        # # dashed_line(game, display, PURPLE, (0, 0), (w, h), 3, 35, seg_proportion=0.9)

        tsmap.update_intersections()
        # tsmap.draw_roadways()
        # tsmap.draw_intersections()
        tsmap.draw_all()

        return tsmap


class TrafficSimulator(PygameApplication):

    def __init__(self, title, w, h):
        super().__init__(title, w, h)
        self.init()
        self.w = w
        self.h = h
        self.map_obj = TrafficSimulatorMap.default_map(super())

    def set_map(self, map_obj):
        assert isinstance(map_obj, TrafficSimulatorMap)
        self.map_obj = map_obj

    def run(self, fps=60):
        fps = max(4, min(1000, fps))
        tick_time=1
        while self.is_playing:
            self.tick(fps)
            print("T", self.clock.get_time(), "T", self.clock.get_rawtime())
            if self.clock.get_rawtime() % fps == 0:
                self.map_obj.tick(tick_time)
                self.map_obj.draw_all()
                super().run()


if __name__ == '__main__':
    app = TrafficSimulator("app", 900, 600)
    app.run()

from pygame_application import *
from colour_utility import *
from pygame_utility import *


class Car:

    # Note x, y are coordinates of the centre of the car, not top-left.
    def __init__(self, game, display, id_num, x, y, speed=1, name="car", colour=BLACK, img_path=None, is_circle=True,
                 radius=6):
        self.game = game
        self.display = display
        self.speed = speed
        self.id_num = id_num
        self.name = name
        self.colour = colour
        self.img_path = img_path
        self.is_circle = is_circle
        self.radius = radius
        self.w = radius
        self.h = radius
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
        return "car<#{}, {}>".format(self.id_num, self.rect)


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
        for c in self.car_queue:
            if c != car:
                if c.rect.collide_rect(car.rect, strictly_inside=strictly_inside):
                    print("\t\tlate exit")
                    return False
        return True

    def is_exiting(self, car):
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
        top_o = top_i.translated(0, -1)
        bottom_o = bottom_i.translated(0, 1)
        left_o = left_i.translated(-1, 0)
        right_o = right_i.translated(1, 0)
        car_r = car.rect
        # lm = lambda v, vs: (v[0] + vs[0], v[1] + vs[1])
        # top = Line(*lm(a, (-1, -1)), *lm(b, (1, -1)))
        # bottom = Line(*lm(c, (-1, 1)), *lm(d, (1, 1)))
        # left = Line(*lm(a, (-1, -1)), *lm(c, (-1, 1)))
        # right = Line(*lm(b, (1, -1)), *lm(d, (1, 1)))
        ie = False
        if self.lane_mode == "vertical":
            ie = not self.valid_place(car) and (((car_r.collide_line(top_o) and not car_r.collide_line(top_i)) or (car_r.collide_line(bottom_o) and not car_r.collide_line(bottom_i))))
        if self.lane_mode == "vertical":
            ie = not self.valid_place(car) and (((car_r.collide_line(left_o) and not car_r.collide_line(left_i)) or (car_r.collide_line(right_o) and not car_r.collide_line(right_i))))
        print(dict_print({
            "car": car.rect,
            "self": self.rect,
            "self.dir": str(self.direction),
            "top_i": "{} <{}>".format(top_i, car_r.collide_line(top_i)),
            "top_o": "{} <{}>".format(top_o, car_r.collide_line(top_o)),
            "bottom_i": "{} <{}>".format(bottom_i, car_r.collide_line(bottom_i)),
            "bottom_o": "{} <{}>".format(bottom_o, car_r.collide_line(bottom_o)),
            "Cto && ~Cti": "{}".format(car_r.collide_line(top_o) and not car_r.collide_line(top_i)),
            "Cbo && ~Cbi": "{}".format(car_r.collide_line(bottom_o) and not car_r.collide_line(bottom_i)),
            "Cbo && ~Cbi || Cbo && ~Cbi": "{}".format((car_r.collide_line(top_o) and not car_r.collide_line(top_i)) or (car_r.collide_line(bottom_o) and not car_r.collide_line(bottom_i))),

            "left_i": "{} <{}>".format(left_i, car_r.collide_line(left_i)),
            "left_o": "{} <{}>".format(left_o, car_r.collide_line(left_o)),
            "right_i": "{} <{}>".format(right_i, car_r.collide_line(right_i)),
            "right_o": "{} <{}>".format(right_o, car_r.collide_line(right_o)),
            "Clo && ~Cli": "{}".format(car_r.collide_line(left_o) and not car_r.collide_line(left_i)),
            "Cro && ~Cri": "{}".format(car_r.collide_line(right_o) and not car_r.collide_line(right_i)),
            "Clo && ~Cli || Cro && ~Cri": "{}".format((car_r.collide_line(left_o) and not car_r.collide_line(left_i)) or (car_r.collide_line(right_o) and not car_r.collide_line(right_i))),
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
        if self.lane_mode == "vertical":
            return not self.valid_place(car) and (((car_r.collide_line(top_o) and not car_r.collide_line(top_i)) or (car_r.collide_line(bottom_o) and not car_r.collide_line(bottom_i))))
        elif self.lane_mode == "horizontal":
            return not self.valid_place(car) and (((car_r.collide_line(left_o) and not car_r.collide_line(left_i)) or (car_r.collide_line(right_o) and not car_r.collide_line(right_i))))
        else:
            raise ValueError("diagonal roadways not supported yet.")

    def add_car(self, car):
        assert isinstance(car, Car)
        self.car_queue.append(car)

    def tick(self, tick):
        for car in self.car_queue:
            i_inc = DIRECTIONS[self.direction[1]]["i"] * car.speed * tick
            j_inc = DIRECTIONS[self.direction[1]]["j"] * car.speed * tick
            if i_inc < 1 or j_inc < 1:
                if i_inc != j_inc:
                    if i_inc > j_inc:
                        i_inc = 1
                    else:
                        j_inc = 1
            car.add_x(j_inc)
            car.add_y(i_inc)

            self.check_collision(car)

    def check_collision(self, car):
        # print("r", car.rect, "(i, j): ({}, {})".format(i_inc, j_inc))
        if not self.valid_place(car):
            if self.is_exiting(car):
                print("EXITING SUCCESSFULLY:", car)
                self.car_queue.remove(car)
            # crash
            else:
                print("CRASH!\nBy:\n\t{} \non road:\n\t{}".format(car, self))
                raise ValueError("CRASH!")

    def center_car(self, car, true_center=False):
        sr = self.rect
        cr = car.rect
        c = sr.center
        if true_center:
            car.set_rect(*c, cr.width, cr.height)
        else:


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
        for r_name, roadway in self.roadways.items():
            roadway.tick(tick)

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
            "east bound": RoadWay(("W", "E"), Rect(0, h * 0.39, w * 1, h * 0.11), BLACK, n_lanes=2, centre_side="bottom"),
            "west bound": RoadWay(("E", "W"), Rect(0, h * 0.5, w * 1, h * 0.11), BLACK, n_lanes=3, centre_side="top")
        }
        print("START:", w * 0.40, ", ", h * 0.05)
        print("pygame collide:", pygame.rect.Rect(w * 0.39, 0, w * 0.11, h * 1).colliderect(pygame.rect.Rect(w * 0.41, h * 0.05, 6, 6)))
        print("rect collide:", Rect(w * 0.39, 0, w * 0.11, h * 1).collide_rect(Rect(w * 0.41, h * 0.05, 6, 6)))
        print("Car#1 should go on (\"N\", \"S\")")
        tsmap.add_car(w * 0.42, h * 0.15, colour=RED)
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

    def run(self):
        tick_time = 1000
        tick_time = 100
        tick_time = max(4, min(1000, tick_time))
        while self.is_playing:
            self.tick(tick_time)
            self.map_obj.tick(tick_time)
            self.map_obj.draw_all()
            super().run()


if __name__ == '__main__':
    app = TrafficSimulator("app", 900, 600)
    app.run()

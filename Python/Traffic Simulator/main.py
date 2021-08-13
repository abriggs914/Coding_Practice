from pygame_application import *
from colour_utility import *
from pygame_utility import *


class RoadWay:

    def __init__(self, direction, rect, colour, n_lanes=1, centre_side="left"):
        self.rect = rect
        assert (isinstance(direction, list) or isinstance(direction, tuple)) and all([direct in DIRECTIONS for direct in direction])
        # TODO; include diagonal roadway functionality
        assert any([direction == ("N", "S"), direction == ("S", "N"), direction == ("E", "W"), direction == ("W", "E")])
        assert any([centre_side == "left", centre_side == "right", centre_side == "top", centre_side == "bottom"])
        self.direction = direction  # tuple rough directionality vie pygame_utility directions ex: ("N", "S")
        self.colour = colour
        self.n_lanes = n_lanes
        self.lane_mode = "diagonal"
        self.centre_side = centre_side  # left == top, right == bottom

        if direction == ("N", "S") or direction == ("S", "N"):
            self.lane_width = rect[2] / n_lanes
            self.lane_height = rect[3]
            self.lane_mode = "vertical"
        elif direction == ("E", "W") or direction == ("W", "E"):
            self.lane_width = rect[3] / n_lanes
            self.lane_height = rect[2]
            self.lane_mode = "horizontal"

        self.info_print()

    def info_print(self):
        print(dict_print({
            "direction": self.direction,
            "colour": self.colour,
            "n_lanes": self.n_lanes,
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
            self.lane_mode == other.lane_mode
        ])


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
            rar = game.Rect(*rar)
        if not isinstance(rbr, game.Rect):
            rbr = game.Rect(*rbr)
        self.rect = game.Rect.clip(rar, rbr)

    def draw_intersection(self, draw_stop_lines=True, stop_line_colour=WHITE, stop_line_width=4, draw_crosswalk=True, crosswalk_colour=(GRAY_69)):
        print("roadwayA:", self.roadway_a, "\n\tdir:", self.roadway_a.direction)
        print("roadwayB:", self.roadway_b, "\n\tdir:", self.roadway_b.direction)
        dsa, dea = self.roadway_a.direction
        dsb, deb = self.roadway_b.direction
        r = self.rect
        if draw_stop_lines:
            line = None
            if dsa == "S" or dsb == "S":
                print("SOUTH")
                self.game.draw.line(self.display, RED, (r.left + 2, r.bottom + stop_line_width), (r.right - 2, r.bottom + stop_line_width), stop_line_width)
            if dsa == "W" or dsb == "W":
                print("WEST")
                self.game.draw.line(self.display, GREEN, (r.right + stop_line_width, r.top + 2), (r.right + stop_line_width, r.bottom - 2), stop_line_width)
            if dsa == "N" or dsb == "N":
                print("NORTH")
                self.game.draw.line(self.display, BLUE, (r.left + 2, r.top - stop_line_width), (r.right - 2, r.top - stop_line_width), stop_line_width)
            if dsa == "E" or dsb == "E":
                print("EAST")
                self.game.draw.line(self.display, PURPLE, (r.left - stop_line_width, r.top + 2), (r.left - stop_line_width, r.bottom - 2), stop_line_width)
        self.game.draw.rect(self.display, self.colour, self.rect)  # background

    def crosses(self):
        return sum(self.game.Rect.clip(self.roadway_a.rect, self. roadway_b.rect))

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

    def add_stop_sign(self):
        pass

    def update_intersections(self, colour=BLACK):
        intersections = []
        for ra_name, roadway_a in self.roadways.items():
            for rb_name, roadway_b in self.roadways.items():
                if ra_name != rb_name:
                    rect_a = self.game.Rect(*roadway_a.rect)
                    rect_b = self.game.Rect(*roadway_b.rect)
                    rect = self.game.Rect.clip(rect_a, rect_b)
                    if sum(rect.size):
                        inter = Intersection(roadway_a, roadway_b, self.game, self.display, colour=random_colour())
                        if inter not in intersections:
                            intersections.append(inter)
                            print("\n\troad a collides with road b: ({}, {})".format(ra_name, rb_name))
                    print("R:", rect, "SIZE:", rect.size)
        self.intersections = intersections

    def draw_roadways(self, draw_lane_lines=True, lane_line_colour=WHITE, draw_yellow_line=True, yellow_line_colour=YELLOW_1__YELLOW_, yellow_line_width=3):
        for r_name, roadway in self.roadways.items():
            rect = roadway.rect
            if isinstance(rect, list) or isinstance(rect, tuple) and len(rect) == 4:
                rect = self.game.Rect(*rect)
            else:
                raise ValueError("rect object: <{}> is not a valid pygame.Rect object.")

            if draw_lane_lines:
                self.game.draw.rect(self.display, roadway.colour, rect)
                n_lanes = roadway.n_lanes
                lane_w = roadway.lane_width
                lane_h = roadway.lane_height
                for i in range(n_lanes - 1):
                    print("dashed line:\n# lanes:", n_lanes, "\nlane_w:", lane_w, "\nlane_h:", lane_h, "\nmode:", roadway.lane_mode)
                    if roadway.lane_mode == "vertical":
                        dashed_line(self.game, self.display, lane_line_colour, ((rect.left + ((i + 1) * lane_w)), 0), ((rect.left + ((i + 1) * lane_w)), lane_h), 3, 26,
                            seg_proportion=0.45)
                    elif roadway.lane_mode == "horizontal":
                        dashed_line(self.game, self.display, lane_line_colour, (0, rect.top + ((i + 1) * lane_w)), (rect.right, rect.top + ((i + 1) * lane_w)), 3, 26,
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

    def draw_intersections(self):
        for inter in self.intersections:
            inter.draw_intersection(draw_stop_lines=True)

    def draw_all(self):
        self.draw_roadways()
        self.draw_intersections()


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
            "south bound": RoadWay(("N", "S"), (w * 0.39, 0, w * 0.11, h * 1), BLACK, n_lanes=2, centre_side="right"),
            "north bound": RoadWay(("S", "N"), (w * 0.5, 0, w * 0.11, h * 1), BLACK, n_lanes=3, centre_side="left"),
            "east bound": RoadWay(("W", "E"), (0, h * 0.39, w * 1, h * 0.11), BLACK, n_lanes=2, centre_side="bottom"),
            "west bound": RoadWay(("E", "W"), (0, h * 0.5, w * 1, h * 0.11), BLACK, n_lanes=3, centre_side="top")
        }
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
        super().run()


if __name__ == '__main__':
    app = TrafficSimulator("app", 900, 600)
    app.run()

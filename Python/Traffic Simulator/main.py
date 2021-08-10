from pygame_application import *
from colour_utility import *

class TrafficSimulatorMap:
    def __init__(self, name, game, display, w, h):
        self.name = name
        self.game = game
        self.display = display
        self.w = w
        self.h = h
        self.roadways = {}

    def add_stop_sign(self):

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

        game.draw.rect(display, BLACK, (w * 0.39, 0, w * 0.22, h))
        game.draw.rect(display, BLACK, (0, h * 0.39, w, h * 0.22))

        # stop lines
        game.draw.line(display, WHITE, (w * 0.39, h * 0.35), (w * 0.5, h * 0.35), 3)  # north
        game.draw.line(display, WHITE, (w * 0.5, h * 0.65), (w * 0.61, h * 0.65), 3)  # south
        game.draw.line(display, WHITE, (w * 0.35, h * 0.5), (w * 0.35, h * 0.61), 3)  # east
        game.draw.line(display, WHITE, (w * 0.65, h * 0.39), (w * 0.65, h * 0.5), 3)  # west

        # centre lines
        game.draw.line(display, YELLOW_2, (w * 0.5, 0), (w * 0.5, h * 0.35), 3)  # north
        game.draw.line(display, YELLOW_2, (w * 0.5, h * 0.65), (w * 0.5, h), 3)  # south
        game.draw.line(display, YELLOW_2, (0, h * 0.5), (w * 0.35, h * 0.5), 3)  # east
        game.draw.line(display, YELLOW_2, (w * 0.65, h * 0.5), (w, h * 0.5), 3)  # west

        # lane lines
        dashed_line(game, display, WHITE, (w * 0.555, 0), (w * 0.555, h * 0.35), 3, 8, seg_proportion=0.45)  # north-north
        dashed_line(game, display, WHITE, (w * 0.445, 0), (w * 0.445, h * 0.35), 3, 8, seg_proportion=0.45)  # south-north
        dashed_line(game, display, WHITE, (w * 0.555, h * 0.65), (w * 0.555, h), 3, 8, seg_proportion=0.45)  # north-south
        dashed_line(game, display, WHITE, (w * 0.445, h * 0.65), (w * 0.445, h), 3, 8, seg_proportion=0.45)  # south-south
        dashed_line(game, display, WHITE, (0, h * 0.445), (w * 0.35, h * 0.445), 3, 8, seg_proportion=0.45)  # east-east
        dashed_line(game, display, WHITE, (0, h * 0.555), (w * 0.35, h * 0.555), 3, 8, seg_proportion=0.45)  # west-east
        dashed_line(game, display, WHITE, (w * 0.65, h * 0.445), (w, h * 0.445), 3, 8, seg_proportion=0.45)  # east-west
        dashed_line(game, display, WHITE, (w * 0.65, h * 0.555), (w, h * 0.555), 3, 8, seg_proportion=0.45)  # west-west
        # game.draw.line(display, WHITE, (w * 0.445, 0), (w * 0.445, h * 0.35))  # north-north
        # game.draw.line(display, WHITE, (w * 0.5, h * 0.65), (w * 0.5, h), 3)  # south
        # game.draw.line(display, WHITE, (0, h * 0.5), (w * 0.35, h * 0.5), 3)  # east
        # game.draw.line(display, WHITE, (w * 0.65, h * 0.5), (w, h * 0.5), 3)  # west

        b1 = (RED, (0, 0, w * 0.35, h * 0.35))
        b2 = (YELLOW_2, (w * 0.65, 0, w * 0.35, h * 0.35))
        b3 = (ORANGE, (0, h * 0.65, w * 0.35, h * 0.35))
        b4 = (GREEN, (w * 0.65, h * 0.65, w * 0.35, h * 0.35))
        game.draw.rect(display, *b1)
        game.draw.rect(display, *b2)
        game.draw.rect(display, *b3)
        game.draw.rect(display, *b4)

        # dashed_line(game, display, HOTPINK, (0, 0), (w, 0), 3, 35, seg_proportion=0.9)
        # dashed_line(game, display, PURPLE, (0, 0), (w, h), 3, 35, seg_proportion=0.9)
        return tsmap


class TrafficSimulator(PygameApplication):

    def __init__(self, title, w, h):
        super().__init__(title, w, h)
        self.init()
        self.w = w
        self.h = h
        self.map_obj = TrafficSimulatorMap.default_map(super())

    def set_map(self, map_obj):
        self.map = map_obj

    def run(self):
        super().run()


if __name__ == '__main__':
    app = TrafficSimulator("app", 900, 600)
    app.run()

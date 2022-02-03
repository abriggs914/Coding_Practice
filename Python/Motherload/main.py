from vehicle import *
from grid import *
from pygame_utility import *

PYGAME_EVENT_KEYDOWN = 768
PYGAME_EVENT_KEYUP = 769

PYGAME_KEY_ARROW_UP = 1073741906
PYGAME_KEY_ARROW_RIGHT = 1073741903
PYGAME_KEY_ARROW_DOWN = 1073741905
PYGAME_KEY_ARROW_LEFT = 1073741904


class MotherloadGame:

    def __init__(self):
        self.grid = None
        self.view_rect = None
        self.view_rect_w = 25
        self.view_rect_h = 18

        self.app = PygameApplication("Name Goes Here!", 750, 500)
        self.game = self.app.get_game()
        self.display = self.app.display

        self.drawing_rect = self.game.Rect(25, 25, 700, 450)
        self.drawing_rect_colour = GRAY_45
        self.tile_border_width = 1

    def set_grid(self, grid):
        assert isinstance(grid, Grid)
        self.grid = grid
        self.update_view_rect()

    def main_loop(self):
        app = self.app
        game = self.game
        display = self.display

        while app.is_playing:
            display.fill(BLACK)

            # draw widgets and objects here
            game.draw.rect(display, self.drawing_rect_colour, self.drawing_rect)

            tiles_list = self.grid.tiles
            ix, iy = self.drawing_rect.topleft
            # draw tiles:
            xb1, yb1, xbd, ybd = self.view_rect
            xb2 = xb1 + xbd
            yb2 = yb1 + ybd
            tbw = self.tile_border_width
            # print("\t\t(xb1: {}, xb2: {}, xbd: {}, yb1: {}, yb2 {}, ybd: {})".format(xb1, xb2, xbd, yb1, yb2, ybd))
            th = self.drawing_rect.height / len(tiles_list[yb1: yb2 + 1])
            for i, row in enumerate(tiles_list[yb1: yb2 + 1]):
                tw = self.drawing_rect.width / len(row[xb1: xb2 + 1])
                for j, tile in enumerate(row[xb1: xb2 + 1]):
                    tile_rect = game.Rect(ix + (j * tw) + tbw, iy + (i * th) + tbw, tw - (2 * tbw), th - (2 * tbw))
                    game.draw.rect(display, tile.colour, tile_rect)

            event_queue = app.run()
            for event in event_queue:
                # handle events
                # print("Event:", event, event.type)
                if event.type == PYGAME_EVENT_KEYDOWN:
                    dx, dy = 0, 0
                    if event.key == PYGAME_KEY_ARROW_UP:
                        dy = -1
                    elif event.key == PYGAME_KEY_ARROW_LEFT:
                        dx = -1
                    elif event.key == PYGAME_KEY_ARROW_DOWN:
                        dy = 1
                    elif event.key == PYGAME_KEY_ARROW_RIGHT:
                        dx = 1

                    vehicle, cvy, cvx = g1.get_active_vehicle()
                    cvy += dy
                    cvx += dx
                    rows = g1.grid_data_in["height"]
                    cols = g1.grid_data_in["width"]
                    cvy = 0 if cvy < 0 else (rows - 1 if cvy >= rows else cvy)
                    cvx = 0 if cvx < 0 else (cols - 1 if cvx >= cols else cvx)
                    g1.set_vehicle(vehicle, (cvx, cvy))
                    self.update_view_rect()

                    os.system('cls' if os.name == 'nt' else 'clear')
                    # g1.print_tile_symbols()
                    print("mgl:", self.view_rect)
                    # print("VIEW:", "\n".join([str(row) for row in self.grid.tiles[self.view_rect[1]:self.view_rect[3]]]))
                    # print("VIEW:", "\n".join([str(row[self.view_rect[0]:self.view_rect[3]]) for row in self.grid.tiles[self.view_rect[1]:self.view_rect[3]]]))
                # if event[:4]
            polled = game.event.poll()
            if str(polled) != "<Event(0-NoEvent {})>":
                print("peeking:", polled)
        app.clock.tick(30)

    def update_view_rect(self):
        v, cy, cx = self.grid.get_active_vehicle()

        if v is None:
            cy, cx = self.grid.grid_data_in["width"] // 2, self.grid.grid_data_in["ground_level"]

        print("update_view_rect: ({}, {})".format(cx, cy))

        self.view_rect = (
            max(0, min(cx - (self.view_rect_w // 2), self.grid.grid_data_in["width"] - self.view_rect_w)),
            max(0, min(cy - (self.view_rect_h // 2), self.grid.grid_data_in["height"] - self.view_rect_h)),
            self.view_rect_w,
            self.view_rect_h
        )

        # self.view_rect = (
        #     max(0, (cx - (self.grid.grid_data_in["width"] // 2))),
        #     max(0, (cy - (self.grid.grid_data_in["height"] // 2))),
        #     self.view_rect_w,
        #     self.view_rect_h
        # )



if __name__ == '__main__':
    t1 = Vehicle(1, "Tank", None, GREEN)
    grid_data_template = [
            "width",
            "height",
            "ground_level",
            "shop_pos",
            "fuel_station_pos",
            "spawn_pos",
            "gem_data"
    ]
    gd1 = GemDiamond(SILVER, 16)
    gq1 = GemQuartz(BROWN_4, 6)
    gi1 = GemIron(GRAY_27, 8)
    g1 = Grid(1, "Grid 1", dict(zip(
        grid_data_template,
        [
            100,
            100,
            12,
            (75, 12),
            (60, 12),
            (25, 12),
            [
                {
                    "gem": gd1,
                    "probability": 0.002,
                    "min_depth": 30,
                    "max_depth": 1000
                },
                {
                    "gem": gq1,
                    "probability": 0.006,
                    "min_depth": 12,
                    "max_depth": 1000
                },
                {
                    "gem": gi1,
                    "probability": 0.01,
                    "min_depth": 12,
                    "max_depth": 1000
                }
            ]
        ]
    )))
    # g1.add_gem(gd1, (45, 45))
    # g1.add_gem(gd1, (45, 45))
    # print("grid.tiles:", g1.tiles)

    g1.set_vehicle(t1, (50, 10))
    g1.print_tile_symbols()
    mlg = MotherloadGame()
    mlg.set_grid(g1)

    mlg.main_loop()

# tank
# - drill
# - hull
# - storage
# - propeller
# - fuel tank
# grid
# gems
# shop
# fuel
# fuel station


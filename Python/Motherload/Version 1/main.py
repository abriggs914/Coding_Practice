from vehicle import *
from grid import *
from pygame_utility import *

PYGAME_EVENT_KEYDOWN = 768
PYGAME_EVENT_KEYUP = 769

# PYGAME_KEY_ARROW_UP = 1073741906
# PYGAME_KEY_ARROW_RIGHT = 1073741903
# PYGAME_KEY_ARROW_DOWN = 1073741905
# PYGAME_KEY_ARROW_LEFT = 1073741904


class MotherloadGame:

    def __init__(self):
        self.grid = None

        self.app = PygameApplication("Name Goes Here!", 750, 500)
        self.game = self.app.get_game()
        self.display = self.app.display

    def set_grid(self, grid):
        assert isinstance(grid, Grid)
        self.grid = grid
        if self.grid.is_init:
            raise ValueError("This Grid has already been initialized.")
        self.grid.init(self.game, self.display)
        # self.update_view_rect()

    def max_ceil(self, n):
        an = ceil(abs(n))
        return an if n >= 0 else -an

    def main_loop(self):
        app = self.app
        game = self.game
        display = self.display
        t_sec = self.grid.grid_data_in["tick_time"]

        dx, dy = 0, 0
        vehicle, cvx, cvy = self.grid.get_active_vehicle()
        print("vehicle:", vehicle)

        while app.is_playing:
            display.fill(BLACK)
            vehicle, cvx, cvy = self.grid.get_active_vehicle()

            # draw widgets and objects here

            # Background
            game.draw.rect(display, self.grid.drawing_rect_colour, self.grid.drawing_rect)

            # Grid Tiles
            tiles = self.grid.get_drawing_tiles()
            for i, tile_row in enumerate(tiles):
                for j, tile in enumerate(tile_row):
                    # print("rect ({}, {}):".format(i, j), tile.rect)
                    game.draw.rect(display, tile.colour, tile.rect)

            # Draw vehicle
            # vehicle, vx, vy = self.grid.get_active_vehicle()
            print("drawing vehicle:", vehicle.rect, "x: {}, maxx:{}, y: {}, maxy:{}, Tile: {}".format(vehicle.x_vel, vehicle.x_vel_max, vehicle.y_vel, vehicle.y_vel_max, self.grid.tile_at_x_y(cvx, cvy)))
            game.draw.rect(display, vehicle.colour, vehicle.rect)

            # Handle Events
            change_x, change_y = vehicle.x_vel, vehicle.y_vel
            event_queue = app.run()
            for event in event_queue:
                if event.type == pygame.KEYDOWN:
                    k = event.key
                    if k == game.K_UP or k == game.K_w:
                        dy = -vehicle.y_acc
                    elif k == game.K_LEFT or k == game.K_a:
                        dx = -vehicle.x_acc
                    elif k == game.K_DOWN or k == game.K_s:
                        dy = vehicle.y_acc
                    elif k == game.K_RIGHT or k == game.K_d:
                        dx = vehicle.x_acc
                elif event.type == pygame.KEYUP:
                    if event.key in (game.K_UP, game.K_DOWN, game.K_w, game.K_s):
                        dy = 0
                    if event.key in (game.K_LEFT, game.K_RIGHT, game.K_a, game.K_d):
                        dx = 0

            # print("dx: {}, dy: {}".format(dx, dy))
            change_x += dx
            change_y += dy
            if abs(change_x) >= vehicle.x_vel_max:  # If max_speed is exceeded.
                # Normalize the x_change and multiply it with the max_speed.
                change_x = change_x/abs(change_x) * vehicle.x_vel_max

            if abs(change_y) >= vehicle.y_vel_max:  # If max_speed is exceeded.
                # Normalize the x_change and multiply it with the max_speed.
                change_y = change_y/abs(change_y) * vehicle.y_vel_max

            # Decelerate if no key is pressed.
            if dx == 0:
                change_x *= vehicle.x_acc_d
            if dy == 0:
                change_y *= vehicle.y_acc_d

            cvx += change_x
            cvy += change_y
            vehicle.x_vel = change_x
            vehicle.y_vel = change_y
            # self.grid.set_vehicle(vehicle, (cvx, cvy))




            # # Handle Keys
            # pressed = game.key.get_pressed()
            # dir_keys = [game.K_UP, game.K_LEFT, game.K_DOWN, game.K_RIGHT, game.K_w, game.K_a, game.K_s, game.K_d]
            # pressed_a_key = False
            # for k in dir_keys:
            #     if pressed[k]:
            #         pressed_a_key = True
            #         if k == game.K_UP:
            #             dy += -vehicle.y_acc
            #         elif k == game.K_LEFT:
            #             dx += -vehicle.x_acc
            #         elif k == game.K_DOWN:
            #             dy += vehicle.y_acc
            #         elif k == game.K_RIGHT:
            #             dx += vehicle.x_acc
            #         elif k == game.K_w:
            #             dy += -vehicle.y_acc
            #         elif k == game.K_a:
            #             dx += -vehicle.x_acc
            #         elif k == game.K_s:
            #             dy += vehicle.y_acc
            #         elif k == game.K_d:
            #             dx += vehicle.x_acc
            #
            # cvx, cvy = vehicle.rect.center
            #
            # # Apply vehicle movement
            # if not pressed_a_key:
            #     # Free fall, apply gravity
            #     vehicle.set_falling()
            #
            # gravity = self.grid.grid_data_in["gravity"]
            # x_vel = vehicle.x_vel
            # y_vel = vehicle.y_vel
            #
            # vehicle.x_acc = dx
            # vehicle.y_acc = dy
            # x_acc = vehicle.x_acc
            # y_acc = vehicle.y_acc
            #
            # # dx *= abs(x_vel)
            # # dy *= abs(y_vel)
            #
            # mf = 1
            # vehicle.x_vel = self.max_ceil(((x_vel * (t_sec / mf)) + (0.5 * x_acc * ((t_sec / mf) ** 2))) / 1000)
            # vehicle.y_vel = self.max_ceil(((y_vel * (t_sec / mf)) + (0.5 * y_acc * ((t_sec / mf) ** 2))) / 1000)
            # dx = vehicle.x_vel * (t_sec / mf)
            # dy = vehicle.y_vel * (t_sec / mf)
            #
            # # convert cvx, cvy, dx, and dy back to ij tiles coordinates from xy grid coordinates.
            # cvy += dy
            # cvx += dx


            # # print("1, (cvx, cvy): ({}, {}), (dx, dy): ({}, {}), (x_vel, y_vel): ({}, {}), (x_acc, y_acc): ({}, {}), (nx_vel, vy_vel): ({}, {}), self.grid.r_c_at_x_y({}), d.rect: {}, t.rect: {}".format(cvx, cvy, dx, dy, x_vel, y_vel, x_acc, y_acc, vehicle.x_vel, vehicle.y_vel, self.grid.r_c_at_x_y(cvx, cvy), self.grid.drawing_rect, "None" if self.grid.tile_at_x_y(cvx, cvy) is None else self.grid.tile_at_x_y(cvx, cvy).rect))
            # d_rect = self.grid.drawing_rect
            # if not (cvx in range(d_rect.left, d_rect.right-2)):
            #     # hit left tor right side wall
            #     vehicle.x_vel = 0
            # if not (cvy in range(d_rect.top, d_rect.bottom-2)):
            #     # hit a top or bottom side wall
            #     vehicle.y_vel = 0
            # cvx = min(d_rect.right-2, max(d_rect.left, cvx))
            # cvy = min(d_rect.bottom-2, max(d_rect.top, cvy))
            #
            # # print("2, (cvx, cvy): ({}, {}), (dx, dy): ({}, {}), (x_vel, y_vel): ({}, {}), (x_acc, y_acc): ({}, {}), (nx_vel, vy_vel): ({}, {}), self.grid.r_c_at_x_y({}), d.rect: {}, t.rect: {}".format(cvx, cvy, dx, dy, x_vel, y_vel, x_acc, y_acc, vehicle.x_vel, vehicle.y_vel, self.grid.r_c_at_x_y(cvx, cvy), self.grid.drawing_rect, "None" if self.grid.tile_at_x_y(cvx, cvy) is None else self.grid.tile_at_x_y(cvx, cvy).rect))
            # cvy, cvx = self.grid.r_c_at_x_y(cvx, cvy)
            #
            # # Move vehicle(s)
            # rows = self.grid.grid_data_in["height"]
            # cols = self.grid.grid_data_in["width"]
            # cvy = 0 if cvy < 0 else (rows - 1 if cvy >= rows else cvy)
            # cvx = 0 if cvx < 0 else (cols - 1 if cvx >= cols else cvx)


            # # Check vehicle collisions
            # tile_to_be_c = self.grid.tiles[cvy][cvx]
            # # print("tile to be covered:", tile_to_be_c)
            # if (isinstance(tile_to_be_c, Vehicle) and tile_to_be_c.id_no != vehicle.id_no):
            #     print("collide with vehicle tile:", tile_to_be_c, "type(tile):", type(tile_to_be_c))
            # elif not isinstance(tile_to_be_c, Vehicle) and not isinstance(tile_to_be_c, TileAir):
            #     print("collide with tile:", tile_to_be_c, "type(tile):", type(tile_to_be_c))
            # # if not isinstance(tile_to_be_c, TileAir):
            # #     print("collide with tile:", tile_to_be_c, "type(tile):", type(tile_to_be_c))

            # ncvx, ncvy = self.grid.r_c_at_x_y(cvx, cvy, bind=True)
            # print("cvx:", cvx, ", cvy:", cvy, ", ncvx:", ncvx, ", ncvy:", ncvy)
            # self.grid.set_vehicle(vehicle, (ncvx, ncvy))

            dr = self.grid.drawing_rect
            if not (dr.left <= cvx <= (dr.right - vehicle.rect.width)):
                vehicle.x_vel = 0
            if not (dr.top <= cvx <= (dr.bottom - vehicle.rect.height)):
                vehicle.y_vel = 0
            self.grid.set_vehicle(vehicle, (cvx, cvy))

            self.grid.update_view_rect()


            # vehicles = [self.grid.get_active_vehicle()]
            # v_rects = [v[0].rect for v in vehicles]
            # for tile_row in tiles:
            #     for tile in tile_row:
            #         for vehicle, row_pos, col_pos in vehicles:
            #             print("vehicle:", vehicle)
            #             if tile.rect.contains(vehicle.rect):
            #                 if not isinstance(tile, TileAir):
            #                     if (isinstance(tile, Vehicle) and tile.id_no != vehicle.id_no):
            #                         print("collide with vehicle tile:", tile, "type(tile):", type(tile))
            #                     elif not isinstance(tile, Vehicle):
            #                         print("collide with tile:", tile, "type(tile):", type(tile))
            #                     else:
            #                         print("else a")
            #                 else:
            #                     print("else b")
            #             else:
            #                 print("else c")



            # os.system('cls' if os.name == 'nt' else 'clear')
            # g1.print_tile_symbols()
            # print("mgl:", self.view_rect)
            app.clock.tick(t_sec)



        # self.view_rect = (
        #     max(0, (cx - (self.grid.grid_data_in["width"] // 2))),
        #     max(0, (cy - (self.grid.grid_data_in["height"] // 2))),
        #     self.view_rect_w,
        #     self.view_rect_h
        # )

    def add_active_vehicle(self, vehicle, pos):
        if self.grid is None or not self.grid.is_init:
            raise ValueError("Must initialize the Grid object from within Motherload class before you can add vehicles.")
        self.grid.set_vehicle(vehicle, pos)


if __name__ == '__main__':
    t1 = Vehicle(1, "Tank", pygame.Rect(0, 0, 10, 10), GREEN, x_acc=0.3, y_acc=0.3)
    grid_data_template = Grid.req_keys
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
            ],
            9.812,
            0.65,
            30
        ]
    )))
    # g1.add_gem(gd1, (45, 45))
    # g1.add_gem(gd1, (45, 45))
    # print("grid.tiles:", g1.tiles)

    # g1.set_vehicle(t1, (50, 10))
    # g1.print_tile_symbols()
    mlg = MotherloadGame()
    mlg.set_grid(g1)
    mlg.add_active_vehicle(t1, (100, 100))

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


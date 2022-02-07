from colour_utility import *
from utility import *
from vehicle import *


COLOUR_TILE_AIR = WHITE
DURABILITY_TILE_AIR = 0
COLOUR_TILE_DIRT = BROWN_3
DURABILITY_TILE_DIRT = 1


class Tile:
    def __init__(self, text_symbol, colour, durability, rect):
        self.text_symbol = text_symbol
        self.colour = colour
        self.durability = durability
        self.rect = rect

    def __eq__(self, other):
        return isinstance(other, Tile) and other.text_symbol == self.text_symbol and other.rect == self.rect


class TileAir(Tile):
    def __init__(self, colour, durability, rect, text_symbol=" "):
        super().__init__(text_symbol, colour, durability, rect)


class TileDirt(Tile):
    def __init__(self, colour, durability, rect, text_symbol="O"):
        super().__init__(text_symbol, colour, durability, rect)


class Gem(Tile):
    def __init__(self, name, colour, durability, rect, text_symbol):
        super().__init__(text_symbol, colour, durability, rect)
        self.name = name


class GemDiamond(Gem):
    def __init__(self, colour, durability, rect=None, name="Diamond", text_symbol="D"):
        super().__init__(name, colour, durability, rect, text_symbol)


class GemQuartz(Gem):
    def __init__(self, colour, durability, rect=None, name="Quartz", text_symbol="Q"):
        super().__init__(name, colour, durability, rect, text_symbol)


class GemIron(Gem):
    def __init__(self, colour, durability, rect=None, name="Iron", text_symbol="I"):
        super().__init__(name, colour, durability, rect, text_symbol)


class Grid:
    req_keys = [
        "width",
        "height",
        "ground_level",
        "shop_pos",
        "fuel_station_pos",
        "spawn_pos",
        "gem_data",
        "gravity",
        "vehicle_magnifier",
        "tick_time"
    ]
    req_gem_keys = [
        "gem",
        "probability",
        "min_depth",
        "max_depth"
    ]

    def __init__(self, id_no, name, grid_data_in):
        assert isinstance(grid_data_in, dict), "Parameter \"grid_data_in\" must be a dictionary."
        assert all([k in grid_data_in for k in self.req_keys]), "Parameter \"grid_data_in\" must be contain all of the following keys:\n\t" + "\n\t".join(self.req_keys)
        assert isinstance(grid_data_in["gem_data"], list), "Gem data needs to be a List."

        self.is_init = False
        self.game = None
        self.display = None

        self.grid_data_in = grid_data_in
        self.id_no = id_no
        self.name = name

        self.tiles = []
        self.active_vehicle = None, None, None

        # TODO HARDCODE
        self.view_rect = None
        self.view_rect_w = 25
        self.view_rect_h = 18

        self.drawing_rect = None
        self.drawing_rect_colour = None
        self.tile_border_width = None

    def init(self, game, display):

        # Grid class MUST have game and display objects from the PygameApplication class.
        self.game = game
        self.display = display

        tiles = []
        width = self.grid_data_in["width"]
        height = self.grid_data_in["height"]
        ground_level = self.grid_data_in["ground_level"]
        shop_pos = self.grid_data_in["shop_pos"]
        fuel_station_pos = self.grid_data_in["fuel_station_pos"]
        spawn_pos = self.grid_data_in["spawn_pos"]
        gem_data = self.grid_data_in["gem_data"]

        # TODO HARDCODE
        self.drawing_rect = self.game.Rect(25, 25, 700, 450)
        self.drawing_rect_colour = GRAY_45
        self.tile_border_width = 0

        self.update_view_rect()




        tiles_list = self.tiles
        ix, iy = self.drawing_rect.topleft
        # draw tiles:
        xb1, yb1, xbd, ybd = self.drawing_rect
        xb2 = xb1 + xbd
        yb2 = yb1 + ybd
        tbw = self.tile_border_width
        # print("\t\t(xb1: {}, xb2: {}, xbd: {}, yb1: {}, yb2 {}, ybd: {})".format(xb1, xb2, xbd, yb1, yb2, ybd))
        # th = self.drawing_rect.height / max(1, len(tiles_list[yb1: yb2 + 1]))
        # for i, row in enumerate(tiles_list[yb1: yb2 + 1]):
        #     tw = self.drawing_rect.width / len(row[xb1: xb2 + 1])
            # for j, tile in enumerate(row[xb1: xb2 + 1]):
                # tile_rect = game.Rect(ix + (j * tw) + tbw, iy + (i * th) + tbw, tw - (2 * tbw), th - (2 * tbw))
                # if isinstance(tile, Vehicle):
                #     m = self.grid_data_in["vehicle_magnifier"]
                #     n_w = tile_rect.width * m
                #     n_h = tile_rect.height * m
                #     d_w = tile_rect.width - n_w
                #     d_h = tile_rect.height - n_h
                #     n_x1 = tile_rect.left + (d_w / 2)
                #     n_y1 = tile_rect.top + (d_h / 2)
                #     n_tr = game.Rect(n_x1, n_y1, n_w, n_h)
                #     tile_rect = n_tr
                # game.draw.rect(display, tile.colour, tile_rect)



        for r in range(height):
            row = []
            for c in range(width):
                tile = None

                # th = self.drawing_rect.height / max(1, len(tiles_list[yb1: yb2 + 1]))
                # tw = self.drawing_rect.width / max(1, len(row[xb1: xb2 + 1]))
                th = self.drawing_rect.height / height
                tw = self.drawing_rect.width / width
                tile_rect = game.Rect(ix + (c * tw) + tbw, iy + (r * th) + tbw, tw - (2 * tbw), th - (2 * tbw))

                if r < ground_level:
                    tile = TileAir(COLOUR_TILE_AIR, DURABILITY_TILE_AIR, tile_rect)
                else:
                    # tile = TileDirt(COLOUR_TILE_DIRT, DURABILITY_TILE_DIRT)
                    gems = [(g["gem"], g["probability"]) for g in gem_data]
                    s_ps = sum([g[1] for g in gems])
                    ns_ps = 1 - s_ps
                    # add extra dirt tiles to simulate random spawning
                    gems.append((TileDirt(COLOUR_TILE_DIRT, DURABILITY_TILE_DIRT, tile_rect), ns_ps))
                    tile = weighted_choice(gems)
                    tile.rect = tile_rect

                    # if isinstance(tile, Gem):
                    #     print("Adding Gem \"{}\" at ({}, {})".format(tile, r, c))
                row.append(tile)
            tiles.append(row)

        self.tiles = tiles
        print("post_init tiles:", self.tiles)
        self.is_init = True

    def print_tile_symbols(self):
        syms = []
        for row in self.tiles:
            r = []
            for col in row:
                r.append(col.text_symbol)
            syms.append("".join(r))
        print("\n" + "\n".join(syms) + "\n")

    def update_view_rect(self):
        v, cy, cx = self.get_active_vehicle()

        if v is None:
            cy, cx = self.grid_data_in["width"] // 2, self.grid_data_in["ground_level"]

        # print("update_view_rect: ({}, {})".format(cx, cy))

        self.view_rect = self.game.Rect(
            max(0, min(cx - (self.view_rect_w // 2), self.grid_data_in["width"] - self.view_rect_w)),
            max(0, min(cy - (self.view_rect_h // 2), self.grid_data_in["height"] - self.view_rect_h)),
            self.view_rect_w,
            self.view_rect_h
        )

        self.update_viewing_tiles()

    def update_viewing_tiles(self):

        tiles_list = self.get_drawing_tiles()
        # print("drawing tiles:", "\n" + "\n".join(["".join([t.text_symbol for t in tile_row]) for tile_row in tiles_list]))
        # print("len(drawing_tiles):", len(tiles_list), "len(drawing_tiles)[0]:", (len(tiles_list[0]) if tiles_list else "None"))
        ix, iy = self.drawing_rect.topleft
        # draw tiles:
        # xb1, yb1, xbd, ybd = self.view_rect
        xb1, yb1, xbd, ybd = self.view_rect.left, self.view_rect.top, self.view_rect.width, self.view_rect.height
        # xb2 = xb1 + xbd
        # yb2 = yb1 + ybd
        xb1, yb1 = yb1, xb1
        xb2 = yb1 + ybd
        yb2 = xb1 + xbd

        # return [row[yb1: yb2 + 1] for row in tiles_list[xb1: xb2 + 1]]

        tbw = self.tile_border_width
        # print("\t\t(xb1: {}, xb2: {}, xbd: {}, yb1: {}, yb2 {}, ybd: {})".format(xb1, xb2, xbd, yb1, yb2, ybd))
        th = self.drawing_rect.height / max(1, ybd)
        for i, row in enumerate(tiles_list):
            tw = self.drawing_rect.width / max(1, xbd)
            for j, tile in enumerate(row):
                tile_rect = self.game.Rect(ix + (j * tw) + tbw, iy + (i * th) + tbw, tw - (2 * tbw), th - (2 * tbw))
                # print("(i, j): ({}, {}), tw: {}, th: {}, rect: {}".format(i, j, tw, th, tile_rect))
                if isinstance(tile, Vehicle):
                    m = self.grid_data_in["vehicle_magnifier"]
                    n_w = tile_rect.width * m
                    n_h = tile_rect.height * m
                    d_w = tile_rect.width - n_w
                    d_h = tile_rect.height - n_h
                    n_x1 = tile_rect.left + (d_w / 2)
                    n_y1 = tile_rect.top + (d_h / 2)
                    tile_rect = self.game.Rect(n_x1, n_y1, n_w, n_h)

                tiles_list[i][j].rect = tile_rect

        # # reset all other tile rect sizes
        # xb1, yb1, xbd, ybd = self.drawing_rect
        # xb2 = xb1 + xbd
        # yb2 = yb1 + ybd
        # tbw = self.tile_border_width
        #
        # for i, row in enumerate(tiles_list[:yb1] + tiles_list[yb2 + 1:]):
        #     tw = self.drawing_rect.width / max(1, len(row[:xb1] + row[xb2 + 1:]))
        #     for j, tile in enumerate(row[:xb1] + row[xb2 + 1:]):
        #         th = self.drawing_rect.height / max(1, len(tiles_list[:yb1] + tiles_list[yb2 + 1:]))
        #         tile_rect = self.game.Rect(ix + (j * tw) + tbw, iy + (i * th) + tbw, tw - (2 * tbw), th - (2 * tbw))
        #         self.tiles[i][j].rect = tile_rect

    def set_gem(self, gem, pos):
        assert isinstance(gem, Gem), "Cannot insert non-gem value \"{}\" into this grid.".format(gem)
        assert (isinstance(pos, tuple) or isinstance(pos, list)) and len(pos) == 2, "Parameter pos \"{}\" must be a tuple / list of length 2"
        c, r = pos
        assert 0 <= r < self.grid_data_in["height"], "Row \"{}\" from param pos: \"{}\" is out of range ({}, {}).".format(pos[0], pos, 0, self.grid_data_in["height"])
        assert 0 <= c < self.grid_data_in["width"], "Col \"{}\" from param pos: \"{}\" is out of range ({}, {}).".format(pos[1], pos, 0, self.grid_data_in["width"])
        self.tiles[r][c] = gem

    # Requires a Vehicle object and (row, col) grid coordinates
    def set_vehicle(self, vehicle, pos):
        assert isinstance(vehicle, Vehicle), "Cannot insert non-vehicle value \"{}\" into this grid.".format(vehicle)
        assert (isinstance(pos, tuple) or isinstance(pos, list)) and len(pos) == 2, "Parameter pos \"{}\" must be a tuple / list of length 2"
        c, r = pos
        assert 0 <= r < self.grid_data_in["height"], "Row \"{}\" from param pos: \"{}\" is out of range ({}, {}).".format(pos[0], pos, 0, self.grid_data_in["height"])
        assert 0 <= c < self.grid_data_in["width"], "Col \"{}\" from param pos: \"{}\" is out of range ({}, {}).".format(pos[1], pos, 0, self.grid_data_in["width"])

        cv, cy, cx = self.get_active_vehicle()

        # Clear the grid square where the vehicle just was
        if cv is not None:
            tr = cv.rect
            self.tiles[cy][cx] = TileAir(COLOUR_TILE_AIR, DURABILITY_TILE_AIR, tr)

        ix, iy = self.drawing_rect.topleft
        xb1, yb1, xbd, ybd = self.view_rect
        xb2 = xb1 + xbd
        yb2 = yb1 + ybd
        tbw = self.tile_border_width
        th = self.drawing_rect.height / len(self.tiles[yb1: yb2 + 1])
        tw = self.drawing_rect.width / len(self.tiles[xb1: xb2 + 1])
        tile_rect = self.game.Rect(ix + (c * tw) + tbw, iy + (r * th) + tbw, tw - (2 * tbw), th - (2 * tbw))
        m = max(0, min(1, self.grid_data_in["vehicle_magnifier"]))
        n_w = tile_rect.width * m
        n_h = tile_rect.height * m
        d_w = tile_rect.width - n_w
        d_h = tile_rect.height - n_h
        n_x1 = tile_rect.left + (d_w / 2)
        n_y1 = tile_rect.top + (d_h / 2)
        n_tr = self.game.Rect(n_x1, n_y1, n_w, n_h)

        vehicle.rect = n_tr
        self.tiles[r][c] = vehicle
        self.active_vehicle = vehicle, r, c

    def get_active_vehicle(self):
        return self.active_vehicle

    def get_drawing_tiles(self):
        tiles_list = self.tiles
        xb1, yb1, xbd, ybd = self.view_rect.left, self.view_rect.top, self.view_rect.width, self.view_rect.height
        xb2 = xb1 + xbd
        yb2 = yb1 + ybd
        # print("\t\t(xb1: {}, xb2: {}, xbd: {}, yb1: {}, yb2 {}, ybd: {})".format(xb1, xb2, xbd, yb1, yb2, ybd))

        return [row[xb1: xb2] for row in tiles_list[yb1: yb2]]

    def tile_at_x_y(self, x, y):
        for r, tile_row in enumerate(self.tiles):
            for c, tile in enumerate(tile_row):
                if tile.rect.collidepoint((x, y)):
                    return tile

    def tile_at_r_c(self, r, c):
        if r in range(len(self.tiles)):
            if c in range(len(self.tiles[r])):
                return self.tiles[r][c]

    def x_y_at_tile(self, t_tile):
        for r, tile_row in enumerate(self.tiles):
            for c, tile in enumerate(tile_row):
                if tile == t_tile:
                    return tile.rect.topleft
        return None, None

    def r_c_at_tile(self, t_tile):
        for r, tile_row in enumerate(self.tiles):
            for c, tile in enumerate(tile_row):
                if tile == t_tile:
                    return r, c
        return None, None

    def r_c_at_x_y(self, x, y):
        # print("({}, {})".format(x, y))
        for r, tile_row in enumerate(self.tiles):
            for c, tile in enumerate(tile_row):
                # print("(" + str(r) + ", " + str(c) + ") tile.rect:", tile.rect, "tile.rect.collidepoint((x, y):", tile.rect.collidepoint((x, y)))
                if tile.rect.collidepoint((x, y)):
                    return r, c
        return None, None

    def x_y_at_r_c(self, r, c):
        if r in range(len(self.tiles)):
            if c in range(len(self.tiles[r])):
                return self.tiles[r][c].rect.topleft
        return None, None

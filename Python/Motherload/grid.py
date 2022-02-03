from colour_utility import *
from utility import *
from vehicle import *


COLOUR_TILE_AIR = WHITE
DURABILITY_TILE_AIR = 0
COLOUR_TILE_DIRT = BROWN_3
DURABILITY_TILE_DIRT = 1


class Tile:
    def __init__(self, text_symbol, colour, durability):
        self.text_symbol = text_symbol
        self.colour = colour
        self.durability = durability


class TileAir(Tile):
    def __init__(self, colour, durability, text_symbol=" "):
        super().__init__(text_symbol, colour, durability)


class TileDirt(Tile):
    def __init__(self, colour, durability, text_symbol="O"):
        super().__init__(text_symbol, colour, durability)


class Gem(Tile):
    def __init__(self, name, colour, durability, text_symbol):
        super().__init__(text_symbol, colour, durability)
        self.name = name


class GemDiamond(Gem):
    def __init__(self, colour, durability, name="Diamond", text_symbol="D"):
        super().__init__(name, colour, durability, text_symbol)


class GemQuartz(Gem):
    def __init__(self, colour, durability, name="Quartz", text_symbol="Q"):
        super().__init__(name, colour, durability, text_symbol)


class GemIron(Gem):
    def __init__(self, colour, durability, name="Iron", text_symbol="I"):
        super().__init__(name, colour, durability, text_symbol)


class Grid:

    def __init__(self, id_no, name, grid_data_in):
        assert isinstance(grid_data_in, dict), "Parameter \"grid_data_in\" must be a dictionary."
        req_keys = [
            "width",
            "height",
            "ground_level",
            "shop_pos",
            "fuel_station_pos",
            "spawn_pos",
            "gem_data"
        ]
        req_gem_keys = [
            "gem",
            "probability",
            "min_depth",
            "max_depth"
        ]
        assert all([k in grid_data_in for k in req_keys]), "Parameter \"grid_data_in\" must be contain all of the following keys:\n\t" + "\n\t".join(req_keys)
        assert isinstance(grid_data_in["gem_data"], list), "Gem data needs to be a List."
        self.grid_data_in = grid_data_in
        self.id_no = id_no
        self.name = name

        self.tiles = []
        self.active_vehicle = None, None, None

        self.init()

    def init(self):
        tiles = []
        width = self.grid_data_in["width"]
        height = self.grid_data_in["height"]
        ground_level = self.grid_data_in["ground_level"]
        shop_pos = self.grid_data_in["shop_pos"]
        fuel_station_pos = self.grid_data_in["fuel_station_pos"]
        spawn_pos = self.grid_data_in["spawn_pos"]
        gem_data = self.grid_data_in["gem_data"]
        for r in range(height):
            row = []
            for c in range(width):
                tile = None
                if r < ground_level:
                    tile = TileAir(COLOUR_TILE_AIR, DURABILITY_TILE_AIR)
                else:
                    # tile = TileDirt(COLOUR_TILE_DIRT, DURABILITY_TILE_DIRT)
                    gems = [(g["gem"], g["probability"]) for g in gem_data]
                    s_ps = sum([g[1] for g in gems])
                    ns_ps = 1 - s_ps
                    gems.append((TileDirt(COLOUR_TILE_DIRT, DURABILITY_TILE_DIRT), ns_ps))
                    # print("gems:", gems)
                    tile = weighted_choice(gems)
                    # if isinstance(tile, Gem):
                    #     print("Adding Gem \"{}\" at ({}, {})".format(tile, r, c))
                row.append(tile)
            tiles.append(row)

        self.tiles = tiles

    def print_tile_symbols(self):
        syms = []
        for row in self.tiles:
            r = []
            for col in row:
                r.append(col.text_symbol)
            syms.append("".join(r))
        print("\n" + "\n".join(syms) + "\n")

    def set_gem(self, gem, pos):
        assert isinstance(gem, Gem), "Cannot insert non-gem value \"{}\" into this grid.".format(gem)
        assert (isinstance(pos, tuple) or isinstance(pos, list)) and len(pos) == 2, "Parameter pos \"{}\" must be a tuple / list of length 2"
        c, r = pos
        assert 0 <= r < self.grid_data_in["height"], "Row \"{}\" from param pos: \"{}\" is out of range ({}, {}).".format(pos[0], pos, 0, self.grid_data_in["height"])
        assert 0 <= c < self.grid_data_in["width"], "Col \"{}\" from param pos: \"{}\" is out of range ({}, {}).".format(pos[1], pos, 0, self.grid_data_in["width"])
        self.tiles[r][c] = gem

    def set_vehicle(self, vehicle, pos):
        assert isinstance(vehicle, Vehicle), "Cannot insert non-vehicle value \"{}\" into this grid.".format(vehicle)
        assert (isinstance(pos, tuple) or isinstance(pos, list)) and len(pos) == 2, "Parameter pos \"{}\" must be a tuple / list of length 2"
        c, r = pos
        assert 0 <= r < self.grid_data_in["height"], "Row \"{}\" from param pos: \"{}\" is out of range ({}, {}).".format(pos[0], pos, 0, self.grid_data_in["height"])
        assert 0 <= c < self.grid_data_in["width"], "Col \"{}\" from param pos: \"{}\" is out of range ({}, {}).".format(pos[1], pos, 0, self.grid_data_in["width"])

        cv, cy, cx = self.get_active_vehicle()
        if cv is not None:
            self.tiles[cy][cx] = TileAir(COLOUR_TILE_AIR, DURABILITY_TILE_AIR)

        self.tiles[r][c] = vehicle
        self.active_vehicle = vehicle, r, c

    def get_active_vehicle(self):
        return self.active_vehicle


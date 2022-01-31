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
        assert all([k in grid_data_in for k in req_keys]), "Parameter \"grid_data_in\" must be contain all of the following keys:\n\t" + "\n\t".join(req_keys)
        self.grid_data_in = grid_data_in
        self.id_no = id_no
        self.name = name

        self.tiles = []

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
            for c in range(height):
        self.tiles = tiles

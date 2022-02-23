from Tile import *


class TileAir(Tile):
    def __init__(self, colour, durability, rect, text_symbol=" "):
        super().__init__(text_symbol, colour, durability, rect)

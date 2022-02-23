from Tile import *


class TileDirt(Tile):
    def __init__(self, colour, durability, rect, text_symbol="O"):
        super().__init__(text_symbol, colour, durability, rect)

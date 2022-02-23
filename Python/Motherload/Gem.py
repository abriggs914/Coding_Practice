from Tile import *


class Gem(Tile):
    def __init__(self, name, colour, durability, rect, text_symbol):
        super().__init__(text_symbol, colour, durability, rect)
        self.name = name

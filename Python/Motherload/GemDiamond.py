from Gem import *


class GemDiamond(Gem):
    def __init__(self, colour, durability, rect=None, name="Diamond", text_symbol="D"):
        super().__init__(name, colour, durability, rect, text_symbol)

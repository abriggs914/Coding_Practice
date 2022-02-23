from Gem import *


class GemIron(Gem):
    def __init__(self, colour, durability, rect=None, name="Iron", text_symbol="I"):
        super().__init__(name, colour, durability, rect, text_symbol)

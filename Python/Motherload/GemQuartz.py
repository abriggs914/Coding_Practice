from Gem import *


class GemQuartz(Gem):
    def __init__(self, colour, durability, rect=None, name="Quartz", text_symbol="Q"):
        super().__init__(name, colour, durability, rect, text_symbol)

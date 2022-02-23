
class Tile:
    def __init__(self, text_symbol, colour, durability, rect=None, hit_points=0):
        self._text_symbol = text_symbol
        self._colour = colour
        self._durability = durability
        self._hit_points = hit_points
        self._rect = rect  # May not need to to actually store the rect in the object if the grid will change so frequently.
        # Can just calculate the visual rect.

    def set_text_symbol(self, value):
        self._text_symbol = value

    def get_text_symbol(self):
        return self._text_symbol

    def del_text_symbol(self):
        del self._text_symbol

    def set_colour(self, value):
        self._colour = value

    def get_colour(self):
        return self._colour

    def del_colour(self):
        del self._colour

    def set_durability(self, value):
        self._durability = value

    def get_durability(self):
        return self._durability

    def del_durability(self):
        del self._durability

    def set_hit_points(self, value):
        self._hit_points = value

    def get_hit_points(self):
        return self._hit_points

    def del_hit_points(self):
        del self._hit_points

    def set_rect(self, value):
        self._rect = value

    def get_rect(self):
        return self._rect

    def del_rect(self):
        del self._rect

    def __eq__(self, other):
        return isinstance(other, Tile) and other.text_symbol == self.text_symbol and other.rect == self.rect

    def is_broken(self):
        return self.hit_points > self.durability

    text_symbol = property(get_text_symbol, set_text_symbol, del_text_symbol, "Identifying Ascii character for printing.")
    colour = property(get_colour, set_colour, del_colour, "Colour of the tile.")
    durability = property(get_durability, set_durability, del_durability, "Durability of the tile.")
    hit_points = property(get_hit_points, set_hit_points, del_hit_points, "Count of hit points taken to the tile.")
    rect = property(get_rect, set_rect, del_rect, "Pygame rect object.")

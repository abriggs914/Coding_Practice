from utility import *


namer = alpha_seq(100000)
UNDEF = "UNDEFINED"


class Square:

    def __init__(self, name, movement_speed=1, is_foggy=False):
        self.iid = next(namer)
        self.name = name
        self.is_safe = False
        self.movement_speed = movement_speed
        self.is_foggy = is_foggy


class ChanceBattleSquare(Square):
    def __init__(self, name, chance=0.08, chance_of="all", *args, **kwargs):
        super().__init__(name, *args, **kwargs)
        self.chance = chance
        self.chance_of = chance_of


class Path(Square):
    def __init__(self, *args, **kwargs):
        super().__init__(name="path", *args, **kwargs)


class TallGrass(ChanceBattleSquare):
    def __init__(self, *args, **kwargs):
        super().__init__(name="tall_grass", *args, **kwargs)


class DeepWater(ChanceBattleSquare):
    def __init__(self, *args, **kwargs):
        super().__init__(name="water", *args, **kwargs)


GRID_LEGEND = {
    " ": None,
    "_": UNDEF,
    "!": UNDEF,
    "@": UNDEF,
    "#": "wall",
    "$": UNDEF,
    "%": UNDEF,
    "^": UNDEF,
    "&": UNDEF,
    "*": UNDEF,
    "(": UNDEF,
    ")": UNDEF,
    "-": UNDEF,
    "=": UNDEF,
    "+": UNDEF,
    "`": UNDEF,
    "~": UNDEF,
    "0": UNDEF,
    "1": UNDEF,
    "2": UNDEF,
    "3": UNDEF,
    "4": UNDEF,
    "5": UNDEF,
    "6": UNDEF,
    "7": UNDEF,
    "8": UNDEF,
    "9": UNDEF,
}



class Grid:

    def __init__(self, viewable_w_h=(25, 25), max_w_h=(1000, 1000), grid_in=None):
        self.max_w_h = max_w_h
        self.grid = {}
        self.viewable_w_h = viewable_w_h
        self._visible_start = 0, 0

        self.grid = grid_in if grid_in else self.new_blank_grid(max_w_h)
        self.center_viewing_window()

    def new_blank_grid(self, max_w_h):
        w, h = self.max_w_h
        for i in range(w):
            for j in range(h):
                self.grid[self.keyify(i, j)] = GRID_LEGEND[" "]

        for i in range(w):
            self.grid[self.keyify(i, 0)] = GRID_LEGEND["#"]
            for j in range(h):
                self.grid[self.keyify(i, 0)] = GRID_LEGEND["#"]

        return self.grid


    def center_viewing_window(self, inplace=True):
        w, h = self.viewable_w_h
        mw, mh = self.max_w_h
        x, y = (mw - w) // 2, (mh - h) // 2
        if inplace:
            self.visible_start = x, y
        return x, y

    def keyify(self, i, j):
        assert i in range(0, self.max_w_h[0]), f"Row index '{i}' is out of range"
        assert j in range(0, self.max_w_h[1]), f"Column index '{j}' is out of range"
        return f"{i}__{j}"

    def get_visible_start(self):
        return self._visible_start

    def set_visible_start(self, visible_start_in):
        self._visible_start = visible_start_in

    def del_visible_start(self):
        del self._visible_start

    def __repr__(self):
        w, h = self.viewable_w_h
        return "\n".join(["".join([self.grid[self.keyify(i, j)] for j in range(h)]) for i in range(w)])
        # return res

    visible_start = property(get_visible_start, set_visible_start, del_visible_start)


if __name__ == '__main__':

    g1 = Grid()
    tg1 = TallGrass(movement_speed=1.25)
    while input():
        print(g1)

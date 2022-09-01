import dataclasses
import random
from dataclasses import dataclass
from random import randint

from utility import clamp


@dataclass
class Grid:

    class NotInitializedError(Exception):
        def __init__(self, message="Error this grid has not been initialized"):
            raise ValueError(message)

    class GridIndexRangeError(Exception):
        def __init__(self, message="Error index out of range for this grid."):
            raise ValueError(message)

    rows: int
    cols: int

    _grid_space: list[list[int]] = dataclasses.field(default_factory=list)
    _has_initialized: bool = False
    food: tuple[int, int] = dataclasses.field(default_factory=tuple)
    allow_wrap = False
    allow_diagonal = False

    def init(self):
        assert 0 < self.cols < 1000, f"Error, can't make a grid with this many columns ({self.cols}) max 1000."
        assert 0 < self.rows < 1000, f"Error, can't make a grid with this many rows ({self.rows}) max 1000."
        self.grid_space = [[(r * self.cols) + c for c in range(self.cols)] for r in range(self.rows)]
        self.has_initialized = True
        return self

    def gen_new_food(self, weight_in=1, position_in=None):
        position = None
        weight = None
        max_pos = self.cols * self.rows

        if position_in is not None:
            if self.valid_index(position_in):
                position = position_in
        if position is None:
            position = randint(0, max_pos)

        if isinstance(weight_in, int):
            weight = clamp(1, weight_in, 5)

        self.food = (weight, position)
        return self.food

    def rc2i(self, *rc):
        if len(rc) == 1:
            rc = rc[0]
            if isinstance(rc, tuple) and len(rc) == 2:
                if isinstance(rc[0], int) and isinstance(rc[1], int):
                    return (rc[0] * self.cols) + rc[1]
        raise ValueError(f"Error in params '{rc=}'")

    def i2rc(self, i):
        if isinstance(i, int):
            if self.valid_index(i):
                return i // self.cols, i % self.cols
        raise ValueError(f"Error in params '{i=}'")

    def valid_index(self, index, is_row=False, is_col=False):
        if isinstance(index, tuple):
            index = self.rc2i(index)
        if (not is_row and not is_col) or (is_row and is_col):
            return 0 <= index < (self.rows * self.cols)
        elif is_row:
            return  0 <= index < self.rows
        elif is_col:
            return  0 <= index < self.cols
        return False

    def direction_between(self, a, b, normal=False):
        r_a, c_a = self.i2rc(a)
        r_b, c_b = self.i2rc(b)
        r, c = r_b - r_a, c_b - c_a
        if normal:
            if abs(r) > abs(c):
                c = 0
                r //= abs(r)
            elif abs(c) > abs(r):
                r = 0
                c //= abs(c)
            else:
                if random.choice([0, 1]) == 0:
                    c = 0
                    r //= abs(r)
                else:
                    r = 0
                    c //= abs(c)

        # else:
            # return r_b - r_a, c_b - c_a
        return r, c
        # r_a, c_a = self.i2rc(a)
        # r_b, c_b = self.i2rc(b)
        # r, c = 0, 0
        # if r_a == r_b:
        #     return r, c
        #
        # if r_a > r_b:
        #     r = -1
        # elif r_b > r_a:
        #     r = 1
        #
        # if c_a > c_b:
        #     c = -1
        # elif c_b > c_a:
        #     c = 1
        #
        # return r, c

    def get_grid_space(self):
        if not self.has_initialized:
            raise Grid.NotInitializedError()
        return self._grid_space

    def set_grid_space(self, grid_space_in):
        self._grid_space = grid_space_in

    def del_grid_space(self):
        del self._grid_space

    def get_has_initialized(self):
        return self._has_initialized

    def set_has_initialized(self, is_initialized):
        self._has_initialized = is_initialized

    def del_has_initialized(self):
        del self._has_initialized

    grid_space = property(get_grid_space, set_grid_space, del_grid_space)
    has_initialized = property(get_has_initialized, set_has_initialized, del_has_initialized)

@dataclass
class Snake:

    head: tuple[int, int] = dataclasses.field(default_factory=tuple)
    segments: list[int] = dataclasses.field(default_factory=list)
    _x_dir: int = 0
    _y_dir: int = 0
    _has_init: bool = False

    def init(self, grid, position="random"):
        assert isinstance(grid, Grid), f"Error, param 'grid' must be a Grid object. Got {grid=}"
        max_n = grid.rows * grid.cols
        if position == "random":
            a, b = (random.randint(0, grid.rows), random.randint(0, grid.cols))
        else:
            if isinstance(position, tuple):
                if len(position) == 2:
                    a, b = position
                    if isinstance(a, int) and isinstance(b, int):
                        a = clamp(0, a, grid.rows)
                        b = clamp(0, b, grid.cols)
                    else:
                        raise ValueError("Error, param 'position' must be a tuple of integers.")
                else:
                    raise ValueError("Error, param 'position' must be a tuple of exactly length 2.")
            else:
                raise ValueError("Error, param 'position' must be 'random' or be a tuple.")
        self.head = a, b
        self.has_init = True
        return self

    def move(self, grid):
        assert isinstance(grid, Grid)
        assert self.has_init, "Error, this snake object has not been initialized"
        print(f"\t\t{grid=}")
        print(f"\t\t{grid.grid_space}")

        def apply_move(point, direction):
            xd, yd = direction
            if grid.allow_wrap:
                return ((point[0] + xd) % grid.rows, (point[1] + yd) % grid.cols)
            else:
                return (clamp(0, point[0] + xd, grid.rows - 1), clamp(0, point[1] + yd, grid.cols - 1))

        # return grid.direction_between(0, 55, normal=True)
        x_dir, y_dir = self._x_dir, self._y_dir
        print(f"OLD: {self.head}")
        print(f"{x_dir=}, {y_dir=}")
        self.head = apply_move(self.head, (x_dir, y_dir))
        print(f"NEW: {self.head}, XXX: {sum(list(map(abs, [x_dir, y_dir])))}")
        if not self.segments:
            return {"exiting": [grid.rc2i(self.head)]}
        else:
            return {"exiting": self.segments[-sum(list(map(abs, [x_dir, y_dir]))):] if self.segments else []}

        # for i, segment in enumerate(self.segments):
        #     if i < len(self.segments) - 1:
        #         next_segment = self.segments[i + 1]
        #         distance_between = grid.direction_between(segment, next_segment)
        #         move = apply_move(grid.i2rc(segment), distance_between)
        #         self.segments[i] = grid.rc2i(move)
        #     else:

    def set_direction(self, xd, yd=None):
        if yd is None:
            if not (isinstance(xd, tuple) and len(xd) == 2 and isinstance(xd[0], int) and isinstance(xd[1], int)):
                raise ValueError("Error if param 'yd' is omitted then param 'xd' must be a tuple of length 2.")
        self.set_x_dir(xd)
        self.set_y_dir(yd)
        return self

    def get_has_init(self):
        return self._has_init

    def set_has_init(self, is_init):
        self._has_init = is_init

    def del_has_init(self):
        del self._has_init

    def get_x_dir(self):
        return self._x_dir

    def set_x_dir(self, x_dir_in):
        self._x_dir = x_dir_in

    def del_x_dir(self):
        del self._x_dir

    def get_y_dir(self):
        return self._y_dir

    def set_y_dir(self, y_dir_in):
        self._y_dir = y_dir_in

    def del_y_dir(self):
        del self._y_dir

    has_init = property(get_has_init, set_has_init, del_has_init)
    x_dir = property(get_x_dir, set_x_dir, del_x_dir)
    y_dir = property(get_y_dir, set_y_dir, del_y_dir)


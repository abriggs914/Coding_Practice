import dataclasses
import random
import tkinter
from dataclasses import dataclass

from snake import Grid, Snake
from utility import clamp
from colour_utility import *


@dataclass
class SnakeGameDriver(tkinter.Tk):

    window_title: str = "Look out! It's a Snake!"
    game_grid: Grid = None
    game_snake: Snake = None

    def __init__(self):
        super().__init__()
        self.title(self.window_title)
        self.geometry(f"{600}x{500}")

        self.tv_btn_play = tkinter.StringVar(self, value="play")
        self.btn_play = tkinter.Button(textvariable=self.tv_btn_play, command=self.play_game)

        self.grid()
        self.btn_play.grid(row=1, column=1, rowspan=1, columnspan=1)

        self.canvas_grid_space = tkinter.Canvas(self, background="green", width=400, height=400)
        self.canvas_grid_space.grid(row=2, column=1, rowspan=3, columnspan=3)

        self.grid_tile_space = 1
        self.grid_tiles = []

    def init_game(self, rows=10, cols=10, grid_in="random", snake_pos="random", snake_dir="random"):
        if grid_in == "random":
            # self.game_grid = Grid(random.randint(5, rows), random.randint(5, cols))
            self.game_grid = Grid(rows, cols)
            self.game_grid.init()
        else:
            assert isinstance(grid_in, Grid), f"Error, param 'grid_in' must be a Grid object.\nGot {grid_in=}, {type(grid_in)=}"
            self.game_grid = grid_in
            if not self.game_grid.has_initialized:
                self.game_grid.init()
            else:
                raise ValueError("Error, the given grid param has already been initialized.")

        if snake_pos == "random":
            snake_pos = random.randint(0, self.game_grid.rows * self.game_grid.cols)
        else:
            if not self.game_grid.valid_index(snake_pos):
                raise ValueError(f"Error invalid snake position passed to this grid. {snake_pos=}")
            else:
                snake_pos = self.game_grid.i2rc(snake_pos)
        if snake_dir == "random":
            a, b = (random.randint(-1, 1), random.randint(-1, 1))
        else:
            if not isinstance(snake_dir, tuple):
                raise ValueError(f"Error, param {snake_dir=} must be a tuple")
            else:
                a, b = snake_dir
                if not (isinstance(a, int) and isinstance(b, int)):
                    raise ValueError(f"Error, param {snake_dir=} must be a tuple of integers")
                else:
                    a = clamp(-1, a, 1)
                    b = clamp(-1, b, 1)

        self.game_snake = Snake(head=snake_pos, _x_dir=a, _y_dir=b).init(self.game_grid)
        self.update()  # https://stackoverflow.com/questions/66516760/get-height-width-of-tkinter-canvas
        n_rows = self.game_grid.rows
        n_cols = self.game_grid.cols
        t_width = self.canvas_grid_space.winfo_width()
        t_height = self.canvas_grid_space.winfo_height()
        t_w = (t_width - (self.grid_tile_space * (n_cols + 1))) / n_cols
        t_h = (t_height - (self.grid_tile_space * (n_rows + 1))) / n_rows
        print(f"{n_rows=}, {n_cols=}, {t_width=}, {t_height=}, {t_w=}, {t_h=}")
        print(f"XXX{[[(0 + (((c + 1) * (self.grid_tile_space)) + (c * t_w)), 0 + (((r + 1) * (self.grid_tile_space)) + (r * t_h)), 0 + (((c + 1) * (self.grid_tile_space)) + ((1 + c) * t_w)), 0 + (((r + 1) * (self.grid_tile_space)) + ((1 + r) * t_h))) for c in range(n_cols)] for r in range(n_rows)]}")
        self.grid_tiles = [[
                self.canvas_grid_space.create_rectangle(
                    (((c + 1) * self.grid_tile_space) + (c * t_w)),
                    (((r + 1) * self.grid_tile_space) + (r * t_h)),
                    (((c + 1) * self.grid_tile_space) + ((1 + c) * t_w)),
                    (((r + 1) * self.grid_tile_space) + ((1 + r) * t_h)),
                    # fill=rgb_to_hex(random_colour()))
                    fill="firebrick")
                for c in range(n_cols)
            ] for r in range(n_rows)
        ]



    def play_game(self):
        print(f"{self.game_snake=}")
        move = self.game_snake.move(self.game_grid)
        print(f"new {move=}")

    def draw_grid(self):
        x = self.winfo_pointerx()
        y = self.winfo_pointery()
        abs_coord_x = self.winfo_pointerx() - self.winfo_rootx()
        abs_coord_y = self.winfo_pointery() - self.winfo_rooty()
        x1, y1, x2, y2 = self.canvas_grid_space.winfo_x(), self.canvas_grid_space.winfo_y(), self.canvas_grid_space.winfo_width(), self.canvas_grid_space.winfo_height()
        print(f"\t{x1=}, {x2=}, {y1=}, {y2=}")
        n_rows = self.game_grid.rows
        n_cols = self.game_grid.cols
        # self.canvas_grid_space.create_oval(clamp(x1, abs_coord_x, x2) - 5, clamp(y1, abs_coord_y, y2) - 5, clamp(x1, abs_coord_x, x2) + 5, clamp(y1, abs_coord_y, y2) + 5, fill="orange")
        t_width = self.canvas_grid_space.winfo_width()
        t_height = self.canvas_grid_space.winfo_height()

        r, c = self.game_snake.head
        print(f"{r=}, {c=}")
        print(f"{self.grid_tiles=}")
        self.canvas_grid_space.itemconfigure(self.grid_tiles[r][c], fill="violet")
        print(f"snake head: {self.game_snake.head}")
        for tile_idx in self.game_snake.segments:
            r, c = self.game_grid.i2rc(tile_idx)
            self.canvas_grid_space.itemconfigure(self.grid_tiles[r][c], fill="brown")
        # for row_idx, row_dat in enumerate(self.grid_tiles):
        #     for col_idx, tile in enumerate(row_dat):
        #         idx = self.game_grid.rc2i(row_idx, col_idx)














    def update(self):
        print("update")
        if self.grid_tiles:
            self.draw_grid()
        if self.game_snake:
            self.game_snake.move(self.game_grid)
        super().update()
        self.after(100, self.update)

    def mainloop(self, n: int = ...) -> None:
        print("mainloop")
        self.update()
        super(SnakeGameDriver, self).mainloop()




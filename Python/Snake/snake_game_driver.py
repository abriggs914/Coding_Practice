import dataclasses
import random
import tkinter
from dataclasses import dataclass

from snake import Grid, Snake
from utility import clamp


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

    def init_game(self, rows=100, cols=100, grid_in="random", snake_pos="random", snake_dir="random"):
        if grid_in == "random":
            self.game_grid = Grid(random.randint(5, 100), random.randint(5, 100))
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



    def play_game(self):
        print(f"{self.game_snake=}")
        move = self.game_snake.move(self.game_grid)
        print(f"new {move=}")




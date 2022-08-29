
from snake import Snake, Grid
from snake_game_driver import SnakeGameDriver

if __name__ == '__main__':
    grid_1 = Grid(10, 10).init()
    snake_1 = Snake().init(grid_1).set_direction(1, 1)
    print(f"gen_new_food: {grid_1.gen_new_food()}")
    print(f"{snake_1=}")
    print(f"{grid_1=}")
    print(f"MOVE {snake_1.move(grid_1)}")

    game = SnakeGameDriver()
    game.init_game()
    game.mainloop()

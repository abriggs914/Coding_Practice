import tkinter
from PongGame import PongGame
from tkinter_utility import *
from colour_utility import *


class PongDriver(tkinter.Tk):

    def __init__(self):
        super().__init__()
        self.total_width, self.total_height = 800, 550
        self.title("Pong")
        self.geometry(f"{self.total_width}x{self.total_height}")

        self.game = None
        # self.game_data = tkinter.Variable(self, value={})

        self.frame_top_bar = tkinter.Frame(self)
        self.frame_bottom_bar = tkinter.Frame(self)

        self.tv_button_play_game,\
        self.button_play_game,\
            = button_factory(
                self.frame_top_bar,
                tv_btn="new game",
                kwargs_btn={
                    "command": self.click_btn_new_game
                }
        )
        self.frame_top_bar.pack()
        self.frame_bottom_bar.pack()
        self.button_play_game.pack()

    def click_btn_new_game(self, *event):
        if not self.game:
            self.game = PongGame(self)
            # self.game_data.set(self.game.data)
            self.game.pack()
        else:
            raise Exception("Error, game already in progress.")

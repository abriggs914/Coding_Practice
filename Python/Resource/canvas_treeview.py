import tkinter

from utility import *
import screeninfo
from tkinter_utility import *


class TreeViewCanvas(tkinter.Frame):

    def __init__(self, master, width=600, height=400, auto_grid=True):
        super().__init__(master, height=height, width=width)

        self.auto_grid = auto_grid

        self.frame_title_label = tkinter.Frame(self)
        self.frame_search_objects = tkinter.Frame(self)
        self.frame_tree_canvas = tkinter.Frame(self)
        self.frame_aggregate_row = tkinter.Frame(self)
        self.tree_window = tkinter.Canvas(self.frame_tree_canvas)

        if self.auto_grid:
            self.grid_widgets()

    def grid_widgets(self):
        


class App(tkinter.Tk):

    def __init__(self, width="zoomed", height="zoomed"):
        super().__init__()

        self.x_, self.y_, self.width_, self.height_ = self.calc_monitor_dims()

        if width == height == "zoomed":
            self.state(width)
        else:
            if width == "zoomed":
                self.x_ = 0
                self.height_ = height
            elif height == "zoomed":
                self.y_ = 0
                self.width_ = width
            else:
                width_c = clamp(1, width, self.width_)
                height_c = clamp(1, height, self.height_)
                x = (self.width_ - width_c) // 2
                y = (self.height_ - height_c) // 2
                self.x_, self.y_, self.width_, self.height_ = x, y, width_c, height_c

            self.geometry(f"{self.width_}x{self.height_}+{self.x_}+{self.y_}")

    def calc_monitor_dims(self):
        monitors = screeninfo.get_monitors()

        for mon in monitors:
            print(f"{mon=}")

        lm = get_largest_monitor()
        print(f"\n{lm}")
        return lm.x, lm.y, lm.width, lm.height


if __name__ == '__main__':
    app = App(600, 400)
    app.mainloop()

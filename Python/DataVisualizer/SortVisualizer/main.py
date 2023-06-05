import tkinter

from colour_utility import BLACK, DODGERBLUE
from tkinter_utility import *
from utility import minmax


class App(tkinter.Tk):

    def __init__(self, array):
        super().__init__()

        self.original_array = list(array)
        self.n = len(self.original_array)
        self.geometry(f"700x500")
        self.title("")
        self.width_canvas, self.height_canvas = 400, 150
        self.fc_bars, self.oc_bars = Colour(DODGERBLUE).hex_code, Colour(BLACK).hex_code
        self.canvas = tkinter.Canvas(self, width=self.width_canvas, height=self.height_canvas)

        self.tv_btn_reset,\
        self.btn_reset=\
            button_factory(
                self,
                tv_btn="reset",
                command=self.reset
            )

        self.tv_btn_go,\
        self.btn_go=\
            button_factory(
                self,
                tv_btn="go",
                command=self.go
            )

        self.min_, self.max_ = minmax(self.original_array)
        self.spread = abs(self.max_) + abs(self.min_)
        gc = grid_cells(self.width_canvas, self.n, self.height_canvas, 1, 1, 1)
        bar_dims = gc[0][0]  # x1, y1, x2, y2
        w_bar, h_bar = bar_dims[2] - bar_dims[0], bar_dims[3] - bar_dims[1]
        for i, el in enumerate(self.original_array):
            
        bars = [
            self.canvas.create_rectangle(
                *gc[0][i],
                fill=self.fc_bars,
                outline=self.oc_bars
            )
            for i in range(self.n)
        ]

        self.canvas.pack()
        self.btn_go.pack()
        self.btn_reset.pack()

    def go(self):
        print(f"go")

    def reset(self):
        print(f"reset")


if __name__ == '__main__':
    arr = [8, 18, 9, -1, 0, 6, 1, 5, -7, 15, 16, 7]
    app = App(arr).mainloop()

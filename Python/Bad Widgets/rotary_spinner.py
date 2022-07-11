import tkinter
from colour_utility import *


class RotarySpinner(tkinter.Frame):

    def __init__(self, master, width=300, height=300, radius=60, **kwargs):
        super().__init__(master, kwargs)

        self.background_canvas_width = width
        self.background_canvas_height = height
        self.number = tkinter.IntVar(value=0)
        self.canvas_background = tkinter.Canvas(self, width=self.background_canvas_width, height=self.background_canvas_height, background=rgb_to_hex(BLACK))
        self.canvas_background.pack()

        self.background_rect = [
            self.canvas_background.winfo_x(),
            self.canvas_background.winfo_y(),
            self.background_canvas_width,
            self.background_canvas_height
        ]
        self.rotary_rect = [
            self.background_rect[0] + 10,
            self.background_rect[1] + 10,
            
        ]
        self.oval_rotary = self.canvas_background.create_oval(*self.rotary_rect)


if __name__ == "__main__":

    WIDTH, HEIGHT = 600, 500
    WINDOW = tkinter.Tk()
    WINDOW.geometry(f"{WIDTH}x{HEIGHT}")
    rs = RotarySpinner(WINDOW)
    rs.pack()
    WINDOW.mainloop()

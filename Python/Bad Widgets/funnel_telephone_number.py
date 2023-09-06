import tkinter

from tkinter_utility import *


key_order = [
    ["q", "w", "e", "r", "t", "y", "u", "i", "o", "p"],
    ["a", "s", "d", "f", "g", "h", "j", "K", "l"],
    ["z", "x", "c", "v", "b", "n", "m"]
]


class App(tkinter.Tk):

    def __init__(self):
        super().__init__()

        self.col_f_key_btn = Colour("#CEC8CE")
        self.col_af_key_btn = self.col_f_key_btn.darkened(0.2)
        self.col_f_key_text = self.col_f_key_btn.inverted()
        self.col_af_key_text = self.col_f_key_text.brightened(0.2)

        self.geometry(calc_geometry_tl(0.72, 0.48))

        self.width_canvas, self.height_canvas = 400, 400
        self.frame_buttons = tkinter.Canvas(
            self,
            width=self.width_canvas,
            height=self.height_canvas,
            background="#997345"
        )
        # top_canvas.configure(bg="systemTransparent")
        # self.windows = {}
        self.buttons = {}
        self.texts = {}
        self.create_buttons()
        # self.windows = {
        #     chr(97 + i).upper(): self.frame_buttons.create_window()
        # }

        r, c, rs, cs, ix, iy, x, y, s = grid_keys()
        self.grid_args = {
            "frame_buttons": {r: 0, c: 0, s: "nsew"}
        }
        self.init_grid_args = {
            "frame_buttons"
        }
        self.grid_widgets()
        # self.grid_buttons()

    def grid_buttons(self):
        for i, row in enumerate(key_order):
            for j, k in enumerate(row):
                if not k.upper() in self.buttons:
                    continue
                tv, btn = self.buttons[k.upper()]
                btn.grid(row=i, column=j)

    def grid_widgets(self):
        for k in self.init_grid_args:
            args = self.grid_args[k]
            if not k.startswith("."):
                k = f".{k}"
            print(f"self{k}.grid(**{args})")
            eval(f"self{k}.grid(**{args})")

    def create_buttons(self):
        bwm, bhm = 6, 6
        bwm, bhm = 1, 4
        bx0, by0 = 0, 0
        bw, bh = 30, 45
        tw, th = 3, 1
        bx0 += (bwm / 2)
        by0 += (bhm / 2)
        for i, row in enumerate(key_order):
            bx0 = (self.width_canvas - (bw * len(row)) - bwm) / 2
            for j, k in enumerate(row):
                k = k.upper()
                # self.buttons[k] = button_factory(
                #     self.frame_buttons,
                #     tv_btn=k,
                #     kwargs_btn={
                #         "width": tw,
                #         "height": th
                #     },
                #     command=lambda k_=k: self.click_letter(k_)
                # )
                self.buttons[k] = self.frame_buttons.create_rectangle(
                    ((j + 0) * bw) + bx0 + (bwm / 2),
                    ((i + 0) * bh) + by0 + (bhm / 2),
                    ((j + 1) * bw) + bx0 - (bwm / 2),
                    ((i + 1) * bh) + by0 - (bhm / 2),
                    fill=self.col_f_key_btn.hex_code,
                    activefill=self.col_af_key_btn.hex_code,
                )
                self.texts[k] = self.frame_buttons.create_text(
                    ((j + 0.5) * bw) + bx0 + (bwm / 4),
                    ((i + 0.5) * bh) + by0 + (bhm / 4),
                    text=k,
                    fill=self.col_f_key_text.hex_code,
                    activefill=self.col_af_key_text.hex_code,
                )
                self.frame_buttons.tag_bind(self.texts[k], "<Enter>", lambda event, k_=k: self.mouse_enter_key(event, k_))
                self.frame_buttons.tag_bind(self.texts[k], "<Leave>", lambda event, k_=k: self.mouse_exit_key(event, k_))
                self.frame_buttons.tag_bind(self.texts[k], "<ButtonRelease-1>", lambda event, k_=k: self.click_key(event, k_))
                self.frame_buttons.tag_bind(self.buttons[k], "<ButtonRelease-1>", lambda event, k_=k: self.click_key(event, k_))
                # self.windows[k] = self.frame_buttons.create_window(
                #     ((j + 0.5) * bw) + by0,
                #     ((i + 0.5) * bh) + bx0,
                #     width=bw,
                #     height=bh
                #     ,
                #     window=self.buttons[k]
                # )



        # self.buttons = {
        #     chr(97 + i).upper(): button_factory(
        #         self.frame_buttons,
        #         tv_btn=chr(97 + i).upper()
        #     ) for i in range(26)
        # }

    def click_letter(self, k):
        # win = self.windows[k]
        # coords = self.frame_buttons.bbox(win)
        # coords = self.frame_buttons.coords(win)
        # x, y = list(map(lambda x: x+10, coords))
        # print(f"{k=}, {win=}, {x=}, {y=}, {coords=}")
        print(f"{k=}")
        # self.frame_buttons.create_text(x, y, text=k, fill="#0024FF", font="Arial 32")
        self.frame_buttons.create_text(110, 110, text=k, fill="#0024FF", font="Arial 56")

    def mouse_enter_key(self, event, k):
        t = self.buttons[k]
        # f = self.frame_buttons.itemcget(t, "fill")
        # af = self.frame_buttons.itemcget(t, "activefill")
        self.frame_buttons.itemconfigure(t, fill=self.col_af_key_btn.hex_code)

    def mouse_exit_key(self, event, k):
        t = self.buttons[k]
        self.frame_buttons.itemconfigure(t, fill=self.col_f_key_btn.hex_code)

    def click_key(self, event, k):
        self.frame_buttons.create_text(110, 110, text=k, fill="#0024FF", font="Arial 56")



if __name__ == '__main__':

    app = App()
    app.mainloop()

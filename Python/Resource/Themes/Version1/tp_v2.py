import tkinter

import ttkwidgets.font
from ttkwidgets import *

from colour_utility import *
from tkinter_utility import button_factory, label_factory


class App(tkinter.Tk):

    def __init__(self, geometry=(900, 600)):
        super().__init__()
        self.frame_buttons = tkinter.Frame(self, name="frame_btns")
        self.geometry("{}x{}".format(*geometry))

        self.tv_btn_font_chooser, \
            self.btn_font_chooser = \
            button_factory(
                self.frame_buttons,
                tv_btn="font",
                command=self.toggle_font_chooser
            )

        self.tv_btn_text_colour, \
            self.btn_text_colour = \
            button_factory(
                self.frame_buttons,
                tv_btn="text colour",
                command=self.toggle_text_colour
            )

        self.frame_elem_controller = tkinter.Frame(self)
        self.frame_font_chooser = tkinter.Frame(self.frame_elem_controller)
        self.ctl_font_chooser = ttkwidgets.font.FontSelectFrame(
            self.frame_font_chooser,
            callback=self.update_font_chooser
        )
        self.frame_text_colour = tkinter.Frame(self.frame_elem_controller)
        self.ctl_text_colour = ttkwidgets.C(
            self.frame_text_colour,
            callback=self.update_text_colour
        )

        self.frame_demos = tkinter.Frame(self, background=Colour(TEAL).hex_code)
        self.demo_tv_lbl_font, \
            self.demo_lbl_font = \
            label_factory(
                self.frame_demos,
                tv_label="Demo font!"
            )
        self.demo_tv_lbl_text_colour, \
            self.demo_lbl_text_colour = \
            label_factory(
                self.frame_demos,
                tv_label="Demo text colour!"
            )

        self.ctls_list = {
            "ctl_font_chooser",
            "ctl_text_colour"
        }

        r, c, rs, cs, ix, iy, x, y, s = self.grid_keys()

        self.grid_args = {
            "frame_buttons": {r: 0, c: 0},
            "frame_elem_controller": {r: 1, c: 0},
            "frame_demos": {r: 2, c: 0, x: 10, y: 10},

            # frame_buttons
            "btn_font_chooser": {r: 0, c: 0},
            "btn_text_colour": {r: 0, c: 1},

            # frame_elem_controller
            "frame_font_chooser": {r: 0, c: 0},
            "frame_text_colour": {r: 0, c: 0},

            # frame_font_chooser
            "ctl_font_chooser": {r: 0, c: 0},

            # frame_text_colour
            "ctl_text_colour": {r: 0, c: 0},

            # frame_demos
            "demo_lbl_font": {r: 0, c: 0, x: 10, y: 10},
            "demo_lbl_text_colour": {r: 0, c: 1, x: 10, y: 10}

        }
        self.init_grid_args = {
            "frame_buttons",
            "frame_elem_controller",
            "btn_font_chooser",
            "btn_text_colour",
            "ctl_font_chooser",
            "ctl_text_colour",
            "frame_demos",
            "demo_lbl_font",
            "demo_lbl_text_colour"
        }

        self.grid_widgets()

    def grid_widgets(self):
        for k in self.grid_args:
            if k in self.init_grid_args:
                v = self.grid_args[k]
                eval(f"self.{k}.grid(**{v})")
            else:
                print(f"skipping {k=}")

    def grid_keys(self):
        return "row", "column", "rowspan", "columnspan", "ipadx", "ipady", "padx", "pady", "sticky"

    def update_font_chooser(self, font_tuple):
        print(f"{font_tuple=}")
        font = self.ctl_font_chooser.font[0]
        if font is not None:
            self.demo_lbl_font.configure(font=font)

    def update_text_colour(self, *args):
        print(f"{args=}")
        # font = self.ctl_font_chooser.font[0]
        # if font is not None:
        #     self.demo_lbl_font.configure(font=font)

    def toggle_helper(self, elem):
        if not (info := eval(f"self.{elem}.winfo_manager()")):
            # print(f"now showing {elem=} {info=}")
            eval(f"self.{elem}.grid(**{self.grid_args[elem]})")

            for k in self.ctls_list:
                if k != elem:
                    eval(f"self.{k}.grid_forget()")
        else:
            # print(f"now hiding {elem=} {info=}")
            eval(f"self.{elem}.grid_forget()")
            # print(f"already open")

    def toggle_font_chooser(self):
        self.toggle_helper(elem="frame_font_chooser")
        # if not (info := eval(f"self.{elem}.winfo_manager()")):
        #     # print(f"now showing {elem=} {info=}")
        #     eval(f"self.{elem}.grid(**{self.grid_args[elem]})")
        # else:
        #     # print(f"now hiding {elem=} {info=}")
        #     eval(f"self.{elem}.grid_forget()")
        #     # print(f"already open")

    def toggle_text_colour(self, elem="frame_text_colour"):
        self.toggle_helper(elem="frame_text_colour")


if __name__ == '__main__':
    App().mainloop()

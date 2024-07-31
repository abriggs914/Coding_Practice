from Version4.utility import percent
from customtkinter_utility import *
from colour_utility import *


class App(ctk.CTk):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.def_col_canvas = Colour(WHITE)
        self.col_canvas = Colour(self.def_col_canvas)

        self.canvas = ctk.CTkCanvas(
            self,
            width=250,
            height=250,
            background=self.col_canvas.hex_code
        )

        self.frame_sliders = ctk.CTkFrame(self)

        self.vars = [
            ctk.IntVar(self, name=f"red", value=self.def_col_canvas.rgb_code[0]),
            ctk.IntVar(self, name=f"green", value=self.def_col_canvas.rgb_code[1]),
            ctk.IntVar(self, name=f"blue", value=self.def_col_canvas.rgb_code[2])
        ]

        self.lbl_sl_red = label_factory(
            self.frame_sliders,
            tv_label=f"Red:"
        )
        self.sl_red = ctk.CTkSlider(
            self.frame_sliders,
            from_=0,
            to=255,
            variable=self.vars[0]
        )

        self.lbl_sl_green = label_factory(
            self.frame_sliders,
            tv_label=f"Green:"
        )
        self.sl_green = ctk.CTkSlider(
            self.frame_sliders,
            from_=0,
            to=255,
            variable=self.vars[1]
        )

        self.lbl_sl_blue = label_factory(
            self.frame_sliders,
            tv_label=f"Blue:"
        )
        self.sl_blue = ctk.CTkSlider(
            self.frame_sliders,
            from_=0,
            to=255,
            variable=self.vars[2]
        )

        self.frame_slider_res = ctk.CTkFrame(
            self.frame_sliders,
            width=250,
            height=80
        )

        w_lbl = 40
        bg_lbl = "#565656"
        font_lbl = ("Calibri", 16, "bold")

        self.lbl_leg_hex = label_factory(
            self.frame_slider_res,
            tv_label=f"Hex:",
            kwargs_label={
                "text_color": "#323232",
                "fg_color": bg_lbl,
                "font": font_lbl,
                "width": w_lbl
            }
        )

        self.lbl_val_hex = label_factory(
            self.frame_slider_res,
            tv_label=f"",
            kwargs_label={
                "font": font_lbl
            }
        )

        self.lbl_leg_red = label_factory(
            self.frame_slider_res,
            tv_label=f"R:",
            kwargs_label={
                "text_color": "#AA2323",
                "fg_color": bg_lbl,
                "font": font_lbl,
                "width": w_lbl
            }
        )

        self.lbl_val_red = label_factory(
            self.frame_slider_res,
            tv_label=f"",
            kwargs_label={
                "font": font_lbl
            }
        )

        self.lbl_leg_green = label_factory(
            self.frame_slider_res,
            tv_label=f"G:",
            kwargs_label={
                "text_color": "#23AA23",
                "fg_color": bg_lbl,
                "font": font_lbl,
                "width": w_lbl
            }
        )

        self.lbl_val_green = label_factory(
            self.frame_slider_res,
            tv_label=f"",
            kwargs_label={
                "font": font_lbl
            }
        )

        self.lbl_leg_blue = label_factory(
            self.frame_slider_res,
            tv_label=f"B:",
            kwargs_label={
                "text_color": "#2323AA",
                "fg_color": bg_lbl,
                "font": font_lbl,
                "width": w_lbl
            }
        )

        self.lbl_val_blue = label_factory(
            self.frame_slider_res,
            tv_label=f"",
            kwargs_label={
                "font": font_lbl
            }
        )

        self.frame_controls = ctk.CTkFrame(
            self
        )

        self.frame_ctl_sliders = ctk.CTkFrame(
            self.frame_controls
        )

        def_p = 10

        self.ctl_vars = [
            ctk.IntVar(self, name=f"red_p", value=def_p),
            ctk.IntVar(self, name=f"green_p", value=def_p),
            ctk.IntVar(self, name=f"blue_p", value=def_p),
            ctk.IntVar(self, name=f"dark_p", value=def_p),
            ctk.IntVar(self, name=f"light_p", value=def_p)
        ]

        self.lbl_ctl_sl_red = label_factory(
            self.frame_ctl_sliders,
            tv_label=f"Red:"
        )
        self.ctl_sl_red = ctk.CTkSlider(
            self.frame_ctl_sliders,
            from_=0,
            to=100,
            variable=self.ctl_vars[0]
        )
        self.ctl_btn_red = button_factory(
            self.frame_ctl_sliders,
            tv_btn=f"{percent(def_p / 100)} Red-er",
            command=self.click_ctl_red
        )

        self.lbl_ctl_sl_green = label_factory(
            self.frame_ctl_sliders,
            tv_label=f"Green:"
        )
        self.ctl_sl_green = ctk.CTkSlider(
            self.frame_ctl_sliders,
            from_=0,
            to=100,
            variable=self.ctl_vars[1]
        )
        self.ctl_btn_green = button_factory(
            self.frame_ctl_sliders,
            tv_btn=f"{percent(def_p / 100)} Green-er",
            command=self.click_ctl_green
        )

        self.lbl_ctl_sl_blue = label_factory(
            self.frame_ctl_sliders,
            tv_label=f"Blue:"
        )
        self.ctl_sl_blue = ctk.CTkSlider(
            self.frame_ctl_sliders,
            from_=0,
            to=100,
            variable=self.ctl_vars[2]
        )
        self.ctl_btn_blue = button_factory(
            self.frame_ctl_sliders,
            tv_btn=f"{percent(def_p / 100)} Blue-er",
            command=self.click_ctl_blue
        )

        self.lbl_ctl_sl_dark = label_factory(
            self.frame_ctl_sliders,
            tv_label=f"Dark:"
        )
        self.ctl_sl_dark = ctk.CTkSlider(
            self.frame_ctl_sliders,
            from_=0,
            to=100,
            variable=self.ctl_vars[3]
        )
        self.ctl_btn_dark = button_factory(
            self.frame_ctl_sliders,
            tv_btn=f"{percent(def_p / 100)} Dark-er",
            command=self.click_ctl_dark
        )

        self.lbl_ctl_sl_light = label_factory(
            self.frame_ctl_sliders,
            tv_label=f"Light:"
        )
        self.ctl_sl_light = ctk.CTkSlider(
            self.frame_ctl_sliders,
            from_=0,
            to=100,
            variable=self.ctl_vars[4]
        )
        self.ctl_btn_light = button_factory(
            self.frame_ctl_sliders,
            tv_btn=f"{percent(def_p / 100)} Bright-er",
            command=self.click_ctl_light
        )

        self.frame_slider_res.grid_propagate(False)
        for i in range(6):
            self.frame_slider_res.grid_columnconfigure(i, weight=int(100/6))

        self.lbl_val_red[0].set(self.col_canvas.rgb_code[0])
        self.lbl_val_green[0].set(self.col_canvas.rgb_code[1])
        self.lbl_val_blue[0].set(self.col_canvas.rgb_code[2])
        self.lbl_val_hex[0].set(self.col_canvas.hex_code)

        self.vars[0].trace_variable("w", self.update_sl_red)
        self.vars[1].trace_variable("w", self.update_sl_green)
        self.vars[2].trace_variable("w", self.update_sl_blue)

        self.ctl_vars[0].trace_variable("w", self.update_sl_ctl_red)
        self.ctl_vars[1].trace_variable("w", self.update_sl_ctl_green)
        self.ctl_vars[2].trace_variable("w", self.update_sl_ctl_blue)
        self.ctl_vars[3].trace_variable("w", self.update_sl_ctl_dark)
        self.ctl_vars[4].trace_variable("w", self.update_sl_ctl_light)

        frame_px, frame_py = 5, 5
        lbl_px, lbl_py = 5, 5

        # self
        self.frame_sliders.grid(row=0, column=0, rowspan=1, columnspan=1, padx=frame_px, pady=frame_py)
        self.canvas.grid(row=0, column=1, rowspan=1, columnspan=1)
        self.frame_controls.grid(row=0, column=2, rowspan=1, columnspan=1)

        # frame_sliders
        self.lbl_sl_red[1].grid(row=0, column=0, rowspan=1, columnspan=1)
        self.sl_red.grid(row=0, column=1, rowspan=1, columnspan=1)
        self.lbl_sl_green[1].grid(row=1, column=0, rowspan=1, columnspan=1)
        self.sl_green.grid(row=1, column=1, rowspan=1, columnspan=1)
        self.lbl_sl_blue[1].grid(row=2, column=0, rowspan=1, columnspan=1)
        self.sl_blue.grid(row=2, column=1, rowspan=1, columnspan=1)
        self.frame_slider_res.grid(row=3, column=0, rowspan=1, columnspan=2, padx=frame_px, pady=frame_py)

        # frame_slider_res
        self.lbl_leg_hex[1].grid(row=0, column=0, rowspan=1, columnspan=2, padx=lbl_px, pady=lbl_py)
        self.lbl_val_hex[1].grid(row=0, column=2, rowspan=1, columnspan=4, padx=lbl_px, pady=lbl_py)
        self.lbl_leg_red[1].grid(row=1, column=0, rowspan=1, columnspan=1, padx=lbl_px, pady=lbl_py)
        self.lbl_val_red[1].grid(row=1, column=1, rowspan=1, columnspan=1, padx=lbl_px, pady=lbl_py)
        self.lbl_leg_green[1].grid(row=1, column=2, rowspan=1, columnspan=1, padx=lbl_px, pady=lbl_py)
        self.lbl_val_green[1].grid(row=1, column=3, rowspan=1, columnspan=1, padx=lbl_px, pady=lbl_py)
        self.lbl_leg_blue[1].grid(row=1, column=4, rowspan=1, columnspan=1, padx=lbl_px, pady=lbl_py)
        self.lbl_val_blue[1].grid(row=1, column=5, rowspan=1, columnspan=1, padx=lbl_px, pady=lbl_py)

        # frame_controls
        self.frame_ctl_sliders.grid(row=0, column=0, rowspan=1, columnspan=1)

        # frame_ctl_sliders
        self.lbl_ctl_sl_red[1].grid(row=0, column=0, rowspan=1, columnspan=1)
        self.ctl_sl_red.grid(row=0, column=1, rowspan=1, columnspan=1)
        self.ctl_btn_red[1].grid(row=0, column=2, rowspan=1, columnspan=1)
        self.lbl_ctl_sl_green[1].grid(row=1, column=0, rowspan=1, columnspan=1)
        self.ctl_sl_green.grid(row=1, column=1, rowspan=1, columnspan=1)
        self.ctl_btn_green[1].grid(row=1, column=2, rowspan=1, columnspan=1)
        self.lbl_ctl_sl_blue[1].grid(row=2, column=0, rowspan=1, columnspan=1)
        self.ctl_sl_blue.grid(row=2, column=1, rowspan=1, columnspan=1)
        self.ctl_btn_blue[1].grid(row=2, column=2, rowspan=1, columnspan=1)
        self.lbl_ctl_sl_dark[1].grid(row=3, column=0, rowspan=1, columnspan=1)
        self.ctl_sl_dark.grid(row=3, column=1, rowspan=1, columnspan=1)
        self.ctl_btn_dark[1].grid(row=3, column=2, rowspan=1, columnspan=1)
        self.lbl_ctl_sl_light[1].grid(row=4, column=0, rowspan=1, columnspan=1)
        self.ctl_sl_light.grid(row=4, column=1, rowspan=1, columnspan=1)
        self.ctl_btn_light[1].grid(row=4, column=2, rowspan=1, columnspan=1)

    def update_canvas_background(self, r, g, b):
        new = Colour(r, g, b)
        self.col_canvas = new
        # print(f"{r}, {g}, {b}")
        self.canvas.configure(background=new.hex_code)
        self.lbl_val_hex[0].set(self.col_canvas.hex_code)

    def update_sl_red(self, *args):
        r = self.vars[0].get()
        # print(f"{r=}")
        old = self.col_canvas
        o_r, o_g, o_b = old.rgb_code
        self.update_canvas_background(r, o_g, o_b)
        self.lbl_val_red[0].set(r)

    def update_sl_green(self, *args):
        g = self.vars[1].get()
        # print(f"{g=}")
        old = self.col_canvas
        o_r, o_g, o_b = old.rgb_code
        self.update_canvas_background(o_r, g, o_b)
        self.lbl_val_green[0].set(g)

    def update_sl_blue(self, *args):
        b = self.vars[2].get()
        # print(f"{b=}")
        old = self.col_canvas
        o_r, o_g, o_b = old.rgb_code
        self.update_canvas_background(o_r, o_g, b)
        self.lbl_val_blue[0].set(b)

    def update_sl_ctl_red(self, *args):
        r = self.ctl_vars[0].get()
        self.ctl_btn_red[0].set(f"{percent(r / 100)} Red-er")
        # print(f"{r=}")

    def update_sl_ctl_green(self, *args):
        g = self.ctl_vars[1].get()
        self.ctl_btn_green[0].set(f"{percent(g / 100)} Green-er")
        # print(f"{g=}")

    def update_sl_ctl_blue(self, *args):
        b = self.ctl_vars[2].get()
        self.ctl_btn_blue[0].set(f"{percent(b / 100)} Blue-er")
        # print(f"{b=}")

    def update_sl_ctl_dark(self, *args):
        d = self.ctl_vars[3].get()
        self.ctl_btn_dark[0].set(f"{percent(d / 100)} Dark-er")
        # print(f"{b=}")

    def update_sl_ctl_light(self, *args):
        l = self.ctl_vars[4].get()
        self.ctl_btn_light[0].set(f"{percent(l / 100)} Bright-er")
        # print(f"{b=}")

    def click_ctl_red(self):
        pr = self.ctl_vars[0].get()
        # print(f"{pr=}")
        new = reder(self.col_canvas, pr / 100)
        self.update_canvas_background(*new.rgb_code)
        rgb = new.rgb_code
        for i in range(3):
            self.vars[i].set(rgb[i])

    def click_ctl_green(self):
        pg = self.ctl_vars[1].get()
        # print(f"{pg=}")
        new = greener(self.col_canvas, pg / 100)
        self.update_canvas_background(*new.rgb_code)
        rgb = new.rgb_code
        for i in range(3):
            self.vars[i].set(rgb[i])

    def click_ctl_blue(self):
        pb = self.ctl_vars[2].get()
        # print(f"{pb=}")
        new = bluer(self.col_canvas, pb / 100)
        self.update_canvas_background(*new.rgb_code)
        rgb = new.rgb_code
        for i in range(3):
            self.vars[i].set(rgb[i])

    def click_ctl_dark(self):
        pb = self.ctl_vars[3].get()
        # print(f"{pb=}")
        new = Colour(darken(self.col_canvas, pb / 100))
        self.update_canvas_background(*new.rgb_code)
        rgb = new.rgb_code
        for i in range(3):
            self.vars[i].set(rgb[i])

    def click_ctl_light(self):
        pb = self.ctl_vars[4].get()
        # print(f"{pb=}")
        new = Colour(brighten(self.col_canvas, pb / 100))
        self.update_canvas_background(*new.rgb_code)
        rgb = new.rgb_code
        for i in range(3):
            self.vars[i].set(rgb[i])

def test_red_blue_green_sliders():
    app = App()
    app.mainloop()


if __name__ == "__main__":
    test_red_blue_green_sliders()
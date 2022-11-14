import tkinter
from utility import dict_print
from colour_utility import *


class PongGame(tkinter.Canvas):

    def __init__(
            self,
            master,
            radius=6,
            total_width=600,
            total_height=450
    ):
        super().__init__(master)

        self.radius = radius
        self.canvas_background = rgb_to_hex(GRAY_45)
        self.total_width, self.total_height = total_width, total_height
        self.configure(
            width=self.total_width,
            height=self.total_height,
            background=self.canvas_background
        )

        center_xy = self.calc_center_point()

        self.data_ball = {
            "x": center_xy[0],
            "y": center_xy[1],
            "radius": self.radius,
            "x_vel": 0,
            "y_vel": 0,
            "x_acc": 0,
            "y_acc": 0,
            "max_x_vel": 0,
            "max_y_vel": 0,
            "max_x_acc": 0,
            "max_y_acc": 0,
            "x_rate_acc": 0.2,
            "y_rate_acc": 0.2,
            "x_rate_dacc": 0.92,
            "y_rate_dacc": 0.92,
            "x_change": 0,
            "y_change": 0,
            "fill": rgb_to_hex(WILDERNESS_MINT),
            "outline": rgb_to_hex(GRAY_17),
            "activefill": brighten(WILDERNESS_MINT, 0.25, False),
            "activeoutline": brighten(GRAY_17, 0.25, False),
            "disabledfill": darken(WILDERNESS_MINT, 0.25, False),
            "disabledoutline": darken(GRAY_17, 0.25, False)
        }

        self.tag_ball = self.create_oval(
            self.data_ball["x"] - self.radius,
            self.data_ball["y"] - self.radius,
            self.data_ball["x"] + self.radius,
            self.data_ball["y"] + self.radius,
            fill=self.data_ball["fill"],
            outline=self.data_ball["outline"],
            activefill=self.data_ball["activefill"],
            activeoutline=self.data_ball["activeoutline"],
            disabledfill=self.data_ball["disabledfill"],
            disabledoutline=self.data_ball["disabledoutline"]
        )

        self.lb_width, self.lb_height = 20, 100
        self.lb_x_r_acc, self.lb_y_r_acc = 0.2, 0.2
        self.lb_x_r_dacc, self.lb_y_r_dacc = 0.92, 0.92
        self.rb_width, self.rb_height = 20, 100
        self.rb_x_r_acc, self.rb_y_r_acc = 0.2, 0.2
        self.rb_x_r_dacc, self.rb_y_r_dacc = 0.92, 0.92

        self.data_left_bumper = {
            "x": self.total_width * 0.1,
            "y": center_xy[1],
            "w": self.lb_width,
            "h": self.lb_height,
            "x_vel": 0,
            "y_vel": 0,
            "x_acc": 0,
            "y_acc": 0,
            "max_x_vel": 0,
            "max_y_vel": 0,
            "max_x_acc": 0,
            "max_y_acc": 0,
            "x_rate_acc": 0.2,
            "y_rate_acc": 0.2,
            "x_rate_dacc": 0.92,
            "y_rate_dacc": 0.92,
            "x_change": 0,
            "y_change": 0,
            "fill": rgb_to_hex(FIREBRICK_3),
            "outline": rgb_to_hex(GRAY_25),
            "activefill": brighten(FIREBRICK_3, 0.25, False),
            "activeoutline": brighten(GRAY_25, 0.25, False),
            "disabledfill": darken(FIREBRICK_3, 0.25, False),
            "disabledoutline": darken(GRAY_25, 0.25, False)
        }

        self.tag_left_bumper = self.create_rectangle(
            self.data_left_bumper["x"] - (self.data_left_bumper["w"] / 2),
            self.data_left_bumper["y"] - (self.data_left_bumper["h"] / 2),
            self.data_left_bumper["x"] + (self.data_left_bumper["w"] / 2),
            self.data_left_bumper["y"] + (self.data_left_bumper["h"] / 2),
            fill=self.data_left_bumper["fill"],
            outline=self.data_left_bumper["outline"],
            activefill=self.data_left_bumper["activefill"],
            activeoutline=self.data_left_bumper["activeoutline"],
            disabledfill=self.data_left_bumper["disabledfill"],
            disabledoutline=self.data_left_bumper["disabledoutline"]
        )

        self.data_right_bumper = {
            "x": self.total_width * 0.9,
            "y": center_xy[1],
            "w": self.rb_width,
            "h": self.rb_height,
            "x_vel": 0,
            "y_vel": 0,
            "x_acc": 0,
            "y_acc": 0,
            "max_x_vel": 0,
            "max_y_vel": 0,
            "max_x_acc": 0,
            "max_y_acc": 0,
            "x_rate_acc": 0.2,
            "y_rate_acc": 0.2,
            "x_rate_dacc": 0.92,
            "y_rate_dacc": 0.92,
            "x_change": 0,
            "y_change": 0,
            "fill": rgb_to_hex(FIREBRICK_3),
            "outline": rgb_to_hex(GRAY_25),
            "activefill": brighten(FIREBRICK_3, 0.25, False),
            "activeoutline": brighten(GRAY_25, 0.25, False),
            "disabledfill": darken(FIREBRICK_3, 0.25, False),
            "disabledoutline": darken(GRAY_25, 0.25, False)
        }

        self.tag_right_bumper = self.create_rectangle(
            self.data_right_bumper["x"] - (self.data_right_bumper["w"] / 2),
            self.data_right_bumper["y"] - (self.data_right_bumper["h"] / 2),
            self.data_right_bumper["x"] + (self.data_right_bumper["w"] / 2),
            self.data_right_bumper["y"] + (self.data_right_bumper["h"] / 2),
            fill=self.data_right_bumper["fill"],
            outline=self.data_right_bumper["outline"],
            activefill=self.data_right_bumper["activefill"],
            activeoutline=self.data_right_bumper["activeoutline"],
            disabledfill=self.data_right_bumper["disabledfill"],
            disabledoutline=self.data_right_bumper["disabledoutline"]
        )

        self.nametowidget(self.master).bind("<KeyPress-w>", self.key_press_w)
        self.nametowidget(self.master).bind("<KeyPress-s>", self.key_press_s)
        self.nametowidget(self.master).bind("<KeyPress-Up>", self.key_press_up)
        self.nametowidget(self.master).bind("<KeyPress-Down>", self.key_press_down)

    def calc_center_point(self):
        return self.total_width / 2, self.total_height / 2

    def key_press_w(self, *event):
        print("W")
        # y_acc = self.lb_y_r_acc
        # if abs(self.data_left_bumper["max_y_acc"])

        x = 0
        y = self.data_left_bumper["y"] - self.data_left_bumper["y_vel"]

        x_acc, y_acc = self.data_left_bumper["x_acc"], self.data_left_bumper["y_acc"]
        y_acc += -self.data_left_bumper["y_rate_acc"]
        self.data_left_bumper["y_change"] += y_acc
        self.data_left_bumper["y_acc"] = y_acc
        if abs(self.data_left_bumper["y_change"]) >= self.data_left_bumper["max_y_vel"]:
            self.data_left_bumper["y_change"] = self.data_left_bumper["y_change"] / abs(self.data_left_bumper["y_change"]) * self.data_left_bumper["max_y_vel"]

        # self.data_left_bumper["y_acc"] == 0:

        # self.data_left_bumper["y"] = y
        # self.data_left_bumper["y_vel"] *= self.data_left_bumper["y_acc"]
        # self.update_left_bumper(x, y)
        self.data_left_bumper["y"] = clamp(0, self.data_left_bumper["y"] + self.data_left_bumper["y_change"], self.total_height - (self.data_left_bumper["h"] / 2))
        self.update_left_bumper(self.data_left_bumper["x"], self.data_left_bumper["y"])
        print(dict_print(self.data_left_bumper, "self.data_left_bumper"))

    def key_press_s(self, *event):
        print("S")

    def key_press_up(self, *event):
        print("UP")

    def key_press_down(self, *event):
        print("DOWN")

    def update_left_bumper(self, x, y):
        self.moveto(self.tag_left_bumper, x, y)

    def update_right_bumper(self, x, y):
        self.moveto(self.tag_right_bumper, x, y)

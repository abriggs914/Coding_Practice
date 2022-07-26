import math
import tkinter
from colour_utility import *
from utility import distance, dict_print, calc_bounds
from game_state_machine import GSM, BooleanGSM
import numpy as np


def get_angle(p0, p1=np.array([0, 0]), p2=None):
    ''' compute angle (in degrees) for p0p1p2 corner
        Inputs:
        p0,p1,p2 - points in the form of [x,y]
    '''
    if p2 is None:
        p2 = p1 + np.array([1, 0])
    v0 = np.array(p0) - np.array(p1)
    v1 = np.array(p2) - np.array(p1)

    angle = np.degrees(np.math.atan2(np.linalg.det([v0, v1]), np.dot(v0, v1)))
    if angle < 0:
        # angle %= 360
        angle = abs(angle)
    else:
        angle = 360 - angle
    # return 360 - angle
    return angle


class RotarySpinner(tkinter.Frame):

    def __init__(self, master, width=300, height=300, radius=60, stop_angle=345, number_radius=15, **kwargs):
        super().__init__(master, kwargs)

        self.gsm_drag_number = GSM(name="drag_number", options=list(range(10)))
        self.gsm_is_dragging = BooleanGSM(name="gsm_is_dragging", t_first=False)
        self.background_canvas_width = width
        self.background_canvas_height = height
        self.number = tkinter.IntVar(value=0)
        self.entry_number = tkinter.Entry(self, textvariable=self.number,justify="center",state="readonly")
        self.entry_number.pack()
        self.canvas_background = tkinter.Canvas(self, width=self.background_canvas_width, height=self.background_canvas_height, background=rgb_to_hex(BLACK))
        self.canvas_background.pack()

        self.background_rect = [
            self.canvas_background.winfo_x(),
            self.canvas_background.winfo_y(),
            self.background_canvas_width,
            self.background_canvas_height
        ]
        self.stop_angle = stop_angle
        self.rotary_radius = 120
        self.number_radius = number_radius
        self.center_rotary = self.background_rect[0] + (self.background_rect[2] / 2), self.background_rect[1] + (self.background_rect[3] / 2)
        self.rotary_rect = [
            self.center_rotary[0] - self.rotary_radius,
            self.center_rotary[1] - self.rotary_radius,
            self.center_rotary[0] + self.rotary_radius,
            self.center_rotary[1] + self.rotary_radius
        ]
        self.colour_rotary_oval = SNOW_3
        self.oval_rotary = self.canvas_background.create_oval(*self.rotary_rect, fill=rgb_to_hex(self.colour_rotary_oval))

        # start_positions = self.calc_start_positions()
        # self.oval_numbers = [
        #     self.canvas_background.create_oval()
        # ]

        # xc = self.angle_on_circle(270)
        # self.canvas_background.create_oval(xc[0] - xr, xc[1] - xr, xc[0] + xr, xc[1] + xr, fill=rgb_to_hex(ORANGE_2))
        self.ovals = {}
        self.calc_ovals()
        # self.ovals.update({i: {"center": positions[i]} for i in range(10)})
        # positions.reverse()
        # print(f"{positions}")
        # rainbow = rainbow_gradient(10)
        # for i in range(10):
        #     data = self.ovals[i]
        #     data.update({"rect": [
        #         data["center"][0] - xr,
        #         data["center"][1] - xr,
        #         data["center"][0] + xr,
        #         data["center"][1] + xr
        #     ]})
        #     self.canvas_background.create_oval(*data["rect"], fill=rgb_to_hex(rainbow.__next__()))
        #
        # print(f"A")
        rainbow = rainbow_gradient(10)
        for i in range(10):
            colour = rainbow.__next__()
            self.ovals[i].update({
                "oval": self.canvas_background.create_oval(*self.ovals[i]["rect"], fill=rgb_to_hex(colour)),
                "text": self.canvas_background.create_text(*self.ovals[i]["center"], fill=rgb_to_hex(font_foreground(colour)), text=str(i))
            })

        # print(f"B")
        self.rotary_stopper_line = self.canvas_background.create_line(*self.angle_on_circle(self.stop_angle, radius=self.rotary_radius*0.8), *self.angle_on_circle(self.stop_angle, radius=self.rotary_radius*1.2), fill=rgb_to_hex(BURLYWOOD_4), width=5)
        self.mouse_dot = self.canvas_background.create_oval(calc_bounds(self.center_rotary, 14), fill=rgb_to_hex(LIMEGREEN))
        self.canvas_background.bind("<B1-Motion>", self.mouse_motion)
        self.canvas_background.bind("<ButtonRelease-1>", self.mouse_button_release)
        # print(f"C")
        # print(dict_print(self.ovals, "Ovals A"))

    def calc_ovals_1(self, start_angle=None, do_stop=False):
        # start_angle = start_angle if start_angle is not None else self.stop_angle
        if do_stop:
            # stop_angle = None if start_angle is None else ((((start_angle + 180) % 360) + 135) % 360)
            stop_angle = start_angle
            positions = self.calc_start_positions(stop_angle=stop_angle)
            positions.reverse()
            # print(dict_print(self.ovals, "PRE OVALS"))
            if not self.ovals:
                self.ovals.update({i: {"center": positions[i]} for i in range(10)})
            # print(dict_print(self.ovals, "POST OVALS"))
            print(f"{positions=}")
            for i in range(10):
                self.ovals[i].update({"rect": [
                    self.ovals[i]["center"][0] - self.number_radius,
                    self.ovals[i]["center"][1] - self.number_radius,
                    self.ovals[i]["center"][0] + self.number_radius,
                    self.ovals[i]["center"][1] + self.number_radius
                    ],
                    "center": positions[i]
                })
        else:
            stop_angle = None if start_angle is None else ((((start_angle + 180) % 360) + 135) % 360)
            positions = self.calc_start_positions(stop_angle=stop_angle)
            positions.reverse()
            # print(dict_print(self.ovals, "PRE OVALS"))
            if not self.ovals:
                self.ovals.update({i: {"center": positions[i]} for i in range(10)})
            # print(dict_print(self.ovals, "POST OVALS"))
            print(f"{positions}")
            for i in range(10):
                self.ovals[i].update({"rect": [
                    self.ovals[i]["center"][0] - self.number_radius,
                    self.ovals[i]["center"][1] - self.number_radius,
                    self.ovals[i]["center"][0] + self.number_radius,
                    self.ovals[i]["center"][1] + self.number_radius
                    ],
                    "center": positions[i]
                })

    # def calc_ovals(self, start_angle=None, do_stop=False):
    def calc_ovals(self):
        # stop_angle = None if start_angle is None else ((((start_angle + 180) % 360) + 135) % 360)
        # positions = self.calc_start_positions(stop_angle=stop_angle)
        positions = self.calc_start_positions()
        positions.reverse()
        # print(dict_print(self.ovals, "PRE OVALS"))
        if not self.ovals:
            self.ovals.update({i: {"center": positions[i]} for i in range(10)})
        # print(dict_print(self.ovals, "POST OVALS"))
        print(f"{positions}")
        for i in range(10):
            self.ovals[i].update({"rect": [
                self.ovals[i]["center"][0] - self.number_radius,
                self.ovals[i]["center"][1] - self.number_radius,
                self.ovals[i]["center"][0] + self.number_radius,
                self.ovals[i]["center"][1] + self.number_radius
                ],
                "center": positions[i]
            })

    def update_ovals(self):
        for i in range(10):
            # print(f"{i=}, {self.ovals[i]=}")
            self.canvas_background.moveto(self.ovals[i]["oval"], *self.ovals[i]["rect"][:2])
            self.canvas_background.moveto(self.ovals[i]["text"], *self.ovals[i]["center"])

    # def calc_start_positions(self, stop_angle=None, number_radius=None):
    def calc_start_positions(self, stop_angle=None, drag_oval=0):
        # number_radius = number_radius if number_radius is not None else self.number_radius
        if stop_angle is None:
            stop_angle = self.stop_angle
            start_angle = int((((stop_angle + 180) % 360) - 135) % 360)
        else:
            start_angle = stop_angle
            print(f"{start_angle=}")
        start_angle = int(round(start_angle))
        slice = 25
        positions = []
        for i in range(start_angle, start_angle + ((10 - drag_oval) * slice), slice):
            positions.append(self.angle_on_circle(i, radius=round(self.rotary_radius * 0.75)))
        positions += [(0, 0) for i in range(10)]
        positions = positions[:10]
        return positions




    def angle_on_circle(self, angle, radius=None):
        radius = radius if radius is not None else self.rotary_radius
        return radius * math.cos(math.radians(angle)) + self.center_rotary[0], radius * math.sin(math.radians(angle)) + self.center_rotary[0]


    def mouse_motion(self, event):
        # self.center_rotary = event.x, event.y
        # self.rotary_rect = [
        #     self.center_rotary[0] - self.rotary_radius,
        #     self.center_rotary[1] - self.rotary_radius,
        #     self.center_rotary[0] + self.rotary_radius,
        #     self.center_rotary[1] + self.rotary_radius
        # ]
        # self.canvas_background.moveto(self.oval_rotary, *self.rotary_rect[:2])
        m_x, m_y = event.x, event.y

        angle = get_angle((m_x, m_y), np.array(self.center_rotary))
        self.number.set(angle)
        o_x, o_y = self.angle_on_circle(angle, 100)
        o_x -= 14/2
        o_y -= 14/2
        self.canvas_background.moveto(self.mouse_dot, o_x, o_y)

        for i in range(10):

            center = self.ovals[i]["center"]
            d = distance(center, (m_x, m_y))
            r = self.number_radius
            if self.gsm_is_dragging.state() and self.gsm_drag_number.state() == i:
                if d <= r:
                    print(f"DRAGGED #{i}")
                    self.spin_dial(m_x, m_y)
                    # print(f"{m_x=}, {m_y=}, isDragging: {self.gsm_is_dragging}, dragging: {self.gsm_drag_number}")
            elif not self.gsm_is_dragging.state():
                if d <= r:
                    print(f"NEW DRAG #{i}")
                    self.spin_dial(m_x, m_y)
                    self.gsm_is_dragging.__next__()
                    self.gsm_drag_number.set_state(i)
                    # print(f"{m_x=}, {m_y=}, isDragging: {self.gsm_is_dragging}, dragging: {self.gsm_drag_number}")
        # print(f"{m_x=}, {m_y=}, isDragging: {self.gsm_is_dragging}, dragging: {self.gsm_drag_number}")

    def mouse_button_release(self, event):
        self.gsm_is_dragging.set_state(False)


    def spin_dial(self, m_x, m_y):
        angle = get_angle((m_x, m_y), np.array(list(map(lambda x: int(x - (self.rotary_radius / 2)), self.center_rotary))))
        # # self.calc_ovals(start_angle=angle)
        # # self.calc_ovals(start_angle=angle, do_stop=True)
        # # print(dict_print(self.ovals, "Ovals B"))
        # # stop_angle = None if start_angle is None else ((((start_angle + 180) % 360) + 135) % 360)
        # # positions = self.calc_start_positions(stop_angle=stop_angle)
        # #########################################
        #
        # positions = self.calc_start_positions()
        # positions.reverse()
        # # print(dict_print(self.ovals, "PRE OVALS"))
        # if not self.ovals:
        #     self.ovals.update({i: {"center": positions[i]} for i in range(10)})
        # # print(dict_print(self.ovals, "POST OVALS"))
        # print(f"{positions}")
        # for i in range(10):
        #     self.ovals[i].update({"rect": [
        #         self.ovals[i]["center"][0] - self.number_radius,
        #         self.ovals[i]["center"][1] - self.number_radius,
        #         self.ovals[i]["center"][0] + self.number_radius,
        #         self.ovals[i]["center"][1] + self.number_radius
        #     ],
        #         "center": positions[i]
        #     })
        #
        #
        # #########################################

        drag_oval = self.gsm_drag_number.state()
        positions = self.calc_start_positions(stop_angle=angle, drag_oval=drag_oval)
        positions.reverse()
        # print(dict_print(self.ovals, "PRE OVALS"))
        if not self.ovals:
            self.ovals.update({i: {"center": positions[i]} for i in range(10)})
        # print(dict_print(self.ovals, "POST OVALS"))
        print(f"{positions}")
        for i in range(drag_oval, 10):
            self.ovals[i].update({"rect": [
                self.ovals[i]["center"][0] - self.number_radius,
                self.ovals[i]["center"][1] - self.number_radius,
                self.ovals[i]["center"][0] + self.number_radius,
                self.ovals[i]["center"][1] + self.number_radius
            ],
                "center": positions[i]
            })

        self.update_ovals()


if __name__ == "__main__":

    WIDTH, HEIGHT = 600, 500
    WINDOW = tkinter.Tk()
    WINDOW.geometry(f"{WIDTH}x{HEIGHT}")
    rs = RotarySpinner(WINDOW)
    rs.pack()
    WINDOW.mainloop()

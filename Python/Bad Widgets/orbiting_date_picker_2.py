import math
import tkinter
from tkinter import Frame
from colour_utility import *
from utility import distance


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
    return angle


class OrbitingDatePicker(Frame):

    def __init__(self, master, width=300, height=300, sun_width=50, earth_width=25, **kwargs):
        super().__init__(master, kwargs)

        self.tv_entry_date_result = tkinter.StringVar()
        self.entry_date_result = tkinter.Entry(self, textvariable=self.tv_entry_date_result)
        self.entry_date_result.grid(row=1, column=1)

        self.w_canvas_background = width
        self.h_canvas_background = height

        self.canvas_background = tkinter.Canvas(self.master, background=rgb_to_hex(BLACK), width=self.w_canvas_background, height=self.h_canvas_background)
        self.canvas_background.grid(row=1, column=2)#, rowspan=3, columnspan=3)

        self.sun_width = sun_width
        self.earth_width = earth_width
        oww = 40
        self.background_rect = [
            self.canvas_background.winfo_x(),
            self.canvas_background.winfo_y(),
            self.w_canvas_background,
            self.h_canvas_background
        ]
        self.centre = [
            self.background_rect[0] + (self.background_rect[2] / 2),
            self.background_rect[1] + (self.background_rect[3] / 2)
        ]
        self.orbit_rect = [
            oww,
            oww + 25,
            self.background_rect[0] + self.background_rect[2] - oww,
            self.background_rect[1] + self.background_rect[3] - (oww + 25)
        ]
        self.earth_rect = [
            25,  # self.canvas_background.winfo_x(),
            25,  # self.canvas_background.winfo_y(),
            25 + self.earth_width,  # self.w_canvas_background,
            25 + self.earth_width  # self.h_canvas_background
        ]
        self.oval_orbit = self.canvas_background.create_oval(
            *self.orbit_rect,
            # fill=rgb_to_hex(WHITE),
            outline=rgb_to_hex(WHITE),
            width=3
        )
        self.oval_sun = self.canvas_background.create_oval(
            self.background_rect[0] + ((self.background_rect[2] - self.sun_width) / 2),
            self.background_rect[1] + ((self.background_rect[3] - self.sun_width) / 2),
            self.background_rect[0] + ((self.background_rect[2] + self.sun_width) / 2),
            self.background_rect[1] + ((self.background_rect[3] + self.sun_width) / 2),
            fill=rgb_to_hex(YELLOW_2)
        )
        self.oval_earth = self.canvas_background.create_oval(
            *self.earth_rect,
            fill=rgb_to_hex(DODGERBLUE_3)
        )
        print(f"earth: {self.oval_earth}")

        self.canvas_background.bind("<B1-Motion>", self.mouse_motion)

    def update_date(self):
        pos = self.centre_of_earth()
        xs = self.orbit_rect
        new_date = f"{pos=}"
        self.tv_entry_date_result.set(new_date)

    def centre_of_earth(self):
        rect = self.earth_rect
        return rect[0] + ((rect[2] - rect[0]) / 2), rect[1] + ((rect[3] - rect[1]) / 2)

    def mouse_motion(self, event):
        # print(f"Mouse Motion: {event}\n{dir(event)}")
        mouse_x, mouse_y = event.x, event.y
        self.earth_rect = [
            mouse_x - (self.earth_width / 2),
            mouse_y - (self.earth_width / 2),
            mouse_x + (self.earth_width / 2),
            mouse_y + (self.earth_width / 2)
        ]
        angle = get_angle((mouse_x, mouse_y), np.array(self.centre))
        a = (self.background_rect[3] - self.background_rect[1]) / 3
        b = (self.background_rect[2] - self.background_rect[0]) / 3

        #############
        # oval_x, oval_y = (
        #     ((a ** 2 * b ** 2 * self.centre[0] ** 2) / ((b ** 2 * self.centre[0] ** 2) + (a ** 2 * self.centre[1] ** 2))),
        #     ((a ** 2 * b ** 2 * self.centre[1] ** 2) / ((b ** 2 * self.centre[0] ** 2) + (a ** 2 * self.centre[1] ** 2)))
        # )

        ############
        # if 0 <= angle < 90 or 270 < angle <= 360:
        #     oval_x, oval_y = (
        #         ((a*b) / (math.sqrt(b**2 + (a**2 * math.tan(angle)**2)))),
        #         ((a*b * math.tan(angle)) / (math.sqrt(b**2 + (a**2 * math.tan(angle)**2))))
        #     )
        # else:
        #     oval_x, oval_y = (
        #         -((a*b) / (math.sqrt(b**2 + (a**2 * math.tan(angle)**2)))),
        #         -((a*b * math.tan(angle)) / (math.sqrt(b**2 + (a**2 * math.tan(angle)**2))))
        #     )
        # oval_x += self.centre[0]
        # oval_y += self.centre[1]

        # https://math.stackexchange.com/questions/22064/calculating-a-point-that-lies-on-an-ellipse-given-an-angle
        ############
        oval_x, oval_y = (
            self.centre[0] + ((a * b * math.sin(angle)) / math.sqrt(((b * math.cos(angle))**2) + ((a * math.sin(angle))**2))),
            self.centre[1] + ((a * b * math.cos(angle)) / math.sqrt(((b * math.cos(angle))**2) + ((a * math.sin(angle))**2)))
        )


        self.earth_rect = [
            oval_x - (self.earth_width / 2),
            oval_y - (self.earth_width / 2),
            oval_x + (self.earth_width / 2),
            oval_y + (self.earth_width / 2)
        ]
        print(f"Oval: x={oval_x:.2f}, y={oval_y:.2f}")
        self.canvas_background.coords(self.oval_earth, *self.earth_rect)

        self.update_date()


if __name__ == "__main__":

    # Usage:
    # compute_angle((0, 15), (0, 0)) => 0 degrees
    # compute_angle((15, 0), (0, 0)) => 90 degrees
    # compute_angle(0, 15, 0, 0) => 0 degrees
    # compute_angle(15, 0, 0, 0) => 90 degrees
    def compute_angle(point, centre, cx=None, cy=None):
        case_a = ((isinstance(point, list) or isinstance(point, tuple)) and len(point) == 2) and ((isinstance(centre, list) or isinstance(centre, tuple)) and len(centre) == 2)
        case_b = all([isinstance(x, int) or isinstance(x, float) for x in [point, centre, cx, cy]])
        if not case_a and not case_b:
            raise ValueError(f"Error cannot compute the angle with the given params.\npoint='{point}', centre='{centre}', cx='{cx}', and cy='{cy}' do not match usage.")
        p1, p2 = point if case_a else (point, centre)
        c1, c2 = centre if case_a else (cx, cy)
        p1, p2 = float(p1), float(p2)
        c1, c2 = float(c1), float(c2)
        cx = max(abs(p1), abs(c1))
        c1 = cx * (-1 if abs(p1) == cx and p1 < 0 or abs(c1) == cx and c1 < 0 else 1)
        print(f"p1={p1}, p2={p2}, c1={c1}, c2={c2}, point={point}, centre={centre}, cA={case_a}, cB={case_b}")
        magnitude = distance((p1, p2), (c1, c2))
        theta = math.degrees(math.atan(abs(c2 - p2) / (1 if abs(c1 - p1) == 0 else abs(c1 - p1))))
        print(f"abs(c2 - p2): {abs(c2 - p2)}\n(1 if abs(c1 - p1) == 0 else abs(c1 - p1)): {(1 if abs(c1 - p1) == 0 else abs(c1 - p1))}\nabs(c2 - p2) / (1 if abs(c1 - p1) == 0 else abs(c1 - p1)): {abs(c2 - p2) / (1 if abs(c1 - p1) == 0 else abs(c1 - p1))}\nmath.atan(abs(c2 - p2) / (1 if abs(c1 - p1) == 0 else abs(c1 - p1))): {math.atan(abs(c2 - p2) / (1 if abs(c1 - p1) == 0 else abs(c1 - p1)))}")
        print(f"{magnitude=}, {theta=}")
        comp_x = magnitude * math.cos(theta)
        comp_y = magnitude * math.sin(theta)
        return theta


    centre = 0, 0, 0
    points = [
        p1 := (15, 0, 0),
        p9 := (14.142, 5, 30),
        p5 := (5, 14.142, 70),
        p2 := (0, 15, 90),
        p6 := (-5, 14.142, 105),
        p10 := (-14.142, 5, 160),
        p3 := (-15, 0, 180),
        p12 := (-14.142, -5, 205),
        p8 := (-5, -14.142, 255),
        p4 := (0, -15, 270),
        p7 := (5, -14.142, 305),
        p11 := (14.142, -5, 340),
        centre
    ]
    for pt in points:
        # print(f"pt: {pt} angle: {compute_angle(pt, centre)}\n")
        angle = ("%.2f" % get_angle(pt[:2], np.array(centre[:2]))).ljust(20)
        answer = pt[2]
        pts = str(pt)
        pts = pts.ljust(20)
        print(f"pt: {pts}{angle=}\t{answer=:.2f}")


    WIDTH, HEIGHT = 400, 400
    WINDOW = tkinter.Tk()
    WINDOW.geometry(f"{WIDTH}x{HEIGHT}")
    ss = OrbitingDatePicker(WINDOW)
    ss.grid()
    WINDOW.mainloop()


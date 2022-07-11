import datetime
import math
import tkinter
from tkinter import Frame
from colour_utility import *
from utility import distance, Rect2


import numpy as np


DEFAULT_SEASONS = {
    "Spring": {
        "test": lambda date: datetime.datetime(date.year, 3, 20) <= date < datetime.datetime(date.year, 6, 21),
        "colour": WILDERNESS_MINT,
        "font_colour": WHITE
    },
    "Summer": {
        "test": lambda date: datetime.datetime(date.year, 6, 21) <= date < datetime.datetime(date.year, 9, 22),
        "colour": GOLD_1__GOLD_,
        "font_colour": BLACK
    },
    "Fall": {
        "test": lambda date: datetime.datetime(date.year, 9, 22) <= date < datetime.datetime(date.year, 12, 21),
        "colour": DARKORANGE_2,
        "font_colour": WHITE
    },
    "Winter": {
        "test": lambda date: datetime.datetime(date.year, 12, 21) <= date <= datetime.datetime(date.year, 12, 31) or datetime.datetime(date.year, 1, 1) <= date < datetime.datetime(date.year, 3, 20),
        "colour": LIGHTSKYBLUE,
        "font_colour": BLACK
    }
}


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
    return 360 - angle


class OrbitingDatePicker(Frame):

    class TEvent:

        def __init__(self, orbit_rect):
            self.x1, self.y1, self.x2, self.y2 = orbit_rect
            self.rect = Rect2(self.x1, self.y1, self.x2 - self.x1, self.y2 - self.y1)
            self._event_x, self._event_y = self.rect.center
            self.x, self.y = None, None

        def top_left(self):
            self.event_x, self.event_y = self.rect.top_left
            return self

        def center_top(self):
            self.event_x, self.event_y = self.rect.center_top
            return self

        def top_right(self):
            self.event_x, self.event_y = self.rect.top_right
            return self

        def center_left(self):
            self.event_x, self.event_y = self.rect.center_left
            return self

        def center(self):
            self.event_x, self.event_y = self.rect.center
            return self

        def center_right(self):
            self.event_x, self.event_y = self.rect.center_right
            return self

        def bottom_left(self):
            self.event_x, self.event_y = self.rect.bottom_left
            return self

        def center_bottom(self):
            self.event_x, self.event_y = self.rect.center_bottom
            return self

        def bottom_right(self):
            self.event_x, self.event_y = self.rect.bottom_right
            return self

        def set_event_x(self, event_x_in):
            self._event_x = event_x_in
            self.x = self.event_x

        def set_event_y(self, event_y_in):
            self._event_y = event_y_in
            self.y = self.event_y

        def get_event_x(self):
            return self._event_x

        def get_event_y(self):
            return self._event_y

        def del_event_x(self):
            del self._event_x

        def del_event_y(self):
            del self._event_y

        event_x = property(get_event_x, set_event_x, del_event_x)
        event_y = property(get_event_y, set_event_y, del_event_y)

    def __init__(self, master, width=300, height=300, sun_width=50, earth_width=25, start_date=None, start_year=None, start_month=None, start_day=None, seasons=None, **kwargs):
        super().__init__(master, kwargs)

        self.today = datetime.datetime.now()
        if start_date is None:
            if all([x is None for x in [start_year, start_month, start_day]]):
                start_date = datetime.datetime.now()
            else:
                if start_year is None:
                    start_year = self.today.year
                if start_month is None:
                    start_month = self.today.month
                if start_day is None:
                    start_day = self.today.day
                start_date = datetime.datetime.strptime(f"{start_year}-{start_month}-{start_day}", "%Y-%m-%d")
        elif not isinstance(start_date, datetime.datetime):
            raise TypeError("Error param 'start_date' must either be None or a datetime.datetime object.")

        self.seasons = seasons if seasons is not None else DEFAULT_SEASONS

        self.tv_entry_date_result_top = tkinter.StringVar()
        self.tv_entry_date_result_bottom = tkinter.StringVar()
        self.entry_date_result = tkinter.Entry(self, textvariable=self.tv_entry_date_result_top, width=100)
        self.entry_date_result.grid(row=1, column=1, columnspan=3)
        self.entry_date_result_data = tkinter.Entry(self, textvariable=self.tv_entry_date_result_bottom, width=100)
        self.entry_date_result_data.grid(row=2, column=1, columnspan=3)

        self.w_canvas_background = width
        self.h_canvas_background = height

        self.canvas_background = tkinter.Canvas(self, background=rgb_to_hex(BLACK), width=self.w_canvas_background, height=self.h_canvas_background)
        self.canvas_background.grid(row=3, column=1, rowspan=3, columnspan=3)

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
        self.sun_rect = [
            self.centre[0] - (self.sun_width / 2),
            self.centre[1] - (self.sun_width / 2),
            self.centre[0] + (self.sun_width / 2),
            self.centre[1] + (self.sun_width / 2)
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
            *self.sun_rect,
            fill=rgb_to_hex(YELLOW_2)
        )
        self.oval_earth = self.canvas_background.create_oval(
            *self.earth_rect,
            fill=rgb_to_hex(DODGERBLUE_3)
        )

        self.start_date = start_date
        self.date = start_date
        self.degrees_per_day = self.calc_deg_per_day()

        # self.SQUARE = self.canvas_background.create_rectangle(*self.earth_rect, fill=rgb_to_hex(OLIVEDRAB_2))
        self.text_year_label = self.canvas_background.create_text(*self.centre, text=f"{self.date.year}", font=("Arial", 12, "bold"))
        self.text_month_label = self.canvas_background.create_text(*self.centre_of_earth(), text=f"{self.date.strftime('%b')}", fill=rgb_to_hex(WHITE))
        print(f"earth: {self.oval_earth}, {self.date=:%Y-%m-%d}")
        print(f"earth: {self.oval_earth}, {self.date=:%Y-%m-%d}")

        self.canvas_background.bind("<B1-Motion>", self.mouse_motion)
        # self.set_earth_pos(0, "STARTING AT 0")
        self.t_event = OrbitingDatePicker.TEvent(self.orbit_rect).center_right()
        self.mouse_motion(self.t_event)


    def calc_date(self, angle=None):
        angle = angle if angle is not None else self.get_angle_to_earth()


    def calc_days_per_year(self, year_in=None):
        year_in = year_in if year_in is not None else self.date.year
        return (datetime.datetime(year_in, 12, 31) - datetime.datetime(year_in, 1, 1)).days

    def calc_deg_per_day(self, year_in=None):
        return 359 / self.calc_days_per_year(year_in)

    def angle_to_date(self, angle=None, year_in=None):
        deg_per_day = year_in if year_in is not None else self.calc_deg_per_day()
        angle = angle if angle is not None else self.get_angle_to_earth()
        days = round(angle / deg_per_day)
        return datetime.datetime(self.date.year, 1, 1) + datetime.timedelta(days=days)

    def date_to_angle(self, date_in=None):
        # deg_per_day = year_in if year_in is not None else self.calc_deg_per_day()
        # angle = angle if angle is not None else self.get_angle_to_earth()
        date_in = date_in if date_in is not None else self.date
        deg_per_day = self.calc_deg_per_day(year_in=date_in.year)
        # days = self.calc_days_per_year(year_in=date_in.year)
        p = (date_in - datetime.datetime(date_in.year, 1, 1)).days
        return p * deg_per_day


    def get_season(self, date_in=None):
        date_in = date_in if date_in is not None else self.date
        for season, data in self.seasons.items():
            test = data["test"]
            # colour = data["colour"]
            if test(date_in):
                return season
        raise KeyError(f"Error, param date_in '{date_in}' does not have a suitable season associated with it.")

    def update_date(self, *data):
        # new_date = self.today
        # new_date = self.calc_date()
        new_date = self.angle_to_date()
        self.date = new_date, data

    def centre_of_earth(self):
        rect = self.earth_rect
        return rect[0] + ((rect[2] - rect[0]) / 2), rect[1] + ((rect[3] - rect[1]) / 2)

    def get_angle_to_earth(self, mouse=None):
        pos = self.centre_of_earth() if mouse is None else mouse
        return get_angle(pos, np.array(self.centre))

    def calc_a_b(self):
        return (
            (self.orbit_rect[3] - self.orbit_rect[1]) / 2,
            (self.orbit_rect[2] - self.orbit_rect[0]) / 2
        )

    def calc_oval_x_y(self, a=None, b=None, angle=None):
        a, b = self.calc_a_b() if any([x is None for x in [a, b]]) else (a, b)
        angle = math.radians(90 + (self.get_angle_to_earth() if angle is None else angle))
        denom = math.sqrt(((b * math.cos(angle))**2) + ((a * math.sin(angle))**2))
        return (
            self.centre[0] + ((a * b * math.sin(angle)) / denom),
            self.centre[1] + ((a * b * math.cos(angle)) / denom)
        )

    # def mouse_motion(self, event):
    #     # print(f"Mouse Motion: {event}\n{dir(event)}")
    #     mouse_x, mouse_y = event.x, event.y
    #     self.earth_rect = [
    #         mouse_x - (self.earth_width / 2),
    #         mouse_y - (self.earth_width / 2),
    #         mouse_x + (self.earth_width / 2),
    #         mouse_y + (self.earth_width / 2)
    #     ]
    #     angle = get_angle((mouse_x, mouse_y), np.array(self.centre))
    #     a = (self.background_rect[3] - self.background_rect[1]) / 3
    #     b = (self.background_rect[2] - self.background_rect[0]) / 3
    #
    #     #############
    #     # oval_x, oval_y = (
    #     #     ((a ** 2 * b ** 2 * self.centre[0] ** 2) / ((b ** 2 * self.centre[0] ** 2) + (a ** 2 * self.centre[1] ** 2))),
    #     #     ((a ** 2 * b ** 2 * self.centre[1] ** 2) / ((b ** 2 * self.centre[0] ** 2) + (a ** 2 * self.centre[1] ** 2)))
    #     # )
    #
    #     ############
    #     # if 0 <= angle < 90 or 270 < angle <= 360:
    #     #     oval_x, oval_y = (
    #     #         ((a*b) / (math.sqrt(b**2 + (a**2 * math.tan(angle)**2)))),
    #     #         ((a*b * math.tan(angle)) / (math.sqrt(b**2 + (a**2 * math.tan(angle)**2))))
    #     #     )
    #     # else:
    #     #     oval_x, oval_y = (
    #     #         -((a*b) / (math.sqrt(b**2 + (a**2 * math.tan(angle)**2)))),
    #     #         -((a*b * math.tan(angle)) / (math.sqrt(b**2 + (a**2 * math.tan(angle)**2))))
    #     #     )
    #     # oval_x += self.centre[0]
    #     # oval_y += self.centre[1]
    #
    #     # https://math.stackexchange.com/questions/22064/calculating-a-point-that-lies-on-an-ellipse-given-an-angle
    #     ############
    #     oval_x, oval_y = (
    #         self.centre[0] + ((a * b * math.sin(angle)) / math.sqrt(((b * math.cos(angle))**2) + ((a * math.sin(angle))**2))),
    #         self.centre[1] + ((a * b * math.cos(angle)) / math.sqrt(((b * math.cos(angle))**2) + ((a * math.sin(angle))**2)))
    #     )
    #
    #
    #     self.earth_rect = [
    #         oval_x - (self.earth_width / 2),
    #         oval_y - (self.earth_width / 2),
    #         oval_x + (self.earth_width / 2),
    #         oval_y + (self.earth_width / 2)
    #     ]
    #     print(f"Oval: x={oval_x:.2f}, y={oval_y:.2f}")
    #     self.canvas_background.coords(self.oval_earth, *self.earth_rect)
    #
    #     self.update_date()

    def set_earth_pos(self, pos, *data):
        if not isinstance(pos, tuple) and not isinstance(pos, list) and (isinstance(pos, int) or isinstance(pos, float)):
            pos = self.calc_oval_x_y(angle=pos)
            # print(f"{pos=}")
        if isinstance(pos, datetime.datetime):
            pos = self.calc_oval_x_y(angle=self.date_to_angle(date_in=pos))


        # elif isinstance(pos, datetime.datetime):
        #     pos = self.calc_oval_x_y(angle=self.date_to_angle(date_in=pos))
        # elif ((isinstance(pos, tuple) or isinstance(pos, list)) and len(pos) == 2) and isinstance(pos[0], datetime.datetime):
        #     pos = self.calc_oval_x_y(angle=self.date_to_angle(date_in=pos[0])), pos[1]

        pos_x, pos_y = pos
        self.earth_rect = [
            pos_x - (self.earth_width / 2),
            pos_y - (self.earth_width / 2),
            pos_x + (self.earth_width / 2),
            pos_y + (self.earth_width / 2)
        ]
        # print(f"-> {pos=}, {data=}, {self.date=:%Y-%m-%d}")
        self.update_date(pos, data)
        # print(f"<- {pos=}, {data=}, {self.date=:%Y-%m-%d}")
        season = self.get_season()
        # self.canvas_background.coords(self.SQUARE, *self.earth_rect)
        # print(f"Pos: {self.date=:%Y-%m-%d} x={pos_x:.2f}, y={pos_y:.2f}, {season=}")
        self.canvas_background.coords(self.oval_earth, *self.earth_rect)
        self.canvas_background.itemconfig(self.oval_earth, fill=rgb_to_hex(self.seasons[season]["colour"]))
        self.canvas_background.itemconfig(self.text_month_label, text=self.date.strftime('%b'), font=("Arial", 10, "bold"), fill=rgb_to_hex(self.seasons[season]["font_colour"]))
        self.canvas_background.itemconfig(self.text_year_label, text=self.date.strftime('%Y'))
        text_x, text_y = self.earth_rect[:2]
        # text_x += self.earth_width / 4
        text_y += self.earth_width / 4
        self.canvas_background.moveto(self.text_month_label, text_x, text_y)

    def mouse_motion(self, event):
        # print(f"Mouse Motion: {event}\n{dir(event)}")
        mouse_x, mouse_y = event.x, event.y
        mouse = mouse_x, mouse_y
        old_angle = self.get_angle_to_earth()
        angle = self.get_angle_to_earth(mouse)
        if (0 <= angle < 60) and (300 < old_angle <= 360):
            # winter -> spring - inc year
            self.date = datetime.datetime(self.date.year + 1, self.date.month, self.date.day)
            # print("\t\tINC YEAR")
        elif (0 <= old_angle < 60) and (300 < angle <= 360):
            # spring -> winter - dec year
            self.date = datetime.datetime(self.date.year - 1, self.date.month, self.date.day)
            # print("\t\tDEC YEAR")
        self.set_earth_pos(angle, f"{mouse=}, TE:{angle=}")


        # # print(f"Mouse Motion: {event}\n{dir(event)}")
        # mouse_x, mouse_y = event.x, event.y
        # mouse = mouse_x, mouse_y
        # # self.earth_rect = [
        # #     mouse_x - (self.earth_width / 2),
        # #     mouse_y - (self.earth_width / 2),
        # #     mouse_x + (self.earth_width / 2),
        # #     mouse_y + (self.earth_width / 2)
        # # ]
        # angle = self.get_angle_to_earth(mouse)
        #
        # a = (self.background_rect[3] - self.background_rect[1]) / 3
        # b = (self.background_rect[2] - self.background_rect[0]) / 3
        #
        # # a, b = self.calc_a_b()
        # oval_x, oval_y = self.calc_oval_x_y(angle=angle)
        # self.set_earth_pos((oval_x, oval_y), f"{mouse=}, {angle=}")
        # # self.earth_rect = [
        # #     oval_x - (self.earth_width / 2),
        # #     oval_y - (self.earth_width / 2),
        # #     oval_x + (self.earth_width / 2),
        # #     oval_y + (self.earth_width / 2)
        # # ]
        # # print(f"Oval: x={oval_x:.2f}, y={oval_y:.2f}")
        # # self.canvas_background.coords(self.oval_earth, *self.earth_rect)
        # #
        # # self.update_date()

    def animate(self):
        for i in range(100):
            self.after(i * 10, self.add_day)

    def add_day(self, days=1):
        self.date += datetime.timedelta(days=days)

    def get_date(self):
        return self._date

    def set_date(self, date_in):
        rest = None
        # print(f"\t\t\tDATE_IN: {date_in}")
        if isinstance(date_in, tuple) or isinstance(date_in, list):
            date_in, *rest = date_in
        self._date = date_in
        angle = self.get_angle_to_earth()
        pos = self.centre_of_earth()
        xs = self.orbit_rect
        pos_s = ["%.2f" % p for p in pos]
        new_date = f"=<{rest=}>"
        self.tv_entry_date_result_top.set(self.date.strftime("%Y-%m-%d") + f" - {angle=:.3f}, {pos_s=}" + f"calc_date={self.angle_to_date()}")
        self.tv_entry_date_result_bottom.set(new_date)

    def del_date(self):
        del self._date

    date = property(get_date, set_date, del_date)


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


    WIDTH, HEIGHT = 600, 400
    WINDOW = tkinter.Tk()
    WINDOW.geometry(f"{WIDTH}x{HEIGHT}")
    ss = OrbitingDatePicker(WINDOW)
    ss.grid()
    btn = tkinter.Button(WINDOW, text="animate", command=ss.animate)
    btn.grid()
    WINDOW.mainloop()


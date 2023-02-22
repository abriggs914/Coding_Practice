import datetime
import math
import tkinter
from tkinter import Frame
from tkcalendar import DateEntry
from colour_utility import *
from utility import Rect2
import numpy as np


#######################################################################################################################
#######################################################################################################################
#######################################################################################################################

VERSION = \
    """	
        Class to add an Orbiting Date Picker Widget in place of a traditional date picker. Works with tkcalendar.DateEntry and datetime.datetime objects.
        Version..............1.03
        Date...........2023-02-16
        Author.......Avery Briggs
    """


def VERSION_NUMBER():
    return float(VERSION.split("\n")[2].split(".")[-2] + "." + VERSION.split("\n")[2].split(".")[-1])


def VERSION_DATE():
    return VERSION.split("\n")[3].split(".")[-1]


def VERSION_AUTHOR():
    return VERSION.split("\n")[4].split(".")[-1]

#######################################################################################################################
#######################################################################################################################
#######################################################################################################################


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
        must_place = False
        if start_date is None:
            if all([x is None for x in [start_year, start_month, start_day]]):
                start_date = datetime.datetime.now()
                must_place = True
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
        else:
            must_place = True

        self.seasons = seasons if seasons is not None else DEFAULT_SEASONS

        self.w_canvas_background = width
        self.h_canvas_background = height

        self.canvas_background = tkinter.Canvas(self, background=rgb_to_hex(BLACK), width=self.w_canvas_background, height=self.h_canvas_background)

        # self.tv_showing_orbiter = tkinter.StringVar(value="Show Orbiter")
        # self.showing_orbiter = BooleanGSM(name="showing_orbiter", t_first=False)
        # self.showing_orbiter.bind_callback(self.switch_showing_orbiter)
        self.iv_showing_orbiter = tkinter.IntVar()
        self.checkbox_showing_orbiter = tkinter.Checkbutton(self, text="Show Orbiter", command=self.switch_showing_orbiter, onvalue=1, offvalue=0, variable=self.iv_showing_orbiter)
        self.checkbox_showing_orbiter.grid(row=4, column=3)

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
        self._date = start_date
        self.degrees_per_day = self.calc_deg_per_day()

        self.dateentry_entry = DateEntry(self, year=self.date.year, month=self.date.month, day=self.date.day, font=("Arial", 12), cursor="hand1")
        self.dateentry_entry.grid(row=4, column=1, columnspan=2)
        self.dateentry_entry.bind("<<DateEntrySelected>>", self.dateentry_change)

        # self.SQUARE = self.canvas_background.create_rectangle(*self.earth_rect, fill=rgb_to_hex(OLIVEDRAB_2))
        self.text_year_label = self.canvas_background.create_text(*self.centre, text=f"{self.date.year}", font=("Arial", 12, "bold"))
        self.text_month_label = self.canvas_background.create_text(*self.centre_of_earth(), text=f"{self.date.strftime('%b')}", fill=rgb_to_hex(WHITE))

        self.canvas_background.bind("<B1-Motion>", self.mouse_motion)
        self.config(highlightbackground=rgb_to_hex(DODGERBLUE_4), highlightthickness=2)

        # possible starting calls
        # self.set_earth_pos(0, "STARTING AT 0")
        # self.set_earth_pos(359, "STARTING AT 359")
        # self.set_earth_pos(datetime.datetime(2022,1,1), "STARTING AT Jan 1st 2022")
        # self.set_earth_pos(datetime.datetime(2022,8,3), "STARTING AT Aug 3rd 2022")
        # self.t_event = OrbitingDatePicker.TEvent(self.orbit_rect).center_right()
        # self.mouse_motion(self.t_event)
        if must_place:
            self.set_earth_pos(self.date)

    def switch_showing_orbiter(self):
        if self.iv_showing_orbiter.get() == 1:
            print("SHOWING")
            self.canvas_background.grid(row=1, column=1, rowspan=3, columnspan=3)
            # self.tv_showing_orbiter.set("Hide Orbiter")
            # self.checkbox_showing_orbiter.config(text="Hide Orbiter")
        else:
            print("HIDING")
            self.canvas_background.grid_forget()
            # self.tv_showing_orbiter.set("Show Orbiter")
            # self.checkbox_showing_orbiter.config(text="Show Orbiter")

    def dateentry_change(self, *event):
        self.set_earth_pos(self.dateentry_entry.get_date(), from_date_entry=True)

    def calc_days_per_year(self, year_in=None):
        year_in = year_in if year_in is not None else self.date.year
        return (datetime.datetime(year_in, 12, 31) - datetime.datetime(year_in, 1, 1)).days

    def calc_deg_per_day(self, year_in=None):
        return 359 / self.calc_days_per_year(year_in)

    def angle_to_date(self, angle=None, year_in=None):
        deg_per_day = self.calc_deg_per_day(year_in=year_in)
        year_in = year_in if year_in is not None else self.date.year
        angle = angle if angle is not None else self.get_angle_to_earth()
        days = round((359 - angle) / deg_per_day)
        return datetime.datetime(year_in, 1, 1) + datetime.timedelta(days=days)

    def date_to_angle(self, date_in=None):
        date_in = date_in if date_in is not None else self.date
        if isinstance(date_in, datetime.date):
            date_in = datetime.datetime(date_in.year, date_in.month, date_in.day)
        deg_per_day = self.calc_deg_per_day(year_in=date_in.year)
        p = self.calc_days_per_year() - (date_in - datetime.datetime(date_in.year, 1, 1)).days
        return p * deg_per_day

    def get_season(self, date_in=None):
        date_in = date_in if date_in is not None else self.date
        for season, data in self.seasons.items():
            test = data["test"]
            if test(date_in):
                return season
        raise KeyError(f"Error, param date_in '{date_in}' does not have a suitable season associated with it.")

    def update_date(self, *data, year=None):
        # new_date = self.today
        # new_date = self.calc_date()
        new_date = self.angle_to_date(year_in=year)
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

    def set_earth_pos(self, pos, *data, from_date_entry=False):
        year = self.date.year
        if not isinstance(pos, tuple) and not isinstance(pos, list) and (isinstance(pos, int) or isinstance(pos, float)):
            pos = self.calc_oval_x_y(angle=pos)
            # print(f"{pos=}")
        elif isinstance(pos, datetime.datetime) or isinstance(pos, datetime.date):
            year = pos.year
            pos = self.calc_oval_x_y(angle=self.date_to_angle(date_in=pos))
        else:
            raise ValueError(f"INVALID pos='{pos}'")

        pos_x, pos_y = pos
        self.earth_rect = [
            pos_x - (self.earth_width / 2),
            pos_y - (self.earth_width / 2),
            pos_x + (self.earth_width / 2),
            pos_y + (self.earth_width / 2)
        ]
        # print(f"-> {pos=}, {data=}, {self.date=:%Y-%m-%d}")
        self.update_date(pos, data, year=year)
        if not from_date_entry:
            self.dateentry_entry.set_date(datetime.date(self.date.year, self.date.month, self.date.day))
        # print(f"<- {pos=}, {data=}, {self.date=:%Y-%m-%d}")
        season = self.get_season()
        self.canvas_background.coords(self.oval_earth, *self.earth_rect)
        self.canvas_background.itemconfig(self.oval_earth, fill=rgb_to_hex(self.seasons[season]["colour"]))
        self.canvas_background.itemconfig(self.text_month_label, text=self.date.strftime('%b'), font=("Arial", 10, "bold"), fill=rgb_to_hex(self.seasons[season]["font_colour"]))
        self.canvas_background.itemconfig(self.text_year_label, text=self.date.strftime('%Y'))
        text_x, text_y = self.earth_rect[:2]
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
            self.date = datetime.datetime(self.date.year - 1, self.date.month, self.date.day)
        elif (0 <= old_angle < 60) and (300 < angle <= 360):
            # spring -> winter - dec year
            self.date = datetime.datetime(self.date.year + 1, self.date.month, self.date.day)
        self.set_earth_pos(angle, f"{mouse=}, TE:{angle=}")

    def animate(self, n_days=100, fps=10):
        for i in range(n_days):
            self.after(i * fps, self.set_earth_pos, self.get_angle_to_earth() + i)

    def add_day(self, days=1):
        self.date += datetime.timedelta(days=days)

    def get_date(self):
        return self._date

    def set_date(self, date_in):
        # print(f"\t\t\tDATE_IN: {date_in}")
        if isinstance(date_in, tuple) or isinstance(date_in, list):
            date_in, *rest = date_in
        self._date = date_in

    def del_date(self):
        del self._date

    date = property(get_date, set_date, del_date)


if __name__ == "__main__":

    WIDTH, HEIGHT = 600, 400
    WINDOW = tkinter.Tk()
    WINDOW.geometry(f"{WIDTH}x{HEIGHT}")
    # ss = OrbitingDatePicker(WINDOW)
    ss = OrbitingDatePicker(WINDOW, start_date=datetime.datetime(2022, 6, 6))
    ss.pack()
    WINDOW.mainloop()


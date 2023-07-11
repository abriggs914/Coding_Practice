import calendar
import tkinter

from datetime_utility import datetime2
from tkinter_utility import *
from utility import dict_print


class CountDownTimer(tkinter.Frame):

    def __init__(
            self,
            master,
            year_in=0,
            month_in=0,
            day_in=0,
            hour_in=0,
            min_in=0,
            sec_in=0,
            leave_as_set=True,
            count_mode: Literal["up", "down", "date"]="down",
            auto_grid=True):
        super().__init__(master)

        self.init_time = datetime.datetime.now()
        self.MAX_TIME = 1e100  # seconds

        self.auto_grid = auto_grid
        self.count_mode = count_mode
        self.leave_as_set = leave_as_set

        year_in, month_in, day_in, hour_in, min_in, sec_in = self.validate_input(year_in, month_in, day_in, hour_in, min_in, sec_in)

        self.year_in = year_in
        self.month_in = month_in
        self.day_in = day_in
        self.hour_in = hour_in
        self.min_in = min_in
        self.sec_in = sec_in

        self.frame_countdowns = tkinter.Frame(self)

        self.tv_lbl_hour, \
            self.lbl_hour \
            = label_factory(
                self.frame_countdowns,
                tv_label="00"
            )

        self.tv_lbl_hm_space, \
            self.lbl_hm_space \
            = label_factory(
                self.frame_countdowns,
                tv_label=":"
            )

        self.tv_lbl_min, \
            self.lbl_min \
            = label_factory(
                self.frame_countdowns,
                tv_label="00"
            )

        self.tv_lbl_ms_space, \
            self.lbl_ms_space \
            = label_factory(
                self.frame_countdowns,
                tv_label=":"
            )

        self.tv_lbl_sec, \
            self.lbl_sec \
            = label_factory(
                self.frame_countdowns,
                tv_label="00"
            )

        r, c, rs, cs, ix, iy, x, y, s = self.grid_keys()
        self.grid_args = {

            ".": {},

            "frame_countdowns": {r: 0, c: 0},

            "lbl_hour": {r: 0, c: 0},
            "lbl_hm_space": {r: 0, c: 1},
            "lbl_min": {r: 0, c: 2},
            "lbl_ms_space": {r: 0, c: 3},
            "lbl_sec": {r: 0, c: 4}
        }

        if self.auto_grid:
            self.grid_widgets()

        self.c_time = datetime.datetime.now()
        self.running = tkinter.BooleanVar(self, value=False)

    def grid_widgets(self):
        for k, args in self.grid_args.items():
            if k == ".":
                self.grid(**args)
            else:
                eval(f"self.{k}.grid(**{args})")

    def grid_keys(self):
        return "row", "column", "rowspan", "columnspan", "ipadx", "ipady", "padx", "pady", "sticky"

    def validate_input(self, year_in, month_in, day_in, hour_in, min_in, sec_in):

        spm = 60
        sph = 60 * spm
        spd = 24 * sph
        spy = 365 * spd

        if not isinstance(year_in, int):
            raise TypeError("Error, param 'year_in' must be an int.")
        if not isinstance(month_in, int):
            raise TypeError("Error, param 'month_in' must be an int.")
        if not isinstance(day_in, int):
            raise TypeError("Error, param 'day_in' must be an int.")
        if not isinstance(hour_in, int):
            raise TypeError("Error, param 'hour_in' must be an int.")
        if not isinstance(min_in, int):
            raise TypeError("Error, param 'min_in' must be an int.")
        if not isinstance(sec_in, int):
            raise TypeError("Error, param 'sec_in' must be an int.")

        if year_in < 0:
            raise ValueError("Error, param 'year_in' cannot be negative.")
        if month_in < 0:
            raise ValueError("Error, param 'month_in' cannot be negative.")
        if day_in < 0:
            raise ValueError("Error, param 'day_in' cannot be negative.")
        if hour_in < 0:
            raise ValueError("Error, param 'hour_in' cannot be negative.")
        if min_in < 0:
            raise ValueError("Error, param 'min_in' cannot be negative.")
        if sec_in < 0:
            raise ValueError("Error, param 'sec_in' cannot be negative.")

        t_used = 0
        cont_year = 0
        cont_month = 0
        cont_day = 0
        cont_hour = 0
        cont_min = 0
        cont_sec = 0
        today = self.init_time
        today2 = datetime2(today.year, today.month, today.day, today.hour, today.minute, today.second, today.microsecond)
        today3 = today2
        t_year = today.year

        leap_years = 0
        for i in range(t_year, year_in + t_year):
            if calendar.isleap(i):
                leap_years += 1
        cont_year = (year_in * spy) + (leap_years * spd)

        for i in range(month_in):
            today2.add_month(1)
            cont_month += (spd * (today2 - today3).days)
            today3 = today2

        t_used = cont_year + cont_month + cont_day + cont_hour + cont_min + cont_sec
        print(dict_print({
            "t_used": t_used,
            "cont_year": cont_year,
            "cont_month": cont_month,
            "cont_day": cont_day,
            "cont_hour": cont_hour,
            "cont_min": cont_min,
            "cont_sec": cont_sec
        }, "results"))

        return year_in, month_in, day_in, hour_in, min_in, sec_in


if __name__ == '__main__':

    app = tkinter.Tk()
    app.geometry(f"600x400")
    cdt = CountDownTimer(app, month_in=2)
    app.mainloop()
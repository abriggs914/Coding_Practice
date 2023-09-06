import calendar
import datetime
import tkinter

from colour_utility import Colour
from tkinter_utility import radio_factory

# simple tkinter application to demo radio_factory.
# Avery Briggs
# 2023-09-02


def update_month_choice(*args):
    print(f"New month choice '{calendar.month_name[var_1.get() + 1]}'")  # +1 due to 1-based arrays in calendar


def update_weekday_choice(*args):
    print(f"New weekday choice '{calendar.day_name[var_2.get() - 1]}'")  # -1 due to Monday being 0 in calendar


if __name__ == '__main__':

    win = tkinter.Tk()
    win.geometry("300x600")

    btn_lbls_1 = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    btn_lbls_2 = ["SUN", "MON", "TUE", "WED", "THU", "FRI", "SAT"]

    c1 = Colour("#465778")
    c2 = Colour("#161518")
    c3 = Colour("#A6C5A8")

    #
    var_1, tv_vars_1, r_buttons_1 = radio_factory(
        win,
        buttons=btn_lbls_1,
        default_value=datetime.datetime.now().month - 1,  # must be an integer representing desired item's index.
        kwargs_buttons={
            "bg": c2.hex_code,
            "fg": c1.hex_code,
            "activebackground": c2.brightened(0.1).hex_code,
            "activeforeground": c1.brightened(0.1).hex_code
        }
    )
    var_2, tv_vars_2, r_buttons_2 = radio_factory(
        win,
        buttons=btn_lbls_2,
        default_value=(datetime.datetime.now().weekday() + 1) % 7,  # must be an integer representing desired item's index.
        kwargs_buttons={
            "bg": c1.hex_code,
            "fg": c3.hex_code,
            "activebackground": c1.brightened(0.1).hex_code,
            "activeforeground": c3.brightened(0.1).hex_code,
            "font": "Arial 12 bold"
        }
    )

    var_1.trace_variable("w", update_month_choice)
    var_2.trace_variable("w", update_weekday_choice)

    for btn in r_buttons_1:
        btn.pack()
    for btn in r_buttons_2:
        btn.pack()

    win.mainloop()

import tkinter

from tkinter_utility import *


def time_until(time_in=datetime.datetime(2022, 12, 21, 19), unit: Literal["seconds", "minutes", "hours", "days", "months", "years"] = "seconds", rtype: Literal["str", "float"] = "str"):
    seconds = (time_in - datetime.datetime.now()).seconds
    match unit:
        case "years":
            seconds /= 60 * 60 * 24 * 365
            return f"{seconds} seconds" if rtype == "str" else seconds
        case "months":
            seconds /= 60 * 60 * 24 * 30
            return f"{seconds} seconds" if rtype == "str" else seconds
        case "days":
            seconds /= 60 * 60 * 24
            return f"{seconds} seconds" if rtype == "str" else seconds
        case "hours":
            seconds /= 60 * 60
            return f"{seconds} seconds" if rtype == "str" else seconds
        case "minutes":
            seconds /= 60
            return f"{seconds} seconds" if rtype == "str" else seconds
        case _:
            return f"{seconds} seconds" if rtype == "str" else seconds
        #.strftime("%Y-%m-%d %H:%M:%S")


def update_time():
    tv_time_years.set(time_until(unit="years", rtype="float"))
    tv_time_months.set(time_until(unit="months", rtype="float"))
    tv_time_days.set(time_until(unit="days", rtype="float"))
    tv_time_hours.set(time_until(unit="hours", rtype="float"))
    tv_time_minutes.set(time_until(unit="minutes", rtype="float"))
    tv_time_seconds.set(time_until(rtype="float"))
    window.after(1000, update_time)


if __name__ == '__main__':

    WIDTH, HEIGHT = 600, 500
    window = tkinter.Tk()
    window.geometry(f"{WIDTH}x{HEIGHT}")

    tv_time_years = tkinter.StringVar(window, value=time_until())
    tv_time_months = tkinter.StringVar(window, value=time_until())
    tv_time_days = tkinter.StringVar(window, value=time_until())
    tv_time_hours = tkinter.StringVar(window, value=time_until())
    tv_time_minutes = tkinter.StringVar(window, value=time_until())
    tv_time_seconds = tkinter.StringVar(window, value=time_until())

    label_years = tkinter.Label(window, textvariable=tv_time_years)
    label_months = tkinter.Label(window, textvariable=tv_time_months)
    label_days = tkinter.Label(window, textvariable=tv_time_days)
    label_hours = tkinter.Label(window, textvariable=tv_time_hours)
    label_minutes = tkinter.Label(window, textvariable=tv_time_minutes)
    label_seconds = tkinter.Label(window, textvariable=tv_time_seconds)

    label_years_title = tkinter.Label(window, text="Years")
    label_months_title = tkinter.Label(window, text="Months")
    label_days_title = tkinter.Label(window, text="Days")
    label_hours_title = tkinter.Label(window, text="Hours")
    label_minutes_title = tkinter.Label(window, text="Minutes")
    label_seconds_title = tkinter.Label(window, text="Seconds")

    for i, time_val_title in enumerate(zip(
        [label_years, label_months, label_days, label_hours, label_minutes, label_seconds],
        [label_years_title, label_months_title, label_days_title, label_hours_title, label_minutes_title, label_seconds_title]
    )):
        time_val, title = time_val_title
        time_val.grid(row=0, column=i)
        title.grid(row=1, column=i)

    update_time()

    window.mainloop()

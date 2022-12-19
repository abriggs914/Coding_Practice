import tkinter

from tkinter_utility import *


fmt = "%Y-%m-%d %H:%M:%S"
game_time = datetime.datetime(2022, 12, 19, 18, 30) + datetime.timedelta(hours=-3.75)
# game_time = datetime.datetime(2022, 12, 16, 10)


def time_until(time_in=game_time, start_time=None, unit: Literal["seconds", "minutes", "hours", "days", "months", "years"] = "seconds", rtype: Literal["str", "float"] = "str", vtype: Literal["whole", "remainder"] = "remainder"):
    if start_time is None:
        start_time = datetime.datetime.now()
    w_seconds = (86400 * (time_in - start_time).days) + (time_in - start_time).seconds
    # print(f"{start_time=}, {time_in=}, {w_seconds=}, {(time_in - start_time)=}")
    w_minutes = w_seconds / 60
    w_hours = w_minutes / 60
    w_days = w_hours / 24
    w_months = w_days / 31
    w_years = w_days / 365

    r_years = int(w_seconds / (60 * 60 * 24 * 365))
    r_months = int(w_seconds / (60 * 60 * 24 * (365 / 12))) % 12
    r_days = int(w_seconds / (60 * 60 * 24)) % 365
    r_hours = int(w_seconds / (60 * 60)) % 60
    r_minutes = int(w_seconds / 60) % 60
    r_seconds = w_seconds % 60
    match unit:
        case "years":
            if vtype == "whole":
                return f"{w_years} years" if rtype == "str" else w_years
            return f"{r_years} years" if rtype == "str" else r_years
        case "months":
            if vtype == "whole":
                # w_seconds /= 60 * 60 * 24 * 30
                return f"{w_months} months" if rtype == "str" else w_months
            return f"{r_months} months" if rtype == "str" else r_months
        case "days":
            if vtype == "whole":
                # w_seconds /= 60 * 60 * 24
                return f"{w_days} days" if rtype == "str" else w_days
            return f"{r_days} days" if rtype == "str" else r_days
        case "hours":
            if vtype == "whole":
                # w_seconds /= 60 * 60
                return f"{w_hours} hours" if rtype == "str" else w_hours
            return f"{r_hours} hours" if rtype == "str" else r_hours
        case "minutes":
            if vtype == "whole":
                # w_seconds /= 60
                return f"{w_minutes} minutes" if rtype == "str" else w_minutes
            return f"{r_minutes} minutes" if rtype == "str" else r_minutes
        case _:
            if vtype == "whole":
                return f"{w_seconds} seconds" if rtype == "str" else w_seconds
            return f"{r_seconds} seconds" if rtype == "str" else r_seconds
        #.strftime("%Y-%m-%d %H:%M:%S")


def update_time():
    if not testing:
        tv_date_1.set(datetime.datetime.now().strftime(fmt))
        tv_time_years.set(f"{time_until(unit='years', rtype='float'): d}")
        tv_time_months.set(f"{time_until(unit='months', rtype='float'): d}")
        tv_time_days.set(f"{time_until(unit='days', rtype='float'): d}")
        tv_time_hours.set(f"{time_until(unit='hours', rtype='float'): d}")
        tv_time_minutes.set(f"{time_until(unit='minutes', rtype='float'): d}")
        tv_time_seconds.set(f"{time_until(rtype='float'): d}")
        print(f"{time_until(vtype='whole')=}")
    else:
        tv_date_1.set(st.strftime(fmt))
        tv_time_years.set(f"{time_until(start_time=st, unit='years', rtype='float'): .4f}")
        tv_time_months.set(f"{time_until(start_time=st, unit='months', rtype='float'): .4f}")
        tv_time_days.set(f"{time_until(start_time=st, unit='days', rtype='float'): .4f}")
        tv_time_hours.set(f"{time_until(start_time=st, unit='hours', rtype='float'): .4f}")
        tv_time_minutes.set(f"{time_until(start_time=st, unit='minutes', rtype='float'): .4f}")
        tv_time_seconds.set(f"{time_until(start_time=st, rtype='float'): .4f}")
        print(f"{time_until(start_time=st, vtype='whole')=}")
    window.after(1000, update_time)


if __name__ == '__main__':

    WIDTH, HEIGHT = 800, 500
    window = tkinter.Tk()
    window.geometry(f"{WIDTH}x{HEIGHT}")

    testing = False
    st = datetime.datetime(2021, 12, 16, 11, 9)
    st = game_time + datetime.timedelta(hours=-3.25)
    tv_label_date_1, label_date_1, tv_date_1, date_1 = entry_factory(window, tv_label="Start Date:", tv_entry=datetime.datetime.now().strftime(fmt), kwargs_entry={"state": "readonly", "justify": "center"})
    tv_label_date_2, label_date_2, tv_date_2, date_2 = entry_factory(window, tv_label="Game Time:", tv_entry=game_time.strftime(fmt), kwargs_entry={"state": "readonly", "justify": "center"})

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

    label_date_1.grid(row=0, column=0, columnspan=2, sticky="ew")
    date_1.grid(row=0, column=2, columnspan=4, sticky="ew")
    label_date_2.grid(row=1, column=0, columnspan=2, sticky="ew")
    date_2.grid(row=1, column=2, columnspan=4, sticky="ew")

    for i, time_val_title in enumerate(zip(
        [label_years, label_months, label_days, label_hours, label_minutes, label_seconds],
        [label_years_title, label_months_title, label_days_title, label_hours_title, label_minutes_title, label_seconds_title]
    )):
        time_val, title = time_val_title
        time_val.grid(row=3, column=i)
        title.grid(row=2, column=i)

    update_time()

    window.mainloop()

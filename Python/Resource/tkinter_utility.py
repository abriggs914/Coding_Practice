
import tkinter
from tkinter import ttk


#######################################################################################################################
#######################################################################################################################
#######################################################################################################################

VERSION = \
    """	
    General Utility Functions
    Version..............1.04
    Date...........2022-09-13
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


def entry_factory(master, tv_label=None, tv_entry=None, kwargs_label=None, kwargs_entry=None):
    """Return tkinter StringVar, Label, StringVar, Entry objects"""
    if tv_label is not None and tv_entry is not None:
        res_tv_label = tkinter.StringVar(master, value=tv_label)
        res_tv_entry = tkinter.StringVar(master, value=tv_entry)
    elif tv_label is not None:
        res_tv_label = tkinter.StringVar(master, value=tv_label)
        res_tv_entry = tkinter.StringVar(master)
    elif tv_entry is not None:
        res_tv_label = tkinter.StringVar(master)
        res_tv_entry = tkinter.StringVar(master, value=tv_entry)
    else:
        res_tv_label = tkinter.StringVar(master)
        res_tv_entry = tkinter.StringVar(master)

    if kwargs_label is not None and kwargs_entry is not None:
        res_label = tkinter.Label(master, textvariable=res_tv_label, **kwargs_label)
        res_entry = tkinter.Entry(master, textvariable=res_tv_entry, **kwargs_entry)
    elif kwargs_label is not None:
        res_label = tkinter.Label(master, textvariable=res_tv_label, **kwargs_label)
        res_entry = tkinter.Entry(master, textvariable=res_tv_entry)
    elif kwargs_entry is not None:
        res_label = tkinter.Label(master, textvariable=res_tv_label)
        res_entry = tkinter.Entry(master, textvariable=res_tv_entry, **kwargs_entry)
    else:
        res_label = tkinter.Label(master, textvariable=res_tv_label)
        res_entry = tkinter.Entry(master, textvariable=res_tv_entry)
    return res_tv_label, res_label, res_tv_entry, res_entry


def button_factory(master, tv_btn=None, kwargs_btn=None):
    """Return tkinter StringVar, Button objects"""
    res_tv_btn = tkinter.StringVar(master)
    if tv_btn is not None:
        res_tv_btn = tkinter.StringVar(master, value=tv_btn)
    res_btn = tkinter.Button(master, textvariable=res_tv_btn)
    if kwargs_btn is not None:
        res_btn = tkinter.Button(master, textvariable=res_tv_btn, **kwargs_btn)
    return res_tv_btn, res_btn


def combo_factory(master, tv_label=None, kwargs_label=None, tv_combo=None, kwargs_combo=None):
    """Return tkinter StringVar, Label, StringVar, Entry objects"""
    if tv_label is not None and tv_combo is not None:
        res_tv_label = tkinter.StringVar(master, value=tv_label)
        res_tv_combo = tkinter.StringVar(master, value=tv_combo)
    elif tv_label is not None:
        res_tv_label = tkinter.StringVar(master, value=tv_label)
        res_tv_combo = tkinter.StringVar(master)
    elif tv_combo is not None:
        res_tv_label = tkinter.StringVar(master)
        res_tv_combo = tkinter.StringVar(master, value=tv_combo)
    else:
        res_tv_label = tkinter.StringVar(master)
        res_tv_combo = tkinter.StringVar(master)

    if kwargs_label is not None and kwargs_combo is not None:
        res_label = tkinter.Label(master, textvariable=res_tv_label, **kwargs_label)
        res_combo = ttk.Combobox(master, textvariable=res_tv_combo, **kwargs_combo)
    elif kwargs_label is not None:
        res_label = tkinter.Label(master, textvariable=res_tv_label, **kwargs_label)
        res_combo = ttk.Combobox(master, textvariable=res_tv_combo)
    elif kwargs_combo is not None:
        res_label = tkinter.Label(master, textvariable=res_tv_label)
        res_combo = ttk.Combobox(master, textvariable=res_tv_combo, **kwargs_combo)
    else:
        res_label = tkinter.Label(master, textvariable=res_tv_label)
        res_combo = ttk.Combobox(master, textvariable=res_tv_combo)
    return res_tv_label, res_label, res_tv_combo, res_combo


def test_entry_factory():
    WIN = tkinter.Tk()
    WIDTH, HEIGHT = 500, 500
    WIN.geometry(f"{WIDTH}x{HEIGHT}")
    tv_1, lbl_1, tv_2, entry_1 = entry_factory(WIN, tv_label="This is a Label", tv_entry="This is an Entry", kwargs_entry={"background": "yellow"})
    lbl_1.pack()
    entry_1.pack()
    WIN.mainloop()


def test_combo_1():
    WIN = tkinter.Tk()
    WIN.geometry(f"500x500")
    WIN.title("Select Start Date")

    f1 = tkinter.Frame(WIN)
    f2 = tkinter.Frame(f1)
    dealers = ["A", "B", "C"]
    colours = ["red", "blue", "green", "custom", "none"]
    tv1 = tkinter.StringVar(f2, value="")
    cb1 = ttk.Combobox(f2, values=dealers, textvariable=tv1, state="readonly")
    tv2 = tkinter.StringVar(f2, value="")
    cb2 = ttk.Combobox(f2, values=colours, textvariable=tv2, state="readonly")

    def new_dealer(var_name, index, mode):
        d = tv1.get()
        c = tv2.get()
        if c and d:
            if c not in ["custom", "none"]:
                print(f"Setting {d=} to {c=}")
            elif c == "custom":
                print(f"custom colour from dealer {d=}")
            else:
                print(f"removing colour from dealer {d=}")

    def new_colour(var_name, index, mode):
        d = tv1.get()
        c = tv2.get()
        if c and d:
            if c not in ["custom", "none"]:
                print(f"Setting {d=} to {c=}")
            elif c == "custom":
                print(f"custom colour from dealer {d=}")
            else:
                print(f"removing colour from dealer {d=}")

    tv1.trace_variable("w", new_dealer)
    tv2.trace_variable("w", new_colour)

    cb1.grid()
    cb2.grid()
    f1.grid()
    f2.grid()
    WIN.mainloop()


def test_combo_factory():
    WIN = tkinter.Tk()
    WIN.geometry(f"500x500")
    WIN.title("Select Start Date")
    dealers = ["A", "B", "C"]
    colours = ["red", "blue", "green", "custom", "none"]
    sv_lbl_1, lbl_1, sv_cb_1, cb_1 = combo_factory(WIN, tv_label="Dealer", kwargs_combo={"values": dealers})
    sv_lbl_2, lbl_2, sv_cb_2, cb_2 = combo_factory(WIN, tv_label="Colour", kwargs_combo={"values": colours})

    def new_dealer(var_name, index, mode):
        d = sv_cb_1.get()
        c = sv_cb_2.get()
        if c and d:
            if c not in ["custom", "none"]:
                print(f"Setting {d=} to {c=}")
            elif c == "custom":
                print(f"custom colour from dealer {d=}")
            else:
                print(f"removing colour from dealer {d=}")

    def new_colour(var_name, index, mode):
        d = sv_cb_1.get()
        c = sv_cb_2.get()
        if c and d:
            if c not in ["custom", "none"]:
                print(f"Setting {d=} to {c=}")
            elif c == "custom":
                print(f"custom colour from dealer {d=}")
            else:
                print(f"removing colour from dealer {d=}")

    sv_cb_1.trace_variable("w", new_dealer)
    sv_cb_2.trace_variable("w", new_colour)
    lbl_1.grid(row=1, column=1)
    lbl_2.grid(row=2, column=1)
    cb_1.grid(row=1, column=2)
    cb_2.grid(row=2, column=2)
    WIN.mainloop()


if __name__ == '__main__':
    print('PyCharm')

    # test_entry_factory()
    # test_combo_1()
    test_combo_factory()


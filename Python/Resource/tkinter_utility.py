
import tkinter


#######################################################################################################################
#######################################################################################################################
#######################################################################################################################

VERSION = \
"""	
	General Utility Functions
	Version..............1.02
	Date...........2022-09-09
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



if __name__ == '__main__':
    print('PyCharm')

    WIN = tkinter.Tk()
    WIDTH, HEIGHT = 500, 500
    WIN.geometry(f"{WIDTH}x{HEIGHT}")
    tv_1, lbl_1, tv_2, entry_1 = entry_factory(WIN, tv_label="This is a Label", tv_entry="This is an Entry", kwargs_entry={"background": "yellow"})
    lbl_1.pack()
    entry_1.pack()
    WIN.mainloop()

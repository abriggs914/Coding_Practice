import tkinter
from tkinter_utility import label_factory

# simple tkinter application to demo label_factory.
# Avery Briggs
# 2023-09-01


if __name__ == '__main__':

    win = tkinter.Tk()
    win.geometry("300x200")

    tv_1, lbl_1 = label_factory(win, tv_label="Hello World")

    tv_2, lbl_2 = label_factory(
        win,
        tv_label="Hello World",
        kwargs_label={
            "bg": "#185445",
            "fg": "#A477F3",
            "font": ("Times 14 bold")
        }
    )

    lbl_1.pack()
    lbl_2.pack()

    win.mainloop()

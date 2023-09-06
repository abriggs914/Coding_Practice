import tkinter
from tkinter_utility import entry_tip_factory

# simple tkinter application to demo entry_factory.
# Avery Briggs
# 2023-09-01


if __name__ == '__main__':

    win = tkinter.Tk()
    win.geometry("300x200")

    tv_1, lbl_1, tv_entry_1, entry_1 = entry_tip_factory(
        win,
        tip="First Name"
    )

    tv_2, lbl_2, tv_entry_2, entry_2 = entry_tip_factory(
        win,
        tip="Last Name",
        kwargs_entry={
            "bg": "#185445",
            "fg": "#A477F3",
            "font": "Times 14 bold"
        }
    )

    entry_1.pack()
    entry_2.pack()

    win.mainloop()

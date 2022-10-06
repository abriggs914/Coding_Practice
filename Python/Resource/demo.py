from tkinter_utility import *
from colour_utility import *

from time import sleep

if __name__ == '__main__':
    from tkinter import *

    t = Tk()
    v = IntVar(t, value=5)
    t.geometry(f"500x500")

    def foo(*args):
        if v.get() != 0:
            # you can use a widget here to ex: tkinter.Button.after(1000, f)
            t.after(1000, foo)
            v.set(v.get() - 1)
        return

    def foo1(*args):
        sleep(5)

    a, b, c, d = entry_factory(t, tv_entry=v, tv_label="name", kwargs_entry={"background": random_colour(rgb=False)})
    e, f = button_factory(t, tv_btn="click1", kwargs_btn={"command": foo})
    g, h = button_factory(t, tv_btn="click2", kwargs_btn={"command": foo1})

    b.pack()
    d.pack()
    f.pack()
    h.pack()

    t.mainloop()

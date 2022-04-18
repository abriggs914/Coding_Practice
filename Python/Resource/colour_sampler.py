from utility import *
from colour_utility import *
import tkinter
from tkinter import ttk
from tkinter import colorchooser


if __name__ == "__main__":
    WINDOW = tkinter.Tk()
    WINDOW.geometry(f"{800}x{500}")
    WINDOW.title("Colour Sampler")

    # text fg
    # text bg
    # rect
    # border
    tv_text = tkinter.StringVar(WINDOW, "Sample Text [{1}, 2, 3?, ':!@#$%^&*()']", name="tv_text")
    tv_r1 = tkinter.IntVar(WINDOW, 0, name="tv_r1")
    tv_r2 = tkinter.IntVar(WINDOW, 0, name="tv_r2")
    tv_r3 = tkinter.IntVar(WINDOW, 0, name="tv_r3")
    tv_r4 = tkinter.IntVar(WINDOW, 0, name="tv_r4")
    tv_g1 = tkinter.IntVar(WINDOW, 0, name="tv_g1")
    tv_g2 = tkinter.IntVar(WINDOW, 0, name="tv_g2")
    tv_g3 = tkinter.IntVar(WINDOW, 0, name="tv_g3")
    tv_g4 = tkinter.IntVar(WINDOW, 0, name="tv_g4")
    tv_b1 = tkinter.IntVar(WINDOW, 0, name="tv_b1")
    tv_b2 = tkinter.IntVar(WINDOW, 0, name="tv_b2")
    tv_b3 = tkinter.IntVar(WINDOW, 0, name="tv_b3")
    tv_b4 = tkinter.IntVar(WINDOW, 0, name="tv_b4")

    def parse_c1():
        return rgb_to_hex((tv_r1.get(), tv_g1.get(), tv_b1.get()))

    def parse_c2():
        return rgb_to_hex((tv_r2.get(), tv_g2.get(), tv_b2.get()))

    def parse_c3():
        return rgb_to_hex((tv_r3.get(), tv_g3.get(), tv_b3.get()))

    def parse_c4():
        return rgb_to_hex((tv_r4.get(), tv_g4.get(), tv_b4.get()))

    tv_h1 = tkinter.StringVar(WINDOW, value=parse_c1(), name="tv_h1")
    tv_h2 = tkinter.StringVar(WINDOW, value=parse_c2(), name="tv_h2")
    tv_h3 = tkinter.StringVar(WINDOW, value=parse_c3(), name="tv_h3")
    tv_h4 = tkinter.StringVar(WINDOW, value=parse_c4(), name="tv_h4")

    def update_c1():
        # Background
        tv_h1.set(parse_c1())
        frame_h1.config(bg=tv_h1.get())
        frame_demo.config(bg=tv_h1.get())
        lbl_c1.config(bg=tv_h1.get())
        if sum(hex_to_rgb(tv_h1.get())) < (3 * 255) / 2:
            lbl_c1.config(fg="white")
        else:
            lbl_c1.config(fg="black")

    def update_c2():
        # Border
        tv_h2.set(parse_c2())
        frame_h2.config(bg=tv_h2.get())
        frame_border.config(bg=tv_h2.get())
        lbl_c2.config(bg=tv_h2.get())
        if sum(hex_to_rgb(tv_h2.get())) < (3 * 255) / 2:
            lbl_c2.config(fg="white")
        else:
            lbl_c2.config(fg="black")

    def update_c3():
        # Font Background
        tv_h3.set(parse_c3())
        frame_h3.config(bg=tv_h3.get())
        entry_text.config(bg=tv_h3.get())
        lbl_c3.config(bg=tv_h3.get())
        if sum(hex_to_rgb(tv_h3.get())) < (3 * 255) / 2:
            lbl_c3.config(fg="white")
        else:
            lbl_c3.config(fg="black")

    def update_c4():
        # Font Foreground
        tv_h4.set(parse_c4())
        frame_h4.config(bg=tv_h4.get())
        entry_text.config(fg=tv_h4.get())
        lbl_c4.config(bg=tv_h4.get())
        if sum(hex_to_rgb(tv_h4.get())) < (3 * 255) / 2:
            lbl_c4.config(fg="white")
        else:
            lbl_c4.config(fg="black")

    def inc_r1():
        v = clamp(0, tv_r1.get() + 1, 255)
        tv_r1.set(v)
        update_c1()

    def inc_r2():
        v = clamp(0, tv_r2.get() + 1, 255)
        tv_r2.set(v)
        update_c2()

    def inc_r3():
        v = clamp(0, tv_r3.get() + 1, 255)
        tv_r3.set(v)
        update_c3()

    def inc_r4():
        v = clamp(0, tv_r4.get() + 1, 255)
        tv_r4.set(v)
        update_c4()

    def dec_r1():
        v = clamp(0, tv_r1.get() - 1, 255)
        tv_r1.set(v)
        update_c1()

    def dec_r2():
        v = clamp(0, tv_r2.get() - 1, 255)
        tv_r2.set(v)
        update_c2()

    def dec_r3():
        v = clamp(0, tv_r3.get() - 1, 255)
        tv_r3.set(v)
        update_c3()

    def dec_r4():
        v = clamp(0, tv_r4.get() - 1, 255)
        tv_r4.set(v)
        update_c4()

    def inc_g1():
        v = clamp(0, tv_g1.get() + 1, 255)
        tv_g1.set(v)
        update_c1()

    def inc_g2():
        v = clamp(0, tv_g2.get() + 1, 255)
        tv_g2.set(v)
        update_c2()

    def inc_g3():
        v = clamp(0, tv_g3.get() + 1, 255)
        tv_g3.set(v)
        update_c3()

    def inc_g4():
        v = clamp(0, tv_g4.get() + 1, 255)
        tv_g4.set(v)
        update_c4()

    def dec_g1():
        v = clamp(0, tv_g1.get() - 1, 255)
        tv_g1.set(v)
        update_c1()

    def dec_g2():
        v = clamp(0, tv_g2.get() - 1, 255)
        tv_g2.set(v)
        update_c2()

    def dec_g3():
        v = clamp(0, tv_g3.get() - 1, 255)
        tv_g3.set(v)
        update_c3()

    def dec_g4():
        v = clamp(0, tv_g4.get() - 1, 255)
        tv_g4.set(v)
        update_c4()

    def inc_b1():
        v = clamp(0, tv_b1.get() + 1, 255)
        tv_b1.set(v)
        update_c1()

    def inc_b2():
        v = clamp(0, tv_b2.get() + 1, 255)
        tv_b2.set(v)
        update_c2()

    def inc_b3():
        v = clamp(0, tv_b3.get() + 1, 255)
        tv_b3.set(v)
        update_c3()

    def inc_b4():
        v = clamp(0, tv_b4.get() + 1, 255)
        tv_b4.set(v)
        update_c4()

    def dec_b1():
        v = clamp(0, tv_b1.get() - 1, 255)
        tv_b1.set(v)
        update_c1()

    def dec_b2():
        v = clamp(0, tv_b2.get() - 1, 255)
        tv_b2.set(v)
        update_c2()

    def dec_b3():
        v = clamp(0, tv_b3.get() - 1, 255)
        tv_b3.set(v)
        update_c3()

    def dec_b4():
        v = clamp(0, tv_b4.get() - 1, 255)
        tv_b4.set(v)
        update_c4()

    frame_colour_controls = tkinter.Frame(WINDOW, name="frame_colour_controls")

    frame_demo = tkinter.Frame(WINDOW, name="frame_demo")
    frame_border = tkinter.Frame(frame_demo, name="frame_border", padx=25, pady=25)
    entry_text = tkinter.Entry(frame_border, textvariable=tv_text, width=65, name="entry_text")

    frame_h1 = tkinter.Frame(frame_colour_controls, bg="orange")
    frame_h2 = tkinter.Frame(frame_colour_controls)
    frame_h3 = tkinter.Frame(frame_colour_controls)
    frame_h4 = tkinter.Frame(frame_colour_controls)

    frame_c1 = tkinter.Frame(frame_h1, name="frame_c1", bg="yellow")
    frame_r1 = tkinter.Frame(frame_c1, name="frame_r1")
    frame_g1 = tkinter.Frame(frame_c1, name="frame_g1")
    frame_b1 = tkinter.Frame(frame_c1, name="frame_b1")
    frame_c2 = tkinter.Frame(frame_h2, name="frame_c2")
    frame_r2 = tkinter.Frame(frame_c2, name="frame_r2")
    frame_g2 = tkinter.Frame(frame_c2, name="frame_g2")
    frame_b2 = tkinter.Frame(frame_c2, name="frame_b2")
    frame_c3 = tkinter.Frame(frame_h3, name="frame_c3")
    frame_r3 = tkinter.Frame(frame_c3, name="frame_r3")
    frame_g3 = tkinter.Frame(frame_c3, name="frame_g3")
    frame_b3 = tkinter.Frame(frame_c3, name="frame_b3")
    frame_c4 = tkinter.Frame(frame_h4, name="frame_c4")
    frame_r4 = tkinter.Frame(frame_c4, name="frame_r4")
    frame_g4 = tkinter.Frame(frame_c4, name="frame_g4")
    frame_b4 = tkinter.Frame(frame_c4, name="frame_b4")

    frame_l1 = tkinter.Frame(frame_h1)
    frame_l2 = tkinter.Frame(frame_h2)
    frame_l3 = tkinter.Frame(frame_h3)
    frame_l4 = tkinter.Frame(frame_h4)

    lbl_c1 = tkinter.Label(frame_l1, text="Background")
    lbl_h1 = tkinter.Entry(frame_l1, textvariable=tv_h1)
    lbl_c2 = tkinter.Label(frame_l2, text="Border")
    lbl_h2 = tkinter.Entry(frame_l2, textvariable=tv_h2)
    lbl_c3 = tkinter.Label(frame_l3, text="Font Background")
    lbl_h3 = tkinter.Entry(frame_l3, textvariable=tv_h3)
    lbl_c4 = tkinter.Label(frame_l4, text="Font Foreground")
    lbl_h4 = tkinter.Entry(frame_l4, textvariable=tv_h4)

    lbl_r1 = tkinter.Label(frame_r1, text="R:")
    lbl_r2 = tkinter.Label(frame_r2, text="R:")
    lbl_r3 = tkinter.Label(frame_r3, text="R:")
    lbl_r4 = tkinter.Label(frame_r4, text="R:")

    lbl_g1 = tkinter.Label(frame_g1, text="G:")
    lbl_g2 = tkinter.Label(frame_g2, text="G:")
    lbl_g3 = tkinter.Label(frame_g3, text="G:")
    lbl_g4 = tkinter.Label(frame_g4, text="G:")

    lbl_b1 = tkinter.Label(frame_b1, text="B:")
    lbl_b2 = tkinter.Label(frame_b2, text="B:")
    lbl_b3 = tkinter.Label(frame_b3, text="B:")
    lbl_b4 = tkinter.Label(frame_b4, text="B:")

    btn_i_r1 = tkinter.Button(frame_r1, command=inc_r1, text="+", name="btn_i_r1")
    btn_i_r2 = tkinter.Button(frame_r2, command=inc_r2, text="+", name="btn_i_r2")
    btn_i_r3 = tkinter.Button(frame_r3, command=inc_r3, text="+", name="btn_i_r3")
    btn_i_r4 = tkinter.Button(frame_r4, command=inc_r4, text="+", name="btn_i_r4")

    btn_i_g1 = tkinter.Button(frame_g1, command=inc_g1, text="+", name="btn_i_g1")
    btn_i_g2 = tkinter.Button(frame_g2, command=inc_g2, text="+", name="btn_i_g2")
    btn_i_g3 = tkinter.Button(frame_g3, command=inc_g3, text="+", name="btn_i_g3")
    btn_i_g4 = tkinter.Button(frame_g4, command=inc_g4, text="+", name="btn_i_g4")

    btn_i_b1 = tkinter.Button(frame_b1, command=inc_b1, text="+", name="btn_i_b1")
    btn_i_b2 = tkinter.Button(frame_b2, command=inc_b2, text="+", name="btn_i_b2")
    btn_i_b3 = tkinter.Button(frame_b3, command=inc_b3, text="+", name="btn_i_b3")
    btn_i_b4 = tkinter.Button(frame_b4, command=inc_b4, text="+", name="btn_i_b4")

    btn_d_r1 = tkinter.Button(frame_r1, command=dec_r1, text="-", name="btn_d_r1")
    btn_d_r2 = tkinter.Button(frame_r2, command=dec_r2, text="-", name="btn_d_r2")
    btn_d_r3 = tkinter.Button(frame_r3, command=dec_r3, text="-", name="btn_d_r3")
    btn_d_r4 = tkinter.Button(frame_r4, command=dec_r4, text="-", name="btn_d_r4")

    btn_d_g1 = tkinter.Button(frame_g1, command=dec_g1, text="-", name="btn_d_g1")
    btn_d_g2 = tkinter.Button(frame_g2, command=dec_g2, text="-", name="btn_d_g2")
    btn_d_g3 = tkinter.Button(frame_g3, command=dec_g3, text="-", name="btn_d_g3")
    btn_d_g4 = tkinter.Button(frame_g4, command=dec_g4, text="-", name="btn_d_g4")

    btn_d_b1 = tkinter.Button(frame_b1, command=dec_b1, text="-", name="btn_d_b1")
    btn_d_b2 = tkinter.Button(frame_b2, command=dec_b2, text="-", name="btn_d_b2")
    btn_d_b3 = tkinter.Button(frame_b3, command=dec_b3, text="-", name="btn_d_b3")
    btn_d_b4 = tkinter.Button(frame_b4, command=dec_b4, text="-", name="btn_d_b4")

    entry_r1 = tkinter.Entry(frame_r1, textvariable=tv_r1, width=25, name="entry_r1")
    entry_r2 = tkinter.Entry(frame_r2, textvariable=tv_r2, width=25, name="entry_r2")
    entry_r3 = tkinter.Entry(frame_r3, textvariable=tv_r3, width=25, name="entry_r3")
    entry_r4 = tkinter.Entry(frame_r4, textvariable=tv_r4, width=25, name="entry_r4")
    entry_g1 = tkinter.Entry(frame_g1, textvariable=tv_g1, width=25, name="entry_g1")
    entry_g2 = tkinter.Entry(frame_g2, textvariable=tv_g2, width=25, name="entry_g2")
    entry_g3 = tkinter.Entry(frame_g3, textvariable=tv_g3, width=25, name="entry_g3")
    entry_g4 = tkinter.Entry(frame_g4, textvariable=tv_g4, width=25, name="entry_g4")
    entry_b1 = tkinter.Entry(frame_b1, textvariable=tv_b1, width=25, name="entry_b1")
    entry_b2 = tkinter.Entry(frame_b2, textvariable=tv_b2, width=25, name="entry_b2")
    entry_b3 = tkinter.Entry(frame_b3, textvariable=tv_b3, width=25, name="entry_b3")
    entry_b4 = tkinter.Entry(frame_b4, textvariable=tv_b4, width=25, name="entry_b4")

    frame_border.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
    # entry_text.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
    # frame_border.pack()
    entry_text.pack()

    lbl_c1.pack(side=tkinter.TOP)
    lbl_h1.pack(side=tkinter.TOP)

    lbl_r1.pack(side=tkinter.LEFT)
    btn_i_r1.pack(side=tkinter.LEFT)
    entry_r1.pack(side=tkinter.LEFT)
    btn_d_r1.pack(side=tkinter.RIGHT)
    frame_r1.pack(side=tkinter.TOP)

    lbl_g1.pack(side=tkinter.LEFT)
    btn_i_g1.pack(side=tkinter.LEFT)
    entry_g1.pack(side=tkinter.LEFT)
    btn_d_g1.pack(side=tkinter.RIGHT)
    frame_g1.pack(side=tkinter.TOP)

    lbl_b1.pack(side=tkinter.LEFT)
    btn_i_b1.pack(side=tkinter.LEFT)
    entry_b1.pack(side=tkinter.LEFT)
    btn_d_b1.pack(side=tkinter.RIGHT)
    frame_b1.pack(side=tkinter.TOP)

    frame_l1.pack(side=tkinter.LEFT)
    frame_c1.pack(side=tkinter.RIGHT)
    frame_h1.pack()

    lbl_c2.pack(side=tkinter.TOP)
    lbl_h2.pack(side=tkinter.TOP)

    lbl_r2.pack(side=tkinter.LEFT)
    btn_i_r2.pack(side=tkinter.LEFT)
    entry_r2.pack(side=tkinter.LEFT)
    btn_d_r2.pack(side=tkinter.RIGHT)
    frame_r2.pack(side=tkinter.TOP)

    lbl_g2.pack(side=tkinter.LEFT)
    btn_i_g2.pack(side=tkinter.LEFT)
    entry_g2.pack(side=tkinter.LEFT)
    btn_d_g2.pack(side=tkinter.RIGHT)
    frame_g2.pack(side=tkinter.TOP)

    lbl_b2.pack(side=tkinter.LEFT)
    btn_i_b2.pack(side=tkinter.LEFT)
    entry_b2.pack(side=tkinter.LEFT)
    btn_d_b2.pack(side=tkinter.RIGHT)
    frame_b2.pack(side=tkinter.TOP)

    frame_l2.pack(side=tkinter.LEFT)
    frame_c2.pack(side=tkinter.RIGHT)
    frame_h2.pack()

    lbl_c3.pack(side=tkinter.TOP)
    lbl_h3.pack(side=tkinter.TOP)

    lbl_r3.pack(side=tkinter.LEFT)
    btn_i_r3.pack(side=tkinter.LEFT)
    entry_r3.pack(side=tkinter.LEFT)
    btn_d_r3.pack(side=tkinter.RIGHT)
    frame_r3.pack(side=tkinter.TOP)

    lbl_g3.pack(side=tkinter.LEFT)
    btn_i_g3.pack(side=tkinter.LEFT)
    entry_g3.pack(side=tkinter.LEFT)
    btn_d_g3.pack(side=tkinter.RIGHT)
    frame_g3.pack(side=tkinter.TOP)

    lbl_b3.pack(side=tkinter.LEFT)
    btn_i_b3.pack(side=tkinter.LEFT)
    entry_b3.pack(side=tkinter.LEFT)
    btn_d_b3.pack(side=tkinter.RIGHT)
    frame_b3.pack(side=tkinter.TOP)

    frame_l3.pack(side=tkinter.LEFT)
    frame_c3.pack(side=tkinter.RIGHT)
    frame_h3.pack()

    lbl_c4.pack(side=tkinter.TOP)
    lbl_h4.pack(side=tkinter.TOP)

    lbl_r4.pack(side=tkinter.LEFT)
    btn_i_r4.pack(side=tkinter.LEFT)
    entry_r4.pack(side=tkinter.LEFT)
    btn_d_r4.pack(side=tkinter.RIGHT)
    frame_r4.pack(side=tkinter.TOP)

    lbl_g4.pack(side=tkinter.LEFT)
    btn_i_g4.pack(side=tkinter.LEFT)
    entry_g4.pack(side=tkinter.LEFT)
    btn_d_g4.pack(side=tkinter.RIGHT)
    frame_g4.pack(side=tkinter.TOP)

    lbl_b4.pack(side=tkinter.LEFT)
    btn_i_b4.pack(side=tkinter.LEFT)
    entry_b4.pack(side=tkinter.LEFT)
    btn_d_b4.pack(side=tkinter.RIGHT)
    frame_b4.pack(side=tkinter.TOP)

    frame_l4.pack(side=tkinter.LEFT)
    frame_c4.pack(side=tkinter.RIGHT)
    frame_h4.pack()

    frame_demo.pack(side=tkinter.LEFT, expand=True, fill=tkinter.BOTH)
    frame_colour_controls.pack(side=tkinter.RIGHT)

    print(f"Children: {[c for c in WINDOW.children]}")
    print(f"Children: {[type(c) for c in WINDOW.children]}")
    # for c in WINDOW.children:
    #     print(f"c: {c}")
    #     print(f"WINDOW[c]: {WINDOW[c]}")
    # tree = tkinter.ttk.Treeview(WINDOW)
    # for child in tree.get_children():
    #     print(tree.item(child)["values"])
    # tree.pack()

    # default starting values
    tv_r1.set(205)
    tv_g1.set(173)
    tv_b1.set(0)
    update_c1()
    tv_r2.set(16)
    tv_g2.set(78)
    tv_b2.set(139)
    update_c2()
    tv_r3.set(41)
    tv_g3.set(36)
    tv_b3.set(33)
    update_c3()
    tv_r4.set(173)
    tv_g4.set(255)
    tv_b4.set(47)
    update_c4()
    WINDOW.mainloop()

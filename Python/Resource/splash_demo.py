import tkinter

from tkinter_utility import *


def _draw_gradient(colour1, colour2, event=None):
    '''Draw the gradient'''
    print('''Draw the gradient''')
    can.delete("gradient")
    width = can.winfo_width()
    height = can.winfo_height()
    limit = width
    (r1, g1, b1) = can.winfo_rgb(colour1)
    (r2, g2, b2) = can.winfo_rgb(colour2)
    print(f"{width=}, {height=}, {limit=}")
    print(f"{r1=}, {g1=}, {b1=}")
    print(f"{r2=}, {g2=}, {b2=}")
    r_ratio = float(r2 - r1) / limit
    g_ratio = float(g2 - g1) / limit
    b_ratio = float(b2 - b1) / limit

    for i in range(limit):
        nr = int(r1 + (r_ratio * i))
        ng = int(g1 + (g_ratio * i))
        nb = int(b1 + (b_ratio * i))
        color = "#%4.4x%4.4x%4.4x" % (nr, ng, nb)
        can.create_line(i, 0, i, height, tags=("gradient",), fill=color)
    can.lower("gradient")


def draw_letter(char, x, y, w, h, fw=3):
    x1, y1, x2, y2 = x, y, x + w, y + h
    cx, cy = x1 + (w/2), y1 + (h/2)
    fw = fw + (0 if fw % 2 == 0 else 1)
    hfw = fw / 2
    match char:
        case "A":
            points = [
                cx - hfw, y1,  # top left
                cx + hfw, y1,  # top right
                cx + (w * 0.25), y2,  # bottom right outside
                cx + (w * 0.25) - fw, y2,  # bottom right inside
                cx + (w * 0.04), cy + fw,  # middle right inside bottom
                cx - (w * 0.035), cy + fw,  # middle left inside bottom
                cx - (w * 0.03), cy,  # middle left inside top
                cx + (w * 0.03), cy,  # middle right inside top
                cx, y1 + fw,  # middle inside top
                cx - (w * 0.25) + fw, y2,  # bottom left inside
                cx - (w * 0.25), y2,  # bottom left outside
            ]
        case "B":
            points = [
                x1, y2,  # bottom left outside
                x1, y1,  # top left outside
                cx, y1,  # center middle top
                x1 + (w * 0.65), y1 + (h * 0.25),  # middle of top round
                x1 + (w * 0.55), cy - hfw,  # middle of rounds
                x1 + (w * 0.72), y1 + (h * 0.75),  # middle of bottom round
                cx, y2,  # center middle bottom


                x1 + fw, y2,  # bottom round left outside
                x1 + fw, y2 - fw,  # bottom round left inside
                cx - hfw, y2 - fw,  # center middle bottom
                x1 + (w * 0.72) - fw, y1 + (h * 0.75),  # middle of bottom round
                x1 + fw, cy + hfw,  # middle of rounds
                x1 + (w * 0.55), cy - fw,  # middle of rounds
                x1 + (w * 0.65) - fw, y1 + (h * 0.25),  # middle of top round
                cx, y1 + fw,  # center middle top
                x1 + fw, y1 + fw,  # top left outside
                x1 + fw, y2,  # bottom left outside
            ]
        case _:
            raise ValueError("ERROR HERE")

    can.create_polygon(points, fill=Colour(CRIMSON_RED).hex_code)



if __name__ == '__main__':

    win = tkinter.Tk()
    win.geometry(calc_geometry_tl(500, 300))

    can = tkinter.Canvas(win, width=500, height=300, bg=Colour(GRAY_9).hex_code)
    # can.configure(bg=)
    # _draw_gradient(Colour(RED).hex_code, Colour(EMERALD).hex_code)
    can.pack()
    draw_letter("A", 50, 50, 150, 150, fw=16)
    draw_letter("B", 200, 50, 150, 150, fw=16)
    # can.bind("<Configure>", _draw_gradient(Colour(RED).hex_code, Colour(EMERALD).hex_code))

    win.after(3000, _draw_gradient, Colour(RED).hex_code, Colour(EMERALD).hex_code)
    win.mainloop()

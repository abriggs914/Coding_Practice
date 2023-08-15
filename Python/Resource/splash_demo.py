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


def test_cursor():
    import win32con
    import win32api
    import win32gui
    import ctypes
    import time
    import atexit

    # save system cursor, before changing it
    cursor = win32gui.LoadImage(0, 32512, win32con.IMAGE_CURSOR,
                                0, 0, win32con.LR_SHARED)
    save_system_cursor = ctypes.windll.user32.CopyImage(cursor, win32con.IMAGE_CURSOR,
                                                        0, 0, win32con.LR_COPYFROMRESOURCE)

    def restore_cursor():
        # restore the old cursor
        print("restore_cursor")
        ctypes.windll.user32.SetSystemCursor(save_system_cursor, 32512)
        ctypes.windll.user32.DestroyCursor(save_system_cursor)

    # Make sure cursor is restored at the end
    atexit.register(restore_cursor)

    # change system cursor
    cursor = win32gui.LoadImage(0, r"C:\Users\ABriggs\Downloads\sword.ico", win32con.IMAGE_CURSOR,
                                0, 0, win32con.LR_LOADFROMFILE)
    ctypes.windll.user32.SetSystemCursor(cursor, 32512)
    ctypes.windll.user32.DestroyCursor(cursor)

    time.sleep(9)
    exit()


def test_cursor2():
    import win32con
    import win32api
    import win32gui
    import ctypes
    import time
    import atexit

    def restore_cursor():
        # restore the old cursor
        print("restore_cursor")
        ctypes.windll.user32.SetSystemCursor(save_system_cursor, 32512)
        ctypes.windll.user32.DestroyCursor(save_system_cursor)

    try:

        # save system cursor, before changing it
        cursor = win32gui.LoadImage(0, 32512, win32con.IMAGE_CURSOR,
                                    0, 0, win32con.LR_SHARED)
        save_system_cursor = ctypes.windll.user32.CopyImage(cursor, win32con.IMAGE_CURSOR,
                                                            0, 0, win32con.LR_COPYFROMRESOURCE)

        # Make sure cursor is restored at the end
        atexit.register(restore_cursor)

        # change system cursor
        ico_x = win32api.GetSystemMetrics(win32con.SM_CXSMICON)
        ico_y = win32api.GetSystemMetrics(win32con.SM_CYSMICON)
        cursor = win32gui.LoadImage(
            # 0,
            None,
            r"C:\Users\ABriggs\Downloads\sword_18_23.ico",
            win32con.IMAGE_CURSOR,
            # ico_x,
            # ico_y,
            40,40,
            win32con.LR_LOADFROMFILE
        )

        ctypes.windll.user32.SetSystemCursor(cursor, 32512)
        ctypes.windll.user32.DestroyCursor(cursor)

        def click_change_colour(event=None):
            lbl.configure(background=random_colour(rgb=False))

        # time.sleep(9)
        win = tkinter.Tk()
        win.geometry(calc_geometry_tl(0.63, 0.42))

        tv_lbl, lbl = label_factory(
            win,
            "Hello World!",
            {
                "bg": random_colour(rgb=False),
                "width": 60,
                "height": 20,
                "font": ("Arial", 20)
            }
        )
        lbl.bind("<Button-1>", click_change_colour)
        lbl.pack()

        win.mainloop()

    except Exception as e:
        print(f"{e=}")
    finally:
        exit()


def test_cursor3():
    import win32con
    import win32api
    import win32gui
    import ctypes
    import time
    import atexit

    def restore_cursor():
        # restore the old cursor
        print("restore_cursor")
        ctypes.windll.user32.SetSystemCursor(save_system_cursor, 32512)
        ctypes.windll.user32.DestroyCursor(save_system_cursor)

    try:

        # save system cursor, before changing it
        cursor = win32gui.LoadImage(0, 32512, win32con.IMAGE_CURSOR,
                                    0, 0, win32con.LR_SHARED)
        save_system_cursor = ctypes.windll.user32.CopyImage(cursor, win32con.IMAGE_CURSOR,
                                                            0, 0, win32con.LR_COPYFROMRESOURCE)

        # Make sure cursor is restored at the end
        atexit.register(restore_cursor)

        # change system cursor
        cursor = win32gui.LoadImage(0, r"C:\Users\ABriggs\Downloads\sword_18_23.ico", win32con.IMAGE_CURSOR,
                                    0, 0, win32con.LR_LOADFROMFILE)

        ctypes.windll.user32.SetSystemCursor(cursor, 32512)
        ctypes.windll.user32.DestroyCursor(cursor)

        info = win32gui.GetCursorInfo()
        x_hotspot, y_hotspot = 9, 11  # Adjust hotspot coordinates
        cursor = win32gui.CreateIconFromResourceEx(
            info[2],
            info[3],
            True,
            0x00030000,
            x_hotspot,
            y_hotspot,
            win32con.LR_DEFAULTSIZE | win32con.LR_SHARED
        )
        ctypes.windll.user32.SetSystemCursor(cursor, 32512)
        ctypes.windll.user32.DestroyCursor(cursor)


        def click_change_colour(event=None):
            lbl.configure(background=random_colour(rgb=False))

        # time.sleep(9)
        win = tkinter.Tk()
        win.geometry(calc_geometry_tl(0.63, 0.42))

        tv_lbl, lbl = label_factory(win, "Hello World!", {"bg": random_colour(rgb=False)})
        lbl.bind("<Button-1>", click_change_colour)
        lbl.pack()

        win.mainloop()

    except Exception as e:
        print(f"{e=}")
    finally:
        exit()


if __name__ == '__main__':

    # win = tkinter.Tk()
    # win.geometry(calc_geometry_tl(500, 300))
    #
    # can = tkinter.Canvas(win, width=500, height=300, bg=Colour(GRAY_9).hex_code)
    # # can.configure(bg=)
    # # _draw_gradient(Colour(RED).hex_code, Colour(EMERALD).hex_code)
    # can.pack()
    # draw_letter("A", 50, 50, 150, 150, fw=16)
    # draw_letter("B", 200, 50, 150, 150, fw=16)
    # # can.bind("<Configure>", _draw_gradient(Colour(RED).hex_code, Colour(EMERALD).hex_code))
    #
    # win.after(3000, _draw_gradient, Colour(RED).hex_code, Colour(EMERALD).hex_code)
    # win.mainloop()

    # test_cursor()
    test_cursor2()

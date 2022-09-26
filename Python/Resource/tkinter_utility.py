import tkinter
from tkinter import ttk
from utility import grid_cells, clamp_rect, clamp, isnumber
from colour_utility import rgb_to_hex, font_foreground, Colour

#######################################################################################################################
#######################################################################################################################
#######################################################################################################################

VERSION = \
    """	
    General Utility Functions
    Version..............1.08
    Date...........2022-09-26
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


def is_tk_var(var_in, str_var=True, int_var=True, dbl_var=True, bol_var=True, var_var=True):
    valid = [v for c, v in zip(
        [str_var, int_var, dbl_var, bol_var, var_var],
        [tkinter.StringVar, tkinter.IntVar, tkinter.DoubleVar, tkinter.BooleanVar, tkinter.Variable]
    ) if c]
    return type(var_in) in valid


def entry_factory(master, tv_label=None, tv_entry=None, kwargs_label=None, kwargs_entry=None):
    """Return tkinter StringVar, Label, StringVar, Entry objects"""
    if tv_label is not None and tv_entry is not None:
        res_tv_label = tv_label if is_tk_var(tv_label) else tkinter.StringVar(master, value=tv_label)
        res_tv_entry = tv_entry if is_tk_var(tv_entry) else tkinter.StringVar(master, value=tv_entry)
    elif tv_label is not None:
        res_tv_label = tv_label if is_tk_var(tv_label) else tkinter.StringVar(master, value=tv_label)
        res_tv_entry = tkinter.StringVar(master)
    elif tv_entry is not None:
        res_tv_label = tkinter.StringVar(master)
        res_tv_entry = tv_entry if is_tk_var(tv_entry) else tkinter.StringVar(master, value=tv_entry)
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
    if is_tk_var(tv_btn):
        res_tv_btn = tv_btn
    else:
        if tv_btn is not None:
            res_tv_btn = tkinter.StringVar(master, value=tv_btn)
        else:
            res_tv_btn = tkinter.StringVar(master)
    res_btn = tkinter.Button(master, textvariable=res_tv_btn)
    if kwargs_btn is not None:
        res_btn = tkinter.Button(master, textvariable=res_tv_btn, **kwargs_btn)
    return res_tv_btn, res_btn


def combo_factory(master, tv_label=None, kwargs_label=None, tv_combo=None, kwargs_combo=None):
    """Return tkinter StringVar, Label, StringVar, Entry objects"""
    if tv_label is not None and tv_combo is not None:
        res_tv_label = tv_label if is_tk_var(tv_label) else tkinter.StringVar(master, value=tv_label)
        res_tv_combo = tv_combo if is_tk_var(tv_combo) else tkinter.StringVar(master, value=tv_combo)
    elif tv_label is not None:
        res_tv_label = tv_label if is_tk_var(tv_label) else tkinter.StringVar(master, value=tv_label)
        res_tv_combo = tkinter.StringVar(master)
    elif tv_combo is not None:
        res_tv_label = tkinter.StringVar(master)
        res_tv_combo = tv_combo if is_tk_var(tv_combo) else tkinter.StringVar(master, value=tv_combo)
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


def label_factory(master, tv_label=None, kwargs_label=None):
    """Return tkinter StringVar, label objects"""
    if is_tk_var(tv_label):
        res_tv_lbl = tv_label
    else:
        if tv_label is not None:
            res_tv_lbl = tkinter.StringVar(master, value=tv_label)
        else:
            res_tv_lbl = tkinter.StringVar(master)
    res_lbl = tkinter.Label(master, textvariable=res_tv_lbl)
    if kwargs_label is not None:
        res_lbl = tkinter.Label(master, textvariable=res_tv_lbl, **kwargs_label)
    return res_tv_lbl, res_lbl


def list_factory(master, tv_label=None, kwargs_label=None, tv_list=None, kwargs_list=None):
    """Return tkinter StringVar, Label, StringVar, Entry objects"""
    if not (isinstance(tv_list, list) or isinstance(tv_list, tuple) or isinstance(tv_list, dict) or isinstance(tv_list,
                                                                                                               set)):
        if tv_list:
            res_tv_list = list(tv_list)
        else:
            res_tv_list = []
    else:
        res_tv_list = tv_list

    res_tv_list = tkinter.Variable(master, res_tv_list)

    print(f"{tv_list=}, {res_tv_list=}")

    if tv_label is not None:
        res_tv_label = tv_label if is_tk_var(tv_label) else tkinter.StringVar(master, value=tv_label)
    else:
        res_tv_label = tkinter.StringVar(master)

        # res_tv_list = tv_list if is_tk_var(tv_list) else tkinter.StringVar(master, value=tv_list)
    # elif tv_label is not None:
    #     res_tv_label = tv_label if is_tk_var(tv_label) else tkinter.StringVar(master, value=tv_label)
    # res_tv_list = tkinter.StringVar(master)
    # elif tv_list is not None:
    #     res_tv_label = tkinter.StringVar(master)
    #     res_tv_list = tv_list if is_tk_var(tv_list) else tkinter.StringVar(master, value=tv_list)
    # else:
    #     res_tv_label = tkinter.StringVar(master)
    #     res_tv_list = tkinter.StringVar(master)

    if kwargs_label is not None and kwargs_list is not None:
        res_label = tkinter.Label(master, textvariable=res_tv_label, **kwargs_label)
        res_list = tkinter.Listbox(master, listvariable=res_tv_list, **kwargs_list)
    elif kwargs_label is not None:
        res_label = tkinter.Label(master, textvariable=res_tv_label, **kwargs_label)
        res_list = tkinter.Listbox(master, listvariable=res_tv_list)
    elif kwargs_list is not None:
        res_label = tkinter.Label(master, textvariable=res_tv_label)
        res_list = tkinter.Listbox(master, listvariable=res_tv_list, **kwargs_list)
    else:
        res_label = tkinter.Label(master, textvariable=res_tv_label)
        res_list = tkinter.Listbox(master, listvariable=res_tv_list)
    return res_tv_label, res_label, res_tv_list, res_list


def test_entry_factory():
    WIN = tkinter.Tk()
    WIDTH, HEIGHT = 500, 500
    WIN.geometry(f"{WIDTH}x{HEIGHT}")
    tv_1, lbl_1, tv_2, entry_1 = entry_factory(WIN, tv_label="This is a Label", tv_entry="This is an Entry",
                                               kwargs_entry={"background": "yellow"})
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


def test_list_factory():
    WIN = tkinter.Tk()
    WIN.geometry(f"500x500")
    a, b, c, d = list_factory(WIN, tv_label="This is a demo List:", tv_list=["hi", "there"])
    b.grid(row=1, column=1)
    d.grid(row=2, column=1)

    def update_f(*args):
        print(f"{args=}")
        selected_indices = d.curselection()
        print(f"{selected_indices=}")
        for i in selected_indices:
            print(f"\t{d.get(i)=}")

    d.bind('<<ListboxSelect>>', update_f)
    WIN.mainloop()


class Slider(tkinter.Frame):

    def __init__(self, master, minimum=0, maximum=100, steps=None, label_text=None, show_entry=True,
                 background="#252525", foreground="#e31234"):
        super(Slider, self).__init__(master)
        # TODO incorporate param 'steps' to have the slider jump between divisions of the sliding line.
        #  Could use this functionality to make a sliding combobox where values are discrete and could not be numbers.
        self.c_width, self.c_height = 400, 50
        self.minimum = minimum
        self.maximum = maximum
        self.value = tkinter.DoubleVar(self, value=self.half_point())
        self.background_colour = Colour(background)
        self.foreground_colour = Colour(foreground)
        self.label_text = label_text if label_text is not None else "UNNAMED"
        self.canvas = tkinter.Canvas(self, width=self.c_width, height=self.c_height,
                                     background=self.background_colour.hex_code)

        # bbox = self.canvas.bbox("all")
        # x1, y1, x2, y2 = bbox
        bbox = 0, 0, 400, 50
        x1, y1, x2, y2 = bbox
        w = x2 - x1
        h = y2 - y1
        dims = grid_cells(w, 1, h, 1, w * 0.85, h * 0.1)[0][0]
        # print(f"{dims=}")
        self.app_state = "idle"
        self.r_width = dims[2] - dims[0]
        self.r_height = dims[3] - dims[1]
        self.slider_dims = dims
        self.sliding_dims = [0, (self.c_height - self.r_height) / 2, self.c_width, self.c_height - self.r_height]
        self.s_width = self.sliding_dims[2] - self.sliding_dims[0]
        self.s_height = self.sliding_dims[3] - self.sliding_dims[1]
        self.slider = self.canvas.create_rectangle(*dims, fill=self.foreground_colour.hex_code)
        self.tv_label, self.label, self.tv_entry, self.entry = entry_factory(self, tv_label=self.label_text,
                                                                             tv_entry=self.value)

        self.canvas.tag_bind(self.slider, "<Button-1>", self.click_canvas)
        self.canvas.tag_bind(self.slider, "<Motion>", self.motion_canvas)
        self.canvas.tag_bind(self.slider, "<ButtonRelease-1>", self.release_canvas)

        self.entry.bind("<Return>", self.enter_submit)
        # self.tv_entry.trace_variable("w", self.update_entry)
        self.label.grid(row=1, column=1)
        self.entry.grid(row=1, column=2)
        self.canvas.grid(row=2, column=1, columnspan=2)

    def half_point(self):
        return ((self.maximum - self.minimum) / 2) + self.minimum

    def center_y(self):
        return self.c_height / 2

    def points_per_x(self):
        return (self.maximum - self.minimum) / self.c_width

    def x_per_point(self):
        return self.s_width / (self.maximum - self.minimum)

    def point_to_xy(self, point):
        def p(v, a, b):
            maab = max(a, b)
            miab = min(a, b)
            maaab = max(abs(a), abs(b))
            miaab = min(abs(a), abs(b))
            v_right = abs(abs(v) - abs(maab))
            denom_a = abs(maab - miab)
            denom_f = 1 if denom_a == 0 else denom_a
            inb1 = (1 - (v_right / denom_f))
            final = inb1
            # final = 100 * inb1
            print(f"{maab=}\n{miab=}\n{maaab=}\n{miaab=}\n{v_right=}\n{denom_a=}\n{denom_f=}\n{inb1=}\n{final=}\n")
            return final

        print(f"A {point=}")
        point = clamp(self.minimum, point, self.maximum)
        print(f"B {point=}")
        # point = 100 * point / abs(self.maximum - self.minimum)
        # xpp = self.x_per_point()
        # print(f"{point=}, {xpp=}, {point * xpp =}")
        # return xpp * point, self.center_y()
        return self.s_width * p(point, self.minimum, self.maximum), self.center_y()

    def xy_to_point(self, xy):
        # print(f"{xy=}")
        x, y = xy
        x = clamp(0, x, self.c_width)
        y = clamp(0, y, self.c_height)
        sw = self.slider_dims[2] - self.slider_dims[0]
        p = x / (self.c_width - sw)
        res = (p * (self.maximum - self.minimum)) + self.minimum
        # print(f"{p=}, {x=}, {y=}, {xy=}")
        return res

    def click_canvas(self, event):
        self.app_state = "dragging"

    def set_slider_pos(self, x, y):
        new_rect = [x - (self.r_width / 2), y - (self.r_height / 2), x + (self.r_width / 2),
                    y + (self.r_height / 2)]
        new_rect = clamp_rect(
            new_rect, self.sliding_dims, maintain_inner_dims=True
        )
        nx1, ny1, nx2, ny2 = new_rect
        self.slider_dims = new_rect
        self.canvas.moveto(self.slider, nx1, ny1)
        self.value.set(self.xy_to_point((nx1, nx2)))

    def motion_canvas(self, event):
        if self.app_state == "dragging":
            cx, cy = event.x, event.y
            self.set_slider_pos(cx, cy)

    def release_canvas(self, event):
        self.app_state = "idle"

    def enter_submit(self, *args):
        print(f"{self.minimum=}, {self.maximum=}, range= {self.maximum - self.minimum}")
        print(f"{args=}")
        point = float(self.tv_entry.get())
        x, y = self.point_to_xy(point)
        self.set_slider_pos(x, y)

    #
    # def set(self, value_in):
    #     x, y = self.point_to_xy(value_in)
    #     self.set_slider_pos(x, y)
    #
    # def (update_entry


class RGBSlider(tkinter.Frame):

    def __init__(self, master):
        super().__init__(master)

        self.colour = None

        self.slider_red = Slider(self, minimum=0, maximum=255)
        self.slider_green = Slider(self, minimum=0, maximum=255)
        self.slider_blue = Slider(self, minimum=0, maximum=255)

        self.tv_label_red, self.label_red, self.tv_entry_red, self.entry_red = entry_factory(self, tv_label="Red:",
                                                                                             tv_entry=self.slider_red.value)
        self.tv_label_green, self.label_green, self.tv_entry_green, self.entry_green = entry_factory(self,
                                                                                                     tv_label="Green:",
                                                                                                     tv_entry=self.slider_green.value)
        self.tv_label_blue, self.label_blue, self.tv_entry_blue, self.entry_blue = entry_factory(self, tv_label="Blue:",
                                                                                                 tv_entry=self.slider_blue.value)
        self.tv_label_res, self.label_res, self.tv_entry_res, self.entry_res = entry_factory(self, tv_label="Result:",
                                                                                             tv_entry="Sample Text #123.")

        self.slider_red.value.trace_variable("w", self.update_colour)
        self.slider_green.value.trace_variable("w", self.update_colour)
        self.slider_blue.value.trace_variable("w", self.update_colour)

        self.tv_entry_red.trace_variable("w", self.update_colour_entry)
        self.tv_entry_green.trace_variable("w", self.update_colour_entry)
        self.tv_entry_blue.trace_variable("w", self.update_colour_entry)

        self.label_red.grid(row=1, column=1)
        self.entry_red.grid(row=1, column=2)
        self.slider_red.grid(row=1, column=3)
        self.label_green.grid(row=2, column=1)
        self.entry_green.grid(row=2, column=2)
        self.slider_green.grid(row=2, column=3)
        self.label_blue.grid(row=3, column=1)
        self.entry_blue.grid(row=3, column=2)
        self.slider_blue.grid(row=3, column=3)
        self.label_res.grid(row=4, column=1)
        self.entry_res.grid(row=4, column=2)
        self.update_colour(None, None, None)

    def update_colour_entry(self, *args):
        print(f"update_colour_entry {args=}")
        # self.

    def update_colour(self, var_name, index, mode):
        print(f"update_colour")
        try:
            r = self.slider_red.value.get()
            r_flag = False
        except tkinter.TclError as te:
            # if self.slider_red.value != "":
            #     self.slider_red.value.set(0)
            # r = self.slider_red.value.get()
            r = 0
            r_flag = True
            print(f"{te=}")

        try:
            g = self.slider_green.value.get()
            g_flag = False
        except tkinter.TclError as te:
            # if self.slider_green.value != "":
            #     self.slider_green.value.set(0)
            # g = self.slider_green.value.get()
            g = 0
            g_flag = True
            print(f"{te=}")

        try:
            b = self.slider_blue.value.get()
            b_flag = False
        except tkinter.TclError as te:
            # if self.slider_blue.value != "":
            #     self.slider_blue.value.set(0)
            # b = self.slider_blue.value.get()
            b = 0
            b_flag = True
            print(f"{te=}")

        print(f"{r=} {g=}, {b=}")
        if not isnumber(r) or r < 0 or r > 255 or r_flag:
            self.entry_red.configure(foreground="red")
        else:
            self.entry_red.configure(foreground="black")
        if not isnumber(g) or g < 0 or g > 255 or g_flag:
            self.entry_green.configure(foreground="red")
        else:
            self.entry_green.configure(foreground="black")
        if not isnumber(b) or b < 0 or b > 255 or b_flag:
            self.entry_blue.configure(foreground="red")
        else:
            self.entry_blue.configure(foreground="black")

        try:
            self.colour = Colour(r, g, b)
        except TypeError as te:
            self.colour = Colour(125, 125, 125)
            print(f"{te=}")

        h = self.colour.hex_code
        self.entry_res.config(background=h, foreground=font_foreground(h, rgb=False))


# https://stackoverflow.com/questions/70147814/hint-entry-widget-tkinter
class EntryWithPlaceholder(tkinter.Entry):
    def __init__(self, master=None, font=None, placeholder="PLACEHOLDER", color='grey', textvariable=None):
        super().__init__()

        self.placeholder = placeholder
        self.placeholder_color = color
        self.default_fg_color = self['fg']
        self['textvariable'] = textvariable
        self.bind("<FocusIn>", self.foc_in)
        self.bind("<FocusOut>", self.foc_out)

        self.put_placeholder()

    def put_placeholder(self):
        self.insert(0, self.placeholder)
        self['fg'] = self.placeholder_color

    def foc_in(self, *args):
        if self['fg'] == self.placeholder_color:
            self['show'] = '*'
            self.delete('0', 'end')
            self['fg'] = self.default_fg_color

    def foc_out(self, *args):
        if not self.get():
            self.put_placeholder()
            self['show'] = ''


if __name__ == '__main__':
    print('PyCharm')

    # test_entry_factory()
    # test_combo_1()
    # test_combo_factory()
    test_list_factory()

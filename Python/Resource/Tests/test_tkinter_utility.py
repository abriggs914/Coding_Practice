import random

from tkinter_utility import *


class DemoWindow(tkinter.Tk):
    def __init__(self):
        super().__init__()
        self.title("Demo Window")
        self.geometry("300x300")

        self.custom_text = TextWithVar(self)
        # self.custom_text.pack(fill=tkinter.BOTH, expand=True)
        self.custom_text.pack()

        self.tv_btn, self.btn = button_factory(self, tv_btn="click me", kwargs_btn={"command": self.click})

        self.btn.pack()

    def click(self, *args):
        word = "".join([chr(random.randint(ord('a'), ord('z'))) for i in range(10)])
        print(f"click!, {word=}")
        self.custom_text.text.set(f"WORD='{word}'")

        # text_label = tk.Label(self, textvariable=custom_text.text)
        # text_label.pack()


class Example(tkinter.Frame):
    def __init__(self, parent):
        tkinter.Frame.__init__(self, parent)

        self.textvar = tkinter.StringVar()
        self.textvar.set("Hello, world!")

        # create an cell_is_entry widget and a text widget that
        # share a textvariable; typing in one should update
        # the other
        self.entry = tkinter.Entry(self, textvariable=self.textvar)
        self.text = TextWithVar_DON(self, textvariable=self.textvar,
                                    borderwidth=1, relief="sunken",
                                    background="bisque")

        self.entry.pack(side="top", fill="x", expand=True)
        self.text.pack(side="top", fill="both", expand=True)


# def multi_combo_factory(master, data, tv_label=None, kwargs_label=None, tv_combo=None, kwargs_combo=None):
#     assert isinstance(data, pandas.DataFrame), f"Error param 'data' must be an instance of a pandas.DataFrame, got '{type(data)}'."
#     assert False if (kwargs_combo and ("values" in kwargs_combo)) else True, f"Cannot pass values as a keyword argument here. Pass all data in the data param as a pandas.DataFrame."
#
#     """Return tkinter StringVar, Label, StringVar, Entry objects"""
#     if tv_label is not None and tv_combo is not None:
#         res_tv_label = tv_label if is_tk_var(tv_label) else tkinter.StringVar(master, value=tv_label)
#         res_tv_entry = tv_combo if is_tk_var(tv_combo) else tkinter.StringVar(master, value=tv_combo)
#     elif tv_label is not None:
#         res_tv_label = tv_label if is_tk_var(tv_label) else tkinter.StringVar(master, value=tv_label)
#         res_tv_entry = tkinter.StringVar(master)
#     elif tv_combo is not None:
#         res_tv_label = tkinter.StringVar(master)
#         res_tv_entry = tv_combo if is_tk_var(tv_combo) else tkinter.StringVar(master, value=tv_combo)
#     else:
#         res_tv_label = tkinter.StringVar(master)
#         res_tv_entry = tkinter.StringVar(master)
#
#     if kwargs_label is not None and kwargs_combo is not None:
#         res_label = tkinter.Label(master, textvariable=res_tv_label, **kwargs_label)
#         # res_combo = ttk.Combobox(master, textvariable=res_tv_combo, **kwargs_combo)
#     elif kwargs_label is not None:
#         res_label = tkinter.Label(master, textvariable=res_tv_label, **kwargs_label)
#         # res_combo = ttk.Combobox(master, textvariable=res_tv_combo)
#     elif kwargs_combo is not None:
#         res_label = tkinter.Label(master, textvariable=res_tv_label)
#         # res_combo = ttk.Combobox(master, textvariable=res_tv_combo, **kwargs_combo)
#     else:
#         res_label = tkinter.Label(master, textvariable=res_tv_label)
#         # res_combo = ttk.Combobox(master, textvariable=res_tv_combo)
#
#     tv1 = treeview_factory(master, data)
#
#     def click_canvas_dropdown_button(event):
#         tv1
#
#     res_entry = tkinter.Entry(master, textvariable=res_tv_entry)
#     res_canvas = tkinter.Canvas(master, width_canvas=20, height_canvas=20, background=rgb_to_hex("GRAY_62"))
#     res_canvas.create_line(11, 6, 11, 19, arrow=tkinter.LAST, arrowshape=(12, 12, 9))
#     res_canvas.bind("<Button-1>", click_canvas_dropdown_button)
#
#     return (res_tv_label, res_label), (res_tv_entry, res_entry), res_canvas, tv1


#######################################################################################################################
#######################################################################################################################
#######################################################################################################################


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


def test_radio_factory():
    WIN = tkinter.Tk()
    WIN.geometry(f"500x500")

    def update_radio_choice(*args):
        print(f"{a.get()=}")

    buttons_list = [
        "a",
        "b",
        "c",
        "quit"
    ]
    a, b, c = radio_factory(WIN, buttons_list)

    for btn in c:
        btn.pack()

    a.trace_variable("w", update_radio_choice)

    WIN.mainloop()


def test_treeview_factory_1():
    WIN = tkinter.Tk()
    WIN.geometry(f"500x500")

    df = pandas.DataFrame({
        "species": ["Cat", "Dog", "Fish", "Parrot"]
        , "name": ["Tim", "Tam", "Tom", "Tum"]
        , "dob": [datetime.datetime(2000, 2, 13), datetime.datetime(2016, 4, 9), datetime.datetime(2010, 6, 7),
                  datetime.datetime(2005, 8, 31)]
    })

    print(f"df:\n\n{df}")

    tv_label, label, treeview, scrollbar_x, scrollbar_y = treeview_factory(WIN, df)
    tv_label.set("I forgot to pass a title! - no worries.")
    label.pack()
    treeview.pack()

    WIN.mainloop()


def test_treeview_factory_2():
    WIN = tkinter.Tk()
    WIN.geometry(f"500x500")

    df = pandas.DataFrame({
        "species": ["Cat", "Dog", "Fish", "Parrot"]
        , "name": ["Tim", "Tam", "Tom", "Tum"]
        , "invisible_col": [True, True, True, False]
        , "dob": [datetime.datetime(2000, 2, 13), datetime.datetime(2016, 4, 9), datetime.datetime(2010, 6, 7),
                  datetime.datetime(2005, 8, 31)]
    })

    print(f"df:\n\n{df}")

    tv_label, label, treeview, scrollbar_x, scrollbar_y = treeview_factory(
        WIN,
        df,
        viewable_column_names=["species", "name", "dob"],
        viewable_column_widths=[300, 125, 200]
    )
    tv_label.set("I forgot to pass a title! - no worries.")
    label.pack(side=tkinter.TOP)
    scrollbar_y.pack(side=tkinter.RIGHT, anchor="e", fill="y")
    treeview.pack(side=tkinter.TOP)
    scrollbar_x.pack(side=tkinter.BOTTOM)

    WIN.mainloop()


def test_treeview_factory_3():
    WIN = tkinter.Tk()
    WIN.geometry(f"500x500")

    df = pandas.DataFrame({
        "species": ["Cat", "Dog", "Fish", "Parrot"]
        , "name": ["Tim", "Tam", "Tom", "Tum"]
        , "invisible_col": [True, True, True, False]
        , "dob": [datetime.datetime(2000, 2, 13), datetime.datetime(2016, 4, 9), datetime.datetime(2010, 6, 7),
                  datetime.datetime(2005, 8, 31)]
    })

    namer = alpha_seq(4, numbers_instead=True)

    for i in range(df.shape[0]):
        next(namer)

    def gen_random_entry():
        return [
            str(random.randint(0, 25)),
            str(random.randint(0, 25)),
            # random.choice([True, False]),
            random_date(start_year=2020, end_year=2024)
        ]

    def insert_new_entry(index=tkinter.END):
        data = gen_random_entry()
        iid = int(next(namer))
        text = f"NEW TEXT"
        treeview.insert("", index, iid=iid, text=text, values=data)

    def delete_entry():
        selection = treeview.selection()
        print(f"{selection=}")
        if selection:
            # delete the selected entries
            # row_id = treeview.focus()  # return only 1
            for row_id in selection:
                print(f"{row_id=}")
                treeview.delete(row_id)

    print(f"df:\n\n{df}")

    tv_label, label, treeview, scrollbar_x, scrollbar_y = treeview_factory(
        WIN,
        df,
        viewable_column_names=["species", "name", "dob"],
        viewable_column_widths=[300, 125, 200]
    )
    tv_label.set("I forgot to pass a title! - no worries.")
    label.pack(side=tkinter.TOP)
    scrollbar_y.pack(side=tkinter.RIGHT, anchor="e", fill="y")
    treeview.pack(side=tkinter.TOP)
    scrollbar_x.pack(side=tkinter.BOTTOM)

    tv_btn1, btn1 = button_factory(WIN, tv_btn="new cell_is_entry", kwargs_btn={"command": insert_new_entry})
    tv_btn2, btn2 = button_factory(WIN, tv_btn="del cell_is_entry", kwargs_btn={"command": delete_entry})
    btn1.pack()
    btn2.pack()

    WIN.mainloop()


def test_treeview_factory_4():
    WIN = tkinter.Tk()
    WIN.geometry(f"500x500")

    df = pandas.DataFrame({
        "species": ["Cat", "Dog", "Fish", "Parrot"]
        , "name": ["Tim", "Tam", "Tom", "Tum"]
        , "invisible_col": [True, True, True, False]
        , "dob": [datetime.datetime(2000, 2, 13), datetime.datetime(2016, 4, 9), datetime.datetime(2010, 6, 7),
                  datetime.datetime(2005, 8, 31)]
        , "# lives": [9, 1, 1, 1]
    })

    df["age(D)"] = (datetime.datetime.now() - df["dob"]).tolist()[0].days

    print(f"df:\n\n{df}")

    def avg(*lst):
        # print(f"average of {lst=}, {type(lst)=}")
        return utility.avg(*lst)

    def show_column_info():
        for k, v in treeview_controller.aggregate_data.items():
            if k not in treeview_controller.viewable_column_names:
                try:
                    if not k.startswith("#"):
                        raise Exception(
                            f"Error aggregate data key '{k}' not found in the list of visible column names.")
                    elif 0 > (num := int(k[1:])) > len(treeview_controller.viewable_column_names):
                        raise Exception(f"Error aggregate data key '{k}' is out of range.")
                    else:
                        key = treeview_controller.viewable_column_names[num]
                except ValueError as ve:
                    raise ValueError(f"Error aggregate data key '{k}' not found in the list of visible column names.")
            else:
                key = k

            print(f"{v=}")
            print(f"{treeview_controller.treeview.column(key)=}, {type(treeview_controller.treeview.column(key))=}")
            print(f"{treeview_controller.treeview.heading(key)=}, {type(treeview_controller.treeview.heading(key))=}")

    treeview_controller = treeview_factory(
        WIN,
        df,
        viewable_column_names=["species", "name", "age(D)", "# lives", "dob"],
        viewable_column_widths=[300, 125, 75, 75, 200],
        aggregate_data={
            "#1": min,
            "species": max,
            "age(D)": avg,
            "# lives": avg,
            "dob": min
        }
        # aggregate_data={
        #     "#1": min,
        #     "species": max,
        #     "age(D)": avg,
        #     "# lives": avg
        # }
    )
    frame, \
    tv_label, \
    label, \
    treeview, \
    scrollbar_x, \
    scrollbar_y, \
    insert_btn_data, \
    delete_btn_data, \
    aggregate_objects \
        = treeview_controller.get_objects()
    tv_label.set("I forgot to pass a title! - no worries.")
    label.grid()
    scrollbar_y.grid(sticky="ns")
    treeview.grid()
    scrollbar_x.grid(sticky="ew")

    tv_button_insert_item, button_insert_item = insert_btn_data
    tv_button_delete_item, button_delete_item = delete_btn_data

    frame.grid()
    for i, aggregate_data in enumerate(aggregate_objects):
        # print(f"\t{i=}, {aggregate_data=}")
        if i == 0:
            # first is always the frame
            aggregate_data.grid()
        else:
            tv, entry, x1x2 = aggregate_data
            entry.pack(side=tkinter.LEFT)
            x1, x2 = x1x2
            # print(f"{x1=}")
            # cell_is_entry.place(x=x1, y=500)

    button_insert_item.grid()
    button_delete_item.grid()

    tv_button_column_info, button_column_info = button_factory(
        WIN,
        tv_btn="column info",
        kwargs_btn={
            "command": show_column_info
        }
    )
    button_column_info.grid()

    WIN.mainloop()


def test_messagebox():
    root = tkinter.Tk()

    def func():
        a = CustomMessageBox(msg='Hello I m your multiline message',
                             title='Hello World',
                             b1='Button 1',
                             b2='Button 2',
                             )
        print(a.choice)

    tkinter.Button(root, text='Click Me', command=func).pack()

    root.mainloop()


def test_apply_state_1():
    root = tkinter.Tk()
    root.geometry("500x500")
    a = tkinter.Frame(root, width=450, background=random_colour(rgb=False))
    b = tkinter.Frame(a, width=400, background=random_colour(rgb=False))
    c = tkinter.Frame(b, width=350, background=random_colour(rgb=False))
    d = tkinter.Frame(c, width=300, background=random_colour(rgb=False))
    e = tkinter.Frame(d, width=250, background=random_colour(rgb=False))

    f = tkinter.StringVar(root, value="a")
    g = tkinter.StringVar(root, value="b")
    h = tkinter.StringVar(root, value="c")
    i = tkinter.StringVar(root, value="dictionary")
    j = tkinter.StringVar(root, value="e")

    k = tkinter.Entry(a, textvariable=f)
    l = tkinter.Entry(b, textvariable=g)
    m = tkinter.Entry(c, textvariable=h)
    n = tkinter.Entry(d, textvariable=i)
    o = tkinter.Entry(e, textvariable=j)

    a.pack()
    k.pack()
    b.pack()
    l.pack()
    c.pack()
    m.pack()
    d.pack()
    n.pack()
    e.pack()
    o.pack()

    apply_state(c, "disabled")
    # apply_state(c, "disabled", "down")
    root.mainloop()


def test_apply_state_2():
    root = tkinter.Tk()
    root.geometry("500x500")

    namer_1 = alpha_seq(1000, prefix="a_")
    namer_2 = alpha_seq(1000, prefix="b_")

    a_s = tkinter.StringVar(root, value="g", name=next(namer_1))
    a_t = tkinter.StringVar(root, value="h", name=next(namer_1))
    a_u = tkinter.StringVar(root, value="i", name=next(namer_1))
    a_v = tkinter.StringVar(root, value="j", name=next(namer_1))
    a_w = tkinter.StringVar(root, value="n", name=next(namer_1))
    a_x = tkinter.StringVar(root, value="o", name=next(namer_1))
    a_y = tkinter.StringVar(root, value="p", name=next(namer_1))
    a_z = tkinter.StringVar(root, value="q", name=next(namer_1))

    a_a = tkinter.Frame(root, width=480, background=random_colour(rgb=False), name=next(namer_2))
    a_b = tkinter.Frame(a_a, width=470, background=random_colour(rgb=False), name=next(namer_2))
    a_c = tkinter.Frame(a_a, width=460, background=random_colour(rgb=False), name=next(namer_2))
    a_d = tkinter.Frame(a_b, width=450, background=random_colour(rgb=False), name=next(namer_2))
    a_e = tkinter.Frame(a_b, width=440, background=random_colour(rgb=False), name=next(namer_2))
    a_f = tkinter.Frame(a_c, width=430, background=random_colour(rgb=False), name=next(namer_2))
    a_g = tkinter.Entry(a_d, textvariable=a_s, width=100, name=next(namer_2))
    a_h = tkinter.Entry(a_d, textvariable=a_t, width=90, name=next(namer_2))
    a_i = tkinter.Entry(a_e, textvariable=a_u, width=80, name=next(namer_2))
    a_j = tkinter.Entry(a_f, textvariable=a_v, width=70, name=next(namer_2))
    a_k = tkinter.Frame(a_f, width=420, background=random_colour(rgb=False), name=next(namer_2))
    a_l = tkinter.Frame(a_k, width=410, background=random_colour(rgb=False), name=next(namer_2))
    a_m = tkinter.Frame(a_l, width=400, background=random_colour(rgb=False), name=next(namer_2))
    a_n = tkinter.Entry(a_l, textvariable=a_w, width=60, name=next(namer_2))
    a_o = tkinter.Entry(a_l, textvariable=a_x, width=50, name=next(namer_2))
    a_p = tkinter.Entry(a_m, textvariable=a_y, width=50, name=next(namer_2))
    a_q = tkinter.Entry(a_m, textvariable=a_z, width=40, name=next(namer_2))

    a_a.pack()
    a_b.pack()
    a_c.pack()
    a_d.pack()
    a_e.pack()
    a_f.pack()
    a_g.pack()
    a_h.pack()
    a_i.pack()
    a_j.pack()
    a_k.pack()
    a_l.pack()
    a_m.pack()
    a_n.pack()
    a_o.pack()
    a_p.pack()
    a_q.pack()

    # apply_state(a_j, "disabled")
    # apply_state(a_j, "disabled", "down")

    # apply_state(a_k, "disabled")
    apply_state(a_k, "disabled", "down")
    root.mainloop()


def test_apply_state_3():
    root = tkinter.Tk()
    root.geometry("500x500")

    namer_1 = alpha_seq(1000, prefix="a_")
    namer_2 = alpha_seq(1000, prefix="b_")

    a_v = tkinter.StringVar(root, value="g", name=next(namer_1))
    a_w = tkinter.StringVar(root, value="h", name=next(namer_1))
    a_x = tkinter.StringVar(root, value="i", name=next(namer_1))
    a_y = tkinter.StringVar(root, value="j", name=next(namer_1))
    a_z = tkinter.StringVar(root, value="n", name=next(namer_1))
    b_a = tkinter.StringVar(root, value="o", name=next(namer_1))
    b_b = tkinter.StringVar(root, value="p", name=next(namer_1))
    b_c = tkinter.StringVar(root, value="q", name=next(namer_1))
    b_d = tkinter.StringVar(root, value="r", name=next(namer_1))
    b_e = tkinter.StringVar(root, value="s", name=next(namer_1))
    b_f = tkinter.StringVar(root, value="t", name=next(namer_1))
    b_g = tkinter.StringVar(root, value="u", name=next(namer_1))

    a_a = tkinter.Frame(root, width=480, background=random_colour(rgb=False), name=next(namer_2))
    a_b = tkinter.Frame(a_a, width=470, background=random_colour(rgb=False), name=next(namer_2))
    a_c = tkinter.Frame(a_a, width=460, background=random_colour(rgb=False), name=next(namer_2))
    a_d = tkinter.Frame(a_b, width=450, background=random_colour(rgb=False), name=next(namer_2))
    a_e = tkinter.Frame(a_b, width=440, background=random_colour(rgb=False), name=next(namer_2))
    a_f = tkinter.Frame(a_c, width=430, background=random_colour(rgb=False), name=next(namer_2))
    a_g = tkinter.Entry(a_d, textvariable=a_v, width=100, name=next(namer_2))
    a_h = tkinter.Entry(a_d, textvariable=a_w, width=90, name=next(namer_2))
    a_i = tkinter.Entry(a_e, textvariable=a_x, width=80, name=next(namer_2))
    a_j = tkinter.Entry(a_f, textvariable=a_y, width=70, name=next(namer_2))
    a_k = tkinter.Frame(a_f, width=420, background=random_colour(rgb=False), name=next(namer_2))
    a_l = tkinter.Frame(a_k, width=410, background=random_colour(rgb=False), name=next(namer_2))
    a_m = tkinter.Frame(a_l, width=400, background=random_colour(rgb=False), name=next(namer_2))
    a_n = tkinter.Entry(a_l, textvariable=a_z, width=60, name=next(namer_2))
    a_o = tkinter.Entry(a_l, textvariable=b_a, width=50, name=next(namer_2))
    a_p = tkinter.Entry(a_m, textvariable=b_b, width=50, name=next(namer_2))
    a_q = tkinter.Entry(a_m, textvariable=b_c, width=40, name=next(namer_2))

    a_r = tkinter.Entry(a_a, textvariable=b_d, width=35, name=next(namer_2))
    a_s = tkinter.Entry(a_b, textvariable=b_e, width=35, name=next(namer_2))
    a_t = tkinter.Entry(a_c, textvariable=b_f, width=35, name=next(namer_2))
    a_u = tkinter.Entry(a_k, textvariable=b_g, width=35, name=next(namer_2))

    a_a.pack()
    a_b.pack()
    a_r.pack()
    a_c.pack()
    a_d.pack()
    a_e.pack()
    a_f.pack()
    a_g.pack()
    a_h.pack()
    a_i.pack()
    a_s.pack()
    a_j.pack()
    a_k.pack()
    a_l.pack()
    a_m.pack()
    a_n.pack()
    a_o.pack()
    a_p.pack()
    a_q.pack()
    a_u.pack()
    a_t.pack()

    # apply_state(a_j, "disabled", exclude_self=True)
    apply_state(a_j, "disabled", exclude_self=False)
    # apply_state(a_j, "disabled", "down")

    # apply_state(a_k, "disabled", "up")
    # apply_state(a_k, "disabled", "down")
    root.mainloop()


def test_multi_combo_factory():
    WIN = tkinter.Tk()
    WIN.geometry(f"800x800")
    WIN.title("Select Start Date")

    data = pandas.DataFrame({
        "ColA": list(range(5)),
        "ColB": list(range(6, 11)),
        "ColC": list(range(11, 16)),
        "ColD": list(range(16, 21))
    })

    print(f"{data.to_html()=}")

    mc = MultiComboBox(
        WIN,
        data,
        limit_to_list=False
    )

    def dd():
        print(f"\n\nAbout to delete:\n")
        mc.delete_item(value=14)

    mc.add_new_item(val=1000, col="ColA", rest_values=[-1, False, "0"])
    mc.add_new_item(val=1000, col="ColA", rest_values={"ColB": -1, "ColC": False, "ColD": "0"})
    WIN.after(5000, dd)
    # mc.delete_item(value=14)
    # mc.delete_item(iid=0)

    # a, c, dictionary, b = multi_combo_factory(WIN, data, tv_label="Multi-ComboBox Demo")
    #
    # a1, a2 = a
    # c1, c2 = c
    #
    # tv1_fact, tv1_tv_label, tv1_label, tv1_treeview, tv1_scrollbar_x, tv1_scrollbar_y, \
    # (tv1_tv_button_new_item, tv1_button_new_item), (tv1_tv_button_delete_item, tv1_button_delete_item), \
    # tv1_aggregate_objects = b.get_objects()
    #
    # a2.grid()
    # c2.grid(row=1, column=0)
    # dictionary.grid(row=1, column=1)
    #
    # tv1_fact.grid()
    # tv1_label.grid(row=0)
    # tv1_scrollbar_x.grid(row=3, sticky="ew")
    # tv1_treeview.grid(row=1, column=0)
    # tv1_scrollbar_y.grid(row=1, column=1, sticky="ns")
    # for i, data in enumerate(tv1_aggregate_objects):
    #     if i > 0:
    #         tv, cell_is_entry, x1x2 = data
    #         # print(f"{i=}, {tv.get()=}")
    #         cell_is_entry.grid(row=0, column=i)
    #     else:
    #         data.grid(row=2)

    # dealers = ["A", "B", "C"]
    # colours = ["red", "blue", "green", "custom", "none"]
    # sv_lbl_1, lbl_1, sv_cb_1, cb_1 = combo_factory(WIN, tv_label="Dealer", kwargs_combo={"values": dealers})
    # sv_lbl_2, lbl_2, sv_cb_2, cb_2 = combo_factory(WIN, tv_label="Colour", kwargs_combo={"values": colours})
    #
    # def new_dealer(var_name, index, game_mode):
    #     dictionary = sv_cb_1.get()
    #     c = sv_cb_2.get()
    #     if c and dictionary:
    #         if c not in ["custom", "none"]:
    #             print(f"Setting {dictionary=} to {c=}")
    #         elif c == "custom":
    #             print(f"custom colour from dealer {dictionary=}")
    #         else:
    #             print(f"removing colour from dealer {dictionary=}")
    #
    # def new_colour(var_name, index, game_mode):
    #     dictionary = sv_cb_1.get()
    #     c = sv_cb_2.get()
    #     if c and dictionary:
    #         if c not in ["custom", "none"]:
    #             print(f"Setting {dictionary=} to {c=}")
    #         elif c == "custom":
    #             print(f"custom colour from dealer {dictionary=}")
    #         else:
    #             print(f"removing colour from dealer {dictionary=}")
    #
    # sv_cb_1.trace_variable("w", new_dealer)
    # sv_cb_2.trace_variable("w", new_colour)
    # lbl_1.grid(row=1, column=1)
    # lbl_2.grid(row=2, column=1)
    # cb_1.grid(row=1, column=2)
    # cb_2.grid(row=2, column=2)
    WIN.mainloop()


def test_arrow_button():
    win = tkinter.Tk()
    win.geometry(f"600x600")
    win.title("test_arrow_button")

    modes = ["nw", "n", "ne", "w", None, "e", "sw", "s", "se"]
    canvases = []
    w, h = 20, 20
    for i, mode in enumerate(modes):
        if mode:
            canvases.append(ab := ArrowButton(win, mode=mode, name=f"{i=}, {mode=}"))
            ab.grid(row=i // 3, column=i % 3)
        else:
            canvases.append(c := tkinter.Canvas(win, width=w, height=h))
            c.grid(row=i // 3, column=i % 3)

    win.mainloop()


def test_demo_window():
    app = DemoWindow()
    app.mainloop()


def test_test_factory():
    win = tkinter.Tk()
    win.geometry("600x600")

    t = tkinter.Text(win,)

    win.mainloop()


def test_checkbox_factory():
    win = tkinter.Tk()
    win.geometry("600x600")

    a, b = checkbox_factory(
        win,
        ["a", "b", "c"]
    )

    for _ in b:
        _.pack()

    win.mainloop()


if __name__ == '__main__':
    print('PyCharm')

    # test_entry_factory()
    # test_combo_1()
    # test_combo_factory()
    # test_list_factory()
    # test_messagebox()
    # test_radio_factory()
    # test_treeview_factory_1()
    # test_treeview_factory_2()
    # test_treeview_factory_3()
    # test_treeview_factory_4()
    # test_apply_state_1()
    # test_apply_state_3()
    test_multi_combo_factory()
    # test_arrow_button()


    # root = tkinter.Tk()
    # Example(root).pack(fill="both", expand=True)
    # root.mainloop()

    # test_demo_window()

    # test_checkbox_factory()

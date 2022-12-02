import datetime
import random
import tkinter

import pandas

from typing import Literal

import utility
from utility import grid_cells, clamp_rect, clamp, isnumber, alpha_seq, random_date
from colour_utility import rgb_to_hex, font_foreground, Colour, random_colour
from tkinter import ttk, messagebox

#######################################################################################################################
#######################################################################################################################
#######################################################################################################################

VERSION = \
    """	
    General Utility Functions
    Version..............1.21
    Date...........2022-12-02
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


def top_most_tk(obj):
    assert isinstance(obj, tkinter.Tk) or isinstance(obj, tkinter.Widget) or isinstance(obj,
                                                                                        tkinter.Toplevel), f"Error, function requires an instance of tkinter Tk or tkinter Widget Got '{type(obj)=}'"
    if isinstance(obj, tkinter.Tk):
        return obj
    else:
        return top_most_tk(obj.master)


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


def radio_factory(master, buttons, default_value=None, kwargs_buttons=None):
    if isinstance(buttons, list) or isinstance(buttons, tuple) and buttons:
        if default_value is not None:
            if is_tk_var(default_value):
                var = default_value
            else:
                var = tkinter.StringVar(default_value)
        else:
            var = tkinter.StringVar(master, buttons[0])

        # print(f"CREATED {var.get()=}")

        r_buttons = []
        tv_vars = []
        for btn in buttons:
            if is_tk_var(btn):
                tv_var = btn
            else:
                tv_var = tkinter.StringVar(master, value=btn)
            tv_vars.append(tv_var)
            if kwargs_buttons is not None:
                print(f"WARNING kwargs param is applied to each radio button")
                r_buttons.append(
                    tkinter.Radiobutton(master, variable=var, textvariable=tv_var, **kwargs_buttons, value=btn))
            else:
                r_buttons.append(tkinter.Radiobutton(master, variable=var, textvariable=tv_var, value=btn))

        return var, tv_vars, r_buttons
    else:
        raise Exception("Error, must pass a list of buttons.")

        # tv_sort_direction = StringVar(WIN, value="descending")
        # tv_sort_dir_a = StringVar(WIN, value="ascending")
        # tv_sort_dir_d = StringVar(WIN, value="descending")
        # rb_sda = Radiobutton(frame_rb_group_3, variable=tv_sort_direction, value="ascending", textvariable=tv_sort_dir_a)
        # rb_sdd = Radiobutton(frame_rb_group_3, variable=tv_sort_direction, value="descending", textvariable=tv_sort_dir_d)


class TreeviewExt(ttk.Treeview):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def treeview_sort_column(self, col, reverse):
        l = [(self.set(k, col), k) for k in self.get_children('')]
        l.sort(reverse=reverse)

        # rearrange items in sorted positions
        for index, (val, k) in enumerate(l):
            self.move(k, '', index)

        # reverse sort next time
        self.heading(col, command=lambda: \
            self.treeview_sort_column(col, not reverse))


class TreeviewController(tkinter.Frame):

    # choose which columns should have totals
    # add button
    # delete button
    def __init__(
            self,
            master,
            df,
            viewable_column_names=None,
            viewable_column_widths=None,
            tv_label=None,
            kwargs_label=None,
            kwargs_treeview=None,
            default_col_width=100,
            include_scroll_x=True,
            include_scroll_y=True,
            text_prefix="B_",
            iid_prefix="C_",
            aggregate_data=None,
            *args,
            **kwargs
    ):
        """Create a frame with controls to interact with a ttk treeview widget.
        Insert and Delete functions have been pre-defined, in order to change this to your own callbacks,
        use self.button_insert_item.configure(command=<YOUR_CALLBACK_HERE>).

        Call self.get_objects() to retrieve the text variables and widgets used on this frame.
        self                            -   tkinter.Frame for background
        self.tv_label                   -   tkinter.StringVar for top level
        self.label                      -   tkinter.Label at top
        self.treeview                   -   ttk.Treeview
        self.scrollbar_x                -   ttk.Scrollbar for horizontal scrolling
        self.scrollbar_y                -   ttk.Scrollbar for vertical scrolling
        (
            self.tv_button_new_item     -   tkinter.StringVar for new item button
            self.button_new_item        -   tkinter.Button for new items
        )
        (
            self.tv_button_delete_item  -   tkinter.StringVar for new item button
            self.button_delete_item     -   tkinter.Button for new items
        )
        """
        super().__init__(*args, **kwargs)

        assert isinstance(df,
                          pandas.DataFrame), f"Error, param 'dataframe' must be an instance of a pandas Dataframe, got: '{type(df)}'."

        self.master = master
        self.viewable_column_names = viewable_column_names
        self.viewable_column_widths = viewable_column_widths
        self.tv_label = tv_label
        self.kwargs_label = kwargs_label
        self.kwargs_treeview = kwargs_treeview
        self.default_col_width = default_col_width
        self.include_scroll_x = include_scroll_x
        self.include_scroll_y = include_scroll_y
        self.text_prefix = text_prefix
        self.aggregate_data = aggregate_data if isinstance(aggregate_data, dict) else dict()

        self.iid_namer = (i for i in range(1000000))

        if self.viewable_column_names is None:
            self.viewable_column_names = list(df.columns)

        if not is_tk_var(self.tv_label):
            self.tv_label = tkinter.StringVar(self, value="")

        if self.kwargs_label is None:
            self.kwargs_label = {}

        if self.kwargs_treeview is None:
            self.kwargs_treeview = {}

        if self.viewable_column_widths is None:
            self.viewable_column_widths = [self.default_col_width for _ in range(len(self.viewable_column_names))]
        elif len(self.viewable_column_widths) < len(self.viewable_column_names):
            self.viewable_column_widths = self.viewable_column_widths + [self.default_col_width for _ in range(
                len(self.viewable_column_names) - len(self.viewable_column_widths))]

        self.label = tkinter.Label(self, textvariable=self.tv_label, **self.kwargs_label)
        self.treeview = TreeviewExt(
            self,
            columns=self.viewable_column_names
            , displaycolumns=self.viewable_column_names
            , **self.kwargs_treeview
            # , **kwargs
        )

        for i, col in enumerate(self.viewable_column_names):
            c_width = self.viewable_column_widths[i]
            # print(f"{c_width=}, {type(c_width)=}")
            self.treeview.column(col, width=c_width, anchor=tkinter.CENTER)
            self.treeview.heading(col, text=col, anchor=tkinter.CENTER, command=lambda _col=col: \
                self.treeview.treeview_sort_column(_col, False))

        self.idx_width = 50
        self.treeview.column("#0", width=self.idx_width, stretch=False)
        self.treeview.heading("#0", text="#", anchor=tkinter.CENTER)

        for i, row in enumerate(df.iterrows()):
            next(self.iid_namer)
            idx, row = row
            # print(f"{row=}, {type(row)=}")
            dat = [row[c_name] for c_name in self.viewable_column_names]
            self.treeview.insert("", tkinter.END, text=f"{i+1}", iid=i, values=dat)

        # treeview.bind("<<TreeviewSelect>>", CALLBACK_HERE)
        self.scrollbar_x, self.scrollbar_y = None, None
        if self.include_scroll_y:
            self.scrollbar_y = ttk.Scrollbar(self, orient=tkinter.VERTICAL,
                                             command=self.treeview.yview)
        if self.include_scroll_x:
            self.scrollbar_x = ttk.Scrollbar(self, orient=tkinter.HORIZONTAL,
                                             command=self.treeview.xview)
        if self.scrollbar_x is not None and self.scrollbar_y is not None:
            self.treeview.configure(yscrollcommand=self.scrollbar_y.set, xscrollcommand=self.scrollbar_x.set)
        elif self.scrollbar_x is not None:
            self.treeview.configure(xscrollcommand=self.scrollbar_x.set)
        elif self.scrollbar_y is not None:
            self.treeview.configure(yscrollcommand=self.scrollbar_y.set)

        self.tv_button_new_item, self.button_new_item = button_factory(self, tv_btn="new entry",
                                                                       kwargs_btn={"command": self.insert_new_entry})
        self.tv_button_delete_item, self.button_delete_item = button_factory(self, tv_btn="del entry",
                                                                             kwargs_btn={"command": self.delete_entry})
        # button_new_item.pack()
        # button_delete_item.pack()

        self.frame_aggregate_row = tkinter.Frame(self)
        self.aggregate_objects = [self.frame_aggregate_row]

        # diff_keys = set(self.viewable_column_names).difference(set(self.aggregate_data.keys()))
        order = self.viewable_column_names
        order_s = set(order)
        order_a = []
        to_add = {}
        checked = set()
        for i, k in enumerate(self.aggregate_data):
            # print(f"\t\t{i=}")
            if k.startswith("#") and k[1:].isalnum():
                num = int(k[1:])
                if -1 < num < len(order):
                    key = order[num]
                    to_add[key] = self.aggregate_data[k]
                else:
                    continue
                    # raise Exception("Out of range")
            else:
                if k not in order_s:
                    continue
                key = k
            idx = order.index(key)
            checked.add(key)
            # print(f"HERE {k=}, {key=}, {idx=}, {order_a=}")
            order_a.insert(idx, (key, k))

        self.aggregate_data.update(to_add)

        print(utility.dict_print(self.aggregate_data, "Aggregate data"))
        print(f'A {order_a=}')
        print(f'{order_s=}')
        print(f'{checked=}')
        for kk in order_s.difference(checked):
            idx = self.viewable_column_names.index(kk)
            order_a.insert(idx, (kk, kk))
        # order_a.insert(0, ("#0", "#0"))
        print(f'B {order_a=}')

        for key in order_a:
            print(f"Analyzing COLUMN '{key}'")
        #     if k not in self.aggregate_data:
        # # for k, v in self.aggregate_data.items():
        # #     if k not in self.viewable_column_names:
        #         try:
        #             if k.startswith("#"):
        #                 if 0 > (num:=int(k[1:])) > len(self.viewable_column_names):
        #                     raise Exception(f"Error aggregate data key '{k}' is out of range.")
        #                 else:
        #                     key = self.viewable_column_names[num]
        #             else:
        #                 continue
        #                 # raise Exception(f"Error aggregate data key '{k}' not found in the list of visible column names.")
        #         except ValueError as ve:
        #             raise ValueError(f"Error aggregate data key '{k}' not found in the list of visible column names.")
        #     else:
        #         key = k
            key, k = key
            col_data = self.treeview.column(key)
            p_width = 0.16
            width = col_data.get("width")
            width = int(width * p_width) if width is not None else 10
            x1, x2 = self.column_x(key)
            if k in self.aggregate_data:
                v = self.aggregate_data[k]
                # tv = tkinter.StringVar(self, value=f"{key=}, {v=}")
                tv = tkinter.StringVar(self, value=self.calc_aggregate_value(key))
                entry = tkinter.Entry(
                    self.frame_aggregate_row,
                    textvariable=tv,
                    width=width,
                    state="readonly",
                    justify=tkinter.CENTER
                )
            else:
                v = "NO AGG FOR COL"
                # tv = tkinter.StringVar(self, value=f"{key=}, {v=}")
                tv = tkinter.StringVar(self, value="")
                entry = tkinter.Entry(
                    self.frame_aggregate_row,
                    textvariable=tv,
                    width=width,
                    state="readonly",
                    justify=tkinter.CENTER
                )

            self.aggregate_objects.append(
                (tv, entry, (x1, x2))
            )

            print(f"{key=}, {key=}, {v=}")
            # print(f"{self.treeview.bbox(column=key)=}, {type(self.treeview.bbox(key))=}")
            print(f"{self.treeview.column(key)=}, {type(self.treeview.column(key))=}")
            print(f"{self.treeview.heading(key)=}, {type(self.treeview.heading(key))=}")

        self.treeview.bind("<B1-Motion>", self.check_column_width_update)
        self.treeview.bind("<Button-1>", self.stop_row_idx_resize)

    def column_x(self, column_name):
        x1, x2 = 0, 0
        for i, name in enumerate(self.viewable_column_names):
            col_data = self.treeview.column(name)
            x2 += col_data.get("width", 0)
            if name != column_name:
                x1 += col_data.get("width", 0)
            else:
                break
        return x1, x2

    def calc_aggregate_value(self, column):
        if column not in self.viewable_column_names:
            return "!ERROR"
        idx = self.viewable_column_names.index(column)
        func = self.aggregate_data[column]
        values = []
        scan_unk = True
        scan_num = False
        scan_int = False
        for i, child in enumerate(self.treeview.get_children()):
            item_data = self.treeview.item(child)
            vals = item_data.get("values", [])
            # print(f"{i=}, {idx=}, {child=}, {values=}, {vals=}")
            val = vals[idx]
            values.append(val)
            val_s = str(val)
            # assert isinstance(val, str), f"got {val=}, {type(val)=}"
            # print(f"{i=}, {child=}, {values=}, {val=}")
            if scan_unk:
                scan_unk = False
                if val_s.isnumeric() and ((dot_count:=val_s.count(".")) < 2):
                    scan_num = True
                    scan_int = (dot_count == 0)
            else:
                if val_s.isnumeric() and ((dot_count:=val_s.count(".")) < 2):
                    if scan_num:
                        # values = list(map(str, values))
                        scan_int = (scan_int and (dot_count == 0))
                else:
                    scan_num = False
                    scan_int = False
                    # else:

                    # scan_num = True
        if scan_num:
            if scan_int:
                values = list(map(int, values))
            else:
                values = list(map(float, values))
        else:
            values = list(map(str, values))

        try:
            result = func(values)
        except:
            return "!VALUE"
        if scan_num:
            if scan_int:
                result = int(result)
            else:
                result = float(result)

        return result

    def update_aggregate_row(self):
        for i, col in enumerate(self.viewable_column_names):
            print(f"{i=}, {col=}")
            print(f"\t{self.aggregate_objects[i]=}")
            if i > 0:
                # first is always the frame
                # add 1 to skip the row index column
                tv, *rest = self.aggregate_objects[i + 1]
                tv.set(self.calc_aggregate_value(col))

    def stop_row_idx_resize(self, event):
        """break the event loop before trying to resize the index column"""
        # print(f"{event=}")
        region1 = self.treeview.identify("region", event.x, event.y)
        column = self.treeview.identify_column(event.x)
        # print(f"{region1=}")
        # print(f"{column=}")
        if region1 == "separator" and (column == "#0" or column == f"#{len(self.viewable_column_widths)}"):
            # column_data = self.treeview.column(column)
            return "break"


    def check_column_width_update(self, event):
        print(f"{event=}, {type(event)=}")
        region1 = self.treeview.identify("region", event.x, event.y)
        column = self.treeview.identify_column(event.x)
        column_data = self.treeview.column(column)
        width1 = column_data.get("width", 0)
        name = column_data.get("id", None)
        print(f"{name=}")
        # col_idx1 = 0 if column == "#0" else (self.viewable_column_names.index(name) + 1)
        # col_idx2 = (col_idx1 + 1) if col_idx1 < (len(self.viewable_column_names) - 1) else (col_idx1 - 1)
        col_idx1 = 0 if column == "#0" else (self.viewable_column_names.index(name) - 1)
        col_idx2 = (col_idx1 + 1) if col_idx1 < (len(self.viewable_column_names) - 1) else (col_idx1 - 1)
        width2 = self.treeview.column(f"#{col_idx2}").get("width", 0)
        if region1 == "separator" and column != "#0":
            diff_width = self.viewable_column_widths[col_idx1 - 1] - width1
            print(f"\n\n\t{column_data=}, {width1=}, {width2=}, {diff_width=}")
            print(f"{region1=}, {column=}")
            print(f"{col_idx1=}, {col_idx2=}")
            print(f"{self.viewable_column_widths=}")
            print(f"{self.viewable_column_widths[col_idx1]=}, {self.viewable_column_widths[col_idx2]=}")

            self.viewable_column_widths[col_idx1 - 1] -= diff_width
            self.viewable_column_widths[col_idx2 - 1] += diff_width

            # stretch = column_data.get("stretch", None)
            # print(f"\n\n\t{column_data=}, {stretch=}")
            # if stretch:



            # self.update_aggregate_row()

    def get_objects(self):
        return \
            self, \
            self.tv_label, \
            self.label, \
            self.treeview, \
            self.scrollbar_x, \
            self.scrollbar_y, \
            (self.tv_button_new_item, self.button_new_item), \
            (self.tv_button_delete_item, self.button_delete_item),\
            self.aggregate_objects

    def next_iid(self):
        return next(self.iid_namer) + 1

    def gen_random_entry(self):
        return [random.randint(0, 25) for _ in self.viewable_column_names]

    def insert_new_entry(self, index=tkinter.END):
        data = self.gen_random_entry()
        iid = self.next_iid()
        text = f"{iid}"
        self.treeview.insert("", index, iid=iid, text=text, values=data)

        self.update_aggregate_row()

    def delete_entry(self):
        selection = self.treeview.selection()
        print(f"{selection=}")
        if selection:
            # delete the selected entries
            # row_id = treeview.focus()  # return only 1
            for row_id in selection:
                print(f"{row_id=}")
                self.treeview.delete(row_id)

        self.update_aggregate_row()


def treeview_factory(
        master,
        dataframe,
        viewable_column_names=None,
        viewable_column_widths=None,
        tv_label=None,
        kwargs_label=None,
        kwargs_treeview=None,
        default_col_width=100,
        include_scroll_x=True,
        include_scroll_y=True,
        text_prefix="B_",
        iid_prefix="C_",
        aggregate_data=None
):
    return \
        TreeviewController(
            master,
            dataframe,
            viewable_column_names,
            viewable_column_widths,
            tv_label, kwargs_label,
            kwargs_treeview,
            default_col_width,
            include_scroll_x,
            include_scroll_y,
            text_prefix,
            iid_prefix,
            aggregate_data
        )


# old version 2022-11-30
#
# def treeview_factory(
#         master,
#         dataframe,
#         viewable_column_names=None,
#         viewable_column_widths=None,
#         tv_label=None,
#         kwargs_label=None,
#         kwargs_treeview=None,
#         default_col_width=100,
#         include_scroll_x=True,
#         include_scroll_y=True,
#         text_prefix="B_",
#         iid_prefix="C_"
# ):
#     assert isinstance(dataframe, pandas.DataFrame), f"Error, param 'dataframe' must be an instance of a pandas Dataframe, got: '{type(dataframe)}'."
#
#     def treeview_sort_column(tv, col, reverse):
#         l = [(tv.set(k, col), k) for k in tv.get_children('')]
#         l.sort(reverse=reverse)
#
#         # rearrange items in sorted positions
#         for index, (val, k) in enumerate(l):
#             tv.move(k, '', index)
#
#         # reverse sort next time
#         tv.heading(col, command=lambda: \
#             treeview_sort_column(tv, col, not reverse))
#
#     if viewable_column_names is None:
#         viewable_column_names = list(dataframe.columns)
#
#     if not is_tk_var(tv_label):
#         tv_label = tkinter.StringVar(master, value="")
#
#     if kwargs_label is None:
#         kwargs_label = {}
#
#     if kwargs_treeview is None:
#         kwargs_treeview = {}
#
#     if viewable_column_widths is None:
#         viewable_column_widths = [default_col_width for _ in range(len(viewable_column_names))]
#     elif len(viewable_column_widths) < len(viewable_column_names):
#         viewable_column_widths = viewable_column_widths + [default_col_width for _ in range(len(viewable_column_names) - len(viewable_column_widths))]
#
#     # print(f"About to look at column_names: {viewable_column_names=}, with {viewable_column_widths=}")
#
#     # kwargs = {
#     #     "viewable_column_names": viewable_column_names,
#     #     "viewable_column_widths": viewable_column_widths,
#     #     "tv_label": tv_label,
#     #     "kwargs_label": kwargs_label,
#     #     "kwargs_treeview": kwargs_treeview,
#     #     "default_col_width": default_col_width,
#     #     "include_scroll_x": include_scroll_x,
#     #     "include_scroll_y": include_scroll_y,
#     #     "text_prefix": text_prefix,
#     #     "iid_prefix": iid_prefix
#     # }
#
#     label = tkinter.Label(master, textvariable=tv_label, **kwargs_label)
#     treeview = TreeviewExt(
#         master,
#         columns=viewable_column_names
#         , displaycolumns=viewable_column_names
#         , **kwargs_treeview
#         # , **kwargs
#     )
#     treeview.column("#0", width=0, stretch=tkinter.NO)
#     treeview.heading("#0", text="", anchor=tkinter.CENTER)
#
#     for i, col in enumerate(viewable_column_names):
#         c_width = viewable_column_widths[i]
#         # print(f"{c_width=}, {type(c_width)=}")
#         treeview.column(col, width=c_width, anchor=tkinter.CENTER)
#         treeview.heading(col, text=col, anchor=tkinter.CENTER, command=lambda _col=col: \
#                      treeview_sort_column(treeview, _col, False))
#
#     for i, row in enumerate(dataframe.iterrows()):
#         idx, row = row
#         # print(f"{row=}, {type(row)=}")
#         dat = [row[c_name] for c_name in viewable_column_names]
#         treeview.insert("", tkinter.END, text=f"{text_prefix}{i}", iid=i, values=dat)
#
#     # treeview.bind("<<TreeviewSelect>>", CALLBACK_HERE)
#     scrollbar_x, scrollbar_y = None, None
#     if include_scroll_y:
#         scrollbar_y = ttk.Scrollbar(master, orient=tkinter.VERTICAL,
#                                                      command=treeview.yview)
#     if include_scroll_x:
#         scrollbar_x = ttk.Scrollbar(master, orient=tkinter.HORIZONTAL,
#                                                      command=treeview.xview)
#     if scrollbar_x is not None and scrollbar_y is not None:
#         treeview.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
#     elif scrollbar_x is not None:
#         treeview.configure(xscrollcommand=scrollbar_x.set)
#     elif scrollbar_y is not None:
#         treeview.configure(yscrollcommand=scrollbar_y.set)
#
#     return tv_label, label, treeview, scrollbar_x, scrollbar_y


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

    tv_btn1, btn1 = button_factory(WIN, tv_btn="new entry", kwargs_btn={"command": insert_new_entry})
    tv_btn2, btn2 = button_factory(WIN, tv_btn="del entry", kwargs_btn={"command": delete_entry})
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
        print(f"average of {lst=}, {type(lst)=}")
        return utility.avg(*lst)

    def show_column_info():
        for k, v in treeview_controller.aggregate_data.items():
            if k not in treeview_controller.viewable_column_names:
                try:
                    if not k.startswith("#"):
                        raise Exception(f"Error aggregate data key '{k}' not found in the list of visible column names.")
                    elif 0 > (num:=int(k[1:])) > len(treeview_controller.viewable_column_names):
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
    frame,\
    tv_label,\
    label,\
    treeview,\
    scrollbar_x,\
    scrollbar_y,\
    insert_btn_data,\
    delete_btn_data,\
    aggregate_objects\
        = treeview_controller.get_objects()
    tv_label.set("I forgot to pass a title! - no worries.")
    label.pack(side=tkinter.TOP)
    scrollbar_y.pack(side=tkinter.RIGHT, anchor="e", fill="y")
    treeview.pack(side=tkinter.TOP)
    scrollbar_x.pack(side=tkinter.BOTTOM)

    tv_button_insert_item, button_insert_item = insert_btn_data
    tv_button_delete_item, button_delete_item = delete_btn_data

    frame.pack()
    for i, aggregate_data in enumerate(aggregate_objects):
        print(f"\t{i=}, {aggregate_data=}")
        if i == 0:
            # first is always the frame
            aggregate_data.pack()
        else:
            tv, entry, x1x2 = aggregate_data
            entry.pack(side=tkinter.LEFT)
            x1, x2 = x1x2
            print(f"{x1=}")
            # entry.place(x=x1, y=500)

    button_insert_item.pack()
    button_delete_item.pack()

    tv_button_column_info, button_column_info = button_factory(
        WIN,
        tv_btn="column info",
        kwargs_btn={
            "command": show_column_info
        }
    )
    button_column_info.pack()

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


# class RGBSlider(tkinter.Frame):
#
#     def __init__(self, master):
#         super().__init__(master)
#
#         self.colour = None
#
#         self.slider_red = Slider(self, minimum=0, maximum=255)
#         self.slider_green = Slider(self, minimum=0, maximum=255)
#         self.slider_blue = Slider(self, minimum=0, maximum=255)
#
#         self.tv_label_red, self.label_red, self.tv_entry_red, self.entry_red = entry_factory(self, tv_label="Red:",
#                                                                                              tv_entry=self.slider_red.value)
#         self.tv_label_green, self.label_green, self.tv_entry_green, self.entry_green = entry_factory(self,
#                                                                                                      tv_label="Green:",
#                                                                                                      tv_entry=self.slider_green.value)
#         self.tv_label_blue, self.label_blue, self.tv_entry_blue, self.entry_blue = entry_factory(self, tv_label="Blue:",
#                                                                                                  tv_entry=self.slider_blue.value)
#         self.tv_label_res, self.label_res, self.tv_entry_res, self.entry_res = entry_factory(self, tv_label="Result:",
#                                                                                              tv_entry="Sample Text #123.")
#
#         self.slider_red.value.trace_variable("w", self.update_colour)
#         self.slider_green.value.trace_variable("w", self.update_colour)
#         self.slider_blue.value.trace_variable("w", self.update_colour)
#
#         self.tv_entry_red.trace_variable("w", self.update_colour_entry)
#         self.tv_entry_green.trace_variable("w", self.update_colour_entry)
#         self.tv_entry_blue.trace_variable("w", self.update_colour_entry)
#
#         self.label_red.grid(row=1, column=1)
#         self.entry_red.grid(row=1, column=2)
#         self.slider_red.grid(row=1, column=3)
#         self.label_green.grid(row=2, column=1)
#         self.entry_green.grid(row=2, column=2)
#         self.slider_green.grid(row=2, column=3)
#         self.label_blue.grid(row=3, column=1)
#         self.entry_blue.grid(row=3, column=2)
#         self.slider_blue.grid(row=3, column=3)
#         self.label_res.grid(row=4, column=1)
#         self.entry_res.grid(row=4, column=2)
#         self.update_colour(None, None, None)
#
#     def update_colour_entry(self, *args):
#         print(f"update_colour_entry {args=}")
#         # self.
#
#     def update_colour(self, var_name, index, mode):
#         print(f"update_colour")
#         try:
#             r = self.slider_red.value.get()
#             r_flag = False
#         except tkinter.TclError as te:
#             # if self.slider_red.value != "":
#             #     self.slider_red.value.set(0)
#             # r = self.slider_red.value.get()
#             r = 0
#             r_flag = True
#             print(f"{te=}")
#
#         try:
#             g = self.slider_green.value.get()
#             g_flag = False
#         except tkinter.TclError as te:
#             # if self.slider_green.value != "":
#             #     self.slider_green.value.set(0)
#             # g = self.slider_green.value.get()
#             g = 0
#             g_flag = True
#             print(f"{te=}")
#
#         try:
#             b = self.slider_blue.value.get()
#             b_flag = False
#         except tkinter.TclError as te:
#             # if self.slider_blue.value != "":
#             #     self.slider_blue.value.set(0)
#             # b = self.slider_blue.value.get()
#             b = 0
#             b_flag = True
#             print(f"{te=}")
#
#         print(f"{r=} {g=}, {b=}")
#         if not isnumber(r) or r < 0 or r > 255 or r_flag:
#             self.entry_red.configure(foreground="red")
#         else:
#             self.entry_red.configure(foreground="black")
#         if not isnumber(g) or g < 0 or g > 255 or g_flag:
#             self.entry_green.configure(foreground="red")
#         else:
#             self.entry_green.configure(foreground="black")
#         if not isnumber(b) or b < 0 or b > 255 or b_flag:
#             self.entry_blue.configure(foreground="red")
#         else:
#             self.entry_blue.configure(foreground="black")
#
#         try:
#             self.colour = Colour(r, g, b)
#         except TypeError as te:
#             self.colour = Colour(125, 125, 125)
#             print(f"{te=}")
#
#         h = self.colour.hex_code
#         self.entry_res.config(background=h, foreground=font_foreground(h, rgb=False))

class RGBSlider(tkinter.Frame):

    def __init__(self, master, show_result=True):
        super().__init__(master)

        self.colour = tkinter.Variable(self, value=None)

        self.show_result = show_result

        self.tv_value_red = tkinter.IntVar(self, value=0)
        self.tv_value_green = tkinter.IntVar(self, value=0)
        self.tv_value_blue = tkinter.IntVar(self, value=0)

        self.slider_red = ttk.Scale(
            self,
            from_=0,
            to=255,
            orient=tkinter.HORIZONTAL,
            variable=self.tv_value_red,
            command=self.update_colour
        )
        self.slider_green = ttk.Scale(
            self,
            from_=0,
            to=255,
            orient=tkinter.HORIZONTAL,
            variable=self.tv_value_green,
            command=self.update_colour
        )
        self.slider_blue = ttk.Scale(
            self,
            from_=0,
            to=255,
            orient=tkinter.HORIZONTAL,
            variable=self.tv_value_blue,
            command=self.update_colour
        )

        self.tv_label_red, \
        self.label_red, \
        self.tv_entry_red, \
        self.entry_red \
            = entry_factory(
            self,
            tv_label="Red:",
            tv_entry=self.tv_value_red
        )

        self.tv_label_green, \
        self.label_green, \
        self.tv_entry_green, \
        self.entry_green \
            = entry_factory(
            self,
            tv_label="Green:",
            tv_entry=self.tv_value_green
        )

        self.tv_label_blue, \
        self.label_blue, \
        self.tv_entry_blue, \
        self.entry_blue \
            = entry_factory(
            self,
            tv_label="Blue:",
            tv_entry=self.tv_value_blue
        )

        if self.show_result:
            self.tv_label_res, \
            self.label_res, \
            self.tv_entry_res, \
            self.entry_res \
                = entry_factory(
                self,
                tv_label="Result:",
                tv_entry="Sample Text #123."
            )

        # self.slider_red.value.trace_variable("w", self.update_colour)
        # self.slider_green.value.trace_variable("w", self.update_colour)
        # self.slider_blue.value.trace_variable("w", self.update_colour)

        self.tv_entry_red.trace_variable("w", self.update_colour)
        self.tv_entry_green.trace_variable("w", self.update_colour)
        self.tv_entry_blue.trace_variable("w", self.update_colour)

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

    def update_colour(self, *args):
        print(f"update_colour")
        try:
            # r = self.slider_red.get()
            r = self.tv_entry_red.get()
            r_flag = False
        except tkinter.TclError as te:
            # if self.slider_red.value != "":
            #     self.slider_red.value.set(0)
            # r = self.slider_red.value.get()
            r = 0
            r_flag = True
            print(f"{te=}")

        try:
            # g = self.slider_green.get()
            g = self.tv_entry_green.get()
            g_flag = False
        except tkinter.TclError as te:
            # if self.slider_green.value != "":
            #     self.slider_green.value.set(0)
            # g = self.slider_green.value.get()
            g = 0
            g_flag = True
            print(f"{te=}")

        try:
            # b = self.slider_blue.get()
            b = self.tv_entry_blue.get()
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
            self.colour.set(Colour(r, g, b).hex_code)
        except TypeError as te:
            self.colour.set(Colour(125, 125, 125).hex_code)
            print(f"{te=}")

        if self.show_result:
            h = Colour(self.colour.get()).hex_code
            self.entry_res.config(background=h, foreground=font_foreground(h, rgb=False))


# https://stackoverflow.com/questions/70147814/hint-entry-widget-tkinter
class EntryWithPlaceholder(tkinter.Entry):
    def __init__(self, master=None, font=None, placeholder="PLACEHOLDER", color='grey', textvariable=None):
        super(EntryWithPlaceholder, self).__init__(master)

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
            # self['show'] = '*'
            self.delete('0', 'end')
            self['fg'] = self.default_fg_color

    def foc_out(self, *args):
        if not self.get():
            self.put_placeholder()
            self['show'] = ''


class CustomMessageBox:
    # https://stackoverflow.com/questions/29619418/how-to-create-a-custom-messagebox-using-tkinter-in-python-with-changing-message
    # root = Tk()
    #
    # def func():
    #     a = CustomMessageBox(msg='Hello I m your multiline message',
    #                    title='Hello World',
    #                    b1='Button 1',
    #                    b2='Button 2',
    #                    )
    #     print(a.choice)
    #
    # Button(root, text='Click Me', command=func).pack()
    #
    # root.mainloop()

    def __init__(
            self,
            title='Mess',
            msg='',
            x=None,
            y=None,
            b1='OK',
            b2='',
            b3='',
            b4='',
            tab_colour="red",
            bg_colour="blue",
            bg_colour2="yellow",
            text_colour="Green",
            btn_font_colour="white",
            close_btn_active_colour="red",
            close_btn_active_font_colour="white",
            w=500,
            h=120,
            font_message=("Helvetica", 9),
            font_title=("Helvetica", 10, 'bold'),
            font_x_btn=("Helvetica", 12),
            font_btn=("Helvetica", 10)
    ):

        # Required Data of Init Function
        self.title = title  # Is title of titlebar
        self.msg = msg  # Is message to display
        self.font_message = font_message
        self.font_title = font_title
        self.font_x_btn = font_x_btn
        self.font_btn = font_btn
        self.w = w
        self.h = h
        self.x = x if x is not None else 150
        self.y = y if y is not None else 150
        self.b1 = b1  # Button 1 (outputs '1')
        self.b2 = b2  # Button 2 (outputs '2')
        self.b3 = b3  # Button 3 (outputs '3')
        self.b4 = b4  # Button 4 (outputs '4')
        self.choice = ''  # it will be the return of messagebox according to button press

        # Just the colors for my messagebox

        self.tab_colour = tab_colour  # Button color for Active State
        self.bg_colour = bg_colour  # Button color for Non-Active State
        self.bg_color2 = bg_colour2  # Background color of Dialogue
        self.text_colour = text_colour  # Text color for Dialogue
        self.btn_font_colour = btn_font_colour
        self.close_btn_active_colour = close_btn_active_colour
        self.close_btn_active_font_colour = close_btn_active_font_colour

        # Creating Dialogue for messagebox
        self.root = tkinter.Toplevel()

        # Removing titlebar from the Dialogue
        self.root.overrideredirect(True)

        # Setting Geometry
        self.root.geometry(f"{self.w}x{self.h}+{self.x}+{self.y}")

        # Setting Background color of Dialogue
        self.root.config(bg=self.bg_color2)

        # Creating Label For message
        self.msg = tkinter.Label(self.root, text=msg,
                                 font=self.font_message,
                                 bg=self.bg_color2,
                                 fg=self.text_colour,
                                 # anchor='nw'
                                 )
        self.msg.place(x=self.w * 0.04, y=self.h * 0.15, height=self.h * 0.7, width=self.w * 0.92)

        # Creating TitleBar
        self.titlebar = tkinter.Label(self.root, text=self.title,
                                      bg=self.bg_color2,
                                      fg=self.text_colour,
                                      bd=0,
                                      font=self.font_title
                                      )
        self.titlebar.place(x=self.w * 0.35, y=5)

        # Creating Close Button
        self.CloseBtn = tkinter.Button(self.root,
                                       text='x',
                                       font=self.font_x_btn,
                                       command=lambda: self.closed(),
                                       bd=0,
                                       activebackground=self.close_btn_active_colour,
                                       activeforeground=self.close_btn_active_font_colour,
                                       background=self.bg_color2,
                                       foreground=self.text_colour)
        self.CloseBtn.place(x=self.w - 50, y=5, width=40)

        # Changing Close Button Color on Mouseover
        self.CloseBtn.bind("<Enter>", lambda e,: self.CloseBtn.config(bg=self.close_btn_active_colour,
                                                                      fg=self.close_btn_active_font_colour))
        self.CloseBtn.bind("<Leave>", lambda e,: self.CloseBtn.config(bg=self.bg_color2, fg=self.text_colour))

        ts = 5
        dims = grid_cells(self.w, 4, 25, 1, ts, ts, y_0=90)
        r1c1, r1c2, r1c3, r1c4 = dims[0]
        # Creating B1
        self.B1 = tkinter.Button(self.root, text=self.b1, command=self.click1,
                                 bd=0,
                                 font=self.font_btn,
                                 bg=self.bg_colour,
                                 fg=self.btn_font_colour,
                                 activebackground=self.tab_colour,
                                 activeforeground=self.text_colour)
        self.B1.place(x=r1c1[0], y=r1c1[1], height=r1c1[3] - r1c1[1], width=r1c1[2] - r1c1[0])

        # Getting place_info of B1
        self.B1.info = self.B1.place_info()

        # Creating B2
        if not b2 == "":
            self.B2 = tkinter.Button(self.root, text=self.b2, command=self.click2,
                                     bd=0,
                                     font=self.font_btn,
                                     bg=self.bg_colour,
                                     fg=self.btn_font_colour,
                                     activebackground=self.tab_colour,
                                     activeforeground=self.text_colour)
            self.B2.place(x=r1c2[0], y=r1c2[1], height=r1c2[3] - r1c2[1], width=r1c2[2] - r1c2[0])
        # Creating B3
        if not b3 == '':
            self.B3 = tkinter.Button(self.root, text=self.b3, command=self.click3,
                                     bd=0,
                                     font=self.font_btn,
                                     bg=self.bg_colour,
                                     fg=self.btn_font_colour,
                                     activebackground=self.tab_colour,
                                     activeforeground=self.text_colour)
            self.B3.place(x=r1c3[0], y=r1c3[1], height=r1c3[3] - r1c3[1], width=r1c3[2] - r1c3[0])
        # Creating B4
        if not b4 == '':
            self.B4 = tkinter.Button(self.root, text=self.b4, command=self.click4,
                                     bd=0,
                                     font=self.font_btn,
                                     bg=self.bg_colour,
                                     fg=self.btn_font_colour,
                                     activebackground=self.tab_colour,
                                     activeforeground=self.text_colour)
            self.B4.place(x=r1c4[0], y=r1c4[1], height=r1c4[3] - r1c4[1], width=r1c4[2] - r1c4[0])

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        # self.root.bind("<Configure>", self.update_configure)
        # x = self.root.winfo_x()
        # y = self.root.winfo_y()
        # self.root.geometry('+{}+{}'.format(x+10, y+30))

        # Making MessageBox Visible
        self.root.wait_window()

    def on_closing(self, *args):
        self.closed()

    # def update_configure(self, *args):
    #     print(f"{args=}")
    #     x = self.root.winfo_x()
    #     y = self.root.winfo_y()
    #     self.root.geometry('+{}+{}'.format(x, y))

    # Function on Closeing MessageBox
    def closed(self):
        self.root.destroy()  # Destroying Dialogue
        self.choice = 'closed'  # Assigning Value

    # Function on pressing B1
    def click1(self):
        self.root.destroy()  # Destroying Dialogue
        self.choice = '1'  # Assigning Value

    # Function on pressing B2
    def click2(self):
        self.root.destroy()  # Destroying Dialogue
        self.choice = '2'  # Assigning Value

    # Function on pressing B3
    def click3(self):
        self.root.destroy()  # Destroying Dialogue
        self.choice = '3'  # Assigning Value

    # Function on pressing B4
    def click4(self):
        self.root.destroy()  # Destroying Dialogue
        self.choice = '4'  # Assigning Value


class ScannableEntry(tkinter.Entry):

    def __init__(self, master):
        super().__init__(master)

        self.top_most = top_most_tk(master)

        self.validated_text = tkinter.StringVar(self.top_most,
                                                value="")  # use this variable to ensure that the text has already been validated
        self.text = tkinter.StringVar(self.top_most, value="")
        self.passing_through = tkinter.BooleanVar(self.top_most, value=False)
        self.has_passed_through = tkinter.BooleanVar(self.top_most, value=False)
        self.top_level_keypress = tkinter.StringVar(self.top_most, value="")
        self.top_level_return = tkinter.StringVar(self.top_most, value="")

        self.valid_submission = tkinter.BooleanVar(self.top_most, value=False)  # use this to prevent early submissions.
        self.accepting_counter_reset = 2000
        self.accepting_counter = tkinter.IntVar(self.top_most,
                                                value=self.accepting_counter_reset)  # use this to prevent submission while editing.

        self.entry = tkinter.Entry(self, textvariable=self.text, font=("Arial", 16), justify=tkinter.CENTER)

        # show entry widget
        self.entry.pack()

        # bind and trace widgets and variables
        self.set_bindings()
        self.set_listeners()

    def set_listeners(self):
        self.stop_listeners()
        self.accepting_counter.trace_variable("w", self.update_accepting_counter)
        self.valid_submission.trace_variable("w", self.update_valid_submission)
        self.text.trace_variable("w", self.update_text)

    def set_bindings(self):
        self.stop_bindings()
        self.entry.bind("<Return>", self.return_text)
        self.entry.bind("<FocusIn>",
                        self.update_has_focus_in)  # prevents duplicate event firing when typing directly into the entry widget
        self.entry.bind("<FocusOut>", self.update_has_focus_out)

    def stop_listeners(self):
        if self.accepting_counter.trace_info():
            self.accepting_counter.trace_remove(*self.accepting_counter.trace_info()[0])
        if self.valid_submission.trace_info():
            self.valid_submission.trace_remove(*self.valid_submission.trace_info()[0])
        if self.text.trace_info():
            self.text.trace_remove(*self.text.trace_info()[0])

    def stop_bindings(self):
        # self.entry.unbind("<Return>")
        self.entry.unbind("<FocusIn>")
        self.entry.unbind("<FocusOut>")

    def reset(self):
        # does not reset pass through status
        self.set_bindings()
        self.set_listeners()
        self.accepting_counter.set(self.accepting_counter_reset)
        self.valid_submission.set(False)
        self.text.set("")

    def update_text(self, *args):
        print(f"==\ttk_utility {args=}, {self.text.get()=}, {self.validated_text.get()=}")
        if len(args) == 1:
            # print("\t\t\tFROM TOP MOST")
            event, *rest = args
            ch = event.char
            if ch.isalnum():
                self.text.set(self.text.get() + ch)

        self.accepting_counter.set(self.accepting_counter_reset)
        self.valid_submission.set(False)
        self.validated_text.set("")

        self.count_stop_editing()

    def return_text(self, event):
        # print(f"==\tself.return_text")
        # print(f"{self.accepting_counter.trace_info()[0]=}, {self.accepting_counter.get()=}")
        # self.update_accepting_counter(None)
        # print(f"{self.valid_submission.trace_info()[0]=}")
        # print(f"{self.text.trace_info()[0]=}")
        # print(f"{self.accepting_counter.trace_info()=}")
        # print(f"{self.accepting_counter.trace_vinfo()=}")
        # print(f"AA\tpre set v={self.accepting_counter.get()}, t={self.text.get()}")
        self.accepting_counter.set(0)
        # print(f"AA\tpost set v={self.accepting_counter.get()}, t={self.text.get()}")

    def count_stop_editing(self):
        # print(f"==\tself.count_stop_editing {self.accepting_counter.get()=}")
        x = self.accepting_counter.get()
        if x > 1:
            self.accepting_counter.set(x - 1)
            self.after(1, self.count_stop_editing)

    def update_accepting_counter(self, *args):
        # print(f"==\tupdate_accepting_counter, {self.accepting_counter.get()=}")
        if self.accepting_counter.get() <= 0:
            self.valid_submission.set(True)
        # else:
        #     print(f"{self.accepting_counter.get()=}")

    def update_valid_submission(self, *args):
        # this is called when the entry is ready to be read.
        if self.valid_submission.get() and self.text.get():
            print(f"DONE!! '{self.text.get()}'")
            self.validated_text.set(self.text.get())
        # else:
        #     print(f"\t{self.valid_submission.get()=}, {self.text.get()=}, {(self.valid_submission.get() and self.text.get())=}")

    def update_has_focus_in(self, *event):
        # print(f"==\tupdate_has_focus_in")
        self.top_most.unbind("<Return>")
        self.top_most.unbind("<KeyPress>")

    def update_has_focus_out(self, *event):
        # print(f"==\tupdate_has_focus_out")
        self.top_most.bind("<Return>", self.return_text)
        self.top_most.bind("<KeyPress>", self.update_text)

    def set_scan_pass_through(self):
        print(
            f"WARNING, this forces all generic keyPress and Return key events through this widget.\nDo not use on a single form with multiple text / entry input widgets.")
        self.passing_through.set(True)
        self.has_passed_through.set(True)
        self.top_level_keypress.set(self.top_most.bind("<KeyPress>"))
        self.top_level_return.set(self.top_most.bind("<Return>"))
        # self.top_most.bind("<Return>", self.return_text)
        # self.top_most.bind("<KeyPress>", self.update_text)
        self.update_has_focus_out("")

    def stop_scan_pass_through(self):
        if self.has_passed_through.get():
            if self.top_level_keypress.get():
                self.top_most.bind("<KeyPress>", self.top_level_keypress.get())
            # if self.top_level_return.get():
            #     self.top_most.bind("<Return>", self.top_level_return.get())
        self.passing_through.set(False)
        self.top_level_keypress.set("")
        self.top_level_return.set("")


def apply_state(root, state_in, direction: Literal["up", "down"] = "up", exclude_self=False):
    og_root = root

    if direction not in ("up", "down"):
        raise Exception(f"Error, param 'direction' must be one of 'up' or 'down', got '{direction}'")

    def apply_state_inner(root, state_in, direction, depth, from_processing=False, visited=None):

        # print(f"{root=}")

        if visited is None:
            visited = set()

        # base case
        if isinstance(root, tkinter.Tk) and direction == "up":
            return

        # apply state to current widget
        if str(root) not in visited:
            try:
                if (not exclude_self) or (root != og_root):
                    root.configure(state=state_in)
                    # print(f"SUCCESS!\t\t{depth=}\t{direction=}\t{root=}")
            except tkinter.TclError as te:
                # print(f"\t{depth=}\t{root=}\t{direction=}\t{te=}")

                if depth < 0 and direction == "up" and (not from_processing):
                    for child in root.children:
                        # if (from_processing and (depth + 1 < 0)) or not from_processing:
                        if child not in visited:
                            visited.add(child)
                            wid = root.nametowidget(child)
                            apply_state_inner(wid, state_in, "down", depth + 1, from_processing=True, visited=visited)

        # recursive calls
        if direction == "up":
            apply_state_inner(root.master, state_in, direction, depth - 1, visited)

        else:
            for child in root.children:
                if (from_processing and ((depth + 1) < 0)) or not from_processing:
                    if child not in visited:
                        visited.add(child)
                        wid = root.nametowidget(child)
                        apply_state_inner(wid, state_in, direction, depth + 1, from_processing, visited)

    apply_state_inner(root, state_in, direction, depth=0, visited=set())


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
    i = tkinter.StringVar(root, value="d")
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
    test_treeview_factory_4()
    # test_apply_state_1()
    # test_apply_state_3()

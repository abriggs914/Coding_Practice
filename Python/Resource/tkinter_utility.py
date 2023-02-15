import datetime
import random
import tkinter
from collections import OrderedDict

import pandas

from typing import Literal

import pandas as pd

import utility
from utility import grid_cells, clamp_rect, clamp, isnumber, alpha_seq, random_date
from colour_utility import rgb_to_hex, font_foreground, Colour, random_colour, brighten, darken, gradient, iscolour
from tkinter import ttk, messagebox

#######################################################################################################################
#######################################################################################################################
#######################################################################################################################

VERSION = \
    """	
    General Utility Functions
    Version..............1.34
    Date...........2023-02-15
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


# https://stackoverflow.com/questions/12892180/how-to-get-the-name-of-the-master-frame-in-tkinter
def patriarch(widget, window_b=False):
    while widget and widget.master:
        widget = widget.master
        if window_b and isinstance(widget, tkinter.Toplevel):
            break
    return widget


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
                var = tkinter.StringVar(master, value=default_value)
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
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

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
        super().__init__(master, *args, **kwargs)

        assert isinstance(df,
                          pandas.DataFrame), f"Error, param 'dataframe' must be an instance of a pandas Dataframe, got: '{type(df)}'."

        self.master = master
        self.df = df.reset_index(drop=True)
        self.viewable_column_names = viewable_column_names
        self.viewable_column_widths = viewable_column_widths
        self.tv_label = tv_label
        self.kwargs_label = kwargs_label
        self.kwargs_treeview = kwargs_treeview
        self.default_col_width = default_col_width
        self.include_scroll_x = include_scroll_x
        self.include_scroll_y = include_scroll_y
        self.p_width = 0.16
        self.aggregate_data = aggregate_data if isinstance(aggregate_data, dict) else dict()

        # self.iid_namer = (i for i in range(1000000))

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

        print(f"A {df.shape=}")
        print(f"{list(df.itertuples())=}\n{len(list(df.itertuples()))}")
        # for i, row in df.itertuples():
        f = list(range(1015))
        for i, row in df.iterrows():
            # next(self.iid_namer)
            print(f"{i=}, {row=}, {type(row)=}")
            dat = [row[c_name] for c_name in self.viewable_column_names]
            self.treeview.insert("", tkinter.END, text=f"{i + 1}", iid=i, values=dat)
            f.remove(i)
        print(f"{f=}")
        print(f"B {df.shape=}")
        print(f"{len(list(df.iterrows()))=}")

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

        self.aggregate_data.update(to_add)

        order_d = order_s.difference(checked)
        # print(utility.dict_print(self.aggregate_data, "Aggregate data"))
        # print(f'A {order_a=}')
        # print(f'{order_s=}')
        # print(f'{checked=}')
        # for kk in order_s.difference(checked):
        for idx, kk in enumerate(self.viewable_column_names):
            if kk in order_d:
                # idx = self.viewable_column_names.index(kk)
                order_a.insert(idx, (kk, kk))
        order_a.insert(0, ("#0", "#0"))

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
            # order_a.insert(idx, (key, k))
            order_a[idx + 1] = (key, k)

        # print(f'B {order_a=}')

        for key in order_a:
            # print(f"Analyzing COLUMN '{key}'")
            key, k = key
            col_data = self.treeview.column(key)
            width = col_data.get("width_canvas")
            width = int(width * self.p_width) if width is not None else 10
            x1, x2 = self.column_x(key)
            if k in self.aggregate_data:
                # v = self.aggregate_data[k]
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

            # print(f"{key=}, {key=}, {v=}")
            # # print(f"{self.treeview.bbox(column=key)=}, {type(self.treeview.bbox(key))=}")
            # print(f"{self.treeview.column(key)=}, {type(self.treeview.column(key))=}")
            # print(f"{self.treeview.heading(key)=}, {type(self.treeview.heading(key))=}")

        self.treeview.bind("<B1-Motion>", self.check_column_width_update)
        self.treeview.bind("<Button-1>", self.stop_row_idx_resize)

    def column_x(self, column_name):
        x1, x2 = 0, 0
        for i, name in enumerate(self.viewable_column_names):
            col_data = self.treeview.column(name)
            x2 += col_data.get("width_canvas", 0)
            if name != column_name:
                x1 += col_data.get("width_canvas", 0)
            else:
                break
        return x1, x2

    def calc_aggregate_value(self, column):
        if column not in self.viewable_column_names:
            return "!ERROR"
        idx = self.viewable_column_names.index(column)
        s_agg_d = self.aggregate_data[column]
        func, *formatting = s_agg_d if (isinstance(s_agg_d, list) or isinstance(s_agg_d, tuple)) else (s_agg_d,)
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
                if val_s.isnumeric() and ((dot_count := val_s.count(".")) < 2):
                    scan_num = True
                    scan_int = (dot_count == 0)
            else:
                if val_s.isnumeric() and ((dot_count := val_s.count(".")) < 2):
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

        fail_safe = "!VALUE"
        try:
            result = func(values)
            if formatting:
                formatting = formatting[0]
                if not isinstance(formatting, str):
                    # print(f"ELSE {formatting=}, {type(formatting)=}")
                    if callable(formatting):
                        # print(f"A CALLABLE {result=}, {type(result)=}")
                        result = formatting(result)
                        # print(f"B CALLABLE {result=}, {type(result)=}")
                    else:
                        fail_safe = "!FORMAT"
                        raise Exception(f"Error invalid formatting")
                else:
                    # using string interpolation here.
                    result = formatting % result
        except:
            return fail_safe
        if scan_num:
            if scan_int:
                result = int(result)
            else:
                result = float(result)

        return result

    def update_aggregate_row(self):
        for i, col in enumerate(["#0", *self.viewable_column_names]):
            # print(f"{i=}, {col=}")
            # print(f"\t{self.aggregate_objects[i]=}")
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
        # print(f"{event=}, {type(event)=}")
        region1 = self.treeview.identify("region", event.x, event.y)
        column = self.treeview.identify_column(event.x)
        column_data = self.treeview.column(column)
        width1 = column_data.get("width_canvas", 0)
        name = column_data.get("id", None)
        # print(f"{name=}\n{self.viewable_column_names=}\n{self.viewable_column_widths=}")
        col_idx1 = self.viewable_column_names.index(name)
        col_idx2 = (col_idx1 + 1) if col_idx1 < len(self.viewable_column_names) else (
                len(self.viewable_column_names) - 1)
        width2 = self.treeview.column(f"#{col_idx2}").get("width_canvas", 0)
        if region1 == "separator" and column != "#0":
            diff_width = self.viewable_column_widths[col_idx1 - 1] - width1
            # print(f"\n\n\t{column_data=}, {width1=}, {width2=}, {diff_width=}")
            # print(f"{region1=}, {column=}")
            # print(f"{col_idx1=}, {col_idx2=}")
            # print(f"{self.viewable_column_widths=}")
            # print(f"{self.viewable_column_widths[col_idx1]=}, {self.viewable_column_widths[col_idx2]=}")

            self.viewable_column_widths[col_idx1 - 1] -= diff_width
            self.viewable_column_widths[col_idx2 - 1] += diff_width

            # print(f"{self.aggregate_objects=}")
            # print(f"{self.aggregate_objects[col_idx1 + 2]=}")
            # print(f"{self.aggregate_objects[col_idx1 + 2][1]=}")
            self.aggregate_objects[col_idx1 + 2][1].configure(
                width=int(self.viewable_column_widths[col_idx1 - 1] * self.p_width))
            self.aggregate_objects[col_idx2 + 2][1].configure(
                width=int(self.viewable_column_widths[col_idx2 - 1] * self.p_width))

    def get_objects(self):
        """TreeViewController(tkinter.Frame) || StringVar || Label || TreeViewExt(ttk.TreeView) || ttk.Srollbar || ttk.ScrollBar || Tuple(StringVar, Button) || Tuple(StringVar, Button) || ListOf(Frame, Tuple(TextVariablev, Entry, (x1, x2))) ... Tuple(TextVariablev, Entry, (x1, x2)))"""
        return \
            self, \
            self.tv_label, \
            self.label, \
            self.treeview, \
            self.scrollbar_x, \
            self.scrollbar_y, \
            (self.tv_button_new_item, self.button_new_item), \
            (self.tv_button_delete_item, self.button_delete_item), \
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
        # print(f"{selection=}")
        if selection:
            # delete the selected entries
            # row_id = treeview.focus()  # return only 1
            for row_id in selection:
                # print(f"{row_id=}")
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
#     treeview.column("#0", width_canvas=0, stretch=tkinter.NO)
#     treeview.heading("#0", text="", anchor=tkinter.CENTER)
#
#     for i, col in enumerate(viewable_column_names):
#         c_width = viewable_column_widths[i]
#         # print(f"{c_width=}, {type(c_width)=}")
#         treeview.column(col, width_canvas=c_width, anchor=tkinter.CENTER)
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


class MultiComboBox(tkinter.Frame):

    def __init__(self, master, data, viewable_column_names=None, height_in_rows=10, indexable_column=0, tv_label=None,
                 kwargs_label=None, tv_combo=None, kwargs_combo=None, auto_grid=True, limit_to_list=True,
                 new_entry_defaults=None, lock_result_col=None, allow_insert_ask=True):
        super().__init__(master)

        assert isinstance(data,
                          pandas.DataFrame), f"Error param 'data' must be an instance of a pandas.DataFrame, got '{type(data)}'."
        assert False if (kwargs_combo and (
                "values" in kwargs_combo)) else True, f"Cannot pass values as a keyword argument here. Pass all data in the data param as a pandas.DataFrame."
        # assert auto_pack + auto_grid <= 1, f"Error parameters 'auto_pack'={auto_pack} and 'auto_grid'={auto_grid} must be in a configuration where both params are not True.\nCannot grid and pack child widgets. (1 or None)"

        assert (lock_result_col in viewable_column_names) if viewable_column_names else ((
                                                                                                 lock_result_col in data.columns) if lock_result_col else True), f"Error column '{lock_result_col}' cannot be set as the locked result column. It is not in the list of viewable column names or in the list of columns in the passed dataframe."
        if len(viewable_column_names) == 1:
            new_entry_defaults = []
        assert (new_entry_defaults is not None or allow_insert_ask) if not limit_to_list else 1, "Error, if allow new inserts to this combobox, then you must also either pass rest_values as 'new_entry_defaults' or set 'allow_insert_ask' to True.\nOtherwise there is no way to assign the rest of the column values."

        self.master = master
        self.namer = alpha_seq(10000000)
        self.top_most = patriarch(master)
        self.data = data
        self.limit_to_list = limit_to_list
        self.allow_insert_ask = False if limit_to_list else allow_insert_ask
        self.lock_result_col = lock_result_col

        self.ask_cancelled = f"#!#!# CANCELLED #!#!#"
        self.insert_none = "|/|/||NONE||/|/|"
        self.invalid_inp_codes = {self.ask_cancelled, self.insert_none}

        if tv_label is not None and tv_combo is not None:
            self.res_tv_label = tv_label if is_tk_var(tv_label) else tkinter.StringVar(self, value=tv_label)
            self.res_tv_entry = tv_combo if is_tk_var(tv_combo) else tkinter.StringVar(self, value=tv_combo)
        elif tv_label is not None:
            self.res_tv_label = tv_label if is_tk_var(tv_label) else tkinter.StringVar(self, value=tv_label)
            self.res_tv_entry = tkinter.StringVar(self)
        elif tv_combo is not None:
            self.res_tv_label = tkinter.StringVar(self)
            self.res_tv_entry = tv_combo if is_tk_var(tv_combo) else tkinter.StringVar(self, value=tv_combo)
        else:
            self.res_tv_label = tkinter.StringVar(self)
            self.res_tv_entry = tkinter.StringVar(self)

        if kwargs_label is not None and kwargs_combo is not None:
            self.res_label = tkinter.Label(self, textvariable=self.res_tv_label, **kwargs_label)
        elif kwargs_label is not None:
            self.res_label = tkinter.Label(self, textvariable=self.res_tv_label, **kwargs_label)
        elif kwargs_combo is not None:
            self.res_label = tkinter.Label(self, textvariable=self.res_tv_label)
        else:
            self.res_label = tkinter.Label(self, textvariable=self.res_tv_label)

        self.frame_top_most = tkinter.Frame(self, name="ftm")
        self.frame_tree = tkinter.Frame(self, name="ft")

        # print(f"{data.shape=}")
        # print(f"{data=}")
        self.tree_controller = treeview_factory(self.frame_tree, data, kwargs_treeview={"selectmode": "browse",
                                                                                        "height": height_in_rows},
                                                viewable_column_names=viewable_column_names)
        self.tree_controller, \
        self.tree_tv_label, \
        self.tree_label, \
        self.tree_treeview, \
        self.tree_scrollbar_x, \
        self.tree_scrollbar_y, \
        (self.tree_tv_button_new_item, self.tree_button_new_item), \
        (self.tree_tv_button_delete_item, self.tree_button_delete_item), \
        self.tree_aggregate_objects = self.tree_controller.get_objects()

        cn = self.tree_controller.viewable_column_names
        assert "All" not in cn, "Error, cannot use column name 'All'. This is reserved as a column filtering label."
        self.indexable_column = indexable_column if (
                isinstance(indexable_column, int) and indexable_column < self.data.shape[1]) else (
            0 if not isinstance(indexable_column, str) or indexable_column not in cn else cn.index(indexable_column))

        if isinstance(new_entry_defaults, list) or isinstance(new_entry_defaults, tuple):
            for i, col_default in enumerate(zip(cn, new_entry_defaults)):
                col, default = col_default
                if default in self.invalid_inp_codes:
                    self.throw_fit(default)
                self.new_entry_defaults[col] = default
        elif isinstance(new_entry_defaults, dict):
            self.new_entry_defaults = new_entry_defaults
        else:
            # self.new_entry_defaults = dict(zip(cn, [None for _ in cn]))
            self.new_entry_defaults = dict()

        n_rows, n_cols = data.shape
        # t_width = self.tree_controller.idx_width + (n_cols * sum(self.tree_controller.viewable_column_widths))
        # self.configure(width=t_width)
        # self.frame_top_most.configure(width=t_width)

        self.tv_tree_is_hidden = tkinter.BooleanVar(self, value=True)

        self.frame_top_most.grid_columnconfigure(0, weight=9)
        self.frame_top_most.grid_columnconfigure(1, weight=1)
        self.frame_middle = tkinter.Frame(self, name="fm")
        self.rg_var, self.rg_tv_var, self.rg_btns = radio_factory(self.frame_middle,
                                                                  buttons=["All",
                                                                           *self.tree_controller.viewable_column_names])
        self.rg_var.trace_variable("w", self.update_radio_group)
        self.res_tv_entry.trace_variable("w", self.update_entry)
        self.typed_in = tkinter.BooleanVar(self, value=False)

        self.res_entry = tkinter.Entry(self.frame_top_most, textvariable=self.res_tv_entry, justify="center")
        # self.res_canvas = tkinter.Canvas(self.frame_top_most, width=20, height=20, background=rgb_to_hex("GRAY_62"))
        # self.res_canvas.create_line(11, 6, 11, 19, arrow=tkinter.LAST, arrowshape=(12, 12, 9))

        self.res_canvas = ArrowButton(self.frame_top_most, background=rgb_to_hex("GRAY_62"))

        self.res_canvas.bind("<Button-1>", self.click_canvas_dropdown_button)
        self.tree_treeview.bind("<<TreeviewSelect>>", self.treeview_selection_update)
        self.res_entry.bind("<Key>", self.update_typed_in)
        self.res_entry.bind("<Return>", self.submit_typed_in)

        self.returned_value = tkinter.StringVar(self, value="")

        if auto_grid:
            self.grid(ipadx=12, ipady=12)
            # self.grid_columnconfigure(, weight=10)
            self.res_label.grid(row=0, column=0)

            self.frame_top_most.grid(row=1, column=0, sticky="ew")
            self.res_entry.grid(row=0, column=0, sticky="ew")
            self.res_canvas.grid(row=0, column=1)

        # print(f"Multicombobox created with dimensions (r x c)=({self.data.shape[0]} x {self.data.shape[1]})")

    def treeview_selection_update(self, event):
        # print(f"treeview_selection_update")
        row_ids = self.tree_treeview.selection()
        if row_ids:

            row_id = int(self.tree_treeview.selection()[0])
            # print(f"{row_id=}")
            # print(f"{self.data.shape=}")
            # print(f"{self.tree_treeview.get_children()=}")

            # print(f"{row_id[0]=}")
            # print(f"{self.data=}")
            # data = self.data.iloc[[row_id[0]]]
            # print(f"{data=}")

            # x = self.res_tv_entry.get()
            # self.res_tv_entry.set(str(1 + int(x if x else 0)))

            col = self.tree_controller.viewable_column_names[self.indexable_column]
            if lrc := self.lock_result_col:
                col = lrc
            value = self.data[col].tolist()[row_id]
            # print(f"{col=}")
            # print(f"{value=}")
            self.res_tv_entry.set(str(value))

    def value_exists(self, value_in):
        for i, row in self.data.iterrows():
            for j, x in enumerate(row.values):
                if value_in == x:
                    return True
        return False

    def value_iid(self, value_in):
        for i, row in self.data.iterrows():
            for j, x in enumerate(row.values):
                if value_in == x:
                    return i
        return None

    def select(self, iid):
        if isinstance(iid, int):
            if 0 <= iid < self.data.shape[0]:
                self.tree_treeview.selection_add(iid)
        else:
            iid = self.value_iid(iid)
            if iid is not None:
                self.tree_treeview.selection_add(iid)

    def update_entry(self, *args):
        # print(f"update_entity")
        self.filter_treeview()

    def submit_typed_in(self, event):
        # print(f"submit_typed_in")
        children = self.tree_treeview.get_children()
        if children:
            self.tree_treeview.selection_set(children[0])
        else:
            val = self.res_tv_entry.get()
            col = self.rg_var.get()
            if val:
                self.add_new_item(val, col, self.new_entry_defaults)

    def update_typed_in(self, event):
        # print(f"update_typed_in")
        self.typed_in.set(True)
        self.update_entry()
        self.after(250, lambda: self.typed_in.set(False))

    def update_radio_group(self, *args):
        # print(f"update_radio_group, {args=}")
        col = self.rg_var.get()
        # print(f"{col=}")
        self.filter_treeview()
        self.indexable_column = 0 if col == "All" else self.tree_controller.viewable_column_names.index(col)

    def delete_item(self, iid=None, value="|/|/||NONE||/|/|", mode="first" | Literal["first", "all", "ask"]):
        delete_code = "|/|/||NONE||/|/|"
        if iid is None and value == delete_code:
            self.tree_treeview.delete(*self.tree_treeview.get_children())
        else:
            if iid is not None:
                if isinstance(iid, int):
                    # print(f"DROPPING {iid}")
                    self.data.drop([iid], inplace=True)
                else:
                    raise ValueError(f"Cannot delete row '{iid}' from this dataframe.")
            else:
                # find value, then delete
                if mode == "ask":
                    delete_multi = ((ans := tkinter.YES) == tkinter.messagebox.askyesnocancel(title="Delete",
                                                                                              message="Delete only the first occurence, or all rows that contain this value?"))
                    # print(f"{ans=}")
                    if ans == "cancel":
                        return
                else:
                    delete_multi = mode == "all"
                to_delete = []
                for i, row in self.data.iterrows():
                    for j, x in enumerate(row.values):
                        if value == x:
                            to_delete.append(i)
                            break
                    if to_delete and not delete_multi:
                        break

                if to_delete:
                    # print(f"DROPPING {to_delete=}")
                    self.data.drop(to_delete, inplace=True)
                else:
                    raise ValueError(
                        f"Cannot delete row(s) containing value '{value}' from this dataframe. The value was not found was not Found.")
        self.update_treeview()

    def add_new_item(self, val, col, rest_values=None):
        if val in self.invalid_inp_codes:
            self.throw_fit(val)
        cn = self.tree_controller.viewable_column_names
        col = cn[0] if col == "All" else col
        idx = cn.index(col)
        i = self.data.shape[0]
        # print(f"{type(rest_values)=}\n{rest_values=}")
        if not self.limit_to_list:
            if rest_values and (isinstance(rest_values, list) or isinstance(rest_values, list) or isinstance(rest_values, dict)):
                if isinstance(rest_values, list) or isinstance(rest_values, tuple):
                    row = list(rest_values)
                    row.insert(idx, val)
                    self.data = self.data.append(pandas.DataFrame({k: [v] for k, v in zip(cn, row)}), ignore_index=True)
                    # print(f"\nB\t{self.data=}")
                    self.tree_treeview.insert("", "end", iid=i, text=str(i + 1), values=row)
                    # self.res_entry.config(foreground="black")
                else:
                    row = rest_values.update({col: val})
                    self.data = self.data.append(pandas.DataFrame(row), ignore_index=True)
                    self.tree_treeview.insert("", "end", iid=i, text=str(i + 1), values=list({k: [v] for k, v in zip(cn, row)}.values()))

            elif self.allow_insert_ask:
                ans = tkinter.messagebox.askyesnocancel("Create New Item",
                                                        message=f"Create a new combo box entry with '{val}' in column '{col}' position?")
                row = []
                if ans == tkinter.YES:
                    # print(f"SELECTING {i=}")
                    column_names = self.tree_controller.viewable_column_names
                    for column in column_names:
                        if col != column:
                            if column in self.new_entry_defaults:
                                row.append(self.new_entry_defaults[column])
                            else:
                                ask_value = self.ask_value(column)
                                if ask_value in self.invalid_inp_codes:
                                    self.throw_fit(ask_value)
                                else:
                                    row.append(ask_value)
                        else:
                            row.append(val)

                    # row = [(self.new_entry_defaults[col] if col in self.new_entry_defaults else self.ask_value(col)) for col in column_names]
                    # print(f"\nA\t{self.data=}")
                    # print(f"{pandas.DataFrame({k: [v] for k, v in zip(cn, row)})}")
                    self.data = self.data.append(pandas.DataFrame({k: [v] for k, v in zip(cn, row)}), ignore_index=True)
                    # print(f"\nB\t{self.data=}")
                    self.tree_treeview.insert("", "end", iid=i, text=str(i + 1), values=list(row))
                    self.res_entry.config(foreground="black")
                else:
                    self.res_entry.config(foreground="red")
            elif len(self.tree_controller.viewable_column_names) == 1:
                return
            else:
                raise ValueError("Cannot insert into this combobox")
        else:
            raise ValueError("Cannot insert into this combobox")

    def throw_fit(self, code):
        raise ValueError(f"You cannot use code='{code}'. It is a keyword.")

    def ask_value(self, col):
        tl = tkinter.Toplevel(self)
        tv_lbl, lbl, tv_entry, entry = entry_factory(tl, tv_label=f"Please enter a value for column '{col}':")
        frame = tkinter.Frame(tl)

        def click_submit(*event):
            self.returned_value.set(tv_entry.get())
            tl.destroy()

        def click_cancel(*event):
            self.returned_value.set(self.ask_cancelled)
            tl.destroy()

        entry.bind("<Return>", click_submit)
        tv_btn_cancel, btn_cancel = button_factory(frame, tv_btn="cancel", kwargs_btn={"command": click_cancel})
        tv_btn_ok, btn_ok = button_factory(frame, tv_btn="ok", kwargs_btn={"command": click_submit})
        lbl.pack()
        entry.pack()
        frame.pack()
        btn_cancel.pack(side=tkinter.LEFT)
        btn_ok.pack(side=tkinter.LEFT)
        entry.focus()
        self.top_most.wait_window(tl)

        return self.returned_value.get()

    def update_treeview(self):
        self.tree_treeview.delete(*self.tree_treeview.get_children())
        for i, row in self.data.iterrows():
            # print(f"{i=}, {row=}")
            self.tree_treeview.insert("", "end", iid=i, text=str(i + 1), values=list(row))

    def filter_treeview(self):
        # print(f"filter_treeview: {self.typed_in.get()}\n\n\tDATA\n{self.data}")
        if self.typed_in.get():
            val = self.res_tv_entry.get().lower()
            col = self.rg_var.get()
            some = False
            if not val:
                # print(f"Not val")
                self.update_treeview()
                some = True

                if some:
                    self.res_entry.config(foreground="black")
                else:
                    self.res_entry.config(foreground="red")

                # if not self.limit_to_list:
                #     self.add_new_item(val, col)

                return

            if col != "All":
                # print(f"col != All")
                self.tree_treeview.delete(*self.tree_treeview.get_children())
                for i, value in enumerate(self.data[col].tolist()):
                    # print(f"\t\t{i=}, {value=}")
                    if val in str(value).lower():
                        some = True
                        row = self.data.iloc[[i]].values
                        # print(f"\t\t{i=}, {value=}, {row=}")
                        self.tree_treeview.insert("", "end", iid=i, text=str(i + 1), values=list(*row))
            else:
                # print(f"\n\nFilter Else")
                self.tree_treeview.delete(*self.tree_treeview.get_children())
                c = 0
                for i, row in self.data.iterrows():
                    found = False
                    for j, x in enumerate(row.values):
                        if val in str(x):
                            found = True
                            break
                    if found:
                        # print(f"BACK IN {i=}\t{row=}")
                        self.tree_treeview.insert("", "end", iid=i, text=i + 1, values=list(row))
                        c += 1
                        some = True
                    # print(f"{i=}\n{row=}\n{found=}")

            if some:
                self.res_entry.config(foreground="black")
            else:
                self.res_entry.config(foreground="red")
            # if not self.limit_to_list:
            #     self.add_new_item(val, col)

    def click_canvas_dropdown_button(self, event):
        is_hidden = self.tv_tree_is_hidden.get()
        if is_hidden:
            # now show

            self.res_canvas.change_direction("n")
            self.frame_middle.grid(row=2, column=0)
            self.frame_tree.grid(row=3, column=0)

            for i, btn in enumerate(self.rg_btns):
                btn.grid(row=0, column=i)

            self.tree_controller.grid(row=1, column=0)
            self.tree_treeview.grid(row=0, column=0)
            self.tree_scrollbar_x.grid(row=3, sticky="ew")
            self.tree_scrollbar_y.grid(row=0, column=1, sticky="ns")
            for i, data in enumerate(self.tree_aggregate_objects):
                if i > 0:
                    tv, entry, x1x2 = data
                    # print(f"{i=}, {tv.get()=}")
                    entry.grid(row=0, column=i)
                else:
                    data.grid(row=2)
        else:
            # now hide
            self.res_canvas.change_direction("s")
            self.frame_middle.grid_forget()
            self.frame_tree.grid_forget()
            self.tree_treeview.grid_forget()
            self.tree_controller.grid_forget()
            self.tree_scrollbar_x.grid_forget()
            self.tree_scrollbar_y.grid_forget()
            for btn in self.rg_btns:
                btn.grid_forget()
            for i, data in enumerate(self.tree_aggregate_objects):
                if i > 0:
                    tv, entry, x1x2 = data
                    # print(f"{i=}, {tv.get()=}")
                    entry.grid_forget()
                else:
                    data.grid_forget()
        self.tv_tree_is_hidden.set(not is_hidden)

    def is_valid(self):
        return self.res_tv_entry.get() and self.tree_treeview.get_children()


class ArrowButton(tkinter.Canvas):
    def __init__(self, master, mode: Literal[
        "up", "down", "left", "right",
        "top-left", "top-right", "bottom-left", "bottom-right",
        "n", "s", "e", "w", "ne", "nw", "se", "sw",
        "N", "S", "E", "W", "NE", "NW", "SE", "SW"] = "down", width=20, height=20, *args, **kwargs):
        super().__init__(master, width=width, height=height, *args, **kwargs)

        self.valid = {
            "up", "down", "left", "right",
            "top-left", "top-right", "bottom-left", "bottom-right",
            "n", "s", "e", "w", "ne", "nw", "se", "sw",
            "N", "S", "E", "W", "NE", "NW", "SE", "SW"
        }
        mode = self.validate_mode(mode)

        self.mode = mode
        self.width = width
        self.height = height

        self.configure(width=20, height=20, background=rgb_to_hex("GRAY_62"))

        self.draw_arrow()
        # print(f"=={mode=} :: ({x1}, {y1}), ({x2}, {y2})")
        self.bind("<Button-1>", self.click_canvas_button)

    def validate_mode(self, mode):
        if mode not in self.valid:
            mode = "s"
        return mode

    def calc_arrow(self):
        x1, y1, x2, y2 = 11, 6, 11, 19  # down

        if self.mode in {"down", "s", "S"}:
            pass
        elif self.mode in {"up", "n", "N"}:
            y1, y2 = y2, y1
        elif self.mode in {"left", "w", "W"}:
            x1, y1, x2, y2 = y2, x1, y1, x2
        elif self.mode in {"bottom-left", "sw", "SW"}:
            x1, y1, x2, y2 = x1, x2, y1, y2
        elif self.mode in {"top-right", "ne", "NE"}:
            x1, y1, x2, y2 = x1, x2, y2, y1
        elif self.mode in {"top-left", "nw", "NE"}:
            x1, y1, x2, y2 = x1, x2, y1, y1
        elif self.mode in {"bottom-right", "se", "SE"}:
            x1, y1, x2, y2 = x1, x2, y2, y2
        elif self.mode in {"right", "e", "E"}:
            x1, y1, x2, y2 = y1, x1, y2, x2
        else:
            print(f"\tFAILURE\t\t{self.mode=}")
            pass

        return x1, y1, x2, y2

    def draw_arrow(self, clear_first=True):
        if clear_first:
            self.delete("all")
        x1, y1, x2, y2 = self.calc_arrow()
        self.create_line(x1, y1, x2, y2, arrow=tkinter.LAST, arrowshape=(12, 12, 9))

    def click_canvas_button(self, event):
        # Add functionality here, or use the same binding in your code.
        print(f"click_canvas_button\n{self}")

    def change_direction(self, mode):
        self.mode = self.validate_mode(mode)
        self.draw_arrow()


# https://stackoverflow.com/questions/44099594/how-to-make-a-tkinter-canvas-rectangle-with-rounded-corners
# see below (round_rect) as well
# Usage:
# from tkinter import *
# root = Tk()
# canvas = Canvas(root, width = 1000, height = 1000)
# canvas.pack()
# my_rectangle = roundPolygon([50, 350, 350, 50], [50, 50, 350, 350], 10 , width=5, outline="#82B366", fill="#D5E8D4")
# my_triangle = roundPolygon([50, 650, 50], [400, 700, 1000], 8 , width=5, outline="#82B366", fill="#D5E8D4")
#
# root.mainloop()
def round_polygon(canvas, x, y, sharpness, **kwargs):
    # The sharpness here is just how close the sub-points
    # are going to be to the vertex. The more the sharpness,
    # the more the sub-points will be closer to the vertex.
    # (This is not normalized)
    if sharpness < 2:
        sharpness = 2

    ratioMultiplier = sharpness - 1
    ratioDividend = sharpness

    # Array to store the points
    points = []

    # Iterate over the x points
    for i in range(len(x)):
        # Set vertex
        points.append(x[i])
        points.append(y[i])

        # If it's not the last point
        if i != (len(x) - 1):
            # Insert submultiples points. The more the sharpness, the more these points will be
            # closer to the vertex.
            points.append((ratioMultiplier * x[i] + x[i + 1]) / ratioDividend)
            points.append((ratioMultiplier * y[i] + y[i + 1]) / ratioDividend)
            points.append((ratioMultiplier * x[i + 1] + x[i]) / ratioDividend)
            points.append((ratioMultiplier * y[i + 1] + y[i]) / ratioDividend)
        else:
            # Insert submultiples points.
            points.append((ratioMultiplier * x[i] + x[0]) / ratioDividend)
            points.append((ratioMultiplier * y[i] + y[0]) / ratioDividend)
            points.append((ratioMultiplier * x[0] + x[i]) / ratioDividend)
            points.append((ratioMultiplier * y[0] + y[i]) / ratioDividend)
            # Close the polygon
            points.append(x[0])
            points.append(y[0])

    return canvas.create_polygon(points, **kwargs, smooth=tkinter.TRUE)


# https://stackoverflow.com/questions/44099594/how-to-make-a-tkinter-canvas-rectangle-with-rounded-corners
# see above (round_polygon) as well
# Usage:
# import tkinter
# root = tkinter.Tk()
# canvas = tkinter.Canvas(root)
# canvas.pack()
# rounded_rect(canvas, 20, 20, 60, 40, 10)
# root.mainloop()
def rounded_rect(canvas, x, y, w, h, c):
    assert isinstance(canvas,
                      tkinter.Canvas), f"Error param 'canvas' must be a tkinter.Canvas object. Got '{canvas}', {type(canvas)=}"
    return [
        canvas.create_arc(x, y, x + 2 * c, y + 2 * c, start=90, extent=90, style="arc"),
        canvas.create_arc(x + w - 2 * c, y + h - 2 * c, x + w, y + h, start=270, extent=90, style="arc"),
        canvas.create_arc(x + w - 2 * c, y, x + w, y + 2 * c, start=0, extent=90, style="arc"),
        canvas.create_arc(x, y + h - 2 * c, x + 2 * c, y + h, start=180, extent=90, style="arc"),
        canvas.create_line(x + c, y, x + w - c, y),
        canvas.create_line(x + c, y + h, x + w - c, y + h),
        canvas.create_line(x, y + c, x, y + h - c),
        canvas.create_line(x + w, y + c, x + w, y + h - c)
    ]


class ToggleButton(tkinter.Frame):

    def __init__(
            self,
            master,
            label_text="Toggle",
            state: bool = False,
            labels=("On", "Off"),
            width_label=25,
            height_label=1,
            width_canvas=100,
            height_canvas=50,
            t_animation_time=500,
            n_slices=10,
            label_font=("Arial", 12),
            labels_font=("Arial", 12),
            colour_fg_true="#003000",
            colour_bg_true="#29c164",
            colour_fg_false="#300000",
            colour_bg_false="#c12929",
            auto_grid=True,
            *args, **kwargs):
        super().__init__(master, width=width_canvas, height=height_canvas, *args, **kwargs)

        assert iscolour(
            colour_bg_false), f"Error param 'colour_bg_false' must be a colour. Got '{colour_bg_false}', {type(colour_bg_false)=}."
        assert iscolour(
            colour_bg_true), f"Error param 'colour_bg_true' must be a colour. Got '{colour_bg_true}', {type(colour_bg_true)=}."
        assert iscolour(
            colour_fg_false), f"Error param 'colour_fg_false' must be a colour. Got '{colour_fg_false}', {type(colour_fg_false)=}."
        assert iscolour(
            colour_fg_true), f"Error param 'colour_fg_true' must be a colour. Got '{colour_fg_true}', {type(colour_fg_true)=}."
        assert labels is None or (isinstance(labels, tuple) and len(labels) == 2 and all(
            [isinstance(labels[i], str) for i in
             range(2)])), f"Error param 'labels' must be a tuple of 2 strings OR None. Got '{labels}', {type(labels)=}"
        assert isinstance(t_animation_time, int) and (
                    0 < t_animation_time <= 2500), f"Error param 't_animation_time' must be a integer between 1 and 2500 ms. Got '{t_animation_time}', {type(t_animation_time)=}."

        self.label_font = label_font  # for the main label
        self.labels_font = labels_font  # for the button labels, if needed
        self.height_label = height_label
        self.tv_label = tkinter.StringVar(self, value=label_text)
        self.label = tkinter.Label(self, textvariable=self.tv_label, width=width_label, height=height_label,
                                   font=self.label_font)
        self.frame_canvas = tkinter.Frame(self, width=width_label + width_canvas)
        self.canvas = tkinter.Canvas(self.frame_canvas, width=width_canvas, height=height_canvas)

        self.switch_mode = tkinter.BooleanVar(self)

        # print(f"{labels=}")

        if labels is None:
            self.switch_mode.set(True)
        else:
            self.switch_mode.set(False)

        self.colour_bg_true = colour_bg_true
        self.colour_bg_false = colour_bg_false
        self.colour_fg_true = colour_fg_true
        self.colour_fg_false = colour_fg_false
        self.width = width_canvas
        self.height = height_canvas
        self.auto_grid = auto_grid

        self.t_animation_time = t_animation_time
        self.n_slices = clamp(3, n_slices, self.t_animation_time // 50)
        self.after_time = self.t_animation_time // self.n_slices
        # print(f"\tInit\n{self.t_animation_time=}\n{self.n_slices=}\n{self.after_time=}\n{self.n_slices*self.after_time=}")
        self.state = tkinter.BooleanVar(self, value=state)
        self.state.trace_variable("w", self.state_update)

        self.sliding = tkinter.BooleanVar(self, value=False)

        self.bind("<Button-1>", self.click)
        self.label.bind("<Button-1>", self.click)
        self.frame_canvas.bind("<Button-1>", self.click)
        self.canvas.bind("<Button-1>", self.click)

        o_x1, o_y1, o_x2, o_y2 = self.width, self.height, self.width, self.height
        x1, y1, x2, y2 = o_x1 * 0.15, o_y1 * 0.15, o_x2 * 0.85, o_y2 * 0.85
        pts = [
            (x1, y1),
            (x2, y1),
            (x2, y2),
            (x1, y2)
        ]
        xs, ys = [[pt[i] for pt in pts] for i in range(2)]
        self.round_rect = round_polygon(
            self.canvas,
            xs,
            ys,
            width=2,
            sharpness=25,
            outline=self.colour_fg_false,
            fill=brighten(self.colour_bg_false, 0.25, rgb=False)
        )

        if not self.switch_mode.get():
            # print(f"init NOT switch mode")
            self.labels = labels  # (True part, False part)
            lbl_on, lbl_off = self.labels
            self.text_off = self.canvas.create_text(self.width * 0.25, self.height / 2, text=lbl_off,
                                                    fill=self.colour_fg_false, font=self.labels_font)
            self.text_on = self.canvas.create_text(self.width * 0.75, self.height / 2, text=lbl_on,
                                                   fill=self.colour_fg_true, font=self.labels_font)
        else:
            # print(f"init switch mode")
            x1, y1, x2, y2 = \
                o_x1 * 0.5, \
                o_y1 * 0.35, \
                o_x2 * 0.6, \
                o_y2 * 0.65
            sw = x2 - x1
            sh = y2 - y1
            pts = [
                (x1, y1),
                (x2, y1),
                (x2, y2),
                (x1, y2)
            ]
            xs, ys = [[pt[i] for pt in pts] for i in range(2)]
            self.switch_btn = round_polygon(
                self.canvas,
                xs,
                ys,
                sharpness=10,
                outline=self.colour_fg_false,
                fill=darken(self.colour_bg_false, 0.25, rgb=False)
            )

            x1, x2 = o_x1 * 0.2, o_x2 * 0.7
            wd = x2 - x1
            ws = wd / self.n_slices
            self.switch_positions = [(x1 + (i * ws), y1 * 0.9) for i in range(self.n_slices)]
            if not self.state.get():
                self.switch_positions.reverse()

        # idx 0 == state (0 / 1)
        # idx 1 == state (bg_gradient, fg_gradient)
        self.gradients = [
            [
                [gradient(i, self.n_slices - 1, colour_bg_true, colour_bg_false, rgb=False) for i in
                 range(self.n_slices)],
                [gradient(i, self.n_slices - 1, self.colour_fg_true, self.colour_fg_false, rgb=False) for i in
                 range(self.n_slices)]
            ],
            [
                [gradient(i, self.n_slices - 1, self.colour_bg_false, self.colour_bg_true, rgb=False) for i in
                 range(self.n_slices)],
                [gradient(i, self.n_slices - 1, self.colour_fg_false, self.colour_fg_true, rgb=False) for i in
                 range(self.n_slices)]
            ]
        ]

        self.state_update()

    def state_update(self, *args):
        # print(f"\tstate update\n\t{self.tv_label.get()=}\n\t{self.state.get()=}\n\t{self.switch_mode.get()=}")
        slices = self.n_slices
        state = self.state.get()

        if not self.switch_mode.get():
            if state:
                self.canvas.itemconfigure(self.text_on, state="normal")
                self.canvas.itemconfigure(self.text_off, state="hidden")
            else:
                self.canvas.itemconfigure(self.text_on, state="hidden")
                self.canvas.itemconfigure(self.text_off, state="normal")

        def iter_update(i):
            # print(f"\titer_{i=}")
            if i == slices:
                self.sliding.set(False)
                return

            bg_colour, fg_colour = self.gradients[int(state)]
            bg_colour = bg_colour[i]
            fg_colour = fg_colour[i]
            fill_colour = brighten(bg_colour, 0.25, rgb=False) if not state else darken(bg_colour, 0.25, rgb=False)
            switch_colour = darken(bg_colour, 0.25, rgb=False) if not state else brighten(bg_colour, 0.25, rgb=False)

            # https://stackoverflow.com/questions/22838255/tkinter-canvas-resizing-automatically
            self.configure(background=bg_colour, highlightthickness=0)
            self.canvas.itemconfigure(
                self.round_rect,
                outline=fg_colour,
                fill=fill_colour
            )

            if not self.switch_mode.get():
                # print(f"update NOT switch mode")
                self.canvas.itemconfigure(self.text_on, fill=fg_colour)
                self.canvas.itemconfigure(self.text_off, fill=fg_colour)
            else:
                # print(f"update switch mode")
                x, y = self.switch_positions[i]
                self.canvas.moveto(self.switch_btn, x=x, y=y)
                self.canvas.itemconfigure(self.switch_btn, outline=fg_colour, fill=switch_colour)

            self.canvas.configure(background=bg_colour, highlightthickness=0)
            self.label.configure(background=bg_colour, foreground=fg_colour, highlightthickness=0)

            self.after(self.after_time, iter_update, i + 1)

        iter_update(0)

    def click(self, *args):
        # print(f"\nclick '{self.tv_label.get()=}'")
        if not self.sliding.get():
            if self.switch_mode.get():
                self.switch_positions.reverse()
            self.sliding.set(True)
            self.state.set(not self.state.get())

    def get_objects(self):
        # Button, (Label_var, Label), canvas_frame, (State, canvas)
        return (
            self,
            (self.tv_label, self.label),
            self.frame_canvas,
            (self.state, self.canvas)
        )


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
            # entry.place(x=x1, y=500)

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

    # a, c, d, b = multi_combo_factory(WIN, data, tv_label="Multi-ComboBox Demo")
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
    # d.grid(row=1, column=1)
    #
    # tv1_fact.grid()
    # tv1_label.grid(row=0)
    # tv1_scrollbar_x.grid(row=3, sticky="ew")
    # tv1_treeview.grid(row=1, column=0)
    # tv1_scrollbar_y.grid(row=1, column=1, sticky="ns")
    # for i, data in enumerate(tv1_aggregate_objects):
    #     if i > 0:
    #         tv, entry, x1x2 = data
    #         # print(f"{i=}, {tv.get()=}")
    #         entry.grid(row=0, column=i)
    #     else:
    #         data.grid(row=2)

    # dealers = ["A", "B", "C"]
    # colours = ["red", "blue", "green", "custom", "none"]
    # sv_lbl_1, lbl_1, sv_cb_1, cb_1 = combo_factory(WIN, tv_label="Dealer", kwargs_combo={"values": dealers})
    # sv_lbl_2, lbl_2, sv_cb_2, cb_2 = combo_factory(WIN, tv_label="Colour", kwargs_combo={"values": colours})
    #
    # def new_dealer(var_name, index, mode):
    #     d = sv_cb_1.get()
    #     c = sv_cb_2.get()
    #     if c and d:
    #         if c not in ["custom", "none"]:
    #             print(f"Setting {d=} to {c=}")
    #         elif c == "custom":
    #             print(f"custom colour from dealer {d=}")
    #         else:
    #             print(f"removing colour from dealer {d=}")
    #
    # def new_colour(var_name, index, mode):
    #     d = sv_cb_1.get()
    #     c = sv_cb_2.get()
    #     if c and d:
    #         if c not in ["custom", "none"]:
    #             print(f"Setting {d=} to {c=}")
    #         elif c == "custom":
    #             print(f"custom colour from dealer {d=}")
    #         else:
    #             print(f"removing colour from dealer {d=}")
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

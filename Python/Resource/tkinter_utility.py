import datetime
import random
import tkinter
from collections import OrderedDict, deque

import pandas

from typing import Literal, Tuple, List, Callable, Optional

import pandas as pd

import utility
from datetime_utility import random_date
from utility import grid_cells, clamp_rect, clamp, isnumber, alpha_seq, lstindex, dict_print
from colour_utility import *
from tkinter import ttk, messagebox

#######################################################################################################################
#######################################################################################################################
#######################################################################################################################

VERSION = \
    """	
    General tkinter Centered Utility Functions
    Version..............1.81
    Date...........2024-09-16
    Author(s)....Avery Briggs
    """


def VERSION_DETAILS():
    return VERSION.lower().split("version")[0].strip()


def VERSION_NUMBER():
    return float(".".join(VERSION.lower().split("version")[-1].split("date")[0].split(".")[-2:]).strip())


def VERSION_DATE():
    return datetime.datetime.strptime(VERSION.lower().split("date")[-1].split("author")[0].split(".")[-1].strip(),
                                      "%Y-%m-%d")


def VERSION_AUTHORS():
    return [w.removeprefix(".").strip().title() for w in VERSION.lower().split("author(s)")[-1].split("..") if
            w.strip()]


#######################################################################################################################
#######################################################################################################################
#######################################################################################################################


def grid_keys():
    """r, c, rs, cs, ix, iy, x, y, s = grid_keys()"""
    return "row", "column", "rowspan", "columnspan", "ipadx", "ipady", "padx", "pady", "sticky"


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


def entry_tip_factory(master, tip, tv_label=None, tv_entry=None, kwargs_label=None, kwargs_entry=None):
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

    fg = res_entry.cget("foreground")

    def check_empty(*args):
        # print(f"check_empty, {tip=}, {res_tv_entry.get()=} {res_tv_entry.get()==tip=}")
        if (txt := res_entry.get()) == "":
            res_tv_entry.set(tip)
            res_entry.configure(foreground=Colour(fg).brighten(0.75).hex_code)
        else:
            res_entry.configure(foreground=fg)
            clear_entry()

    def kp(event=None):
        # print(f"1 kp => {event}, {tip=}, {res_tv_entry.get()=} {res_tv_entry.get()==tip=}")
        if (txt := res_tv_entry.get()) == tip and event.char in valid_chars:
            res_tv_entry.trace_remove("write", tv_cb.get())
            res_tv_entry.set("")
            tv_cb.set(res_tv_entry.trace_variable("w", check_empty))
            # print(f"DONE: {res_tv_entry.get()=}")

        # print(f"2 kp => {event}, {tip=}, {res_tv_entry.get()=} {res_tv_entry.get()==tip=}")

    def clear_entry(event=None):
        # print(f"clear_entry, {res_tv_entry.get()=} {res_tv_entry.get()==tip=}")
        if res_tv_entry.get() == tip:
            res_tv_entry.set("")

    valid_chars = {chr(i) for i in range(97, 124)}
    valid_chars.update({c.upper() for c in valid_chars})
    for i in range(10):
        valid_chars.add(str(i))
    for c in ["!", "@", "#", "$", "%", "%", "^", "&", "*", "(", ")", "_", "-", "=", "+", "`", "~", "\\", "|", "[", "]",
              "{", "}", ";", ":", "'", "\"", ",", "<", ".", ">", "/", "?"]:
        valid_chars.add(c)

    tv_cb = tkinter.Variable(value=res_tv_entry.trace_variable("w", check_empty))
    res_entry.bind("<FocusIn>", clear_entry)
    res_entry.bind("<KeyPress>", kp)
    check_empty()
    res_entry.setvar("tip", tip)

    return res_tv_label, res_label, res_tv_entry, res_entry


def text_factory(master, tv_label=None, tv_text=None, kwargs_label=None, kwargs_text=None):
    """Return tkinter StringVar, Label, StringVar, and TextWithVar objects"""
    if tv_label is not None and tv_text is not None:
        res_tv_label = tv_label if is_tk_var(tv_label) else tkinter.StringVar(master, value=tv_label)
        res_tv_text = tv_text if is_tk_var(tv_text) else tkinter.StringVar(master, value=tv_text)
    elif tv_label is not None:
        res_tv_label = tv_label if is_tk_var(tv_label) else tkinter.StringVar(master, value=tv_label)
        res_tv_text = tkinter.StringVar(master)
    elif tv_text is not None:
        res_tv_label = tkinter.StringVar(master)
        res_tv_text = tv_text if is_tk_var(tv_text) else tkinter.StringVar(master, value=tv_text)
    else:
        res_tv_label = tkinter.StringVar(master)
        res_tv_text = tkinter.StringVar(master)

    print(f"{tv_label=}\n{tv_text=}\n{kwargs_label=}\n{kwargs_text=}")
    print(f"{res_tv_label=}\n{res_tv_text=}")

    if kwargs_label is not None and kwargs_text is not None:
        res_label = tkinter.Label(master, textvariable=res_tv_label, **kwargs_label)
        res_text = TextWithVar(master, textvariable=res_tv_text, **kwargs_text)
    elif kwargs_label is not None:
        res_label = tkinter.Label(master, textvariable=res_tv_label, **kwargs_label)
        res_text = TextWithVar(master, textvariable=res_tv_text)
    elif kwargs_text is not None:
        res_label = tkinter.Label(master, textvariable=res_tv_label)
        res_text = TextWithVar(master, textvariable=res_tv_text, **kwargs_text)
    else:
        res_label = tkinter.Label(master, textvariable=res_tv_label)
        res_text = TextWithVar(master, textvariable=res_tv_text)
    return res_tv_label, res_label, res_text.text, res_text


def button_factory(master, tv_btn=None, kwargs_btn=None, command=None):
    """Return tkinter StringVar, Button objects"""

    if kwargs_btn is not None:
        assert isinstance(kwargs_btn,
                          dict), f"Error param 'kwargs_btn' must be a dict if not None. Got: '{kwargs_btn}'."
        if "command" in kwargs_btn and command is not None:
            raise KeyError(
                f"Error, command key has already been passed in param 'kwargs_btn'. Please pass only one command.")
        elif command is not None:
            assert callable(command), "Error, param 'command' is not callable."
            kwargs_btn.update({"command": command})
    elif command is not None:
        assert callable(command), "Error, param 'command' is not callable."
        kwargs_btn = {"command": command}

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


def combo_factory(master, tv_label=None, kwargs_label=None, tv_combo=None, kwargs_combo=None, values=None):
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

    if values is not None:
        if not (kcn := kwargs_combo is None) and not (kcvn := kwargs_combo.get("values") is None):
            raise ValueError("Error, cannot explicitly pass values as parameter and in 'kwargs_combo'.")
        else:
            if kcn:
                kwargs_combo = {"values": values}
            else:
                kwargs_combo.update({"values": values})

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
    if hasattr(buttons, '__iter__') and buttons:
        if not (isinstance(buttons, list) and isinstance(buttons, tuple)):
            buttons = list(buttons)
        if default_value is not None:
            # print(f"not None")
            if isinstance(default_value, tkinter.IntVar):
                # print(f"is_var")
                var = default_value
            elif isnumber(default_value):
                # print(f"not var")
                var = tkinter.IntVar(master, value=int(default_value))
            else:
                raise ValueError(f"Error default value '{default_value}' is not a number.")
        else:
            print(f"is None")
            var = tkinter.IntVar(master, value=-1)

        if 0 > var.get() >= len(buttons):
            raise IndexError("Error var index is out of range")

        # print(f"CREATED {var.get()=}")

        r_buttons = []
        tv_vars = []
        for i, btn in enumerate(buttons):
            # print(f"{i=}, {btn=}, name=rbtn_{str(btn).lower()}, {master=}, {master.winfo_parent()=}, {type(master)=}")
            if is_tk_var(btn):
                tv_var = btn
            else:
                tv_var = tkinter.StringVar(master, value=btn)
            tv_vars.append(tv_var)
            if kwargs_buttons is not None:
                print(f"WARNING kwargs param is applied to each radio button")
                r_buttons.append(
                    tkinter.Radiobutton(master, variable=var, textvariable=tv_var, **kwargs_buttons, value=i,
                                        name=f"rbtn_{btn.replace('.', '_')}"))
            else:
                r_buttons.append(
                    tkinter.Radiobutton(master, variable=var, textvariable=tv_var, value=i,
                                        name=f"rbtn_{str(btn).lower().replace('.', '_')}")
                )

        # print(f"OUT {var.get()=}")
        return var, tv_vars, r_buttons
    else:
        raise Exception("Error, must pass a list of buttons.")

        # tv_sort_direction = StringVar(WIN, value="descending")
        # tv_sort_dir_a = StringVar(WIN, value="ascending")
        # tv_sort_dir_d = StringVar(WIN, value="descending")
        # rb_sda = Radiobutton(frame_rb_group_3, variable=tv_sort_direction, value="ascending", textvariable=tv_sort_dir_a)
        # rb_sdd = Radiobutton(frame_rb_group_3, variable=tv_sort_direction, value="descending", textvariable=tv_sort_dir_d)


def checkbox_factory(master, buttons, default_values=None, kwargs_buttons=None, rtype=list):
    if hasattr(buttons, '__iter__') and buttons:
        if not (isinstance(buttons, list) and isinstance(buttons, tuple)):
            buttons = list(buttons)
        if default_values is not None:
            if isinstance(default_values, list):
                tv_vars = [tkinter.BooleanVar(master, value=value) for value in default_values]
            else:
                raise Exception("Error, default_values must be a list of boolean values.")
        else:
            tv_vars = [tkinter.BooleanVar(master, False) for _ in buttons]

        c_buttons = []
        for i, btn in enumerate(buttons):
            func, arg = None, "w"
            if isinstance(btn, (list, tuple)) and (len(btn) > 1):
                if len(btn) == 3:
                    btn, func, arg = btn
                if len(btn) == 2:
                    btn, func, arg = *btn, "w"
                else:
                    raise ValueError(f"Parameter 'buttons' must be a list of strings indicating button names, or a list of lists or tuples of length 2 or 3 containing a string name and a single callable arg (name, func) or a callable arg and a trace_variable binding (name, func, 'w').")

            if kwargs_buttons is not None:
                print(f"WARNING kwargs param is applied to each checkbox button")
                c_buttons.append(
                    tkinter.Checkbutton(master, variable=tv_vars[i], text=btn, **kwargs_buttons))
            else:
                c_buttons.append(tkinter.Checkbutton(master, variable=tv_vars[i], text=btn))

            if func is not None:
                if callable(func):
                    tv_vars[i].trace_variable(arg, func)
                else:
                    raise ValueError(f"Received a non-callable function as a trace got button '{btn}'")

        if rtype in (list, tuple):
            return tv_vars, c_buttons
        else:
            return {btn if not isinstance(btn, (list, tuple)) else btn[0]: {"btn": c_buttons[i], "var": tv_vars[i]} for i, btn, in enumerate(buttons)}
    else:
        raise Exception("Error, must pass a list of buttons.")


class TreeviewExt(ttk.Treeview):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        # self.key_delim = "_|_=_|_=_|_"
        # self.col_keys = ["background", "foreground"]
        # self.colours = {}

    def treeview_sort_column(self, col, reverse):
        l = [(self.set(k, col), k) for k in self.get_children('')]
        l.sort(reverse=reverse)

        # rearrange items in sorted positions
        for index, (val, k) in enumerate(l):
            self.move(k, '', index)

        # reverse sort next time
        self.heading(col, command=lambda: \
            self.treeview_sort_column(col, not reverse))

    # def keyify(self, row, column):
    #     if self.key_delim in str(row):
    #         raise ValueError("Error, cannot use key_delim in the table it is a reserved string.")
    #     if self.key_delim in str(column):
    #         raise ValueError("Error, cannot use key_delim in the table it is a reserved string.")
    #     return f"{row}{self.key_delim}{column}"

    # def set(self, item, column=None, value=None, options=None):
    #     super().set(item, column, value)
    #     if self.key_delim in str(value):
    #         raise ValueError("Error, cannot use key_delim in the table it is a reserved string.")
    #
    #     if options:
    #         if not isinstance(options, dict):
    #             raise TypeError(f"Error, 'options' must either be none or a dictionary, got '{type(options)}'.")
    #
    #         key = self.keyify(item, column)
    #         self.colours.update({
    #             key: {k: options[k] for k in self.col_keys if k in options}
    #         })
    #
    #     print(f"{self.colours=}")


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
            show_index_column=True,
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

        # print(f"\n\nNEW TREEVIEW_CONTROLLER")

        self.master = master
        self.df = df.reset_index(drop=True)
        self.show_index_column = show_index_column
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
        self.cell_tag_delim = "|-=-=-=-|"
        self.row_tag_delim = "row="

        # self.iid_namer = (i for i in range(1000000))

        # print(f"--CC {self.viewable_column_names=}\n{self.df=}")
        cn = list(self.df.columns)
        if self.viewable_column_names is None:
            self.viewable_column_names = list(df.columns)
        elif isinstance(self.viewable_column_names, dict):
            # print(f"\tDICT PROCESSING")
            self.df = self.df.rename(columns=self.viewable_column_names)
            vcn = []
            for i, col in enumerate(cn):
                col_a = col
                if col in self.viewable_column_names:
                    col_a = self.viewable_column_names[col]
                    vcn.append(col_a)
            self.viewable_column_names = vcn

        # print(f"--AA {self.viewable_column_names=}\n{self.df=}")

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

        # self.viewable_column_names_indexable = {}

        # for i, col in enumerate(cn):
        # self.viewable_column_names_indexable[col] = "#" + col.replace(" ", "").strip()
        # self.viewable_column_names_indexable[col] = col
        # self.viewable_column_names_indexable[col] = f"#{i}"

        # # print(
        # #     f"AA {self.viewable_column_names=}\n{self.viewable_column_names_indexable.keys()=}\n{self.viewable_column_names_indexable.values()=}")
        # # for col in self.viewable_column_names:
        # #     print(f"\t{col}, {cn[cn.index(col)]=}")
        #     if isinstance(self.viewable_column_names, dict):
        #         col = self.viewable_column_names[col]
        #     # self.viewable_column_names_indexable[cn[cn.index(col)]] = col
        #     self.viewable_column_names_indexable[col] = "#" + col.replace(" ", "").strip()
        #     self.viewable_column_names_indexable[col] = "#"

        # print(f"BB {self.viewable_column_names=}\n{self.viewable_column_names_indexable.keys()=}\n{self.viewable_column_names_indexable.values()=}")

        self.label = tkinter.Label(self, textvariable=self.tv_label, **self.kwargs_label)
        self.treeview = TreeviewExt(
            self,
            # columns=list(self.viewable_column_names_indexable.values())
            # columns=self.viewable_column_names
            # , displaycolumns=self.viewable_column_names
            columns=self.viewable_column_names
            # ,displaycolumns=self.viewable_column_names_indexable
            , displaycolumns="#all"
            , **self.kwargs_treeview
            , show=("tree headings" if show_index_column else "headings")
            # , **kwargs
        )

        # print(f"==TC\n{self.df=}\n{viewable_column_names=}")

        # for i, col in enumerate(self.viewable_column_names_indexable):
        for i, col in enumerate(self.viewable_column_names):
            # if isinstance(self.viewable_column_names, dict):
            # col_i = self.viewable_column_names_indexable[col]
            # col_i = f"#{i}"
            col_i = col
            c_width = self.viewable_column_widths[i]
            # print(f"{c_width=}, {type(c_width)=}, {i=}, {col=}, {col_i=}")
            self.treeview.column(col_i, width=c_width, anchor=tkinter.CENTER)
            self.treeview.heading(col_i, text=col, anchor=tkinter.CENTER, command=lambda _col=col_i: \
                self.treeview.treeview_sort_column(_col, False))

        self.idx_width = 50
        if show_index_column:
            self.treeview.column("#0", width=self.idx_width, stretch=False)
            self.treeview.heading("#0", text="#", anchor=tkinter.CENTER)

        # print(f"--BB {df.shape=}\n{self.df}")
        # print(f"{list(df.itertuples())=}\n{len(list(df.itertuples()))}")
        # for i, row in df.itertuples():
        # f = list(range(1015))
        for i, row in self.df.iterrows():
            # next(self.iid_namer)
            # print(f"{i=}, {row=}, {type(row)=}")
            dat = [row[c_name] for c_name in self.viewable_column_names]
            tags = (self.gen_row_tag(i),)
            self.treeview.insert("", tkinter.END, text=f"{i + 1}", iid=i, values=dat, tags=tags)
            # print(f"{tags=}")
            # f.remove(i)
        # print(f"{f=}")
        # print(f"B {df.shape=}")
        # print(f"{len(list(df.iterrows()))=}")

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

        self.tv_button_new_item, self.button_new_item = button_factory(self, tv_btn="new cell_is_entry",
                                                                       kwargs_btn={
                                                                           "command": self.insert_new_random_entry})
        self.tv_button_delete_item, self.button_delete_item = button_factory(self, tv_btn="del cell_is_entry",
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

        self.binding_treeview_b1_motion = self.treeview.bind("<B1-Motion>", self.check_column_width_update)
        self.binding_treeview_b1 = self.treeview.bind("<Button-1>", self.stop_row_idx_resize)

    def gen_cell_tag(self, i, j):
        """12|-=-=-=-|12"""
        return f"{i}{self.cell_tag_delim}{j}"

    def gen_row_tag(self, i):
        """row=5"""
        return f"{self.row_tag_delim}{i}"

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
        # print(f"Treeview B1 Motion {column=}")
        if column:
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

    def insert_new_random_entry(self, index=tkinter.END):
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
        aggregate_data=None,
        show_index_column=True
):
    return \
        TreeviewController(
            master,
            dataframe,
            viewable_column_names,
            viewable_column_widths,
            tv_label,
            kwargs_label,
            kwargs_treeview,
            default_col_width,
            include_scroll_x,
            include_scroll_y,
            aggregate_data,
            show_index_column
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

        # bbox = self.canvas_stg.bbox("all")
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
        # self.tv_text.trace_variable("w", self.update_entry)
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
#                                                                                              tv_text=self.slider_red.value)
#         self.tv_label_green, self.label_green, self.tv_entry_green, self.entry_green = entry_factory(self,
#                                                                                                      tv_label="Green:",
#                                                                                                      tv_text=self.slider_green.value)
#         self.tv_label_blue, self.label_blue, self.tv_entry_blue, self.entry_blue = entry_factory(self, tv_label="Blue:",
#                                                                                                  tv_text=self.slider_blue.value)
#         self.tv_label_res, self.label_res, self.tv_entry_res, self.entry_res = entry_factory(self, tv_label="Result:",
#                                                                                              tv_text="Sample Text #123.")
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
#     def update_colour(self, var_name, index, game_mode):
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


# class CustomMessageBox:
#     # https://stackoverflow.com/questions/29619418/how-to-create-a-custom-messagebox-using-tkinter-in-python-with-changing-message
#     # root = Tk()
#     #
#     # def func():
#     #     a = CustomMessageBox(msg='Hello I m your multiline message',
#     #                    title='Hello World',
#     #                    b1='Button 1',
#     #                    b2='Button 2',
#     #                    )
#     #     print(a.choice)
#     #
#     # Button(root, text='Click Me', command=func).pack()
#     #
#     # root.mainloop()
#
#     def __init__(
#             self,
#             title='Mess',
#             msg='',
#             x=None,
#             y=None,
#             b1='OK',
#             b2='',
#             b3='',
#             b4='',
#             tab_colour="red",
#             bg_colour="blue",
#             bg_colour2="yellow",
#             text_colour="Green",
#             btn_font_colour="white",
#             close_btn_active_colour="red",
#             close_btn_active_font_colour="white",
#             w=500,
#             h=120,
#             font_message=("Helvetica", 9),
#             font_title=("Helvetica", 10, 'bold'),
#             font_x_btn=("Helvetica", 12),
#             font_btn=("Helvetica", 10)
#     ):
#
#         # Required Data of Init Function
#         self.title = title  # Is title of titlebar
#         self.msg = msg  # Is message to display
#         self.font_message = font_message
#         self.font_title = font_title
#         self.font_x_btn = font_x_btn
#         self.font_btn = font_btn
#         self.w = w
#         self.h = h
#         self.x = x if x is not None else 150
#         self.y = y if y is not None else 150
#         self.b1 = b1  # Button 1 (outputs '1')
#         self.b2 = b2  # Button 2 (outputs '2')
#         self.b3 = b3  # Button 3 (outputs '3')
#         self.b4 = b4  # Button 4 (outputs '4')
#         self.choice = ''  # it will be the return of messagebox according to button press
#
#         # Just the colors for my messagebox
#
#         self.tab_colour = tab_colour  # Button color for Active State
#         self.bg_colour = bg_colour  # Button color for Non-Active State
#         self.bg_color2 = bg_colour2  # Background color of Dialogue
#         self.text_colour = text_colour  # Text color for Dialogue
#         self.btn_font_colour = btn_font_colour
#         self.close_btn_active_colour = close_btn_active_colour
#         self.close_btn_active_font_colour = close_btn_active_font_colour
#
#         # Creating Dialogue for messagebox
#         self.root = tkinter.Toplevel()
#
#         # Removing titlebar from the Dialogue
#         self.root.overrideredirect(True)
#
#         # Setting Geometry
#         self.root.geometry(f"{self.w}x{self.h}+{self.x}+{self.y}")
#
#         # Setting Background color of Dialogue
#         self.root.config(bg=self.bg_color2)
#
#         # Creating Label For message
#         self.msg = tkinter.Label(self.root, text=msg,
#                                  font=self.font_message,
#                                  bg=self.bg_color2,
#                                  fg=self.text_colour,
#                                  # anchor='nw'
#                                  )
#         self.msg.place(x=self.w * 0.04, y=self.h * 0.15, height=self.h * 0.7, width=self.w * 0.92)
#
#         # Creating TitleBar
#         self.titlebar = tkinter.Label(self.root, text=self.title,
#                                       bg=self.bg_color2,
#                                       fg=self.text_colour,
#                                       bd=0,
#                                       font=self.font_title
#                                       )
#         self.titlebar.place(x=self.w * 0.35, y=5)
#
#         # Creating Close Button
#         self.CloseBtn = tkinter.Button(self.root,
#                                        text='x',
#                                        font=self.font_x_btn,
#                                        command=lambda: self.closed(),
#                                        bd=0,
#                                        activebackground=self.close_btn_active_colour,
#                                        activeforeground=self.close_btn_active_font_colour,
#                                        background=self.bg_color2,
#                                        foreground=self.text_colour)
#         self.CloseBtn.place(x=self.w - 50, y=5, width=40)
#
#         # Changing Close Button Color on Mouseover
#         self.CloseBtn.bind("<Enter>", lambda e,: self.CloseBtn.config(bg=self.close_btn_active_colour,
#                                                                       fg=self.close_btn_active_font_colour))
#         self.CloseBtn.bind("<Leave>", lambda e,: self.CloseBtn.config(bg=self.bg_color2, fg=self.text_colour))
#
#         ts = 5
#         dims = grid_cells(self.w, 4, 25, 1, ts, ts, y_0=90)
#         r1c1, r1c2, r1c3, r1c4 = dims[0]
#         # Creating B1
#         self.B1 = tkinter.Button(self.root, text=self.b1, command=self.click1,
#                                  bd=0,
#                                  font=self.font_btn,
#                                  bg=self.bg_colour,
#                                  fg=self.btn_font_colour,
#                                  activebackground=self.tab_colour,
#                                  activeforeground=self.text_colour)
#         self.B1.place(x=r1c1[0], y=r1c1[1], height=r1c1[3] - r1c1[1], width=r1c1[2] - r1c1[0])
#
#         # Getting place_info of B1
#         self.B1.info = self.B1.place_info()
#
#         # Creating B2
#         if not b2 == "":
#             self.B2 = tkinter.Button(self.root, text=self.b2, command=self.click2,
#                                      bd=0,
#                                      font=self.font_btn,
#                                      bg=self.bg_colour,
#                                      fg=self.btn_font_colour,
#                                      activebackground=self.tab_colour,
#                                      activeforeground=self.text_colour)
#             self.B2.place(x=r1c2[0], y=r1c2[1], height=r1c2[3] - r1c2[1], width=r1c2[2] - r1c2[0])
#         # Creating B3
#         if not b3 == '':
#             self.B3 = tkinter.Button(self.root, text=self.b3, command=self.click3,
#                                      bd=0,
#                                      font=self.font_btn,
#                                      bg=self.bg_colour,
#                                      fg=self.btn_font_colour,
#                                      activebackground=self.tab_colour,
#                                      activeforeground=self.text_colour)
#             self.B3.place(x=r1c3[0], y=r1c3[1], height=r1c3[3] - r1c3[1], width=r1c3[2] - r1c3[0])
#         # Creating B4
#         if not b4 == '':
#             self.B4 = tkinter.Button(self.root, text=self.b4, command=self.click4,
#                                      bd=0,
#                                      font=self.font_btn,
#                                      bg=self.bg_colour,
#                                      fg=self.btn_font_colour,
#                                      activebackground=self.tab_colour,
#                                      activeforeground=self.text_colour)
#             self.B4.place(x=r1c4[0], y=r1c4[1], height=r1c4[3] - r1c4[1], width=r1c4[2] - r1c4[0])
#
#         self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
#         # self.root.bind("<Configure>", self.update_configure)
#         # x = self.root.winfo_x()
#         # y = self.root.winfo_y()
#         # self.root.geometry('+{}+{}'.format(x+10, y+30))
#
#         # Making MessageBox Visible
#         self.root.wait_window()
#
#     def on_closing(self, *args):
#         self.closed()
#
#     # def update_configure(self, *args):
#     #     print(f"{args=}")
#     #     x = self.root.winfo_x()
#     #     y = self.root.winfo_y()
#     #     self.root.geometry('+{}+{}'.format(x, y))
#
#     # Function on Closeing MessageBox
#     def closed(self):
#         self.root.destroy()  # Destroying Dialogue
#         self.choice = 'closed'  # Assigning Value
#
#     # Function on pressing B1
#     def click1(self):
#         self.root.destroy()  # Destroying Dialogue
#         self.choice = '1'  # Assigning Value
#
#     # Function on pressing B2
#     def click2(self):
#         self.root.destroy()  # Destroying Dialogue
#         self.choice = '2'  # Assigning Value
#
#     # Function on pressing B3
#     def click3(self):
#         self.root.destroy()  # Destroying Dialogue
#         self.choice = '3'  # Assigning Value
#
#     # Function on pressing B4
#     def click4(self):
#         self.root.destroy()  # Destroying Dialogue
#         self.choice = '4'  # Assigning Value


class CustomMessageBox(tkinter.Toplevel):
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

    def __init__(self, title='Mess', msg='', x=None, y=None, b1='OK', b2='', b3='', b4='', tab_colour="red",
                 bg_colour="blue", bg_colour2="yellow", text_colour="Green", btn_font_colour="white",
                 close_btn_active_colour="red", close_btn_active_font_colour="white", w=500, h=120,
                 font_message=("Helvetica", 10), font_title=("Helvetica", 10, 'bold'), font_x_btn=("Helvetica", 12),
                 font_btn=("Helvetica", 10), btn_border_colour=Colour(TEAL).hex_code, btn_border_sel_colour="#d2d2d2",
                 answer_handle=None, ret_btn_text=False):

        # Required Data of Init Function
        super().__init__()
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
        self.ret_btn_text = ret_btn_text
        # self.choice = ''  # it will be the return of messagebox according to button press

        # Just the colors for my messagebox

        self.tab_colour = tab_colour  # Button color for Active State
        self.bg_colour = bg_colour  # Button color for Non-Active State
        self.bg_color2 = bg_colour2  # Background color of Dialogue
        self.text_colour = text_colour  # Text color for Dialogue
        self.btn_font_colour = btn_font_colour
        self.close_btn_active_colour = close_btn_active_colour
        self.close_btn_active_font_colour = close_btn_active_font_colour
        self.btn_border_colour = btn_border_colour
        self.btn_border_sel_colour = btn_border_sel_colour

        # Creating Dialogue for messagebox
        # self.root = tkinter.Toplevel()

        # Removing titlebar from the Dialogue
        self.overrideredirect(True)

        # Setting Geometry
        self.geometry(f"{self.w}x{self.h}+{self.x}+{self.y}")

        # Setting Background color of Dialogue
        self.config(bg=self.bg_color2)

        # Creating Label For message
        self.msg = tkinter.Label(
            self,
            text=msg,
            font=self.font_message,
            bg=self.bg_color2,
            fg=self.text_colour,
            # anchor='nw'
        )
        self.msg.place(x=self.w * 0.04, y=self.h * 0.15, height=self.h * 0.7, width=self.w * 0.92)

        # Creating TitleBar
        self.titlebar = tkinter.Label(self, text=self.title,
                                      bg=self.bg_color2,
                                      fg=self.text_colour,
                                      bd=0,
                                      font=self.font_title
                                      )
        self.titlebar.place(x=self.w * 0.35, y=5)

        # Creating Close Button
        self.CloseBtn = tkinter.Button(self,
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

        # https://stackoverflow.com/questions/47352833/no-way-to-color-the-border-of-a-tkinter-button
        # I am using linux and when I run your code, I get a button with a thick red border, so it looks like that the default Windows theme does not support highlightthickness while the default linux theme does.

        ts = 5
        dims = grid_cells(self.w, 4, int(self.h * 0.24), 1, ts, ts, y_0=int(self.h * 0.7))
        r1c1, r1c2, r1c3, r1c4 = dims[0]
        px, py = 3, 2
        self.f1 = tkinter.LabelFrame(self, name="lf1", borderwidth=3, bg=self.btn_border_colour)
        self.f2 = tkinter.LabelFrame(self, name="lf2", borderwidth=3, bg=self.btn_border_colour)
        self.f3 = tkinter.LabelFrame(self, name="lf3", borderwidth=3, bg=self.btn_border_colour)
        self.f4 = tkinter.LabelFrame(self, name="lf4", borderwidth=3, bg=self.btn_border_colour)
        # Creating B1
        self.B1 = tkinter.Button(
            self.f1,
            text=self.b1,
            command=self.click1,
            font=self.font_btn,
            bg=self.bg_colour,
            fg=self.btn_font_colour,
            activebackground=self.tab_colour,
            activeforeground=self.text_colour,
            width=int(r1c1[2] - r1c1[0]),
            bd=0,
            name="b1"
        )
        self.f1.place(x=r1c1[0], y=r1c1[1], height=r1c1[3] - r1c1[1], width=r1c1[2] - r1c1[0])
        self.B1.pack(padx=px, pady=py)

        # Getting place_info of B1
        self.f1.info = self.f1.place_info()

        # Creating B2
        if not b2 == "":
            self.B2 = tkinter.Button(
                self.f2,
                text=self.b2,
                command=self.click2,
                font=self.font_btn,
                bg=self.bg_colour,
                fg=self.btn_font_colour,
                activebackground=self.tab_colour,
                activeforeground=self.text_colour,
                width=int(r1c2[2] - r1c2[0]),
                bd=0,
                name="b2"
            )
            self.f2.place(x=r1c2[0], y=r1c2[1], height=r1c2[3] - r1c2[1], width=r1c2[2] - r1c2[0])
            self.B2.pack(padx=px, pady=py)
        # Creating B3
        if not b3 == '':
            self.B3 = tkinter.Button(
                self.f3,
                text=self.b3,
                command=self.click3,
                font=self.font_btn,
                bg=self.bg_colour,
                fg=self.btn_font_colour,
                activebackground=self.tab_colour,
                activeforeground=self.text_colour,
                width=int(r1c3[2] - r1c3[0]),
                bd=3,
                name="b3"
            )
            self.f3.place(x=r1c3[0], y=r1c3[1], height=r1c3[3] - r1c3[1], width=r1c3[2] - r1c3[0])
            self.B3.pack(padx=px, pady=py)
        # Creating B4
        if not b4 == '':
            self.B4 = tkinter.Button(
                self.f4,
                text=self.b4,
                command=self.click4,
                font=self.font_btn,
                bg=self.bg_colour,
                fg=self.btn_font_colour,
                activebackground=self.tab_colour,
                activeforeground=self.text_colour,
                bd=0,
                width=int(r1c4[2] - r1c4[0]),
                name="b4"
            )
            self.f4.place(x=r1c4[0], y=r1c4[1], height=r1c4[3] - r1c4[1], width=r1c4[2] - r1c4[0])
            self.B4.pack(padx=px, pady=py)

        self.destroy_funcs = [self.destroy]
        print(f"{answer_handle=}")
        self.choice = tkinter.StringVar(self, value="") if not is_tk_var(answer_handle) else answer_handle
        print(f"{self.choice=}, {self.choice.get()=}")

        self.btn_texts = [t for t in [self.b1, self.b2, self.b3, self.b4] if t]
        self.state_hover_btn = [v for v in self.btn_texts]
        self.state_hover_btn_i = list(range(len(self.btn_texts)))
        self.bind("<Return>", self.submit_return)
        self.bind("<Left>", self.click_left)
        self.bind("<Right>", self.click_right)
        self.select_btn(0)

        # if answer_handle is None:
        #     self.protocol("WM_DELETE_WINDOW", self.on_closing)
        # elif callable(answer_handle):
        #     self.destroy_funcs.insert(0, answer_handle)

        # self.root.bind("<Configure>", self.update_configure)
        # x = self.root.winfo_x()
        # y = self.root.winfo_y()
        # self.root.geometry('+{}+{}'.format(x+10, y+30))

        # # Making MessageBox Visible
        # self.root.wait_window()

    def submit_return(self, event):
        # print(f"SUBMIT!")
        # hovered = self.state_hover_btn_i[0]
        self.choice.set(self.state_hover_btn[0])
        self.destroy_handle()

    def select_btn(self, idx):
        # print(f"{self.state_hover_btn_i=}\n{self.state_hover_btn=}")
        if isinstance(idx, str):
            idx = lstindex(self.btn_texts, idx)
            if idx is None:
                raise ValueError(f"Error, key '{idx}' not found in this list.")
        lframe = eval(f"self.f{idx + 1}")
        # print(f"selecting {idx=}, {eval('self.B' + str(idx + 1))['text']=}, {lframe=}")
        lframe.configure(bg=self.btn_border_sel_colour)
        for i in self.state_hover_btn_i:
            # print(f"{i=}, {idx=}")
            if i != idx:
                # ix = self.state_hover_btn_i[i]
                if getattr(self, f"f{i + 1}", None) is not None:
                    lframe = eval(f"self.f{i + 1}")
                    # print(f"\treverting {i=}, {lframe=}")
                    lframe.configure(bg=self.btn_border_colour)

    def click_left(self, event):
        self.state_hover_btn = self.state_hover_btn[-1:] + self.state_hover_btn[:-1]
        self.state_hover_btn_i = self.state_hover_btn_i[-1:] + self.state_hover_btn_i[:-1]
        self.select_btn(self.state_hover_btn_i[0])

    def click_right(self, event):
        self.state_hover_btn = self.state_hover_btn[1:] + self.state_hover_btn[:1]
        self.state_hover_btn_i = self.state_hover_btn_i[1:] + self.state_hover_btn_i[:1]
        self.select_btn(self.state_hover_btn_i[0])

    def on_closing(self, *args):
        print(f"self closing")
        self.closed()

    def destroy_handle(self):
        for func in self.destroy_funcs:
            func()
        # self.answer_handle()

    # def update_configure(self, *args):
    #     print(f"{args=}")
    #     x = self.root.winfo_x()
    #     y = self.root.winfo_y()
    #     self.root.geometry('+{}+{}'.format(x, y))

    # Function on Closing MessageBox
    def closed(self):
        if self.ret_btn_text:
            self.choice.set("closed")  # Assigning Value
        else:
            self.choice.set("-1")  # Assigning Value
        self.destroy_handle()  # Destroying Dialogue

    # Function on pressing B1
    def click1(self):
        if self.ret_btn_text:
            self.choice.set(self.b1)  # Assigning Value
        else:
            self.choice.set("1")  # Assigning Value
        self.destroy_handle()  # Destroying Dialogue

    # Function on pressing B2
    def click2(self):
        if self.ret_btn_text:
            self.choice.set(self.b2)  # Assigning Value
        else:
            self.choice.set("2")  # Assigning Value
        self.destroy_handle()  # Destroying Dialogue

    # Function on pressing B3
    def click3(self):
        if self.ret_btn_text:
            self.choice.set(self.b3)  # Assigning Value
        else:
            self.choice.set("3")  # Assigning Value
        self.destroy_handle()  # Destroying Dialogue

    # Function on pressing B4
    def click4(self):
        if self.ret_btn_text:
            self.choice.set(self.b4)  # Assigning Value
        else:
            self.choice.set("4")  # Assigning Value
        self.destroy_handle()  # Destroying Dialogue


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

        # show cell_is_entry widget
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
                        self.update_has_focus_in)  # prevents duplicate event firing when typing directly into the cell_is_entry widget
        self.entry.bind("<FocusOut>", self.update_has_focus_out)

    def stop_listeners(self):
        if self.accepting_counter.trace_info():
            self.accepting_counter.trace_remove(*self.accepting_counter.trace_info()[0])
        if self.valid_submission.trace_info():
            self.valid_submission.trace_remove(*self.valid_submission.trace_info()[0])
        if self.text.trace_info():
            self.text.trace_remove(*self.text.trace_info()[0])

    def stop_bindings(self):
        # self.cell_is_entry.unbind("<Return>")
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
        # this is called when the cell_is_entry is ready to be read.
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
            f"WARNING, this forces all generic keyPress and Return key events through this widget.\nDo not use on a single form with multiple text / cell_is_entry input widgets.")
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
                 new_entry_defaults=None, lock_result_col=None, allow_insert_ask=True, viewable_column_widths=None,
                 include_aggregate_row=True, include_drop_down_arrow=True, drop_down_is_clicked=True,
                 include_searching_widgets=True, exhaustive_filtering=False, default_null_char="",
                 row_colour_bg=None, row_colour_fg=None, use_str_dtype: bool = True, nan_repr: str | None = None,
                 width: float | None = None, height: float | None = None, show_index_column: bool = True,
                 include_clear_button: bool = True
                 ):
        super().__init__(master)

        assert isinstance(data,
                          pandas.DataFrame), f"Error param 'data' must be an instance of a pandas.DataFrame, got '{type(data)}'."
        assert False if (kwargs_combo and (
                "values" in kwargs_combo)) else True, f"Cannot pass values as a keyword argument here. Pass all data in the data param as a pandas.DataFrame."
        # assert auto_pack + auto_grid <= 1, f"Error parameters 'auto_pack'={auto_pack} and 'auto_grid'={auto_grid} must be in a configuration where both params are not True.\nCannot grid and pack child widgets. (1 or None)"

        # print(f"{lock_result_col=}\n{viewable_column_names=}\n{data.columns=}")
        if lock_result_col is not None:
            assert ((lock_result_col in viewable_column_names) if isinstance(viewable_column_names, (list, tuple)) else (lock_result_col in viewable_column_names.values())) if viewable_column_names else ((
                                                                                                     lock_result_col in data.columns) if (
                        lock_result_col is not None) else True), f"Error column '{lock_result_col}' cannot be set as the locked result column. It is not in the list of viewable column names or in the list of columns in the passed dataframe."

        self.data = data
        self.use_str_dtype = use_str_dtype
        self.nan_repr = nan_repr

        # print(f"PRE\n{self.data=}")

        if self.nan_repr is not None:
            self.data = self.data.fillna(self.nan_repr)

        # print(f"POST\n{self.data=}")

        # convert the datatypes to string for all columns
        if self.use_str_dtype:
            for col_ in self.data.columns:
                self.data[col_] = self.data[col_].astype(str)

        if viewable_column_names is None:
            viewable_column_names = list(data.columns)
        else:
            # print(f"PRE=RENAME\n{self.data=}")
            self.data = self.data.rename(columns=viewable_column_names)
            # print(f"POST=RENAME\n{self.data=}")

        if None in viewable_column_names:
            raise ValueError(
                "Error, the None datatype cannot be the name of any column in the dataframe. This is a reserved keyword, please use 'None' as a string.")

        if len(viewable_column_names) == 1:
            new_entry_defaults = []
        # assert (
        #        new_entry_defaults is not None or allow_insert_ask) if not limit_to_list else 1, "Error, if allow new inserts to this combobox, then you must also either pass rest_values as 'new_entry_defaults' or set 'allow_insert_ask' to True.\nOtherwise there is no way to assign the rest of the column values."

        self.master = master
        self.namer = alpha_seq(10000000)
        self.top_most = patriarch(master)
        self.limit_to_list = limit_to_list
        self.p_allow_insert_ask = allow_insert_ask
        self.allow_insert_ask = False if limit_to_list else allow_insert_ask
        self.lock_result_col = lock_result_col
        self.inc_aggregate_row = include_aggregate_row
        self.include_drop_down_arrow = include_drop_down_arrow
        self.drop_down_is_clicked = drop_down_is_clicked
        self.include_searching_widgets = include_searching_widgets
        self.exhaustive_filtering = exhaustive_filtering
        self.default_null_char = default_null_char
        self.show_index_column = show_index_column
        self.include_clear_button = include_clear_button

        if not self.include_drop_down_arrow:
            # must show table, if this is false
            self.drop_down_is_clicked = True

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
        # print(f"PRE-TREE-CONTROLLER\n{self.data=}")
        # print(f"PRE-TREE-CONTROLLER\n{data=}")
        self.tree_controller = treeview_factory(
            self.frame_tree,
            data,
            kwargs_treeview={
                "selectmode": "browse",
                "height": height_in_rows
            },
            viewable_column_names=viewable_column_names,
            viewable_column_widths=viewable_column_widths,
            show_index_column=show_index_column
        )
        self.tree_controller, \
            self.tree_tv_label, \
            self.tree_label, \
            self.tree_treeview, \
            self.tree_scrollbar_x, \
            self.tree_scrollbar_y, \
            (self.tree_tv_button_new_item, self.tree_button_new_item), \
            (self.tree_tv_button_delete_item, self.tree_button_delete_item), \
            self.tree_aggregate_objects = self.tree_controller.get_objects()

        # print(f"PRE {self.tree_controller.df=}")
        if self.nan_repr is not None:
            self.tree_controller.df = self.tree_controller.df.fillna(self.nan_repr)
        # print(f"POST {self.tree_controller.df=}")

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

        if width is not None:
            if not (0 < width < 10000):
                raise ValueError(f"Parameter 'width' is out of range: '{width}'")
            self.configure(width=width)
        if height is not None:
            if not (0 < height < 10000):
                raise ValueError(f"Parameter 'width' is out of range: '{height}'")
            self.configure(height=height)

        self.tv_tree_is_hidden = tkinter.BooleanVar(self, value=not self.drop_down_is_clicked)

        self.frame_top_most.grid_columnconfigure(0, weight=9)
        self.frame_top_most.grid_columnconfigure(1, weight=1)
        self.frame_middle = tkinter.Frame(self, name="fm")
        self.radio_btn_texts = ["All", *self.tree_controller.viewable_column_names]
        if not self.show_index_column:
            self.radio_btn_texts.pop(0)
        self.rg_var, self.rg_tv_var, self.rg_btns = radio_factory(self.frame_middle,
                                                                  buttons=self.radio_btn_texts, default_value=0)
        self.rg_var.trace_variable("w", self.update_radio_group)
        self.trace_res_tv_entry = self.res_tv_entry.trace_variable("w", self.update_entry)
        self.typed_in = tkinter.BooleanVar(self, value=False)

        self.res_entry = tkinter.Entry(self.frame_top_most, textvariable=self.res_tv_entry, justify="center")
        self.tv_btn_clear = tkinter.StringVar(self, value="x")
        self.btn_clear = tkinter.Button(self.frame_top_most, textvariable=self.tv_btn_clear, command=self.click_btn_clear)
        # self.res_canvas = tkinter.Canvas(self.frame_top_most, width=20, height=20, background=rgb_to_hex("GRAY_62"))
        # self.res_canvas.create_line(11, 6, 11, 19, arrow=tkinter.LAST, arrowshape=(12, 12, 9))

        self.res_canvas = ArrowButton(self.frame_top_most, background=rgb_to_hex("GRAY_62"))

        self.bind_button1_res_camvas = self.res_canvas.bind("<Button-1>", self.click_canvas_dropdown_button)
        self.bind_treeview_select_tree_treeview = self.tree_treeview.bind("<<TreeviewSelect>>",
                                                                          self.treeview_selection_update)
        self.bind_key_res_entry = self.res_entry.bind("<Key>", self.update_typed_in)
        self.bind_return_res_entry = self.res_entry.bind("<Return>", self.submit_typed_in)

        self.returned_value = tkinter.StringVar(self, value="")

        x, y = 0, 0
        if isinstance(auto_grid, list) or isinstance(auto_grid, tuple):
            if len(auto_grid) == 2:
                x, y = auto_grid
            else:
                raise ValueError(f"Error, auto_grid param is not the right dimensions.")
        elif isinstance(auto_grid, int):
            x, y = 0, auto_grid
        if x < 0 or y < 0:
            raise ValueError(f"Error, auto_grid param is invalid.")
        self.grid_args = {
            "self": {"ipadx": 12, "ipady": 12},
            "self.res_label": {"row": 0, "column": 0},
            "self.frame_top_most": {"row": 1, "column": 0, "sticky": "ew"},
            "self.res_entry": {"row": 0, "column": 0, "sticky": "ew"},
            "self.res_canvas": {"row": 0, "column": 1}
        }

        if auto_grid:
            self.grid_widget()
        if not self.tv_tree_is_hidden.get():
            # print(f"NOT is hidden")
            self.tv_tree_is_hidden.set(True)
            self.click_canvas_dropdown_button(None)
        # else:
        #     print(f"is hidden")

        # print(f"Multicombobox created with dimensions (r x c)=({self.data.shape[0]} x {self.data.shape[1]})")

        # print(f"END SETUP {self.data=}")
        # print(f"END SETUP {self.tree_controller.df=}")

    def grid_widget(self, do_grid: bool = True):
        """Use this to appropriately place self and all sub widgets."""

        if not do_grid:
            self.grid_forget()
            self.res_label.grid_forget()
            self.frame_top_most.grid_forget()
            self.res_entry.grid_forget()
            self.res_canvas.grid_forget()
            self.btn_clear.grid_forget()
        else:
            self.grid(ipadx=12, ipady=12)
            # self.grid_columnconfigure(, weight=10)
            self.res_label.grid(row=0, column=0)

            if self.include_searching_widgets:
                self.frame_top_most.grid(row=1, column=0, sticky="ew")
                self.res_entry.grid(row=0, column=0, sticky="ew")
                self.btn_clear.grid(row=0, column=1)

            if self.include_drop_down_arrow:
                self.res_canvas.grid(row=0, column=1)
            else:
                if self.tv_tree_is_hidden.get():
                    self.click_canvas_dropdown_button(None)
        print(f"{do_grid=}, {self.include_searching_widgets=}, {self.include_drop_down_arrow=}, {self.tv_tree_is_hidden.get()=}")

    def click_btn_clear(self):
        self.res_tv_entry.set("")
        self.update_treeview()

    def set_cell_colours(self, i, j, bg_colour, fg_colour):
        # self.tree_treeview.tag_configure(f"{row}-{column}", background=bg_colour, foreground=fg_colour)
        # self.tree_treeview.tag_configure(f"{row}", background=bg_colour, foreground=fg_colour)
        # self.tree_treeview.tag_configure(f"{column}", background=bg_colour, foreground=fg_colour)
        self.tree_treeview.tag_configure(self.tree_controller.gen_cell_tag(i, j), background=bg_colour,
                                         foreground=fg_colour)
        # self.tree_treeview.set

    def set_row_colours(self, i, bg_colour, fg_colour):
        # self.tree_treeview.tag_configure(f"{row}-{column}", background=bg_colour, foreground=fg_colour)
        # self.tree_treeview.tag_configure(f"{row}", background=bg_colour, foreground=fg_colour)
        # self.tree_treeview.tag_configure(f"{column}", background=bg_colour, foreground=fg_colour)
        self.tree_treeview.tag_configure(self.tree_controller.gen_row_tag(i, +-j), background=bg_colour,
                                         foreground=fg_colour)

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

    def submit_typed_in(self, event, bypass=False):
        # print(f"submit_typed_in")
        children = self.tree_treeview.get_children()
        if children and not bypass:
            self.tree_treeview.selection_set(children[0])
        elif bypass or not children and not self.limit_to_list:
            val = self.res_tv_entry.get()
            col = self.tree_controller.viewable_column_names[self.rg_var.get()]
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
        print(f"{col=}")
        # self.filter_treeview()
        self.indexable_column = col
        self.update_typed_in(None)

    def delete_item(self, iid=None, value="|/|/||NONE||/|/|", mode="first" | Literal["first", "all", "ask"], error_on_not_found: bool = True):
        # print(f"delete_item: {iid=}, {value=}, {mode=}")
        # print(f"A self.data=\n{self.data}")
        delete_code = "|/|/||NONE||/|/|"
        if iid is None and value == delete_code:
            self.tree_treeview.delete(*self.tree_treeview.get_children())
            self.data = self.data.iloc[0:0]
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
                if not isinstance(value, (list, tuple)):
                    value = [value]
                value = value.copy()
                # # if not delete_multi:
                # #     value = value[:1]
                # print(f"{value=}")

                while value:
                    val = value.pop(0)
                    val_found = False
                    for i, row in self.data.iterrows():
                        if i in to_delete:
                            continue
                        for j, x in enumerate(row.values):
                            if val == x:
                                to_delete.append(i)
                                val_found = True
                                break
                            elif self.use_str_dtype and (str(val) == x):
                                to_delete.append(i)
                                val_found = True
                                break
                        if val_found:
                            break

                # for val in value:
                #     val_found = False
                #     # print(f"{val=}")
                #     for i, row in self.data.iterrows():
                #         for j, x in enumerate(row.values):
                #             if val == x:
                #                 to_delete.append(i)
                #                 val_found = True
                #                 break
                #             elif self.use_str_dtype and (str(val) == x):
                #                 to_delete.append(i)
                #                 val_found = True
                #                 break
                #         if val_found:
                #             break
                #
                #         # if to_delete and not delete_multi:
                #         #     break

                if to_delete:
                    # print(f"DROPPING #{len(to_delete)}, {to_delete=}")
                    # print(f"PRE  SHAPE: {self.data.shape=}")
                    # print(f"{self.data.head(5)}")
                    # print(f"{self.data.iloc[to_delete[0] - 3: to_delete[0] + 3]}")
                    self.data.drop(to_delete, inplace=True)
                    self.data.reset_index(drop=True, inplace=True)
                    # print(f"POST SHAPE: {self.data.shape=}")
                    # print(f"{self.data.head(5)}")
                    # print(f"{self.data.iloc[to_delete[0] - 3: to_delete[0] + 3]}")
                else:
                    if error_on_not_found:
                        raise ValueError(
                            f"Cannot delete row(s) containing value '{value}' from this dataframe. The value was not found was not Found.")

        # print(f"B self.data=\n{self.data}")
        self.update_treeview()

    def add_new_item(self, val, col=None, rest_values=None, rest_tags=None):
        # TODO support multiple values to be passed in iterable or dictionary fashion.

        cn = self.tree_controller.viewable_column_names
        # print(f"{self.data=}, {cn=}, {val=}, {col=}, {rest_values=}, {rest_tags=}")

        tags = set()
        i = self.data.shape[0]
        new_dfs = []

        if isinstance(val, pd.DataFrame):
            # print(f"DATAFRAME")

            if set(val.columns).difference(set(cn)) != set():
                raise ValueError("New dataframe cannot have unspecified columns from the original.")

            is_dict = False
            is_list = False
            if (is_list := isinstance(rest_tags, (tuple, list))) or (is_dict := isinstance(rest_tags, dict)):
                if is_dict:
                    for j, col_ in enumerate(cn):
                        tags.add(rest_tags.get(col_, self.tree_controller.gen_row_tag(i)))
                else:
                    if (l_rt := len(rest_tags)) != (l_cn := len(cn)):
                        if l_rt > l_cn:
                            raise ValueError(
                                f"Error, too many tags were passed for this table. Got {l_rt}, expected {l_cn}")
                        else:
                            raise ValueError(
                                f"Error, too few tags were passed for this table. Got {l_rt}, expected {l_cn}")
                    else:
                        [tags.add(tag) for tag in rest_tags]
            else:
                tags = [[self.tree_controller.gen_cell_tag(k, j) for j in range(len(cn))] for k in
                        range(i, i + val.shape[0])]

            new_dfs.append((val, [tup[1:] for tup in val.itertuples()], tags))
        else:
            print(f"SINGLE RECORD")

            if col is None:
                if hasattr(val, "__iter__") and not isinstance(val, str):
                    if len(val) == len(cn):
                        col = cn[0]
                    elif rest_values:
                        if (1 + len(rest_values)) == len(cn):
                            col = cn[0]
                        elif not self.limit_to_list or self.allow_insert_ask:
                            # allowed to insert later, choose the
                            if self.lock_result_col is not None:
                                col = self.lock_result_col
                            else:
                                col = cn[0]
                        else:
                            raise ValueError("Error, when 'col' is None, then 'rest_values' must cover the ")
                    else:
                        raise ValueError("Error, when 'col' is None, then the ")
                elif rest_values:
                    if (1 + len(rest_values)) == len(cn):
                        if isinstance(rest_values, dict):
                            col = set(cn).difference(set(rest_values)).pop()
                        else:
                            col = cn[0]
                    elif not self.limit_to_list and self.allow_insert_ask:
                        # allowed to insert later, choose the
                        if self.lock_result_col is not None:
                            col = self.lock_result_col
                        else:
                            col = cn[0]
                    else:
                        raise ValueError("Error, when 'col' is None, then 'rest_values' must cover the ")
                elif not self.limit_to_list and self.allow_insert_ask:
                    col = cn[0]
                else:
                    raise ValueError("Error, when 'col' is None, then the ")

            print(f"COL VAL IN {col=}")

            try:
                print(f"{cn=}, {col=}")
                idx = cn.index(col)
            except ValueError as ie:
                raise ValueError(
                    f"Column '{col}' is not a valid column name for this dataframe. Remember to use visible column names.")

            if (typ := type(val)) == dict:
                val_keys = set(val.keys())
                set_cn = set(cn)
                if val_keys.difference(set_cn):
                    # the dictionary 'val' has unknown column names.
                    raise KeyError(f"param 'val' has unknown column names.")

            elif typ in (list, tuple):
                if len(val) > len(cn):
                    # the list or tuple has too many positional values to insert
                    raise ValueError(f"param 'val' has too many values.")

            if val in self.invalid_inp_codes:
                self.throw_fit(val)
            print(f"{col=}")
            # idx = col
            # col = cn[col]
            # col = cn[0] if col == 0 else col
            # print(f"{type(rest_values)=}\n{rest_values=}")

            if not self.limit_to_list:
                if rest_values and (
                        isinstance(rest_values, (tuple, list, dict))):

                    is_dict = False
                    is_list = False
                    if (is_list := isinstance(rest_tags, (tuple, list))) or (is_dict := isinstance(rest_tags, dict)):
                        if is_dict:
                            for j, col_ in enumerate(cn):
                                tags.add(rest_tags.get(col_, self.tree_controller.gen_row_tag(i)))
                        else:
                            if (l_rt := len(rest_tags)) != (l_cn := len(cn)):
                                if l_rt > l_cn:
                                    raise ValueError(
                                        f"Error, too many tags were passed for this table. Got {l_rt}, expected {l_cn}")
                                else:
                                    raise ValueError(
                                        f"Error, too few tags were passed for this table. Got {l_rt}, expected {l_cn}")
                            else:
                                [tags.add(tag) for tag in rest_tags]
                    else:
                        tags = [self.tree_controller.gen_cell_tag(i, j) for j in range(len(cn))]

                    if isinstance(rest_values, list) or isinstance(rest_values, tuple):
                        row = list(rest_values)
                        row.insert(idx, val)
                        # self.data = self.data.append(pandas.DataFrame({k: [v] for k, v in zip(cn, row)}), ignore_index=True)
                        new_dfs.append((pandas.DataFrame({k: [v] for k, v in zip(cn, row)}), [row], [tags]))
                        # print(f"\nB\t{self.data=}").0
                        # self.tree_treeview.insert("", "end", iid=i, text=str(i + 1), values=row, tags=tuple(tags))
                        # self.res_entry.config(foreground="black")
                    else:
                        row = dict(rest_values)
                        row.update({col: val})
                        print(f"\n\trow:\n{row}\n\n\tcn\n{cn}\n>")
                        # self.data = self.data.append(pandas.DataFrame(row))
                        print(f"A\n\tData\n{self.data}\n{type(self.data)=}")
                        print(f"\n\tcols\n{self.data.columns}")
                        # print(f"DF 2:{pandas.DataFrame(row)}")
                        df1 = pandas.DataFrame([row], columns=list(row.keys()))
                        print(f"DF 1:{df1}\n{type(df1)=}")
                        # self.data = self.data.append(pandas.DataFrame([row], columns=row.keys()), ignore_index=True)
                        # self.data = self.data.append(df1, ignore_index=True)
                        # self.data = pd.concat([self.data, df1], ignore_index=True)
                        # print(f"B\n\tData\n{self.data}\n{type(self.data)=}")
                        # self.data = self.data.append(pandas.DataFrame(row))
                        row_vals = [row.get(c, self.default_null_char) for c in cn]
                        new_dfs.append((df1, [row_vals], [tags]))
                        cdvd = {k: [v] for k, v in zip(cn, row)}.values()
                        print(f"{row_vals=}")
                        print(f"{cn=}, {row=}")
                        print(f"{cdvd=}")
                        print(f"{list({k: [v] for k, v in zip(cn, row)}.values())=}")

                        # self.tree_treeview.insert("", "end", iid=i, text=str(i + 1),
                        #                           values=list({k: [v] for k, v in zip(cn, row)}.values()))

                        # self.tree_treeview.insert("", "end", iid=i, text=str(i + 1), values=row_vals, tags=tuple(tags))

                elif self.allow_insert_ask and not self.p_allow_insert_ask:
                    # prevents situations where an item can be inserted by typing. Will accept if and only if its column values are passed with it.
                    print(
                        f"Combobox is not limited to list contents, however, it is alos not allowed to ask for new values. You must pass default values.")
                elif self.allow_insert_ask:
                    ans = tkinter.messagebox.askyesnocancel("Create New Item",
                                                            message=f"Create a new combo box cell_is_entry with '{val}' in column '{col}' position?")
                    row = []
                    if ans == tkinter.YES:
                        tags = (self.tree_controller.gen_row_tag(i),)
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
                        # self.data = self.data.append(pandas.DataFrame({k: [v] for k, v in zip(cn, row)}), ignore_index=True)
                        # self.data = pd.concat([self.data, (pandas.DataFrame({k: [v] for k, v in zip(cn, row)}))],
                        #                       ignore_index=True)
                        # print(f"\nB\t{self.data=}")
                        new_dfs.append((pandas.DataFrame({k: [v] for k, v in zip(cn, row)}), [row], [tags]))
                        # self.tree_treeview.insert("", "end", iid=i, text=str(i + 1), values=list(row), tags=tuple(tags))
                        self.res_entry.config(foreground="black")

                        # i = self.data.shape[0]
                        # for df, vals, tags in new_dfs:
                        #     self.tree_treeview.insert("", "end", iid=i, text=str(i + 1), values=vals, tags=tuple(tags))
                        #     i += 1
                        # self.data = pd.concat(new_dfs, ignore_index=True)
                    else:
                        self.res_entry.config(foreground="red")
                elif len(self.tree_controller.viewable_column_names) == 1:
                    return
                else:
                    raise ValueError("Cannot insert into this combobox.")
            else:
                raise ValueError("Cannot insert into this combobox, 'limit_to_list' is True.")

        # print(f"PRE-INSERT")
        # print(f"{new_dfs=}")
        # print(f"{tags=}")
        # print(f"self.data={self.data}")
        k = self.data.shape[0]
        for df, vals, tags in new_dfs:
            if self.nan_repr is not None:
                df = df.fillna(self.nan_repr)
            for i, row in df.iterrows():
                vals_ = vals[i]
                tags_ = tags[i]
                # # for df_, vals_, tags_ in zip(df.iterrows(), vals, tags):
                #     print(f"INSERTING {vals_=}, {k+i=}, {tags_=}, {i=}")
                self.tree_treeview.insert("", "end", iid=k + i, text=str(k + i + 1), values=vals_, tags=tuple(tags_))
            k += df.shape[0]
        self.data = pd.concat([self.data, *[df for df, *rest in new_dfs]], ignore_index=True)

        if self.nan_repr is not None:
            self.tree_controller.df = self.tree_controller.df.fillna(self.nan_repr)
            self.data = self.data.fillna(self.nan_repr)

        # print(f"END==\n{self.data=}")

    # def add_new_item(self, val, col, rest_values=None, rest_tags=None):
    #     # TODO support multiple values to be passed in iterable or dictionary fashion.
    #
    #     cn = self.tree_controller.viewable_column_names
    #
    #     idx = cn.index(col)
    #     if (typ := type(val)) == dict:
    #         val_keys = set(val.keys())
    #         set_cn = set(cn)
    #         if val_keys.difference(set_cn):
    #             # the dictionary 'val' has unknown column names.
    #             raise KeyError(f"param 'val' has unknown column names.")
    #
    #     elif typ in (list, tuple):
    #         if len(val) > len(cn):
    #             # the list or tuple has too many positional values to insert
    #             raise ValueError(f"param 'val' has too many values.")
    #
    #     if val in self.invalid_inp_codes:
    #         self.throw_fit(val)
    #     print(f"{col=}")
    #     # idx = col
    #     # col = cn[col]
    #     # col = cn[0] if col == 0 else col
    #     tags = set()
    #     i = self.data.shape[0]
    #     # print(f"{type(rest_values)=}\n{rest_values=}")
    #     if not self.limit_to_list:
    #         if rest_values and (
    #                 isinstance(rest_values, (tuple, list, dict))):
    #
    #             is_dict = False
    #             is_list = False
    #             if (is_list := isinstance(rest_tags, (tuple, list))) or (is_dict := isinstance(rest_tags, dict)):
    #                 if is_dict:
    #                     for j, col_ in enumerate(cn):
    #                         tags.add(rest_tags.get(col_, self.tree_controller.gen_row_tag(i)))
    #                 else:
    #                     if (l_rt := len(rest_tags)) != (l_cn := len(cn)):
    #                         if l_rt > l_cn:
    #                             raise ValueError(
    #                                 f"Error, too many tags were passed for this table. Got {l_rt}, expected {l_cn}")
    #                         else:
    #                             raise ValueError(
    #                                 f"Error, too few tags were passed for this table. Got {l_rt}, expected {l_cn}")
    #                     else:
    #                         [tags.add(tag) for tag in rest_tags]
    #             else:
    #                 tags = [self.tree_controller.gen_cell_tag(i, j) for j in range(len(cn))]
    #
    #             if isinstance(rest_values, list) or isinstance(rest_values, tuple):
    #                 row = list(rest_values)
    #                 row.insert(idx, val)
    #                 self.data = self.data.append(pandas.DataFrame({k: [v] for k, v in zip(cn, row)}), ignore_index=True)
    #                 # print(f"\nB\t{self.data=}").0
    #                 self.tree_treeview.insert("", "end", iid=i, text=str(i + 1), values=row, tags=tuple(tags))
    #                 # self.res_entry.config(foreground="black")
    #             else:
    #                 row = dict(rest_values)
    #                 row.update({col: val})
    #                 print(f"\n\trow:\n{row}\n\n\tcn\n{cn}\n>")
    #                 # self.data = self.data.append(pandas.DataFrame(row))
    #                 print(f"A\n\tData\n{self.data}\n{type(self.data)=}")
    #                 print(f"\n\tcols\n{self.data.columns}")
    #                 # print(f"DF 2:{pandas.DataFrame(row)}")
    #                 df1 = pandas.DataFrame([row], columns=list(row.keys()))
    #                 print(f"DF 1:{df1}\n{type(df1)=}")
    #                 # self.data = self.data.append(pandas.DataFrame([row], columns=row.keys()), ignore_index=True)
    #                 # self.data = self.data.append(df1, ignore_index=True)
    #                 self.data = pd.concat([self.data, df1], ignore_index=True)
    #                 print(f"B\n\tData\n{self.data}\n{type(self.data)=}")
    #                 # self.data = self.data.append(pandas.DataFrame(row))
    #
    #                 row_vals = [row.get(c, self.default_null_char) for c in cn]
    #                 cdvd = {k: [v] for k, v in zip(cn, row)}.values()
    #                 print(f"{row_vals=}")
    #                 print(f"{cn=}, {row=}")
    #                 print(f"{cdvd=}")
    #                 print(f"{list({k: [v] for k, v in zip(cn, row)}.values())=}")
    #
    #                 # self.tree_treeview.insert("", "end", iid=i, text=str(i + 1),
    #                 #                           values=list({k: [v] for k, v in zip(cn, row)}.values()))
    #
    #                 self.tree_treeview.insert("", "end", iid=i, text=str(i + 1), values=row_vals, tags=tuple(tags))
    #
    #         elif self.allow_insert_ask and not self.p_allow_insert_ask:
    #             # prevents situations where an item can be inserted by typing. Will accept if and only if its column values are passed with it.
    #             print(
    #                 f"Combobox is not limited to list contents, however, it is alos not allowed to ask for new values. You must pass default values.")
    #         elif self.allow_insert_ask:
    #             ans = tkinter.messagebox.askyesnocancel("Create New Item",
    #                                                     message=f"Create a new combo box cell_is_entry with '{val}' in column '{col}' position?")
    #             row = []
    #             if ans == tkinter.YES:
    #                 tags = (self.tree_controller.gen_row_tag(i),)
    #                 # print(f"SELECTING {i=}")
    #                 column_names = self.tree_controller.viewable_column_names
    #                 for column in column_names:
    #                     if col != column:
    #                         if column in self.new_entry_defaults:
    #                             row.append(self.new_entry_defaults[column])
    #                         else:
    #                             ask_value = self.ask_value(column)
    #                             if ask_value in self.invalid_inp_codes:
    #                                 self.throw_fit(ask_value)
    #                             else:
    #                                 row.append(ask_value)
    #                     else:
    #                         row.append(val)
    #
    #                 # row = [(self.new_entry_defaults[col] if col in self.new_entry_defaults else self.ask_value(col)) for col in column_names]
    #                 # print(f"\nA\t{self.data=}")
    #                 # print(f"{pandas.DataFrame({k: [v] for k, v in zip(cn, row)})}")
    #                 # self.data = self.data.append(pandas.DataFrame({k: [v] for k, v in zip(cn, row)}), ignore_index=True)
    #                 self.data = pd.concat([self.data, (pandas.DataFrame({k: [v] for k, v in zip(cn, row)}))],
    #                                       ignore_index=True)
    #                 # print(f"\nB\t{self.data=}")
    #                 self.tree_treeview.insert("", "end", iid=i, text=str(i + 1), values=list(row), tags=tuple(tags))
    #                 self.res_entry.config(foreground="black")
    #             else:
    #                 self.res_entry.config(foreground="red")
    #         elif len(self.tree_controller.viewable_column_names) == 1:
    #             return
    #         else:
    #             raise ValueError("Cannot insert into this combobox")
    #     else:
    #         raise ValueError("Cannot insert into this combobox")
    #
    #     print(f"{tags=}")

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

    # def update_treeview(self):
    #     self.tree_treeview.delete(*self.tree_treeview.get_children())
    #     for i, row in self.data.iterrows():
    #         # print(f"{i=}, {row=}")
    #         tags =[self.tree_controller.gen_row_tag(i)]
    #         self.tree_treeview.insert("", "end", iid=i, text=str(i + 1), values=list(row), tags=tags)
    #         print(f"{tags=}")

    def update_treeview(self):
        self.tree_treeview.delete(*self.tree_treeview.get_children())
        # sic = self.show_index_column
        # for i, row in enumerate(self.data.itertuples(), 0):
        for i, data in self.data.iterrows():
            # print(f"{i=}, {data=}, {self.tree_controller.viewable_column_names=}")
            row = [data[k] for k in self.tree_controller.viewable_column_names]
            # print(f"{i=}, {row=}, {self.tree_controller.viewable_column_names=}")
            tags = [self.tree_controller.gen_row_tag(i)]
            # self.tree_treeview.insert("", "end", iid=i, text=str(i + 1), values=row[1:], tags=tags)
            self.tree_treeview.insert("", "end", iid=i, text=str(i + 1), values=row, tags=tags)
            # self.tree_treeview.set(str(i + 1), j, val, tags=)
            # print(f"{tags=}")

    def filter_treeview(self):
        # print(f"filter_treeview: {self.typed_in.get()}\n\n\tDATA\n{self.data}")
        if self.typed_in.get():
            val = self.res_tv_entry.get().lower()
            # print(f"SUBMISSION VAL {val=}")
            col = self.rg_var.get()
            col = self.radio_btn_texts[col]
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
                        # row = self.data.iloc[[i]].values
                        row = list(self.data.iloc[i][self.tree_controller.viewable_column_names])
                        # print(f"A {row=}")
                        # print(f"\t\t{i=}, {value=}, {row=}")
                        tags = tags = [self.tree_controller.gen_cell_tag(i, j) for j in
                                       range(len(self.tree_controller.viewable_column_names))]
                        self.tree_treeview.insert("", "end", iid=i, text=str(i + 1), values=row, tags=tags)
                        # print(f"{tags=}")
            else:
                # print(f"\n\nFilter Else")
                self.tree_treeview.delete(*self.tree_treeview.get_children())
                c = 0
                for i, row in self.data.iterrows():
                    found = False
                    for j, x in enumerate(row.values):
                        # print(f"\t\t{j=}, {x=} {val=} {val in str(x)=}")
                        if val in str(x).lower():
                            found = True
                            break
                    if found:
                        # print(f"BACK IN {i=}\t{row=}")
                        tags = [self.tree_controller.gen_cell_tag(i, j) for j in
                                range(len(self.tree_controller.viewable_column_names))]
                        row = list(self.data.iloc[i][self.tree_controller.viewable_column_names])
                        # print(f"B {row=}")
                        self.tree_treeview.insert("", "end", iid=i, text=i + 1, values=row, tags=tags)
                        # print(f"{tags=}")
                        c += 1
                        some = True
                    # print(f"{i=}\n{row=}\n{found=}")

            if self.exhaustive_filtering and not some:
                cn = self.tree_controller.viewable_column_names
                for i, row in self.data.iterrows():
                    do_break = False
                    # for j, x in enumerate(row.values):
                    for j, col_name in enumerate(cn):
                        # print(f"\t\t{j=}, {x=} {val=} {val in str(x)=}")
                        x = row[col_name]
                        if val in str(x).lower():
                            # print(f"FLASHING")
                            self.rg_btns[j + 1].flash()
                            do_break = True
                            break
                    if do_break:
                        break

                    # # self.tree_treeview.delete(*self.tree_treeview.get_children())
                    # # do_break = False
                    # if col != 0 and col != "All":
                    #     for j, value in enumerate(self.data[].tolist()):
                    #         # print(f"\t\t{i=}, {value=}")
                    #         if val in str(value).lower():
                    #             self.rg_btns[0].flash()
                    #             # do_break = True
                    #             break
                    # # if do_break:
                    # #     break
                    #         # some = True
                    #         # row = self.data.iloc[[i]].values
                    #         # print(f"\t\t{i=}, {value=}, {row=}")
                    #         # self.tree_treeview.insert("", "end", iid=i, text=str(i + 1), values=list(*row))

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

            if self.include_searching_widgets:
                for i, btn in enumerate(self.rg_btns):
                    btn.grid(row=0, column=i)

            self.tree_controller.grid(row=1, column=0)
            self.tree_treeview.grid(row=0, column=0)
            self.tree_scrollbar_x.grid(row=3, sticky="ew")
            self.tree_scrollbar_y.grid(row=0, column=1, sticky="ns")
            if self.inc_aggregate_row:
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
    def __init__(
            self,
            master,
            mode: Literal[
                "up", "down", "left", "right",
                "top-left", "top-right", "bottom-left", "bottom-right",
                "n", "s", "e", "w", "ne", "nw", "se", "sw",
                "N", "S", "E", "W", "NE", "NW", "SE", "SW"
            ] = "down",
            width: int = 20,
            height: int = 20,
            autogrid: bool = True,
            callback: Optional[Callable] = None,
            callback_binding: Literal[
                "<Button-1>", "<Button-2>", "<Button-3>"
            ] = "<Button-1>",
            *args, **kwargs
    ):
        super().__init__(master, width=width, height=height, *args, **kwargs)

        self.valid = {
            "up", "down", "left", "right",
            "top-left", "top-right", "bottom-left", "bottom-right",
            "n", "s", "e", "w", "ne", "nw", "se", "sw",
            "N", "S", "E", "W", "NE", "NW", "SE", "SW"
        }
        self.valid_btns = ("<Button-1>", "<Button-2>", "<Button-3>")
        mode = self.validate_mode(mode)
        binding = self.valid_btns[0] if (callback_binding not in self.valid_btns) else callback_binding

        self.mode = mode
        self.width = width
        self.height = height
        self.auto_grid = autogrid
        self.callback = callback
        self.callback_binding = binding

        self.configure(width=20, height=20, background=rgb_to_hex("GRAY_62"))

        if self.auto_grid:
            self.draw_arrow()
        # print(f"=={game_mode=} :: ({x1}, {y1}), ({x2}, {y2})")
        if self.callback is None:
            self.tag_bind_click_button = self.bind(self.callback_binding, self.click_canvas_button)
        else:
            self.tag_bind_click_button = self.bind(self.callback_binding, self.callback)

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
# canvas_stg = Canvas(root, width = 1000, height = 1000)
# canvas_stg.pack()
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
# canvas_stg = tkinter.Canvas(root)
# canvas_stg.pack()
# rounded_rect(canvas_stg, 20, 20, 60, 40, 10)
# root.mainloop()
def rounded_rect(canvas, x, y, w, h, c):
    assert isinstance(canvas,
                      tkinter.Canvas), f"Error param 'canvas_stg' must be a tkinter.Canvas object. Got '{canvas}', {type(canvas)=}"
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
            # print(f"init NOT switch game_mode")
            self.labels = labels  # (True part, False part)
            lbl_on, lbl_off = self.labels
            self.text_off = self.canvas.create_text(self.width * 0.25, self.height / 2, text=lbl_off,
                                                    fill=self.colour_fg_false, font=self.labels_font)
            self.text_on = self.canvas.create_text(self.width * 0.75, self.height / 2, text=lbl_on,
                                                   fill=self.colour_fg_true, font=self.labels_font)
        else:
            # print(f"init switch game_mode")
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

        x, y = 0, 0
        if not isinstance(auto_grid, bool):
            # print(f"A")
            if isinstance(auto_grid, list) or isinstance(auto_grid, tuple):
                # print(f"B")
                if len(auto_grid) == 2:
                    # print(f"C")
                    x, y = auto_grid
                else:
                    raise ValueError(f"Error, auto_grid param is not the right dimensions.")
            elif isinstance(auto_grid, int):
                print(f"D")
                x, y = 0, auto_grid
            if x < 0 or y < 0:
                raise ValueError(f"Error, auto_grid param is invalid.")
        # print(f"AAA {x=}, {y=}")
        self.grid_args = {
            "self": {"row": 0 + y, "column": 0 + x},
            "self.tv_label": {},
            "self.label": {"row": 0, "column": 0},
            "self.frame_canvas": {"row": 0, "column": 1},
            "self.state": {},
            "self.canvas_stg": {"row": 0, "column": 0}
        }

        if self.auto_grid is not None and self.auto_grid:
            self.grid_widgets()

    def grid_widgets(self):
        """Use this to grid self and all sub-widgets."""
        # print(f"Auto_grid '{self.tv_label.get()}'")
        # # self.grid(row=0, column=0)
        # self.grid()
        # self.label.grid(row=0, column=0)
        # self.frame_canvas.grid(row=0, column=1)
        # self.canvas_stg.grid(row=0, column=0)
        # dictionary = self.__dict__
        # print(f"{dictionary=}")
        for k, v in self.grid_args.items():
            if k != "self.state" and k != "self.tv_label":
                # print(f"{k=}")
                eval(f"{k}.grid(**{v})")
            # if isinstance(dictionary.get(k, None), tkinter.Widget):
            #     eval(f"{k}.grid(**{v})")
            # else:
            #     print(f"not a widget")

    def grid_forget_widgets(self):
        """Use this to grid self and all sub-widgets."""
        # self.grid(row=0, column=0)
        self.grid_forget()
        self.label.grid_forget()
        self.frame_canvas.grid_forget()
        self.canvas.grid_forget()

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
                # print(f"update NOT switch game_mode")
                self.canvas.itemconfigure(self.text_on, fill=fg_colour)
                self.canvas.itemconfigure(self.text_off, fill=fg_colour)
            else:
                # print(f"update switch game_mode")
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
        # Button, (Label_var, Label), canvas_frame, (State, canvas_stg)
        return (
            self,
            (self.tv_label, self.label),
            self.frame_canvas,
            (self.state, self.canvas)
        )


class TextWithVar(tkinter.Text):
    def __init__(self, master, textvariable=None, max_undos=100, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.text = textvariable
        if self.text is None:
            self.text = tkinter.StringVar(value=self.get("0.0", tkinter.END))
        self.trace = self.text.trace_variable("w", self._on_text_changed)

        self.max_undos = max_undos
        self.history = deque(maxlen=self.max_undos)
        self.history.append(self.text.get())

        self.scrollbar = ttk.Scrollbar(master, orient="vertical", command=self.yview)
        self.configure(yscrollcommand=self.scrollbar.set)

        self.bind("<Control-z>", self.undo)
        self.bind("<Control-Shift-z>", self.redo)
        self.bind("<KeyRelease>", self.key_up)

    def key_up(self, event):
        self.text.trace_remove("write", self.trace)
        self.text.set(self.get("0.0", tkinter.END))
        self.trace = self.text.trace_variable("w", self._on_text_changed)
        # nl = "\n"
        # print(f"KP '{event.char}', t='{self.get('0.0', tkinter.END).removesuffix(nl)}', txt:{self.text.get()}")

    def _on_text_changed(self, *args):
        self.delete("0.0", tkinter.END)
        self.insert("0.0", self.text.get())
        self.history.append(self.text.get())

    def set_text(self, new_text):
        self.text.set(new_text)

    def undo(self, event=None):
        if len(self.history) > 1:
            current_state = self.text.get()
            self.history.pop()  # Remove the current state
            previous_state = self.history.pop()
            self.text.set(previous_state)
            self.insert("0.0", self.text.get())  # Update the text widget
            self.history.append(previous_state)  # Add back the previous state
            self.history.append(current_state)  # Add the current state for redo
            return "break"  # Prevent default behavior of Ctrl+z
        return None

    def redo(self, event=None):
        if len(self.history) > 1:
            current_state = self.text.get()
            self.history.pop()  # Remove the current state (undo of undo)
            next_state = self.history.pop()
            self.text.set(next_state)
            self.insert("0.0", self.text.get())  # Update the text widget
            self.history.append(next_state)  # Add back the next state
            self.history.append(current_state)  # Add the current state for undo
            return "break"  # Prevent default behavior of Ctrl+y
        return None


# class TextWithVar(tkinter.Text):
#     def __init__(self, master, textvariable=None, max_undos=100, *args, **kwargs):
#         super().__init__(master, *args, **kwargs)
#         if textvariable is None:
#             textvariable = tkinter.StringVar(value=self.get("1.0", tkinter.END))
#         self.text = textvariable
#         self.text.trace_variable("w", self._on_text_changed)
#
#         self.max_undos = max_undos
#         self.history = deque(maxlen=self.max_undos)
#         self.history.append(self.text.get())
#
#         self.bind("<Control-z>", self.undo)
#         self.bind("<Control-y>", self.redo)
#
#     def _on_text_changed(self, *args):
#         self.delete("1.0", tkinter.END)
#         self.insert("1.0", self.text.get())
#
#     def set_text(self, new_text):
#         self.text.set(new_text)
#
#     def undo(self, event=None):
#         if len(self.history) > 1:
#             current_state = self.text.get()
#             self.history.pop()  # Remove the current state
#             previous_state = self.history.pop()
#             self.text.set(previous_state)
#             self.insert("1.0", self.text.get())  # Update the text widget
#             self.history.append(previous_state)  # Add back the previous state
#             self.history.append(current_state)  # Add the current state for redo
#             return "break"  # Prevent default behavior of Ctrl+z
#         return None
#
#     def redo(self, event=None):
#         if len(self.history) > 1:
#             current_state = self.text.get()
#             self.history.pop()  # Remove the current state (undo of undo)
#             next_state = self.history.pop()
#             self.text.set(next_state)
#             self.insert("1.0", self.text.get())  # Update the text widget
#             self.history.append(next_state)  # Add back the next state
#             self.history.append(current_state)  # Add the current state for undo
#             return "break"  # Prevent default behavior of Ctrl+y
#         return None


# class TextWithVar(tkinter.Text):
#     def __init__(self, master, textvariable=None, max_undos=100, *args, **kwargs):
#         super().__init__(master, *args, **kwargs)
#         if textvariable is None:
#             print(f"TextWithVar A")
#             textvariable = tkinter.StringVar(value=self.get("1.0", tkinter.END))
#         else:
#             if isinstance(textvariable, tkinter.StringVar):
#                 print(f"TextWithVar B")
#                 textvariable = textvariable
#             elif isinstance(textvariable, tkinter.Variable):
#                 print(f"TextWithVar C")
#                 textvariable = tkinter.StringVar(self, value=str(textvariable.get()))
#             else:
#                 print(f"TextWithVar D")
#                 textvariable = tkinter.StringVar(self, value=textvariable)
#
#         print(f"HELLO TEXT: '{textvariable.get()}'")
#
#         self.max_undos = clamp(0, max_undos, 1000)
#         self.history = deque(maxlen=self.max_undos)
#         self.text = textvariable
#         self.text.trace_variable("w", self.update_set_text)
#         self.bind("<<CustomTextChanged>>", self._on_text_changed)
#         self.bind("<Control-Return>", self.submit)
#         self.bind("<KeyRelease>", self.key_release)
#         self.history.append(self.text.get())
#
#         # Initialize the text widget if a initial value is passed with the StringVar.
#         if txt := self.text.get():
#             self.insert("1.0", txt, pass_thru=False)
#             # self.text.set(txt)
#
#     def submit(self, event):
#         print(f"submit")
#         print(f"{self.history=}")
#
#     def key_release(self, *event):
#         self.text.set(self.get("1.0", "end-1c"))
#         # self._update_text_variable()
#         # print(f"key_release TEXT='{self.text.get()}', T2='{}' {event=}")
#
#     def undo(self):
#         if len(self.history) > 1:
#             hist = self.history.pop()
#             hist = self.history.pop()
#             # print(f"hist='{hist}'")
#             self.text.set(hist)
#             return True
#         elif len(self.history):
#             hist = self.history.pop()
#             self.text.set(hist)
#             return True
#         else:
#             print("Nothing to undo.")
#             self.history.append('')
#             return False
#
#     # def update_set_text(self, *args):
#     #     # print(f"update_set_text, {self.text.get()=}")
#     #     self._on_text_changed(None, pass_thru=False)
#
#     def update_set_text(self, *args, pass_thru=True):
#         try:
#             if self.focus_get() == self:
#                 self.text.set(self.get("1.0", tkinter.END).rstrip())
#                 if not pass_thru:
#                     self.event_generate("<<CustomTextChanged>>")
#             else:
#                 print(f"does not have focus")
#         except KeyError as ke:
#             self._on_text_changed(None, pass_thru=False)
#
#     def _on_text_changed(self, event, pass_thru=True):
#         self.trim_history()
#         self.history.append(self.text.get())
#         self.delete("1.0", tkinter.END, pass_thru=pass_thru)
#         self.insert("1.0", self.text.get(), pass_thru=pass_thru)
#
#     def trim_history(self):
#         if len(self.history) >= self.max_undos:
#             self.history.popleft()
#
#     def insert(self, index, text, pass_thru=True):
#         super().insert(index, text)
#         if pass_thru:
#             self._update_text_variable()
#
#     def delete(self, index1, index2=None, pass_thru=True):
#         print(f"Delete: {index1=}, {index2=}, {pass_thru=}")
#         super().delete(index1, index2)
#         if pass_thru:
#             self._update_text_variable()
#
#     def _update_text_variable(self):
#         print(f"{self.text.get()=}")
#         self.text.set(self.get("1.0", tkinter.END))
#         self.event_generate("<<CustomTextChanged>>")


class TextWithVar_DON(tkinter.Text):
    '''A text widget that accepts a 'textvariable' option'''

    def __init__(self, parent, textvariable, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        try:
            self._textvariable = kwargs.pop("textvariable")
        except KeyError:
            self._textvariable = None

        # if the variable has data in it, use it to initialize
        # the widget
        if self._textvariable is not None:
            self.insert("1.0", self._textvariable.get())

        # this defines an internal proxy which generates a
        # virtual event whenever text is inserted or deleted
        self.tk.eval('''
            proc widget_proxy {widget widget_command args} {

                # call the real tk widget command with the real args
                set result [uplevel [linsert $args 0 $widget_command]]

                # if the contents changed, generate an event we can bind to
                if {([lindex $args 0] in {insert replace delete})} {
                    event generate $widget <<Change>> -when tail
                }
                # return the result from the real widget command
                return $result
            }
            ''')

        # this replaces the underlying widget with the proxy
        self.tk.eval('''
            rename {widget} _{widget}
            interp alias {{}} ::{widget} {{}} widget_proxy {widget} _{widget}
        '''.format(widget=str(self)))

        # set up a binding to update the variable whenever
        # the widget changes
        self.bind("<<Change>>", self._on_widget_change)

        # set up a trace to update the text widget when the
        # variable changes
        if self._textvariable is not None:
            self._textvariable.trace("wu", self._on_var_change)

    def _on_var_change(self, *args):
        '''Change the text widget when the associated textvariable changes'''

        # only change the widget if something actually
        # changed, otherwise we'll get into an endless
        # loop
        text_current = self.get("1.0", "end-1c")
        var_current = self._textvariable.get()
        if text_current != var_current:
            self.delete("1.0", "end")
            self.insert("1.0", var_current)

    def _on_widget_change(self, event=None):
        '''Change the variable when the widget changes'''
        if self._textvariable is not None:
            self._textvariable.set(self.get("1.0", "end-1c"))


# class InfoFrame(tkinter.Frame):
#
#     def __init__(
#             self,
#             master,
#             labels=None,
#             auto_grid=False,
#             key_width=10,
#             val_width=10,
#             header=None,
#             footer=None,
#             cell_border=None,
#             key_label_keywords=None,
#             value_label_keywords=None,
#             header_kwargs=None,
#             footer_kwargs=None,
#             formats=None,
#             allow_inserts=True,
#             *args, **kwargs
#     ):
#         super().__init__(master, *args, **kwargs)
#         self.auto_grid = auto_grid
#         self.header = header
#         self.footer = footer
#         self.header_kwargs = header_kwargs
#         self.footer_kwargs = footer_kwargs
#         self.allow_inserts = allow_inserts
#         self.grid_args = {}
#         self.labels_in = labels if (labels is not None) else dict()
#         self.info_labels = {}
#         self.key_gener = (i for i in range(1000000))
#         self.key_width = key_width
#         self.val_width = val_width
#         self.cell_border = cell_border
#         self.key_label_kwargs = key_label_keywords if key_label_keywords is not None else {}
#         self.val_label_kwargs = value_label_keywords if value_label_keywords is not None else {}
#
#         assert hasattr(self.labels_in,
#                        "__iter__"), f"Error param 'labels_in' must be an iterable. Got type='{type(self.labels_in)}'"
#         if not isinstance(self.labels_in, dict):
#             self.labels_in = dict(zip(self.labels_in, [None] * len(self.labels_in)))
#
#         self.formats = {}
#         if formats is None:
#             pass
#         elif isinstance(formats, dict):
#             for k, v in formats.items():
#                 if k in self.labels_in:
#                     self.formats.update({k: v})
#                 else:
#                     raise KeyError(f"Error key '{k}' is not a valid label for this infoframe.")
#         elif isinstance(formats, (list, tuple)):
#             for lbl, v in zip(self.labels_in, formats):
#                 self.formats.update({lbl: v})
#         else:
#             self.formats = {lbl: formats for lbl in self.labels_in}
#
#         # print(dict_print(self.formats, "formats"))
#
#         self.check_header()
#         self.check_footer()
#
#         hi = 1 if self.header is not None else 0
#         for i, k in enumerate(self.labels_in):
#             self.create_key(i + hi, k)
#
#         if self.auto_grid:
#             self.auto_grid_widgets()
#
#     def create_key(self, i, k, v=None):
#         r, c, rs, cs, ix, iy, x, y, s = self.grid_keys()
#         if isinstance(self.labels_in, dict):
#             gk = str(self.labels_in.get(k, ""))
#             if gk:
#                 k, v = str(k), gk
#             else:
#                 self.labels_in.update({k: v})
#         elif hasattr(k, "__iter__") and len(k) == 2:
#             k, v = map(str, k)
#         else:
#             k, v = str(k), ""
#
#         # ke = self.keyify(k)
#
#         self.check_border()
#         self.check_width()
#
#         k_tv, k_label = label_factory(
#             self,
#             tv_label=k,
#             kwargs_label=self.key_label_kwargs
#         )
#         v_tv, v_label = label_factory(
#             self,
#             tv_label=v,
#             kwargs_label=self.val_label_kwargs
#         )
#         ri = i
#         self.info_labels[k] = {
#             "k_tv": k_tv,
#             "k_label": k_label,
#             "v_tv": v_tv,
#             "v_label": v_label
#         }
#         self.grid_args[k] = {
#             "k_label": {r: ri, c: 0},
#             "v_label": {r: ri, c: 1}
#         }
#         print(f"({i}) finished making key {k=}, {v=}")
#
#     def check_border(self):
#         if "highlightthickness" not in self.key_label_kwargs and "highlightbackground" not in self.key_label_kwargs and "borderwidth" not in self.key_label_kwargs:
#             cb = 1 if self.cell_border is not None else 0
#             cc = None if cb != 1 else self.cell_border
#             if isinstance(cc, bool):
#                 cc = f"#000000"
#             self.key_label_kwargs.update({
#                 "borderwidth": 1,
#                 "highlightthickness": cb,
#                 "highlightbackground": cc
#             })
#
#         if "highlightthickness" not in self.val_label_kwargs and "highlightbackground" not in self.val_label_kwargs and "borderwidth" not in self.val_label_kwargs:
#             cb = 1 if self.cell_border is not None else 0
#             cc = None if cb != 1 else self.cell_border
#             if isinstance(cc, bool):
#                 cc = f"#000000"
#             self.val_label_kwargs.update({
#                 "borderwidth": 1,
#                 "highlightthickness": cb,
#                 "highlightbackground": cc
#             })
#
#     def check_width(self):
#         if "width" not in self.key_label_kwargs:
#             self.key_label_kwargs.update({
#                 "width": self.key_width
#             })
#         if "width" not in self.val_label_kwargs:
#             self.val_label_kwargs.update({
#                 "width": self.val_width
#             })
#
#     def check_header(self):
#         if self.header is not None:
#             r, c, rs, cs, ix, iy, x, y, s = self.grid_keys()
#             off_r, off_c = self.parse_auto_grid()
#             self.header = label_factory(
#                 self,
#                 tv_label=self.header,
#                 kwargs_label=self.header_kwargs
#             )
#             self.auto_grid = (off_r + 1, off_c)
#             self.grid_args["header"] = {r: 0, c: 0, rs: 1, cs: 2}
#
#     def check_footer(self):
#         if self.footer is not None:
#             r, c, rs, cs, ix, iy, x, y, s = self.grid_keys()
#             self.footer = label_factory(
#                 self,
#                 tv_label=self.footer,
#                 kwargs_label=self.footer_kwargs
#             )
#             ri = len(self.labels_in) + (1 if self.header is not None else 0)
#             self.grid_args["footer"] = {r: ri, c: 0, rs: 1, cs: 2}
#
#     # def keyify(self, label_name_in):
#     #     return f"k_{('000000' + str(next(self.key_gener)))[-6:]}_{label_name_in}"
#
#     # def de_keyify(self, key_in, new_value=None):
#     #     print(f"dekeying '{key_in}'")
#     #     print(f"{self.labels_in=}")
#     #     alike = []
#     #     ke = key_in.lower()
#     #     for k in self.info_labels:
#     #         if k.split("_")[-1].lower() == ke:
#     #             alike.append(k)
#     #
#     #     if not alike:
#     #         print(f"not alike")
#     #         if not self.allow_inserts:
#     #             raise KeyError(f"Error cannot find any keys that are alike the given key '{key_in}'")
#     #         else:
#     #             if isinstance(self.labels_in, dict):
#     #                 print(f"adding new item")
#     #                 self.labels_in.update({key_in: new_value})
#     #                 self.create_key(len(self.labels_in) + 1, key_in)
#     #                 if self.auto_grid is not None:
#     #                     self.info_labels[key_in]["k_label"].grid(**self.grid_args[key_in])
#     #                     self.info_labels[key_in]["v_label"].grid(**self.grid_args[key_in])
#     #             return key_in
#     #     else:
#     #         if len(alike) > 1:
#     #             print(
#     #                 f"WARNING de-keyify function found multiple keys with the given name '{key_in}', returning the first occurence.")
#     #         return alike[0]
#
#     def grid_keys(self):
#         return "row", "column", "rowspan", "columnspan", "ipadx", "ipady", "padx", "pady", "sticky"
#
#     def parse_auto_grid(self):
#         ag = self.auto_grid
#         off = 0 if isinstance(ag, bool) else ag
#         return (off, 0) if isinstance(off, int) else off
#
#     def auto_grid_widgets(self):
#         off_r, off_c = self.parse_auto_grid()
#         r, c, rs, cs, ix, iy, x, y, s = self.grid_keys()
#
#         self.grid_args.update({
#             ".": {r: off_r, c: off_c, cs: 1, rs: 1}
#         })
#
#         # print(dict_print(self.grid_args, "GA"))
#
#         for k in self.grid_args:
#             v = self.grid_args[k]
#             if k == ".":
#                 self.grid(**v)
#             elif k == "header":
#                 self.header[1].grid(**v)
#             elif k == "footer":
#                 self.footer[1].grid(**v)
#             else:
#                 # print(f"{self.grid_args[k]=}")
#                 self.info_labels[k]["k_label"].grid(**v["k_label"])
#                 self.info_labels[k]["v_label"].grid(**v["v_label"])
#
#     def grid_widgets(self, offset=None):
#         r, c = (0, 0) if offset is None else ((offset, 0) if isinstance(offset, int) else offset)
#         assert isinstance(r, int) and r >= 0, f"Error row offset value '{r}' is not valid for gridding"
#         assert isinstance(c, int) and c >= 0, f"Error column offset value '{c}' is not valid for gridding"
#         self.auto_grid = (r, c)
#         self.auto_grid_widgets()
#
#     def get_objects(self):
#         return self, *self.info_labels
#
#     def change_value(self, key: str | dict, value=None):
#         if isinstance(key, str):
#             data = {key: value}
#         else:
#             data = {k: v for k, v in key.items()}
#
#         for k, v in data.items():
#             if k not in self.info_labels:
#                 # print(f"de-keying")
#                 if not self.allow_inserts:
#                     raise KeyError(f"Error cannot find any keys that are alike the given key '{k}'")
#                 else:
#                     self.create_key(len(self.info_labels), k, v)
#                     if self.auto_grid is not None:
#                         self.info_labels[k]["k_label"].grid(**self.grid_args[k]["k_label"])
#                         self.info_labels[k]["v_label"].grid(**self.grid_args[k]["v_label"])
#             #         ke = key
#             #     # ke = self.de_keyify(key, new_value=value)
#             # else:
#             # ke = key
#
#             # val = value
#             if k in self.formats:
#                 fmt = self.formats[k]
#                 try:
#                     v = fmt(v)
#                 except Exception as e:
#                     print(f"FAILED TO FORMAT key='{k}'.")
#                     # v = v
#
#             self.info_labels[k]["v_tv"].set(v)
#
#     def get_value(self, key, default=None):
#         if key not in self.info_labels:
#             if not self.allow_inserts:
#                 raise KeyError(f"Error cannot find any keys that are alike the given key '{key_in}'")
#             else:
#                 self.create_key(len(self.info_labels), key, default)
#                 self.change_value(key, default)
#                 if self.auto_grid is not None:
#                     self.info_labels[key]["k_label"].grid(**self.grid_args[key]["k_label"])
#                     self.info_labels[key]["v_label"].grid(**self.grid_args[key]["v_label"])
#             # print(f"de-keying")
#             # try:
#             #     ke = self.de_keyify(key)
#             # except KeyError:
#             #     return default
#         # else:
#         #     ke = key
#         return self.info_labels[key]["v_tv"].get()


class InfoFrame(tkinter.Frame):

    def __init__(self, master, labels=None, auto_grid=False, key_width=10, val_width=10, header=None, footer=None,
                 cell_border=None, key_label_keywords=None, value_label_keywords=None, header_kwargs=None,
                 footer_kwargs=None, formats=None, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.auto_grid = auto_grid
        self.header = header
        self.footer = footer
        self.header_kwargs = header_kwargs
        self.footer_kwargs = footer_kwargs
        self.grid_args = {}
        self.labels_in = labels
        self.info_labels = {}
        self.key_gener = (i for i in range(1000000))
        self.key_width = key_width
        self.val_width = val_width
        self.cell_border = cell_border
        self.key_label_kwargs = key_label_keywords if key_label_keywords is not None else {}
        self.val_label_kwargs = value_label_keywords if value_label_keywords is not None else {}
        r, c, rs, cs, ix, iy, x, y, s = self.grid_keys()

        assert hasattr(self.labels_in,
                       "__iter__"), f"Error param 'labels_in' must be an iterable. Got type='{type(self.labels_in)}'"

        self.formats = {}
        if formats is None:
            pass
        elif isinstance(formats, dict):
            for k, v in formats.items():
                if k in self.labels_in:
                    self.formats.update({k: v})
                else:
                    raise KeyError(f"Error key '{k}' is not a valid label for this infoframe.")
        elif isinstance(formats, (list, tuple)):
            for lbl, v in zip(self.labels_in, formats):
                self.formats.update({lbl: v})
        else:
            self.formats = {lbl: formats for lbl in self.labels_in}

        # print(dict_print(self.formats, "formats"))

        self.frame_header = None
        self.check_header()
        self.check_footer()
        hi = 1 if self.header is not None else 0

        for i, k in enumerate(self.labels_in):
            if isinstance(self.labels_in, dict):
                k, v = str(k), str(self.labels_in[k])
            elif hasattr(k, "__iter__") and len(k) == 2:
                k, v = map(str, k)
            else:
                k, v = str(k), ""

            ke = self.keyify(k)

            self.check_border()
            self.check_width()

            k_tv, k_label = label_factory(
                self,
                tv_label=k,
                kwargs_label=self.key_label_kwargs
            )
            v_tv, v_label = label_factory(
                self,
                tv_label=v,
                kwargs_label=self.val_label_kwargs
            )
            ri = i + hi
            self.info_labels[ke] = {
                "k_tv": k_tv,
                "k_label": k_label,
                "v_tv": v_tv,
                "v_label": v_label
            }
            self.grid_args[ke] = {
                "k_label": {r: ri, c: 0},
                "v_label": {r: ri, c: 1}
            }

        if self.auto_grid:
            self.auto_grid_widgets()

    def check_border(self):
        if "highlightthickness" not in self.key_label_kwargs and "highlightbackground" not in self.key_label_kwargs and "borderwidth" not in self.key_label_kwargs:
            cb = 1 if self.cell_border is not None else 0
            cc = None if cb != 1 else self.cell_border
            if isinstance(cc, bool):
                cc = f"#000000"
            self.key_label_kwargs.update({
                "borderwidth": 1,
                "highlightthickness": cb,
                "highlightbackground": cc
            })

        if "highlightthickness" not in self.val_label_kwargs and "highlightbackground" not in self.val_label_kwargs and "borderwidth" not in self.val_label_kwargs:
            cb = 1 if self.cell_border is not None else 0
            cc = None if cb != 1 else self.cell_border
            if isinstance(cc, bool):
                cc = f"#000000"
            self.val_label_kwargs.update({
                "borderwidth": 1,
                "highlightthickness": cb,
                "highlightbackground": cc
            })

    def check_width(self):
        if "width" not in self.key_label_kwargs:
            self.key_label_kwargs.update({
                "width": self.key_width
            })
        if "width" not in self.val_label_kwargs:
            self.val_label_kwargs.update({
                "width": self.val_width
            })

    def check_header(self):
        if self.header is not None:
            r, c, rs, cs, ix, iy, x, y, s = self.grid_keys()
            off_r, off_c = self.parse_auto_grid()
            self.frame_header = tkinter.Frame(self)
            self.header = label_factory(
                self.frame_header,
                tv_label=self.header,
                kwargs_label=self.header_kwargs
            )
            self.auto_grid = (off_r + 1, off_c)
            self.grid_args["frame_header"] = {r: 0, c: 0, rs: 1, cs: 2}
            self.grid_args["header"] = {r: 0, c: 0, rs: 1, cs: 1}

    def check_footer(self):
        if self.footer is not None:
            r, c, rs, cs, ix, iy, x, y, s = self.grid_keys()
            self.footer = label_factory(
                self,
                tv_label=self.footer,
                kwargs_label=self.footer_kwargs
            )
            ri = len(self.labels_in) + (1 if self.header is not None else 0)
            self.grid_args["footer"] = {r: ri, c: 0, rs: 1, cs: 2}

    def keyify(self, label_name_in):
        return f"k_{('000000' + str(next(self.key_gener)))[-6:]}_{label_name_in}"

    def de_keyify(self, key_in):
        alike = []
        ke = key_in.lower()
        for k in self.info_labels:
            if k.split("_")[-1].lower() == ke:
                alike.append(k)

        if not alike:
            raise KeyError(f"Error cannot find any keys that are alike the given key '{key_in}'")
        else:
            if len(alike) > 1:
                print(
                    f"WARNING de-keyify function found multiple keys with the given name '{key_in}', returning the first occurence.")
            return alike[0]

    def grid_keys(self):
        return "row", "column", "rowspan", "columnspan", "ipadx", "ipady", "padx", "pady", "sticky"

    def parse_auto_grid(self):
        ag = self.auto_grid
        off = 0 if isinstance(ag, bool) else ag
        return (off, 0) if isinstance(off, int) else off

    def auto_grid_widgets(self):
        off_r, off_c = self.parse_auto_grid()
        r, c, rs, cs, ix, iy, x, y, s = self.grid_keys()

        self.grid_args.update({
            ".": {r: off_r, c: off_c, cs: 1, rs: 1}
        })

        # print(dict_print(self.grid_args, "GA"))

        for k in self.grid_args:
            v = self.grid_args[k]
            if k == ".":
                self.grid(**v)
            elif k == "frame_header":
                self.frame_header.grid(**v)
            elif k == "header":
                self.header[1].grid(**v)
            elif k == "footer":
                self.footer[1].grid(**v)
            else:
                # print(f"{self.grid_args[k]=}")
                self.info_labels[k]["k_label"].grid(**v["k_label"])
                self.info_labels[k]["v_label"].grid(**v["v_label"])

    def grid_widgets(self, offset=None):
        r, c = (0, 0) if offset is None else ((offset, 0) if isinstance(offset, int) else offset)
        assert isinstance(r, int) and r >= 0, f"Error row offset value '{r}' is not valid for gridding"
        assert isinstance(c, int) and c >= 0, f"Error column offset value '{c}' is not valid for gridding"
        self.auto_grid = (r, c)
        self.auto_grid_widgets()

    def get_objects(self):
        return self, *self.info_labels

    def change_value(self, key, value):
        if key not in self.info_labels:
            # print(f"de-keying")
            ke = self.de_keyify(key)
        else:
            ke = key

        val = value
        if key in self.formats:
            fmt = self.formats[key]
            try:
                val = fmt(value)
            except Exception as e:
                print(f"FAILED TO FORMAT key='{key}'.")
                val = value

        self.info_labels[ke]["v_tv"].set(val)

    def get_value(self, key, default=None):
        if key not in self.info_labels:
            # print(f"de-keying")
            try:
                ke = self.de_keyify(key)
            except KeyError:
                return default
        else:
            ke = key
        return self.info_labels[ke]["v_tv"].get()


def calc_geometry_tl(
        width: int | float,
        height: int | float = None,
        dims: None | tuple | list = None,
        largest: bool | int = True,
        rtype: str | dict | list | tuple = str,
        parent: tkinter.BaseWidget | tkinter.Toplevel | tkinter.Tk = None,
        do_print: bool = False,
        ask: bool = False,
        bypass_parent_withdraw: bool = False  # use for customtkinter and windows that are problematic to re-display
        # one_display_orient: Literal["horizontal", "vertical"]="horizontal"
) -> str | dict | list | tuple:

    x_off, y_off = 0, 0

    monitors = utility.get_largest_monitors()

    if dims is None:
        # monitors_lr = sorted(list(monitors), key=lambda m: m.x)
        if isinstance(largest, bool) and largest:
            monitor = monitors[0]
            largest = 1
        else:
            assert isinstance(largest, int), f"Error param 'largest' must be an integer."
            assert -1 < largest < len(
                monitors), f"Error param 'largest' must be in range {len(monitors)}. That is the maximum number of monitors you have."
            monitor = monitors[largest]
        x_, y_, width_, height_ = monitor.x, monitor.y, monitor.width, monitor.height

        # if treat_as_one_display:
        x_off = monitor.x
        y_off = monitor.y
        # if one_display_orient == "horizontal":
        #    x_off = monitor.x  # sum([m.width for m in monitors_lr[:largest]])
        # else:
        #    y_off = monitor.y  #  sum([m.height for m in monitors_lr[:largest]])
    else:
        x_, y_, width_, height_ = dims

    # print(f"{parent=}")
    if parent is not None:
        # a parent widget or window has been identified.
        # calculate this new geometry
        px, py = parent.winfo_rootx(), parent.winfo_rooty()
        # print(f"{px=}, {py=}")
        x_off = px
        y_off = py

        if len(monitors) > 1:
            if ask:

                idx = tkinter.IntVar(parent, value=0)

                def close_tl():
                    tl.destroy()

                def click(event, monitor_idx):
                    # print(f"click {event=}, {idx=}")
                    idx.set(monitor_idx)
                    close_tl()

                tl = tkinter.Toplevel(parent)
                w_w, h_w = 600, 200
                tl.geometry = calc_geometry_tl(w_w, h_w, parent=parent, ask=False)
                tl_canvas = tkinter.Canvas(tl, width=w_w, height=h_w)

                # print(f"{monitors=}")
                wx0 = monitors[0].x
                wx1 = monitors[-1].x + monitors[-1].height
                wy0 = min([m.y for m in monitors])
                wy1 = max([m.y + m.height for m in monitors])
                wwr = w_w / (wx1 - wx0)
                whr = h_w / (wy1 - wy0)
                for i, m in enumerate(monitors):
                    x0, y0 = (m.x - wx0), (m.y - wy0)
                    x1, y1 = (x0 + m.width) * wwr, (y0 + m.height) * whr
                    x0 *= wwr
                    y0 *= wwr
                    x0 = clamp(0, x0, w_w - ((len(monitors) - i) * 5))
                    y0 = clamp(0, y0, h_w - ((len(monitors) - i) * 5))
                    x1 = clamp(0, x1, w_w)
                    y1 = clamp(0, y1, h_w)
                    w, h = x1 - x0, y1 - y0
                    tr = tl_canvas.create_rectangle(x0, y0, x1, y1, fill="#AEAEAE")
                    tt = tl_canvas.create_text(x0 + (w / 2), y0 + (h / 2), fill="#000000", text=f"Monitor {i + 1}")
                    tl_canvas.tag_bind(tr, "<Button-1>", lambda event, i_=i: click(event, i_))
                    tl_canvas.tag_bind(tt, "<Button-1>", lambda event, i_=i: click(event, i_))

                # gc = grid_cells(w_w, len(monitors), h_w, 1, r_type=list, x_pad=10, y_pad=5)[0]
                # print(f"{monitors=}")
                # for i, m in enumerate(monitors):
                #     tr = tl_canvas.create_rectangle(*gc[i], fill="#AEAEAE")
                #     x0, y0, x1, y1 = gc[i]
                #     w, h = x1 - x0, y1 - y0
                #     tt = tl_canvas.create_text(x0 + (w/2), y0 + (h/2), fill="#000000", text=f"Monitor {i+1}")
                #     tl_canvas.tag_bind(tr, "<Button-1>", lambda event, i_=i: click(event, i_))
                #     tl_canvas.tag_bind(tt, "<Button-1>", lambda event, i_=i: click(event, i_))

                tl_canvas.grid()
                tl.protocol("WM_DELETE_WINDOW", close_tl)
                tl.grab_set()
                if not bypass_parent_withdraw:
                    parent.withdraw()
                parent.wait_window(tl)
                if not bypass_parent_withdraw:
                    parent.deiconify()

                monitor = monitors[idx.get()]
                x_, y_, width_, height_ = monitor.x, monitor.y, monitor.width, monitor.height
                x_off = monitor.x
                y_off = monitor.y

    else:
        if ask:
            raise ValueError(f"Cannot use param 'ask' when 'parent' is not supplied. The 'ask' param is used to create a brief TopLevel to ask which monitor you want to use. Therefore, 'parent' must be a valid instance of (tkinter.BaseWidget | tkinter.Toplevel | tkinter.Tk)")

    t_width, t_height = width_, height_

    if height is None:
        height = width

    if isinstance(height, float):
        assert 0 < height <= 1, "Error, if param 'height' is a float, it must be between 0 and 1."
        height = int(height * height_)

    if isinstance(width, float):
        assert 0 < width <= 1, "Error, if param 'width' is a float, it must be between 0 and 1."
        width = int(width * width_)

    p_a = width == "zoomed"
    p_b = height == "zoomed"
    if p_a or p_b:
        if do_print:
            print(f"A, {p_a=}, {p_b=}")

        if p_a:
            height_o = height_ if p_b else height
            x_ = 0
            height_c = clamp(1, height_o, height_)
            y_ = (height_ - height_c) // 2
            height_ = height_c

        if p_b:
            width_o = width_ if p_a else width
            y_ = 0
            width_c = clamp(1, width_o, width_)
            x_ = (width_ - width_c) // 2
            width_ = width_c
    else:
        if do_print:
            print(f"B")
        width_c = clamp(1, width, width_)
        height_c = clamp(1, height, height_)
        x = (width_ - width_c) // 2
        y = (height_ - height_c) // 2
        x_, y_, width_, height_ = x, y, width_c, height_c

    x_ += x_off
    y_ += y_off

    if width == height == "zoomed":
        res = "zoomed"
    else:
        res = f"{width_}x{height_}+{x_}+{y_}"

    if do_print:
        print(f"x={x_}, y={y_}, w={width_}, h={height_}, {x_off=}, {y_off=}" + f" geo=({res})")
    if rtype == str:
        return res
    elif rtype == dict:
        return {"x": x_, "y": y_, "width": width_, "height": height_, "x1": x_, "y1": y_, "x2": x_ + width_,
                "y2": y_ + height_, "str": res, str: res, "geometry": res, str: res, "res": res, str: res}
    else:
        return [x_, y_, width_, height_]


def auto_font(font, text, c_width, c_height, min_font_size=4, max_font_size=300):
    """Clamp a font's size between c_width, and c_height when rendering text in pixels."""

    assert isinstance(min_font_size, int) and (
            3 < min_font_size < 301), f"Error param 'min_font_size' must be an integer between 4 and 301 exclusive."
    assert isinstance(max_font_size, int) and (
            3 < max_font_size < 301), f"Error param 'max_font_size' must be an integer between 4 and 301 exclusive."
    assert min_font_size <= max_font_size, f"Error param 'min_font_size' cannot be larger than param 'max_font_size'."

    width = font.measure(text)
    family = font.actual()["family"]
    size = font.actual()["size"]
    ls = font.metrics()["linespace"]
    # print(f"{family=}, {size=}, {ls=}, {font=}")
    while size < max_font_size:
        # font = tkinter.font.Font(family=family, size=size)
        font.configure(size=size)
        width = font.measure(text)
        ls = font.metrics()["linespace"]
        c_a = (width * ls) >= (c_width * c_height)
        c_w = (width >= c_width)
        c_h = (ls >= c_height)
        # print(f"{ls=}, {width=}, {c_width=}, {c_height=}, {width*ls=}, {c_width*c_height=}, {c_a=}, {c_w=}, {c_h=}")
        if c_a or c_w or c_h:
            break
        size += 1
        # print(f"\tgrow {size=}")
    while size > min_font_size:
        # font = tkinter.font.Font(family=family, size=size)
        font.configure(size=size)
        width = font.measure(text)
        ls = font.metrics()["linespace"]
        c_a = (width * ls) <= (c_width * c_height)
        c_w = (width <= c_width)
        c_h = (ls <= c_height)
        # print(f"{ls=}, {width=}, {c_width=}, {c_height=}, {width*ls=}, {c_width*c_height=}, {c_a=}, {c_w=}, {c_h=}")
        if c_a or c_w or c_h:
            break
        size -= 1
        # print(f"\tshrink {size=}")

    # ls = font.metrics()["linespace"]
    # print(f"FINAL {family=}, {size=}, {ls=}, {font=}")
    return font


class ToggleCanvas(tkinter.Canvas):

    def __init__(
            self,
            master,
            option_a: str | list[str, str] | tuple[str, str] = "On",
            option_b: str | None = None,
            default_value: int | None = None,
            width: int = 100,
            height: int = 20,
            colour_background: str | Colour = "#BBBBCE",
            colour_divider: str | Colour = "#000000",
            colour_text_option_a: str | Colour = "#9F0808",
            colour_text_option_b: str | Colour = "#089F08",
            colour_option_a: str | None | Colour = None,
            colour_option_b: str | None | Colour = None,
            font_text_option_a: str | Tuple[str, int] = "Arial 16",
            font_text_option_b: str | Tuple[str, int] = "Arial 16",
            auto_grid: bool = True,
            margin_rect_w: int = 2,
            margin_rect_h: int = 2,
            width_divider: int = 3,
            p_bright: float = 0.15
    ):
        super().__init__(master)

        if not (0 < width < 10000):
            raise ValueError(f"Parameter 'width' is out of range: '{width}'")
        if not (0 < height < 10000):
            raise ValueError(f"Parameter 'height' is out of range: '{height}'")

        if not (0.05 < p_bright < 0.9):
            raise ValueError(f"Parameter 'p_bright' is out of range: '{p_bright}'")

        if isinstance(option_a, (list, tuple)):
            option_b = None

        if option_b is None:
            if isinstance(option_a, (list, tuple)):
                if len(option_a) != 2:
                    raise ValueError(f"Parameter 'option_a' can be a single string or a list or tuple of length 2.")
                option_a, option_b = option_a
            elif option_a.lower() == "on":
                option_b = "Off"
            else:
                option_b = f"Not {option_a}"

        self.width = width
        self.height = height
        self.option_a = option_a
        self.option_b = option_b
        self.colour_background = colour_background if isinstance(colour_background, Colour) else Colour(colour_background)
        self.colour_divider = colour_divider if isinstance(colour_divider, Colour) else Colour(colour_divider)
        self.colour_text_option_a = colour_text_option_a if isinstance(colour_text_option_a, Colour) else Colour(colour_text_option_a)
        self.colour_text_option_b = colour_text_option_b if isinstance(colour_text_option_b, Colour) else Colour(colour_text_option_b)
        self.colour_option_a = colour_option_a if isinstance(colour_option_a, Colour) else (Colour(colour_option_a) if colour_option_a is not None else self.colour_background)
        self.colour_option_b = colour_option_b if isinstance(colour_option_b, Colour) else (Colour(colour_option_b) if colour_option_b is not None else self.colour_background)
        self.font_text_option_a = font_text_option_a
        self.font_text_option_b = font_text_option_b

        self.margin_rect_w = margin_rect_w
        self.margin_rect_h = margin_rect_h
        self.width_divider = width_divider
        self.p_bright = p_bright

        self.configure(
            width=self.width,
            height=self.height,
            background=self.colour_background.hex_code
        )

        self.default_value = default_value
        if default_value is not None:
            if default_value not in [self.option_a, self.option_b]:
                raise ValueError(f"Error with default value '{default_value}' it is not recognized as option.")

        self.value = tkinter.StringVar(self, value=default_value)

        self.rect_option_a = self.create_rectangle(
            self.margin_rect_w,
            self.margin_rect_h,
            (self.width / 2) - self.margin_rect_w,
            self.height - self.margin_rect_h,
            fill=self.colour_option_a.hex_code,
            outline=self.colour_option_b.hex_code,
            activefill=self.colour_option_a.brightened(self.p_bright).hex_code,
            activeoutline=self.colour_option_b.brightened(self.p_bright).hex_code
        )

        self.rect_option_b = self.create_rectangle(
            (self.width / 2) + self.margin_rect_w,
            self.margin_rect_h,
            self.width - self.margin_rect_w,
            self.height - self.margin_rect_h,
            fill=self.colour_option_b.hex_code,
            outline=self.colour_option_b.hex_code,
            activefill=self.colour_option_b.brightened(self.p_bright).hex_code,
            activeoutline=self.colour_option_b.brightened(self.p_bright).hex_code
        )

        self.line_divider = self.create_line(
            self.width / 2,
            self.height * 0.1,
            self.width / 2,
            self.height * 0.9,
            fill=self.colour_divider.hex_code,
            width=self.width_divider
        )

        self.tag_option_a = self.create_text(
            self.width * 0.25,
            self.height * 0.5,
            text=self.option_a,
            fill=self.colour_text_option_a.hex_code,
            font=self.font_text_option_a
        )

        self.tag_option_b = self.create_text(
            self.width * 0.75,
            self.height * 0.5,
            text=self.option_b,
            fill=self.colour_text_option_b.hex_code,
            font=self.font_text_option_b
        )

        self.auto_grid = auto_grid
        if self.auto_grid:
            self.auto_grid_widgets()

        self.tag_bind(self.rect_option_a, "<Button-1>", self.click_option_a)
        self.tag_bind(self.tag_option_a, "<Button-1>", self.click_option_a)
        self.tag_bind(self.tag_option_a, "<Enter>", self.enter_option_a)
        self.tag_bind(self.tag_option_a, "<Leave>", self.leave_option_a)

        self.tag_bind(self.rect_option_b, "<Button-1>", self.click_option_b)
        self.tag_bind(self.tag_option_b, "<Button-1>", self.click_option_b)
        self.tag_bind(self.tag_option_b, "<Enter>", self.enter_option_b)
        self.tag_bind(self.tag_option_b, "<Leave>", self.leave_option_b)

        if self.default_value is not None:
            if self.default_value.lower() == self.option_a.lower():
                self.click_option_a()
            elif self.default_value.lower() == self.option_b.lower():
                self.click_option_b()

    def auto_grid_widgets(self):
        # auto_grid_widgets
        self.grid()

    def click_option_a(self, event=None):
        # print(f"click_option_a")
        self.value.set(self.option_a)
        self.itemconfigure(
            self.rect_option_a,
            fill=self.colour_option_a.darkened(self.p_bright).hex_code,
            outline=self.colour_option_a.darkened(self.p_bright).hex_code,
            activefill=self.colour_option_a.darkened(self.p_bright).hex_code,
            activeoutline=self.colour_option_a.darkened(self.p_bright).hex_code
        )
        self.itemconfigure(
            self.rect_option_b,
            fill=self.colour_option_b.hex_code,
            outline=self.colour_option_b.hex_code,
            activefill=self.colour_option_b.brightened(self.p_bright).hex_code,
            activeoutline=self.colour_option_b.brightened(self.p_bright).hex_code
        )

    def click_option_b(self, event=None):
        # print(f"click_option_b")
        self.value.set(self.option_b)
        self.itemconfigure(
            self.rect_option_a,
            fill=self.colour_option_a.hex_code,
            outline=self.colour_option_a.hex_code,
            activefill=self.colour_option_a.brightened(self.p_bright).hex_code,
            activeoutline=self.colour_option_a.brightened(self.p_bright).hex_code
        )
        self.itemconfigure(
            self.rect_option_b,
            fill=self.colour_option_b.darkened(self.p_bright).hex_code,
            outline=self.colour_option_b.darkened(self.p_bright).hex_code,
            activefill=self.colour_option_b.darkened(self.p_bright).hex_code,
            activeoutline=self.colour_option_b.darkened(self.p_bright).hex_code
        )

    def enter_option_a(self, event):
        # print(f"enter_option_a {self.value.get()=}, {self.option_a=}")
        c = self.colour_option_a
        b = c.brightened(self.p_bright)
        d = c.darkened(self.p_bright)
        self.itemconfigure(
            self.rect_option_a,
            fill=(b if (self.value.get() != self.option_a) else d).hex_code,
            outline=(b if (self.value.get() != self.option_a) else d).hex_code
        )

    def leave_option_a(self, event):
        # print(f"leave_option_a {self.value.get()=}, {self.option_a=}")
        c = self.colour_option_a
        b = c.brightened(self.p_bright)
        d = c.darkened(self.p_bright)
        self.itemconfigure(
            self.rect_option_a,
            fill=(c if (self.value.get() != self.option_a) else d).hex_code,
            outline=(c if (self.value.get() != self.option_a) else d).hex_code
        )

    def enter_option_b(self, event):
        # print(f"enter_option_b {self.value.get()=}, {self.option_b=}")
        c = self.colour_option_b
        b = c.brightened(self.p_bright)
        d = c.darkened(self.p_bright)
        self.itemconfigure(
            self.rect_option_b,
            fill=(b if self.value.get() != self.option_b else d).hex_code,
            outline=(b if self.value.get() != self.option_b else d).hex_code
        )

    def leave_option_b(self, event):
        # print(f"leave_option_b {self.value.get()=}, {self.option_b=}")
        c = self.colour_option_b
        b = c.brightened(self.p_bright)
        d = c.darkened(self.p_bright)
        self.itemconfigure(
            self.rect_option_b,
            fill=(c if (self.value.get() != self.option_b) else d).hex_code,
            outline=(c if (self.value.get() != self.option_b) else d).hex_code
        )


def test_multi_combobox():
    def col_label(c):
        result = ""
        while c >= 0:
            result = result + chr((c % 26) + ord('A'))
            c = c // 26 - 1
            if c < 0:
                break
        return result

    def random_table(rows, cols, low=-8, high=20):
        return [[col_label(i) for i in range(cols)]] + [[random.randint(low, high) for j in range(cols)] for i in
                                                        range(rows)]

    def delete_some():
        unlucky = random.sample(random_data["A"].values.tolist(), 180)
        print(f"{unlucky=}")
        # for unl in unlucky:
        #     mc.delete_item(value=unl)
        mc.delete_item(value=unlucky)

    app = tkinter.Tk()
    app.geometry(calc_geometry_tl(800, 800, rtype=str))
    app.title("Test MultiCombobox")

    random_data = random_table(600, 16)
    print(f"{random_data=}")
    random_data = pd.DataFrame(random_data[1:], columns=random_data[0])
    print(f"{random_data=}")

    mc = MultiComboBox(
        app,
        data=random_data
    )

    app.after(2500, lambda: delete_some())

    mc.grid()
    app.mainloop()



if __name__ == '__main__':
    print(f"\n\tVersion:\n{VERSION}\n")
    print(f"Details: {VERSION_DETAILS()}.")
    print(f"{VERSION_NUMBER()=}.")
    print(f"{VERSION_DATE()=}.")
    print(f"{VERSION_AUTHORS()=}.")

    # app = tkinter.Tk()
    # app.geometry(calc_geometry_tl(800, 800, parent=app, ask=True))
    # tb = ToggleCanvas(
    #     app,
    #     width=600,
    #     height=200
    #     # ,
    #     # colour_option_a="#874556",
    #     # colour_option_b="#455687",
    #     ,font_text_option_a="CourierNew 18"
    #     ,font_text_option_b="Arial 32",
    #     option_a=["PART 1", "PART 2"],
    #     p_bright=0.25
    # )
    # app.mainloop()

    test_multi_combobox()

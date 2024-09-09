import functools
import math
import random
import tkinter
from copy import deepcopy
from tkinter import font
from typing import List, Any, Literal, Optional
import calendar

import datetime
import customtkinter as ctk
from CTkTable import CTkTable
from tkcalendar import Calendar
from ttkwidgets.font import FontFamilyDropdown, FontSizeDropdown, FontPropertiesFrame

from datetime_utility import is_date
from colour_utility import Colour, iscolour, random_colour
from utility import grid_cells, clamp, isnumber
import pandas as pd
from screeninfo import get_monitors

#######################################################################################################################
#######################################################################################################################
#######################################################################################################################

VERSION = \
    """	
    General Utility Functions
    ans class for customtkinter
    Version................1.09
    Date.............2024-08-08
    Author(s)......Avery Briggs
    """


def VERSION_DETAILS():
    return VERSION.lower().split("version")[0].strip()


def VERSION_NUMBER():
    return float(".".join(VERSION.lower().split("version")[-1].split("date")[0].split(".")[-2:]).strip())


def VERSION_DATE():
    return datetime.datetime.strptime(VERSION.lower().split("date")[-1].split("author")[0].split(".")[-1].strip(),
                                      "%Y-%m-%dictionary")


def VERSION_AUTHORS():
    return [w.removeprefix(".").strip().title() for w in VERSION.lower().split("author(s)")[-1].split("..") if
            w.strip()]


#######################################################################################################################
#######################################################################################################################
#######################################################################################################################


def calc_geometry_tl(
        width: int | float,
        height: int | float = None,
        dims: Optional[tuple | list] = None,
        largest: bool | int = True,
        rtype: str | dict | list | tuple = str,
        parent: ctk.CTkBaseClass | ctk.CTkToplevel | ctk.CTk = None,
        do_print: bool = False,
        ask: bool = False,
        ask_title: str = "Select which monitor you would like to use:",
        bypass_parent_withdraw: bool = False,  # use for customtkinter and windows that are problematic to re-display
        # one_display_orient: Literal["horizontal", "vertical"]="horizontal",
        colour_code: Optional[dict[str: str]] = None
) -> str | dict | list | tuple:
    x_off, y_off = 0, 0

    if not isinstance(colour_code, dict):
        colour_code = {}

    bg_canvas = colour_code.get("bg_canvas", "#898989")
    bg_colour = colour_code.get("bg_colour", "#454545")
    fg_colour = colour_code.get("fg_colour", "#CCCCCC")
    bg_hover_colour = colour_code.get("bg_hover_colour", "#DE9E9E")
    fg_hover_colour = colour_code.get("fg_hover_colour", "#FFFFFF")

    monitors = get_largest_monitors()

    if dims is None:
        # monitors_lr = sorted(list(monitors), ss_key=lambda m: m.x)
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

                idx = ctk.IntVar(parent, value=0)

                def close_tl():
                    tl.destroy()

                def click(event, monitor_idx):
                    # print(f"click {event=}, {idx=}")
                    idx.set(monitor_idx)
                    close_tl()

                def motion(event):
                    x, y = event.x, event.y
                    found_one = False
                    for i, m in enumerate(monitors):
                        tr, tt = tags[i]
                        x0, y0, x1, y1 = tl_canvas.bbox(tr)
                        if not found_one and ((x0 <= x <= x1) and (y0 <= y <= y1)):
                            tl_canvas.itemconfigure(tr, fill=bg_hover_colour)
                            tl_canvas.itemconfigure(tt, fill=fg_hover_colour)
                            found_one = True
                        else:
                            tl_canvas.itemconfigure(tr, fill=bg_colour)
                            tl_canvas.itemconfigure(tt, fill=fg_colour)

                tl = ctk.CTkToplevel(parent)
                w_w, h_w = 600, 200
                tl.geometry = calc_geometry_tl(w_w, h_w, parent=parent, ask=False)
                tl_label_dat = label_factory(tl, tv_label=ask_title, kwargs_label={"font": ("Calibri", 18, "bold")})
                tl_canvas = ctk.CTkCanvas(tl, width=w_w, height=h_w, background=bg_canvas)

                # print(f"{monitors=}")
                wx0 = monitors[0].x
                wx1 = monitors[-1].x + monitors[-1].height
                wy0 = min([m.y for m in monitors])
                wy1 = max([m.y + m.height for m in monitors])
                wwr = w_w / (wx1 - wx0)
                whr = h_w / (wy1 - wy0)
                tags = []
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
                    tr = tl_canvas.create_rectangle(x0, y0, x1, y1, fill=bg_colour)
                    tt = tl_canvas.create_text(x0 + (w / 2), y0 + (h / 2), fill=fg_colour, text=f"Monitor {i + 1}")
                    tl_canvas.tag_bind(tr, "<Button-1>", lambda event, i_=i: click(event, i_))
                    tl_canvas.tag_bind(tt, "<Button-1>", lambda event, i_=i: click(event, i_))
                    tags.append((tr, tt))

                # gc = grid_cells(w_w, len(monitors), h_w, 1, r_type=list, x_pad=10, y_pad=5)[0]
                # print(f"{monitors=}")
                # for i, m in enumerate(monitors):
                #     tr = tl_canvas.create_rectangle(*gc[i], fill="#AEAEAE")
                #     x0, y0, x1, y1 = gc[i]
                #     w, h = x1 - x0, y1 - y0
                #     tt = tl_canvas.create_text(x0 + (w/2), y0 + (h/2), fill="#000000", text=f"Monitor {i+1}")
                #     tl_canvas.tag_bind(tr, "<Button-1>", lambda event, i_=i: click(event, i_))
                #     tl_canvas.tag_bind(tt, "<Button-1>", lambda event, i_=i: click(event, i_))

                tl_canvas.bind("<Motion>", motion)
                tl_label_dat[1].grid(padx=25, pady=25)
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
            raise ValueError(
                f"Cannot use param 'ask' when 'parent' is not supplied. The 'ask' param is used to create a brief TopLevel to ask which monitor you want to use. Therefore, 'parent' must be a valid instance of (tkinter.BaseWidget | tkinter.Toplevel | tkinter.Tk)")

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
        return {
            "x": x_,
            "y": y_,
            "w": width_,
            "h": height_,
            "width": width_,
            "height": height_,
            "x1": x_,
            "y1": y_,
            "x2": x_ + width_,
            "y2": y_ + height_,
            "str": res,
            str: res,
            "geometry": res,
            "res": res
        }
    else:
        return [x_, y_, width_, height_]


def get_largest_monitors():
    return sorted(get_monitors(), key=lambda m: (-m.width_mm, m.width_mm * m.height_mm))


class CtkTableSortable(CTkTable):

    def __init__(
            self,
            master: any,
            sortable: bool = True,
            **kwargs
    ):
        super().__init__(master, **kwargs)

        self.sortable = sortable

        if sortable:
            self.header = self.values[0]
            # self.og_values = [[v for v in row] for row in self.values[1:]]
            self.og_values = deepcopy(self.values[1:])
            self.data_rev = {k: None for k in self.header}
            self.selected_rows = list()
            self.selected_cols = list()
            self.history_sorts = dict()

            callback = kwargs.pop("command", None)
            if callback:
                self.command = callback_wrapper(self, callback, self.clicked)
            else:
                self.command = None
            # print(f"{self._internal_callback=}")

    def clicked(self, data):
        print(f"\nclicked {data=}")
        row = data.get("row")
        col = data.get("column")
        val = data.get("value")
        args = data.get("args")
        if row == 0:
            self.sort_table(row, col)
        else:
            self.clear_selected_rows()
            self.select_row(row)
            self.selected_rows.append(row)

    def clear_selected_rows(self):
        print(f"clear_selected_rows {self.selected_rows}")
        for row in self.selected_rows:
            self.deselect_row(row)
        self.selected_rows.clear()
        self.update_selected_cols()

    def update_selected_rows(self):
        print(f"update_selected_rows, {self.selected_rows}")
        for row in self.selected_rows:
            self.select_row(row)

    def update_selected_cols(self):
        print(f"update_selected_cols {self.selected_cols}")
        for col in self.selected_cols:
            self.select_column(col)

    def clear_selected_cols(self):
        print(f"clear_selected_cols {self.selected_cols}")
        for col in self.selected_cols:
            self.deselect_column(col)
        self.selected_cols.clear()
        self.update_selected_rows()

    def sort_table(self, row, col):
        print(f"sort_table")
        col_name = self.header[col]
        rev = self.data_rev[col_name]
        if rev is None:
            rev = False
            rev_s = " (ASC)"
        elif rev:
            rev = None
            rev_s = ""
        else:
            rev = True
            rev_s = " (DESC)"

        for i, cn in enumerate(self.header):
            self.data_rev[cn] = None
            self.insert(0, i, f"{cn}")

        self.clear_selected_cols()
        self.data_rev[col_name] = rev
        print(f"{row=}, {col=}, {col_name=}, {rev=}")
        if rev is None:
            # original values
            # s_values = [[v for v in r] for r in self.og_values]
            s_values = deepcopy(self.og_values)
        else:
            # s_values = [[v for v in r] for r in self.history_sorts.get((col, rev), [[]])]
            s_values = deepcopy(self.history_sorts.get((col, rev), [[]]))
            if (len(s_values) == 1) and (len(s_values[0]) == 0):
                s_values = sorted(
                    self.values[1:],
                    key=lambda r: r[col],
                    reverse=rev
                )
                # self.history_sorts[(col, rev)] = [[v for v in r] for r in s_values]
                self.history_sorts[(col, rev)] = deepcopy(s_values)

        s_values.insert(0, self.header)
        self.check_new_selected_rows(s_values)
        self.update_values(s_values)
        self.insert(0, col, f"{col_name}{rev_s}")
        self.select_column(col)
        self.selected_cols.append(col)
        self.update_selected_rows()

    def check_new_selected_rows(self, s_values):
        new_idxs = []
        for row in self.selected_rows:
            row_data = self.values[row]
            try:
                new_idx = s_values.index(row_data)
            except (IndexError, ValueError):
                pass
            else:
                new_idxs.append(new_idx)

        self.selected_rows = [r for r in new_idxs]


class CtkTableExt(ctk.CTkScrollableFrame):

    def __init__(
            self,
            master: any,
            table_data: List[List[any]] = None,
            width: int = 400,
            height: int = 250,
            sortable: bool = True,
            searchable: bool = True,
            allow_partial_match: bool = True,
            auto_grid: bool = True,
            kwargs_entry: dict = None,
            kwargs_table: dict = None,
            **kwargs
    ):
        super().__init__(master, width=width, height=height, **kwargs)

        self.table_data = table_data if isinstance(table_data, list) else [[]]
        self.width = width
        self.height = height
        self.sortable = sortable
        self.searchable = searchable
        self.allow_partial_match = allow_partial_match
        self.kwargs_entry = kwargs_entry if kwargs_entry is not None else dict()
        self.kwargs_table = kwargs_table if kwargs_table is not None else dict()
        self.search_idx = 0
        self.search_idxs = list()

        if self.sortable:
            print(f"sortable")
            if self.kwargs_table.get("command") is None:
                self.kwargs_table.update({"command": self.click_command})
            self.table = CtkTableSortable(self, values=self.table_data, **self.kwargs_table)
        else:
            print(f"NOT sortable")
            self.table = CTkTable(self, values=self.table_data, **self.kwargs_table)

        self.header = self.table.values[0]

        self.frame_search_widgets = ctk.CTkFrame(self)
        self.frame_search_nav_widgets = ctk.CTkFrame(self)

        if self.searchable:
            self.searching = tkinter.BooleanVar(self, value=False)

            self.var_text_entry = tkinter.StringVar(self, value="")
            self.entry = ctk.CTkEntry(
                self.frame_search_widgets,
                textvariable=self.var_text_entry,
                **self.kwargs_entry
            )

            self.var_text_btn_submit_search = tkinter.StringVar(self, value="search")
            self.btn_submit_search = ctk.CTkButton(
                self.frame_search_widgets,
                textvariable=self.var_text_btn_submit_search,
                command=self.submit_entry
            )

            self.var_text_btn_clear_search = tkinter.StringVar(self, value="x")
            self.btn_clear_search = ctk.CTkButton(
                self.frame_search_widgets,
                textvariable=self.var_text_btn_clear_search,
                command=self.clear_entry
            )

            self.var_text_btn_next_search = tkinter.StringVar(self, value=">>")
            self.btn_next_search = ctk.CTkButton(
                self.frame_search_nav_widgets,
                textvariable=self.var_text_btn_next_search,
                command=self.next_search
            )

            self.var_text_btn_prev_search = tkinter.StringVar(self, value="<<")
            self.btn_prev_search = ctk.CTkButton(
                self.frame_search_nav_widgets,
                textvariable=self.var_text_btn_prev_search,
                command=self.prev_search
            )

            self.var_text_btn_show_all_search = tkinter.StringVar(self, value="show all")
            self.btn_show_all_search = ctk.CTkButton(
                self.frame_search_nav_widgets,
                textvariable=self.var_text_btn_show_all_search,
                command=self.show_all_search
            )

            self.var_text_lbl_num = tkinter.StringVar(self, value="")
            self.var_text_lbl_sls = tkinter.StringVar(self, value="/")
            self.var_text_lbl_den = tkinter.StringVar(self, value="")

            self.lbl_search_num = ctk.CTkLabel(
                self.frame_search_nav_widgets,
                textvariable=self.var_text_lbl_num
            )
            self.lbl_search_sls = ctk.CTkLabel(
                self.frame_search_nav_widgets,
                textvariable=self.var_text_lbl_sls
            )
            self.lbl_search_den = ctk.CTkLabel(
                self.frame_search_nav_widgets,
                textvariable=self.var_text_lbl_den
            )

        if auto_grid:
            self.grid_widgets()

    def grid_widgets(self):
        rc, cc = 0, 0
        if self.searchable:
            self.frame_search_widgets.grid(row=0, column=0, rowspan=1, columnspan=1)
            self.entry.grid(row=0, column=0, rowspan=1, columnspan=1)
            self.btn_submit_search.grid(row=0, column=1, rowspan=1, columnspan=1)
            self.btn_clear_search.grid(row=0, column=2, rowspan=1, columnspan=1)

            self.show_search_fraction(False)
            rc += 2
            cc += 1

        self.table.grid(row=rc, column=0, rowspan=1, columnspan=cc + 1)

    def click_command(self, *args):
        # print(f"click_command, {args=}")
        # self.hide_search_widgets()
        pass

    def clear_entry(self):
        self.var_text_entry.set("")
        self.hide_search_widgets()

    def hide_search_widgets(self):
        self.searching.set(False)
        # self.table.clear_selected_cols()
        # self.table.clear_selected_update_selected_rowsrows()
        self.table.update_selected_rows()
        self.table.update_selected_cols()
        self.show_search_fraction(False)
        self.clear_search_idxs()

    def show_search_fraction(self, show: bool):
        if show:
            self.frame_search_nav_widgets.grid(row=1, column=0, rowspan=1, columnspan=1)
            self.lbl_search_num.grid(row=0, column=1, rowspan=1, columnspan=1)
            self.lbl_search_sls.grid(row=0, column=2, rowspan=1, columnspan=1)
            self.lbl_search_den.grid(row=0, column=3, rowspan=1, columnspan=1)

            self.btn_prev_search.grid(row=0, column=4, rowspan=1, columnspan=1)
            self.btn_next_search.grid(row=0, column=5, rowspan=1, columnspan=1)
            self.btn_show_all_search.grid(row=0, column=6, rowspan=1, columnspan=1)
        else:
            self.frame_search_nav_widgets.grid_forget()
            self.lbl_search_num.grid_forget()
            self.lbl_search_sls.grid_forget()
            self.lbl_search_den.grid_forget()

            self.btn_prev_search.grid_forget()
            self.btn_next_search.grid_forget()
            self.btn_show_all_search.grid_forget()

    def show_all_search(self):
        if self.searching.get():
            for i, j in self.search_idxs:
                self.table.select(i, j)

    def clear_search_idxs(self):
        for i, j in self.search_idxs:
            self.table.deselect(i, j)
        self.search_idxs.clear()

    def next_search(self):
        print(f"next_search")
        if self.searching.get():
            idx = self.search_idx
            idxs = self.search_idxs
            tot = len(idxs)
            print(f"{idx=}, {tot=}")
            if idx < tot:
                self.search_idx += 1
                self.var_text_lbl_num.set(str(idx + 1))
                self.table.deselect(*self.search_idxs[idx - 1])
                self.table.select(*self.search_idxs[idx])

    def prev_search(self):
        print(f"prev_search")
        if self.searching.get():
            idx = self.search_idx
            idxs = self.search_idxs
            tot = len(idxs)
            print(f"{idx=}, {tot=}")
            if idx > 1:
                self.search_idx -= 1
                self.var_text_lbl_num.set(str(idx - 1))
                self.table.deselect(*self.search_idxs[idx - 1])
                self.table.select(*self.search_idxs[idx - 2])

    def submit_entry(self):
        value = self.var_text_entry.get()
        print(f"submit_entry {value=}")

        if value:
            self.searching.set(True)
            self.show_search_fraction(True)
            self.search_table(value)

    def search_table(self, value):
        print(f"searching for {value=}")
        l_value = str(value).lower()
        self.table.clear_selected_cols()
        self.table.clear_selected_rows()
        # i, j = None, None
        f_idxs = []
        for i, row in enumerate(self.table.values[1:]):
            for j, val in enumerate(row):
                print(f"{i=}, {j=}, {val=}")
                if self.allow_partial_match:
                    if l_value in str(val).lower():
                        f_idxs.append((i + 1, j))
                    else:
                        self.table.deselect(i + 1, j)
                else:
                    if str(val).lower() == l_value:
                        f_idxs.append((i + 1, j))
                    else:
                        self.table.deselect(i + 1, j)

        self.var_text_lbl_num.set("1" if len(f_idxs) else "0")
        self.var_text_lbl_den.set(str(len(f_idxs)))

        self.search_idx = 1
        self.search_idxs = [tup for tup in f_idxs]

        # r, c = i, j
        for i, j in f_idxs[:1]:
            self.table.select(i, j)

        # if r is not None:
        #     for i in range(r - 1):
        #         for j in range(c):
        #             self.table.deselect(i + 1, j)

    def clear_all_selected(self):
        for i, row in enumerate(self.table.values[1:]):
            for j, val in enumerate(row):
                self.table.deselect(i + 1, j)


class CtkEntryDate_2(ctk.CTkEntry):
    # https://github.com/YakirNissim/customtkinter-CTkEntryDate
    def __init__(self,
                 master: Any,
                 placeholder_text: str = 'DD / MM / YY',
                 *args, **kwargs):
        super().__init__(master=master, placeholder_text=placeholder_text, *args, **kwargs)
        self.__super_get = super().get
        self.__super_delete = super().delete
        self.__super_insert = super().insert
        self.letter_input = False
        self.temp = ""
        self.bind("<KeyRelease>", self.__check_entry)

    def get(self):
        date_int_list = []
        for i in self.__super_get().split(' / '):
            if not i.isdigit() or len(i) != 2:
                return False
            date_int_list += [int(i)]
        if date_int_list[1] > 12 or (calendar.monthrange(2000 + date_int_list[2], date_int_list[1])[1]) < date_int_list[
            0]:
            return False
        return tuple(date_int_list)

    def delete(self, first_index, last_index=None):
        self.__super_delete(0, tkinter.END)
        self.__super_insert(0, self.temp)
        self.__super_delete(first_index, last_index)
        self.temp = self.__super_get()
        self.__insert_fix()

        if not self._is_focused and self._entry.get() == "":
            self._activate_placeholder()

    def insert(self, index, string=None, date=None):
        if date is not None and type(date) == tuple and len(date) == 3:
            string = ''
            for i in date:
                if type(i) == int and i < 100:
                    string += str(i)
                else:
                    raise TypeError('The format of a "date" is (DD, MM, YY) where DD, MM, YY is an integer!')
            if date[1] > 12 or (calendar.monthrange(2000 + date[2], date[1])[1]) < date[0]:
                raise ValueError('The "date" is invalid!')
            self.temp = string
            return self.__insert_fix()
        if string is not None:
            if type(string) != str:   raise TypeError('The type "string" likes to be "str".'
                                                      '\nThe format of a "string" is "DDMMYY"')
            if string.isdigit():
                self.__super_delete(0, tkinter.END)
                self.__super_insert(0, self.temp)
                self.__super_insert(index, string)
                self.temp = self.__super_get()
                return self.__insert_fix()
            raise ValueError('The "string" can only contain numbers!')

    def __insert_fix(self):
        if len(self.temp) > 6:  self.temp = self.temp[-6:]
        insert_str = ''
        for i in range(len(self.temp)):
            insert_str += self.temp[i]
            if i % 2 == 1 and i < 5:  insert_str += ' / '
        self.__super_delete(0, tkinter.END)
        self.__super_insert(0, insert_str)

    def __check_entry(self, evt):
        if evt.char.isdigit():
            self.temp += evt.char
        elif evt.keysym != 'BackSpace':
            self.delete(0, tkinter.END)
            self.letter_input = True
        else:
            self.temp = self.temp[:-1]
        if len(self.__super_get()) == 2:
            self.__super_insert(tkinter.END, ' / ')
        if len(self.__super_get()) == 7:
            self.__super_insert(tkinter.END, ' / ')

        if len(self.__super_get()) > 12 or evt.keysym == 'BackSpace' or self.letter_input:
            self.__insert_fix()
            self.letter_input = False


class CtkEntryDate(ctk.CTkFrame):
    # calendar docs: https://github.com/j4321/tkcalendar

    def __init__(
            self,
            master: Any,
            auto_grid: bool = True,
            date_format: str = "y-mm-dd",
            entry_kwargs: dict = None,
            button_kwargs: dict = None,
            calendar_kwargs: dict = None,
            **kwargs
    ):
        super().__init__(master, **kwargs)

        self.date_format = date_format
        self.entry_kwargs = entry_kwargs if entry_kwargs is not None else dict()
        self.button_kwargs = button_kwargs if button_kwargs is not None else dict()
        self.calendar_kwargs = calendar_kwargs if calendar_kwargs is not None else dict()

        # if 'date_pattern' is not in 'calendar_kwargs', then use the 'date_format' param.
        # WARNING: the year value is sometimes not parsed correctly when using date_format values:
        #   'yy' - this shows only a 2 digit year use 'y' for 4 instead.
        self.calendar_kwargs.setdefault("date_pattern", date_format)
        self.date: datetime.datetime = datetime.datetime.now()
        self.var_date_picker = tkinter.StringVar(self, value=f"{self.date:%Y-%m-%d}")
        self.var_date_entry = tkinter.StringVar(self, value=self.var_date_picker.get())

        # self.var_entry = tkinter.StringVar(self, value="")
        self.entry = ctk.CTkEntry(
            self,
            textvariable=self.var_date_entry,
            **self.entry_kwargs
        )
        self.var_text_btn_dropdown = tkinter.StringVar(self, value="V")
        self.btn_dropdown = ctk.CTkButton(
            self,
            textvariable=self.var_text_btn_dropdown,
            command=self.click_dropdown,
            **self.button_kwargs
        )
        self.date_picker = Calendar(
            self,
            textvariable=self.var_date_picker,
            **self.calendar_kwargs
        )

        if auto_grid:
            self.grid_widgets()

        self.var_date_picker.trace_variable("w", self.update_selected_date)
        self.entry.bind("<Return>", self.submit_entry)

    def grid_widgets(self):
        self.entry.grid(row=0, column=0, rowspan=1, columnspan=1)
        self.btn_dropdown.grid(row=0, column=1, rowspan=1, columnspan=1)

    def click_dropdown(self):
        is_down = self.var_text_btn_dropdown.get() == "^"

        if is_down:
            self.date_picker.grid_forget()
            self.var_text_btn_dropdown.set("V")
        else:
            self.date_picker.grid(row=1, column=0, rowspan=1, columnspan=2)
            self.var_text_btn_dropdown.set("^")

    def submit_entry(self, event):
        # print(f"submit_entry v={self.var_date_picker.get()}")
        # val = self.var_date_picker.get()
        print(f"submit_entry v={self.var_date_entry.get()}")
        val = self.var_date_entry.get()
        if is_date(val):
            # date = self.date_picker.parse_date(val)
            # self.date_picker.date = date
            val = is_date(val)
            print(f"A: {val}")
            val = self.date_picker.format_date(val)
            print(f"B: {val}")
            self.date_picker.selection_set(val)

    def update_selected_date(self, *args):
        self.var_date_entry.set(self.var_date_picker.get())
        # text = self.var_date_picker.get()
        # print(f"{text=}")
        # if is_date(text):
        #     print(f"ISDATE")
        #     for fmt in (
        #         "%x",
        #         "%Y-%m-%d"
        #     ):
        #         try:
        #             self.date = datetime.datetime.strptime(text, fmt)
        #             print(f"{self.date=}")
        #             self.date_picker.selection_set(self.date)
        #         except ValueError:
        #             pass
        #         else:
        #             break
        # print(f"END")

        # date = self.date_picker.selection_get()
        # print(f"update_selected_date v={date}")
        # fmt = "%x"
        # if isinstance(date, str):
        #     for fmt in (
        #         "%x",
        #         "%Y-%m-%d"
        #     ):
        #         try:
        #             self.date = datetime.datetime.strptime(date, fmt)
        #         except ValueError:
        #             pass
        #         else:
        #             break
        # else:
        #     # self.date = self.date_picker.format_date(date)
        #     self.date = date
        #
        # print(f"New Date! {self.date:%Y-%m-%d}")
        # self.var_date_picker.set(f"{self.date:%Y-%m-%d}")


def callback_wrapper(obj, callback, secondary_callback):
    @functools.wraps(callback)
    def wrapper(*args, **kwargs):
        print("Callback function has been invoked")
        secondary_callback(*args, **kwargs)
        return callback(*args, **kwargs)

    return wrapper


def callback_a(data):
    row = data.get("row")
    col = data.get("column")
    val = data.get("value")
    args = data.get("args")
    print(f"{row=}, {col=}, {val=}, {args=}")


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


class CalendarCanvas2(ctk.CTkCanvas):
    def __init__(
            self,
            master,
            year: int | None = datetime.datetime.now().year,
            show_weekdays: bool = True,
            months_per_row: int = 4,
            width: int = 600,
            height: int = 700,
            colour_background_canvas: Colour = Colour("#AEBEBE"),
            colour_foreground_canvas: Colour = Colour("#000000"),
            colour_background_owned_number_check: Colour = Colour("#2A4AFA"),
            colour_background_header_year: Colour = Colour("#627272"),
            colour_background_header_month: Colour = Colour("#7B8B8B"),
            colour_foreground_header_month: Colour = Colour("#200000"),
            colour_background_header_weekday: Colour = Colour("#94A4A4"),
            colour_foreground_header_weekday: Colour = Colour("#000000"),
            colour_background_canvas_selected: Colour = Colour("#081688"),
            colour_active_background_canvas_selected: Colour = Colour("#2836A8"),
            colour_active_foreground_canvas_selected: Colour = Colour("#DDDDDD"),
            colour_foreground_canvas_selected: Colour = Colour("#FFFFFF"),
            colour_outline: Colour = Colour("#000000"),
            colour_scheme_month: dict[int: Colour] = None,
            colour_scheme_day: dict[tuple[int, int]: Colour] = None,
            hover_style: Literal[None, "darken", "brighten"] = "brighten",
            invalid_style: Literal[None, "darken", "brighten", "invisible"] = None,
            disabled_style: Literal["darken", "brighten"] = "darken",
            invalid_style_safe: bool = True,
            show_all_rows: bool = False,
            selectable: bool = False,
            *args, **kwargs
    ):
        super().__init__(master=master, *args, **kwargs)

        # colour_scheme_month overrides the default colours

        self.year: None | int = year
        self.show_weekdays = show_weekdays and bool(self.year)
        self.show_all_rows = show_all_rows
        self.selectable = selectable
        self.selected_date = ctk.Variable(self, value=None)
        self.months_per_row = clamp(3, months_per_row, 4)
        self.weeks_per_month = 6 + 1  # for the month label
        self.weeks_per_month += (1 if self.show_weekdays else 0)  # offset for weekday labels
        self.weeks_per_month -= (1 if self.year is None else 0)  # offset for weekday labels
        # self.n_rows: int = ((self.weeks_per_month + int(self.show_weekdays)) * (12 // self.months_per_row)) + 1
        self.n_rows: int = (self.weeks_per_month * (12 // self.months_per_row)) + int(self.show_weekdays)
        self.n_cols: int = 7 * self.months_per_row
        self.w_canvas: int = width
        self.h_canvas: int = height
        self.colour_background_canvas = colour_background_canvas
        self.colour_foreground_canvas = colour_foreground_canvas
        self.colour_background_owned_number_check = colour_background_owned_number_check
        self.colour_background_header_year = colour_background_header_year
        self.colour_background_header_month = colour_background_header_month
        self.colour_foreground_header_month = colour_foreground_header_month
        self.colour_background_header_weekday = colour_background_header_weekday
        self.colour_foreground_header_weekday = colour_foreground_header_weekday
        self.colour_background_canvas_selected = colour_background_canvas_selected
        self.colour_foreground_canvas_selected = colour_foreground_canvas_selected
        self.colour_active_background_canvas_selected = colour_active_background_canvas_selected
        self.colour_active_foreground_canvas_selected = colour_active_foreground_canvas_selected
        self.colour_outline = colour_outline
        self.colour_scheme_month: dict[int: Colour] = self.validate_colour_scheme(
            colour_scheme_month) if colour_scheme_month is not None else dict()
        # self.colour_scheme_day: dict[tuple[int, int]: Colour] = self.validate_colour_scheme(colour_scheme_day) if colour_scheme_day is not None else dict()
        self.colour_scheme_day: dict[tuple[
                                         int, int]: Colour] = colour_scheme_day if colour_scheme_day is not None else dict()
        self.hover_style = hover_style
        self.invalid_style = invalid_style
        self.disabled_style = disabled_style
        self.invalid_style_safe = invalid_style_safe
        self.v_cell_ids_hovered = ctk.Variable(self, value=None)
        self.v_cell_ids_selected = ctk.Variable(self, value=None)
        self.max_days_per_month = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

        # Tracking structures
        self.finished_init = False
        self.finished_calc = False
        self.dict_canvas_tags = dict()
        self.set_date_cells = set()
        self.dict_cell_to_cal_idx = dict()
        self.date_to_cell = dict()
        self.cell_to_date = dict()
        self.disabled_cells = set()

        self.configure(
            width=self.w_canvas,
            height=self.h_canvas,
            # background=self.colour_background_canvas.hex_code
            background=self.get_colour("colour_background_canvas").hex_code
        )
        self.gc = grid_cells(
            t_width=self.w_canvas,
            n_cols=self.n_cols,
            t_height=self.h_canvas,
            n_rows=self.n_rows,
            # x_pad=4,
            # y_pad=4,
            r_type=list
        )

        ri = 1 if self.year is not None else 0

        self.dict_canvas_tags[f"header_month_weekday"] = dict()
        for i, row in enumerate(self.gc):
            for j, coords in enumerate(row):
                n = ((i * self.n_cols) + j) + 1
                # if n == 100:
                #     # no #100
                #     break
                x0, y0, x1, y1 = coords
                # cal_idx = (j // 7) + (i // 7)  # + (i * ((7 * self.months_per_row) // self.weeks_per_month))
                # cal_idx = (j // 7) + (i // (self.weeks_per_month + 1))  # + (i * ((7 * self.months_per_row) // self.weeks_per_month))
                # cal_idx = (j // 7) + (max(0, i - (1 + sum([bool(self.year), self.show_weekdays]))) // (
                #             self.weeks_per_month + 1))  # + (i * ((7 * self.months_per_row) // self.weeks_per_month))

                # j//7
                # j = c_i // self.months_per_row
                # ri0 = ri + (j * self.weeks_per_month)
                # ci0 = (c_i % self.months_per_row) * 7
                # cal_idx =
                p_a = j // 7
                # p_ba = (i - ri) // (self.weeks_per_month + self.show_weekdays)
                p_ba = (i - ri) // (self.weeks_per_month)
                p_bb = p_ba * self.months_per_row
                cal_idx = p_a + p_bb
                self.dict_cell_to_cal_idx[(i, j)] = cal_idx
                self.set_date_cells.add((i, j))

                # cs = self.colour_scheme_month.get(cal_idx, {})
                # col_wd = cs.get("colour_background_canvas", self.colour_background_canvas)
                # col_wd_txt = cs.get("colour_foreground_canvas", col_wd.font_foreground_c())
                # col_wd = self.get_colour("colour_background_canvas", i, j, do_show=((0 < i < 20) and (15 < j < 50)))
                # col_wd_txt = self.get_colour("colour_foreground_canvas", i, j, do_show=((0 < i < 20) and (15 < j < 50)))
                col_wd = self.get_colour("colour_background_canvas", i, j)
                col_wd_txt = self.get_colour("colour_foreground_canvas", i, j)
                col_ou = self.get_colour("colour_outline", i, j)
                # print(f"{i=}, {j=}, {cal_idx=}, {p_a=}, {p_ba=}, {p_bb=}, col_wd={col_wd.hex_code}, col_wd_txt={col_wd_txt.hex_code}, {cs=}")
                tr = self.create_rectangle(
                    x0, y0, x1, y1,
                    fill=col_wd.hex_code,
                    outline=col_ou.hex_code
                )
                tt = self.create_text(
                    x0 + ((x1 - x0) / 2), y0 + ((y1 - y0) / 2),
                    fill=col_wd_txt.hex_code,
                    text=f"{n}"
                )
                if self.selectable:
                    for tag in (tr, tt):
                        self.tag_bind(
                            tag,
                            "<Button-1>",
                            lambda event, i_=i, j_=j: self.click_canvas(event, i_, j_)
                        )

                self.dict_canvas_tags[(i, j)] = {
                    "rect": tr,
                    "text": tt
                }
                if (hs := self.hover_style) is not None:
                    for tag in (tr, tt):
                        self.tag_bind(tr, "<Motion>",
                                      lambda event, i_=i, j_=j, t_=tag: self.motion_cell(event, i_, j_, t_))

        self.dict_canvas_tags["header_year"] = {"rect": None, "text": None}
        self.dict_canvas_tags["header_month"] = {"rect": None, "text": None}
        self.dict_canvas_tags["header_weekday"] = {"rect": None, "text": None}

        if self.year is not None:
            # hide top row cells
            for j in range(self.n_cols):
                #     for tag_name in ("rect", "text"):
                #         self.itemconfigure(
                #             self.dict_canvas_tags[(0, j)][tag_name],
                #             state="hidden"
                #         )
                self.set_date_cells.discard((0, j))

            # create a new rectangle for the year label row
            bbox_year = (
                *self.gc[0][0][:2],
                *self.gc[0][-1][-2:]
            )
            w = bbox_year[2] - bbox_year[0]
            h = bbox_year[3] - bbox_year[1]
            self.dict_canvas_tags["header_year"].update({
                "rect": self.create_rectangle(
                    *bbox_year,
                    # fill=self.colour_background_header_year.hex_code
                    fill=self.get_colour("colour_background_header_year").hex_code
                ),
                "text": self.create_text(
                    bbox_year[0] + (w / 2),
                    bbox_year[1] + (h / 2),
                    text=f"{self.year}",
                    fill=self.colour_background_header_year.font_foreground(rgb=False)
                )
            })

        # blank month row
        # for j in range(self.n_cols):
        #     self.set_date_cells.discard((ri, j))
        #     for tag_name in ("rect", "text"):
        #         self.itemconfigure(
        #             self.dict_canvas_tags[(ri, j)][tag_name],
        #             state="hidden"
        #         )
        self.dict_canvas_tags["header_month"] = list()
        print(f"gc={self.gc}")
        for c_i in range(12):
            j = c_i // self.months_per_row
            ri0 = ri + (j * self.weeks_per_month)
            ci0 = (c_i % self.months_per_row) * 7
            print(f"{c_i=}, {j=}, {ri0=}, {ci0=}")
            month_name = calendar.month_name[c_i + 1]
            bbox_month = (
                *self.gc[ri0][ci0][:2],
                *self.gc[ri0][ci0 + 7 - 1][-2:]
            )
            w = bbox_month[2] - bbox_month[0]
            h = bbox_month[3] - bbox_month[1]
            # cs = self.colour_scheme_month.get(c_i, {})
            # col_hm = cs.get("colour_background_header_month", self.colour_background_header_month)
            # col_txt = cs.get("colour_foreground_header_month", col_hm.font_foreground_c())
            col_hm = self.get_colour("colour_background_header_month", ri0, ci0)
            # col_txt = self.get_colour("colour_foreground_header_month", default=col_hm.font_foreground_c())
            col_txt = self.get_colour("colour_foreground_header_month", ri0, ci0)
            self.dict_canvas_tags[f"header_month"].append({
                "rect": self.create_rectangle(
                    *bbox_month,
                    fill=col_hm.hex_code
                ),
                "text": self.create_text(
                    bbox_month[0] + (w / 2),
                    bbox_month[1] + (h / 2),
                    text=f"{month_name}",
                    fill=col_txt.hex_code
                ),
                "weekdays": list()
            })
            print(f"{month_name[:3].upper()}: {bbox_month=}")

            # col_hw = cs.get("colour_background_header_weekday", self.colour_background_header_weekday)
            col_hw = self.get_colour("colour_background_header_weekday")
            if self.show_weekdays:
                ri0 += 1
                self.dict_canvas_tags[f"header_month_weekday"][c_i] = list()
                for k in range(self.n_cols):
                    self.itemconfigure(
                        self.dict_canvas_tags[(ri0, k)]["rect"],
                        fill=col_hw.hex_code
                    )
                    self.dict_canvas_tags[f"header_month_weekday"][c_i].append((ri0, k))
                    self.set_date_cells.discard((ri0, k))
        # print(f"{self.dict_canvas_tags['header_month']=}")

        self.time_after_motion = 3600
        self.id_after_motion = None

        self.finished_init = True
        self.calc_days()
        self.selected_date.trace_variable("w", self.update_selected_date)

        print(f"END INIT")

    # def deselect_day(self, day_in: int | datetime.datetime = None, month_in: Optional[int] = None)
    def deselect_day(self):
        last_select: tuple[int, int] = self.v_cell_ids_selected.get()
        print(f"{last_select=}")
        if last_select:
            cal_idx_lh = self.dict_cell_to_cal_idx[last_select]
            cs_lh = self.colour_scheme_month.get(cal_idx_lh, {})
            # col_lh = cs_lh.get("colour_background_canvas", self.colour_background_canvas)
            # col_txt_lh = cs_lh.get("colour_foreground_canvas", col_lh.font_foreground_c())
            col_lh = self.get_colour("colour_background_canvas")
            col_txt_lh = self.get_colour("colour_foreground_canvas")
            self.itemconfigure(
                self.dict_canvas_tags[last_select]["rect"],
                fill=col_lh.hex_code
            )
            self.itemconfigure(
                self.dict_canvas_tags[last_select]["text"],
                fill=col_txt_lh.hex_code
            )
            self.v_cell_ids_selected.set(tuple())

    def disable_day(self, month_in: int | datetime.datetime, day_in: Optional[int] = None):
        print(f"disable {day_in=}, {month_in=}")
        if isinstance(month_in, datetime.datetime):
            print(f"DT")
            m_idx = month_in.month - 1
            d_idx = month_in.day
            if not (0 <= m_idx < 12):
                raise ValueError(f"Param 'month_in' must be between 1 and 12, representing the months of the year.")
            if not (1 <= d_idx <= self.max_days_per_month[m_idx]):
                raise ValueError(
                    f"Param 'day_in' must be between 1 and {self.max_days_per_month[m_idx]}, since you supplied 'month_idx'={m_idx + 1}, the maximum number of days can only be {self.max_days_per_month[m_idx]} for {calendar.month_name[m_idx + 1]}.")

        else:
            m_idx, d_idx = month_in - 1, day_in
        if self.year is None:
            i, j = self.date_to_cell[(m_idx, d_idx)]
        else:
            date_in = datetime.datetime(self.year, month_in, day_in)
            i, j = self.date_to_cell[date_in]

        print(f"DD -> {i=}, {j=}, {self.disabled_cells=}")

        # self.click_canvas(None, i, j)
        if (i, j) not in self.disabled_cells:
            self.disabled_cells.add((i, j))
            tr = self.dict_canvas_tags[(i, j)]["rect"]
            tt = self.dict_canvas_tags[(i, j)]["text"]
            # cs = self.colour_scheme_month.get(m_idx, {})
            # ds = self.colour_scheme_day.get((m_idx, d_idx), {})
            # bg, fg = None, None
            # if ds:
            #     bg = ds.get("colour_background_canvas")
            #     fg = ds.get("colour_foreground_canvas")
            # if not bg:
            #     bg = cs.get("colour_background_canvas")
            # if not fg:
            #     fg = cs.get("colour_foreground_canvas")
            # if not bg:
            #     bg = self.colour_background_canvas.darkened(0.3)
            # if not fg:
            #     fg = self.colour_foreground_canvas.darkened(0.3)
            bg = self.get_colour("colour_background_canvas", i, j)
            fg = self.get_colour("colour_foreground_canvas", i, j)

            # is_ = self.invalid_style[]
            self.itemconfigure(tt, fill=fg.hex_code)
            self.itemconfigure(tr, fill=bg.hex_code)

    def disable_date(self, date_in: datetime.datetime):
        if self.year is None:
            raise ValueError(
                f"Please use CalendarCanvas.disable_day when disabling a cell on a calendar with no specified year.")

        d1 = datetime.datetime(self.year, 1, 1)
        d2 = datetime.datetime(self.year, 12, 31, 23, 59, 59, 999999)
        if not (d1 <= date_in <= d2):
            raise ValueError(
                f"Param 'date_in' must be between {d1:%Y-%m-%d} and {d2:%Y-%m-%d} at end of day. Got {date_in:%x}")

        i, j = self.date_to_cell[date_in]

        if (i, j) not in self.disabled_cells:
            cal_idx = date_in.month - 1
            self.disabled_cells.add((i, j))

            tr = self.dict_canvas_tags[(i, j)]["rect"]
            tt = self.dict_canvas_tags[(i, j)]["text"]
            # cs = self.colour_scheme_month.get(cal_idx, {})
            # ds = self.colour_scheme_day.get((date_in.month, date_in.day), {})
            # bg, fg = None, None
            # if ds:
            #     bg = ds.get("colour_background_canvas")
            #     fg = ds.get("colour_foreground_canvas")
            # if not bg:
            #     bg = cs.get("colour_background_canvas")
            # if not fg:
            #     fg = cs.get("colour_foreground_canvas")
            # if not bg:
            #     bg = self.colour_background_canvas.darkened(0.3)
            # if not fg:
            #     fg = self.colour_foreground_canvas.darkened(0.3)

            bg = self.get_colour("colour_background_canvas", i, j)
            fg = self.get_colour("colour_foreground_canvas", i, j)

            # is_ = self.invalid_style[]
            self.itemconfigure(tt, fill=fg.hex_code)
            self.itemconfigure(tr, fill=bg.hex_code)

    def select_day(self, day_in: int | datetime.datetime, month_in: Optional[int] = None):
        if isinstance(day_in, datetime.datetime):
            m_idx = day_in.month - 1
            d_idx = day_in.day
            if not (0 <= m_idx < 12):
                raise ValueError(f"Param 'month_in' must be between 1 and 12, representing the months of the year.")
            if not (1 <= d_idx <= self.max_days_per_month[m_idx]):
                raise ValueError(
                    f"Param 'day_in' must be between 1 and {self.max_days_per_month[m_idx]}, since you supplied 'month_idx'={m_idx + 1}, the maximum number of days can only be {self.max_days_per_month[m_idx]} for {calendar.month_name[m_idx + 1]}.")

        else:
            m_idx, d_idx = month_in, day_in
        i, j = self.date_to_cell[(m_idx, d_idx)]
        self.click_canvas(None, i, j)

    def select_date(self, date_in: datetime.datetime):
        if self.year is None:
            raise ValueError(
                f"Please use CalendarCanvas.select_day when selecting a cell on a calendar with no specified year.")

        d1 = datetime.datetime(self.year, 1, 1)
        d2 = datetime.datetime(self.year, 12, 31, 23, 59, 59, 999999)
        if not (d1 <= date_in <= d2):
            raise ValueError(
                f"Param 'date_in' must be between {d1:%Y-%m-%d} and {d2:%Y-%m-%d} at end of day. Got {date_in:%x}")

        i, j = self.date_to_cell[date_in]

        self.click_canvas(None, i, j)

    def validate_colour_scheme(self, colour_scheme_month) -> dict[int: Colour]:
        if not isinstance(colour_scheme_month, dict):
            raise ValueError(
                f"Param 'colour_scheme_month' must be an instance of a dictionary. Got '{type(colour_scheme_month)}'")

        valid_style_keys = {
            "colour_background_canvas": iscolour,
            "colour_background_owned_number_check": iscolour,
            "colour_background_header_month": iscolour,
            "colour_background_header_weekday": iscolour,

            "colour_foreground_canvas": iscolour,
            "colour_foreground_header_month": iscolour,

            "colour_background_canvas_selected": iscolour,
            "colour_foreground_canvas_selected": iscolour,

            "colour_outline": iscolour
        }

        result = {}

        for k, scheme_data in colour_scheme_month.items():
            if not isinstance(k, int):
                raise ValueError(f"Param 'colour_scheme_month' must only have integer ss_key. Got '{k}'")
            if not (0 <= k < 12):
                raise ValueError(f"Param 'colour_scheme_month' must only have integer keys between 0 and 11. Got '{k}'")
            if not isinstance(scheme_data, dict):
                raise ValueError(f"Param 'scheme_data' must be an instance of a dict. Got '{scheme_data}'")
            result[k] = dict()
            for k_style, v in scheme_data.items():
                if k_style not in valid_style_keys:
                    raise ValueError(
                        f"Style ss_key '{k_style}' is not recognized. Must be an one of: {', '.join(valid_style_keys)}")
                try:
                    col = Colour(v)
                except Colour.ColourCreationError:
                    raise ValueError(
                        f"Param 'colour_scheme_month' must only have Colour objects or equivalent as values. Got '{k}'")
                result[k][k_style] = col

        return result

    def calc_days(self):
        ri = 2 if self.year is not None else 1
        is_ = self.invalid_style
        if self.year is not None:
            # for i, data in enumerate(self.dict_canvas_tags["header_month"]):

            for cal_i in range(12):
                day_one = datetime.datetime(self.year, cal_i + 1, 1)
                wd_d1 = day_one.isoweekday() % 7
                j = cal_i // self.months_per_row
                # cs = self.colour_scheme_month.get(cal_i, {})
                for wk_i in range(self.weeks_per_month - 1):
                    used_row = False
                    ri0 = ri + (j * self.weeks_per_month) + wk_i  # + self.show_weekdays
                    for wkd_i in range(7):
                        # ds = self.colour_scheme_day.get((day_one.month, day_one.day))
                        str_day = f"{day_one.day}"
                        ci0 = ((cal_i % self.months_per_row) * 7) + wkd_i
                        # print(f"{day_one:%Y-%m-%d}, {cal_i=}, {j=}, {ri0=}, {ci0=}, {wk_i=}, {wkd_i=}, {wd_d1=}", end="")
                        # month_name = calendar.month_name[cal_i + 1]
                        tag_txt = self.dict_canvas_tags[(ri0, ci0)]["text"]
                        tag_rect = self.dict_canvas_tags[(ri0, ci0)]["rect"]

                        # s = ds if ds else cs  # TODO this won't work right

                        if self.show_weekdays and (wk_i == 0):
                            # weekday
                            self.set_date_cells.discard((ri0, ci0))
                            self.dict_canvas_tags["header_month"][cal_i]["weekdays"].append({
                                "rect": tag_rect,
                                "text": tag_txt
                            })
                            self.itemconfigure(
                                tag_rect,
                                # fill=s.get("colour_background_header_weekday", self.colour_background_header_weekday).hex_code
                                fill=self.get_colour("colour_background_header_weekday", ri0, ci0,
                                                     do_show=((0 < ri0 < 20) and (15 < ci0 < 50))).hex_code
                            )
                            self.itemconfigure(
                                tag_txt,
                                text=f"{calendar.day_abbr[(wkd_i - 1) % 7]}"[0],
                                # fill=s.get("colour_foreground_header_weekday", self.colour_background_header_weekday.font_foreground_c()).hex_code
                                fill=self.get_colour("colour_foreground_header_weekday", ri0, ci0,
                                                     do_show=((0 < ri0 < 20) and (15 < ci0 < 50))).hex_code
                            )
                            used_row = True
                            continue
                        if cal_i != (day_one.month - 1):
                            self.itemconfigure(tag_txt, state="hidden")
                            if is_ == "invisible":
                                self.itemconfigure(tag_rect, state="hidden")
                            # print(f" -A")
                            self.set_date_cells.discard((ri0, ci0))
                            continue
                        if ((wk_i - (1 if self.show_weekdays else 0)) == 0) and (wd_d1 > 0):
                            wd_d1 -= 1
                            self.itemconfigure(tag_txt, state="hidden")
                            if is_ == "invisible":
                                self.itemconfigure(tag_rect, state="hidden")
                            self.set_date_cells.discard((ri0, ci0))
                            # print(f" -B")
                            continue

                        self.itemconfigure(tag_txt, text=str_day)
                        self.date_to_cell[day_one] = (ri0, ci0)
                        self.cell_to_date[(ri0, ci0)] = day_one
                        self.dict_cell_to_cal_idx[(ri0, ci0)] = day_one.month - 1
                        txt = self.itemcget(tag_txt, "text")
                        day_one += datetime.timedelta(days=1)
                        used_row = True

                        # # bbox_month = (
                        # #     *self.gc[ri0][ci0][:2],
                        # #     *self.gc[ri0][ci0 + 7 - 1][-2:]
                        # # )
                        # # tag_txt = self.dict_canvas_tags["header_month"][cal_i]["text"]
                        # # txt = self.itemcget(tag_txt, "text")
                        # print(f" {txt=}")

                    if (not self.show_all_rows) and (not used_row):
                        for k in range(7):
                            tup = (ri0, ((cal_i % self.months_per_row) * 7) + k)
                            self.set_date_cells.discard(tup)
                            self.itemconfigure(
                                self.dict_canvas_tags[tup]["rect"],
                                state="hidden"
                            )
        else:
            sr = [0 for i in range(self.n_cols)]
            for i in range(1, self.n_rows):
                used_row = False
                for j in range(self.n_cols):
                    tag_txt = self.dict_canvas_tags[(i, j)]["text"]
                    tag_rect = self.dict_canvas_tags[(i, j)]["rect"]
                    wk_i = (i - 1) % (self.weeks_per_month + self.show_weekdays - 1)
                    cal_idx = self.dict_cell_to_cal_idx[((i - 1), j)]
                    cs = self.colour_scheme_month.get(cal_idx, {})
                    print(f"{i=}, {j=}, {wk_i=}, {cal_idx=}, sr={sum(sr)},", end="")
                    # if self.show_weekdays and (wk_i == 0):
                    #     self.itemconfigure(
                    #         tag_txt,
                    #         # text=f"{calendar.day_abbr[j // self.months_per_row]}"[0],
                    #         text=f"{calendar.day_abbr[(j - 1) % 7]}"[0],
                    #         fill=cs.get("colour_foreground_header_weekday",
                    #                     self.colour_background_header_weekday.font_foreground_c()).hex_code
                    #     )
                    #     used_row = True
                    #     print(f" -A")
                    #     sr[i] = 1
                    #     continue
                    # # elif wk_i == ()
                    # # if wk_idx == 0:
                    # #     break
                    # str_day = ((j % 7) + 1) + (((i - (sum(sr) + 1)) * self.n_cols) // self.months_per_row)
                    str_day = ((j % 7) + 1) + (((i - 1) * self.n_cols) // self.months_per_row)
                    str_day %= (self.weeks_per_month * 7)
                    if str_day > self.max_days_per_month[cal_idx]:
                        self.itemconfigure(tag_txt, state="hidden")
                        if is_ == "invisible":
                            self.itemconfigure(tag_rect, state="hidden")
                        self.set_date_cells.discard((i, j))
                        print(f" End of Month")
                        continue
                    print(f" {str_day=}")
                    self.date_to_cell[(cal_idx, str_day)] = (i, j)
                    self.cell_to_date[(i, j)] = (cal_idx, str_day)
                    self.itemconfigure(tag_txt, text=str_day)
                    used_row = True
                    # day_one = datetime.datetime(self.year, cal_i + 1, 1)

                if (not self.show_all_rows) and (not used_row):
                    for k in range(7):
                        self.itemconfigure(
                            # self.dict_canvas_tags[(ri0, ((cal_i % self.months_per_row) * 7) + k)]["rect"],
                            self.dict_canvas_tags[(i, j)]["rect"],
                            state="hidden"
                        )
                        self.set_date_cells.discard((i, j))
        print(f"{self.cell_to_date=}")
        print(f"{self.date_to_cell=}")
        print(f"{self.dict_cell_to_cal_idx=}")
        print(f"END CALC_DAYS")
        self.finished_calc = True

    def get_colour(self, key, i=None, j=None, default=None, do_show=False):

        key_n = key.replace("_active", "").replace("active_", "")
        key_b = key if ("_background" in key) else key.replace("_foreground", "_background")

        selected = self.v_cell_ids_selected.get()
        hovered = self.v_cell_ids_hovered.get()

        ds = self.colour_scheme_day
        ms = self.colour_scheme_month

        ds_ = self.disabled_style
        is_ = self.invalid_style
        hs = self.hover_style

        bg = self.colour_background_canvas
        fg = self.colour_foreground_canvas

        dc = self.disabled_cells
        dtc = self.set_date_cells

        # print(f"{ds=}")

        def sub_get_colour(key_, i_=None, j_=None, default_=None, do_show_=False, depth=1):
            print(f"{key_=}, {i_=}, {j_=}, {default_=}, {do_show_=}, {depth=}")

            c_code = f""

            if (i_ is not None) and (j_ is not None):
                c_code += "a"
                val = None
                pos = i_, j_
                cal_idx = self.dict_cell_to_cal_idx[pos]
                is_invalid_cell = pos not in self.set_date_cells

                midx, didx = None, None
                if (not is_invalid_cell) and self.finished_init and self.finished_calc:
                    c_code += "b"
                    date_in = self.cell_to_date[pos]
                    midx, didx = date_in.month - 1, date_in.day

                if (midx, didx) in ds:
                    c_code += "c"
                    val = ds[(midx, didx)].get(key_)
                if not val:
                    c_code += "d"
                    if cal_idx in ms:
                        c_code += "e"
                        val = ms[cal_idx].get(key_)
                if not val:
                    c_code += "f"
                    if key_ != key_n:
                        if (midx, didx) in ds:
                            c_code += "g"
                            val = ds[(midx, didx)].get(key_n)
                        if not val:
                            c_code += "h"
                            if cal_idx in ms:
                                c_code += "i"
                                val = ms[cal_idx].get(key_n)
                    if not val:
                        try:
                            c_code += "j"
                            if "_foreground" in key:
                                val = self.get_colour(
                                    key.replace("_foreground", "_background"),
                                    i=i,
                                    j=j,
                                    do_show=do_show
                                ).font_foreground_c(threshold=255 / 4)
                            else:
                                val = self.__getattribute__(key_)
                        except AttributeError:
                            c_code += "k"
                            val = fg if ("_foreground" in key) else bg

                if is_invalid_cell:
                    c_code += "l"
                    if pos not in self.dict_canvas_tags[f"header_month_weekday"][cal_idx]:
                        c_code += "m"
                        print(f"invalid  {hovered=}")
                        if pos == hovered:
                            c_code += "n"
                            if is_:
                                c_code += "o"
                                val = val.darkened(0.25, safe=self.invalid_style_safe) if (is_ == "darken") else (
                                    val.brightened(0.25, safe=self.invalid_style_safe) if (is_ == "brighten") else val)

                elif pos in dc:
                    c_code += "p"
                    print(f"disabled")
                    if "_foreground" in key:
                        val = val.brightened(0.35, safe=True) if (ds_ == "darken") else (
                            val.darkened(0.35, safe=True) if (ds_ == "brighten") else val)
                    else:
                        val = val.brightened(0.25, safe=True) if (ds_ == "brighten") else val.darkened(0.25, safe=True)

                elif pos == selected:
                    c_code += "q"
                    print(f"selected")
                    key_s = key_.replace("_active", "").removesuffix("_selected") + "_selected"
                    if depth > 0:
                        val = sub_get_colour(key_s, i_, j_, do_show_=do_show_, depth=depth - 1)

                elif pos == hovered:
                    c_code += "r"
                    print(f"hovered")
                    if hs:
                        c_code += "s"
                        val = val.darkened(0.25) if (hs == "darken") else (
                            val.brightened(0.25) if (hs == "brighten") else val)

            else:
                c_code += "t"
                try:
                    c_code += "u"
                    val = self.__getattribute__(key_)
                except AttributeError:
                    c_code += "v"
                    val = fg if ("_foreground" in key_) else bg

            print(f"CC={c_code.ljust(15)}, C='{val.hex_code}', ij=({i_}, {j_}), {key_=}")
            return val

        return sub_get_colour(key, i, j, default, do_show, depth=1)

    def get_colour2(self, key, i=None, j=None, default=None, do_show=False):
        selected = self.v_cell_ids_selected.get()
        hovered = self.v_cell_ids_hovered.get()
        if do_show:
            print(f"\nPRE GC {key=}, ij=({i}, {j}), {default=}, {selected=}, {hovered=}")

        ds = self.colour_scheme_day
        cs = self.colour_scheme_month
        is_ = self.invalid_style
        hs = self.hover_style
        dc = self.disabled_cells
        dtc = self.set_date_cells

        key_n = key.replace("_active", "").replace("active_", "")
        key_b = key if ("_background" in key) else key.replace("_foreground", "_background")

        valid_style_keys = {
            "colour_background_canvas": iscolour,
            "colour_background_owned_number_check": iscolour,
            "colour_background_header_year": iscolour,
            "colour_background_header_month": iscolour,
            "colour_background_header_weekday": iscolour,
            "colour_foreground_header_weekday": iscolour,

            "colour_foreground_canvas": iscolour,
            "colour_foreground_header_month": iscolour,

            "colour_background_canvas_selected": iscolour,
            "colour_foreground_canvas_selected": iscolour,

            "colour_active_background_canvas": iscolour
        }

        if key not in valid_style_keys:
            if key_n not in valid_style_keys:
                raise ValueError(f"Key '{key}' is not recognized as a valid colour ss_key.")

        val = ds.get(key)

        if do_show:
            print(f"A -- {val=}")
        if not val:
            val = cs.get(key)

        if do_show:
            print(f"B -- {val=}")
        if not val:
            try:
                val_b = None
                # print(f"{ss_key=}, {key_b=}, {key_n=}")
                if key != key_b:
                    print(f'O -- {val=}')
                    val_b = ds.get(key_b)
                    if not val_b:
                        val_b = cs.get(key_b)
                    if not val_b:
                        val_b = self.__getattribute__(key_b)
                    #
                    print(f'P -- {val_b=}')
                    val = val_b.font_foreground_c()
                    print(f'Q -- {val=}')

                if not val_b:
                    val = self.__getattribute__(key) if (default is None) else default
                else:
                    val = val_b.font_foreground_c()

                if do_show:
                    print(f"C -- {val=}")
            except AttributeError:
                try:

                    if key != key_n:
                        val = self.__getattribute__(key_n)
                        if do_show:
                            print(f"D -- {val=}")
                        # val = (val.darkened(0.25) if hs == "darken" else val.brightened(0.25)).font_foreground_c()
                        # print(f"E: {val=}")
                except AttributeError:
                    val = self.colour_background_canvas
                    if do_show:
                        print(f"E -- {val=}")

        if (i is not None) and (j is not None):
            # if (i, j) in self.dict_canvas_tags:
            #     print(f"TEXT => {self.itemcget(self.dict_canvas_tags[(i, j)]['text'], 'text')}")
            # else:
            #     print(f"NO TEXT =><=")
            if do_show:
                print(f"F -- {val=}")
            # # p_a = j // 7
            # # p_ba = (i - ri) // (self.weeks_per_month + self.show_weekdays)
            # # p_bb = p_ba * self.months_per_row
            # # cal_idx = p_a + p_bb
            # if do_show:
            #     print(f"cell_to_date={self.cell_to_date}")
            cal_idx = self.dict_cell_to_cal_idx[(i, j)]
            date_in = self.cell_to_date.get((i, j))

            if cs.get(cal_idx):
                if cs[cal_idx].get(key) is None:
                    if cs[cal_idx].get(key_n) is not None:
                        val = cs[cal_idx][key_n]
                else:
                    val = cs[cal_idx][key]
            if do_show:
                print(f"G -- {val=}")
                print(f"{cal_idx=}, {date_in=}")
            if date_in:

                if hs and ((i, j) == hovered):
                    val = val.darkened(0.25) if (hs == "darken") else (
                        val.brightened(0.25) if (hs == "brighten") else val)
                    print(f"H -- {val=}")

                dm_idx, dd_idx = (date_in.month, date_in.day) if isinstance(date_in, datetime.datetime) else date_in
                if do_show:
                    print(f"{dm_idx=}, {dd_idx=}")
                if (i, j) in dc:
                    # disabled cell
                    if do_show:
                        print(f"I -- {val=}")

                    cs_ij = cs.get(cal_idx, {})
                    ds_ij = ds.get((dm_idx, dd_idx), {})
                    bg, fg = None, None
                    if ds_ij:
                        bg = ds_ij.get("colour_background_canvas")
                        fg = ds_ij.get("colour_foreground_canvas")
                    if not bg:
                        bg = cs_ij.get("colour_background_canvas")
                    if not fg:
                        fg = cs_ij.get("colour_foreground_canvas")
                    if not bg:
                        bg = self.colour_background_canvas.darkened(0.3)
                    if not fg:
                        fg = self.colour_foreground_canvas.darkened(0.3)

                    val = fg if ("_foreground" in key) else bg
                    if do_show:
                        print(f"J -- {val=}")

                elif (i, j) == selected:
                    # selected cell
                    key_n = f"{key.removesuffix('_selected')}_selected"
                    val = self.__getattribute__(key_n)
                    if do_show:
                        print(f"K -- {val=}")
            else:
                if not self.finished_init:
                    return val
                if do_show:
                    print(f"L -- {val=}")
                    print(f"{is_=}, {dtc=}")

                if is_ is None:
                    # no invalid style
                    return val
                if (i, j) not in dtc:
                    # invalid cell
                    if do_show:
                        print(f"M -- {val=}")

                    # val = (val.darkened(0.25) if hs == "darken" else val.brightened(0.25))
                    if (i, j) == hovered:
                        val = val.darkened(0.25) if (is_ == "darken") else (
                            val.brightened(0.25) if (is_ == "brighten") else val)

                        if do_show:
                            print(f"N -- {val=}")

        # # disabled
        # tr = self.dict_canvas_tags[(i, j)]["rect"]
        # tt = self.dict_canvas_tags[(i, j)]["text"]
        # cs = self.colour_scheme_month.get(m_idx, {})
        # ds = self.colour_scheme_day.get((m_idx, d_idx), {})
        # bg, fg = None, None
        # if ds:
        #     bg = ds.get("colour_background_canvas")
        #     fg = ds.get("colour_foreground_canvas")
        # if not bg:
        #     bg = cs.get("colour_background_canvas")
        # if not fg:
        #     fg = cs.get("colour_foreground_canvas")
        # if not bg:
        #     bg = self.colour_background_canvas.darkened(0.3)
        # if not fg:
        #     fg = self.colour_foreground_canvas.darkened(0.3)

        if do_show:
            print(f"GC: {val.hex_code}, {i=}, {j=}, {key=}, {key_n=}, {default=}")
        return val

    # def get_cell_colour(self, n):
    #     # n is offset by 1
    #     if self.owned_numbers[n] > 0:
    #         if self.v_sw_show_heat_map.get():
    #             # return Colour(random_colour(name=True))
    #             return self.heat_map_colours[n]
    #         else:
    #             return self.colour_background_owned_number_check
    #     else:
    #         return self.colour_background_canvas
    def click_canvas(self, event, i, j):
        print(f"click_canvas {i=}, {j=}, {event=}", end="")
        if (i, j) in self.disabled_cells:
            return
        last_select: tuple[int, int] = self.v_cell_ids_selected.get()
        last_select = eval(last_select) if (last_select and isinstance(last_select, str)) else last_select
        if (i, j) == last_select:
            self.deselect_day()
            return
        tr = self.dict_canvas_tags[(i, j)]["rect"]
        tt = self.dict_canvas_tags[(i, j)]["text"]
        cal_idx = self.dict_cell_to_cal_idx[(i, j)]
        text: str = self.itemcget(tt, "text")
        text_vis: str = self.itemcget(tt, "state") != "hidden"
        year = self.year if self.year is not None else datetime.datetime.now().year
        if text_vis and text.isdigit():
            print(f" {year=}, month={cal_idx + 1}, day={int(text)}")
            # TODO highlight that this is now selected

            self.v_cell_ids_selected.set((i, j))
            print(f"{last_select=}")
            if last_select:
                # cal_idx_lh = self.dict_cell_to_cal_idx[last_select]
                # ds = self.colour_scheme_day
                # cs = self.colour_scheme_month
                # bg = self.get_colour("colour_background_canvas", i, j)
                # cs_lh = self.colour_scheme_month.get(cal_idx_lh, {})
                # col_lh = cs_lh.get("colour_background_canvas", self.colour_background_canvas)
                # col_txt_lh = cs_lh.get("colour_foreground_canvas", col_lh.font_foreground_c())
                col_lh = self.get_colour("colour_background_canvas", *last_select)
                col_txt_lh = self.get_colour("colour_foreground_canvas", *last_select)
                self.itemconfigure(
                    self.dict_canvas_tags[last_select]["rect"],
                    fill=col_lh.hex_code
                )
                self.itemconfigure(
                    self.dict_canvas_tags[last_select]["text"],
                    fill=col_txt_lh.hex_code
                )

            self.selected_date.set(datetime.datetime(year, cal_idx + 1, int(text)))

        print(f" SD={self.selected_date.get()}")
        # self.tb_canvas_click_data.delete("0.0", ctk.END)
        # n = ((i * self.n_cols) + j) + 1
        #
        # if not self.v_canvas_has_been_clicked.get():
        #     self.lbl_canvas_click_instruction.grid_forget()
        #     self.tb_canvas_click_data.grid(row=0, column=0, rowspan=1, columnspan=1)
        #     self.v_canvas_has_been_clicked.set(True)
        #
        # n = datetime.datetime(datetime.datetime.now().year, 1, 1) + datetime.timedelta(days=n-1)
        # print(f"{n=}")
        # df_timeline_order_receive = self.ctk_.df_timeline_order_receive.loc[(self.ctk_.df_timeline_order_receive["DOB"].dt.month == n.month) & (self.ctk_.df_timeline_order_receive["DOB"].dt.day == n.day)]
        # df_timeline_order_receive = df_timeline_order_receive.sort_values(by=["Team", "PlayerLast", "PlayerFirst"])
        # text = ""
        # for k, row in df_timeline_order_receive.iterrows():
        #     # text += f"{row['Team'].center(22)} - {row['PlayerFirst'].rjust(11)} {row['PlayerLast'].ljust(18)}\n"
        #     text += f"{row['Team'].center(22)} - {row['PlayerLast']}, {row['PlayerFirst']}\n"
        # if df_timeline_order_receive.shape[0] == 0:
        #     text = "No Data"
        # self.tb_canvas_click_data.insert("0.0", text)

    def motion_cell(self, event, i, j, t_):
        if self.id_after_motion is not None:
            self.after_cancel(self.id_after_motion)

        self.id_after_motion = self.after(self.time_after_motion, self.after_motion)

        # cal_idx = self.dict_cell_to_cal_idx[(i, j)]
        #
        # cs = self.colour_scheme_month.get(cal_idx, {})
        # col = cs.get("colour_background_canvas", self.colour_background_canvas)
        # col_txt = cs.get("colour_foreground_canvas", col.font_foreground_c())
        hs = self.hover_style
        is_ = self.invalid_style
        tr = self.dict_canvas_tags[(i, j)]["rect"]
        tt = self.dict_canvas_tags[(i, j)]["text"]

        last_hover = self.v_cell_ids_hovered.get()
        selected = self.v_cell_ids_selected.get()
        # last_hover = eval(last_hover) if last_hover else ""
        # selected = eval(selected) if selected else ""
        # print(f"{last_hover=}, {selected=} {type(last_hover)=}, {type(selected)=}, {i=}, {j=}")
        print(
            f"ij=({i}, {j}), lh={last_hover}, sl={selected} tlh={type(last_hover)}, tsl{type(selected)}, {is_=}, {hs=}")

        # last_hover = eval(self.v_cell_ids_hovered.get())
        # selected = eval(self.v_cell_ids_selected.get())
        # print(f"LH={last_hover}, IJ={(i, j)=}, {col.hex_code=}, {col_txt.hex_code=}")

        if last_hover and (last_hover != selected) and (last_hover != (i, j)):
            print(f"--A")
            # cal_idx_lh = (last_hover[0] // 7) + (last_hover[1] // 7)  # + (i * ((7 * self.months_per_row) // self.weeks_per_month))
            cal_idx_lh = self.dict_cell_to_cal_idx[last_hover]
            cs_lh = self.colour_scheme_month.get(cal_idx_lh, {})
            # col_lh = cs_lh.get("colour_background_canvas", self.colour_background_canvas)
            # col_txt_lh = cs_lh.get("colour_foreground_canvas", col_lh.font_foreground_c())
            print(f"Correcting last_hover")
            self.v_cell_ids_hovered.set(tuple())
            col_lh = self.get_colour("colour_background_canvas", *last_hover)
            col_txt_lh = self.get_colour("colour_foreground_canvas", *last_hover)
            self.itemconfigure(
                self.dict_canvas_tags[last_hover]["rect"],
                fill=col_lh.hex_code
            )
            self.itemconfigure(
                self.dict_canvas_tags[last_hover]["text"],
                fill=col_txt_lh.hex_code
            )

        "FF7F50"
        "AEBEBE"
        "FFBF90"

        # too slow
        # for r in range(self.n_rows):
        #     for c in range(self.n_cols):
        #         self.itemconfigure(
        #             self.dict_canvas_tags[(r, c)]["rect"],
        #             fill=col.hex_code
        #         )
        #         self.itemconfigure(
        #             self.dict_canvas_tags[(r, c)]["text"],
        #             fill=col_txt.hex_code
        #         )

        if (i, j) in self.disabled_cells:
            print(f"QUIT")
            return

        # print(f"{self.itemcget(tt, 'state')=}")
        text_vis = self.itemcget(tt, "state") != "hidden"
        print(f"{self.set_date_cells=}")
        if not text_vis:
            print(f"--B")
            if is_ is None:
                # invalid cell (no visible date) and invalid_style is None
                return

            # if ((i, j) in self.set_date_cells) and ((i, j) != selected):
            if (i, j) not in self.set_date_cells:
                print(f"New colour")
                self.v_cell_ids_hovered.set((i, j))
                col_a = self.get_colour("colour_active_background_canvas", i, j)
                # col_a = cs.get("colour_active_background_canvas")
                # if col_a is None:
                #     col_a = col.darkened(0.25) if is_ == "darken" else (col.brightened(0.25) if is_ == "brighten" else self.colour_background_canvas)
                # # col_txt_a = cs.get("colour_active_foreground_canvas")
                # # if col_txt_a is None:
                # #     col_txt_a = (col.darkened(0.25) if is_ == "darken" else col.brightened(0.25)).font_foreground_c()
                #     # col_txt_a = col_a.font_foreground_c()
                # # print(f"{col_a.hex_code=}, {col_txt_a.hex_code=}")
                self.itemconfigure(
                    tr,
                    fill=col_a.hex_code
                )
                # self.itemconfigure(
                #     tt,
                #     fill=col_txt_a.hex_code
                # )
            return

        if hs is not None:
            # print(f"--C")
            # # if ((i, j) in self.set_date_cells) and ((i, j) != selected):
            if (i, j) in self.set_date_cells:
                # print(f"--D")
                # # col_a = cs.get("colour_active_background_canvas")
                col = self.get_colour("colour_active_background_canvas", i, j)
                # if col_a is None:
                #     col_a = col.darkened(0.25) if hs == "darken" else col.brightened(0.25)
                # col_txt_a = cs.get("colour_active_foreground_canvas")
                col_txt_a = self.get_colour("colour_active_foreground_canvas", i, j)
                if col_txt_a is None:
                    col_txt_a = (col.darkened(0.25) if hs == "darken" else col.brightened(0.25)).font_foreground_c()
                # print(f"{col_a.hex_code=}, {col_txt_a.hex_code=}")
                self.itemconfigure(
                    tr,
                    fill=col.hex_code
                )
                self.itemconfigure(
                    tt,
                    fill=col_txt_a.hex_code
                )
                if (i, j) != selected:
                    self.v_cell_ids_hovered.set((i, j))

    def after_motion(self, *args):
        mx = self.winfo_pointerx()
        my = self.winfo_pointery()
        # bbox_canvas = self.bbox("all")
        # bbox_canvas = self.grid_bbox()
        # bbox_canvas = self.master.bbox(self)
        bbox_canvas = (self.winfo_rootx(), self.winfo_rooty(), self.winfo_width(), self.winfo_height())
        # print(f"{mx=}, {my=}, {bbox_canvas=}")
        self.id_after_motion = None

        if not ((bbox_canvas[0] <= mx <= bbox_canvas[2]) and (bbox_canvas[1] <= my <= bbox_canvas[3])):
            last_hover = self.v_cell_ids_hovered.get()
            selected = self.v_cell_ids_selected.get()
            # print(f"LH={last_hover}, IJ={(i, j)=}, {col.hex_code=}, {col_txt.hex_code=}")

            if last_hover and (last_hover != selected):
                # cal_idx_lh = (last_hover[0] // 7) + (last_hover[1] // 7)  # + (i * ((7 * self.months_per_row) // self.weeks_per_month))
                # cal_idx_lh = self.dict_cell_to_cal_idx[last_hover]
                # cs_lh = self.colour_scheme_month.get(cal_idx_lh, {})
                # col_lh = cs_lh.get("colour_background_canvas", self.colour_background_canvas)
                # col_txt_lh = cs_lh.get("colour_foreground_canvas", col_lh.font_foreground_c())
                self.v_cell_ids_hovered.set(tuple())
                col_lh = self.get_colour("colour_background_canvas", *last_hover)
                col_txt_lh = self.get_colour("colour_foreground_canvas", *last_hover)
                self.itemconfigure(
                    self.dict_canvas_tags[last_hover]["rect"],
                    fill=col_lh.hex_code
                )
                self.itemconfigure(
                    self.dict_canvas_tags[last_hover]["text"],
                    fill=col_txt_lh.hex_code
                )

    def update_selected_date(self, *args):
        print(f"update_selected_date")
        select: tuple[int, int] = self.v_cell_ids_selected.get()
        if select:
            cal_idx_lh = self.dict_cell_to_cal_idx[select]
            cs_lh = self.colour_scheme_month.get(cal_idx_lh, {})
            # col_lh = cs_lh.get("colour_background_canvas_selected", self.colour_background_canvas_selected)
            # col_txt_lh = cs_lh.get("colour_foreground_canvas_selected", self.colour_foreground_canvas_selected)
            col_lh = self.get_colour("colour_background_canvas_selected", *select)
            col_txt_lh = self.get_colour("colour_foreground_canvas_selected", *select)
            self.itemconfigure(
                self.dict_canvas_tags[select]["rect"],
                fill=col_lh.hex_code
            )
            self.itemconfigure(
                self.dict_canvas_tags[select]["text"],
                fill=col_txt_lh.hex_code
            )


def entry_factory(master, tv_label=None, tv_entry=None, kwargs_label=None, kwargs_entry=None):
    """Return customtkinter StringVar, Label, StringVar, Entry objects"""
    if tv_label is not None and tv_entry is not None:
        res_tv_label = tv_label if isinstance(tv_label, ctk.Variable) else ctk.StringVar(master, value=tv_label)
        res_tv_entry = tv_entry if isinstance(tv_entry, ctk.Variable) else ctk.StringVar(master, value=tv_entry)
    elif tv_label is not None:
        res_tv_label = tv_label if isinstance(tv_label, ctk.Variable) else ctk.StringVar(master, value=tv_label)
        res_tv_entry = ctk.StringVar(master)
    elif tv_entry is not None:
        res_tv_label = ctk.StringVar(master)
        res_tv_entry = tv_entry if isinstance(tv_entry, ctk.Variable) else ctk.StringVar(master, value=tv_entry)
    else:
        res_tv_label = ctk.StringVar(master)
        res_tv_entry = ctk.StringVar(master)

    if kwargs_label is not None and kwargs_entry is not None:
        res_label = ctk.CTkLabel(master, textvariable=res_tv_label, **kwargs_label)
        res_entry = ctk.CTkEntry(master, textvariable=res_tv_entry, **kwargs_entry)
    elif kwargs_label is not None:
        res_label = ctk.CTkLabel(master, textvariable=res_tv_label, **kwargs_label)
        res_entry = ctk.CTkEntry(master, textvariable=res_tv_entry)
    elif kwargs_entry is not None:
        res_label = ctk.CTkLabel(master, textvariable=res_tv_label)
        res_entry = ctk.CTkEntry(master, textvariable=res_tv_entry, **kwargs_entry)
    else:
        res_label = ctk.CTkLabel(master, textvariable=res_tv_label)
        res_entry = ctk.CTkEntry(master, textvariable=res_tv_entry)
    return res_tv_label, res_label, res_tv_entry, res_entry


def button_factory(master, tv_btn=None, kwargs_btn=None, command=None):
    """Return customtkinter StringVar, Button objects"""

    if kwargs_btn is not None:
        assert isinstance(kwargs_btn,
                          dict), f"Error param 'kwargs_btn' must be a dict if not None. Got: '{kwargs_btn}'."
        if "command" in kwargs_btn and command is not None:
            raise KeyError(
                f"Error, command ss_key has already been passed in param 'kwargs_btn'. Please pass only one command.")
        elif command is not None:
            assert callable(command), "Error, param 'command' is not callable."
            kwargs_btn.update({"command": command})
    elif command is not None:
        assert callable(command), "Error, param 'command' is not callable."
        kwargs_btn = {"command": command}

    if isinstance(tv_btn, ctk.Variable):
        res_tv_btn = tv_btn
    else:
        if tv_btn is not None:
            res_tv_btn = ctk.StringVar(master, value=tv_btn)
        else:
            res_tv_btn = ctk.StringVar(master)
    res_btn = ctk.CTkButton(master, textvariable=res_tv_btn)
    if kwargs_btn is not None:
        res_btn = ctk.CTkButton(master, textvariable=res_tv_btn, **kwargs_btn)
    return res_tv_btn, res_btn


def combo_factory(master, tv_label=None, kwargs_label=None, tv_combo=None, kwargs_combo=None, values=None):
    """Return customtkinter StringVar, Label, StringVar, Entry objects"""
    if tv_label is not None and tv_combo is not None:
        res_tv_label = tv_label if isinstance(tv_label, ctk.Variable) else ctk.StringVar(master, value=tv_label)
        res_tv_combo = tv_combo if isinstance(tv_combo, ctk.Variable) else ctk.StringVar(master, value=tv_combo)
    elif tv_label is not None:
        res_tv_label = tv_label if isinstance(tv_label, ctk.Variable) else ctk.StringVar(master, value=tv_label)
        res_tv_combo = ctk.StringVar(master)
    elif tv_combo is not None:
        res_tv_label = ctk.StringVar(master)
        res_tv_combo = tv_combo if isinstance(tv_combo, ctk.Variable) else ctk.StringVar(master, value=tv_combo)
    else:
        res_tv_label = ctk.StringVar(master)
        res_tv_combo = ctk.StringVar(master)

    if values is not None:
        if not (kcn := kwargs_combo is None) and not (kcvn := kwargs_combo.get("values") is None):
            raise ValueError("Error, cannot explicitly pass values as parameter and in 'kwargs_combo'.")
        else:
            if kcn:
                kwargs_combo = {"values": values}
            else:
                kwargs_combo.update({"values": values})

    if kwargs_label is not None and kwargs_combo is not None:
        res_label = ctk.CTkLabel(master, textvariable=res_tv_label, **kwargs_label)
        res_combo = ctk.CTkComboBox(master, variable=res_tv_combo, **kwargs_combo)
    elif kwargs_label is not None:
        res_label = ctk.CTkLabel(master, textvariable=res_tv_label, **kwargs_label)
        res_combo = ctk.CTkComboBox(master, variable=res_tv_combo)
    elif kwargs_combo is not None:
        res_label = ctk.CTkLabel(master, textvariable=res_tv_label)
        res_combo = ctk.CTkComboBox(master, variable=res_tv_combo, **kwargs_combo)
    else:
        res_label = ctk.CTkLabel(master, textvariable=res_tv_label)
        res_combo = ctk.CTkComboBox(master, variable=res_tv_combo)
    return res_tv_label, res_label, res_tv_combo, res_combo


def label_factory(master, tv_label=None, kwargs_label=None):
    """Return customtkinter StringVar, label objects"""
    if isinstance(tv_label, ctk.Variable):
        res_tv_lbl = tv_label
    else:
        if tv_label is not None:
            res_tv_lbl = ctk.StringVar(master, value=tv_label)
        else:
            res_tv_lbl = ctk.StringVar(master)
    res_lbl = ctk.CTkLabel(master, textvariable=res_tv_lbl)
    if kwargs_label is not None:
        res_lbl = ctk.CTkLabel(master, textvariable=res_tv_lbl, **kwargs_label)
    return res_tv_lbl, res_lbl


def list_factory(master, tv_label=None, kwargs_label=None, tv_list=None, kwargs_list=None):
    """Return customtkinter StringVar, Label, StringVar, Entry objects"""
    if not (isinstance(tv_list, list) or isinstance(tv_list, tuple) or isinstance(tv_list, dict) or isinstance(tv_list,
                                                                                                               set)):
        if tv_list:
            res_tv_list = list(tv_list)
        else:
            res_tv_list = []
    else:
        res_tv_list = tv_list

    res_tv_list = ctk.Variable(master, res_tv_list)

    print(f"{tv_list=}, {res_tv_list=}")

    if tv_label is not None:
        res_tv_label = tv_label if isinstance(tv_label, ctk.Variable) else ctk.StringVar(master, value=tv_label)
    else:
        res_tv_label = ctk.StringVar(master)

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
        res_label = ctk.CTkLabel(master, textvariable=res_tv_label, **kwargs_label)
        res_list = tkinter.Listbox(master, listvariable=res_tv_list, **kwargs_list)
    elif kwargs_label is not None:
        res_label = ctk.CTkLabel(master, textvariable=res_tv_label, **kwargs_label)
        res_list = tkinter.Listbox(master, listvariable=res_tv_list)
    elif kwargs_list is not None:
        res_label = ctk.CTkLabel(master, textvariable=res_tv_label)
        res_list = tkinter.Listbox(master, listvariable=res_tv_list, **kwargs_list)
    else:
        res_label = ctk.CTkLabel(master, textvariable=res_tv_label)
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
                var = ctk.IntVar(master, value=int(default_value))
            else:
                raise ValueError(f"Error default value '{default_value}' is not a number.")
        else:
            print(f"is None")
            var = ctk.IntVar(master, value=-1)

        if 0 > var.get() >= len(buttons):
            raise IndexError("Error var index is out of range")

        # print(f"CREATED {var.get()=}")

        r_buttons = []
        tv_vars = []
        for i, btn in enumerate(buttons):
            # print(f"{i=}, {btn=}, name=rbtn_{str(btn).lower()}, {master=}, {master.winfo_parent()=}, {type(master)=}")
            if isinstance(btn, ctk.Variable):
                tv_var = btn
            else:
                tv_var = ctk.StringVar(master, value=btn)
            tv_vars.append(tv_var)
            if kwargs_buttons is not None:
                print(f"WARNING kwargs param is applied to each radio button")
                r_buttons.append(
                    ctk.CTkRadioButton(master, variable=var, textvariable=tv_var, **kwargs_buttons, value=i,
                                       name=f"rbtn_{btn.replace('.', '_')}"))
            else:
                r_buttons.append(
                    ctk.CTkRadioButton(master, variable=var, textvariable=tv_var, value=i,
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


# class TreeviewExt(ttk.Treeview):
#     def __init__(self, master, *args, **kwargs):
#         super().__init__(master, *args, **kwargs)
#
#         # self.key_delim = "_|_=_|_=_|_"
#         # self.col_keys = ["background", "foreground"]
#         # self.colours = {}
#
#     def treeview_sort_column(self, col, reverse):
#         l = [(self.set(k, col), k) for k in self.get_children('')]
#         l.sort(reverse=reverse)
#
#         # rearrange items in sorted positions
#         for index, (val, k) in enumerate(l):
#             self.move(k, '', index)
#
#         # reverse sort next time
#         self.heading(col, command=lambda: \
#             self.treeview_sort_column(col, not reverse))


class TreeviewController(ctk.CTkScrollableFrame):

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
                          pd.DataFrame), f"Error, param 'dataframe' must be an instance of a pandas Dataframe, got: '{type(df)}'."

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

        # print(f"--CC {self.viewable_column_names=}\n{self.df_timeline_order_receive=}")
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

        # print(f"--AA {self.viewable_column_names=}\n{self.df_timeline_order_receive=}")

        if not isinstance(self.tv_label, ctk.Variable):
            self.tv_label = ctk.StringVar(self, value="")

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

        self.label = ctk.CTkLabel(self, textvariable=self.tv_label, **self.kwargs_label)
        self.treeview = CtkTableExt(
            self,
            table_data=[self.viewable_column_names],
            kwargs_table={
                "header_color": "#680002",
                "hover_color": "#985042",
                "height": 20,
                "colors": ["#AECCFF", "#AEEEFF"],
                "text_color": ["#010203", "#030201"]

            }
        )
        # # self.treeview = TreeviewExt(
        # #     self,
        # #     # columns=list(self.viewable_column_names_indexable.values())
        # #     # columns=self.viewable_column_names
        # #     # , displaycolumns=self.viewable_column_names
        # #     columns=self.viewable_column_names
        # #     # ,displaycolumns=self.viewable_column_names_indexable
        # #     , displaycolumns="#all"
        # #     , **self.kwargs_treeview
        # #     , show=("tree headings" if show_index_column else "headings")
        # #     # , **kwargs
        # # )
        #
        # # print(f"==TC\n{self.df_timeline_order_receive=}\n{viewable_column_names=}")
        #
        # # for i, col in enumerate(self.viewable_column_names_indexable):
        # for i, col in enumerate(self.viewable_column_names):
        #     # if isinstance(self.viewable_column_names, dict):
        #     # col_i = self.viewable_column_names_indexable[col]
        #     # col_i = f"#{i}"
        #     col_i = col
        #     c_width = self.viewable_column_widths[i]
        #     # print(f"{c_width=}, {type(c_width)=}, {i=}, {col=}, {col_i=}")
        #     self.treeview.column(col_i, width=c_width, anchor=tkinter.CENTER)
        #     self.treeview.heading(col_i, text=col, anchor=tkinter.CENTER, command=lambda _col=col_i: \
        #         self.treeview.treeview_sort_column(_col, False))
        #
        # self.idx_width = 50
        # if show_index_column:
        #     self.treeview.column("#0", width=self.idx_width, stretch=False)
        #     self.treeview.heading("#0", text="#", anchor=tkinter.CENTER)
        #
        # # print(f"--BB {df_timeline_order_receive.shape=}\n{self.df_timeline_order_receive}")
        # # print(f"{list(df_timeline_order_receive.itertuples())=}\n{len(list(df_timeline_order_receive.itertuples()))}")
        # # for i, row in df_timeline_order_receive.itertuples():
        # # f = list(range(1015))

        values = [self.viewable_column_names]
        for i, row in self.df.iterrows():
            values.append([row[c_name] for c_name in self.viewable_column_names])

        # for i, row in self.df_timeline_order_receive.iterrows():
        #     # next(self.iid_namer)
        #     # print(f"{i=}, {row=}, {type(row)=}")
        #     dat = [row[c_name] for c_name in self.viewable_column_names]
        #     tags = (self.gen_row_tag(i),)
        #     self.treeview.insert("", tkinter.END, text=f"{i + 1}", iid=i, values=dat, tags=tags)
        #     # print(f"{tags=}")
        #     # f.remove(i)
        # # print(f"{f=}")
        # # print(f"B {df_timeline_order_receive.shape=}")
        # # print(f"{len(list(df_timeline_order_receive.iterrows()))=}")

        # # treeview.bind("<<TreeviewSelect>>", CALLBACK_HERE)
        # self.scrollbar_x, self.scrollbar_y = None, None
        # if self.include_scroll_y:
        #     self.scrollbar_y = ttk.Scrollbar(self, orient=tkinter.VERTICAL,
        #                                      command=self.treeview.yview)
        # if self.include_scroll_x:
        #     self.scrollbar_x = ttk.Scrollbar(self, orient=tkinter.HORIZONTAL,
        #                                      command=self.treeview.xview)
        # if self.scrollbar_x is not None and self.scrollbar_y is not None:
        #     self.treeview.configure(yscrollcommand=self.scrollbar_y.set, xscrollcommand=self.scrollbar_x.set)
        # elif self.scrollbar_x is not None:
        #     self.treeview.configure(xscrollcommand=self.scrollbar_x.set)
        # elif self.scrollbar_y is not None:
        #     self.treeview.configure(yscrollcommand=self.scrollbar_y.set)

        self.tv_button_new_item, self.button_new_item = button_factory(self, tv_btn="new cell_is_entry",
                                                                       kwargs_btn={
                                                                           "command": self.insert_new_random_entry})
        self.tv_button_delete_item, self.button_delete_item = button_factory(self, tv_btn="del cell_is_entry",
                                                                             kwargs_btn={"command": self.delete_entry})
        # button_new_item.pack()
        # button_delete_item.pack()

        self.frame_aggregate_row = ctk.CTkFrame(self)
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
            # print(f"HERE {k=}, {ss_key=}, {idx=}, {order_a=}")
            # order_a.insert(idx, (ss_key, k))
            order_a[idx + 1] = (key, k)

        # print(f'B {order_a=}')

        for key in order_a:
            # print(f"Analyzing COLUMN '{ss_key}'")
            key, k = key
            # col_data = self.treeview.column(ss_key)
            # width = col_data.get("width_canvas")
            # width = int(width * self.p_width) if width is not None else 10
            width = 60
            x1, x2 = self.column_x(key)
            if k in self.aggregate_data:
                # v = self.aggregate_data[k]
                # tv = tkinter.StringVar(self, value=f"{ss_key=}, {v=}")
                tv = ctk.StringVar(self, value=self.calc_aggregate_value(key))
                entry = ctk.CTkEntry(
                    self.frame_aggregate_row,
                    textvariable=tv,
                    width=width,
                    state="readonly",
                    justify=tkinter.CENTER
                )
            else:
                # tv = tkinter.StringVar(self, value=f"{ss_key=}, {v=}")
                tv = tkinter.StringVar(self, value="")
                entry = ctk.CTkEntry(
                    self.frame_aggregate_row,
                    textvariable=tv,
                    width=width,
                    state="readonly",
                    justify=tkinter.CENTER
                )

            self.aggregate_objects.append(
                (tv, entry, (x1, x2))
            )

            # print(f"{ss_key=}, {ss_key=}, {v=}")
            # # print(f"{self.treeview.bbox(column=ss_key)=}, {type(self.treeview.bbox(ss_key))=}")
            # print(f"{self.treeview.column(ss_key)=}, {type(self.treeview.column(ss_key))=}")
            # print(f"{self.treeview.heading(ss_key)=}, {type(self.treeview.heading(ss_key))=}")

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
        width = 60
        for i, name in enumerate(self.viewable_column_names):
            # col_data = self.treeview.column(name)
            # x2 += col_data.get("width_canvas", 0)
            x2 += width
            if name != column_name:
                # x1 += col_data.get("width_canvas", 0)
                x1 += width
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


class MultiComboBox(ctk.CTkScrollableFrame):

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
                          pd.DataFrame), f"Error param 'data' must be an instance of a pandas.DataFrame, got '{type(data)}'."
        assert False if (kwargs_combo and (
                "values" in kwargs_combo)) else True, f"Cannot pass values as a keyword argument here. Pass all data in the data param as a pandas.DataFrame."
        # assert auto_pack + auto_grid <= 1, f"Error parameters 'auto_pack'={auto_pack} and 'auto_grid'={auto_grid} must be in a configuration where both params are not True.\nCannot grid and pack child widgets. (1 or None)"

        # print(f"{lock_result_col=}\n{viewable_column_names=}\n{data.columns=}")
        if lock_result_col is not None:
            assert (
                (lock_result_col in viewable_column_names) if isinstance(viewable_column_names, (list, tuple)) else (
                            lock_result_col in viewable_column_names.values())) if viewable_column_names else ((
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
        # self.namer = alpha_seq(10000000)
        # self.top_most = patriarch(master)
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
            self.res_tv_label = tv_label if isinstance(tv_label, ctk.Variable) else ctk.StringVar(self, value=tv_label)
            self.res_tv_entry = tv_combo if isinstance(tv_combo, ctk.Variable) else ctk.StringVar(self, value=tv_combo)
        elif tv_label is not None:
            self.res_tv_label = tv_label if isinstance(tv_label, ctk.Variable) else ctk.StringVar(self, value=tv_label)
            self.res_tv_entry = ctk.StringVar(self)
        elif tv_combo is not None:
            self.res_tv_label = ctk.StringVar(self)
            self.res_tv_entry = tv_combo if isinstance(tv_combo, ctk.Variable) else ctk.StringVar(self, value=tv_combo)
        else:
            self.res_tv_label = ctk.StringVar(self)
            self.res_tv_entry = ctk.StringVar(self)

        if kwargs_label is not None and kwargs_combo is not None:
            self.res_label = ctk.CTkLabel(self, textvariable=self.res_tv_label, **kwargs_label)
        elif kwargs_label is not None:
            self.res_label = ctk.CTkLabel(self, textvariable=self.res_tv_label, **kwargs_label)
        elif kwargs_combo is not None:
            self.res_label = ctk.CTkLabel(self, textvariable=self.res_tv_label)
        else:
            self.res_label = ctk.CTkLabel(self, textvariable=self.res_tv_label)

        self.frame_top_most = ctk.CTkFrame(self, name="ftm")
        self.frame_tree = ctk.CTkFrame(self, name="ft")

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

        # print(f"PRE {self.tree_controller.df_timeline_order_receive=}")
        if self.nan_repr is not None:
            self.tree_controller.df = self.tree_controller.df.fillna(self.nan_repr)
        # print(f"POST {self.tree_controller.df_timeline_order_receive=}")

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
        self.btn_clear = tkinter.Button(self.frame_top_most, textvariable=self.tv_btn_clear,
                                        command=self.click_btn_clear)
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
        # print(f"END SETUP {self.tree_controller.df_timeline_order_receive=}")

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
        print(
            f"{do_grid=}, {self.include_searching_widgets=}, {self.include_drop_down_arrow=}, {self.tv_tree_is_hidden.get()=}")

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

    def delete_item(self, iid=None, value="|/|/||NONE||/|/|", mode="first" | Literal["first", "all", "ask"]):
        print(f"delete_item: {iid=}, {value=}, {mode=}")
        print(f"A self.data=\n{self.data}")
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
                for i, row in self.data.iterrows():
                    for j, x in enumerate(row.values):
                        if value == x:
                            to_delete.append(i)
                            break
                        elif self.use_str_dtype and (str(value) == x):
                            to_delete.append(i)
                            break
                    if to_delete and not delete_multi:
                        break

                if to_delete:
                    # print(f"DROPPING {to_delete=}")
                    # print(f"PRE  SHAPE: {self.data.shape=}")
                    # print(f"{self.data.head(5)}")
                    # print(f"{self.data.iloc[to_delete[0] - 3: to_delete[0] + 3]}")
                    self.data.drop(to_delete, inplace=True)
                    self.data.reset_index(drop=True, inplace=True)
                    # print(f"POST SHAPE: {self.data.shape=}")
                    # print(f"{self.data.head(5)}")
                    # print(f"{self.data.iloc[to_delete[0] - 3: to_delete[0] + 3]}")
                else:
                    raise ValueError(
                        f"Cannot delete row(s) containing value '{value}' from this dataframe. The value was not found was not Found.")

        print(f"B self.data=\n{self.data}")
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
                        # for df_timeline_order_receive, vals, tags in new_dfs:
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
                # # for df_, vals_, tags_ in zip(df_timeline_order_receive.iterrows(), vals, tags):
                #     print(f"INSERTING {vals_=}, {k+i=}, {tags_=}, {i=}")
                self.tree_treeview.insert("", "end", iid=k + i, text=str(k + i + 1), values=vals_, tags=tuple(tags_))
            k += df.shape[0]
        self.data = pd.concat([self.data, *[df for df, *rest in new_dfs]], ignore_index=True)

        if self.nan_repr is not None:
            self.tree_controller.df = self.tree_controller.df.fillna(self.nan_repr)
            self.data = self.data.fillna(self.nan_repr)

        # print(f"END==\n{self.data=}")

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


class PrioritySelection(ctk.CTkCanvas):

    def __init__(
            self,
            master,
            values: list,
            variable: ctk.Variable = None,
            orientation: Literal["vertical", "horizontal"] = "vertical",
            width: Optional[int] = None,
            height: Optional[int] = None,
            *args,
            **kwargs
    ):
        super().__init__(master, width=width, height=height, *args, **kwargs)

        self.values_og = values.copy()
        self.variable = variable if isinstance(variable, ctk.Variable) else ctk.Variable(self, value=list())
        self.orientation = orientation

        if width is None:
            width = 80 if self.orientation == "vertical" else 400
            self.configure(width=width)
        if height is None:
            height = 80 if self.orientation == "horizontal" else 400
            self.configure(height=height)
        self.width = width
        self.height = height

        self.colour_bg_btns = Colour("#193988")
        self.colour_fg_btns = Colour("#CCCCCC")
        self.colour_separator = Colour("#000000")
        self.font_btn_text = ("Helvetica", 14, "bold")

        self.n_rows = len(values)
        self.n_cols = 1
        self.doing_animation = ctk.BooleanVar(self, value=False)
        self.last_animated = ctk.Variable(self, value=None)

        if self.orientation == "horizontal":
            self.n_rows, self.n_cols = self.n_cols, self.n_rows

        self.gc_xpad = max(20, int(round(self.width * 0.15, 0)))
        self.gc_ypad = max(20, int(round(self.height * 0.15, 0)))
        self.gc = grid_cells(
            self.width,
            self.n_cols,
            self.height,
            self.n_rows,
            x_pad=self.gc_xpad,
            y_pad=self.gc_ypad
        )

        self.width_btn = abs(self.gc[0][0][2] - self.gc[0][0][0])
        self.height_btn = abs(self.gc[0][0][3] - self.gc[0][0][1])
        # print(f"{self.gc[0][0]=}\n{self.width_btn=}\n{self.height_btn=}\n{self.gc_xpad=}\n{self.gc_ypad=}")

        self.tags = dict()
        self.dragging = ctk.Variable(self, value=list())

        for i, row in enumerate(self.gc):
            for j, bbox in enumerate(row):
                idx = i if self.orientation == "vertical" else j
                txt = self.values_og[idx]
                x0, y0, x1, y1 = bbox
                w, h = x1 - x0, y1 - y0
                fill = self.colour_bg_btns
                fill_fg = self.colour_fg_btns
                self.tags[(i, j)] = {
                    "rect": self.create_rectangle(
                        *bbox,
                        fill=fill.hex_code
                    ),
                    "text": self.create_text(
                        x0 + ((x1 - x0) / 2),
                        y0 + ((y1 - y0) / 2),
                        text=txt,
                        fill=fill_fg.hex_code,
                        font=self.font_btn_text
                    ),
                    "idx": idx
                }

                if (j > 0) and (self.orientation == "horizontal"):
                    # x0, y0, x1, y1 = row[0]
                    self.tags[j] = {
                        "line": self.create_line(
                            x0 - (self.gc_xpad / 2),
                            y0 - 5,
                            x0 - (self.gc_xpad / 2),
                            y0 + h + 5,
                            fill=self.colour_separator.hex_code
                        )
                    }

            if (i > 0) and (self.orientation == "vertical"):
                x0, y0, x1, y1 = row[0]
                w, h = x1 - x0, y1 - y0
                self.tags[i] = {
                    "line": self.create_line(
                        x0 - 5,
                        y0 - (self.gc_ypad / 2),
                        x0 + w + 5,
                        y0 - (self.gc_ypad / 2),
                        fill=self.colour_separator.hex_code
                    )
                }

        self.bind("<Button-1>", self.click_canvas)
        self.bind("<Button1-Motion>", self.motion_canvas)
        self.bind("<ButtonRelease-1>", self.release_click_canvas)
        self.doing_animation.trace_variable("w", self.update_doing_animation)

    def update_doing_animation(self, *args):
        print(f"DA Update -> {self.doing_animation.get()}")

    def release_click_canvas(self, event):
        x, y = event.x, event.y
        dg_str = self.dragging.get()
        print(f"RELEASE CLICK {x=}, {y=}, {dg_str=}")
        dg = list() if not dg_str else list(dg_str)
        la = self.last_animated.get()
        print(f"RELEASE CLICK {x=}, {y=}, {dg=}, {la=}")
        ori = self.orientation
        t_anim_ms = 1250

        bw, bh = self.width_btn, self.height_btn
        bwh, bhh = bw / 2, bh / 2
        # bbox_c = self.bbox("all")
        bbox_c = (0, 0, self.width, self.height)
        xc0, yc0, xc1, yc1 = bbox_c

        for i, key in enumerate(dg):
            i_, j_ = key
            tag_rect = self.tags[key]["rect"]
            tag_text = self.tags[key]["text"]
            opt_idx = self.tags[key]["idx"]
            txt = self.itemcget(tag_text, "text")
            bbox = self.bbox(tag_rect)
            mid_bbox = (
                bbox[0] + ((bbox[2] - bbox[0]) / 2),
                bbox[1] + ((bbox[3] - bbox[1]) / 2)
            )
            closest = None, None
            for p, row in enumerate(self.gc):
                for q, opt_bbox in enumerate(row):
                    if (p, q) != key:
                        mid_opt_bbox = (
                            opt_bbox[0] + ((opt_bbox[2] - opt_bbox[0]) / 2),
                            opt_bbox[1] + ((opt_bbox[3] - opt_bbox[1]) / 2)
                        )
                        d = math.sqrt(
                            math.pow(mid_bbox[0] - mid_opt_bbox[0], 2)
                            + math.pow(mid_bbox[1] - mid_opt_bbox[1], 2)
                        )
                        # print(f"{p=}, {q=}, {d=}")
                        if (closest[0] is None) or (d < closest[1]):
                            closest = (p, q), d

            if closest[0]:
                p_, q_ = closest[0]
                opt_idx_new = p_ if ori == "vertical" else q_
                txt_ = self.itemcget(self.tags[key]["text"], "text")
                new_txt = self.itemcget(self.tags[closest[0]]["text"], "text")
                print(f"SWAP WITH {opt_idx_new=}, drag_txt={txt_}, new_text={new_txt}")
                # if (int(txt_), opt_idx) != la:
                #     self.animate_swap(int(txt_), opt_idx, a_time_ms=t_anim_ms)
                self.animate_swap(opt_idx, opt_idx_new, a_time_ms=t_anim_ms)

            print(f"{opt_idx=}, {txt=}")
            print(f"{closest=}")
            print(f"CURR BBOX: {bbox}")
            print(f"OG BBOX:   {self.gc[i_][j_]}")

        self.dragging.set(list())
        self.after(t_anim_ms, lambda: self.last_animated.set(""))

    def click_canvas(self, event):
        x, y = event.x, event.y
        dg_str = self.dragging.get()
        print(f"CLICK {x=}, {y=}, {dg_str=}")
        dg = list() if not dg_str else list(dg_str)
        print(f"CLICK {x=}, {y=}, {dg=}")

        # if self.orientation == "vertical":
        found = False
        for i in range(self.n_rows):
            for j in range(self.n_cols):
                tag_rect = self.tags[(i, j)]["rect"]
                bbox = self.bbox(tag_rect)
                if (bbox[0] <= x <= bbox[2]) and (bbox[1] <= y <= bbox[3]):
                    if (i, j) not in dg:
                        dg.append((i, j))
                        found = True
                if found:
                    break
            if found:
                break

        self.dragging.set(dg)

    def motion_canvas(self, event):
        x, y = event.x, event.y
        # dg_str = self.dragging.get()
        dg = self.dragging.get()
        la = self.last_animated.get()
        print(f"{la=}, {type(la)=}")
        ori = self.orientation
        # print(f"MOTION {x=}, {y=}, {dg_str=}")
        # dg = list() if not dg_str else list(dg_str)
        # print(f"MOTION {x=}, {y=}, {dg=}")

        bw, bh = self.width_btn, self.height_btn
        bwh, bhh = bw / 2, bh / 2
        # bbox_c = self.bbox("all")
        bbox_c = (0, 0, self.width, self.height)
        xc0, yc0, xc1, yc1 = bbox_c
        xp0, yp0, xp1, yp1 = (
            x - bwh,
            y - bhh,
            x + bwh,
            y + bhh
        )
        # print(f"{bbox_c=}, {bw=}, {bh=}")
        print(f"{la=}")

        for i, key in enumerate(dg):
            i_, j_ = key
            tag_rect = self.tags[key]["rect"]
            tag_text = self.tags[key]["text"]
            opt_idx = self.tags[key]["idx"]
            bbox = self.bbox(tag_rect)
            x0, y0, x1, y1 = bbox
            w, h = x1 - x0, y1 - y0

            # bbox_n = (
            #     clamp(xc0, xp1, xc1 - bw),
            #     clamp(yc0, yp1, yc1 - bh),
            #     clamp(xc0 + bw, xp0, xc1),
            #     clamp(yc0 + bh, yp0, yc1),
            # )

            bbox_n = [
                clamp(xc0, xp0, xc1 - bw),
                clamp(yc0, yp0, yc1 - bh),
                clamp(xc0, xp0, xc1 - bw) + bw,
                clamp(yc0, yp0, yc1 - bh) + bh
            ]
            # print(f"\t{bbox=}\n\t{bbox_n=}")

            self.tag_raise(tag_rect)
            self.tag_raise(tag_text)
            self.coords(tag_rect, *bbox_n)
            self.coords(
                tag_text,
                bbox_n[0] + bwh,
                bbox_n[1] + bhh
            )
            # self.gc[i_][j_] = bbox_n.copy()

            print(f"{opt_idx=}, {bbox=}")
            if opt_idx > 0:
                if (la is None) or (len(la) == 0):
                    opt_idx_l = opt_idx - 1
                else:
                    opt_idx_l = la[0] - 1 if (la[0] != 1) else la[0]
                print(f"{opt_idx_l=}")
                tag_left_div = self.tags[opt_idx_l]["line"]
                bbox_left = self.bbox(tag_left_div)
                if ori == "horizontal":
                    print(f"{x=}, {self.last_animated.get()=}")
                    if x < (bbox_left[0] + bwh):
                        # crossed into other box
                        if (not self.doing_animation.get()) and (la != (opt_idx_l, opt_idx_l + 1)):
                            self.animate_swap(opt_idx_l, opt_idx_l + 1)

            if opt_idx < (len(self.values_og) - 1):
                tag_right_div = self.tags[opt_idx + 1]["line"]
                bbox_right = self.bbox(tag_left_div)

    def animate_swap(self, idx_0, idx_1, a_time_ms=1600, n_frames=60):
        print(f"Animate {idx_0} -> {idx_1} in {n_frames} frames over {a_time_ms} ms")
        # self.doing_animation.set(True)
        self.last_animated.set((idx_0, idx_1))
        ori = self.orientation

        key0 = (idx_0, 0) if ori == "vertical" else (0, idx_0)
        key1 = (idx_0, 0) if ori == "vertical" else (0, idx_1)
        i0, j0 = key0
        i1, j1 = key1

        t_rect0 = self.tags[key0]["rect"]
        t_text0 = self.tags[key0]["text"]
        t_rect1 = self.tags[key1]["rect"]

        bbox0 = self.gc[i0][j0]
        bbox1 = self.gc[i1][j1]

        bw, bh = self.width_btn, self.height_btn
        bwh, bhh = bw / 2, bh / 2

        mid0 = (bbox0[0] + bwh, bbox0[1] + bhh)
        mid1 = (bbox1[0] + bwh, bbox1[1] + bhh)

        xd = mid1[0] - mid0[0]
        yd = 0  # assume no y change
        xpf = xd / n_frames
        ypf = yd / n_frames
        spf = a_time_ms / n_frames

        print(f"{key0=}, {key1=}, {xpf=}, {ypf=}, {spf=}")

        print(f"{bbox0=}")
        for i in range(n_frames):

            bbox = [
                bbox0[0] + (i * xpf),
                bbox0[1] + (i * ypf),
                bbox0[2] + (i * xpf),
                bbox0[3] + (i * ypf)
            ]
            self.tag_raise(t_rect0)
            self.tag_raise(t_text0)
            self.after(
                int((i + 1) * spf),
                lambda: [
                    self.coords(t_rect0, *bbox),
                    self.coords(
                        t_text0,
                        *[
                            bbox[0] + ((bbox[2] - bbox[0]) / 2),
                            bbox[1] + ((bbox[3] - bbox[1]) / 2)
                        ]
                    )
                ]
            )

            if i == (n_frames - 1):
                print(f"{bbox=}")
        self.after(int((n_frames + 1) * spf), lambda: self.doing_animation.set(False))



class FontSelectFrame(ctk.CTkFrame):
    """
    A frame to use in your own application to let the user choose a font.

    For :class:`~font.Font` object, use :obj:`font` property.
    """

    def __init__(self, master=None, callback=None, **kwargs):
        """
        :param master: master widget
        :type master: widget
        :param callback: callback passed argument
                         (`str` family, `int` size, `bool` bold, `bool` italic, `bool` underline)
        :type callback: function
        :param kwargs: keyword arguments passed on to the :class:`ttk.Frame` initializer
        """
        super().__init__(master, **kwargs)
        self.__callback = callback
        self._family = None
        self._size = 11
        self._bold = False
        self._italic = False
        self._underline = False
        self._overstrike = False

        self.colour_bg_canvas = Colour("#EEEEFE")
        self.colour_fg_canvas = Colour("#000000")

        self.colour_line_can_family_sel = Colour("#882222")

        self.lbl_sample = label_factory(
            self,
            tv_label="Sample Text 123!"
        )

        font_: ctk.CTkFont = self.lbl_sample[1].cget("font")
        family_ = font_.cget("family")
        size_ = font_.cget("size")
        # print(f"{font_=}, {family_=}, {size_=}")

        self.font_families = sorted(set(font.families()))
        self.entry_w = 200
        self.can_w, self.can_h = 300, 7500
        self.can_w_pf, self.can_h_pf = 120, 30
        self.frame_family = ctk.CTkFrame(self)
        self.entry_family = entry_factory(
            self.frame_family,
            tv_entry=family_,
            kwargs_entry={
                "width": self.entry_w,
                "state": ctk.DISABLED,
                "justify": ctk.CENTER,
                "height": self.can_h_pf
            }
        )
        self.btn_dd_family = button_factory(
            self.frame_family,
            tv_btn="v",
            command=self.click_btn_dd_family,
            kwargs_btn={
                "width": 10,
                "height": 10
            }
        )
        self._family = family_
        self.tl_family = None
        self.tag_text_families = None
        self.canvas_family = None
        self.sc_frame_family = None
        self.can_family_pointer_l = None

        self.int_values = [8, 9, 10, 11, 12, 13, 14, 15, 16, 18, 20, 22, 24, 26, 28, 36, 48, 72]
        self.size_values = list(map(str, self.int_values))
        self._size_dropdown = combo_factory(
            self,
            tv_combo=size_,
            kwargs_combo={
                "command": self._on_size,
                "justify": ctk.CENTER,
                "width": 75
            },
            values=self.size_values
        )

        # self._properties_frame = FontPropertiesFrame(self, callback=self._on_properties, label=False)
        self.colour_fg_btn_can_prop_sel = Colour("#FFFFFF")
        self.colour_bg_btn_can_prop = Colour("#949494")
        self.colour_bg_can_prop = Colour("#444444")
        self.colour_bg_btn_can_prop_sel = Colour("#1624CC")
        self._properties_frame = ctk.CTkFrame(
            self,
            bg_color=self.colour_bg_can_prop.hex_code
        )
        self.canvas_properties = ctk.CTkCanvas(
            self._properties_frame,
            width=self.can_w_pf,
            height=self.can_h_pf,
            background=self.colour_bg_can_prop.hex_code
        )

        fs = 12
        self.tags_can_prop = dict()
        self.btns_text_can_prop = [
            {"t": "B", "c": self.click_prop_weight, "v": ctk.StringVar(self, value="normal"), "f": ("Helvetica", fs, "bold")},
            {"t": "I", "c": self.click_prop_itialic, "v": ctk.StringVar(self, value="roman"), "f": ("Helvetica", fs, "italic")},
            {"t": "U", "c": self.click_prop_underline, "v": ctk.BooleanVar(self, value=False), "f": ("Helvetica", fs, "underline")},
            {"t": "O", "c": self.click_prop_overstrike, "v": ctk.BooleanVar(self, value=False), "f": ("Helvetica", fs, "overstrike")}
        ]
        gc = grid_cells(
            self.can_w_pf,
            4,
            self.can_h_pf,
            1,
            x_pad=2,
            y_pad=2,
            x_0=1,
            y_0=1
        )

        for i, row in enumerate(gc):
            for j, bbox in enumerate(row):
                command = self.btns_text_can_prop[j]["c"]
                font_ = self.btns_text_can_prop[j]["f"]
                self.tags_can_prop[(i, j)] = dict()
                self.tags_can_prop[(i, j)]["tag_rect"] = self.canvas_properties.create_rectangle(
                    bbox,
                    fill=self.colour_bg_btn_can_prop.hex_code
                )
                self.tags_can_prop[(i, j)]["tag_text"] = self.canvas_properties.create_text(
                    bbox[0] + ((bbox[2] - bbox[0]) / 2),
                    bbox[1] + ((bbox[3] - bbox[1]) / 2),
                    text=self.btns_text_can_prop[j]["t"],
                    fill=self.colour_fg_btn_can_prop_sel.hex_code,
                    font=font_
                )
                self.canvas_properties.tag_bind(
                    self.tags_can_prop[(i, j)]["tag_rect"],
                    "<Button-1>",
                    command
                )
                self.canvas_properties.tag_bind(
                    self.tags_can_prop[(i, j)]["tag_text"],
                    "<Button-1>",
                    command
                )

        self._size = size_
        self._family = family_
        self._grid_widgets()
        # print(f"NEW FontSelectFrame {self._family=}, {self._size=}")

    def _grid_widgets(self):
        """
        Puts all the widgets in the correct place.
        """
        # self._family_dropdown.grid(row=0, column=0, sticky="nswe")

        # self
        self.lbl_sample[1].grid(row=0, column=0, columnspan=3, sticky=ctk.NSEW, padx=20, pady=10)
        self.frame_family.grid(row=1, column=0, sticky=ctk.NSEW)
        self._size_dropdown[3].grid(row=1, column=1, sticky=ctk.NSEW)
        self._properties_frame.grid(row=1, column=2, sticky=ctk.NSEW)

        # frame_family
        self.entry_family[3].grid(row=0, column=0, sticky=ctk.NSEW)
        self.btn_dd_family[1].grid(row=0, column=1, sticky=ctk.NSEW)

        # _properties_frame
        self.canvas_properties.grid(row=0, column=0, sticky=ctk.NSEW)

    def _on_family(self, name):
        """
        Callback if family is changed.

        :param name: font family name
        """
        self._family = name
        self._on_change()

    def _on_size(self, size):
        """
        Callback if size is changed.

        :param size: font size int
        """
        if size not in self.size_values:
            size = "12"
        self._size = size
        self._on_change()

    def _on_change(self):
        """Call callback if any property is changed."""
        if callable(self.__callback):
            self.__callback((self._family, self._size, self._bold, self._italic, self._underline, self._overstrike))

            # print(f"_on_change {self._family=}, {self._size=}")
        self.update_sample()

    def update_sample(self):
        family = self._family
        size = int(self._size)
        weight = self.btns_text_can_prop[0]["v"].get()
        slant = self.btns_text_can_prop[1]["v"].get()
        underline = self.btns_text_can_prop[2]["v"].get()
        overstrike = self.btns_text_can_prop[3]["v"].get()
        # print(f"{family=}, {size=}, {weight=}, {slant=}, {underline=}, {overstrike=}")
        font_ = ctk.CTkFont(
            family=family,
            size=size,
            weight=weight,
            slant=slant,
            underline=underline,
            overstrike=overstrike
        )
        self.entry_family[2].set(family)
        self.lbl_sample[1].configure(
            font=font_
        )

    def __generate_font_tuple(self):
        """
        Generate a font tuple for tkinter widgets based on the user's entries.

        :return: font tuple (family_name, size, *options)
        """
        if not self._family:
            return None
        font = [self._family, self._size]
        if self._bold:
            font.append("bold")
        if self._italic:
            font.append("italic")
        if self._underline:
            font.append("underline")
        if self._overstrike:
            font.append("overstrike")
        return tuple(font)

    def click_prop_weight(self, event):
        btn_idx = 0
        is_sel = self.btns_text_can_prop[btn_idx]["v"].get() == "bold"
        self.btns_text_can_prop[btn_idx]["v"].set("normal" if is_sel else "bold")
        self._bold = self.btns_text_can_prop[btn_idx]["v"].get()
        t_rect = self.tags_can_prop[(0, btn_idx)]["tag_rect"]
        # t_text = self.tags_can_prop[(0, btn_idx)]["tag_text"]

        # now flipped
        self.canvas_properties.itemconfigure(
            t_rect,
            fill=(self.colour_bg_btn_can_prop if is_sel else self.colour_bg_btn_can_prop_sel).hex_code
        )
        # if is_sel:
        # else:
        self._on_change()

    def click_prop_itialic(self, event):
        btn_idx = 1
        is_sel = self.btns_text_can_prop[btn_idx]["v"].get() == "italic"
        self.btns_text_can_prop[btn_idx]["v"].set("roman" if is_sel else "italic")
        self._italic = self.btns_text_can_prop[btn_idx]["v"].get()
        t_rect = self.tags_can_prop[(0, btn_idx)]["tag_rect"]
        # t_text = self.tags_can_prop[(0, btn_idx)]["tag_text"]

        # now flipped
        self.canvas_properties.itemconfigure(
            t_rect,
            fill=(self.colour_bg_btn_can_prop if is_sel else self.colour_bg_btn_can_prop_sel).hex_code
        )

        self._on_change()

    def click_prop_underline(self, event):
        btn_idx = 2
        is_sel = self.btns_text_can_prop[btn_idx]["v"].get()
        self.btns_text_can_prop[btn_idx]["v"].set(not is_sel)
        self._underline = self.btns_text_can_prop[btn_idx]["v"].get()
        t_rect = self.tags_can_prop[(0, btn_idx)]["tag_rect"]
        # t_text = self.tags_can_prop[(0, btn_idx)]["tag_text"]

        # now flipped
        self.canvas_properties.itemconfigure(
            t_rect,
            fill=(self.colour_bg_btn_can_prop if is_sel else self.colour_bg_btn_can_prop_sel).hex_code
        )

        self._on_change()

    def click_prop_overstrike(self, event):
        btn_idx = 3
        is_sel = self.btns_text_can_prop[btn_idx]["v"].get()
        self.btns_text_can_prop[btn_idx]["v"].set(not is_sel)
        self._overstrike = self.btns_text_can_prop[btn_idx]["v"].get()
        t_rect = self.tags_can_prop[(0, btn_idx)]["tag_rect"]
        # t_text = self.tags_can_prop[(0, btn_idx)]["tag_text"]

        # now flipped
        self.canvas_properties.itemconfigure(
            t_rect,
            fill=(self.colour_bg_btn_can_prop if is_sel else self.colour_bg_btn_can_prop_sel).hex_code
        )

        self._on_change()

    def click_btn_dd_family(self):
        dd = self.btn_dd_family[0].get()
        if dd == "v":
            self.btn_dd_family[0].set("^")
            self.show_dd_family()

        else:
            self.btn_dd_family[0].set("v")
            if self.tl_family is not None:
                self.tl_family.destroy()
            # self.sc_frame_family.grid_forget()

    def calc_left_pointer_pos(self, center):
        c_tl = lambda pt: (pt[0] -3, pt[1] - 3)
        c_ct = lambda pt: (pt[0] -8, pt[1])
        c_br = lambda pt: (pt[0] -3, pt[1] + 3)

        return [
            (*c_tl(center), *center),
            (*c_ct(center), *center),
            (*c_br(center), *center)
        ]

    def show_dd_family(self):
        self.tl_family = ctk.CTkToplevel(self)
        self.tl_family.overrideredirect(True)
        self.tl_family.geometry(
            f"{self.can_w + 50}x{self.entry_w}+{self.winfo_rootx()}+{self.winfo_rooty() + self.winfo_height()}")

        self.sc_frame_family = ctk.CTkScrollableFrame(
            self.tl_family,
            width=self.can_w,
            height=self.entry_w
        )
        self.canvas_family = ctk.CTkCanvas(
            self.sc_frame_family,
            background=self.colour_bg_canvas.hex_code,
            width=self.can_w,
            height=self.can_h
        )

        self.can_family_pointer_l = list()
        point = (5, 10)
        points = self.calc_left_pointer_pos(point)
        for i in range(3):
            pt = points[i]
            self.can_family_pointer_l.append(
                self.canvas_family.create_line(
                    *pt,
                    fill=self.colour_line_can_family_sel.hex_code
                )
            )

        f_w, f_h = self.can_w, self.can_h / len(self.font_families)
        self.tag_text_families = list()
        # self.tag_rect_families = list()
        for i, family in enumerate(self.font_families):
            self.tag_text_families.append(
                self.canvas_family.create_text(
                    f_w / 2,
                    i * f_h,
                    text=family
                    # ,font=(family, 12)
                )
            )
            self.canvas_family.tag_bind(
                self.tag_text_families[-1],
                "<Button-1>",
                lambda event, i_=i: self.click_family(event, i_)
            )

        self.canvas_family.bind("<Motion>", self.motion_canvas_family)

        # sc_frame_family
        self.canvas_family.grid(row=0, column=0)

        # self.tl_family
        self.sc_frame_family.grid(row=0, column=0, sticky=ctk.NSEW)

        self.tl_family.grab_set()
        self.tl_family.bind("<Enter>", self.wm_enter_tl_family)
        self.tl_family.bind("<Motion>", self.motion_tl_family)
        self.tl_family.protocol("WM_DELETE_WINDOW", self.wm_close_tl_family)
        self.tl_family.focus_force()
        self.wait_window(self.tl_family)

    def motion_tl_family(self, event):
        # x, y = event.x, event.y
        # x = self.canvas_properties.canvasx(event.x)
        # y = self.canvas_properties.canvasx(event.y)
        bbox = (
            self.tl_family.winfo_rootx(),
            self.tl_family.winfo_rooty(),
            self.tl_family.winfo_rootx() + self.tl_family.winfo_width(),
            self.tl_family.winfo_rooty() + self.tl_family.winfo_height()
        )
        # x += bbox[0]
        # y += bbox[1]

        # tl: ctk.CTkToplevel = self.tl_family
        # tl.winfo_pointerx()
        x = self.tl_family.winfo_pointerx()
        y = self.tl_family.winfo_pointery()

        # print(f"({x=}, {y=}), {bbox=}")
        if not ((bbox[0] <= x <= bbox[2]) and (bbox[1] <= y <= bbox[3])):
            if self.tl_family.bind("<FocusOut>"):
                # has entered the toplevel canvas already
                # print(f"KILL")
                self.wm_close_tl_family()

    def wm_enter_tl_family(self, *args):
        # print(f"ENTER")
        self.tl_family.bind("<FocusOut>", self.wm_close_tl_family)
        self.tl_family.unbind("<Enter>")

    def wm_close_tl_family(self, *args):
        # print(f"LEAVE")
        if self.tl_family is not None:
            self.tl_family.destroy()
            self.btn_dd_family[0].set("v")

    def click_family(self, event, idx):
        family = self.font_families[idx]
        self._family = family
        self._on_change()

        if self.tl_family is not None:
            self.tl_family.destroy()
            self.btn_dd_family[0].set("v")

    def motion_canvas_family(self, event):
        x, y = event.x, event.y
        col_fg_def = self.colour_fg_canvas
        # col_bg_def = self.colour_bg_canvas
        for i, tag_t in enumerate(self.tag_text_families):
            # tag_r = self.tag_rect_families[i]
            bbox_t = self.canvas_family.bbox(tag_t)
            # bbox_r = self.canvas_family.bbox()
            col_fg = self.canvas_family.itemcget(tag_t, "fill")
            # col_bg = self.canvas_family.itemcget(tag_r, "fill")
            if not col_fg:
                col_fg = col_fg_def
            # if not col_bg:
            #     col_bg = col_bg_def
            col_fg = Colour(col_fg)
            # col_bg = Colour(col_bg)
            if (bbox_t[0] <= x <= bbox_t[2]) and (bbox_t[1] <= y <= bbox_t[3]):
                self.canvas_family.itemconfigure(
                    tag_t,
                    fill=col_fg.bluer_c(0.2).hex_code
                )
                x0 = bbox_t[0] - 20
                y0 = bbox_t[1] + ((bbox_t[3] - bbox_t[1]) / 2)
                left_positions = self.calc_left_pointer_pos((x0, y0))
                for i, pos in enumerate(left_positions):
                    # item_id = self.canvas_family.find_withtag(self.can_family_pointer_l[i])
                    # item_type = self.canvas_family.type(item_id[0])
                    # print(f"{pos=}, {item_id=}, {item_type=}")
                    self.canvas_family.coords(
                        self.can_family_pointer_l[i],
                        *pos
                    )
                # self.canvas_family.itemconfigure(
                #     tag_r,
                #     fill=col_bg.inverted().hex_code
                # )
            else:
                self.canvas_family.itemconfigure(
                    tag_t,
                    fill=col_fg_def.hex_code
                )
                # self.canvas_family.itemconfigure(
                #     tag_r,
                #     fill=col_bg_def.hex_code
                # )

    @property
    def font(self):
        """
        Font property.

        :return: a :class:`~font.Font` object if family is set, else None
        :rtype: :class:`~font.Font` or None
        """
        if not self._family:
            return None, None
        font_obj = ctk.CTkFont(family=self._family, size=self._size,
                               weight=font.BOLD if self._bold else font.NORMAL,
                               slant=font.ITALIC if self._italic else font.ROMAN,
                               underline=bool(1 if self._underline else 0),
                               overstrike=bool(1 if self._overstrike else 0)
                               )
        font_tuple = self.__generate_font_tuple()
        return font_tuple, font_obj


def demo_1():
    def select_cols():
        col = int(round(var_n_cols.get()))
        table.select_column(col)

    def select_rows():
        row = int(round(var_n_rows.get()))
        table.select_row(row)

    def update_slider_cols(col):
        v_btn_cols.set(f"Select col: {col_label(int(round(col)))}")

    def update_slider_rows(row):
        v_btn_rows.set(f"Select row: {int(round(row))}")

    win = ctk.CTk()

    n_rows, n_cols = 16, 6
    var_n_rows = tkinter.IntVar()
    var_n_cols = tkinter.IntVar()
    v_btn_rows = tkinter.StringVar(value=f"Select row: _")
    v_btn_cols = tkinter.StringVar(value=f"Select col: _")
    label_rows = ctk.CTkLabel(
        win,
        text="# Rows"
    )
    slider_rows = ctk.CTkSlider(
        win,
        from_=0,
        to=n_rows,
        variable=var_n_rows,
        command=update_slider_rows,
        number_of_steps=n_rows
    )
    btn_rows = ctk.CTkButton(
        win,
        textvariable=v_btn_rows,
        command=select_rows,
    )
    label_cols = ctk.CTkLabel(
        win,
        text="# Cols"
    )
    slider_cols = ctk.CTkSlider(
        win,
        from_=0,
        to=n_cols - 1,
        variable=var_n_cols,
        command=update_slider_cols,
        number_of_steps=n_cols - 1
    )
    btn_cols = ctk.CTkButton(
        win,
        textvariable=v_btn_cols,
        command=select_cols
    )

    table = CtkTableExt(
        win,
        values=random_table(n_rows, n_cols),
        command=callback_a
    )

    label_rows.grid(row=0, column=0, rowspan=1, columnspan=1)
    slider_rows.grid(row=1, column=0, rowspan=1, columnspan=1)
    btn_rows.grid(row=0, column=1, rowspan=2, columnspan=1)

    label_cols.grid(row=0, column=2, rowspan=1, columnspan=1)
    slider_cols.grid(row=1, column=2, rowspan=1, columnspan=1)
    btn_cols.grid(row=0, column=3, rowspan=2, columnspan=1)

    table.grid(row=2, column=0, rowspan=1, columnspan=4)
    win.mainloop()


def demo_2():
    win = ctk.CTk()

    n_rows, n_cols = 16, 6
    # var_n_rows = tkinter.IntVar()
    # var_n_cols = tkinter.IntVar()
    # v_btn_rows = tkinter.StringVar(value=f"Select row: _")
    # v_btn_cols = tkinter.StringVar(value=f"Select col: _")
    # label_rows = ctk.CTkLabel(
    #     win,
    #     text="# Rows"
    # )
    # slider_rows = ctk.CTkSlider(
    #     win,
    #     from_=0,
    #     to=n_rows,
    #     variable=var_n_rows,
    #     command=update_slider_rows,
    #     number_of_steps=n_rows
    # )
    # btn_rows = ctk.CTkButton(
    #     win,
    #     textvariable=v_btn_rows,
    #     command=select_rows,
    # )
    # label_cols = ctk.CTkLabel(
    #     win,
    #     text="# Cols"
    # )
    # slider_cols = ctk.CTkSlider(
    #     win,
    #     from_=0,
    #     to=n_cols-1,
    #     variable=var_n_cols,
    #     command=update_slider_cols,
    #     number_of_steps=n_cols-1
    # )
    # btn_cols = ctk.CTkButton(
    #     win,
    #     textvariable=v_btn_cols,
    #     command=select_cols
    # )

    table = CtkTableExt(
        win,
        table_data=random_table(n_rows, n_cols),
        width=900,
        height=700,
        kwargs_table={
            "header_color": "#680002",
            "hover_color": "#985042",
            "height": 20,
            "colors": ["#AECCFF", "#AEEEFF"],
            "text_color": ["#010203", "#030201"]

        }
    )

    # date = CtkEntryDate_2(
    #     win
    # )

    # date = Calendar(
    #     win
    # )

    date = CtkEntryDate(
        win
    )

    # label_rows.grid(row=0, column=0, rowspan=1, columnspan=1)
    # slider_rows.grid(row=1, column=0, rowspan=1, columnspan=1)
    # btn_rows.grid(row=0, column=1, rowspan=2, columnspan=1)
    #
    # label_cols.grid(row=0, column=2, rowspan=1, columnspan=1)
    # slider_cols.grid(row=1, column=2, rowspan=1, columnspan=1)
    # btn_cols.grid(row=0, column=3, rowspan=2, columnspan=1)

    table.grid(row=0, column=0, rowspan=1, columnspan=4)
    date.grid(row=1, column=0, rowspan=1, columnspan=4)
    win.mainloop()


def demo_3():
    win = ctk.CTk()
    win.geometry(calc_geometry_tl(1.0, 1.0, largest=0))  # , parent=win, ask=True))
    win.title("CalendarCanvas Demo")

    colour_scheme_keys = {
        "colour_background_canvas": lambda c: c,
        "colour_background_owned_number_check": lambda c: c.brightened(0.25),
        "colour_background_header_month": lambda c: c.darkened(0.2),
        "colour_background_header_weekday": lambda c: c.darkened(0.1),
        "colour_background_canvas_selected": lambda c: c.inverted().brightened(0.25, safe=True),
        "colour_outline": lambda c: c.inverted().darkened(0.25, safe=True)
    }
    month_colours = {
        0: Colour("#1E90FF"),  # January
        1: Colour("#FF69B4"),  # February
        2: Colour("#32CD32"),  # March
        3: Colour("#FFD700"),  # April
        4: Colour("#ADFF2F"),  # May
        5: Colour("#FF4500"),  # June
        6: Colour("#FF6347"),  # July
        7: Colour("#FFDAB9"),  # August
        8: Colour("#6A5ACD"),  # September
        9: Colour("#FF8C00"),  # October
        10: Colour("#A52A2A"),  # November
        11: Colour("#2E8B57")  # December
    }
    month_colours = {
        0: Colour("#4682B4"),  # January - Steel Blue
        1: Colour("#5F9EA0"),  # February - Cadet Blue
        # 2: Colour("#66CDAA"),  # March - Medium Aquamarine
        2: Colour("#000000"),  # March - Medium Aquamarine
        # 3: Colour("#8FBC8F"),  # April - Dark Sea Green
        3: Colour("#000000"),  # March - Medium Aquamarine
        # 4: Colour("#98FB98"),  # May - Pale Green
        5: Colour("#FFD700"),  # June - Gold
        # 6: Colour("#FFA500"),  # July - Orange
        7: Colour("#FF7F50"),
        # ,  # August - Coral
        8: Colour("#FF6347"),  # September - Tomato
        # 9: Colour("#FF4500"),  # October - Orange Red
        10: Colour("#CD5C5C"),  # November - Indian Red
        11: Colour("#B0C4DE")  # December - Light Steel Blue
    }

    colour_scheme_months = {
        m_idx: {
            k: func(col)
            for k, func in colour_scheme_keys.items()
        }
        for m_idx, col in month_colours.items()
    }

    colour_scheme_day = {
        (12, 25): {
            "name": "Christmas",
            "colour_background_canvas": Colour("#A60824"),
            "colour_foreground_canvas": Colour("#085624"),
            "colour_ground_canvas_selected": Colour("#A99511"),
            "colour_foreground_canvas_selected": Colour("#0000A1")
        }
    }

    print(f"colour_scheme_months=", end="")
    vals = {i: {k: f"Colour('#{c.hex_code}')" for k, c in d.items()} for i, d in colour_scheme_months.items()}
    print(f"{vals}")
    print(f"{colour_scheme_months=}")
    print(f"{colour_scheme_day=}")

    # colour_scheme_months[0]["colour_background_canvas"] = Colour("#319141")
    colour_scheme_months[3]["colour_foreground_canvas"] = Colour("#319141")
    colour_scheme_months[3]["colour_outline"] = Colour("#FFD700")

    frame = ctk.CTkFrame(win)
    calendar = CalendarCanvas2(
        frame
        # , year=None
        # ,show_weekdays=False
        , months_per_row=3
        , colour_scheme_month=colour_scheme_months
        , hover_style="brighten"
        , invalid_style="darken"
        , show_all_rows=True
        , selectable=True
        , colour_scheme_day=colour_scheme_day
    )

    frame.grid(row=0, column=0, rowspan=1, columnspan=1, sticky=ctk.NSEW)
    calendar.grid(row=0, column=0, rowspan=1, columnspan=1, sticky=ctk.NSEW)

    # calendar.disable_date(datetime.datetime(2024, 12, 25))  # holiday
    # calendar.disable_date(datetime.datetime(2024, 1, 25))
    calendar.disable_day(1, 25)

    def random_date(year_range=(1995, datetime.datetime.now().year), month_range=(1, 12), day_range=(1, 31)):
        l_year, t_year = year_range
        l_month, t_month = month_range
        l_day, t_day = day_range

        rdate = None

        while rdate is None:
            ry = random.randint(l_year, t_year)
            rm = random.randint(l_month, t_month)
            rd = random.randint(l_day, t_day)
            try:
                rdate = datetime.datetime(ry, rm, rd)
            except ValueError:
                rdate = None

        return rdate

    random_disabled_dates = set()
    while len(random_disabled_dates) < 10:
        random_disabled_dates.add(random_date())

    for date in random_disabled_dates:
        calendar.disable_day(date.month, date.day)

    # win.after(2500, lambda: calendar.select_day(datetime.datetime.now()))
    # win.after(8500, lambda: calendar.deselect_day())

    win.mainloop()


def demo_4():
    win = ctk.CTk()
    win.geometry(f"600x350")
    start_colour = "#560000"
    can = ctk.CTkCanvas(win, width=100, height=100, bg=start_colour)
    btn = ctk.CTkButton(win, text="brighten 12%",
                        command=lambda: can.configure(bg=Colour(can.cget("bg")).brightened(0.12, safe=True).hex_code))
    can.pack()
    btn.pack()
    win.mainloop()


def demo_5():
    win = ctk.CTk()
    win.geometry(f"600x350")

    ff = FontSelectFrame(win)
    ff.pack()

    btn_gf = button_factory(
        win,
        tv_btn="get_tuple",
        command=lambda: print(f"{ff.font=}")
    )

    btn_gf[1].pack()
    win.mainloop()


def demo_6():
    win = ctk.CTk()
    win.geometry(f"600x500")

    ps = PrioritySelection(
        win,
        # values=["A", "B", "C"],
        values=list(range(10)),
        orientation="horizontal"
    )

    # win
    ps.pack()

    win.mainloop()


if __name__ == '__main__':
    # demo_1()
    # demo_2()
    # demo_3()
    # demo_4()
    # demo_5()
    demo_6()

import functools
import random
import tkinter
from copy import deepcopy
from typing import List, Any
import calendar

import datetime
import customtkinter as ctk
from CTkTable import CTkTable
from tkcalendar import Calendar

from datetime_utility import is_date
from colour_utility import Colour, iscolour
from tkinter_utility import calc_geometry_tl
from utility import grid_cells, clamp

#######################################################################################################################
#######################################################################################################################
#######################################################################################################################

VERSION = \
    """	
    General Utility Functions
    ans class for customtkinter
    Version................1.03
    Date.............2024-07-03
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

        # self.var_entry = tkinter.StringVar(self, value="")
        self.entry = ctk.CTkEntry(
            self,
            textvariable=self.var_date_picker,
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
        print(f"submit_entry v={self.var_entry.get()}")
        val = self.var_entry.get()
        if is_date(val):

            # date = self.date_picker.parse_date(val)
            # self.date_picker.date = date
            val = is_date(val)
            print(f"A: {val}")
            val = self.date_picker.format_date(val)
            print(f"B: {val}")
            self.date_picker.selection_set(val)

    def update_selected_date(self, *args):
        date = self.var_date_picker.get()
        print(f"update_selected_date v={date}")
        fmt = "%x"
        for fmt in (
            "%x",
            "%Y-%m-%d"
        ):
            try:
                self.date = datetime.datetime.strptime(date, fmt)
            except ValueError:
                pass
            else:
                break

        print(f"New Date! {self.date:%Y-%m-%d}")
        self.var_entry.set(f"{self.date:{fmt}}")


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


class CalendarCanvas(ctk.CTkCanvas):
    def __init__(
            self,
            master,
            year: int | None = datetime.datetime.now().year,
            show_weekdays: bool = True,
            months_per_row: int = 4,
            width: int = 600,
            height: int = 700,
            colour_background_canvas: Colour = Colour("#AEBEBE"),
            colour_background_owned_number_check: Colour = Colour("#2A4AFA"),
            colour_background_owned_number_check_heat_map: Colour = Colour("#FA2A4A"),
            colour_background_header_year: Colour = Colour("#627272"),
            colour_background_header_month: Colour = Colour("#7B8B8B"),
            colour_background_header_weekday: Colour = Colour("#94A4A4"),
            colour_scheme_month: dict[int: Colour] = None,
            *args, **kwargs
    ):
        super().__init__(master=master, *args, **kwargs)

        self.year = year
        self.show_weekdays = show_weekdays
        self.months_per_row = clamp(3, months_per_row, 4)
        self.weeks_per_month = 6 + 1  # for the month label
        self.weeks_per_month += (1 if self.show_weekdays else 0)  # offset for weekday labels
        self.n_rows: int = (self.weeks_per_month * (12 // self.months_per_row)) + 1
        self.n_cols: int = 7 * self.months_per_row
        self.w_canvas: int = width
        self.h_canvas: int = height
        self.colour_background_canvas = colour_background_canvas
        self.colour_background_owned_number_check = colour_background_owned_number_check
        self.colour_background_owned_number_check_heat_map = colour_background_owned_number_check_heat_map
        self.colour_background_header_year = colour_background_header_year
        self.colour_background_header_month = colour_background_header_month
        self.colour_background_header_weekday = colour_background_header_weekday
        self.colour_scheme_month: dict[int: Colour] = self.validate_colour_scheme(colour_scheme_month) if colour_scheme_month is not None else dict()
        self.configure(
            width=self.w_canvas,
            height=self.h_canvas,
            background=self.colour_background_canvas.hex_code
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
        self.dict_canvas_tags = dict()

        for i, row in enumerate(self.gc):
            for j, coords in enumerate(row):
                n = ((i * self.n_cols) + j) + 1
                # if n == 100:
                #     # no #100
                #     break
                x0, y0, x1, y1 = coords
                col = self.colour_background_canvas
                if j // 7 == 2:
                    col.darkened(0.24)
                elif j // 7 == 1:
                    col.darkened(0.12)
                tr = self.create_rectangle(
                    x0, y0, x1, y1, fill=col.hex_code
                )
                tt = self.create_text(
                    x0 + ((x1 - x0) / 2), y0 + ((y1 - y0) / 2),
                    fill=col.font_foreground(rgb=False),
                    text=f"{n}"
                )
                self.tag_bind(
                    tt,
                    "<Button-1>",
                    lambda event, i_=i, j_=j: self.click_canvas(event, i_, j_)
                )
                self.tag_bind(
                    tr,
                    "<Button-1>",
                    lambda event, i_=i, j_=j: self.click_canvas(event, i_, j_)
                )
                self.dict_canvas_tags[(i, j)] = {
                    "rect": tr,
                    "text": tt
                }

        self.dict_canvas_tags["header_year"] = {"rect": None, "text": None}
        self.dict_canvas_tags["header_month"] = {"rect": None, "text": None}
        self.dict_canvas_tags["header_weekday"] = {"rect": None, "text": None}

        if self.year is not None:
            # hide top row cells
            # for j in range(self.n_cols):
            #     for tag_name in ("rect", "text"):
            #         self.itemconfigure(
            #             self.dict_canvas_tags[(0, j)][tag_name],
            #             state="hidden"
            #         )

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
                    fill=self.colour_background_header_year.hex_code
                ),
                "text": self.create_text(
                    bbox_year[0] + (w / 2),
                    bbox_year[1] + (h / 2),
                    text=f"{self.year}",
                    fill=self.colour_background_header_year.font_foreground(rgb=False)
                )
            })

        # blank month row
        ri = 1 if self.year is not None else 0
        # for j in range(self.n_cols):
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
            self.dict_canvas_tags[f"header_month"].append({
                "rect": self.create_rectangle(
                    *bbox_month,
                    fill=self.colour_background_header_month.hex_code
                ),
                "text": self.create_text(
                    bbox_month[0] + (w / 2),
                    bbox_month[1] + (h / 2),
                    text=f"{month_name}",
                    fill=self.colour_background_header_month.font_foreground(rgb=False)
                ),
                "weekdays": list()
            })
            print(f"{month_name[:3].upper()}: {bbox_month=}")

            if self.show_weekdays:
                ri0 += 1
                for k in range(self.n_cols):
                    self.itemconfigure(
                        self.dict_canvas_tags[(ri0, k)]["rect"],
                        fill=self.colour_background_header_weekday.hex_code
                    )
        # print(f"{self.dict_canvas_tags['header_month']=}")

        self.calc_days()

    def validate_colour_scheme(self, colour_scheme_month) -> dict[int: Colour]:
        if not isinstance(colour_scheme_month, dict):
            raise ValueError(f"Param 'colour_scheme_month' must be an instance of a dictionary. Got '{type(colour_scheme_month)}'")

        valid_style_keys = {
            "colour_background_canvas": iscolour,
            "colour_background_owned_number_check": iscolour,
            "colour_background_owned_number_check_heat_map": iscolour,
            "colour_background_header_year": iscolour,
            "colour_background_header_month": iscolour,
            "colour_background_header_weekday": iscolour
        }

        result = {}

        for k, scheme_data in colour_scheme_month:
            if not isinstance(k, int):
                raise ValueError(f"Param 'colour_scheme_month' must only have integer key. Got '{k}'")
            if not (0 < k < 12):
                raise ValueError(f"Param 'colour_scheme_month' must only have integer keys between 0 and 11. Got '{k}'")
            if not isinstance(scheme_data, dict):
                raise ValueError(f"Param 'scheme_data' must be an instance of a dict. Got '{scheme_data}'")
            result[k] = dict()
            for k_style, v in scheme_data.items():
                if k_style not in valid_style_keys:
                    raise ValueError(f"Style key '{k_style}' is not recognized. Must be an one of: {', '.join(valid_style_keys)}")
                try:
                    col = Colour(v)
                except Colour.ColourCreationError:
                    raise ValueError(f"Param 'colour_scheme_month' must only have Colour objects or equivalent as values. Got '{k}'")
                result[k][k_style] = col

        return result

    def calc_days(self):
        ri = 2 if self.year is not None else 1
        if self.year is not None:
            # for i, data in enumerate(self.dict_canvas_tags["header_month"]):

            for cal_i in range(12):
                day_one = datetime.datetime(self.year, cal_i + 1, 1)
                wd_d1 = day_one.isoweekday() % 7
                j = cal_i // self.months_per_row
                for wk_i in range(self.weeks_per_month - 1):
                    used_row = False
                    ri0 = ri + (j * self.weeks_per_month) + wk_i
                    for wkd_i in range(7):
                        str_day = f"{day_one.day}"
                        ci0 = ((cal_i % self.months_per_row) * 7) + wkd_i
                        print(f"{day_one:%Y-%m-%d}, {cal_i=}, {j=}, {ri0=}, {ci0=}, {wk_i=}, {wkd_i=}, {wd_d1=}", end="")
                        month_name = calendar.month_name[cal_i + 1]
                        tag_txt = self.dict_canvas_tags[(ri0, ci0)]["text"]
                        tag_rect = self.dict_canvas_tags[(ri0, ci0)]["rect"]
                        if self.show_weekdays and (wk_i == 0):
                            self.dict_canvas_tags["header_month"][cal_i]["weekdays"].append({
                                "rect": tag_rect,
                                "text": tag_txt
                            })
                            self.itemconfigure(tag_txt, text=f"{calendar.day_abbr[(wkd_i - 1) % 7]}"[0])
                            used_row = True
                            continue
                        if cal_i != (day_one.month - 1):
                            self.itemconfigure(tag_txt, state="hidden")
                            # day_one += datetime.timedelta(days=1)
                            print(f" -A")
                            continue
                        if ((wk_i - (1 if self.show_weekdays else 0)) == 0) and (wd_d1 > 0):
                            wd_d1 -= 1
                            # day_one += datetime.timedelta(days=1)
                            self.itemconfigure(tag_txt, state="hidden")
                            print(f" -B")
                            continue

                        self.itemconfigure(tag_txt, text=str_day)
                        txt = self.itemcget(tag_txt, "text")
                        day_one += datetime.timedelta(days=1)
                        used_row = True

                        # bbox_month = (
                        #     *self.gc[ri0][ci0][:2],
                        #     *self.gc[ri0][ci0 + 7 - 1][-2:]
                        # )
                        # tag_txt = self.dict_canvas_tags["header_month"][cal_i]["text"]
                        # txt = self.itemcget(tag_txt, "text")
                        print(f" {txt=}")

                    if not used_row:
                        for k in range(7):
                            self.itemconfigure(
                                self.dict_canvas_tags[(ri0, ((cal_i % self.months_per_row) * 7) + k)]["rect"],
                                state="hidden"
                            )



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
        print(f"click_canvas {i=}, {j=}, {event=}")
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
        # df = self.ctk_.df.loc[(self.ctk_.df["DOB"].dt.month == n.month) & (self.ctk_.df["DOB"].dt.day == n.day)]
        # df = df.sort_values(by=["Team", "PlayerLast", "PlayerFirst"])
        # text = ""
        # for k, row in df.iterrows():
        #     # text += f"{row['Team'].center(22)} - {row['PlayerFirst'].rjust(11)} {row['PlayerLast'].ljust(18)}\n"
        #     text += f"{row['Team'].center(22)} - {row['PlayerLast']}, {row['PlayerFirst']}\n"
        # if df.shape[0] == 0:
        #     text = "No Data"
        # self.tb_canvas_click_data.insert("0.0", text)


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
    win.geometry(calc_geometry_tl(1.0, 1.0, parent=win, ask=True))
    win.title("CalendarCanvas Demo")

    frame = ctk.CTkFrame(win)
    calendar = CalendarCanvas(
        frame
        # , year=None
        ,show_weekdays=False
    )

    frame.grid(row=0, column=0, rowspan=1, columnspan=1, sticky=ctk.NSEW)
    calendar.grid(row=0, column=0, rowspan=1, columnspan=1, sticky=ctk.NSEW)

    win.mainloop()


if __name__ == '__main__':
    # demo_1()
    # demo_2()
    demo_3()

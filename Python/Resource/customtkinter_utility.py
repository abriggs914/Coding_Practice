import functools
import random
import tkinter
from copy import deepcopy
from typing import List, Any, Literal, Optional
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
    Version................1.04
    Date.............2024-07-11
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
            colour_scheme_month: dict[int: Colour] = None,
            colour_scheme_day: dict[tuple[int, int]: Colour] = None,
            hover_style: Literal[None, "darken", "brighten"] = "brighten",
            invalid_style: Literal[None, "darken", "brighten", "invisible"] = None,
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
        self.colour_scheme_month: dict[int: Colour] = self.validate_colour_scheme(colour_scheme_month) if colour_scheme_month is not None else dict()
        # self.colour_scheme_day: dict[tuple[int, int]: Colour] = self.validate_colour_scheme(colour_scheme_day) if colour_scheme_day is not None else dict()
        self.colour_scheme_day: dict[tuple[int, int]: Colour] = colour_scheme_day if colour_scheme_day is not None else dict()
        self.hover_style = hover_style
        self.invalid_style = invalid_style
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
                col_wd = self.get_colour("colour_background_canvas", i, j, do_show=(cal_idx == 2))
                col_wd_txt = self.get_colour("colour_foreground_canvas", i, j, do_show=(cal_idx == 2))
                # print(f"{i=}, {j=}, {cal_idx=}, {p_a=}, {p_ba=}, {p_bb=}, col_wd={col_wd.hex_code}, col_wd_txt={col_wd_txt.hex_code}, {cs=}")
                tr = self.create_rectangle(
                    x0, y0, x1, y1, fill=col_wd.hex_code
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
                        self.tag_bind(tr, "<Motion>", lambda event, i_=i, j_=j, t_=tag: self.motion_cell(event, i_, j_, t_))

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
                raise ValueError(f"Param 'day_in' must be between 1 and {self.max_days_per_month[m_idx]}, since you supplied 'month_idx'={m_idx + 1}, the maximum number of days can only be {self.max_days_per_month[m_idx]} for {calendar.month_name[m_idx + 1]}.")

        else:
            m_idx, d_idx = month_in - 1, day_in
        if self.year is None:
            i, j = self.date_to_cell[(m_idx, d_idx)]
        else:
            date_in = datetime.datetime(self.year, month_in, day_in)
            i, j = self.date_to_cell[date_in]

        print(f"DD -> {i=}, {j=}")

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
            raise ValueError(f"Please use CalendarCanvas.disable_day when disabling a cell on a calendar with no specified year.")

        d1 = datetime.datetime(self.year, 1, 1)
        d2 = datetime.datetime(self.year, 12, 31, 23, 59, 59, 999999)
        if not (d1 <= date_in <= d2):
            raise ValueError(f"Param 'date_in' must be between {d1:%Y-%m-%d} and {d2:%Y-%m-%d} at end of day. Got {date_in:%x}")

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
                raise ValueError(f"Param 'day_in' must be between 1 and {self.max_days_per_month[m_idx]}, since you supplied 'month_idx'={m_idx + 1}, the maximum number of days can only be {self.max_days_per_month[m_idx]} for {calendar.month_name[m_idx + 1]}.")

        else:
            m_idx, d_idx = month_in, day_in
        i, j = self.date_to_cell[(m_idx, d_idx)]
        self.click_canvas(None, i, j)

    def select_date(self, date_in: datetime.datetime):
        if self.year is None:
            raise ValueError(f"Please use CalendarCanvas.select_day when selecting a cell on a calendar with no specified year.")

        d1 = datetime.datetime(self.year, 1, 1)
        d2 = datetime.datetime(self.year, 12, 31, 23, 59, 59, 999999)
        if not (d1 <= date_in <= d2):
            raise ValueError(f"Param 'date_in' must be between {d1:%Y-%m-%d} and {d2:%Y-%m-%d} at end of day. Got {date_in:%x}")

        i, j = self.date_to_cell[date_in]

        self.click_canvas(None, i, j)

    def validate_colour_scheme(self, colour_scheme_month) -> dict[int: Colour]:
        if not isinstance(colour_scheme_month, dict):
            raise ValueError(f"Param 'colour_scheme_month' must be an instance of a dictionary. Got '{type(colour_scheme_month)}'")

        valid_style_keys = {
            "colour_background_canvas": iscolour,
            "colour_background_owned_number_check": iscolour,
            "colour_background_header_month": iscolour,
            "colour_background_header_weekday": iscolour,

            "colour_foreground_canvas": iscolour,
            "colour_foreground_header_month": iscolour,

            "colour_background_canvas_selected": iscolour,
            "colour_foreground_canvas_selected": iscolour
        }

        result = {}

        for k, scheme_data in colour_scheme_month.items():
            if not isinstance(k, int):
                raise ValueError(f"Param 'colour_scheme_month' must only have integer key. Got '{k}'")
            if not (0 <= k < 12):
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
                                fill=self.get_colour("colour_background_header_weekday", ri0, ci0, do_show=((0 < ri0 < 20) and (15 < ci0 < 50))).hex_code
                            )
                            self.itemconfigure(
                                tag_txt,
                                text=f"{calendar.day_abbr[(wkd_i - 1) % 7]}"[0],
                                # fill=s.get("colour_foreground_header_weekday", self.colour_background_header_weekday.font_foreground_c()).hex_code
                                fill=self.get_colour("colour_foreground_header_weekday", ri0, ci0, do_show=((0 < ri0 < 20) and (15 < ci0 < 50))).hex_code
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

        is_ = self.invalid_style
        hs = self.hover_style

        bg = self.colour_background_canvas
        fg = self.colour_foreground_canvas

        dc = self.disabled_cells
        dtc = self.set_date_cells
        c_code = f""

        if (i is not None) and (j is not None):
            c_code += "a"
            val = None
            pos = i, j
            cal_idx = self.dict_cell_to_cal_idx[pos]
            is_invalid_cell = pos not in self.set_date_cells

            midx, didx = None, None
            if (not is_invalid_cell) and self.finished_init and self.finished_calc:
                c_code += "b"
                date_in = self.cell_to_date[pos]
                midx, didx = date_in.month - 1, date_in.day

            if (midx, didx) in ds:
                c_code += "c"
                val = ds[(midx, didx)].get(key)
            if not val:
                c_code += "d"
                if cal_idx in ms:
                    c_code += "e"
                    val = ms[cal_idx].get(key)
            if not val:
                c_code += "f"
                if key != key_n:
                    if (midx, didx) in ds:
                        c_code += "g"
                        val = ds[(midx, didx)].get(key_n)
                    if not val:
                        c_code += "h"
                        if cal_idx in ms:
                            c_code += "i"
                            val = ms[cal_idx].get(key_n)
                if not val:
                    c_code += "j"
                    try:
                        c_code += "k"
                        val = self.__getattribute__(key)
                    except AttributeError:
                        c_code += "l"
                        val = fg if ("_foreground" in key) else bg

            if is_invalid_cell:
                c_code += "m"
                if pos not in self.dict_canvas_tags[f"header_month_weekday"][cal_idx]:
                    c_code += "n"
                    print(f"invalid")
                    if is_:
                        c_code += "o"
                        val = val.darkened(0.25) if (is_ == "darken") else (
                            val.brightened(0.25) if (is_ == "brighten") else val)

            elif pos in dc:
                c_code += "p"
                print(f"disabled")

            elif pos == selected:
                c_code += "q"
                print(f"selected")

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
                val = self.__getattribute__(key)
            except AttributeError:
                c_code += "v"
                val = fg if ("_foreground" in key) else bg

        print(f"CC={c_code.ljust(15)}, C='{val.hex_code}', ij=({i}, {j}), {key=}")
        return val


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
                raise ValueError(f"Key '{key}' is not recognized as a valid colour key.")

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
                # print(f"{key=}, {key_b=}, {key_n=}")
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
            print(f" {year=}, month={cal_idx+1}, day={int(text)}")
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
        # df = self.ctk_.df.loc[(self.ctk_.df["DOB"].dt.month == n.month) & (self.ctk_.df["DOB"].dt.day == n.day)]
        # df = df.sort_values(by=["Team", "PlayerLast", "PlayerFirst"])
        # text = ""
        # for k, row in df.iterrows():
        #     # text += f"{row['Team'].center(22)} - {row['PlayerFirst'].rjust(11)} {row['PlayerLast'].ljust(18)}\n"
        #     text += f"{row['Team'].center(22)} - {row['PlayerLast']}, {row['PlayerFirst']}\n"
        # if df.shape[0] == 0:
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
        print(f"ij=({i}, {j}), lh={last_hover}, sl={selected} tlh={type(last_hover)}, tsl{type(selected)}, {is_=}, {hs=}")

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
    win.geometry(calc_geometry_tl(1.0, 1.0, largest=1))  # , parent=win, ask=True))
    win.title("CalendarCanvas Demo")

    colour_scheme_keys = {
        "colour_background_canvas": lambda c: c,
        "colour_background_owned_number_check": lambda c: c.brightened(0.25),
        "colour_background_header_month": lambda c: c.darkened(0.2),
        "colour_background_header_weekday": lambda c: c.darkened(0.1),
        "colour_background_canvas_selected": lambda c: c.inverted().brightened(0.25, safe=True)
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

    frame = ctk.CTkFrame(win)
    calendar = CalendarCanvas2(
        frame
        # , year=None
        # ,show_weekdays=False
        ,months_per_row=3
        ,colour_scheme_month=colour_scheme_months
        ,hover_style="brighten"
        ,invalid_style="darken"
        ,show_all_rows=True
        ,selectable=True
        ,colour_scheme_day=colour_scheme_day
    )

    frame.grid(row=0, column=0, rowspan=1, columnspan=1, sticky=ctk.NSEW)
    calendar.grid(row=0, column=0, rowspan=1, columnspan=1, sticky=ctk.NSEW)

    # calendar.disable_date(datetime.datetime(2024, 12, 25))  # holiday
    # calendar.disable_date(datetime.datetime(2024, 1, 25))
    calendar.disable_day(1, 25)
    # win.after(2500, lambda: calendar.select_day(datetime.datetime.now()))
    # win.after(8500, lambda: calendar.deselect_day())

    win.mainloop()


if __name__ == '__main__':
    # demo_1()
    # demo_2()
    demo_3()

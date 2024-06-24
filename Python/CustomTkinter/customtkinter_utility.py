import functools
import random
import tkinter
from typing import List

import customtkinter as ctk
from CTkTable import CTkTable


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
            self.og_values = [[v for v in row] for row in self.values[1:]]
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
            s_values = [[v for v in r] for r in self.og_values]
        else:
            s_values = [[v for v in r] for r in self.history_sorts.get((col, rev), [[]])]
            if (len(s_values) == 1) and (len(s_values[0]) == 0):
                s_values = sorted(
                    self.values[1:],
                    key=lambda r: r[col],
                    reverse=rev
                )
                self.history_sorts[(col, rev)] = [[v for v in r] for r in s_values]

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
            except IndexError:
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
        self.table.clear_selected_cols()
        self.table.clear_selected_rows()
        # i, j = None, None
        f_idxs = []
        for i, row in enumerate(self.table.values[1:]):
            for j, val in enumerate(row):
                if str(val).lower() == str(value).lower():
                    f_idxs.append((i + 1, j))
                else:
                    self.table.deselect(i + 1, j)

        self.var_text_lbl_num.set("1")
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
    return [[col_label(i) for i in range(cols)]] + [[random.randint(low, high) for j in range(cols)] for i in range(rows)]


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


def demo_1():
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


if __name__ == '__main__':

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

    # label_rows.grid(row=0, column=0, rowspan=1, columnspan=1)
    # slider_rows.grid(row=1, column=0, rowspan=1, columnspan=1)
    # btn_rows.grid(row=0, column=1, rowspan=2, columnspan=1)
    #
    # label_cols.grid(row=0, column=2, rowspan=1, columnspan=1)
    # slider_cols.grid(row=1, column=2, rowspan=1, columnspan=1)
    # btn_cols.grid(row=0, column=3, rowspan=2, columnspan=1)

    table.grid(row=2, column=0, rowspan=1, columnspan=4)
    win.mainloop()

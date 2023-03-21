import tkinter

import pandas as pd

from pyodbc_connection import *
from tkinter_utility import *
from utility import *
from colour_utility import *
import matplotlib.pyplot as plt
import numpy as np
# from main import series_list

from tkinter import *
from dataframe_utility import *
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
NavigationToolbar2Tk)



def grid_keys():
    return "row", "column", "rowspan", "columnspan", "ipadx", "ipady", "padx", "pady", "sticky"

#
# def gen_data(field=None, op_args=0):
#     if field:
#         field_pt = field
#         data_points = []
#         name_points = []
#         for s in series_list:
#             value_retrieved = getattr(s, field_pt)
#             if isclassmethod(value_retrieved):
#                 value_retrieved = value_retrieved()
#             data_points.append(value_retrieved)
#             name_points.append(s.name)
#
#         match field:
#             case "how_long_is_series":
#                 data_points = [dp[op_args] for dp in data_points]
#             case _:
#                 print("pass on format")
#         print(f"\t{data_points=}")
#
#         return data_points, name_points
#
#
# def show_graph(
#         data_in,
#         mode="alpha",
#         reverse=False,
#         title="Shows by length in minutes",
#         xlabel="time (mins)",
#         orientation="horizontal"
# ):
#     # plt.hist(*data_in)
#     # plt.show()
#
#     data_points, show_names = data_in
#
#     plt.rcdefaults()
#     fig, ax = plt.subplots()
#
#     # alpha
#     if mode == "alpha":
#         show_names, data_points = [list(x) for x in zip(*sorted(zip(show_names, data_points), key=itemgetter(0), reverse=reverse))]
#     elif mode == "value":
#         data_points, show_names = [list(x) for x in zip(*sorted(zip(data_points, show_names), key=itemgetter(0), reverse=reverse))]
#     # data_points, show_names = [list(x) for x in zip(*sorted(zip(data_points, show_names), key=itemgetter(0)))]
#
#     y_pos = np.arange(len(show_names))
#     if orientation == "horizontal":
#         ax.barh(y_pos, data_points, align="center")
#         ax.set_yticks(y_pos, labels=show_names)
#         ax.invert_yaxis()
#         ax.set_xlabel(xlabel)
#         ax.set_title(title)
#     else:
#         ax.bar(y_pos, data_points, align="center")
#         ax.set_xticks(y_pos, labels=show_names)
#         ax.tick_params(axis="x", rotation=90)
#         ax.invert_xaxis()
#         ax.set_ylabel(xlabel)
#         ax.set_title(title)
#
#     plot(fig)
#
#     # swap(plot)
#
#     # plt.show()
#     # plot()
#
#
# def plot_g_1():
#     data_series_by_minutes = gen_data("how_long_is_series")
#     print(data_series_by_minutes)
#     show_graph(
#         data_series_by_minutes,
#         mode="value" if tv_sort_style.get() == "by value" else "alpha",
#         reverse=tv_sort_direction.get() == "descending",
#         title="Shows by length in minutes",
#         xlabel="time (mins)",
#         orientation=tv_orientation.get()
#     )
#
#
# def swap(*line_list):
#     """
#     Example
#     -------
#     line = plot(linspace(0, 2, 10), rand(10))
#     swap(line)
#     """
#     for lines in line_list:
#         try:
#             iter(lines)
#         except:
#             lines = [lines]
#
#         for line in lines:
#             xdata, ydata = line.get_xdata(), line.get_ydata()
#             line.set_xdata(ydata)
#             line.set_ydata(xdata)
#             line.axes.autoscale_view()


class PlotFrame(tkinter.Frame):

    def __init__(
            self,
            master,
            df,
            viewable_column_names=None,
            aggregate_data=None,
            auto_grid=None,
            btns_per_row=5,
            btns_horizontal=True,
            max_chart_elements=2,
            max_plottable_categories=50,
            *args,
            **kwargs
    ):
        super().__init__(master, *args, **kwargs)

        assert isinstance(df, pd.DataFrame), f"Error param 'df' must be aa pandas.DataFrame object. Got {type(df)}"

        self.df = df
        self.viewable_column_names = viewable_column_names
        self.can_plot = tkinter.BooleanVar(self, value=False)
        self.auto_grid = auto_grid
        self.btns_per_row = btns_per_row
        self.btns_horizontal = btns_horizontal
        self.max_chart_elements = max_chart_elements
        self.treeview_controller = treeview_factory(
            self, df_IT_requests
            , viewable_column_names=viewable_column_names
            , aggregate_data=aggregate_data
        )
        self.frame_treeview_controller, \
            self.tv_label_treeview_controller, \
            self.label_treeview_controller, \
            self.treeview_treeview_controller, \
            self.scrollbar_x_treeview_controller, \
            self.scrollbar_y_treeview_controller, \
            (self.tv_button_new_item_treeview_controller, self.button_new_item_treeview_controller), \
            (self.tv_button_delete_item_treeview_controller, self.button_delete_item_treeview_controller), \
            self.aggregate_objects_treeview_controller \
            = self.treeview_controller.get_objects()

        self.max_plottable_categories = max_plottable_categories
        self.col_data = {}
        col_data_keys = [
            # "plottable",
            "is_numeric",
            "is_date",
            "count_unique",
            "max_len"
        ]
        col_data_lambdas = [
            # lambda k: (self.df[k].nunique() < self.max_plottable_categories) or is_date_dtype(self.df, k) or is_numeric_dtype(self.df, k),
            lambda k: is_numeric_dtype(self.df, k),
            lambda k: is_date_dtype(self.df, k),
            lambda k: self.df[k].nunique(),
            lambda k: self.df[k].astype(str).str.len().max()
        ]
        for k in self.viewable_column_names:
            print(f"{k=}, dtype: {self.df.dtypes[k]}")
            # self.col_data[k] = dict(zip(col_data_keys, map(lambda f, x: col_data_keys, col_data_lambdas)))
            self.col_data[k] = dict(zip(col_data_keys, map(lambda f, x: f(k), col_data_lambdas, col_data_keys)))
            self.col_data[k].update({
                "plottable": (self.col_data[k]["count_unique"] < self.max_plottable_categories) or self.col_data[k]["is_numeric"] or self.col_data[k]["is_date"]
            })

        print(f"{self.col_data}")
        print(f"{dict_print(self.col_data, 'Col_data')}")

        ag_x, ag_y = 0, 0
        if isinstance(auto_grid, list) or isinstance(auto_grid, tuple):
            if len(auto_grid) == 2:
                ag_x, ag_y = auto_grid
            else:
                raise ValueError(f"Error, auto_grid param is not the right dimensions.")
        elif isinstance(auto_grid, int):
            ag_x, ag_y = 0, auto_grid
        if ag_x < 0 or ag_y < 0:
            raise ValueError(f"Error, auto_grid param is invalid.")

        r, c, rs, cs, ix, iy, x, y, s = grid_keys()
        self.grid_args = {

            # self
            ".": {r: ag_y, c: ag_x},
            "label_treeview_controller": {r: 0},
            "frame_treeview_controller": {r: 1, c: 0},
            "frame_btns": {r: 2, ix: 5, iy: 5},
            "frame_radio_groups": {r: 3, c: 0},
            "plot_button": {r: 4, c: 0},
            "plot_frame": {r: 0, c: 1, rs: 4},

            # frame_treeview_controller
            "scrollbar_x_treeview_controller": {r: 3, s: "ew"},
            "treeview_treeview_controller": {r: 1, c: 0},
            "scrollbar_y_treeview_controller": {r: 1, c: 1, s: "ns"},

            # frame_radio_groups
            "frame_rb_group_1": {r: 0, c: 0},
            "frame_rb_group_2": {r: 0, c: 1},
            "frame_rb_group_3": {r: 0, c: 2},

            # frame_rb_group_1
            "rb_h": {r: 0, c: 0},
            "rb_v": {r: 1, c: 0},

            # frame_rb_group_2
            "rb_sa": {r: 0, c: 0},
            "rb_sv": {r: 1, c: 0},

            # frame_rb_group_3
            "rb_sda": {r: 0, c: 0},
            "rb_sdd": {r: 1, c: 0},

            # plot_frame
            "plot_toolbar": {},
            "plot_canvas.get_tk_widget()": {}
        }

        self.init_grid_args = {
            ".",
            "frame_treeview_controller",
            "label_treeview_controller",
            "scrollbar_x_treeview_controller",
            "treeview_treeview_controller",
            "scrollbar_y_treeview_controller",
            "frame_btns",
            "frame_radio_groups",
            "frame_rb_group_1",
            "frame_rb_group_2",
            "frame_rb_group_3",
            "rb_h",
            "rb_v",
            "rb_sa",
            "rb_sv",
            "rb_sda",
            "rb_sdd",
            "plot_button",
            "plot_frame"
        }

        self.frame_btns = tkinter.Frame(self, background="#4f4f4f")
        self.cb_lookup = {}
        self.selected_queue = deque(maxlen=self.max_chart_elements)

        self.tv_check_boxes, \
        self.check_boxes \
            = checkbox_factory(
                self.frame_btns,
                self.viewable_column_names,
                kwargs_buttons={"width": 12}
        )

        for i, cb in enumerate(self.check_boxes):
            tv = self.tv_check_boxes[i]
            text = self.viewable_column_names[i]
            cb.configure(command=(lambda text=text, cb=cb, tv=tv: self.click_radio(text, cb, tv)))
            self.cb_lookup.update({
                # f"var_{tv_cb}": tv_cb,
                f"var_{text}": tv
                # ,
                # f"text_{tv_cb}": text,
                # f"callback_{text}": cb
            })

        # for i, tv_cb in enumerate(self.tv_check_boxes):
            # text = self.viewable_column_names[i]
            # cb = tv_cb.trace_variable("w", self.update_check_boxes)
            # self.cb_lookup.update({
            #     f"var_{tv_cb}": tv_cb,
            #     f"var_{text}": tv_cb,
            #     f"text_{tv_cb}": text,
            #     f"callback_{text}": cb
            # })

        # ss1 = str(self.tv_check_boxes[0])
        # print(f"{ss1=}")
        # var = self.nametowidget(ss1)
        # print(f"{var=}")

        self.tv_plot_button,\
        self.plot_button\
            = button_factory(
                self,
                tv_btn="plot",
                kwargs_btn={"background": "#983434"},
                command=self.plot
        )

        self.frame_radio_groups = Frame(self)
        self.frame_rb_group_1 = Frame(self.frame_radio_groups)
        self.frame_rb_group_2 = Frame(self.frame_radio_groups)
        self.frame_rb_group_3 = Frame(self.frame_radio_groups)

        self.tv_orientation = StringVar(self, value="vertical")
        self.tv_orientation_h = StringVar(self, value="horizontal")
        self.tv_orientation_v = StringVar(self, value="vertical")
        self.rb_h = Radiobutton(self.frame_rb_group_1, variable=self.tv_orientation, value="horizontal", textvariable=self.tv_orientation_h)
        self.rb_v = Radiobutton(self.frame_rb_group_1, variable=self.tv_orientation, value="vertical", textvariable=self.tv_orientation_v)

        self.tv_sort_style = StringVar(self, value="by value")
        self.tv_sort_style_a = StringVar(self, value="alphabetical")
        self.tv_sort_style_v = StringVar(self, value="by value")
        self.rb_sa = Radiobutton(self.frame_rb_group_2, variable=self.tv_sort_style, value="alphabetical",
                            textvariable=self.tv_sort_style_a)
        self.rb_sv = Radiobutton(self.frame_rb_group_2, variable=self.tv_sort_style, value="by value", textvariable=self.tv_sort_style_v)

        self.tv_sort_direction = StringVar(self, value="descending")
        self.tv_sort_dir_a = StringVar(self, value="ascending")
        self.tv_sort_dir_d = StringVar(self, value="descending")
        self.rb_sda = Radiobutton(self.frame_rb_group_3, variable=self.tv_sort_direction, value="ascending",
                             textvariable=self.tv_sort_dir_a)
        self.rb_sdd = Radiobutton(self.frame_rb_group_3, variable=self.tv_sort_direction, value="descending",
                             textvariable=self.tv_sort_dir_d)

        self.available_plot_types = pd.DataFrame({
            'line': {'description': 'Line plot (default)'},
            'bar': {'description': 'Vertical bar plot'},
            'barh': {'description': 'Horizontal bar plot'},
            'hist': {'description': 'Histogram'},
            'box': {'description': 'Box plot'},
            'kde': {'description': 'Kernel Density Estimation plot'},
            'density': {'description': 'Same as "kde"'},
            'area': {'description': 'Area plot'},
            'scatter': {'description': 'Scatter plot'},
            'hexbin': {'description': 'Hexbin plot'},
            'pie': {'description': 'Pie chart'}
        })

        # MultiComboBox(self.available_plot_types, viewable_column_names=)

        plt.rcdefaults()
        self.plot_frame = tkinter.Frame(self)
        self.plot_fig, self.plot_ax = plt.subplots()
        self.plot_canvas = self.plot_canvas = FigureCanvasTkAgg(self.plot_fig,
                                   master=self.plot_frame)
        self.plot_toolbar = NavigationToolbar2Tk(self.plot_canvas, self.plot_frame, pack_toolbar=False)

        # self.tv_orientation.trace_variable("w", update_orientation_choice)

        if self.auto_grid is not None:
            self.grid_widgets()

        self.grid_args.update({"plot_canvas": self.grid_args["plot_canvas.get_tk_widget()"]})

    def click_radio(self, text, button, var):
        l = self.max_chart_elements - len(self.selected_queue)
        val = var.get()
        if not val:
            self.selected_queue.remove(text)
        else:
            if l > 0:
                # space for selection
                pass
            else:
                # pop the queue then add
                pop_txt = self.selected_queue.popleft()
                pop_var = self.cb_lookup[f"var_{pop_txt}"]
                pop_var.set(False)
            self.selected_queue.append(text)

        if len(self.selected_queue) != self.max_chart_elements:
            self.can_plot.set(False)
        else:
            x_col, y_col = self.selected_queue[0], self.selected_queue[1]
            x_plottable = self.col_data[x_col]["plottable"]
            y_plottable = self.col_data[y_col]["plottable"]
            if not x_plottable or not y_plottable:
                print(f"error columns '{x_col}' and '{y_col}' are not plottable.")
                self.can_plot.set(False)
            else:
                print(f"plotting columns '{x_col}', and '{y_col}'.")
                self.can_plot.set(True)

    # def update_check_boxes(self, *args):
    #     var, x, mode = args
    #     text = self.cb_lookup[f"text_{var}"]
    #     l = self.max_chart_elements - len(self.selected_queue)
    #     print(f"\n{var=}, {text=}, {type(var)=}\n{x=}, {type(x)=}\n{mode=}, {type(mode)=}\n{l=}")
    #
    #     val = self.getvar(var)
    #
    #     if val:
    #         if text not in self.selected_queue:
    #
    #             if l == 0:
    #                 # de_var = self.cb_lookup[self.selected_queue.popleft()]
    #                 # de_var = self.getvar(self.cb_lookup[self.selected_queue.popleft()])
    #
    #                 key = self.selected_queue.popleft()
    #                 print(f"{key=}")
    #                 f_key = f"var_{key}"
    #                 print(f"{f_key=}")
    #                 de_var = self.cb_lookup[f_key]
    #                 # print(f"{l_key=}")
    #                 # v_key = self.getvar(l_key)
    #                 # print(f"{v_key=}")
    #
    #                 # de_var = v_key
    #                 # print(f"{de_var=}")
    #                 val = de_var.get()
    #                 cb = self.cb_lookup[f"callback_{text}"]
    #                 de_var.trace_remove("write", cb)
    #                 de_var.set(not val)
    #                 cb = de_var.trace_variable("w", self.update_check_boxes)
    #                 self.cb_lookup.update({f"callback_{text}": cb})
    #
    #             self.selected_queue.append(text)
    #
    #             # print(dict_print(self.cb_lookup, "CB_LOOKUP"))
    #             # print(f"update_check_boxes, '{args}'\n\t{text=}\t{val=}")
    #         else:
    #             self.selected_queue.remove(text)
    #     else:
    #         # print(f"remove {text}")
    #         self.selected_queue.remove(text)
    #
    #         print(f"QUEUE: {self.selected_queue}")

    def get_xs_ys(self, place_holders=2):

        place_holders = clamp(0, place_holders, self.max_chart_elements)

        # if len(self.selected_queue) != (el := self.max_chart_elements):
        if len(self.selected_queue) < 2:
            messagebox.showinfo(title="PlotFrame", message=f"Please choose at least 2 columns first.")
            return [None for _ in range(place_holders)]

        cols = list(self.selected_queue)
        time_cols = []
        num_cols = []
        catg_cols = []
        for col in cols:
            if self.col_data[col]["is_numeric"]:
                num_cols.append(col)
            elif self.col_data[col]["is_date"]:
                time_cols.append(col)
            elif self.col_data[col]["plottable"]:
                catg_cols.append(col)

        print(f"num_cols: {num_cols}")
        print(f"time_cols: {time_cols}")
        print(f"catg_cols: {catg_cols}")

        if len(time_cols) == 1:
            result = time_cols, catg_cols + num_cols
        elif len(num_cols) == 1:
            result = num_cols, catg_cols + time_cols
        elif len(catg_cols) == 1:
            result = catg_cols, time_cols + num_cols
        else:
            result = time_cols, catg_cols + num_cols

        return result

    def plot(self):
        print(f"PLOT")

        # if len(self.selected_queue) != (el := self.max_chart_elements):
        if len(self.selected_queue) < 2:
            messagebox.showinfo(title="PlotFrame", message=f"Please choose at least 2 columns first.")
            return

        x_cols, y_cols = self.selected_queue[0], self.selected_queue[1]
        # x_col, y_cols = self.get_xs_ys()

        if not self.can_plot.get():
            messagebox.showinfo(title="PlotFrame", message=f"error columns '{x_col}', and '{y_cols}' are not plottable.")
            return

        plt.rcdefaults()
        self.plot_fig, self.plot_ax = plt.subplots()

        if self.plot_canvas is not None:
            self.plot_canvas.get_tk_widget().grid_forget()
            self.plot_toolbar.grid_forget()

        self.plot_canvas = FigureCanvasTkAgg(self.plot_fig,
                                   master=self.plot_frame)
        self.plot_canvas.draw()

        # creating the Matplotlib toolbar
        self.plot_toolbar = NavigationToolbar2Tk(self.plot_canvas,
                                       self.plot_frame, pack_toolbar=False)
        self.plot_toolbar.update()

        # placing the toolbar on the Tkinter window
        # self.plot_canvas.get_tk_widget().grid(**self.grid_args["plot_canvas"])
        self.plot_toolbar.grid(**self.grid_args["plot_toolbar"])

        # placing the canvas on the Tkinter window
        # self.plot_canvas.get_tk_widget().pack()
        self.plot_canvas.get_tk_widget().grid(**self.grid_args["plot_canvas"])

        if self.tv_orientation.get() == self.tv_orientation_h.get():
            x_col, y_cols = y_cols, x_col

        # if self.tv_sort_style.get() == self.tv_sort_style_v.get():
        if self.tv_sort_direction.get() == self.tv_sort_dir_a.get():
            self.df.sort_values(by=y_cols, ascending=True, inplace=True)
        else:
            self.df.sort_values(by=x_col, ascending=False, inplace=True)

        dtypes = self.df.dtypes
        x_type = dtypes[x_col]
        y_type = dtypes[y_cols]

        print(f"graphing a {x_type=} vs. {y_type=}\ncolumns: {x_col}, {y_cols}")

        self.df.set_index(x_col)

        # assert isinstance(self.df, pd.DataFrame)
        self.df.plot(kind="scatter", y=y_cols, color="#ce5656", ax=self.plot_ax)
        colours = rainbow_gradient(len(y_cols), rgb=False)
        # self.df.plot(y=y_cols, color=list(colours), ax=self.plot_ax)


        # data_points, show_names = data_in
        #
        # plt.rcdefaults()
        # fig, ax = plt.subplots()
        #
        # # alpha
        # if mode == "alpha":
        #     show_names, data_points = [list(x) for x in
        #                                zip(*sorted(zip(show_names, data_points), key=itemgetter(0), reverse=reverse))]
        # elif mode == "value":
        #     data_points, show_names = [list(x) for x in
        #                                zip(*sorted(zip(data_points, show_names), key=itemgetter(0), reverse=reverse))]
        # # data_points, show_names = [list(x) for x in zip(*sorted(zip(data_points, show_names), key=itemgetter(0)))]
        #
        # y_pos = np.arange(len(show_names))
        # if orientation == "horizontal":
        #     ax.barh(y_pos, data_points, align="center")
        #     ax.set_yticks(y_pos, labels=show_names)
        #     ax.invert_yaxis()
        #     ax.set_xlabel(xlabel)
        #     ax.set_title(title)
        # else:
        #     ax.bar(y_pos, data_points, align="center")
        #     ax.set_xticks(y_pos, labels=show_names)
        #     ax.tick_params(axis="x", rotation=90)
        #     ax.invert_xaxis()
        #     ax.set_ylabel(xlabel)
        #     ax.set_title(title)
        #
        # plot(fig)

    def grid_widgets(self):
        print(f"grid_widgets")

        r, c, rs, cs, ix, iy, x, y, s = grid_keys()

        for k in self.init_grid_args:
            v = self.grid_args[k]
            ke = "" if k == "." else f".{k}"
            eval(f"self{ke}.grid(**{v})")

        if self.treeview_controller.aggregate_data:
            for i, data in enumerate(self.aggregate_objects_treeview_controller):
                if i > 0:
                    tv, entry, x1x2 = data
                    # print(f"{i=}, {tv.get()=}")
                    entry.grid(row=0, column=i)
                else:
                    data.grid(row=2)

        # self.frame_btns.grid()
        bpr = self.btns_per_row
        cols = len(self.viewable_column_names) // bpr
        for i, cb in enumerate(self.check_boxes):
            ri = i // bpr
            ci = i % bpr
            if not self.btns_horizontal:
                ri, ci = ci, ri

            cb.grid(**{r: ri, c: ci})


if __name__ == '__main__':
    WIN = tkinter.Tk()
    # WIN.geometry(f"900x600")
    WIN.state("zoomed")
    WIN.title("Pyodbc + Treeview + Matplotlib")
    df_IT_requests = connect("SELECT * FROM [IT Requests]")

    pf = PlotFrame(
        WIN,
        df_IT_requests,
        viewable_column_names=[
            "RequestDate",
            "Status",
            "Request",
            "RequestedBy",
            "LabourEstimate",
            "LabourActual",
            "Comments"
        ],
        auto_grid=True,
        btns_horizontal=False,
        max_chart_elements=2
    )

    WIN.mainloop()

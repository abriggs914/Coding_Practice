import random
import tkinter

import pandas

from utility import *
import screeninfo
from tkinter_utility import *


class TreeViewCanvas(tkinter.Frame):

    def __init__(
            self,
            master,
            data,
            title=None,
            viewable_column_names=None,
            n_viewable_rows=10,
            width=600,
            height=400,
            auto_grid=True,
            def_cell_font=("Arial", 12),
            def_cell_background=("#D2D2F5", "#F5D2D2"),
            def_cell_foreground=("#000000",),
            def_cell_border_fill=("#000000",),
            def_cell_border_width=3,
            include_header=True
    ):
        super().__init__(master, height=height, width=width)

        assert isinstance(data,
                          pandas.DataFrame), f"Error param 'data' must be an instance of a pandas.DataFrame, got '{type(data)}'."

        self.include_title = bool(title)
        self.include_header = include_header
        self.title = str(title if title else "")
        self.data = data
        cn = self.data.columns
        if viewable_column_names is not None:
            for col in viewable_column_names:
                assert col in cn, f"Error, column '{col}' specified in param 'viewable_column_names' is not in the dataframe this treeview represents."
        self.viewable_column_names = viewable_column_names if viewable_column_names else cn
        self.n_viewable_rows = n_viewable_rows if n_viewable_rows is not None else 10

        self.def_cell_args = self.validate_cell_args(
            def_cell_font,
            def_cell_background,
            def_cell_foreground,
            def_cell_border_fill,
            def_cell_border_width
        )
        self.cell_args = {i: dict(self.gen_cell_args(i, data.loc[i])) for i, row_data in enumerate(self.data.itertuples())}

        self.auto_grid = self.validate_auto_grid(auto_grid)

        self.width = width
        self.height = height

        # x, y, w, h
        self.frame_dims = {
            "frame_title_label": [0, 0, self.width, self.height * 0.08],
            "frame_search_objects": [0, self.height * 0.08, self.width, self.height * 0.12],
            "frame_tree_canvas": [0, self.height * (0.12 + 0.08), self.width, self.height * 0.75],
            "frame_aggregate_row": [0, self.height * (0.75 + 0.08 + 0.12), self.width, self.height * 0.05]
        }

        self.colours = {
            "frame_title_label": Colour("yellow").hex_code,
            "frame_search_objects": Colour("skyblue").hex_code,
            "frame_tree_canvas": Colour("emerald").hex_code,
            "frame_aggregate_row": Colour("light_red").hex_code,
            "tree_window": Colour("#783426").hex_code
        }

        self.frame_title_label = tkinter.Frame(
            self,
            name="f_title",
            bg=self.colours["frame_title_label"],
            width=self.frame_dims["frame_title_label"][2],
            height=self.frame_dims["frame_title_label"][3]
        )
        self.frame_search_objects = tkinter.Frame(
            self,
            name="f_search",
            bg=self.colours["frame_search_objects"],
            width=self.frame_dims["frame_search_objects"][2],
            height=self.frame_dims["frame_search_objects"][3]
        )
        self.frame_tree_canvas = tkinter.Frame(
            self,
            name="f_tree",
            bg=self.colours["frame_tree_canvas"],
            width=self.frame_dims["frame_tree_canvas"][2],
            height=self.frame_dims["frame_tree_canvas"][3]
        )
        self.frame_aggregate_row = tkinter.Frame(
            self,
            name="f_aggregate",
            bg=self.colours["frame_aggregate_row"],
            width=self.frame_dims["frame_aggregate_row"][2],
            height=self.frame_dims["frame_aggregate_row"][3]
        )
        self.tree_window = tkinter.Canvas(
            self.frame_tree_canvas,
            name="c_tree",
            bg=self.colours["tree_window"],
            width=self.frame_dims["frame_tree_canvas"][2],
            height=self.frame_dims["frame_tree_canvas"][3]
        )

        self.tv_lbl_f1, self.lbl_f1 = label_factory(self.frame_title_label, str(self.frame_title_label), kwargs_label={"bg": self.colours["frame_title_label"]})
        self.tv_lbl_f2, self.lbl_f2 = label_factory(self.frame_search_objects, str(self.frame_search_objects), kwargs_label={"bg": self.colours["frame_search_objects"]})
        self.tv_lbl_f3, self.lbl_f3 = label_factory(self.frame_tree_canvas, str(self.frame_tree_canvas), kwargs_label={"bg": self.colours["frame_tree_canvas"]})
        self.tv_lbl_f4, self.lbl_f4 = label_factory(self.frame_aggregate_row, str(self.frame_aggregate_row), kwargs_label={"bg": self.colours["frame_aggregate_row"]})

        r, c, rs, cs, ix, iy, x, y, s = grid_keys()
        self.grid_args = {
            ".": {
                r: self.auto_grid[1],
                c: self.auto_grid[2]
            },
            "frame_title_label": {r: 0},
            "frame_search_objects": {r: 1},
            "frame_tree_canvas": {r: 2},
            "frame_aggregate_row": {r: 3},

            # frame_title_label
            "lbl_f1": {r: 0},

            # frame_search_objects
            "lbl_f2": {r: 0},

            # frame_tree_canvas
            "tree_window": {r: 1},
            "lbl_f3": {r: 0},

            # frame_aggregate_row
            "lbl_f4": {r: 0}
        }

        self.init_grid_args = {
            ".",
            "frame_title_label",
            "frame_search_objects",
            "frame_tree_canvas",
            "frame_aggregate_row",
            "tree_window",

            "lbl_f1",
            "lbl_f2",
            "lbl_f3",
            "lbl_f4"
        }

        self.init_tree_canvas()

        print(dict_print(self.grid_args, "grid_args"))
        print(dict_print(self.cell_args, "cell_args"))

        if self.auto_grid[0]:
            self.grid_widgets()

    def validate_cell_args(self, font_in, bg_in, fg_in, border_fill_in, border_width_in, use_defaults=False):
        valid_cell_font = ["font_family", "font_size"]
        def_cell_font = (("Arial", 12),)
        def_cell_bg = ("#E2E2E2", "#A2A2A2")
        def_cell_fg = ("#000000",)
        def_cell_border_fill = ("#000000",)
        def_cell_border_width = (2,)
        if use_defaults:
            font_in = def_cell_font
        else:
            assert isinstance(font_in, (tuple, dict)), f"Error, font must be a tuple or dict, got '{type(font_in)}'."
        if isinstance(font_in, dict):
            font_in = [font_in[k] for k in valid_cell_font]
        if len(font_in) != len(valid_cell_font):
            if use_defaults:
                font_in = def_cell_font
            else:
                raise ValueError(f"Invalid font args passed. Got '{font_in}'")
        if font_in[1] <= 0 or font_in[1] > 72:
            if use_defaults:
                font_in = def_cell_font
            else:
                raise ValueError(f"Font size out of range (1-72), got '{font_in[1]}'.")

        if border_width_in < 0 or border_width_in > 20:
            raise ValueError(f"Error, 'border_width' is out of range, got '{border_width_in}'")

        font_in = [font_in] if isinstance(font_in, (list, tuple)) else [[font_in]]
        bg_in = bg_in if isinstance(bg_in, (list, tuple)) else [bg_in]
        fg_in = fg_in if isinstance(fg_in, (list, tuple)) else [fg_in]
        border_fill_in = border_fill_in if isinstance(border_fill_in, (list, tuple)) else [border_fill_in]
        border_width_in = border_width_in if isinstance(border_width_in, (list, tuple)) else [border_width_in]

        t_bg = def_cell_bg[0]
        t_bg_in = []
        for bg in bg_in:
            try:
                t_bg = Colour(bg).hex_code
            except Colour.ColourCreationError as cce:
                if use_defaults:
                    t_bg = def_cell_bg
                else:
                    raise cce
            finally:
                t_bg_in.append(t_bg)
        bg_in = t_bg_in

        t_fg = def_cell_fg[0]
        t_fg_in = []
        for fg in fg_in:
            try:
                t_fg = Colour(fg).hex_code
            except Colour.ColourCreationError as cce:
                if use_defaults:
                    t_fg = def_cell_fg
                else:
                    raise cce
            finally:
                t_fg_in.append(t_fg)
        fg_in = t_fg_in

        t_bf = def_cell_border_fill[0]
        t_bf_in = []
        for bf in border_fill_in:
            try:
                t_bf = Colour(bf).hex_code
            except Colour.ColourCreationError as cce:
                if use_defaults:
                    t_bf = def_cell_border_fill
                else:
                    raise cce
            finally:
                t_bf_in.append(t_bf)
        border_fill_in = t_bf_in

        return {
            "font": font_in,
            "background": bg_in,
            "foreground": fg_in,
            "border_fill": border_fill_in,
            "border_width": border_width_in
        }

    def validate_auto_grid(self, auto_grid):

        do_grid, ag_x, ag_y = False, 0, 0

        if isinstance(auto_grid, list) or isinstance(auto_grid, tuple):
            if len(auto_grid) == 2:
                do_grid, ag_x, ag_y = (True, *auto_grid)
            else:
                raise ValueError(f"Error, auto_grid param is not the right dimensions.")
        elif isinstance(auto_grid, int):
            if isinstance(auto_grid, bool):
                auto_grid = 0
            do_grid, ag_x, ag_y = True, 0, auto_grid

        if ag_x < 0 or ag_y < 0:
            raise ValueError(f"Error, auto_grid param is invalid.")

        return do_grid, ag_x, ag_y

    def grid_widgets(self):
        for k in self.init_grid_args:
            v = self.grid_args[k]
            ke = "" if k == "." else f".{k}"
            eval(f"self{ke}.grid(**{v})")

    def init_tree_canvas(self):
        cw = self.tree_window.cget("width")
        ch = self.tree_window.cget("height")
        ih = self.include_header
        data = self.data
        cn = self.viewable_column_names
        nr = min(self.n_viewable_rows, data.shape[0]) + (1 if ih else 0)

        gc = grid_cells(cw, len(cn), ch, nr)

        cell_tags = []
        cell_frames = []
        for i, dat in enumerate(data.itertuples()):
            for j, dp_col in enumerate(zip(dat, cn)):
                dp, col = dp_col
                cell_tags.append(self.tree_window.create_window(gc[i][j]))
                cell_frames.append(tkinter.Frame(self.tree_window))

    def gen_cell_args(self, row_idx, row_data):
        style = dict(self.def_cell_args)
        font = style["font"][row_idx % len(style["font"])]
        bg = style["background"][row_idx % len(style["background"])]
        fg = style["foreground"][row_idx % len(style["foreground"])]
        border_fill = style["border_fill"][row_idx % len(style["border_fill"])]
        border_width = style["border_width"][row_idx % len(style["border_width"])]

        return {
            "font": font,
            "background": bg,
            "foreground": fg,
            "border_fill": border_fill,
            "border_width": border_width
        }


def gen_random_df(cols, n_rows, cell_range, cell_fill):
    df = pandas.DataFrame(columns=cols)

    match cell_fill:
        case "double":
            func = lambda: random_in_range(*cell_range)
        case "str":
            func = lambda: "".join([chr(random.randint(97, 97+26)) for i in range(random.randint(1, 8))])
        case _:
            func = lambda: random.randint(*cell_range)

    for i in range(n_rows):
        df.loc[i] = [func() for col in cols]
    print(f"{df}")
    return df


class App(tkinter.Tk):

    def __init__(self, width="zoomed", height="zoomed"):
        super().__init__()

        self.x_, self.y_, self.width_, self.height_ = self.calc_monitor_dims()

        if width == height == "zoomed":
            self.state(width)
        else:
            if width == "zoomed":
                self.x_ = 0
                self.height_ = height
            elif height == "zoomed":
                self.y_ = 0
                self.width_ = width
            else:
                width_c = clamp(1, width, self.width_)
                height_c = clamp(1, height, self.height_)
                x = (self.width_ - width_c) // 2
                y = (self.height_ - height_c) // 2
                self.x_, self.y_, self.width_, self.height_ = x, y, width_c, height_c

            self.geometry(f"{self.width_}x{self.height_}+{self.x_}+{self.y_}")

        data = gen_random_df(cols=["A", "B", "C"], n_rows=12, cell_range=(-25, 25), cell_fill="int")

        self.tree_canvas = TreeViewCanvas(
            self,
            data,
            width=200,
            height=300
        )

    def calc_monitor_dims(self):
        monitors = screeninfo.get_monitors()

        for mon in monitors:
            print(f"{mon=}")

        lm = get_largest_monitor()
        print(f"\n{lm}")
        return lm.x, lm.y, lm.width, lm.height


if __name__ == '__main__':
    app = App(600, 400)
    app.mainloop()

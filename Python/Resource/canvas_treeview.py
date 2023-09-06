import random
import tkinter

import pandas

from tkinter import font
from utility import *
import screeninfo
from tkinter_utility import *


def chars_in_width(font, c_width):
    cs = ["w", "a", "n", "0", "."]
    a = avg(map(lambda c: font.measure(c), cs))
    print(f"{list(map(lambda c: font.measure(c), cs))=}")
    print(f"\n\t{a=}")
    print(f"\t{round(c_width / a)=}\n")
    return round(c_width / a)
    # # wc = "w"  # 18c @ 200px
    # # wc = "."  # 66c @ 200px
    # # wc = "n"  # 24c @ 200px
    # tw = 0
    # t = ""
    # i = 1
    # for i in range(1, 1001):
    #     t += wc
    #     tw = font.measure(t)
    #     if c_width <= tw:
    #         break
    # print(f">> chars_in_width: {c_width=}, {i-1=}, {tw=}")
    # return i - 1


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
            include_index_col=True,
            index_starts_at_0=True,
            index_col_label="#",
            # def_cell_font=("Arial", 12),
            def_cell_font="AUTO_FONT",
            def_cell_background=("#D2D2F5", "#F5D2D2"),
            def_cell_foreground=("#000000",),
            def_cell_border_fill=("#000000",),
            def_cell_border_width=1,
            def_cell_auto_font="TkDefaultFont",
            border_thickness_header_row=1,
            include_header=True,
            cell_is_widget=None,
            cell_is_entry=None,
            cell_is_label=None,
            editable=True,
            justify="center"
    ):
        super().__init__(master, height=height, width=width)

        assert isinstance(data,
                          pandas.DataFrame), f"Error param 'data' must be an instance of a pandas.DataFrame, got '{type(data)}'."

        self.border_thickness_header_row = border_thickness_header_row
        self.index_col_label = index_col_label
        self.index_starts_at_0 = index_starts_at_0
        self.include_index_col = include_index_col
        self.include_title = bool(title)
        self.include_header = include_header
        self.title = str(title if title else "")
        self.data = data
        cn = list(self.data.columns)
        if viewable_column_names is not None:
            for col in viewable_column_names:
                assert col in cn, f"Error, column '{col}' specified in param 'viewable_column_names' is not in the dataframe this treeview represents."
        self.viewable_column_names = viewable_column_names if viewable_column_names else cn
        if self.include_index_col:
            assert self.index_col_label not in self.viewable_column_names, f"Error index column label '{self.index_col_label}' cannot be a vieable column already."
            assert self.index_col_label not in cn, f"Error index column label '{self.index_col_label}' cannot be a column in the dataframe already."
            self.viewable_column_names.insert(0, self.index_col_label)
            # self.data[self.index_col_label] = [tup[0] for tup in self.data.itertuples()]

        self.list_tv_entry_vars = []

        self.cell_is_widget, \
        self.cell_is_entry, \
        self.cell_is_label = \
            self.validate_cell_is(cell_is_widget, cell_is_entry, cell_is_label)
        self.text_justify = self.validate_justify(justify)

        for w_, e_, l_ in zip(self.cell_is_widget, self.cell_is_entry, self.cell_is_label):
            print(f"{w_=}, {e_=}, {l_=}")

        # self.cell_is_editable = self.validate_is_ediatble()

        self.n_viewable_rows = n_viewable_rows if n_viewable_rows is not None else 10

        self.def_cell_auto_font = tkinter.font.nametofont(def_cell_auto_font)

        self.def_cell_args = self.validate_cell_args(
            def_cell_font,
            def_cell_background,
            def_cell_foreground,
            def_cell_border_fill,
            def_cell_border_width
        )
        self.cell_args = {(i, j): dict(self.gen_cell_args(i, data.loc[i])) for i, row_data in enumerate(self.data.itertuples()) for j, col in enumerate(cn)}

        print(dict_print(self.cell_args, "cell_args"))
        print(f"{self.data}")
        pca = dict(self.cell_args)
        for k in pca:
            i, j = k
            print(f"{i=}, {j=}, {self.data.loc[i][j]=}")
            pca[k]["v"] = self.data.loc[i][j]
        print(dict_print(pca, "PCA"))

        self.auto_grid = self.validate_auto_grid(auto_grid)

        self.width = width
        self.height = height

        self.height_header = 20

        # x, y, w, h
        self.frame_dims = {
            "frame_title_label": [0, 0, self.width, self.height * 0.08],
            "frame_search_objects": [0, self.height * 0.08, self.width, self.height * 0.12],
            "frame_tree_canvas": [0, self.height * (0.12 + 0.08), self.width, self.height * 0.75],
            "frame_aggregate_row": [0, self.height * (0.75 + 0.08 + 0.12), self.width, self.height * 0.05]
        }

        self.colours = {
            "frame_title_label": Colour("yellow"),
            "frame_search_objects": Colour("skyblue"),
            "frame_tree_canvas": Colour("emerald"),
            "frame_aggregate_row": Colour("light_red"),
            "tree_window": Colour("#263478").brighten(0.35),
            "background_header_row": Colour("#747575"),
            "foreground_header_row": Colour("#747575").font_foreground_c(),
            "border_fill_header_row": Colour("000000")
        }

        self.frame_title_label = tkinter.Frame(
            self,
            name="f_title",
            bg=self.colours["frame_title_label"].hex_code,
            width=self.frame_dims["frame_title_label"][2],
            height=self.frame_dims["frame_title_label"][3]
        )
        self.frame_search_objects = tkinter.Frame(
            self,
            name="f_search",
            bg=self.colours["frame_search_objects"].hex_code,
            width=self.frame_dims["frame_search_objects"][2],
            height=self.frame_dims["frame_search_objects"][3]
        )
        self.frame_tree_canvas = tkinter.Frame(
            self,
            name="f_tree",
            bg=self.colours["frame_tree_canvas"].hex_code,
            width=self.frame_dims["frame_tree_canvas"][2],
            height=self.frame_dims["frame_tree_canvas"][3]
        )
        self.frame_aggregate_row = tkinter.Frame(
            self,
            name="f_aggregate",
            bg=self.colours["frame_aggregate_row"].hex_code,
            width=self.frame_dims["frame_aggregate_row"][2],
            height=self.frame_dims["frame_aggregate_row"][3]
        )
        self.tree_window = tkinter.Canvas(
            self.frame_tree_canvas,
            name="c_tree",
            bg=self.colours["tree_window"].hex_code,
            width=self.frame_dims["frame_tree_canvas"][2],
            height=self.frame_dims["frame_tree_canvas"][3]
        )

        self.tv_lbl_f1, self.lbl_f1 = label_factory(self.frame_title_label, str(self.frame_title_label), kwargs_label={"bg": self.colours["frame_title_label"].hex_code})
        self.tv_lbl_f2, self.lbl_f2 = label_factory(self.frame_search_objects, str(self.frame_search_objects), kwargs_label={"bg": self.colours["frame_search_objects"].hex_code})
        self.tv_lbl_f3, self.lbl_f3 = label_factory(self.frame_tree_canvas, str(self.frame_tree_canvas), kwargs_label={"bg": self.colours["frame_tree_canvas"].hex_code})
        self.tv_lbl_f4, self.lbl_f4 = label_factory(self.frame_aggregate_row, str(self.frame_aggregate_row), kwargs_label={"bg": self.colours["frame_aggregate_row"].hex_code})

        r, c, rs, cs, ix, iy, x, y, s = grid_keys()
        self.grid_args = {
            ".": {
                r: self.auto_grid[1],
                c: self.auto_grid[2]
            },
            "frame_title_label": {r: 0, x: 20, y: 20},
            "frame_search_objects": {r: 1, x: 20},
            "frame_tree_canvas": {r: 2, x: 20},
            "frame_aggregate_row": {r: 3, x: 20},

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
            if font_in != "AUTO_FONT":
                assert isinstance(font_in, (tuple, dict)), f"Error, font must be a tuple or dict, got '{type(font_in)}'."

        if font_in != "AUTO_FONT":
            if isinstance(font_in, dict):
                font_in = [font_in[k] for k in valid_cell_font]
            if len(font_in) != len(valid_cell_font):
                if use_defaults:
                    font_in = def_cell_font
                else:
                    raise ValueError(f"Invalid font args passed. Got '{font_in}'")
            if font_in[1] <= 0 or font_in[1] > 300:
                if use_defaults:
                    font_in = def_cell_font
                else:
                    raise ValueError(f"Font size out of range (1-300), got '{font_in[1]}'.")

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

    def validate_justify(self, justify):

        # TODO not sure why text alignments other than left are not visible.
        #   I am setting the width of the label and text widgets and wrapping frames,
        #   but I can't see the texts when they are aligned center or right.
        # justify = "left"

        r, c = self.data.shape
        justifications = [["center" for j in range(c)] for i in range(r)]
        valid = ["center", "left", "right"]
        if (isinstance(justify, (list, tuple))) and (len(justify) == r) and all([(isinstance(justify[i], (list, tuple)) and (len(justify[i]) == c)) for i in range(r)]):
            for i in range(r):
                for j in range(c):
                    if justify[r][c].lower() not in valid:
                        raise ValueError(f"Error, value '{justify[i][j]}' not a valid text justification.")
                    else:
                        justifications[i][j] = justify[i][j].lower()
        elif isinstance(justify, dict):
            for k in justify:
                if (isinstance(k, tuple)) and (len(k) == 2) and ((-1 < k[0] < r) and (-1 < k[1] < c)) and (justify[k].lower() in valid):
                    justifications[k[0]][k[1]] = justify[k].lower()
                else:
                    raise ValueError(f"Error, value '{justify[k]}' not a valid text justification.")
        elif isinstance(justify, str):
            if justify.lower() in valid:
                justifications = [[justify for j in range(c)] for i in range(r)]
            else:
                raise ValueError(f"Error, value '{justify}' not a valid text justification.")
        else:
            raise ValueError(f"Error, value '{justify}' not a valid text justification.")

        # if just not in valid:
        #     raise ValueError(f"Error, value '{just}' not a valid text justification.")
        return justifications

    def validate_cell_is(self, is_widget_in, is_entry_in, is_label_in):

        r, c = self.data.shape
        widgets = [[False for j in range(c)] for i in range(r)]
        entries = [[False for j in range(c)] for i in range(r)]
        labels = [[True for j in range(c)] for i in range(r)]

        unparsable = False

        print(f"\n\t{is_widget_in=}, {type(is_widget_in)=}\n\t{is_entry_in=}, {type(is_entry_in)=}\n\t{is_label_in=}, {type(is_label_in)=}")

        for i in range(r):
            for j in range(c):
                m = "_"
                if isinstance(is_widget_in, (list, tuple)):
                    m += "A"
                    if len(is_widget_in) == r and all([(isinstance(is_widget_in[ii], (list, tuple)) and len(is_widget_in[ii]) for ii in range(r))]):
                        widgets[i][j] = is_widget_in[i][j]
                        entries[i][j] = not is_widget_in[i][j]
                        labels[i][j] = not is_widget_in[i][j]
                        m += "B"
                    else:
                        unparsable = True
                        m += "C"
                elif isinstance(is_widget_in, dict):
                    m += "D"
                    if len(is_widget_in) == r and all([(isinstance(k, tuple) and (len(k) == 2) and (-1 < k[0] < r) and (-1 < k[1] < c)) for k in is_widget_in]):
                        widgets[i][j] = is_widget_in[(i, j)]
                        entries[i][j] = not is_widget_in[i][j]
                        labels[i][j] = not is_widget_in[i][j]
                        m += "E"
                    else:
                        unparsable = True
                        m += "F"
                elif isinstance(is_widget_in, bool):
                    widgets[i][j] = is_widget_in
                    entries[i][j] = not is_widget_in
                    labels[i][j] = not is_widget_in
                    m += "G"

                elif isinstance(is_entry_in, (list, tuple)):
                    m += "H"
                    if len(is_entry_in) == r and all([(isinstance(is_entry_in[ii], (list, tuple)) and len(is_entry_in[ii]) for ii in range(r))]):
                        widgets[i][j] = not is_entry_in[i][j]
                        entries[i][j] = is_entry_in[i][j]
                        labels[i][j] = not is_entry_in[i][j]
                        m += "I"
                    else:
                        unparsable = True
                elif isinstance(is_entry_in, dict):
                    m += "J"
                    if len(is_entry_in) == r and all([(isinstance(k, tuple) and (len(k) == 2) and (-1 < k[0] < r) and (-1 < k[1] < c)) for k in is_entry_in]):
                        widgets[i][j] = not is_entry_in[(i, j)]
                        entries[i][j] = is_entry_in[i][j]
                        labels[i][j] = not is_entry_in[i][j]
                        m += "K"
                    else:
                        unparsable = True
                        m += "L"
                elif isinstance(is_entry_in, bool):
                    widgets[i][j] = not is_entry_in
                    entries[i][j] = is_entry_in
                    labels[i][j] = not is_entry_in
                    m += "M"

                elif isinstance(is_label_in, (list, tuple)):
                    m += "N"
                    if len(is_widget_in) == r and all([(isinstance(is_label_in[ii], (list, tuple)) and len(is_label_in[ii]) for ii in range(r))]):
                        widgets[i][j] = not is_label_in[i][j]
                        entries[i][j] = not is_label_in[i][j]
                        labels[i][j] = is_label_in[i][j]
                        m += "O"
                    else:
                        unparsable = True
                        m += "P"
                elif isinstance(is_label_in, dict):
                    m += "Q"
                    if len(is_label_in) == r and all([(isinstance(k, tuple) and (len(k) == 2) and (-1 < k[0] < r) and (-1 < k[1] < c)) for k in is_label_in]):
                        widgets[i][j] = not is_label_in[(i, j)]
                        entries[i][j] = not is_label_in[i][j]
                        labels[i][j] = is_label_in[i][j]
                        m += "R"
                    else:
                        unparsable = True
                        m += "S"
                elif isinstance(is_label_in, bool):
                    widgets[i][j] = not is_label_in
                    entries[i][j] = not is_label_in
                    labels[i][j] = is_label_in
                    m += "T"

                else:
                    unparsable = True

                if unparsable:
                    raise ValueError(f"Error, val_in value '{is_widget_in}' is unparsable.")

                if not any([widgets[i][j], entries[i][j], labels[i][j]]):
                    raise ValueError(f"Error, you cannot explicitly set cell ({i}, {j}) as not a widget, not an entry, or not a label (all params are false). You must specify one, or widget is default.")

                print(f"{m=}")

        return widgets, entries, labels

        # def validate_is(is_list, val_in):
        #     r, c = self.data.shape
        #     values = [[True for j in range(c)] for i in range(r)]
        #
        #     unparsable = False
        #     if not isinstance(val_in, bool):
        #         if isinstance(val_in, (list, tuple)) and len(val_in) == r:
        #             for i in range(r):
        #                 if isinstance(val_in[i], (list, tuple)) and len(val_in[i]) == c:
        #                     for j in range(c):
        #                         values[i][j] = bool(val_in[i][j])
        #                 else:
        #                     unparsable = True
        #         elif isinstance(val_in, dict):
        #             for k in val_in:
        #                 if not isinstance(k, tuple) and len(k) == 2:
        #                     if (-1 < k[0] < r) and (-1 < k[1] < c):
        #                         values[k[0]][k[1]] = val_in[(k[0], k[1])]
        #                     else:
        #                         unparsable = True
        #         else:
        #             unparsable = True
        #     else:
        #         for i in range(r):
        #             for j in range(c):
        #                 values[i][j] = val_in
        #
        #     if unparsable:
        #         raise ValueError(f"Error, val_in value '{val_in}' is unparsable.")
        #
        #     for i in range(r):
        #         for j in range(c):
        #             is_list[i][j] = values[i][j]

    def grid_widgets(self):
        for k in self.init_grid_args:
            v = self.grid_args[k]
            ke = "" if k == "." else f".{k}"
            eval(f"self{ke}.grid(**{v})")

    def init_tree_canvas(self):
        hh = self.height_header
        cw = float(self.tree_window.cget("width"))
        ch = float(self.tree_window.cget("height")) - hh
        ih = self.include_header
        data = self.data
        cn = self.viewable_column_names
        # nr = min(self.n_viewable_rows, data.shape[0]) + (1 if ih else 0)
        nr = data.shape[0]

        # gc = grid_cells(cw, len(cn), ch, nr, x_pad=1, y_pad=1, x_0=1, y_0=1)
        gch = grid_cells(cw, len(cn), hh, 1, x_pad=0, y_pad=0, x_0=0, y_0=0)  #, r_int=int)
        gcc = grid_cells(cw, len(cn), ch, nr, x_pad=0, y_pad=0, x_0=0, y_0=hh)  #, r_int=int)
        # gcd = grid_cells(cw, len(cn), ch, nr, x_pad=2, y_pad=2, x_0=0, y_0=hh, r_int=int, r_type=dict)
        # print(f"{gc=}")
        # print(f"{data.shape=}")
        # print(f"cw={float('%.2f'%float(cw))}, ch={float('%.2f'%float(ch))}")
        # print(f"{gcd[0][0]=}")
        # print(f"{gcd[0][1]=}")
        # print(f"{gcd[0][2]=}")

        print(f"{cn=}")

        cell_tags = []
        cell_frames = []

        dim = gch[0][0]
        c_x = dim[0] + 2
        c_y = dim[1] + 2
        c_width = dim[2] - dim[0]
        c_height = dim[3] - dim[1]
        for i, col in enumerate(cn):
            dim = gch[0][i]
            c_x = dim[0]+2
            c_y = dim[1]+2
            b_col = self.colours["border_fill_header_row"].hex_code
            c_bw = self.border_thickness_header_row
            justify = self.text_justify[0][i]
            nfh = tkinter.Frame(
                self.tree_window,
                name=f"header_{0}_{i}",
                width=c_width,
                height=c_height,
                bg=self.colours["background_header_row"].hex_code,
                highlightbackground=b_col,
                highlightthickness=c_bw
            )

            text = f"{col}"
            cell_arg = self.cell_args[(0, i)]
            font = cell_arg["font"]
            if font == ["AUTO_FONT"]:
                font = self.auto_font(text, c_width, c_height)

            print(f"header justify: {justify=}\nheader_font={font.name=}, {font.metrics()['linespace']=}, {font.actual()['size']=}\n{c_width=}\n{c_height=}\n{text=}")
            print(f"{self.colours['background_header_row']=}")
            print(f"{self.colours['foreground_header_row']=}")
            demo_lbl_f = label_factory(
                nfh,
                tv_label=text,
                kwargs_label={
                    "bg": self.colours["background_header_row"].brightened(0.15).hex_code,
                    "fg": self.colours["foreground_header_row"].hex_code,
                    "font": font,
                    # "justify": justify,
                    "height": 1,

                    "width": chars_in_width(font, c_width)//2,
                    # # "width": len(col),
                    # "height": 1,
                    # "width": round(c_width / 8),
                    # "height": round(c_height),

                    # "image": tkinter.PhotoImage(),  # zero size image  # https://stackoverflow.com/questions/63839085/set-label-width-in-pixel-in-tkinter-python,
                    # "width": c_width,
                    # "compound": tkinter.CENTER,
                    # "height": c_height
                }
            )
            # nfh.columnconfigure(0, weight=1)
            # demo_lbl_f[1].grid(sticky="nsew")
            # demo_lbl_f[1].grid(sticky="e")
            demo_lbl_f[1].grid()

            cxy = (round(c_x + (c_width / 2)), round(c_y + (c_height / 2)))
            cell_tags.append(self.tree_window.create_window(
                    # dim[:2],
                    cxy,
                    window=nfh,
                    width=c_width,
                    height=c_height,
                    tags=[f"{{row: {0}, col: {i}}}"]
                ))
            cell_frames.append(nfh)

        for i, dat in enumerate(data.itertuples()):
            for j, dp_col in enumerate(zip(dat[(0 if self.include_index_col else 1):], cn)):
                # i = dat[0]

                val = dp_col[0]
                dim = gcc[i][j]
                c_x = dim[0]+2
                c_y = dim[1]+2
                c_width = dim[2] - dim[0]
                c_height = dim[3] - dim[1]
                # c_col_bg = random_colour(rgb=False)
                cell_arg = self.cell_args[(i, j)]
                c_col_bg = cell_arg["background"]
                c_col_fg = cell_arg["foreground"]
                c_font = cell_arg["font"]
                b_col = cell_arg["border_fill"]
                c_bw = cell_arg["border_width"]
                justify = self.text_justify[i][j]
                self.cell_args[(i, j)].update({"justify": justify})
                text = f"{val}"
                print(f"{c_font=}, {type(c_font)=}")
                if c_font == ["AUTO_FONT"]:
                    c_font = self.auto_font(text, c_width, c_height)
                cxy = (round(c_x + (c_width / 2)), round(c_y + (c_height / 2)))
                # print(f"{i=}, {j=}, cxy={list(map(lambda s: float('%.2f'%s), (c_x + (c_width / 2), c_y + (c_height / 2))))}, {dp_col=}, dim={list(map(lambda s: float('%.2f'%s), dim))}, cw={float('%.2f'%c_width)}, ch={float('%.2f'%c_height)}")
                print(f"{i=}, {j=}, cxy={list(map(lambda s: float('%.2f'%s), cxy))}, {dp_col=}, dim={list(map(lambda s: float('%.2f'%s), dim))}, cw={float('%.2f'%c_width)}, ch={float('%.2f'%c_height)}")
                dp, col = dp_col
                nf = tkinter.Frame(
                    self.tree_window,
                    name=f"cell_{i+1}_{j}",
                    width=c_width,
                    height=c_height,
                    bg=c_col_bg,
                    highlightbackground=b_col,
                    highlightthickness=c_bw
                )
                if self.include_index_col and j == 0 and not self.index_starts_at_0:
                    val += 1

                is_entry = self.cell_is_entry[i][j]
                is_label = self.cell_is_label[i][j]
                is_widget = self.cell_is_widget[i][j]
                is_editatble = "normal"
                # is_editable = self.cell_is_editable[i][j]
                if is_label:
                    demo_lbl_f = label_factory(
                        nf,
                        tv_label=text,
                        kwargs_label={
                            "bg": c_col_bg,
                            "fg": c_col_fg,
                            "font": c_font,
                            # "width": c_width,
                            # "width": len(text),
                            "justify": justify
                        }
                    )
                    demo_lbl_f[1].grid()
                elif is_entry:
                    demo_entry_f = entry_factory(
                        nf,
                        tv_entry=text,
                        kwargs_entry={
                            "bg": c_col_bg,
                            "fg": c_col_fg,
                            "font": c_font,
                            "justify": justify,
                            "state": is_editatble,
                            # "width": round(c_width),
                            "width": len(text)
                        }
                    )
                    demo_entry_f[3].grid()
                else:
                    pass

                cell_tags.append(self.tree_window.create_window(
                    # dim[:2],
                    cxy,
                    window=nf,
                    width=c_width,
                    height=c_height,
                    tags=[f"{{row: {i+1}, col: {j}}}"]
                ))
                cell_frames.append(nf)

        print(f"{cell_tags=}")
        print(f"{cell_frames=}")

    def auto_font(self, text, c_width, c_height):
        font = self.def_cell_auto_font
        width = font.measure(text)
        family = font.actual()["family"]
        size = font.actual()["size"]
        ls = font.metrics()["linespace"]
        # print(f"{family=}, {size=}, {ls=}, {font=}")
        while size < 300:
            font = tkinter.font.Font(family=family, size=size)
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
        while size > 4:
            font = tkinter.font.Font(family=family, size=size)
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

        self.def_cell_auto_font = font
        # ls = font.metrics()["linespace"]
        # print(f"FINAL {family=}, {size=}, {ls=}, {font=}")
        return font

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
    # print(f"{df}")
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

        # data = gen_random_df(
        #     cols=["A", "B", "C"],
        #     n_rows=4,
        #     cell_range=(-25, 25),
        #     cell_fill="int"
        # )

        data = gen_random_df(
            cols=["Fav #", "A"],
            n_rows=1,
            cell_range=(-25, 25),
            cell_fill="int"
        )

        self.tree_canvas = TreeViewCanvas(
            self,
            data,
            width=400,
            height=400,
            index_starts_at_0=False,
            include_index_col=False,
            cell_is_entry=True,
            justify="right"
        )

    def calc_monitor_dims(self):
        monitors = screeninfo.get_monitors()

        for mon in monitors:
            print(f"{mon=}")

        lm = get_largest_monitors()[0]
        print(f"\n{lm}")
        return lm.x, lm.y, lm.width, lm.height


if __name__ == '__main__':
    app = App(550, 550)
    app.mainloop()

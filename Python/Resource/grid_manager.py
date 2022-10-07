from colour_utility import *


#######################################################################################################################
#######################################################################################################################
#######################################################################################################################

VERSION = \
    """	
        Class to simplify tkinter grid geometry.
        Version..............1.01
        Date...........2022-09-26
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


# class GridManager:
#
#     def __init__(self):
#
#         self.valid_keys = {"widget", "columnspan", "rowspan", "padx", "pady", "ipadx", "ipady", "sticky"}
#
#         self._row_idx = 0
#         # self._col_idx = 0
#         self._max_rows = 0
#         self._max_cols = 0
#         self.tiles = [[None]]
#         self.widgets_added = []
#         self.tile_properties = [[None]]
#
#     def ungrid_widget(self, r, c):
#         if r > self.max_rows:
#             raise ValueError(f"Error, row {r} is out of range")
#         if c > self.max_cols:
#             raise ValueError(f"Error, column {c} is out of range")
#         widget = self.tiles[r][c]
#         details = self.tile_properties[r][c]
#         widget.grid_forget()
#         cs = details.get("comlumnspan", 1)
#         rs = details.get("rowspan", 1)
#         for rii in range(r, r + rs):
#             for cii in range(c, c + cs):
#                 # print(f"{rii=}, {cii=}")
#                 self.tile_properties[rii][cii] = None
#
#     def grid_widgets(self, widgets):
#         row_count = self.row_idx
#         ri = 0
#         for r, row in enumerate(widgets):
#             ri = r + 0 + row_count
#             col_count = 0
#             ci = 0
#             r_inner = 0
#             cs = 1
#             none_count = 0
#             for c, widget in enumerate(row):
#                 # print(f"\n--\n")
#                 if widget:
#                     args = {}
#                     cs, rs = 1, 1
#                     if isinstance(widget, dict):
#                         assert "widget" in widget, "Error, key 'widget' not passed."
#                         widget_keys = set(widget.keys())
#                         diff = widget_keys.difference(self.valid_keys)
#                         assert "row" not in diff, f"Error, key 'row' is illegal. Use position in a 2D list to indicate row."
#                         assert "column" not in diff, f"Error, key 'column' is illegal. Use position in a 2D list to indicate column."
#                         assert not diff, f"Error, key(s): '{diff}' are illegal."
#                         cs = widget.get("columnspan", 1)
#                         rs = widget.get("rowspan", 1)
#                         xp = widget.get("padx", None)
#                         yp = widget.get("pady", None)
#                         ixp = widget.get("ipadx", None)
#                         iyp = widget.get("ipady", None)
#                         st = widget.get("sticky", None)
#                         if cs:
#                             args["columnspan"] = cs
#                         if rs:
#                             args["rowspan"] = rs
#                         if xp:
#                             args["padx"] = xp
#                         if yp:
#                             args["pady"] = yp
#                         if ixp:
#                             args["ipadx"] = ixp
#                         if iyp:
#                             args["ipady"] = iyp
#                         if st:
#                             args["sticky"] = st
#
#                         widget = widget["widget"]
#                         # print(f"gridding widget={widget['widget']}, {r=}, {c=}, {ri=}, {ci=}, {args=}")
#                         # widget.grid(row=ri, column=ci, **args)
#
#                         none_count -= (cs - 1)
#                         col_count += cs
#                         ci += (col_count - 1)
#                         r_inner = max(r_inner, (rs - 1))
#
#                         # x, y = 25, 25
#                         # widget["widget"].create_text(x, y, text=str(widget))
#                         # widget["widget"].create_text(x, y + 10, text=str(ri))
#                         # widget["widget"].create_text(x, y + 20, text=str(ci))
#                     # else:
#
#                     ci += none_count
#                     print(f"gridding widget={widget}, {r=}, {c=}, {ri=}, {ci=}, {rs=}, {cs=}")
#
#                     self.validate(ri + (rs - 1), ci + (cs - 1))
#
#                     widget.grid(row=ri, column=ci, **args)
#
#                     x, y = 25, 25
#                     widget.create_text(x, y, text=str(widget))
#                     widget.create_text(x, y + 10, text=str(ri))
#                     widget.create_text(x, y + 20, text=str(ci))
#                     self.widgets_added.append((ri, ci, cs, rs))
#                     # print(f"\tIN {ri=}, {ci=}, rc={row_count}, cc={col_count}, nc={none_count}, {len(self.tiles)=}, {len(self.tiles[ri])=}, {args=}")
#                     for rii in range(ri, ri + rs):
#                         for cii in range(ci, ci + cs):
#                             # print(f"{rii=}, {cii=}")
#                             self.tiles[rii][cii] = widget
#                             self.tile_properties[rii][cii] = args
#                     ci += 1
#                 else:
#                     none_count += 1
#             row_count += r_inner
#         self.row_idx += ri + 1
#
#     def validate(self, r, c):
#         # print(f"A ({r=}, {c=}), mr={self.max_rows}, mc={self.max_cols}, {self.tiles=}")
#         self.max_rows = max(self.max_rows, r)
#         # print(f"B ({r=}, {c=}), mr={self.max_rows}, mc={self.max_cols}, {self.tiles=}")
#         self.max_cols = max(self.max_cols, c)
#         # print(f"C ({r=}, {c=}), mr={self.max_rows}, mc={self.max_cols}, {self.tiles=}")
#         self.max_rows = max(self.max_rows, r)
#         # print(f"D ({r=}, {c=}), mr={self.max_rows}, mc={self.max_cols}, {self.tiles=}")
#         self.grid_print()
#
#     def grid_print(self):
#         print("VVVVVVVVVVVVV")
#         for r, row in enumerate(self.tiles):
#             m = ""
#             for c in row:
#                 if c:
#                     m += f"| {c._name}".center(10)
#                 else:
#                     m += f"|   None  "
#             print(f"[{m + '|'}]")
#         print("^^^^^^^^^^^^^")
#
#     def occupied(self, r, c):
#         if r > self.max_rows:
#             raise ValueError(f"Error, row {r} is out of range")
#         if c > self.max_cols:
#             raise ValueError(f"Error, column {c} is out of range")
#         return self.tiles[r][c] is not None
#
#     # _row_idx
#     def get_row_idx(self):
#         return self._row_idx
#
#     def set_row_idx(self, row_idx_in):
#         self._row_idx = row_idx_in
#
#     def del_row_idx(self):
#         del self._row_idx
#
#     # _max_rows
#     def get_max_rows(self):
#         return self._max_rows
#
#     def set_max_rows(self, max_rows_in):
#         if self.max_rows < max_rows_in:
#             for r in range(max_rows_in - self.max_rows):
#                 self.tiles.append([None for c in range(self.max_cols + 1)])
#                 self.tile_properties.append([None for c in range(self.max_cols + 1)])
#         self._max_rows = max_rows_in
#
#     def del_max_rows(self):
#         del self._max_rows
#
#     # _max_cols
#     def get_max_cols(self):
#         return self._max_cols
#
#     def set_max_cols(self, max_cols_in):
#         if self.max_cols < max_cols_in:
#             for r, row in enumerate(self.tiles):
#                 # print(f"\t\t{1 + max_cols_in=}, {len(row)=}, {1 + max_cols_in - len(row)=}")
#                 for _ in range(1 + max_cols_in - len(row)):
#                     self.tiles[r].append(None)
#                     self.tile_properties[r].append(None)
#         self._max_cols = max_cols_in
#
#     def del_max_cols(self):
#         del self._max_cols
#
#     # col_idx = property(get_col_idx, set_col_idx, del_col_idx)
#     row_idx = property(get_row_idx, set_row_idx, del_row_idx)
#     max_rows = property(get_max_rows, set_max_rows, del_max_rows)
#     max_cols = property(get_max_cols, set_max_cols, del_max_cols)

class GridManager:

    def __init__(self, root):

        self.root = root

        self.valid_keys = {"widget", "columnspan", "rowspan", "padx", "pady", "ipadx", "ipady", "sticky"}

        self._row_idx = 0
        # self._col_idx = 0
        self._max_rows = 0
        self._max_cols = 0
        self.tiles = [[None]]
        self.widgets_added = dict()
        self.tile_properties = [[None]]

    # def ungrid_widget(self, r, c):
    #     if r > self.max_rows:
    #         raise ValueError(f"Error, row {r} is out of range")
    #     if c > self.max_cols:
    #         raise ValueError(f"Error, column {c} is out of range")
    #     widget = self.tiles[r][c]
    #     details = self.tile_properties[r][c]
    #     widget.grid_forget()
    #     cs = details.get("comlumnspan", 1)
    #     rs = details.get("rowspan", 1)
    #     for rii in range(r, r + rs):
    #         for cii in range(c, c + cs):
    #             # print(f"{rii=}, {cii=}")
    #             self.tile_properties[rii][cii] = None

    def grid_widgets(self, *widgets):
        if widgets:
            row_count = self.row_idx
            ri = 0
            for r, row in enumerate(widgets[0]):
                ri = r + 0 + row_count
                col_count = 0
                ci = 0
                r_inner = 0
                cs = 1
                none_count = 0
                for c, widget in enumerate(row):
                    # print(f"\n--\n")
                    if widget:
                        args = {}
                        cs, rs = 1, 1
                        if isinstance(widget, dict):
                            assert "widget" in widget, "Error, key 'widget' not passed."
                            widget_keys = set(widget.keys())
                            diff = widget_keys.difference(self.valid_keys)
                            assert "row" not in diff, f"Error, key 'row' is illegal. Use position in a 2D list to indicate row."
                            assert "column" not in diff, f"Error, key 'column' is illegal. Use position in a 2D list to indicate column."
                            assert not diff, f"Error, key(s): '{diff}' are illegal."
                            cs = widget.get("columnspan", 1)
                            rs = widget.get("rowspan", 1)
                            xp = widget.get("padx", None)
                            yp = widget.get("pady", None)
                            ixp = widget.get("ipadx", None)
                            iyp = widget.get("ipady", None)
                            st = widget.get("sticky", None)
                            if cs:
                                args["columnspan"] = cs
                            if rs:
                                args["rowspan"] = rs
                            if xp:
                                args["padx"] = xp
                            if yp:
                                args["pady"] = yp
                            if ixp:
                                args["ipadx"] = ixp
                            if iyp:
                                args["ipady"] = iyp
                            if st:
                                args["sticky"] = st

                            widget = widget["widget"]
                            # print(f"gridding widget={widget['widget']}, {r=}, {c=}, {ri=}, {ci=}, {args=}")
                            # widget.grid(row=ri, column=ci, **args)

                            none_count -= (cs - 1)
                            col_count += cs
                            ci += (col_count - 1)
                            r_inner = max(r_inner, (rs - 1))

                            # x, y = 25, 25
                            # widget["widget"].create_text(x, y, text=str(widget))
                            # widget["widget"].create_text(x, y + 10, text=str(ri))
                            # widget["widget"].create_text(x, y + 20, text=str(ci))
                        # else:

                        ci += none_count
                        print(f"gridding widget={widget}, {r=}, {c=}, {ri=}, {ci=}, {rs=}, {cs=}")

                        # self.verify_new_widget(widget)
                        #
                        # self.validate(ri + (rs - 1), ci + (cs - 1))
                        #
                        # widget.grid(row=ri, column=ci, **args)
                        #
                        self.place(widget, ri, ci, **args)
                        x, y = 25, 25
                        widget.create_text(x, y, text=str(widget))
                        widget.create_text(x, y + 10, text=str(ri))
                        widget.create_text(x, y + 20, text=str(ci))
                        # # self.widgets_added.append((ri, ci, cs, rs))
                        # # print(f"\tIN {ri=}, {ci=}, rc={row_count}, cc={col_count}, nc={none_count}, {len(self.tiles)=}, {len(self.tiles[ri])=}, {args=}")
                        # for rii in range(ri, ri + rs):
                        #     for cii in range(ci, ci + cs):
                        #         # print(f"{rii=}, {cii=}")
                        #         self.tiles[rii][cii] = widget
                        #         self.tile_properties[rii][cii] = args
                        ci += 1
                    else:
                        none_count += 1
                row_count += r_inner
            self.row_idx += ri + 1
        else:
            assert isinstance(self.root, tkinter.Tk)
            root = self.root
            for child in root.children:
                widget = self.root.nametowidget(child)
                print(f"{child=}, {widget=}")
                if isinstance(child, GridManager):
                    print(f"child {child} is a gridmanager")
                    child.grid_widgets()
                else:
                    self.place(widget, self.row_idx, 0)

                self.row_idx += 1


    def validate(self, r, c):
        # print(f"A ({r=}, {c=}), mr={self.max_rows}, mc={self.max_cols}, {self.tiles=}")
        self.max_rows = max(self.max_rows, r)
        # print(f"B ({r=}, {c=}), mr={self.max_rows}, mc={self.max_cols}, {self.tiles=}")
        self.max_cols = max(self.max_cols, c)
        # print(f"C ({r=}, {c=}), mr={self.max_rows}, mc={self.max_cols}, {self.tiles=}")
        self.max_rows = max(self.max_rows, r)
        # print(f"D ({r=}, {c=}), mr={self.max_rows}, mc={self.max_cols}, {self.tiles=}")

    def verify_new_widget(self, widget_in, assert_is_new=False) -> None | tuple[int, int]:
        if widget_in in self.widgets_added:
            if assert_is_new:
                raise Exception(
                    f"You cannot grid the same widget twice.\nWidget '{widget_in}' has already been gridded by this manager.")
            return self.widgets_added[widget_in]["row"], self.widgets_added[widget_in]["col"]
        self.widgets_added.update({widget_in: dict(zip(self.valid_keys, [None for _ in range(len(self.valid_keys))]))})

    def place(self, widget, r, c, columnspan=None, rowspan=None, padx=None, pady=None, ipadx=None, ipady=None, sticky=None):

        print(f"placing {widget=}, {r=}, {c=}, {columnspan=}, {rowspan=}, {padx=}, {pady=}, {ipadx=}, {ipady=}, {sticky=}")

        self.validate(r, c)
        rc = self.verify_new_widget(widget)
        kwargs = {}
        cs = columnspan
        rs = rowspan
        xp = padx
        yp = pady
        ixp = ipadx
        iyp = ipady
        st = sticky
        if cs:
            kwargs["columnspan"] = cs
        if rs:
            kwargs["rowspan"] = rs
        if xp:
            kwargs["padx"] = xp
        if yp:
            kwargs["pady"] = yp
        if ixp:
            kwargs["ipadx"] = ixp
        if iyp:
            kwargs["ipady"] = iyp
        if st:
            kwargs["sticky"] = st

        if rc is None:
            self.tile_properties[r][c] = kwargs
            self.tiles[r][c] = widget
            self.widgets_added[widget].update({
                "row": r,
                "col": c
            })

            widget.grid(row=r, column=c, **kwargs)
        else:
            fr, fc = rc
            old_args = self.tile_properties[fr][fc]
            for k1, v1 in kwargs.items():
                if v1 is None:
                    kwargs[k1] = old_args.get(k1, None)

            print(f"else {fr=}, {fc=}, {kwargs=}")
            # print(f"\n--\n")
            if 1:
                # args = {}
                ri = fr
                col_count = 0
                ci = fc
                r_inner = 0
                # cs = 1
                none_count = 0
                cs = 1 if cs is None else cs
                rs = 1 if rs is None else rs
                if 1:
                    # assert "widget" in widget, "Error, key 'widget' not passed."
                    # widget_keys = set(widget.keys())
                    # diff = widget_keys.difference(self.valid_keys)
                    # assert "row" not in diff, f"Error, key 'row' is illegal. Use position in a 2D list to indicate row."
                    # assert "column" not in diff, f"Error, key 'column' is illegal. Use position in a 2D list to indicate column."
                    # assert not diff, f"Error, key(s): '{diff}' are illegal."
                    # cs = widget.get("columnspan", 1)
                    # rs = widget.get("rowspan", 1)
                    # xp = widget.get("padx", None)
                    # yp = widget.get("pady", None)
                    # ixp = widget.get("ipadx", None)
                    # iyp = widget.get("ipady", None)
                    # st = widget.get("sticky", None)
                    # if cs:
                    #     args["columnspan"] = cs
                    # if rs:
                    #     args["rowspan"] = rs
                    # if xp:
                    #     args["padx"] = xp
                    # if yp:
                    #     args["pady"] = yp
                    # if ixp:
                    #     args["ipadx"] = ixp
                    # if iyp:
                    #     args["ipady"] = iyp
                    # if st:
                    #     args["sticky"] = st
                    #
                    # widget = widget["widget"]
                    # print(f"gridding widget={widget['widget']}, {r=}, {c=}, {ri=}, {ci=}, {args=}")
                    # widget.grid(row=ri, column=ci, **args)

                    none_count -= (cs - 1)
                    col_count += cs
                    ci += (col_count - 1)
                    r_inner = max(r_inner, (rs - 1))

                    # x, y = 25, 25
                    # widget["widget"].create_text(x, y, text=str(widget))
                    # widget["widget"].create_text(x, y + 10, text=str(ri))
                    # widget["widget"].create_text(x, y + 20, text=str(ci))
                # else:

                ci += none_count

                # self.widgets_added.append((ri, ci, cs, rs))
                print(f"\tIN {ri=}, {ci=}, {rs=}, {cs=}, cc={col_count}, nc={none_count}, {len(self.tiles)=}, {len(self.tiles[ri])=}, {kwargs=}")
                for rii in range(ri, ri + rs):
                    for cii in range(ci, ci + cs):
                        # print(f"{rii=}, {cii=}")
                        self.tiles[rii][cii] = widget
                        self.tile_properties[rii][cii] = kwargs

                widget.grid_forget()
                widget.grid(row=fr, column=fc, **kwargs)
        self.grid_print()

    def grid_print(self):
        print("VVVVVVVVVVVVV")
        for r, row in enumerate(self.tiles):
            m = ""
            for c in row:
                if c:
                    m += f"| {c._name}".center(10)
                else:
                    m += f"|   None  "
            print(f"[{m + '|'}]")
        print("^^^^^^^^^^^^^")

    # def occupied(self, r, c):
    #     if r > self.max_rows:
    #         raise ValueError(f"Error, row {r} is out of range")
    #     if c > self.max_cols:
    #         raise ValueError(f"Error, column {c} is out of range")
    #     return self.tiles[r][c] is not None

    # _row_idx
    def get_row_idx(self):
        return self._row_idx

    def set_row_idx(self, row_idx_in):
        self._row_idx = row_idx_in

    def del_row_idx(self):
        del self._row_idx

    # _max_rows
    def get_max_rows(self):
        return self._max_rows

    def set_max_rows(self, max_rows_in):
        if self.max_rows < max_rows_in:
            for r in range(max_rows_in - self.max_rows):
                self.tiles.append([None for c in range(self.max_cols + 1)])
                self.tile_properties.append([None for c in range(self.max_cols + 1)])
        self._max_rows = max_rows_in

    def del_max_rows(self):
        del self._max_rows

    # _max_cols
    def get_max_cols(self):
        return self._max_cols

    def set_max_cols(self, max_cols_in):
        if self.max_cols < max_cols_in:
            for r, row in enumerate(self.tiles):
                # print(f"\t\t{1 + max_cols_in=}, {len(row)=}, {1 + max_cols_in - len(row)=}")
                for _ in range(1 + max_cols_in - len(row)):
                    self.tiles[r].append(None)
                    self.tile_properties[r].append(None)
        self._max_cols = max_cols_in

    def del_max_cols(self):
        del self._max_cols

    # col_idx = property(get_col_idx, set_col_idx, del_col_idx)
    row_idx = property(get_row_idx, set_row_idx, del_row_idx)
    max_rows = property(get_max_rows, set_max_rows, del_max_rows)
    max_cols = property(get_max_cols, set_max_cols, del_max_cols)


if __name__ == '__main__':

    import tkinter
    from utility import alpha_seq
    from colour_utility import random_colour

    WIN = tkinter.Tk()
    WIN.title("test_grid_manager")
    WIDTH, HEIGHT = 900, 600
    WIN.geometry(f"{WIDTH}x{HEIGHT}")

    n_widgets = 19
    namer = alpha_seq(n_widgets, prefix="frame_", capital_alpha=False)
    grad = rainbow_gradient(n_widgets, rgb=False)
    can_w = 25
    can_h = 25

    widgets_1 = [
        [
            # A, B, C
            tkinter.Canvas(WIN, name=next(namer), background=next(grad), width=can_w, height=can_h),
            tkinter.Canvas(WIN, name=next(namer), background=next(grad), width=can_w, height=can_h),
            tkinter.Canvas(WIN, name=next(namer), background=next(grad), width=can_w, height=can_h)
        ],
        [
            # D
            tkinter.Canvas(WIN, name=next(namer), background=next(grad), width=can_w, height=can_h),
            {
                # E
                "widget":
                    tkinter.Canvas(WIN, name=next(namer), background=next(grad), width=can_w, height=can_h),
                "columnspan": 3,
                "sticky": "ew"
            }
        ],
        [
            {
                # F
                "widget": tkinter.Canvas(WIN, name=next(namer), background=next(grad), width=can_w,
                                         height=can_h),
                "columnspan": 2,
                "rowspan": 2,
                "sticky": "ew"
                # "padx": 45,
                # "pady": 45
            },
            {
                # G
                "widget": tkinter.Canvas(WIN, name=next(namer), background=next(grad), width=can_w,
                                         height=can_h),
                "columnspan": 2,
                "sticky": "ew"
            }
        ],
        [
            # H, I, J
            tkinter.Canvas(WIN, name=next(namer), background=next(grad), width=can_w, height=can_h),
            tkinter.Canvas(WIN, name=next(namer), background=next(grad), width=can_w, height=can_h),
            tkinter.Canvas(WIN, name=next(namer), background=next(grad), width=can_w, height=can_h)
        ],
        [None, None, None,
         # K
         tkinter.Canvas(WIN, name=next(namer), background=next(grad), width=can_w, height=can_h)],
        [None,
         # L
         {"widget": tkinter.Canvas(WIN, name=next(namer), background=next(grad), width=can_w, height=can_h),
          "ipadx": 20, "ipady": 20}]

    ]

    widgets_2 = [
        [
            # M, N, O
            tkinter.Canvas(WIN, name=next(namer), background=next(grad), width=can_w, height=can_h),
            tkinter.Canvas(WIN, name=next(namer), background=next(grad), width=can_w, height=can_h),
            tkinter.Canvas(WIN, name=next(namer), background=next(grad), width=can_w, height=can_h)
        ],
        [
            # P, Q
            tkinter.Canvas(WIN, name=next(namer), background=next(grad), width=can_w, height=can_h),
            tkinter.Canvas(WIN, name=next(namer), background=next(grad), width=can_w, height=can_h)
        ],
        [
            {
                # R
                "widget": tkinter.Canvas(WIN, name=next(namer), background=next(grad), width=can_w,
                                         height=can_h),
                "columnspan": 2
            },
            # S
            tkinter.Canvas(WIN, name=next(namer), background=next(grad), width=can_w, height=can_h)
        ]
    ]

    WIN.grid()
    gm = GridManager(WIN)
    # gm.grid_widgets(widgets_1)
    # gm.grid_widgets(widgets_2)
    gm.grid_widgets()
    gm.grid_widgets(widgets_2)

    # grid_manage_1(widgets_1)
    # grid_manage_1(widgets_2)
    WIN.update()

    # WIN.after(5000, gm.ungrid_widget(0, 0))

    WIN.mainloop()
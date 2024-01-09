import datetime
import math
import os
import random

from utility import *
from colour_utility import *
from fpdf import FPDF
import webbrowser


#######################################################################################################################
#######################################################################################################################
#######################################################################################################################

VERSION = \
    """
        General PDF Creation Class
        Version................1.6
        Date............2023-01-23
        Author........Avery Briggs
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


# MAX_Y = 297
# MAX_X = 210


class PDF(FPDF):

    def __init__(self, file_name, cur_orientation="P", *args, **kwargs):
        super().__init__(cur_orientation, **kwargs)
        self.file_name = file_name

        self.MARGIN_LINES_WIDTH = 3
        self.MARGIN_LINES_MARGIN = 5
        self.TITLE_HEIGHT = 12
        self.TITLE_MARGIN = 15
        self.TABLE_MARGIN = 10
        self.FOOTER_MARGIN = 10
        self.TXT_MARGIN = 10
        self.FILE_NAME = "test.pdf"

        self.time_stamp_rect = (self.w - 100, -15, 0, 10)

        self.cur_orientation = cur_orientation

        if self.cur_orientation == "L":
            self.w = 750
            self.h = 600
        else:
            self.w = 600
            self.h = 750
        self.page_heights = [0]

    def titles(self, title, x, y, w, h, colour, align="C", border=0, font=('Arial', 'B', 16)):
        # self.set_fill_color(*BWS_GREY)
        # self.rect(0, 0, 210, 20, "FD")
        self.set_font(*font)
        self.set_xy(x, y)
        self.set_text_color(*colour)
        self.cell(w=w, h=h, align=align, txt=title, border=border)

    def texts(self, x, y, w, h, name, font=('Arial', '', 12), font_colour=BLACK):
        before = self.get_x(), self.get_y()
        if name in os.listdir():
            with open(name, 'rb') as xy:
                txt = xy.read().decode('latin-1')
        else:
            txt = name
        print("description:", txt[:15])
        print("before: ({}, {})".format(*before))
        self.set_xy(x, y)
        self.set_text_color(*font_colour)
        self.set_font(*font)
        self.multi_cell(w, h, txt, align='J')
        after = self.get_x(), self.get_y()
        print("after: ({}, {})".format(*after))
        print("diff: ({}, {})".format(after[0] - before[0], after[1] - before[1]))
        return after[0] - before[0], after[1] - before[1]

    def add_image(self, name, x, y, w, h, type='', link=''):
        self.image(name, x, y, w, h, type, link)

    def open_in_browser(self):
        webbrowser.open(self.file_name)

    def margin_border(self, border_colour, content_colour, border_width=None):
        if border_width is None:
            border_width = self.MARGIN_LINES_WIDTH
        self.margin_lines(self.MARGIN_LINES_MARGIN, self.MARGIN_LINES_MARGIN, self.w - (2 * self.MARGIN_LINES_MARGIN),
                          self.h - (2 * self.MARGIN_LINES_MARGIN), border_colour, content_colour, border_width)

    def margin_lines(self, x, y, w, h, border_colour, content_colour, border_width=None):
        if border_width is None:
            border_width = self.MARGIN_LINES_WIDTH
        self.set_fill_color(*border_colour)  # color for outer rectangle
        self.rect(x, y, w, h, 'DF')
        self.set_fill_color(*content_colour)  # color for inner rectangle
        self.rect(x + border_width, y + border_width, w - (2 * border_width), h - (2 * border_width), 'FD')

        # self.rect(5.0, 5.0, 200.0, 287.0)

        # self.set_line_width(0.0)
        # self.line(5.0, 5.0, 205.0, 5.0)  # top one
        # self.line(5.0, 292.0, 205.0, 292.0)  # bottom one
        # self.line(5.0, 5.0, 5.0, 292.0)  # left one
        # self.line(205.0, 5.0, 205.0, 292.0)  # right one

    def footer(self):
        old_colour = list(map(lambda colo: int(255 * float(colo.strip())), self.text_color.split(" ")[: -1]))
        self.set_text_color(*BLACK)
        # Go to 1.5 cm from bottom
        self.set_y(-15)
        # Select Arial italic 8
        self.set_font('Arial', 'I', 8)
        # Print centered page number
        self.cell(0, 10, 'Page %s' % self.page_no(), 0, 0, 'C')
        self.set_text_color(*old_colour)

    def preprocess_contents(self, contents):
        print("IN\n", contents)
        if not isinstance(contents, dict) or not dict:
            raise ValueError("Parameter \"contents\" must be a populated dict object.")
        res = {}
        for k, v in contents.items():
            is_list = False
            if not isinstance(v, dict):
                if isinstance(v, list):
                    i = 0
                    for i, col in enumerate(v):
                        if not isinstance(col, dict):
                            break
                        res.update({str(k) + "".join([" " for j in range(i)]): col})
                    if i == len(v) - 1:
                        is_list = True
                        continue
                raise ValueError(
                    "Parameter \"contents\" is not of the correct format.\nNeeds to be a dict of dictionaries")
            if not is_list:
                res.update({k: v})

        print("OUT\n", res)
        return res

    def time_stamp(self, tf=8):
        date = datetime.datetime.now()
        old_colour = list(map(lambda colo: int(255 * float(colo.strip())), self.text_color.split(" ")[: -1]))
        self.set_text_color(*BLACK)
        # Go to 1.5 cm from bottom
        self.set_xy(self.time_stamp_rect[0], self.time_stamp_rect[1])
        # Select Arial italic 8
        self.set_font('Arial', 'I', tf)
        # Print centered page number
        txt = "Prepared: {} at {}".format(
            datetime.datetime.strftime(date, "%Y-%m-%dictionary"),
            datetime.datetime.strftime(date, "%I:%M:%S %p")
        )
        self.cell(self.time_stamp_rect[2], self.time_stamp_rect[3], txt, 0, 0, 'C')
        self.set_text_color(*old_colour)

    # def table(
    #         self,
    #         title,
    #         x,
    #         y,
    #         w,
    #         contents,
    #         desc_txt="",
    #         header_colours=(BLACK, WHITE),
    #         colours=(WHITE, BLACK),
    #         header_height=10,
    #         cell_height=5,
    #         title_v_margin=5,
    #         title_h_margin=5,
    #         title_height=10,
    #         title_colour=BWS_RED,
    #         top_margin=5,
    #         bottom_margin=5,
    #         left_margin=5,
    #         right_margin=5,
    #         line_width=0,
    #         top_link_colours=(WHITE, TEAL),
    #         footer_colours=(BLACK, WHITE),
    #         new_page_for_table=False,
    #         # new_page_for_table=True,
    #         show_row_names=False,
    #         include_top_chart_link=True,
    #         include_top_doc_link=False,
    #         start_with_header=True,
    #         row_name_col_lbl="",
    #         border_colour=BWS_RED,
    #         content_colour=WHITE,
    #         cell_border_style=1,
    #         null_entry="",
    #         col_align=None,
    #         header_font=('Arial', 'B', 14),
    #         cell_font=('Arial', '', 8)
    #         # time_stamp=False
    # ):
    #     contents = self.preprocess_contents(contents)
    #
    #     def add_new_page():
    #         old_colour = list(map(lambda colo: int(255 * float(colo.strip())), self.fill_color.split(" ")[: -1]))
    #         print("\t\t\tADDING NEW PAGE FROM WITHIN")
    #         self.add_page()
    #         # self.margin_lines(MARGIN_LINES_MARGIN, MARGIN_LINES_MARGIN, MAX_X - (2 * MARGIN_LINES_MARGIN),
    #         #                   MAX_Y - (2 * MARGIN_LINES_MARGIN), BWS_RED, WHITE)
    #         self.margin_border(border_colour, content_colour)
    #         self.set_xy(cx, self.MARGIN_LINES_MARGIN + self.MARGIN_LINES_WIDTH + top_margin)
    #         self.set_fill_color(*footer_colours[0])
    #         # self.rect(0, self.h - FOOTER_MARGIN, self.w, FOOTER_MARGIN, 'FD')
    #         self.set_fill_color(*old_colour)
    #
    #     if new_page_for_table:
    #         include_top_doc_link = True
    #
    #     cx = cy = 0
    #
    #     header = []
    #     content_lst = [[]]
    #     title_page = self.page_no()
    #
    #     otx = x + left_margin
    #     oty = y + top_margin
    #     ocx = otx
    #     ocy = oty + line_width + title_v_margin
    #
    #     for i, itms in enumerate(contents):
    #         row = itms
    #         col_vals = contents[row]
    #         if not isinstance(col_vals, list):
    #             col_vals = [col_vals]
    #         print("row:", row, "col_vals:", col_vals)
    #         content_lst.append([])
    #         for col in col_vals:
    #             for head, value in col.items():
    #                 h_names = [h[0] if h else "" for h in header]
    #                 j = lstindex(h_names, head)
    #                 mhv = max(len(str(head)), len(str(value)))
    #                 if j == -1:
    #                     header.append((head, mhv))
    #                     content_lst[0].append(head)
    #                 else:
    #                     header[j] = (head, max(header[j][1], mhv))
    #
    #                 h_names = [h[0] if h else "" for h in header]
    #                 j = lstindex(h_names, head)
    #                 c = len(content_lst[i + 1])
    #                 if 0 < i:
    #                     dictionary = c - j
    #                     # print("i: ", i, "c:", c, "dictionary:", dictionary, "j:", j, "value:", value, "content_list[i]:", content_lst[i + 1])
    #                     if dictionary <= 0:
    #                         content_lst[i + 1] += [None for k in range(abs(dictionary))]
    #                 if j < c:
    #                     content_lst[i + 1][j] = value
    #                 else:
    #                     content_lst[i + 1].append(value)
    #
    #     n_rows = len(contents)
    #     n_cols = len(header)
    #     # table_height = (2 * title_v_margin) + title_height + top_margin + bottom_margin + (
    #     #             n_rows * cell_height) + header_height
    #
    #     # self.set_fill_color(*GREEN_2)
    #     # self.rect(x + table_count, y, w, table_height, "FD")
    #     # table_count += 5
    #
    #     # self.set_fill_color(*BWS_BLACK)
    #
    #     print("before")
    #     print(content_lst)
    #     if show_row_names:
    #         n_cols += 1
    #         header.insert(0, (row_name_col_lbl, 1))
    #         keys = [header[0]] + list(contents.keys())
    #         for i in range(n_rows + 1):
    #             if i == 0:
    #                 content_lst[0].insert(0, header[0][0])
    #             else:
    #                 k = keys[i]
    #                 content_lst[i].insert(0, k)
    #     print("after")
    #     print(content_lst)
    #
    #     for row in content_lst:
    #         row += [None for i in range(max(0, n_cols - len(row)))]
    #
    #     width_canvas = w - (2 * left_margin)
    #     cell_width = width_canvas / n_cols
    #
    #     # self.set_fill_color(*BWS_GREY)
    #     # cch = cell_height + (line_width / 2)
    #     pages = 0
    #     i_off = 0
    #     space_used = 0
    #     page_space_used = 0
    #     # print("ocy:", ocy, "height_canvas:", height_canvas, "self.h:", self.h)
    #
    #     dth = 0 if desc_txt is None else 40
    #     print("\t\tTITLE", title)
    #     print("self.get_y() + title_height + (5 * title_v_margin) + dth + (2 * top_margin):",
    #           (self.get_y() + title_height + (5 * title_v_margin) + dth + (2 * top_margin)))
    #     if new_page_for_table or (
    #             self.get_y() + title_height + (5 * title_v_margin) + dth + (2 * top_margin)) >= self.h:
    #         print("\tNew page to start the chart. new_page_for_table={}".format(new_page_for_table))
    #         add_new_page()
    #         page_left = self.h
    #         pages += 1
    #         # i_off += i
    #         page_space_used += space_used
    #         space_used = 0
    #         ocy = 0
    #         oty = 0
    #         title_page = self.page_no()
    #
    #     # Begin Writing to page
    #
    #     self.line(otx - left_margin, oty + (title_v_margin / 2) + top_margin - 2, otx - left_margin + w,
    #               oty + (title_v_margin / 2) + top_margin - 2)
    #     self.titles(title, otx - left_margin, oty + (title_v_margin / 2) + top_margin, w,
    #                 title_height, title_colour)
    #
    #     ocy += title_height + title_v_margin
    #
    #     x_txt = y_txt = 0
    #     if desc_txt:
    #         y_txt = oty + (title_v_margin / 2) + top_margin + title_height + title_v_margin
    #         x_txt, y_txt = self.texts(otx, y_txt, 0, 5, desc_txt)
    #         ocy += y_txt
    #     print("y_txt:", y_txt, "oty + (title_v_margin / 2) + top_margin:", (oty + (title_v_margin / 2) + top_margin),
    #           "title_height:", title_height, "oty + (title_v_margin / 2) + top_margin + title_height",
    #           oty + (title_v_margin / 2) + top_margin + title_height)
    #
    #     off = 0
    #     i = 0
    #     rh = 0
    #     self.set_xy(ocx, ocy)
    #     while i in range(n_rows + 1):
    #
    #         if i == 0:
    #             self.set_font(*header_font)
    #             self.set_fill_color(*header_colours[0])
    #             self.set_text_color(*header_colours[1])
    #             ch = header_height
    #         else:
    #             self.set_font(*cell_font)
    #             fill_colour = colours[0][(i - 1) % len(colours[0])]
    #             font_colour = colours[1][(i - 1) % len(colours[1])]
    #             self.set_fill_color(*fill_colour)
    #             self.set_text_color(*font_colour)
    #             ch = cell_height
    #
    #         def row_height():
    #             self.set_font(*cell_font)
    #             """
    #             # print("self.get_string_width(str(content_lst[i][4]).strip():", self.get_string_width(str(content_lst[i][4]).strip()), "content_lst[i][4]):", content_lst[i][4])
    #             # print("max([]):", (max(
    #             #     [self.get_string_width(str(content_lst[i][q]).strip() if content_lst[i][q] is not None else null_entry) for q in range(n_cols)]
    #             # )))
    #             # print("max([]) / cell_width:", (max([self.get_string_width(str(content_lst[i][q]).strip() if content_lst[i][q] is not None else null_entry) for q in range(n_cols)]) / cell_width))
    #             # print("[math.ceil(self.get_string_width(str(content_lst[i][q]).strip() if content_lst[i][q] is not None else null_entry) / cell_width) for q in range(n_cols)]\n\t", [math.ceil(self.get_string_width(str(content_lst[i][q]).strip() if content_lst[i][q] is not None else null_entry) / cell_width) for q in range(n_cols)])
    #             # print("max([ceil(string_w(str(c_lst[i={i}][q]).strip() if c_lst[i={i}][q] is not None else null_entry) / cell_width) for q in range(n_cols={nc})]): {r}".format(i=i, nc=n_cols, r=(max([math.ceil(self.get_string_width(str(content_lst[i][q]).strip() if content_lst[i][q] is not None else null_entry) / cell_width) for q in range(n_cols)]))))
    #             # return max([math.ceil(self.get_string_width(str(content_lst[i][q]).strip() if content_lst[i][q] is not None else null_entry) / cell_width) for q in range(n_cols)])
    #             """
    #             """
    #             res = 0
    #             for q in range(n_cols):
    #                 ct = str(content_lst[i][q])#.strip()
    #                 sct = math.ceil(self.get_string_width(ct))
    #                 cww = math.floor(cell_width - 4.55)
    #                 sctd = self.get_string_width(str(content_lst[i][q]).strip() if content_lst[i][q] is not None else null_entry) / cww
    #                 csctd = math.ceil(sctd)
    #
    #                 sp_splt = ct.split(" ")
    #                 line = ""
    #                 line_c = 1
    #                 for ij, word in enumerate(sp_splt):
    #                     spf = "" if ij == 0 else " "
    #                     spe = "" if ij == n_cols - 1 else " "
    #                     line += spf + word.strip()
    #                     ln = line + spe
    #                     print("line ({}) ({}): <{}> math.ceil(math.ceil(self.get_string_width(ln)) / cww): {}".format(len(ln), math.ceil(self.get_string_width(ln)), ln, (math.ceil(math.ceil(self.get_string_width(ln)) / cww))))
    #                     if math.ceil(math.ceil(self.get_string_width(ln)) / cww) > 1:
    #                         print("\tBREAK line ({}) ({}): <{}>".format(len(ln), self.get_string_width(ln), ln))
    #                         line_c += 1
    #                         line = ""
    #
    #                 res = max(res, line_c - csctd)
    #
    #                 res = max(res, csctd)
    #                 print(dict_print({"ct": ct, "ch": ch, "sct": sct, "cww": cww, "sctd": sctd, "csctd": csctd, "line_C": line_c, "res": res}, "Calculated values"))
    #             return res
    #             """
    #
    #             res = 0
    #             for q in range(n_cols):
    #                 ct = str(content_lst[i][q])  # .strip()
    #                 sct = math.ceil(self.get_string_width(ct))
    #                 cww = math.floor(cell_width - 5)
    #                 sctd = self.get_string_width(
    #                     str(content_lst[i][q]).strip() if content_lst[i][q] is not None else null_entry) / cww
    #                 csctd = math.ceil(sctd)
    #
    #                 sp_splt = ct.split(" ")
    #                 line = ""
    #                 line_c = 1
    #                 for ij, word in enumerate(sp_splt):
    #                     spf = "" if ij == 0 else " "
    #                     spe = "" if ij == n_cols - 1 else " "
    #                     line += spf + word.strip()
    #                     ln = line + spe
    #                     if ij < len(sp_splt) - 1:
    #                         next_word = sp_splt[ij + 1]
    #                         if self.get_string_width(ln + next_word) >= cww:
    #                             print("\tBREAK line ({}) ({}): <{}>".format(len(ln), self.get_string_width(ln), ln))
    #                             line_c += 1
    #                             line = ""
    #                             ln = ""
    #                 res = max(res, line_c)
    #                 # if res:
    #                 # print()
    #             res = max(1, res - 1)
    #             # if res > 1:
    #             #     res -= 1
    #             return res
    #
    #         trh = row_height()
    #         rh += trh - 1
    #         print("trh:", trh)
    #         och = ch
    #         ch = max(ch, ch * (trh - 1))
    #
    #         # cy = ocy + (((i + rh - pages) * cell_height) + (((1 if pages else 0) + off) * header_height) + max(0, ((1 if i else 0) * header_height) - 5)) - (
    #         #         1 * page_space_used) + FOOTER_MARGIN + top_margin + title_v_margin
    #         # print("\tself.get_y():", self.get_y(), "ch:", ch, "self.h:", self.h, "(self.get_y() + ch):", (self.get_y() + ch), "(self.get_y() + ch) >= self.h:", (self.get_y() + ch) >= self.h)
    #         # print("\tcy:", cy, "ch:", ch, "self.h:", self.h, "(cy + ch):", (cy + ch), "(cy + ch) >= self.h:", ((cy + ch) >= self.h))
    #         # print("\t\t(self.get_y() + max(cell_height, header_height)):", (self.get_y() + max(cell_height, header_height)), "\n\t\tself.h - (2 * (MARGIN_LINES_WIDTH + MARGIN_LINES_MARGIN + title_v_margin)) - title_height:", (self.h - (2 * (MARGIN_LINES_WIDTH + MARGIN_LINES_MARGIN + title_v_margin)) - title_height), "\n\t\t(self.get_y() + max(cell_height, header_height)) >= self.h - (2 * (MARGIN_LINES_WIDTH + MARGIN_LINES_MARGIN + title_v_margin)) - title_height:", (self.get_y() + max(cell_height, header_height)) >= (self.h - (2 * (MARGIN_LINES_WIDTH + MARGIN_LINES_MARGIN + title_v_margin)) - title_height))
    #         np = False
    #         if i == 0:
    #             if (self.get_y() + max(cell_height, header_height, (max(0, (trh)) * och))) >= self.h - (
    #                     2 * (self.MARGIN_LINES_WIDTH + self.MARGIN_LINES_MARGIN + title_v_margin)) - title_height - y_txt:
    #                 np = True
    #         elif (self.get_y() + max(cell_height, header_height, (max(0, (trh)) * och))) >= self.h - (
    #                 2 * (self.MARGIN_LINES_WIDTH + self.MARGIN_LINES_MARGIN)):
    #             np = True
    #
    #         if np:
    #             add_new_page()
    #             page_left = self.h
    #             pages += 1
    #             print("\tpage break on line i={}, start next page with header: {}".format(i, start_with_header))
    #             i_off += i
    #             page_space_used += space_used
    #             space_used = 0
    #             ocy = 0
    #
    #         space_used += ch + (max(0, (trh - 2)) * och)
    #         j = 0
    #         cy = self.get_y()  # - (max(0, trh - 2) * och)
    #         wo_10015162 = False
    #         m_c_y = cy
    #         while j in range(n_cols):
    #             if start_with_header and np:
    #                 cell_value = str(content_lst[0][j]).strip() if content_lst[0][j] is not None else null_entry
    #                 print("cv:", cell_value)
    #                 self.set_font('Arial', 'B', 14)
    #                 self.set_fill_color(*header_colours[0])
    #                 self.set_text_color(*header_colours[1])
    #                 ch = header_height
    #             else:
    #                 cell_value = str(content_lst[i][j]).strip() if content_lst[i][j] is not None else null_entry
    #             cw = cell_width + (line_width / 2)
    #             cx = ocx + (j * cw)
    #             # cy = ocy + (((i - i_off) * ch) + max(0, ((1 if i else 0) * cch) - 5)) - (pages * height_canvas)
    #             # cy = self.get_y()#ocy + (((i + rh - pages) * cell_height) + (((1 if (start_with_header and np) else 1) + off) * header_height) + max(0, ((1 if i else 0) * header_height) - 5)) - (
    #             #   1 * page_space_used) + FOOTER_MARGIN + top_margin + title_v_margin
    #             # if rh:
    #             #     cy -= cell_height
    #             # print(
    #             #     "pages: {} i: {} j: {} cx: {} cy: {}, self.get_y: {} cv: {} su: {} psu: {}".format(pages, i, j, cx,
    #             #                                                                                        cy,
    #             #                                                                                        self.get_y(),
    #             #                                                                                        cell_value,
    #             #                                                                                        space_used,
    #             #                                                                                        page_space_used))
    #             # self.rect(cx, cy, cell_width, ch, 'DF')
    #             # self.texts(cx + (cw / 2), cy + (ch / 2), cell_value)
    #             # self.texts(cx, cy, cell_value)
    #             if cy >= self.h:
    #                 raise ValueError("cy {} is too high".format(cy))
    #             h_align = "C"
    #             if isinstance(col_align, list):
    #                 if j < len(col_align):
    #                     h_align = col_align[j]
    #             elif isinstance(col_align, dict):
    #                 col_name = header[j][0]
    #                 # print("\t\tcol_name:", col_name)
    #                 if col_name in col_align:
    #                     h_align = col_align[col_name]
    #
    #             self.set_xy(cx, cy)
    #             # self.cell(cell_width, ch, cell_value, cell_border_style, 1, h_align, fill=1)
    #             if trh - 1:
    #                 bs = "F" + ("" if not cell_border_style else "D")
    #                 # old_colo = list(map(lambda abc: int(255 * float(abc.strip())), self.fill_color.split(" ")[:3]))
    #                 # print("old_colo:", old_colo)
    #                 # self.set_fill_color(*TURQUOISE)
    #                 w_off = 1
    #                 # self.rect(cx - w_off, cy, cell_width + (2 * w_off), (max(0, (trh)) * och), bs)
    #                 # self.set_fill_color(*old_colo)
    #             bef = self.get_y()
    #             self.multi_cell(w=cell_width, h=och, txt=cell_value[:300], border=cell_border_style, h_align=h_align,
    #                             fill=1)
    #             aft = self.get_y()
    #             m_c_y = max(m_c_y, self.get_y(), max(0, (trh if trh > 1 else 0)) * och)
    #             # x, y, name, font=('Arial', '', 12), font_colour=BLACK
    #             j += 1
    #             print(
    #                 "page: {}\n\t(i, j): ({}, {})\n\t(cx, cy): ({}, {})\n\tself.get_y: {}\n\tcv: {} su: {} psu: {}\n\t(aft, bef): ({}, {})\n\ttrh: {}\n\tm_c_y: {}".format(
    #                     pages, i, j, cx,
    #                     cy,
    #                     self.get_y(),
    #                     cell_value,
    #                     space_used,
    #                     page_space_used, aft, bef, trh, m_c_y))
    #
    #             if cell_value == "10015162":
    #                 wo_10015162 = True
    #
    #         if start_with_header and np:
    #             i -= 1
    #             off += 1
    #         i += 1
    #         print("\t\tcy:", cy, "\n\t\tself.get_y()", self.get_y())
    #         # self.set_y(cy + och + (max(0, (trh if trh > 1 else 0)) * och))
    #         self.set_y(m_c_y)
    #         # if wo_10015162:
    #         #     raise ValueError("Hey ")
    #
    #     # self.rect(x, y, w, height_canvas, 'FD')
    #
    #     y_link = self.get_y() + title_v_margin
    #     if include_top_chart_link:
    #         self.set_fill_color(*top_link_colours[0])
    #         self.set_text_color(*top_link_colours[1])
    #         self.set_xy(ocx + width_canvas - 30, y_link)
    #         self.cell(30, 5, "Top of Chart", 1, 1, 'C', fill=1,
    #                   link=("{}/{}#page={}".format(os.getcwd(), self.file_name, title_page)))
    #
    #     if include_top_doc_link:
    #         self.set_fill_color(*top_link_colours[0])
    #         self.set_text_color(*top_link_colours[1])
    #         self.set_xy(ocx + width_canvas - 65, y_link)
    #         self.cell(30, 5, "Top of Document", 1, 1, 'C', fill=1,
    #                   link=("{}/{}#page={}".format(os.getcwd(), self.file_name, 1)))
    #
    #     # if time_stamp:
    #     #     self.time_stamp()
    #
    #     # self.line(otx - left_margin, self.get_y() + title_v_margin + 2, otx - left_margin + w, self.get_y() + title_v_margin + 2)
    #     # self.link(ocx, self.get_y() + title_v_margin, 30, 30, FILE_NAME + "#page={}".format(title_page))
    #     print("self.w:", self.w, "width_canvas:", width_canvas)
    #     print("header:", header)
    #     # print("\n##\n" + "\n".join(list(map(str, content_lst))) + "\n##\n")
    #     print("(N x M): ({} x {})".format(n_rows, n_cols))
    #     # print("(H x W): ({} x {})".format(height_canvas, width_canvas))
    #     print("(CH x CW): ({} x {})".format(cell_height, cell_width))
    #
    #     return cx, cy

    def table(
            self,
            title,
            x,
            y,
            w,
            contents,
            desc_txt="",
            header_colours=(BLACK, WHITE),
            colours=((WHITE, BLACK), (BLACK, WHITE)),
            header_height=10,
            cell_height=5,
            title_v_margin=5,
            title_h_margin=5,
            title_height=10,
            title_colour=BWS_RED,
            top_margin=8,
            bottom_margin=8,
            left_margin=8,
            right_margin=8,
            line_width=0,
            top_link_colours=(WHITE, TEAL),
            footer_colours=(BLACK, WHITE),
            new_page_for_table=False,
            # new_page_for_table=True,
            show_row_names=False,
            include_top_chart_link=True,
            include_top_doc_link=False,
            start_with_header=True,
            row_name_col_lbl="",
            border_colour=BWS_RED,
            content_colour=WHITE,
            cell_border_style=1,
            null_entry="",
            col_align=None,
            header_font=('Arial', 'B', 14),
            cell_font=('Arial', '', 10)
            # time_stamp=False
    ):
        contents = self.preprocess_contents(contents)

        def add_new_page():
            old_colour = list(map(lambda colo: int(255 * float(colo.strip())), self.fill_color.split(" ")[: -1]))
            self.add_page()
            print("\t\t\tADDING NEW PAGE FROM WITHIN", self.page_no())
            # self.margin_lines(MARGIN_LINES_MARGIN, MARGIN_LINES_MARGIN, MAX_X - (2 * MARGIN_LINES_MARGIN),
            #                   MAX_Y - (2 * MARGIN_LINES_MARGIN), BWS_RED, WHITE)
            self.margin_border(border_colour, content_colour)
            self.set_xy(cx, self.MARGIN_LINES_MARGIN + self.MARGIN_LINES_WIDTH + top_margin)
            self.set_fill_color(*footer_colours[0])
            # self.rect(0, self.h - FOOTER_MARGIN, self.w, FOOTER_MARGIN, 'FD')
            self.set_fill_color(*old_colour)

        if new_page_for_table:
            include_top_doc_link = True

        cx = cy = 0

        header = []
        content_lst = [[]]
        title_page = self.page_no()

        otx = x + left_margin
        oty = y + top_margin
        ocx = otx + (left_margin / 2)
        ocy = oty + line_width + title_v_margin

        for i, itms in enumerate(contents):
            row = itms
            col_vals = contents[row]
            if not isinstance(col_vals, list):
                col_vals = [col_vals]
            print("row:", row, "col_vals:", col_vals)
            content_lst.append([])
            for col in col_vals:
                for head, value in col.items():
                    h_names = [h[0] if h else "" for h in header]
                    j = lstindex(h_names, head)
                    mhv = max(len(str(head)), len(str(value)))
                    if j == -1:
                        header.append((head, mhv))
                        content_lst[0].append(head)
                    else:
                        header[j] = (head, max(header[j][1], mhv))

                    h_names = [h[0] if h else "" for h in header]
                    j = lstindex(h_names, head)
                    c = len(content_lst[i + 1])
                    if 0 < i:
                        d = c - j
                        # print("i: ", i, "c:", c, "dictionary:", dictionary, "j:", j, "value:", value, "content_list[i]:", content_lst[i + 1])
                        if d <= 0:
                            content_lst[i + 1] += [None for k in range(abs(d))]
                    if j < c:
                        content_lst[i + 1][j] = value
                    else:
                        content_lst[i + 1].append(value)

        n_rows = len(contents)
        n_cols = len(header)
        # table_height = (2 * title_v_margin) + title_height + top_margin + bottom_margin + (
        #             n_rows * cell_height) + header_height

        # self.set_fill_color(*GREEN_2)
        # self.rect(x + table_count, y, w, table_height, "FD")
        # table_count += 5

        # self.set_fill_color(*BWS_BLACK)

        print("before")
        print(content_lst)
        if show_row_names:
            n_cols += 1
            header.insert(0, (row_name_col_lbl, 1))
            keys = [header[0]] + list(contents.keys())
            for i in range(n_rows + 1):
                if i == 0:
                    content_lst[0].insert(0, header[0][0])
                else:
                    k = keys[i]
                    content_lst[i].insert(0, k)
        print("after")
        print(content_lst)

        for row in content_lst:
            row += [None for i in range(max(0, n_cols - len(row)))]

        width = w - (2 * left_margin)
        cell_width = width / n_cols

        # self.set_fill_color(*BWS_GREY)
        # cch = cell_height + (line_width / 2)
        pages = 0
        i_off = 0
        space_used = 0
        page_space_used = 0
        # print("ocy:", ocy, "height_canvas:", height_canvas, "self.h:", self.h)

        dth = 0 if desc_txt is None else 40
        print("\t\tTITLE", title)
        print("self.get_y() + title_height + (3 * title_v_margin) + (0 * top_margin):",
              (self.get_y() + title_height + (1 * title_v_margin) + (0 * top_margin)))
        print("title_height:", title_height)
        print("title_v_margin:", title_v_margin)
        print("top_margin:", top_margin)
        print("self.h:", self.h, "self.get_y():", self.get_y())
        # if new_page_for_table or (
        #         self.get_y() + title_height + (5 * title_v_margin) + dth + (2 * top_margin)) >= self.h:
        if new_page_for_table or (
                self.get_y() + title_height + (1 * title_v_margin) + (0 * top_margin)) > self.h:
            print("\tNew page to start the chart. new_page_for_table={}".format(new_page_for_table))
            add_new_page()
            page_left = self.h
            pages += 1
            # i_off += i
            page_space_used += space_used
            space_used = 0
            ocy = 0
            oty = 0
            title_page = self.page_no()

        # Begin Writing to page

        # self.line(otx - left_margin, oty + (title_v_margin / 2) + top_margin - 2, otx - left_margin + w,
        #           oty + (title_v_margin / 2) + top_margin - 2)
        # self.titles(title, otx - left_margin, oty + (title_v_margin / 2) + top_margin, w,
        #             title_height, title_colour)

        self.line(otx + (left_margin / 2), oty + (title_v_margin / 2) + top_margin - 2, otx + w - left_margin,
                  oty + (title_v_margin / 2) + top_margin - 2)
        self.titles(title, otx + (left_margin / 2), oty + (title_v_margin / 2) + top_margin - 10, w,
                    title_height, title_colour)
        self.set_y(oty + (title_v_margin / 2) + top_margin - 10 + title_height)

        x_txt = y_txt = 0
        if desc_txt:
            y_txt = oty + (title_v_margin / 2) + top_margin + title_height + title_v_margin
            x_txt, y_txt = self.texts(otx, y_txt, 0, 5, desc_txt)
            ocy += y_txt
        print("y_txt:", y_txt, "oty + (title_v_margin / 2) + top_margin:", (oty + (title_v_margin / 2) + top_margin),
              "title_height:", title_height, "oty + (title_v_margin / 2) + top_margin + title_height",
              oty + (title_v_margin / 2) + top_margin + title_height)

        off = 0
        i = 0
        rh = 0
        while i in range(n_rows + 1):

            if i == 0:
                self.set_font(*header_font)
                self.set_fill_color(*header_colours[0])
                self.set_text_color(*header_colours[1])
                ch = header_height
            else:
                self.set_font(*cell_font)
                print(f"{colours=}")
                # fill_colour = colours[0][(i - 1) % len(colours[0])]
                # font_colour = colours[1][(i - 1) % len(colours[1])]
                fill_colour = colours[0][(i - 1) % len(colours[0])]
                font_colour = colours[1][(i - 1) % len(colours[1])]
                print(f"{fill_colour=}, {font_colour=}")
                self.set_fill_color(*fill_colour)
                self.set_text_color(*font_colour)
                ch = cell_height

            def row_height():
                self.set_font(*cell_font)
                # if i == 0:
                #     cv = max([self.get_string_width(str(content_lst[0][j]).strip() if content_lst[0][j] is not None else null_entry)])
                # else:
                #     cv = str(content_lst[i][j]).strip() if content_lst[i][j] is not None else null_entry
                # print("content_lst[i]:", content_lst[i])
                # print("self.get_string_width(str(content_lst[i][4]).strip():",
                #       self.get_string_width(str(content_lst[i][4]).strip()), "content_lst[i][4]):", content_lst[i][4])
                print("max([]):", (max(
                    [self.get_string_width(
                        str(content_lst[i][q]).strip() if content_lst[i][q] is not None else null_entry) for q in
                        range(n_cols)]
                )))
                print("max([]) / cell_width:", (max([self.get_string_width(
                    str(content_lst[i][q]).strip() if content_lst[i][q] is not None else null_entry) for q in
                    range(n_cols)]) / cell_width))
                return max([math.ceil(self.get_string_width(
                    str(content_lst[i][q]).strip() if content_lst[i][q] is not None else null_entry) / cell_width) for q
                            in range(n_cols)])
                # if i == 0:
                #     return math.ceil(max([self.get_string_width(str(content_lst[0][q]).strip() if content_lst[0][q] is not None else null_entry) for q in range(n_cols)]) / cell_width)
                # else:
                #     return math.ceil(max([self.get_string_width(
                #         str(content_lst[i][q]).strip() if content_lst[i][q] is not None else null_entry) for q in
                #                           range(n_cols)]) / cell_width)

            trh = row_height()
            rh += trh - 1
            print("trh:", trh)
            och = ch
            ch = max(ch, ch * (trh - 1))

            # cy = ocy + (((i + rh - pages) * cell_height) + (((1 if pages else 0) + off) * header_height) + max(0, ((1 if i else 0) * header_height) - 5)) - (
            #         1 * page_space_used) + FOOTER_MARGIN + top_margin + title_v_margin
            # print("\tself.get_y():", self.get_y(), "ch:", ch, "self.h:", self.h, "(self.get_y() + ch):", (self.get_y() + ch), "(self.get_y() + ch) >= self.h:", (self.get_y() + ch) >= self.h)
            # print("\tcy:", cy, "ch:", ch, "self.h:", self.h, "(cy + ch):", (cy + ch), "(cy + ch) >= self.h:", ((cy + ch) >= self.h))
            # print("\t\t(self.get_y() + max(cell_height, header_height)):", (self.get_y() + max(cell_height, header_height)), "\n\t\tself.h - (2 * (MARGIN_LINES_WIDTH + MARGIN_LINES_MARGIN + title_v_margin)) - title_height:", (self.h - (2 * (MARGIN_LINES_WIDTH + MARGIN_LINES_MARGIN + title_v_margin)) - title_height), "\n\t\t(self.get_y() + max(cell_height, header_height)) >= self.h - (2 * (MARGIN_LINES_WIDTH + MARGIN_LINES_MARGIN + title_v_margin)) - title_height:", (self.get_y() + max(cell_height, header_height)) >= (self.h - (2 * (MARGIN_LINES_WIDTH + MARGIN_LINES_MARGIN + title_v_margin)) - title_height))
            np = False
            if i == 0:
                if (self.get_y() + max(cell_height, header_height, (max(0, (trh)) * och))) >= self.h - (
                        2 * (self.MARGIN_LINES_WIDTH + self.MARGIN_LINES_MARGIN + title_v_margin)) - title_height - y_txt:
                    np = True
            elif (self.get_y() + max(cell_height, header_height, (max(0, (trh)) * och))) >= self.h - (
                    2 * (self.MARGIN_LINES_WIDTH + self.MARGIN_LINES_MARGIN)):
                np = True

            if np:
                add_new_page()
                page_left = self.h
                pages += 1
                print("\tpage break on line i={}, start next page with header: {}".format(i, start_with_header))
                i_off += i
                page_space_used += space_used
                space_used = 0
                ocy = 0

            space_used += ch + (max(0, (trh - 2)) * och)
            j = 0
            cy = self.get_y()  # - (max(0, trh - 2) * och)
            wo_10015162 = False
            m_c_y = cy
            while j in range(n_cols):
                if start_with_header and np:
                    cell_value = str(content_lst[0][j]).strip() if content_lst[0][j] is not None else null_entry
                    print("cv:", cell_value)
                    self.set_font('Arial', 'B', 14)
                    self.set_fill_color(*header_colours[0])
                    self.set_text_color(*header_colours[1])
                    ch = header_height
                else:
                    cell_value = str(content_lst[i][j]).strip() if content_lst[i][j] is not None else null_entry
                cw = cell_width + (line_width / 2)
                cx = ocx + (j * cw)
                # cy = ocy + (((i - i_off) * ch) + max(0, ((1 if i else 0) * cch) - 5)) - (pages * height_canvas)
                # cy = self.get_y()#ocy + (((i + rh - pages) * cell_height) + (((1 if (start_with_header and np) else 1) + off) * header_height) + max(0, ((1 if i else 0) * header_height) - 5)) - (
                #   1 * page_space_used) + FOOTER_MARGIN + top_margin + title_v_margin
                # if rh:
                #     cy -= cell_height
                # print(
                #     "pages: {} i: {} j: {} cx: {} cy: {}, self.get_y: {} cv: {} su: {} psu: {}".format(pages, i, j, cx,
                #                                                                                        cy,
                #                                                                                        self.get_y(),
                #                                                                                        cell_value,
                #                                                                                        space_used,
                #                                                                                        page_space_used))
                # self.rect(cx, cy, cell_width, ch, 'DF')
                # self.texts(cx + (cw / 2), cy + (ch / 2), cell_value)
                # self.texts(cx, cy, cell_value)
                if cy >= self.h:
                    raise ValueError("cy {} is too high".format(cy))
                align = "C"
                if isinstance(col_align, list):
                    if j < len(col_align):
                        align = col_align[j]
                elif isinstance(col_align, dict):
                    col_name = header[j][0]
                    # print("\t\tcol_name:", col_name)
                    if col_name in col_align:
                        align = col_align[col_name]

                self.set_xy(cx, cy)
                # self.cell(cell_width, ch, cell_value, cell_border_style, 1, h_align, fill=1)
                if trh - 1:
                    bs = "F" + ("" if not cell_border_style else "D")
                    # old_colo = list(map(lambda abc: int(255 * float(abc.strip())), self.fill_color.split(" ")[:3]))
                    # print("old_colo:", old_colo)
                    # self.set_fill_color(*TURQUOISE)
                    w_off = 1
                    # self.rect(cx - w_off, cy, cell_width + (2 * w_off), (max(0, (trh)) * och), bs)
                    # self.set_fill_color(*old_colo)
                bef = self.get_y()
                self.multi_cell(w=cell_width, h=och, txt=cell_value[:300], border=cell_border_style, align=align,
                                fill=1)
                aft = self.get_y()
                m_c_y = max(m_c_y, self.get_y(), max(0, (trh if trh > 1 else 0)) * och)
                # x, y, name, font=('Arial', '', 12), font_colour=BLACK
                j += 1
                print(
                    "page: {}\n\t(i, j): ({}, {})\n\t(cx, cy): ({}, {})\n\tself.get_y: {}\n\tcv: {} su: {} psu: {}\n\t(aft, bef): ({}, {})\n\ttrh: {}\n\tm_c_y: {}".format(
                        pages, i, j, cx,
                        cy,
                        self.get_y(),
                        cell_value,
                        space_used,
                        page_space_used, aft, bef, trh, m_c_y))

                if cell_value == "10015162":
                    wo_10015162 = True

            if start_with_header and np:
                i -= 1
                off += 1
            i += 1
            print("\t\tcy:", cy, "\n\t\tself.get_y()", self.get_y())
            # self.set_y(cy + och + (max(0, (trh if trh > 1 else 0)) * och))
            self.set_y(m_c_y)
            # if wo_10015162:
            #     raise ValueError("Hey ")

        # self.rect(x, y, w, height_canvas, 'FD')

        y_link = self.get_y() + title_v_margin
        if include_top_chart_link:
            self.set_fill_color(*top_link_colours[0])
            self.set_text_color(*top_link_colours[1])
            self.set_xy(ocx + width - 60, y_link)
            rect_ts = Rect2(*self.time_stamp_rect)
            # rect_ts initially has width_canvas 0
            rect_ts.init(rect_ts.x, self.h + rect_ts.y, 30, rect_ts.h, rect_ts.a)
            rect_tl = Rect2(self.get_x(), self.get_y(), 30, 10)
            print("rect_ts", rect_ts)
            print("rect_tl", rect_tl)
            inter = rect_ts.collide_rect(rect_tl)
            # If li
            if inter:
                self.set_xy(ocx + width - 100, y_link)
            print("inter:", inter)
            self.cell(30, 5, "Top of Chart", 1, 1, 'C', fill=1,
                      link=("{}/{}#page={}".format(os.getcwd(), self.file_name, title_page)))

        if include_top_doc_link:
            self.set_fill_color(*top_link_colours[0])
            self.set_text_color(*top_link_colours[1])
            self.set_xy(ocx + width - 65, y_link)
            self.cell(30, 5, "Top of Document", 1, 1, 'C', fill=1,
                      link=("{}/{}#page={}".format(os.getcwd(), self.file_name, 1)))

        # if time_stamp:
        #     self.time_stamp()

        # self.line(otx - left_margin, self.get_y() + title_v_margin + 2, otx - left_margin + w, self.get_y() + title_v_margin + 2)
        # self.link(ocx, self.get_y() + title_v_margin, 30, 30, FILE_NAME + "#page={}".format(title_page))
        print("self.w:", self.w, "width_canvas:", width)
        print("header:", header)
        # print("\n##\n" + "\n".join(list(map(str, content_lst))) + "\n##\n")
        print("(N x M): ({} x {})".format(n_rows, n_cols))
        # print("(H x W): ({} x {})".format(height_canvas, width_canvas))
        print("(CH x CW): ({} x {})".format(cell_height, cell_width))

        return cx, cy


def random_test_set(n, start=0, end=None, step=1):
    step = max(1, step)
    if end is None:
        end = start + (n * step)
    if end < start:
        start, end = end, start
    if start + (n * step) != end:
        end = start + (n * step)
    r_keys = ["a", "b", "c", "dictionary", "e"]

    def random_test_entry(m):
        return {choice(r_keys): int(round(random_in_range(1, 101))) for i in range(m)}

    return {i: random_test_entry(choice(list(range(5)))) for i in range(start, end, step)}


if __name__ == "__main__":
    FILE_NAME = "test.pdf"
    pdf = PDF(FILE_NAME, 'L', 'mm', (600, 750))
    pdf.set_auto_page_break(True, margin=5)
    pdf.set_title("Dealer Delivery Reports")
    pdf.set_author('Avery Briggs')
    pdf.add_page()
    pdf.margin_border(BWS_RED, WHITE)
    pdf.time_stamp()
    pdf.output(FILE_NAME, 'F')
    pdf.open_in_browser()

    # pdf.margin_lines(MARGIN_LINES_MARGIN, MARGIN_LINES_MARGIN, MAX_X - (2 * MARGIN_LINES_MARGIN),
    #                  MAX_Y - (2 * MARGIN_LINES_MARGIN), BWS_RED, WHITE)
    # pdf.titles("Dealer Delivery Reports", MARGIN_LINES_WIDTH + MARGIN_LINES_MARGIN,
    #            TITLE_MARGIN + MARGIN_LINES_WIDTH + MARGIN_LINES_MARGIN,
    #            MAX_X - (2 * (MARGIN_LINES_WIDTH + MARGIN_LINES_MARGIN)), TITLE_HEIGHT, BWS_BLACK)
    #
    # date = datetime.datetime.now()
    # pdf.texts(
    #     MARGIN_LINES_WIDTH + MARGIN_LINES_MARGIN + TXT_MARGIN,
    #     TABLE_MARGIN + MARGIN_LINES_WIDTH + TITLE_HEIGHT + TITLE_MARGIN,
    #     0,
    #     10,
    #     "Prepared at {} on {}".format(
    #         datetime.datetime.strftime(date, "%I:%M:%S %p"),
    #         datetime.datetime.strftime(date, "%Y-%m-%dictionary")
    #     ),
    #     font=('Arial', '', 10)
    # )
    #
    # # TABLE_X = 5 + MARGIN_LINES_WIDTH + TABLE_MARGIN
    # # TABLE_Y = 10 + MARGIN_LINES_WIDTH + TABLE_MARGIN
    # TABLE_W = (MAX_X - (2 * (MARGIN_LINES_WIDTH + MARGIN_LINES_MARGIN)) - (2 * TABLE_MARGIN))
    # # TABLE_H = 200 - (2 * (MARGIN_LINES_WIDTH + TABLE_MARGIN))
    #
    # contents_1 = {
    #     1: {"a": 1, "b": 2, "c": 1},
    #     2: {"a": 2, "b": 563, "c": 2, "dictionary": 15},
    #     3: {"a": 3, "b": 3, "c": 3, "dictionary": 5},
    #     4: {"a": 4, "b": 4, "c": 4, "dictionary": 5},
    #     5: {"c": 44, "dictionary": 6},
    #     8: {"b": "Really lo", "dictionary": 54566678898, "a": "This stri"},
    #     6: {"e": 2},
    #     9: {"e": 22},
    #     10: {"dictionary": 24},
    #     11: {"b": 16},
    #     7: {"e": 21, "dictionary": 5, "a": 13},
    #     12: {'dictionary': 55, 'c': 90, 'a': 84},
    #     13: {'c': 92, 'b': 86},
    #     14: {'a': 36},
    #     15: {'b': 54},
    #     16: {'b': 57},
    #     17: {'b': 31, 'a': 83, 'dictionary': 23, 'c': 55},
    #     18: {'dictionary': 63, 'a': 31, 'c': 72},
    #     19: {'c': 85},
    #     20: {'b': 96, 'a': 12, 'e': 30},
    #     21: {'b': 25, 'e': 55},
    #     22: {'dictionary': 77, 'c': 24, 'a': 28},
    #     23: {'dictionary': 40, 'c': 82},
    #     24: {'e': 84, 'dictionary': 57},
    #     25: {'e': 89},
    #     26: {'a': 90},
    #     27: {'a': 93, 'c': 30, 'e': 22},
    #     28: {'c': 80},
    #     29: {'b': 5, 'c': 64, 'e': 35},
    #     30: {'e': 76, 'c': 88},
    #     31: {'e': 68, 'b': 49, 'a': 24, 'c': 78},
    #     32: {'a': 0, 'e': 34, 'c': 44, 'dictionary': 25},
    #     33: {'dictionary': 68, 'a': 19, 'b': 63},
    #     34: {'e': 74, 'c': 2},
    #     35: {'b': 24, 'e': 92, 'c': 98},
    #     36: {'dictionary': 82, 'e': 23, 'c': 46},
    #     37: {'e': 62, 'a': 94},
    #     38: {'dictionary': 59, 'c': 32},
    #     39: {'e': 48},
    #     40: {'b': 79, 'a': 93, 'dictionary': 61, 'e': 12}
    # }
    # contents_2 = {
    #     1: {"a": 1, "b": 2, "c": 1},
    #     2: {"a": 2, "b": 563, "c": 2, "dictionary": 15},
    #     3: {"a": 3, "b": 3, "c": 3, "dictionary": 5},
    #     4: {"a": 4, "b": 4, "c": 4, "dictionary": 5},
    #     8: {"b": "Really lo", "dictionary": 54566678898, "a": "This stri"},
    #     6: {"e": 2},
    #     9: {"e": 22},
    #     10: {"dictionary": 24},
    #     7: {"e": 21, "dictionary": 5, "a": 13},
    #     12: {'dictionary': 55, 'c': 90, 'a': 84},
    #     13: {'c': 92, 'b': 86},
    #     15: {'b': 54},
    #     17: {'b': 31, 'a': 83, 'dictionary': 23, 'c': 55},
    #     18: {'dictionary': 63, 'a': 31, 'c': 72},
    #     22: {'dictionary': 77, 'c': 24, 'a': 28},
    #     23: {'dictionary': 40, 'c': 82},
    #     26: {'a': 90},
    #     27: {'a': 93, 'c': 30, 'e': 22},
    #     30: {'e': 76, 'c': 88},
    #     31: {'e': 68, 'b': 49, 'a': 24, 'c': 78},
    #     32: {'a': 0, 'e': 34, 'c': 44, 'dictionary': 25},
    #     33: {'dictionary': 68, 'a': 19, 'b': 63},
    #     34: {'e': 74, 'c': 2},
    #     38: {'dictionary': 59, 'c': 32},
    #     39: {'e': 48},
    #     40: {'b': 79, 'a': 93, 'dictionary': 61, 'e': 12}
    # }
    # contents_3 = {
    #     1: {"a": 1, "b": 2, "c": 154654654457112245748},
    #     2: {"a": 2, "b": 563, "c": 2, "dictionary": 15},
    #     3: {"a": 3, "b": 3, "c": 3, "dictionary": 5},
    #     4: {"a": 4, "b": 4, "c": 4, "dictionary": 5},
    #     8: {"b": "Really lo", "dictionary": 54566678898, "a": "This stri"},
    #     6: {"e": 2},
    #     17: {'b': 31, 'a': 83, 'dictionary': 23, 'c': 55},
    #     18: {'dictionary': 63, 'a': 31, 'c': 72},
    #     30: {'e': 76, 'c': 88},
    #     31: {'e': 68, 'b': 49, 'a': 24, 'c': 78},
    #     40: {'b': 79, 'a': 93, 'dictionary': 61, 'e': 12}
    # }
    # contents_4 = {
    #     41: {'b': 87},
    #     42: {'b': 17, 'dictionary': 21, 'a': 95},
    #     43: {'dictionary': 19, 'e': 99, 'c': 26},
    #     44: {'c': 42, 'e': 43},
    #     45: {'b': 13},
    #     46: {'a': 12, 'dictionary': 80},
    #     47: {'a': 97, 'e': 82},
    #     48: {'b': 85, 'c': 38},
    #     49: {'e': 4},
    #     50: {'e': 3, 'c': 93},
    #     51: {'dictionary': 61, 'b': 8, 'a': 88},
    #     52: {'dictionary': 37, 'b': 86, 'c': 70},
    #     53: {'b': 40},
    #     54: {'b': 49, 'a': 80, 'dictionary': 58},
    #     55: {'a': 48},
    #     56: {'b': 70},
    #     57: {'a': 51, 'c': 24},
    #     58: {'e': 59, 'b': 100, 'a': 50},
    #     59: {'c': 2, 'a': 80, 'b': 41},
    #     60: {'c': 32, 'e': 37},
    #     61: {'a': 29, 'dictionary': 30, 'e': 25},
    #     62: {'a': 74, 'c': 63},
    #     63: {'e': 10, 'c': 25},
    #     64: {'e': 23},
    #     65: {'b': 14, 'c': 49},
    #     66: {'e': 72, 'c': 72, 'dictionary': 73},
    #     67: {'dictionary': 13, 'b': 48, 'a': 66, 'c': 10},
    #     68: {'a': 42},
    #     69: {'dictionary': 80, 'b': 70},
    #     70: {'c': 82, 'dictionary': 49, 'b': 3},
    #     71: {'b': 30, 'c': 98, 'a': 54},
    #     72: {'b': 90, 'c': 15, 'e': 6, 'dictionary': 94},
    #     73: {'c': 75, 'b': 40, 'a': 82},
    #     74: {'c': 22, 'e': 87},
    #     75: {'dictionary': 55, 'e': 8, 'a': 8},
    #     76: {'b': 18, 'e': 7, 'dictionary': 65},
    #     77: {'dictionary': 14, 'a': 56},
    #     78: {'b': 68},
    #     79: {'c': 17, 'a': 16, 'dictionary': 59},
    #     80: {'e': 34, 'a': 50, 'b': 20},
    #     81: {'b': 54, 'e': 24, 'dictionary': 52, 'a': 6},
    #     82: {'c': 27, 'dictionary': 50, 'a': 15},
    #     83: {'b': 77},
    #     84: {'e': 21, 'b': 37},
    #     85: {'dictionary': 41, 'c': 26, 'b': 18},
    #     86: {'dictionary': 54, 'b': 19},
    #     87: {'a': 86, 'dictionary': 24, 'c': 49},
    #     88: {'a': 60, 'c': 48},
    #     89: {'dictionary': 20, 'c': 9},
    #     90: {'e': 53, 'b': 27},
    #     91: {'e': 28, 'dictionary': 57, 'c': 18, 'a': 8},
    #     92: {'c': 37, 'b': 47}, 93: {'e': 40, 'c': 35},
    #     94: {'dictionary': 24},
    #     95: {'b': 40},
    #     96: {'dictionary': 79, 'e': 41},
    #     97: {'c': 36, 'a': 74, 'e': 47},
    #     98: {'b': 89, 'a': 73},
    #     99: {'b': 56, 'c': 55, 'a': 5, 'e': 72},
    #     100: {'b': 38},
    #     101: {'a': 86, 'b': 40, 'e': 37, 'c': 41},
    #     102: {'dictionary': 54, 'a': 32, 'b': 37},
    #     103: {'dictionary': 63, 'a': 9, 'e': 58},
    #     104: {'a': 65, 'b': 69},
    #     105: {'c': 15},
    #     106: {'c': 38, 'e': 4, 'a': 16, 'b': 71},
    #     107: {'e': 65, 'b': 31},
    #     108: {'b': 19, 'e': 80},
    #     109: {'c': 62},
    #     110: {'dictionary': 49},
    #     111: {'c': 45, 'e': 65, 'b': 66, 'dictionary': 95},
    #     112: {'a': 93, 'e': 89, 'dictionary': 60, 'c': 36},
    #     113: {'c': 68, 'b': 78},
    #     114: {'a': 16, 'c': 88},
    #     115: {'e': 33, 'b': 26},
    #     116: {'b': 36, 'e': 47, 'a': 98},
    #     117: {'e': 92, 'b': 68, 'dictionary': 53, 'a': 3},
    #     118: {'e': 58, 'a': 84, 'b': 43},
    #     119: {'a': 71, 'c': 67, 'dictionary': 42},
    #     120: {'a': 12},
    #     121: {'b': 13, 'c': 93, 'e': 88, 'dictionary': 1},
    #     122: {'e': 49, 'c': 67, 'b': 73},
    #     123: {'a': 40, 'dictionary': 90, 'b': 84, 'c': 18},
    #     124: {'e': 72},
    #     125: {'b': 91, 'dictionary': 100},
    #     126: {'dictionary': 75, 'c': 72},
    #     127: {'c': 90, 'e': 38, 'a': 18, 'dictionary': 21},
    #     128: {'a': 57, 'b': 84, 'e': 73},
    #     129: {'c': 93, 'e': 51, 'b': 77},
    #     130: {'b': 19, 'a': 86, 'c': 26},
    #     131: {'e': 51, 'a': 33, 'dictionary': 8},
    #     132: {'b': 83, 'a': 73, 'e': 20},
    #     133: {'dictionary': 81, 'b': 2},
    #     134: {'b': 41, 'c': 52, 'a': 95},
    #     135: {'b': 23, 'dictionary': 43, 'c': 17},
    #     136: {'b': 71, 'e': 88, 'dictionary': 49},
    #     137: {'a': 96, 'e': 96, 'dictionary': 42, 'b': 85},
    #     138: {'a': 1, 'c': 55},
    #     139: {'b': 12, 'e': 88, 'c': 18},
    #     140: {'e': 68},
    #     141: {'a': 95, 'dictionary': 65, 'e': 21, 'c': 91},
    #     142: {'e': 74, 'a': 75},
    #     143: {'b': 61},
    #     144: {'a': 49, 'e': 80, 'dictionary': 86},
    #     145: {'e': 92, 'dictionary': 72},
    #     146: {'c': 26},
    #     147: {'e': 7, 'b': 91, 'dictionary': 41, 'a': 17},
    #     148: {'a': 25, 'dictionary': 100, 'e': 17},
    #     149: {'c': 81, 'a': 43, 'b': 59},
    #     150: {'a': 70, 'e': 51, 'b': 7},
    #     151: {'a': 86, 'b': 99},
    #     152: {'e': 30, 'c': 71, 'dictionary': 10},
    #     153: {'c': 38},
    #     154: {'b': 85},
    #     155: {'b': 89, 'e': 77, 'dictionary': 13},
    #     156: {'dictionary': 43, 'a': 23},
    #     157: {'e': 85},
    #     158: {'c': 8},
    #     159: {'b': 73, 'a': 72},
    #     160: {'e': 48},
    #     161: {'a': 57, 'b': 49, 'e': 88},
    #     162: {'dictionary': 83, 'c': 50},
    #     163: {'a': 88, 'b': 33, 'e': 51, 'c': 3},
    #     164: {'dictionary': 63, 'c': 97},
    #     165: {'e': 75, 'a': 20, 'c': 95},
    #     166: {'b': 77},
    #     167: {'e': 4, 'a': 64},
    #     168: {'dictionary': 48, 'a': 50, 'b': 12, 'c': 41},
    #     169: {'b': 96}, 170: {'e': 87},
    #     171: {'b': 8, 'a': 62, 'e': 26},
    #     172: {'c': 61, 'b': 45, 'a': 11},
    #     173: {'a': 61},
    #     174: {'a': 48, 'b': 28, 'e': 30},
    #     175: {'a': 12},
    #     176: {'a': 57, 'c': 48, 'dictionary': 41, 'b': 32},
    #     177: {'a': 97, 'c': 48, 'b': 20},
    #     178: {'a': 60, 'e': 54, 'dictionary': 33},
    #     179: {'a': 44, 'b': 17},
    #     180: {'dictionary': 60},
    #     181: {'a': 8, 'b': 46, 'dictionary': 24},
    #     182: {'e': 14, 'a': 28},
    #     183: {'a': 40, 'c': 6},
    #     184: {'e': 9, 'c': 80, 'b': 48},
    #     185: {'dictionary': 48},
    #     186: {'dictionary': 9, 'c': 52, 'b': 84},
    #     187: {'a': 93, 'b': 52, 'dictionary': 3},
    #     188: {'b': 24},
    #     189: {'dictionary': 3, 'c': 27},
    #     190: {'c': 37, 'e': 8},
    #     191: {'a': 52, 'e': 34},
    #     192: {'e': 14, 'dictionary': 90, 'c': 38},
    #     193: {'e': 39, 'a': 98, 'c': 79},
    #     194: {'dictionary': 34},
    #     195: {'e': 74},
    #     196: {'dictionary': 51, 'a': 78, 'c': 57},
    #     197: {'e': 43, 'b': 75},
    #     198: {'a': 71, 'c': 27},
    #     199: {'e': 52},
    #     200: {'c': 80, 'e': 60},
    #     201: {'c': 27, 'dictionary': 97, 'b': 64},
    #     202: {'e': 70, 'c': 66},
    #     203: {'e': 5},
    #     204: {'b': 49},
    #     205: {'dictionary': 29, 'c': 15},
    #     206: {'a': 10, 'c': 59},
    #     207: {'e': 22, 'dictionary': 36, 'b': 99},
    #     208: {'a': 38, 'c': 8},
    #     209: {'dictionary': 20, 'a': 26, 'e': 14},
    #     210: {'c': 20, 'b': 46},
    #     211: {'dictionary': 21, 'a': 14},
    #     212: {'e': 25, 'dictionary': 34, 'c': 18},
    #     213: {'a': 74},
    #     214: {'a': 14, 'b': 1},
    #     215: {'a': 64, 'e': 53, 'c': 72},
    #     216: {'dictionary': 66, 'e': 87, 'a': 80},
    #     217: {'e': 77, 'dictionary': 75},
    #     218: {'e': 81, 'dictionary': 61},
    #     219: {'dictionary': 17},
    #     220: {'dictionary': 69, 'e': 90},
    #     221: {'a': 34},
    #     222: {'e': 21, 'c': 72, 'dictionary': 6},
    #     223: {'e': 31, 'dictionary': 64},
    #     224: {'dictionary': 77, 'a': 1},
    #     225: {'a': 67, 'dictionary': 74},
    #     226: {'b': 97, 'c': 55, 'dictionary': 41},
    #     227: {'a': 69, 'b': 93, 'dictionary': 89},
    #     228: {'dictionary': 67, 'e': 18, 'b': 37, 'a': 32},
    #     229: {'e': 97, 'c': 21},
    #     230: {'e': 70, 'c': 69},
    #     231: {'a': 98, 'e': 31},
    #     232: {'e': 69},
    #     233: {'b': 47, 'e': 86},
    #     234: {'e': 67},
    #     235: {'b': 63, 'e': 56, 'a': 63, 'dictionary': 51},
    #     236: {'dictionary': 49, 'a': 8},
    #     237: {'a': 90, 'b': 11, 'c': 7},
    #     238: {'a': 3},
    #     239: {'e': 37, 'dictionary': 57},
    #     240: {'dictionary': 40, 'e': 36},
    #     241: {'b': 59, 'dictionary': 35, 'e': 81},
    #     242: {'b': 46},
    #     243: {'a': 65, 'c': 35},
    #     244: {'c': 80, 'a': 16},
    #     245: {'a': 37, 'c': 81, 'b': 34},
    #     246: {'dictionary': 56, 'a': 98},
    #     247: {'c': 53, 'a': 46, 'dictionary': 84},
    #     248: {'a': 45, 'e': 21},
    #     249: {'b': 17, 'a': 26, 'c': 54, 'e': 64},
    #     250: {'c': 50, 'b': 14, 'e': 12},
    #     251: {'a': 33, 'b': 95},
    #     252: {'a': 31, 'e': 8, 'c': 51},
    #     253: {'b': 48, 'dictionary': 44},
    #     254: {'b': 75, 'e': 66},
    #     255: {'b': 96, 'dictionary': 77},
    #     256: {'b': 65, 'dictionary': 27},
    #     257: {'b': 47, 'a': 9},
    #     258: {'b': 18, 'e': 33},
    #     259: {'e': 77, 'c': 16, 'dictionary': 43},
    #     260: {'a': 1, 'b': 38, 'c': 27},
    #     261: {'c': 83},
    #     262: {'e': 66, 'dictionary': 55, 'b': 86},
    #     263: {'b': 94, 'c': 78, 'e': 65},
    #     264: {'b': 59},
    #     265: {'e': 12, 'a': 43},
    #     266: {'c': 84},
    #     267: {'c': 69, 'a': 86, 'e': 56, 'dictionary': 71},
    #     268: {'c': 36, 'b': 16},
    #     269: {'e': 77, 'c': 97},
    #     270: {'a': 86, 'e': 72},
    #     271: {'c': 18},
    #     272: {'a': 14},
    #     273: {'c': 26, 'dictionary': 12, 'a': 59, 'e': 98},
    #     274: {'e': 70},
    #     275: {'b': 55, 'e': 70, 'c': 22},
    #     276: {'a': 40, 'c': 18, 'dictionary': 9},
    #     277: {'c': 33, 'a': 87, 'b': 74},
    #     278: {'e': 6, 'dictionary': 13, 'a': 98},
    #     279: {'b': 64, 'dictionary': 37},
    #     280: {'c': 55},
    #     281: {'b': 46},
    #     282: {'c': 77, 'a': 54},
    #     283: {'e': 74, 'c': 98, 'dictionary': 46},
    #     284: {'c': 54, 'e': 76, 'a': 8},
    #     285: {'e': 14, 'dictionary': 21},
    #     286: {'c': 72},
    #     287: {'c': 89},
    #     288: {'c': 43, 'e': 66},
    #     289: {'a': 29, 'b': 49, 'e': 85, 'c': 46},
    #     290: {'b': 43, 'c': 61},
    #     291: {'e': 41, 'dictionary': 42},
    #     292: {'c': 15, 'b': 13},
    #     293: {'b': 67},
    #     294: {'c': 18, 'e': 71, 'dictionary': 9, 'b': 1, 'a': 17},
    #     295: {'a': 29, 'b': 7, 'c': 69},
    #     296: {'dictionary': 49},
    #     297: {'b': 61, 'dictionary': 71, 'a': 36, 'e': 91},
    #     298: {'e': 28, 'c': 51, 'b': 18},
    #     299: {'a': 70, 'dictionary': 95, 'e': 94},
    #     300: {'a': 63, 'c': 57},
    #     301: {'b': 8},
    #     302: {'b': 8},
    #     303: {'b': 81, 'dictionary': 15, 'e': 100},
    #     304: {'e': 54, 'dictionary': 75, 'c': 15, 'b': 2},
    #     305: {'dictionary': 95, 'e': 95, 'b': 58},
    #     306: {'dictionary': 15, 'c': 76, 'b': 97},
    #     307: {'dictionary': 6, 'c': 89},
    #     308: {'dictionary': 46, 'b': 90},
    #     309: {'dictionary': 53},
    #     310: {'e': 40, 'b': 27},
    #     311: {'a': 13, 'e': 20, 'b': 53},
    #     312: {'c': 10, 'e': 66},
    #     313: {'b': 32, 'e': 62, 'a': 70},
    #     314: {'dictionary': 75, 'e': 61},
    #     315: {'dictionary': 80},
    #     316: {'c': 68},
    #     317: {'b': 33, 'e': 41},
    #     318: {'a': 98, 'c': 54},
    #     319: {'dictionary': 27},
    #     320: {'c': 84, 'a': 66},
    #     321: {'b': 36, 'dictionary': 47},
    #     322: {'a': 92, 'c': 26, 'e': 8, 'dictionary': 92},
    #     323: {'e': 63, 'b': 77, 'dictionary': 17},
    #     324: {'dictionary': 99},
    #     325: {'e': 7, 'a': 19, 'c': 100, 'b': 65},
    #     326: {'c': 30, 'b': 6, 'a': 54},
    #     327: {'dictionary': 32},
    #     328: {'dictionary': 57, 'e': 98},
    #     329: {'b': 92, 'c': 77, 'e': 75},
    #     330: {'dictionary': 54}, 331: {'a': 7},
    #     332: {'c': 68, 'b': 79},
    #     333: {'dictionary': 12, 'b': 75, 'c': 41},
    #     334: {'a': 27, 'e': 16},
    #     335: {'c': 75, 'e': 37},
    #     336: {'b': 8},
    #     337: {'e': 62, 'a': 11, 'b': 30},
    #     338: {'c': 33, 'dictionary': 14, 'a': 23},
    #     339: {'a': 34, 'b': 8, 'c': 85, 'e': 55},
    #     340: {'e': 31, 'c': 47},
    #     341: {'c': 20, 'e': 74, 'a': 18},
    #     342: {'c': 28},
    #     343: {'c': 46, 'a': 8, 'dictionary': 18},
    #     344: {'dictionary': 20, 'b': 73, 'e': 98},
    #     345: {'e': 14, 'b': 10},
    #     346: {'e': 72, 'dictionary': 49},
    #     347: {'e': 81},
    #     348: {'dictionary': 61, 'c': 57},
    #     349: {'a': 21},
    #     350: {'b': 48, 'a': 58},
    #     351: {'b': 58, 'c': 21},
    #     352: {'dictionary': 27, 'a': 16, 'c': 31},
    #     353: {'dictionary': 49, 'c': 36, 'a': 46},
    #     354: {'a': 76, 'b': 49, 'e': 89},
    #     355: {'c': 28},
    #     356: {'e': 36, 'c': 49, 'a': 85},
    #     357: {'c': 43, 'e': 39, 'a': 45},
    #     358: {'b': 51, 'c': 45},
    #     359: {'dictionary': 22},
    #     360: {'a': 98, 'b': 63, 'c': 68},
    #     361: {'e': 80, 'c': 50, 'dictionary': 65, 'b': 70},
    #     362: {'c': 73, 'dictionary': 60},
    #     363: {'c': 25, 'a': 52},
    #     364: {'dictionary': 89, 'e': 66, 'a': 39},
    #     365: {'c': 96, 'b': 49, 'a': 98, 'e': 3},
    #     366: {'dictionary': 67},
    #     367: {'b': 15, 'a': 41, 'e': 82},
    #     368: {'e': 55, 'a': 78, 'dictionary': 94, 'c': 92},
    #     369: {'b': 46}, 370: {'b': 38, 'a': 43},
    #     371: {'c': 75, 'b': 30},
    #     372: {'dictionary': 61, 'b': 75},
    #     373: {'b': 95, 'e': 80, 'c': 40},
    #     374: {'b': 46, 'dictionary': 12},
    #     375: {'e': 64, 'dictionary': 15, 'b': 29, 'a': 57},
    #     376: {'e': 71},
    #     377: {'dictionary': 80},
    #     378: {'e': 8, 'c': 6},
    #     379: {'c': 91, 'e': 79, 'b': 36},
    #     380: {'b': 66, 'e': 10, 'dictionary': 89},
    #     381: {'b': 30},
    #     382: {'a': 89, 'dictionary': 95},
    #     383: {'e': 98, 'a': 92},
    #     384: {'c': 63, 'e': 45, 'dictionary': 19},
    #     385: {'e': 87},
    #     386: {'b': 89, 'a': 3, 'c': 58, 'e': 79},
    #     387: {'e': 89, 'c': 33, 'b': 89, 'dictionary': 61},
    #     388: {'e': 35},
    #     389: {'a': 66},
    #     390: {'dictionary': 23, 'c': 86, 'e': 46, 'a': 95},
    #     391: {'dictionary': 26}
    # }
    # contents_5 = {'Worked': {'monday': 0, 'tuesday': 0, 'wednesday': 0, 'thursday': 0, 'friday': 0},
    #               'Total': {'monday': 0, 'tuesday': 0, 'wednesday': 0, 'thursday': 0, 'friday': 0},
    #               'Off': {'monday': 0, 'tuesday': 0, 'wednesday': 0, 'thursday': 0, 'friday': 0},
    #               'Percentage Worked': {'monday': 0, 'tuesday': 0, 'wednesday': 0, 'thursday': 0, 'friday': 0}}
    #
    # TABLE_X = TABLE_MARGIN + MARGIN_LINES_WIDTH + MARGIN_LINES_MARGIN
    # TABLE_Y = TABLE_MARGIN + MARGIN_LINES_WIDTH + TITLE_HEIGHT + TITLE_MARGIN
    #
    # TABLE_LEFT_MARGIN = 8
    # TITLE_V_MARGIN = 5
    #
    # table1 = pdf.table(
    #     title="Remorques Lewis",
    #     x=TABLE_X,
    #     y=TABLE_Y,
    #     w=TABLE_W,
    #     contents=contents_3,
    #     header_colours=[BLACK, BWS_RED],
    #     colours=[[BWS_RED, BWS_GREY, BWS_BLACK], [BWS_BLACK, BWS_RED, BWS_RED]]
    # )
    #
    # print("1. (TABLE_X, TABLE_Y): ({}, {})".format(TABLE_X, TABLE_Y))
    # TABLE_Y = table1[1] + (2 * TABLE_MARGIN)
    # print("2. (TABLE_X, TABLE_Y): ({}, {})".format(TABLE_X, TABLE_Y))
    #
    # table2 = pdf.table(
    #     title="NorthEast",
    #     x=TABLE_X,
    #     y=TABLE_Y,
    #     w=TABLE_W,
    #     contents=contents_1,
    #     header_colours=[BLACK, BWS_RED],
    #     colours=[[BWS_RED, BWS_GREY, BWS_BLACK], [BWS_BLACK, BWS_RED, BWS_RED]]
    # )
    #
    # TABLE_Y = table2[1] + (2 * TABLE_MARGIN)
    #
    # table3 = pdf.table(
    #     title="Fort Garry International Ltd.",
    #     x=TABLE_X,
    #     y=TABLE_Y,
    #     w=TABLE_W,
    #     contents=contents_2,
    #     header_colours=[BLACK, BWS_RED],
    #     colours=[[BWS_RED, BWS_GREY, BWS_BLACK], [BWS_BLACK, BWS_RED, BWS_RED]]
    # )
    #
    # TABLE_Y = table3[1] + (2 * TABLE_MARGIN)
    #
    # table4 = pdf.table(
    #     title="Diamond International",
    #     x=TABLE_X,
    #     y=TABLE_Y,
    #     w=TABLE_W,
    #     contents=contents_4,
    #     header_colours=[BLACK, BWS_RED],
    #     colours=[[BLUEVIOLET, GREEN_2, YELLOW_4, BLUE, RED, ORANGE],
    #              [WHITE, BLACK, BLACK, ORANGE, BLUE, WHITE]],
    #     desc_txt="This is Diamond's dealer delivery report for this period.\nHow about those new lines?\t\tWhat about these TABS?",
    #     new_page_for_table=True,
    #     show_row_names=True,
    #     start_with_header=False
    # )
    #
    # TABLE_Y = table4[1] + (2 * TABLE_MARGIN)
    #
    # table5 = pdf.table(
    #     title="Weekdays",
    #     x=TABLE_X,
    #     y=TABLE_Y,
    #     w=TABLE_W,
    #     contents=contents_5,
    #     header_colours=[BLACK, BWS_RED],
    #     colours=[[BLACK],
    #              [WHITE]],
    #     desc_txt="This is Diamond's dealer delivery report for this period.\nHow about those new lines?\t\tWhat about these TABS?"
    # )
    #
    # TABLE_Y = table5[1] + (2 * TABLE_MARGIN)
    #
    # table6 = pdf.table(
    #     title="Random Test Set",
    #     x=TABLE_X,
    #     y=TABLE_Y,
    #     w=TABLE_W,
    #     contents=random_test_set(30, start=60, step=101),
    #     header_colours=[BLACK, BWS_RED],
    #     colours=[[BLACK],
    #              [WHITE]],
    #     desc_txt="This is a random test set",
    #     show_row_names=True
    # )
    #
    # TABLE_Y = table6[1] + (2 * TABLE_MARGIN)
    #
    # table7 = pdf.table(
    #     title="Clean Table",
    #     x=TABLE_X,
    #     y=TABLE_Y,
    #     w=TABLE_W,
    #     left_margin=TABLE_LEFT_MARGIN,
    #     title_v_margin=TITLE_V_MARGIN,
    #     contents=random_test_set(43),
    #     header_colours=[GRAY_30, BLACK],
    #     colours=[[WHITE, GRAY_69],
    #              [BLACK]],
    #     desc_txt="Plain black, white and grey table, more professional looking.\nWith bits of extra text\nHere\nAnd Here\n\tAnd over here.",
    #     show_row_names=True,
    #     include_top_doc_link=True,
    #     new_page_for_table=False,
    #     row_name_col_lbl="Number"
    # )
    #
    # # pdf.line(15, 25, 15, 26)
    # # pdf.line(25, 25, 25, 27)
    # # pdf.line(35, 25, 35, 28)
    # # pdf.line(45, 25, 45, 29)
    # # pdf.line(55, 25, 55, 30)
    # # pdf.line(0, 35, 5, 35)
    # # pdf.line(0, 35, 8, 35)
    #
    # pdf.output(FILE_NAME, 'F')
    #
    # print("table1:", table1)
    # print("table2:", table2)
    # print("table3:", table3)
    # print("table4:", table4)
    # webbrowser.open(FILE_NAME)
    #
    # print(dict_print({
    #     "TABLE_MARGIN": TABLE_MARGIN,
    #     "MARGIN_LINES_MARGIN": MARGIN_LINES_MARGIN,
    #     "MARGIN_LINES_WIDTH": MARGIN_LINES_WIDTH,
    #     "TABLE_W": TABLE_W
    # }, "Values"))

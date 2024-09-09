import calendar
import datetime
import os
from typing import Any

import pandas as pd
import customtkinter as ctk
from CTkTable import CTkTable
from PIL import ImageTk, Image

from colour_utility import Colour, random_colour, font_foreground, gradient
from tkinter_utility import calc_geometry_tl
from utility import grid_cells, clamp

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class App(ctk.CTk):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.title_app_long = f"NHL Jersey Data"
        self.image_directory = r"C:\Users\abrig\Documents\Coding_Practice\Python\Hockey pool\Images"
        self.btn_images = {}
        self.res_images = {}
        self.res_img_to_t = {}
        self.res_pyimage_to_t = {}
        # self.history = {}
        self.full_size_image = (200, 200)
        self.small_size_image = (40, 40)
        self.df = pd.read_excel(r"D:\NHL Jerseys.xlsm", sheet_name="JerseyData")
        self.geometry(calc_geometry_tl(0.99, 0.99, parent=self, ask=True))
        # self.geometry(calc_geometry_tl(100, 100, parent=self))
        self.title(self.title_app_long)

        self.load_images()

        self.tab_name_numbers = f"Numbers"
        self.tab_name_teams = f"Teams"
        self.tab_name_birthdays = f"Birthdays"
        self.tab_view_master = ctk.CTkTabview(self)
        self.tab_view_master.add(self.tab_name_numbers)
        self.tab_view_master.add(self.tab_name_teams)
        self.tab_view_master.add(self.tab_name_birthdays)
        self.w_tab_frame, self.h_tab_frame = 1000, 600
        self.f_tab_numbers = FrameNumbersView(
            self.tab_view_master.tab(self.tab_name_numbers),
            self,
            width=self.w_tab_frame,
            height=self.h_tab_frame
        )
        self.f_tab_teams = FrameTeamsView(
            self.tab_view_master.tab(self.tab_name_teams),
            self,
            width=self.w_tab_frame,
            height=self.h_tab_frame
        )
        self.f_tab_birthdays = FrameBirthdaysView(
            self.tab_view_master.tab(self.tab_name_birthdays),
            self,
            width=self.w_tab_frame,
            height=self.h_tab_frame
        )

        self.f_tab_numbers.grid(row=0, column=0, rowspan=1, columnspan=1, sticky=ctk.NSEW)
        self.f_tab_teams.grid(row=0, column=0, rowspan=1, columnspan=1, sticky=ctk.NSEW)
        self.f_tab_birthdays.grid(row=0, column=0, rowspan=1, columnspan=1, sticky=ctk.NSEW)
        self.tab_view_master.grid(row=0, column=0, rowspan=1, columnspan=1, sticky=ctk.NSEW)

    def load_images(self):
        if not os.path.exists(self.image_directory):
            self.image_directory = r"C:\Users\ABriggs\Documents\Coding Practice\Coding_Practice\Python\Hockey pool\Images"

        for pth in os.listdir(self.image_directory):
            if not pth.endswith((".png", ".jpg")):
                continue
            team = pth.replace("logo", "").replace("_", " ").replace(".png", "").replace(".jpg", "").strip()
            # if "division" in team or "conference" in team:
            #     continue
            im_pth = os.path.join(self.image_directory, pth)
            img = Image.open(im_pth)
            # img_c = img.copy()
            btn_image = ImageTk.PhotoImage(img.resize(self.full_size_image))
            res_image = ImageTk.PhotoImage(img.resize(self.small_size_image))
            self.btn_images[team] = btn_image
            self.res_images[team] = res_image

        # no image
        img = Image.open("no_image.png")
        self.btn_images[None] = ImageTk.PhotoImage(img.resize(self.full_size_image))
        self.res_images[None] = ImageTk.PhotoImage(img.resize(self.small_size_image))

        print(f"{len(self.btn_images)=}")


class FrameTeamsView(ctk.CTkScrollableFrame):

    def __init__(self, master: Any, ctk_: App, **kwargs):
        super().__init__(master, **kwargs)

        self.ctk_ = ctk_

        self.frame_controls = ctk.CTkFrame(self)
        self.frame_reporting = ctk.CTkScrollableFrame(self)

        self.list_valid_sorts = ["Alphabetically", "Division", "Total"]
        self.tv_valid_sorts = ctk.StringVar(self, value=self.list_valid_sorts[0])
        self.dict_tags_teams = dict()
        self.df_unique_team_counts = self.ctk_.df.groupby("Team").size().reset_index(name="CountOfTeam")
        print(f"{list(self.ctk_.btn_images)=}")
        for t in self.ctk_.df["Team"].dropna().unique():
            # self.dict_tags_teams[t] = {k: v for k, v in template.items()}
            t_ = t.replace(".", "").strip().lower()
            print(f"{t=}, {t_=}")
            img = self.ctk_.res_images[t_]
            img_lbl = ctk.CTkLabel(self.frame_reporting, text="", image=img)
            lbl = ctk.CTkLabel(self.frame_reporting, text=self.df_unique_team_counts.loc[self.df_unique_team_counts["Team"] == t].iloc[0]["CountOfTeam"])
            self.dict_tags_teams[t] = {
                "img": img,
                "img_lbl": img_lbl,
                "lbl": lbl
            }
            # img_lbl.grid()
            # lbl.grid()
        self.list_sorted_teams = sorted(list(self.dict_tags_teams))

        # template = {"img": None, "lbl": None}
        self.grid_positions = dict()
        for vs in self.list_valid_sorts:
            self.grid_positions[vs] = dict()
            for i, t in enumerate(self.list_sorted_teams):
                self.grid_positions[vs][t] = {
                    "row": i,
                    "column": 0,
                    "rowspan": 1,
                    "columnspan": 1,
                }

        self.frame_controls.grid(row=0, column=0, rowspan=1, columnspan=1, sticky=ctk.NSEW)
        self.frame_reporting.grid(row=1, column=0, rowspan=1, columnspan=1, sticky=ctk.NSEW)
        self.grid_by_sort()

        # self.data = [
        #     [[], row["Team"], row["CountOfTeam"]]
        #     for i, row in self.df_unique_team_counts
        # ]
        # self.table_alpha = CTkTable(self.frame_reporting, values=self.data)

    def grid_by_sort(self):
        sm = self.tv_valid_sorts.get()
        if sm == self.list_valid_sorts[2]:
            # Total
            pass
        elif sm == self.list_valid_sorts[1]:
            # Division
            pass
        else:
            for i, t in enumerate(self.grid_positions[sm]):
                ga_il = self.grid_positions[sm][t]
                ga_l = {k: v for k, v in ga_il.items()}
                ga_l["column"] += 1
                self.dict_tags_teams[t]["img_lbl"].grid(**ga_il)
                self.dict_tags_teams[t]["lbl"].grid(**ga_l)


class FrameNumbersView(ctk.CTkScrollableFrame):

    def __init__(self, master: Any, ctk_: App, **kwargs):
        super().__init__(master, **kwargs)

        self.ctk_ = ctk_

        self.owned_numbers = dict()

        for i in range(100):
            self.owned_numbers[i] = 0

        for i, row in self.ctk_.df.iterrows():
            number = row["Number"]
            if not pd.isna(number):
                number = int(number)
                self.owned_numbers[number] += 1

        # self.count_distinct_jerseys = self.ctk_.df_timeline_order_receive.shape[0]
        self.count_distinct_jerseys = self.ctk_.df["Number"].dropna().count()
        self.v_lbl_demo = ctk.StringVar(self, value=f"Total Jerseys ({self.count_distinct_jerseys})")
        self.lbl_demo = ctk.CTkLabel(self, textvariable=self.v_lbl_demo)

        self.w_canvas, self.h_canvas = 200, 200
        self.gc = grid_cells(200, 10, r_type=list)

        self.colour_background_canvas = Colour("#AEBEBE")
        self.colour_background_owned_number_check = Colour("#2A4AFA")
        self.colour_background_owned_number_check_heat_map = Colour("#FA2A4A")

        self.frame_top = ctk.CTkFrame(self)
        self.canvas = ctk.CTkCanvas(
            self.frame_top,
            background=self.colour_background_canvas.hex_code,
            width=self.w_canvas,
            height=self.h_canvas
        )
        self.frame_top_a = ctk.CTkFrame(self.frame_top)
        self.tv_lbl_canvas_click_instruction = ctk.StringVar(self, value=f"Click a Number")
        self.lbl_canvas_click_instruction = ctk.CTkLabel(self.frame_top_a, textvariable=self.tv_lbl_canvas_click_instruction)
        self.tb_canvas_click_data = ctk.CTkTextbox(self.frame_top_a, width=500, font=("Courier", 14))
        self.v_canvas_has_been_clicked = ctk.BooleanVar(self, value=False)

        self.tv_sw_show_heat_map = ctk.StringVar(self, value=f"Heat Map")
        self.v_sw_show_heat_map = ctk.IntVar(self, value=0)

        self.list_own_numbers = sorted(list(self.owned_numbers))
        self.heat_map_colours = self.calc_heat_map_colours()
        self.dict_canvas_tags = dict()
        for i, row in enumerate(self.gc):
            for j, coords in enumerate(row):
                n = ((i * 10) + j) + 1
                if n == 100:
                    # no #100
                    break
                x0, y0, x1, y1 = coords
                col = self.get_cell_colour(n)
                tr = self.canvas.create_rectangle(
                    x0, y0, x1, y1, fill=col.hex_code
                )
                tt = self.canvas.create_text(
                    x0 + ((x1 - x0) / 2), y0 + ((y1 - y0) / 2),
                    fill=col.font_foreground(rgb=False),
                    text=f"{n}"
                )
                self.canvas.tag_bind(
                    tt,
                    "<Button-1>",
                    lambda event, i_=i, j_=j: self.click_canvas(event, i_, j_)
                )
                self.canvas.tag_bind(
                    tr,
                    "<Button-1>",
                    lambda event, i_=i, j_=j: self.click_canvas(event, i_, j_)
                )
                self.dict_canvas_tags[(i, j)] = {
                    "rect": tr,
                    "text": tt
                }
        self.sw_show_heat_map = ctk.CTkSwitch(
            self,
            textvariable=self.tv_sw_show_heat_map,
            variable=self.v_sw_show_heat_map,
            command=self.update_show_heat_map
        )

        self.fig_frame = ctk.CTkFrame(self)
        self.fig = Figure(figsize=(5, 4), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.canvas_fig = FigureCanvasTkAgg(self.fig, master=self.fig_frame)
        self.canvas_fig.draw()

        self.ax.bar(self.list_own_numbers, [self.owned_numbers[n] for n in self.list_own_numbers])
        self.ax.set_xlabel("Jersey #")
        self.ax.set_ylabel("Count")
        self.ax.set_title(f"Jerseys by Number")

        self.lbl_demo.grid(row=0, column=0, rowspan=1, columnspan=1, sticky=ctk.NSEW)
        self.sw_show_heat_map.grid(row=1, column=0, rowspan=1, columnspan=1, sticky=ctk.NSEW)
        self.frame_top.grid(row=2, column=0, rowspan=1, columnspan=1, sticky=ctk.NSEW)
        self.canvas.grid(row=0, column=0, rowspan=1, columnspan=1, sticky=ctk.NSEW)
        self.frame_top_a.grid(row=0, column=1, rowspan=1, columnspan=1, sticky=ctk.NSEW)
        self.lbl_canvas_click_instruction.grid(row=0, column=0, rowspan=1, columnspan=1, sticky=ctk.NSEW)
        self.fig_frame.grid(row=3, column=0, rowspan=1, columnspan=1, sticky=ctk.NSEW)
        self.canvas_fig.get_tk_widget().pack(side=ctk.TOP, fill=ctk.BOTH, expand=1)

    def get_cell_colour(self, n):
        # n is offset by 1
        if self.owned_numbers[n] > 0:
            if self.v_sw_show_heat_map.get():
                # return Colour(random_colour(name=True))
                return self.heat_map_colours[n]
            else:
                return self.colour_background_owned_number_check
        else:
            return self.colour_background_canvas

    def update_show_heat_map(self):
        for i, row in enumerate(self.gc):
            for j, coords in enumerate(row):
                n = ((i * 10) + j) + 1
                if n == 100:
                    break
                col = self.get_cell_colour(n)
                self.canvas.itemconfigure(
                    self.dict_canvas_tags[(i, j)]["rect"],
                    fill=col.hex_code
                )
                self.canvas.itemconfigure(
                    self.dict_canvas_tags[(i, j)]["text"],
                    fill=col.font_foreground(rgb=False)
                )
        # self.id_after_update_show_heat_map = self.after(self.time_after_update_show_heat_map, self.update)

    def calc_heat_map_colours(self):
        max_slices = max(self.owned_numbers.values())
        c1 = self.colour_background_canvas
        c2 = self.colour_background_owned_number_check_heat_map
        grads = [Colour(gradient(i, max_slices, c1, c2, rgb=False)) for i in range(max_slices+1)]
        return {i: grads[n] for i, n in self.owned_numbers.items()}

    def click_canvas(self, event, i, j):
        self.tb_canvas_click_data.delete("0.0", ctk.END)
        n = ((i * 10) + j) + 1

        if not self.v_canvas_has_been_clicked.get():
            self.lbl_canvas_click_instruction.grid_forget()
            self.tb_canvas_click_data.grid(row=0, column=0, rowspan=1, columnspan=1)
            self.v_canvas_has_been_clicked.set(True)

        df = self.ctk_.df.loc[self.ctk_.df["Number"] == n]
        df = df.sort_values(by=["Team", "PlayerLast", "PlayerFirst"])
        text = ""
        for k, row in df.iterrows():
            # text += f"{row['Team'].center(22)} - {row['PlayerFirst'].rjust(11)} {row['PlayerLast'].ljust(18)}\n"
            text += f"{row['Team'].center(22)} - {row['PlayerLast']}, {row['PlayerFirst']}\n"
        if df.shape[0] == 0:
            text = "No Data"
        self.tb_canvas_click_data.insert("0.0", text)


class CalendarCanvas(ctk.CTkCanvas):
    def __init__(
            self,
            master,
            year: int | None = datetime.datetime.now().year,
            months_per_row: int = 4,
            width: int = 600,
            height: int = 700,
            colour_background_canvas: Colour = Colour("#AEBEBE"),
            colour_background_owned_number_check: Colour = Colour("#2A4AFA"),
            colour_background_owned_number_check_heat_map: Colour = Colour("#FA2A4A"),
            colour_background_header_year: Colour = Colour("#627272"),
            colour_background_header_month: Colour = Colour("#7B8B8B"),
            colour_background_header_weekday: Colour = Colour("#94A4A4"),
            *args, **kwargs
    ):
        super().__init__(master=master, *args, **kwargs)

        self.year = year
        self.months_per_row = clamp(3, months_per_row, 4)
        self.weeks_per_month = 6 + 1  # for the month label
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
        self.configure(
            width=self.w_canvas,
            height=self.h_canvas,
            background=self.colour_background_canvas.hex_code
        )
        self.gc = grid_cells(self.w_canvas, self.n_cols, self.h_canvas, self.n_rows, r_type=list)
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
            for j in range(self.n_cols):
                for tag_name in ("rect", "text"):
                    self.itemconfigure(
                        self.dict_canvas_tags[(0, j)][tag_name],
                        state="hidden"
                    )

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
        for j in range(self.n_cols):
            for tag_name in ("rect", "text"):
                self.itemconfigure(
                    self.dict_canvas_tags[(ri, j)][tag_name],
                    state="hidden"
                )
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
                )
            })
            print(f"{month_name[:3].upper()}: {bbox_month=}")
        # print(f"{self.dict_canvas_tags['header_month']=}")

        self.calc_days()

    def calc_days(self):
        ri = 2 if self.year is not None else 1
        if self.year is not None:
            # for i, data in enumerate(self.dict_canvas_tags["header_month"]):

            for cal_i in range(12):
                day_one = datetime.datetime(self.year, cal_i + 1, 1)
                wd_d1 = day_one.isoweekday() % 7
                for wk_i in range(self.weeks_per_month - 1):
                    for wkd_i in range(7):
                        str_day = f"{day_one.day}"
                        j = cal_i // self.months_per_row
                        ri0 = ri + (j * self.weeks_per_month) + wk_i
                        ci0 = ((cal_i % self.months_per_row) * 7) + wkd_i
                        print(f"{day_one:%Y-%m-%d}, {cal_i=}, {j=}, {ri0=}, {ci0=}, {wk_i=}, {wkd_i=}, {wd_d1=}", end="")
                        month_name = calendar.month_name[cal_i + 1]
                        tag_txt = self.dict_canvas_tags[(ri0, ci0)]["text"]
                        if cal_i != (day_one.month - 1):
                            self.itemconfigure(tag_txt, state="hidden")
                            # day_one += datetime.timedelta(days=1)
                            print(f" -A")
                            continue
                        if (wk_i == 0) and (wd_d1 > 0):
                            wd_d1 -= 1
                            # day_one += datetime.timedelta(days=1)
                            self.itemconfigure(tag_txt, state="hidden")
                            print(f" -B")
                            continue

                        self.itemconfigure(tag_txt, text=str_day)
                        txt = self.itemcget(tag_txt, "text")
                        day_one += datetime.timedelta(days=1)

                        # bbox_month = (
                        #     *self.gc[ri0][ci0][:2],
                        #     *self.gc[ri0][ci0 + 7 - 1][-2:]
                        # )
                        # tag_txt = self.dict_canvas_tags["header_month"][cal_i]["text"]
                        # txt = self.itemcget(tag_txt, "text")
                        print(f" {txt=}")



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
        # df_timeline_order_receive = self.ctk_.df_timeline_order_receive.loc[(self.ctk_.df_timeline_order_receive["DOB"].dt.month == n.month) & (self.ctk_.df_timeline_order_receive["DOB"].dt.day == n.day)]
        # df_timeline_order_receive = df_timeline_order_receive.sort_values(by=["Team", "PlayerLast", "PlayerFirst"])
        # text = ""
        # for k, row in df_timeline_order_receive.iterrows():
        #     # text += f"{row['Team'].center(22)} - {row['PlayerFirst'].rjust(11)} {row['PlayerLast'].ljust(18)}\n"
        #     text += f"{row['Team'].center(22)} - {row['PlayerLast']}, {row['PlayerFirst']}\n"
        # if df_timeline_order_receive.shape[0] == 0:
        #     text = "No Data"
        # self.tb_canvas_click_data.insert("0.0", text)

class FrameBirthdaysView(ctk.CTkScrollableFrame):

    def __init__(self, master: Any, ctk_: App, **kwargs):
        super().__init__(master, **kwargs)

        self.ctk_ = ctk_

        self.owned_numbers = dict()

        for i in range(100):
            self.owned_numbers[i] = 0

        for i, row in self.ctk_.df.iterrows():
            number = row["Number"]
            if not pd.isna(number):
                number = int(number)
                self.owned_numbers[number] += 1

        # self.count_distinct_jerseys = self.ctk_.df_timeline_order_receive.shape[0]
        self.count_distinct_jerseys = self.ctk_.df["Number"].dropna().count()
        self.v_lbl_demo = ctk.StringVar(self, value=f"Total Jerseys ({self.count_distinct_jerseys})")
        self.lbl_demo = ctk.CTkLabel(self, textvariable=self.v_lbl_demo)

        self.w_canvas, self.h_canvas = 600, 700
        # self.n_rows, self.n_cols = 16, 28
        # self.gc = grid_cells(self.w_canvas, self.n_cols, self.h_canvas, self.n_rows, r_type=list)

        self.colour_background_canvas = Colour("#AEBEBE")
        self.colour_background_owned_number_check = Colour("#2A4AFA")
        self.colour_background_owned_number_check_heat_map = Colour("#FA2A4A")

        self.frame_top = ctk.CTkFrame(self)
        self.canvas = CalendarCanvas(
            self.frame_top,
            background=self.colour_background_canvas.hex_code,
            width=self.w_canvas,
            height=self.h_canvas,
            year=2025,
            months_per_row=3
        )
        # self.canvas = ctk.CTkCanvas(
        #     self.frame_top,
        #     background=self.colour_background_canvas.hex_code,
        #     width=self.w_canvas,
        #     height=self.h_canvas
        # )
        self.frame_top_a = ctk.CTkFrame(self.frame_top)
        self.tv_lbl_canvas_click_instruction = ctk.StringVar(self, value=f"Click a Number")
        self.lbl_canvas_click_instruction = ctk.CTkLabel(self.frame_top_a, textvariable=self.tv_lbl_canvas_click_instruction)
        self.tb_canvas_click_data = ctk.CTkTextbox(self.frame_top_a, width=500, font=("Courier", 14))
        self.v_canvas_has_been_clicked = ctk.BooleanVar(self, value=False)

        self.tv_sw_show_heat_map = ctk.StringVar(self, value=f"Heat Map")
        self.v_sw_show_heat_map = ctk.IntVar(self, value=0)

        self.list_own_numbers = sorted(list(self.owned_numbers))
        self.heat_map_colours = self.calc_heat_map_colours()
        self.dict_canvas_tags = dict()
        # for i, row in enumerate(self.gc):
        #     for j, coords in enumerate(row):
        #         n = ((i * self.n_cols) + j) + 1
        #         # if n == 100:
        #         #     # no #100
        #         #     break
        #         x0, y0, x1, y1 = coords
        #         col = self.get_cell_colour(n)
        #         if j // 7 == 2:
        #             col.darkened(0.24)
        #         elif j // 7 == 1:
        #             col.darkened(0.12)
        #         tr = self.canvas.create_rectangle(
        #             x0, y0, x1, y1, fill=col.hex_code
        #         )
        #         tt = self.canvas.create_text(
        #             x0 + ((x1 - x0) / 2), y0 + ((y1 - y0) / 2),
        #             fill=col.font_foreground(rgb=False),
        #             text=f"{n}"
        #         )
        #         self.canvas.tag_bind(
        #             tt,
        #             "<Button-1>",
        #             lambda event, i_=i, j_=j: self.click_canvas(event, i_, j_)
        #         )
        #         self.canvas.tag_bind(
        #             tr,
        #             "<Button-1>",
        #             lambda event, i_=i, j_=j: self.click_canvas(event, i_, j_)
        #         )
        #         self.dict_canvas_tags[(i, j)] = {
        #             "rect": tr,
        #             "text": tt
        #         }



        self.sw_show_heat_map = ctk.CTkSwitch(
            self,
            textvariable=self.tv_sw_show_heat_map,
            variable=self.v_sw_show_heat_map,
            command=self.update_show_heat_map
        )

        self.fig_frame = ctk.CTkFrame(self)
        self.fig = Figure(figsize=(5, 4), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.canvas_fig = FigureCanvasTkAgg(self.fig, master=self.fig_frame)
        self.canvas_fig.draw()

        self.ax.bar(self.list_own_numbers, [self.owned_numbers[n] for n in self.list_own_numbers])
        self.ax.set_xlabel("Jersey #")
        self.ax.set_ylabel("Count")
        self.ax.set_title(f"Jerseys by Number")

        self.lbl_demo.grid(row=0, column=0, rowspan=1, columnspan=1, sticky=ctk.NSEW)
        self.sw_show_heat_map.grid(row=1, column=0, rowspan=1, columnspan=1, sticky=ctk.NSEW)
        self.frame_top.grid(row=2, column=0, rowspan=1, columnspan=1, sticky=ctk.NSEW)
        self.canvas.grid(row=0, column=0, rowspan=1, columnspan=1, sticky=ctk.NSEW)
        self.frame_top_a.grid(row=0, column=1, rowspan=1, columnspan=1, sticky=ctk.NSEW)
        self.lbl_canvas_click_instruction.grid(row=0, column=0, rowspan=1, columnspan=1, sticky=ctk.NSEW)
        self.fig_frame.grid(row=3, column=0, rowspan=1, columnspan=1, sticky=ctk.NSEW)
        self.canvas_fig.get_tk_widget().pack(side=ctk.TOP, fill=ctk.BOTH, expand=1)

    def get_cell_colour(self, n):
        # n is offset by 1
        # if self.owned_numbers[n] > 0:
        #     if self.v_sw_show_heat_map.get():
        #         # return Colour(random_colour(name=True))
        #         return self.heat_map_colours[n]
        #     else:
        #         return self.colour_background_owned_number_check
        # else:
        return self.colour_background_canvas

    def update_show_heat_map(self):
        print(f"update_show_heat_map")
        for i, row in enumerate(self.gc):
            for j, coords in enumerate(row):
                n = ((i * self.n_cols) + j) + 1
                if n == 100:
                    break
                col = self.get_cell_colour(n)
                # self.canvas.itemconfigure(
                #     self.dict_canvas_tags[(i, j)]["rect"],
                #     fill=col.hex_code
                # )
                # self.canvas.itemconfigure(
                #     self.dict_canvas_tags[(i, j)]["text"],
                #     fill=col.font_foreground(rgb=False)
                # )
        # self.id_after_update_show_heat_map = self.after(self.time_after_update_show_heat_map, self.update)

    def calc_heat_map_colours(self):
        max_slices = max(self.owned_numbers.values())
        c1 = self.colour_background_canvas
        c2 = self.colour_background_owned_number_check_heat_map
        grads = [Colour(gradient(i, max_slices, c1, c2, rgb=False)) for i in range(max_slices+1)]
        return {i: grads[n] for i, n in self.owned_numbers.items()}

    def click_canvas(self, event, i, j):
        self.tb_canvas_click_data.delete("0.0", ctk.END)
        n = ((i * self.n_cols) + j) + 1

        if not self.v_canvas_has_been_clicked.get():
            self.lbl_canvas_click_instruction.grid_forget()
            self.tb_canvas_click_data.grid(row=0, column=0, rowspan=1, columnspan=1)
            self.v_canvas_has_been_clicked.set(True)

        n = datetime.datetime(datetime.datetime.now().year, 1, 1) + datetime.timedelta(days=n-1)
        print(f"{n=}")
        df = self.ctk_.df.loc[(self.ctk_.df["DOB"].dt.month == n.month) & (self.ctk_.df["DOB"].dt.day == n.day)]
        df = df.sort_values(by=["Team", "PlayerLast", "PlayerFirst"])
        text = ""
        for k, row in df.iterrows():
            # text += f"{row['Team'].center(22)} - {row['PlayerFirst'].rjust(11)} {row['PlayerLast'].ljust(18)}\n"
            text += f"{row['Team'].center(22)} - {row['PlayerLast']}, {row['PlayerFirst']}\n"
        if df.shape[0] == 0:
            text = "No Data"
        self.tb_canvas_click_data.insert("0.0", text)


if __name__ == '__main__':
    app = App()
    app.mainloop()

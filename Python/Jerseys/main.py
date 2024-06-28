from typing import Any

import pandas as pd
import customtkinter as ctk

from colour_utility import Colour, random_colour, font_foreground, gradient
from tkinter_utility import calc_geometry_tl
from utility import grid_cells

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class App(ctk.CTk):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.title_app_long = f"NHL Jersey Data"
        self.df = pd.read_excel(r"D:\NHL Jerseys.xlsm", sheet_name="JerseyData")
        self.geometry(calc_geometry_tl(0.99, 0.99, parent=self, ask=True))
        # self.geometry(calc_geometry_tl(100, 100, parent=self))
        self.title(self.title_app_long)

        self.tab_name_numbers = f"Numbers"
        self.tab_view_master = ctk.CTkTabview(self)
        self.tab_view_master.add(self.tab_name_numbers)
        self.f_tab_numbers = FrameNumbersView(
            self.tab_view_master.tab(self.tab_name_numbers),
            self,
            width=600,
            height=600
        )

        self.f_tab_numbers.grid(row=0, column=0, rowspan=1, columnspan=1, sticky=ctk.NSEW)
        self.tab_view_master.grid(row=0, column=0, rowspan=1, columnspan=1, sticky=ctk.NSEW)


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

        # self.count_distinct_jerseys = self.ctk_.df.shape[0]
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


if __name__ == '__main__':
    app = App()
    app.mainloop()

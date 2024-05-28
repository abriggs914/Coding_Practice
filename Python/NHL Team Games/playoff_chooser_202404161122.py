import json
import os
import random
import tkinter
from typing import Literal
from json_utility import jsonify

import pandas as pd
from PIL import ImageTk, Image
from itertools import combinations
from random import shuffle, sample
from tkinter import ttk, messagebox

from colour_utility import gradient
from tkinter_utility import calc_geometry_tl, button_factory, entry_factory, checkbox_factory, combo_factory
from utility import clamp, weighted_choice

# def click(t1, t2):
#     default = {
#         "+/-": 0,
#         "+": 0,
#         "-": 0,
#         "wins": [],
#         "%": 0,
#         "losses": []
#     }
#     for t in [t1, t2]:
#         if t not in history:
#             history[t] = {k: v for k, v in default.items()}
#
#     history[t1]["+/-"] += 1
#     history[t1]["+"] += 1
#     history[t1]["wins"].append(t2)
#     history[t1]["%"] = len(history[t1]["wins"]) / (len(history[t1]["wins"]) + len(history[t1]["losses"]))
#
#     history[t2]["+/-"] -= 1
#     history[t2]["-"] += 1
#     history[t2]["losses"].append(t1)
#     history[t2]["%"] = len(history[t2]["wins"]) / (len(history[t1]["wins"]) + len(history[t2]["losses"]))
#
#     next_question()
#
#
# def tie_break(lst):
#     i, c = 0, len(lst)
#     res = []
#     while i < (c - 1):
#         team_1, val1 = lst[i]
#         j = i
#         ties = [lst[i]]
#         while ((i + 1) < c) and (val1 == lst[i + 1][1]):
#             team_2, val2 = lst[i + 1]
#             ties.append(lst[i + 1])
#             # if history[team_1]["wins"]:
#             i += 1
#         i = j + 1
#         res.append((team_1, val1))
#
#
# def show_results():
#
#     frame.pack_forget()
#     top_n = 16
#
#     # -------------------------------
#     # +/-
#
#     frame_results_pm = tkinter.Frame(app, highlightbackground="#010101", highlightthickness=2)
#     label_pm = tkinter.Label(frame_results_pm, text="+/-")
#     frame_top_results_pm = tkinter.Frame(frame_results_pm)
#     frame_bottom_results_pm = tkinter.Frame(frame_results_pm)
#     lbl_1_pm = tkinter.Label(frame_top_results_pm, text=f"Top {top_n}")
#     lbl_2_pm = tkinter.Label(frame_bottom_results_pm, text=f"Bottom {top_n}")
#     lbl_1_pm.pack(side=tkinter.TOP)
#     lbl_2_pm.pack(side=tkinter.TOP)
#     sorted_teams_pm = [(k, v["+/-"]) for k, v in history.items()]
#     sorted_teams_pm.sort(key=lambda tup: tup[1])
#     # sorted_teams_pm = tie_break(sorted_teams_pm)
#
#     # print(f"{history=}\n{sorted_teams_pm=}")
#
#     for team, pm in sorted_teams_pm[len(sorted_teams_pm) - 1: len(sorted_teams_pm) - (top_n + 1): -1]:
#         # print(f"TOP5 {team=}, {pm=}")
#         f = tkinter.Frame(frame_top_results_pm)
#         btn = tkinter.Button(f, image=res_images[team])
#         lbl = tkinter.Label(f, text=f"{pm}")
#         f.pack()
#         btn.pack(side=tkinter.LEFT)
#         lbl.pack(side=tkinter.RIGHT)
#
#     for team, pm in sorted_teams_pm[:top_n]:
#         # print(f"BOT5 {team=}, {pm=}")
#         f = tkinter.Frame(frame_bottom_results_pm)
#         btn = tkinter.Button(f, image=res_images[team])
#         lbl = tkinter.Label(f, text=f"{pm}")
#         f.pack()
#         btn.pack(side=tkinter.LEFT)
#         lbl.pack(side=tkinter.RIGHT)
#
#     frame_results_pm.pack(side=tkinter.LEFT)
#     label_pm.pack(side=tkinter.TOP)
#     frame_top_results_pm.pack(side=tkinter.LEFT)
#     frame_bottom_results_pm.pack(side=tkinter.RIGHT)
#
#     # -------------------------------
#     # Win %
#
#     frame_results_wp = tkinter.Frame(app, highlightbackground="#010101", highlightthickness=2)
#     label_wp = tkinter.Label(frame_results_wp, text="Win %")
#     frame_top_results_wp = tkinter.Frame(frame_results_wp)
#     frame_bottom_results_wp = tkinter.Frame(frame_results_wp)
#     lbl_1_wp = tkinter.Label(frame_top_results_wp, text=f"Top {top_n}")
#     lbl_2_wp = tkinter.Label(frame_bottom_results_wp, text=f"Bottom {top_n}")
#     lbl_1_wp.pack(side=tkinter.TOP)
#     lbl_2_wp.pack(side=tkinter.TOP)
#     sorted_teams_wp = [(k, v["%"]) for k, v in history.items()]
#     sorted_teams_wp.sort(key=lambda tup: tup[1])
#     # sorted_teams_pm = tie_break(sorted_teams_pm)
#
#     # print(f"{history=}\n{sorted_teams_pm=}")
#
#     for team, wp in sorted_teams_wp[len(sorted_teams_wp) - 1: len(sorted_teams_wp) - (top_n + 1): -1]:
#         # print(f"TOP5 {team=}, {wp=}")
#         f = tkinter.Frame(frame_top_results_wp)
#         btn = tkinter.Button(f, image=res_images[team])
#         lbl = tkinter.Label(f, text=f"{wp*100:.2f} %")
#         f.pack()
#         btn.pack(side=tkinter.LEFT)
#         lbl.pack(side=tkinter.RIGHT)
#
#     for team, wp in sorted_teams_wp[:top_n]:
#         # print(f"BOT5 {team=}, {wp=}")
#         f = tkinter.Frame(frame_bottom_results_wp)
#         btn = tkinter.Button(f, image=res_images[team])
#         lbl = tkinter.Label(f, text=f"{wp*100:.2f} %")
#         f.pack()
#         btn.pack(side=tkinter.LEFT)
#         lbl.pack(side=tkinter.RIGHT)
#
#     frame_results_wp.pack(side=tkinter.LEFT)
#     label_wp.pack(side=tkinter.TOP)
#     frame_top_results_wp.pack(side=tkinter.LEFT)
#     frame_bottom_results_wp.pack(side=tkinter.RIGHT)
#
#     # -------------------------------
#     # Picks
#
#     frame_results_np = tkinter.Frame(app, highlightbackground="#010101", highlightthickness=2)
#     label_np = tkinter.Label(frame_results_np, text="# Picks")
#     frame_top_results_np = tkinter.Frame(frame_results_np)
#     frame_bottom_results_np = tkinter.Frame(frame_results_np)
#     lbl_1_np = tkinter.Label(frame_top_results_np, text=f"Top {top_n}")
#     lbl_2_np = tkinter.Label(frame_bottom_results_np, text=f"Bottom {top_n}")
#     lbl_1_np.pack(side=tkinter.TOP)
#     lbl_2_np.pack(side=tkinter.TOP)
#     sorted_teams_np_best = [(k, (v["+"], v["+"] + v["-"])) for k, v in history.items()]
#     sorted_teams_np_worst = [(k, (v["+"], v["+"] + v["-"])) for k, v in history.items()]
#     sorted_teams_np_best.sort(key=lambda tup: (tup[1][0], tup[1][1]))
#     sorted_teams_np_worst.sort(key=lambda tup: (-tup[1][1], tup[1][0]))
#     # sorted_teams_pm = tie_break(sorted_teams_pm)
#
#     # print(f"{history=}\n{sorted_teams_pm=}")
#
#     for team, np in sorted_teams_np_best[len(sorted_teams_np_best) - 1: len(sorted_teams_np_best) - (top_n + 1): -1]:
#         # print(f"TOP5 {team=}, {np=}")
#         f = tkinter.Frame(frame_top_results_np)
#         btn = tkinter.Button(f, image=res_images[team])
#         p, t = np
#         lbl = tkinter.Label(f, text=f"{p} / {t}")
#         f.pack()
#         btn.pack(side=tkinter.LEFT)
#         lbl.pack(side=tkinter.RIGHT)
#
#     for team, np in sorted_teams_np_worst[:top_n]:
#         # print(f"BOT5 {team=}, {np=}")
#         f = tkinter.Frame(frame_bottom_results_np)
#         btn = tkinter.Button(f, image=res_images[team])
#         lbl = tkinter.Label(f, text=f"{np}")
#         f.pack()
#         btn.pack(side=tkinter.LEFT)
#         lbl.pack(side=tkinter.RIGHT)
#
#     frame_results_np.pack(side=tkinter.LEFT)
#     label_np.pack(side=tkinter.TOP)
#     frame_top_results_np.pack(side=tkinter.LEFT)
#     frame_bottom_results_np.pack(side=tkinter.RIGHT)
#
#
# def next_question():
#     global value
#     if not total_games:
#         show_results()
#     else:
#         choice = total_games.pop(0)
#         team_1, team_2 = choice
#         button_1.configure(image=btn_images[team_1], command=lambda t1=team_1, t2=team_2: click(t1, t2))
#         button_2.configure(image=btn_images[team_2], command=lambda t1=team_2, t2=team_1: click(t1, t2))
#         value += (100 * spq)
#         # progressbar.configure(value=value)
#         progressbar["value"] = value
#         # print(f"{progressbar.cget('value')=}")
#         pb_label.configure(text=f"{n_questions - len(total_games)} / {n_questions} -- {value:.2f} %")

bg_canvas = "#686868"
bg_empty_sc = "#D8D525"
bd_empty_sc = "#D89505"
bg_bank_west = "#7793EF"
bg_empty_west = "#25339F"
fg_empty_west = "#000000"
bd_empty_west = "#05134F"
font_empty_west = ("Arial", 14)
bg_bank_east = "#e03535"
bg_empty_east = "#8e1919"
bd_empty_east = "#4F0513"
fg_empty_east = "#000000"
font_empty_east = ("Arial", 14)
bg_line_west = "#000000"
bg_opt_ps_west = "#328944"
bg_line_east = "#000000"
bg_opt_ps_east = "#328944"
bg_btn_sb = "#C7C7C7"
bg_entry_sb = "#E7E7E7"

metropolitan = {
    'Carolina': {'acr': 'CAR', 'mascot': 'Hurricanes', 'masc_short': 'Canes', 'full': 'carolina hurricanes'},
    'New Jersey': {'acr': 'NJD', 'mascot': 'Devils', 'masc_short': 'Devils', 'full': 'new jersey devils'},
    'NY Rangers': {'acr': 'NYR', 'mascot': 'Rangers', 'masc_short': 'Rangers', 'full': 'new york rangers'},
    'Washington': {'acr': 'WSH', 'mascot': 'Capitals', 'masc_short': 'Caps', 'full': 'washington capitals'},
    'NY Islanders': {'acr': 'NYI', 'mascot': 'Islanders', 'masc_short': 'Iles', 'full': 'new york islanders'},
    'Pittsburgh': {'acr': 'PIT', 'mascot': 'Penguins', 'masc_short': 'Pens', 'full': 'pittsburgh penguins'},
    'Philadelphia': {'acr': 'PHI', 'mascot': 'Flyers', 'masc_short': 'Flyers', 'full': 'philadelphia flyers'},
    'Columbus': {'acr': 'CBJ', 'mascot': 'Blue Jackets', 'masc_short': 'Jackets', 'full': 'columbus blue jackets'}
}

atlantic = {
    'Boston': {'acr': 'BOS', 'mascot': 'Bruins', 'masc_short': 'Bruins', 'full': 'boston bruins'},
    'Toronto': {'acr': 'TOR', 'mascot': 'Maple Leafs', 'masc_short': 'Leafs', 'full': 'toronto maple leafs'},
    'Tampa Bay': {'acr': 'TBL', 'mascot': 'Lightning', 'masc_short': 'Bolts', 'full': 'tampa bay lightning'},
    'Buffalo': {'acr': 'BUF', 'mascot': 'Sabres', 'masc_short': 'Sabres', 'full': 'buffalo sabres'},
    'Florida': {'acr': 'FLA', 'mascot': 'Panthers', 'masc_short': 'Panthers', 'full': 'florida panthers'},
    'Detroit': {'acr': 'DET', 'mascot': 'Red Wings', 'masc_short': 'Wings', 'full': 'detroit red wings'},
    'Ottawa': {'acr': 'OTT', 'mascot': 'Senators', 'masc_short': 'Sens', 'full': 'ottawa senators'},
    'Montreal': {'acr': 'MTL', 'mascot': 'Canadiens', 'masc_short': 'Habs', 'full': 'montreal canadiens'}
}

central = {
    'Winnipeg': {'acr': 'WPG', 'mascot': 'Jets', 'masc_short': 'Jets', 'full': 'winnipeg jets'},
    'Dallas': {'acr': 'DAL', 'mascot': 'Stars', 'masc_short': 'Stars', 'full': 'dallas stars'},
    'Minnesota': {'acr': 'MIN', 'mascot': 'Wild', 'masc_short': 'Wild', 'full': 'minnesota wild'},
    'Colorado': {'acr': 'COL', 'mascot': 'Avalanche', 'masc_short': 'Avs', 'full': 'colorado avalanche'},
    'St. Louis': {'acr': 'STL', 'mascot': 'Blues', 'masc_short': 'Blues', 'full': 'st. louis blues'},
    'Nashville': {'acr': 'NSH', 'mascot': 'Predators', 'masc_short': 'Preds', 'full': 'nashville predators'},
    'Arizona': {'acr': 'ARI', 'mascot': 'Coyotes', 'masc_short': 'Coyotes', 'full': 'arizona coyotes'},
    'Chicago': {'acr': 'CHI', 'mascot': 'Blackhawks', 'masc_short': 'Hawks', 'full': 'chicago blackhawks'}
}

pacific = {
    'Vegas': {'acr': 'VGK', 'mascot': 'Golden Knights', 'masc_short': 'Knights', 'full': 'vegas golden knights'},
    'Seattle': {'acr': 'SEA', 'mascot': 'Kraken', 'masc_short': 'Kraken', 'full': 'seattle kraken'},
    'Los Angeles': {'acr': 'LAK', 'mascot': 'Kings', 'masc_short': 'Kings', 'full': 'los angeles kings'},
    'Edmonton': {'acr': 'EDM', 'mascot': 'Oilers', 'masc_short': 'Oilers', 'full': 'edmonton oilers'},
    'Calgary': {'acr': 'CGY', 'mascot': 'Flames', 'masc_short': 'Flames', 'full': 'calgary flames'},
    'Vancouver': {'acr': 'VAN', 'mascot': 'Canucks', 'masc_short': 'Canucks', 'full': 'vancouver canucks'},
    'San Jose': {'acr': 'SJS', 'mascot': 'Sharks', 'masc_short': 'Sharks', 'full': 'san jose sharks'},
    'Anaheim': {'acr': 'ANA', 'mascot': 'Ducks', 'masc_short': 'Ducks', 'full': 'anaheim ducks'}
}

full_team_to_div = {}
full_team_to_div_name = {}
short_name_to_full_name = {}
for div_n, div in {
    "pacific": pacific,
    "central": central,
    "metropolitan": metropolitan,
    "atlantic": atlantic
}.items():
    for t, t_dat in div.items():
        full_name = t_dat["full"].replace(".", "")
        short_name_to_full_name[t] = full_name
        full_team_to_div[full_name] = (t, div)
        full_team_to_div_name[full_name] = div_n
full_team_to_conf = {t: ("w" if div_dat[1] in (pacific, central) else "e") for t, div_dat in full_team_to_div.items()}
west_teams = [t for t, c in full_team_to_conf.items() if c == "w"]
east_teams = [t for t, c in full_team_to_conf.items() if c == "e"]


#
#   Functional SPinBox class using tkinter widgets.
#   Not usable on this project because the widgets are rendered on the top
#
# class SpinBox(tkinter.Frame):
#
#     def __init__(self, master, conf, h, w=2, orientation: Literal["horizontal", "vertical"] = "vertical"):
#         super().__init__(master)
#
#         self.conf = conf
#         self.orientation = tkinter.StringVar(self, value=orientation)
#
#         self.w = w
#         self.h = h
#         self.configure(width=self.w, height=self.h)
#
#         self._min = 4
#         self._max = 7
#
#         self.kwargs_btn = {
#             "background": bg_btn_sb,
#             "width": self.w
#         }
#
#         self.kwargs_entry = {
#             "background": bg_entry_sb,
#             "state": "disabled",
#             "width": self.w,
#             "justify": tkinter.CENTER
#         }
#
#         self.tv_btn_up, self.btn_up = button_factory(
#             self,
#             "^",
#             kwargs_btn=self.kwargs_btn,
#             command=self.click_up
#         )
#
#         self.tv_lbl_entry_num, self.lbl_entry_num, self.tv_entry_num, self.entry_num = entry_factory(
#             self,
#             tv_entry=f"{self._min}",
#             kwargs_entry=self.kwargs_entry
#         )
#
#         self.tv_btn_dn, self.btn_dn = button_factory(
#             self,
#             "v",
#             kwargs_btn=self.kwargs_btn,
#             command=self.click_dn
#         )
#
#         self.btn_up.bind("<MouseWheel>", self.scroll)
#         self.entry_num.bind("<MouseWheel>", self.scroll)
#         self.btn_dn.bind("<MouseWheel>", self.scroll)
#         self.bind("<MouseWheel>", self.scroll)
#
#         self.set_mode()
#
#     def set_mode(self, orientation: Literal["horizontal", "vertical"] = None):
#         self.btn_up.grid_forget()
#         self.entry_num.grid_forget()
#         self.btn_dn.grid_forget()
#
#         if orientation is None:
#             orientation = self.orientation.get()
#
#         if orientation == "vertical":
#             self.btn_up.grid()
#             self.entry_num.grid()
#             self.btn_dn.grid()
#             self.tv_btn_up.set("^")
#             self.tv_btn_dn.set("v")
#         else:
#             self.btn_up.grid(row=0, column=0)
#             self.entry_num.grid(row=0, column=1)
#             self.btn_dn.grid(row=0, column=2)
#             self.tv_btn_up.set("<")
#             self.tv_btn_dn.set(">")
#
#         self.orientation.set(orientation)
#
#     def scroll(self, event):
#         # print(f"scroll, {event=}")
#         x = event.x
#         y = event.y
#         delta = event.delta
#         if delta < 0:
#             self.dec()
#         elif delta > 0:
#             self.inc()
#
#     def inc(self):
#         v = int(self.tv_entry_num.get())
#         self.tv_entry_num.set(max(min(self._max, v + 1), self._min))
#
#     def dec(self):
#         v = int(self.tv_entry_num.get())
#         self.tv_entry_num.set(max(min(self._max, v - 1), self._min))
#
#     def click_up(self):
#         print(f"click up")
#         self.inc()
#
#     def click_dn(self):
#         print(f"click dn")
#         self.dec()


class SpinBox:

    def __init__(self, canvas, conf, x, y, h, w=30, orientation: Literal["horizontal", "vertical"] = "vertical"):

        self.canvas: tkinter.Canvas = canvas
        self.conf = conf
        self._min = 4
        self._max = 7
        self.num = tkinter.IntVar(self.canvas, value=self._min)
        self.orientation = tkinter.StringVar(self.canvas, value="vertical")

        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.bbox = (self.x, self.y, self.x + self.w, self.y + self.h)
        # self.configure(width=self.w, height=self.h)

        self.kwargs_btn = {
            "background": bg_btn_sb,
            "width": self.w
        }

        self.kwargs_entry = {
            "background": bg_entry_sb,
            "state": "disabled",
            "width": self.w,
            "justify": tkinter.CENTER
        }

        t_w = self.w / 3
        t_h = self.h / 3
        h_w = t_w / 2
        h_h = t_h / 2

        self.pos_btn_up = (
            self.x + h_w,
            self.y + h_h
        )

        self.pos_entry_num = (
            self.x + h_w,
            self.y + t_h + h_h
        )

        self.pos_btn_dn = (
            self.x + h_w,
            self.y + (2 * t_h) + h_h
        )
        print(f"pos={self.pos_btn_up}, {self.x=}, {self.y=}, {self.w=}, {self.h=}, {t_w=}, {t_h=}, {h_w=}, {h_h=}")

        self.tag_btn_up = self.canvas.create_rectangle(
            self.pos_btn_up[0] - h_w,
            self.pos_btn_up[1] - h_h,
            self.pos_btn_up[0] + h_w,
            self.pos_btn_up[1] + h_h,
            fill=bg_btn_sb
        )

        self.tag_btn_txt_up = self.canvas.create_text(
            *self.pos_btn_up,
            fill="#000000",
            text="^"
        )

        self.tag_entry_num = self.canvas.create_rectangle(
            self.pos_entry_num[0] - h_w,
            self.pos_entry_num[1] - h_h,
            self.pos_entry_num[0] + h_w,
            self.pos_entry_num[1] + h_h,
            # self.x,
            # self.y + (1 * t_h),
            # self.x + t_w,
            # self.y + (2 * t_h),
            fill=bg_entry_sb
        )

        self.tag_num = self.canvas.create_text(
            # self.x + h_w,
            # self.y + h_h + t_h,
            *self.pos_entry_num,
            fill="#000000",
            text=self.num.get()
        )

        self.tag_btn_dn = self.canvas.create_rectangle(
            self.pos_btn_dn[0] - h_w,
            self.pos_btn_dn[1] - h_h,
            self.pos_btn_dn[0] + h_w,
            self.pos_btn_dn[1] + h_h,
            fill=bg_btn_sb
        )

        self.tag_btn_txt_dn = self.canvas.create_text(
            *self.pos_btn_dn,
            fill="#000000",
            text="v"
        )

        self.bind_btn1_btn_up = self.canvas.tag_bind(self.tag_btn_up, "<Button-1>", self.click_up)
        self.bind_btn1_txt_up = self.canvas.tag_bind(self.tag_btn_txt_up, "<Button-1>", self.click_up)
        # self.canvas.tag_bind(self.tag_btn_up, "<MouseWheel>", self.scroll)
        # self.canvas.tag_bind(self.tag_entry_num, "<MouseWheel>", self.scroll)
        # self.canvas.tag_bind(self.tag_btn_dn, "<MouseWheel>", self.scroll)
        self.bind_btn1_btn_dn = self.canvas.tag_bind(self.tag_btn_dn, "<Button-1>", self.click_dn)
        self.bind_btn1_txt_dn = self.canvas.tag_bind(self.tag_btn_txt_dn, "<Button-1>", self.click_dn)

        # self.tv_btn_up, self.btn_up = button_factory(
        #     self,
        #     "^",
        #     kwargs_btn=self.kwargs_btn,
        #     command=self.click_up
        # )
        #
        # self.tv_lbl_entry_num, self.lbl_entry_num, self.tv_entry_num, self.entry_num = entry_factory(
        #     self,
        #     tv_entry=f"{self._min}",
        #     kwargs_entry=self.kwargs_entry
        # )
        #
        # self.tv_btn_dn, self.btn_dn = button_factory(
        #     self,
        #     "v",
        #     kwargs_btn=self.kwargs_btn,
        #     command=self.click_dn
        # )
        #
        # self.btn_up.bind("<MouseWheel>", self.scroll)
        # self.entry_num.bind("<MouseWheel>", self.scroll)
        # self.btn_dn.bind("<MouseWheel>", self.scroll)
        # self.bind("<MouseWheel>", self.scroll)

        self.set_mode(orientation)

    def set_mode(self, orientation: Literal["horizontal", "vertical"] = None):
        # self.btn_up.grid_forget()
        # self.entry_num.grid_forget()
        # self.btn_dn.grid_forget()

        if orientation is None:
            orientation = self.orientation.get()

        if orientation != self.orientation.get():

            # swap functions
            self.canvas.tag_unbind(self.tag_btn_up, "<Buttom-1>", self.bind_btn1_btn_up)
            self.canvas.tag_unbind(self.tag_btn_txt_up, "<Buttom-1>", self.bind_btn1_txt_up)
            self.canvas.tag_unbind(self.tag_btn_dn, "<Buttom-1>", self.bind_btn1_btn_dn)
            self.canvas.tag_unbind(self.tag_btn_txt_dn, "<Buttom-1>", self.bind_btn1_txt_dn)

            # swap dims
            self.w, self.h = self.h, self.w
            self.bbox = (self.x, self.y, self.x + self.w, self.y + self.h)
            t_w = self.w / 3
            t_h = self.h / 3
            h_w = t_w / 2
            h_h = t_h / 2

            if orientation == "vertical":
                self.pos_btn_up = (
                    self.x + h_w,
                    self.y + h_h
                )

                self.pos_entry_num = (
                    self.x + h_w,
                    self.y + t_h + h_h
                )

                self.pos_btn_dn = (
                    self.x + h_w,
                    self.y + (2 * t_h) + h_h
                )
                self.canvas.itemconfigure(self.tag_btn_txt_up, text="^")
                self.canvas.itemconfigure(self.tag_btn_txt_dn, text="v")

                self.bind_btn1_btn_up = self.canvas.tag_bind(self.tag_btn_up, "<Button-1>", self.click_up)
                self.bind_btn1_txt_up = self.canvas.tag_bind(self.tag_btn_txt_up, "<Button-1>", self.click_up)
                self.bind_btn1_btn_dn = self.canvas.tag_bind(self.tag_btn_dn, "<Button-1>", self.click_dn)
                self.bind_btn1_txt_dn = self.canvas.tag_bind(self.tag_btn_txt_dn, "<Button-1>", self.click_dn)
            else:
                self.pos_btn_up = (
                    self.x + h_w,
                    self.y + h_h
                )

                self.pos_entry_num = (
                    self.x + t_w + h_w,
                    self.y + h_h
                )

                self.pos_btn_dn = (
                    self.x + (2 * t_w) + h_w,
                    self.y + h_h
                )
                self.canvas.itemconfigure(self.tag_btn_txt_up, text="<")
                self.canvas.itemconfigure(self.tag_btn_txt_dn, text=">")

                self.bind_btn1_btn_up = self.canvas.tag_bind(self.tag_btn_up, "<Button-1>", self.click_dn)
                self.bind_btn1_txt_up = self.canvas.tag_bind(self.tag_btn_txt_up, "<Button-1>", self.click_dn)
                self.bind_btn1_btn_dn = self.canvas.tag_bind(self.tag_btn_dn, "<Button-1>", self.click_up)
                self.bind_btn1_txt_dn = self.canvas.tag_bind(self.tag_btn_txt_dn, "<Button-1>", self.click_up)

            self.canvas.coords(
                self.tag_btn_up,
                self.pos_btn_up[0] - h_w,
                self.pos_btn_up[1] - h_h,
                self.pos_btn_up[0] + h_w,
                self.pos_btn_up[1] + h_h
            )

            self.canvas.coords(
                self.tag_entry_num,
                self.pos_entry_num[0] - h_w,
                self.pos_entry_num[1] - h_h,
                self.pos_entry_num[0] + h_w,
                self.pos_entry_num[1] + h_h
            )

            self.canvas.coords(
                self.tag_btn_dn,
                self.pos_btn_dn[0] - h_w,
                self.pos_btn_dn[1] - h_h,
                self.pos_btn_dn[0] + h_w,
                self.pos_btn_dn[1] + h_h
            )

            self.canvas.coords(
                self.tag_num,
                *self.pos_entry_num
            )

            self.canvas.coords(
                self.tag_btn_txt_up,
                *self.pos_btn_up
            )

            self.canvas.coords(
                self.tag_btn_txt_dn,
                *self.pos_btn_dn
            )

            self.orientation.set(orientation)

    def scroll(self, event):
        # print(f"scroll, {event=}")
        x = event.x
        y = event.y
        delta = event.delta
        if delta < 0:
            self.dec()
        elif delta > 0:
            self.inc()

    def show(self):
        for tag in [
            self.tag_btn_up,
            self.tag_btn_txt_up,
            self.tag_num,
            self.tag_entry_num,
            self.tag_btn_dn,
            self.tag_btn_txt_dn
        ]:
            self.canvas.itemconfigure(tag, state="normal")

    def hide(self):
        for tag in [
            self.tag_btn_up,
            self.tag_btn_txt_up,
            self.tag_num,
            self.tag_entry_num,
            self.tag_btn_dn,
            self.tag_btn_txt_dn
        ]:
            self.canvas.itemconfigure(tag, state="hidden")

    def inc(self):
        self.num.set(max(min(self._max, self.num.get() + 1), self._min))
        self.canvas.itemconfigure(self.tag_num, text=self.num.get())

    def dec(self):
        self.num.set(max(min(self._max, self.num.get() - 1), self._min))
        self.canvas.itemconfigure(self.tag_num, text=self.num.get())

    def set(self, val: int):
        self.num.set(clamp(self._min, val, self._max))
        self.canvas.itemconfigure(self.tag_num, text=self.num.get())

    def click_up(self, event):
        print(f"click up")
        self.inc()

    def click_dn(self, event):
        print(f"click dn")
        self.dec()

    def __repr__(self):
        vals = {
            "orientation": self.orientation.get(),
            "num": self.num.get()
        }
        # return f"{vals}"
        return jsonify(vals)


class Lock:

    def __init__(self, canvas: tkinter.Canvas, x, y, w=50, h=50, state="unlocked"):
        self.canvas: tkinter.Canvas = canvas
        self.state = tkinter.BooleanVar(self.canvas, value=state == "locked")

        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.bbox = (self.x, self.y, self.x + self.w, self.y + self.h)

        lbhm, lbvm = 10, 10
        p_box = 0.55
        w_bar = 5
        lbxc = "#111145"
        lbrc = "#33337C"
        diff_ul = 10

        self.pos_bar = {
            True: [
                self.x + lbhm,
                self.y + lbvm,
                self.x + (self.w - (2 * lbhm)),
                self.y + (self.h * clamp(p_box, p_box + 0.15, 1))
            ],
            False: [
                self.x + lbhm,
                self.y + lbvm - diff_ul,
                self.x + (self.w - (2 * lbhm)),
                self.y + (self.h * clamp(p_box, p_box + 0.15, 1)) - diff_ul
            ]
        }

        self.pos_bar_cover = {
            True: [
                self.x + lbhm + w_bar,
                self.y + lbvm + w_bar,
                self.x + (self.w - (2 * lbhm)) - w_bar,
                self.y + (self.h * clamp(p_box, p_box + 0.15, 1)) - w_bar
            ],
            False: [
                self.x + lbhm + w_bar,
                self.y + lbvm + w_bar - diff_ul,
                self.x + (self.w - (2 * lbhm)) - w_bar,
                self.y + (self.h * clamp(p_box, p_box + 0.15, 1)) - w_bar - diff_ul
            ]
        }

        self.pos_bar_vert = {
            True: [
                self.x + (self.w - (2 * lbhm) - w_bar),
                self.y + (self.h * (1 - (p_box + 0.1))),
                self.x + (self.w - (2 * lbhm)),
                self.y + (self.h - lbvm)
            ],
            False: [
                self.x + (self.w - (2 * lbhm) - w_bar),
                self.y + (self.h * (1 - (p_box + 0.1))) - diff_ul,
                self.x + (self.w - (2 * lbhm)),
                self.y + (self.h - lbvm) - diff_ul
            ]
        }

        self.tag_lock_bar_vert = self.canvas.create_rectangle(
            *self.pos_bar_vert[self.state.get()],
            fill=lbrc,
            outline=lbrc
        )

        self.tag_lock_box = self.canvas.create_rectangle(
            self.x + lbhm,
            self.y + (self.h * (1 - p_box)),
            self.x + (self.w - (2 * lbhm)),
            self.y + (self.h - lbvm),
            fill=lbxc
        )

        self.tag_lock_bar = self.canvas.create_arc(
            *self.pos_bar[self.state.get()],
            fill=lbrc,
            outline=lbrc,
            start=0,
            extent=180
        )

        self.tag_lock_bar_cover = self.canvas.create_arc(
            *self.pos_bar_cover[self.state.get()],
            fill=self.canvas.cget("background"),
            outline=self.canvas.cget("background"),
            start=0,
            extent=180
        )

    def set_mode(self, state: bool):
        print(f"set_mode {state=}")
        if state != self.state.get():
            self.canvas.coords(
                self.tag_lock_bar,
                self.pos_bar[state]
            )
            self.canvas.coords(
                self.tag_lock_bar_cover,
                self.pos_bar_cover[state]
            )
            self.canvas.coords(
                self.tag_lock_bar_vert,
                self.pos_bar_vert[state]
            )
            self.state.set(state)

    def __repr__(self):
        vals = {
            "state": self.state.get()
        }
        return jsonify(vals)


class PlayoffChooser(tkinter.Tk):

    def __init__(self, season_stats):
        super().__init__()
        self.season_stats = season_stats
        self.sorted_standings = sorted([(t, p) for t, p in self.season_stats.items()], key=lambda tup: tup[1],
                                       reverse=True)
        self.sorted_west = [tup for tup in self.sorted_standings if tup[0] in west_teams]
        self.sorted_east = [tup for tup in self.sorted_standings if tup[0] in east_teams]
        self.dims_root = 2100, 800
        self.title_app = "2024 Playoff Bracket Challenge"
        self.title(self.title_app)
        # self.calc_geometry = calc_geometry_tl(*self.dims_root, largest=2, rtype=dict)
        # self.calc_geometry = calc_geometry_tl(*self.dims_root, largest=0, rtype=dict)
        self.calc_geometry = calc_geometry_tl(1.0, 1.0, largest=0, rtype=dict)
        self.geometry(self.calc_geometry["geometry"])

        self.unk_team = "no_team"
        self.bg_canvas = bg_canvas
        self.bg_empty_sc = bg_empty_sc
        self.bd_empty_sc = bd_empty_sc
        self.bg_bank_west = bg_bank_west
        self.bg_empty_west = bg_empty_west
        self.fg_empty_west = fg_empty_west
        self.bd_empty_west = bd_empty_west
        self.font_empty_west = font_empty_west
        self.bg_bank_east = bg_bank_east
        self.bg_empty_east = bg_empty_east
        self.bd_empty_east = bd_empty_east
        self.fg_empty_east = fg_empty_east
        self.font_empty_east = font_empty_east
        self.bg_line_west = bg_line_west
        self.bg_opt_ps_west = bg_opt_ps_west
        self.bg_line_east = bg_line_east
        self.bg_opt_ps_east = bg_opt_ps_east
        self.w_line = 2
        self.bw_ps_west = 2
        self.bw_ps_east = 2

        self.w_ps = 75
        self.h_ps = 75
        self.w_space_between_rect = 70
        self.h_space_between_rect = 10
        self.w_canvas, self.h_canvas = self.dims_root[0] * 0.9, self.dims_root[1] * 0.9
        self.pos_bank_west = (25, 25, 205, 25 + (8 * (self.h_ps + self.h_space_between_rect)))
        self.pos_bank_east = (
            self.w_canvas - (25 + 205 + 0),
            25,
            self.w_canvas - (25 + 0),
            25 + (8 * (self.h_ps + self.h_space_between_rect))
        )

        #### NOTE ####
        # Stanley Cup Final PlayOff Spot is treated as though it is in the west conference

        # West PlayOff Spot Xs
        self.x_ps_w_r1 = self.pos_bank_west[2] + self.w_space_between_rect
        self.x_ps_w_r2 = self.x_ps_w_r1 + self.w_ps + self.w_space_between_rect
        self.x_ps_w_r3 = self.x_ps_w_r2 + self.w_ps + self.w_space_between_rect
        self.x_ps_w_r4 = self.x_ps_w_r3 + self.w_ps + self.w_space_between_rect
        self.x_ps_sc = self.x_ps_w_r4 + self.w_ps + self.w_space_between_rect

        # East PlayOff Spot Xs
        # self.x_ps_e_r4 = self.pos_bank_east[2] + self.w_space_between_rect
        self.x_ps_e_r4 = self.x_ps_sc + self.w_ps + self.w_space_between_rect
        self.x_ps_e_r3 = self.x_ps_e_r4 + self.w_ps + self.w_space_between_rect
        self.x_ps_e_r2 = self.x_ps_e_r3 + self.w_ps + self.w_space_between_rect
        self.x_ps_e_r1 = self.x_ps_e_r2 + self.w_ps + self.w_space_between_rect

        # West PlayOff Spot Ys R1
        self.y_ps_wc_t_r1 = self.pos_bank_west[1] + (self.h_space_between_rect / 2)
        self.y_ps_p1_r1 = self.y_ps_wc_t_r1 + self.h_ps + self.h_space_between_rect
        self.y_ps_p2_r1 = self.y_ps_wc_t_r1 + (2 * (self.h_ps + self.h_space_between_rect))
        self.y_ps_p3_r1 = self.y_ps_wc_t_r1 + (3 * (self.h_ps + self.h_space_between_rect))
        self.y_ps_c3_r1 = self.y_ps_wc_t_r1 + (4 * (self.h_ps + self.h_space_between_rect))
        self.y_ps_c2_r1 = self.y_ps_wc_t_r1 + (5 * (self.h_ps + self.h_space_between_rect))
        self.y_ps_c1_r1 = self.y_ps_wc_t_r1 + (6 * (self.h_ps + self.h_space_between_rect))
        self.y_ps_w_wc_b_r1 = self.y_ps_wc_t_r1 + (7 * (self.h_ps + self.h_space_between_rect))

        # West PlayOff Spot Ys R1
        self.y_ps_e_wc_t_r1 = self.pos_bank_east[1] + (self.h_space_between_rect / 2)
        self.y_ps_a1_r1 = self.y_ps_e_wc_t_r1 + self.h_ps + self.h_space_between_rect
        self.y_ps_a2_r1 = self.y_ps_e_wc_t_r1 + (2 * (self.h_ps + self.h_space_between_rect))
        self.y_ps_a3_r1 = self.y_ps_e_wc_t_r1 + (3 * (self.h_ps + self.h_space_between_rect))
        self.y_ps_m3_r1 = self.y_ps_e_wc_t_r1 + (4 * (self.h_ps + self.h_space_between_rect))
        self.y_ps_m2_r1 = self.y_ps_e_wc_t_r1 + (5 * (self.h_ps + self.h_space_between_rect))
        self.y_ps_m1_r1 = self.y_ps_e_wc_t_r1 + (6 * (self.h_ps + self.h_space_between_rect))
        self.y_ps_e_wc_b_r1 = self.y_ps_e_wc_t_r1 + (7 * (self.h_ps + self.h_space_between_rect))

        # West PlayOff Spot Ys R1
        self.y_ps_w_r2_p1 = self.y_ps_wc_t_r1 + ((self.y_ps_p1_r1 - self.y_ps_wc_t_r1) / 2)
        self.y_ps_w_r2_p2 = self.y_ps_p2_r1 + ((self.y_ps_p3_r1 - self.y_ps_p2_r1) / 2)
        self.y_ps_w_r2_c2 = self.y_ps_c3_r1 + ((self.y_ps_c2_r1 - self.y_ps_c3_r1) / 2)
        self.y_ps_w_r2_c1 = self.y_ps_c1_r1 + ((self.y_ps_w_wc_b_r1 - self.y_ps_c1_r1) / 2)

        # East PlayOff Spot Ys R1
        self.y_ps_e_r2_a1 = self.y_ps_e_wc_t_r1 + ((self.y_ps_a1_r1 - self.y_ps_e_wc_t_r1) / 2)
        self.y_ps_e_r2_a2 = self.y_ps_a2_r1 + ((self.y_ps_a3_r1 - self.y_ps_a2_r1) / 2)
        self.y_ps_e_r2_m2 = self.y_ps_m3_r1 + ((self.y_ps_m2_r1 - self.y_ps_m3_r1) / 2)
        self.y_ps_e_r2_m1 = self.y_ps_m1_r1 + ((self.y_ps_e_wc_b_r1 - self.y_ps_m1_r1) / 2)

        # West PlayOff Spot Ys R2
        self.y_ps_w_r3_p = self.y_ps_w_r2_p1 + ((self.y_ps_w_r2_p2 - self.y_ps_w_r2_p1) / 2)
        self.y_ps_w_r3_c = self.y_ps_w_r2_c1 + ((self.y_ps_w_r2_c2 - self.y_ps_w_r2_c1) / 2)

        # East PlayOff Spot Ys R2
        self.y_ps_e_r3_a = self.y_ps_e_r2_a1 + ((self.y_ps_e_r2_a2 - self.y_ps_e_r2_a1) / 2)
        self.y_ps_e_r3_m = self.y_ps_e_r2_m1 + ((self.y_ps_e_r2_m2 - self.y_ps_e_r2_m1) / 2)

        # West PlayOff Spot Ys R3
        self.y_ps_w_r4_w = self.y_ps_w_r3_p + ((self.y_ps_w_r3_c - self.y_ps_w_r3_p) / 2)

        # East PlayOff Spot Ys R3
        self.y_ps_e_r4_e = self.y_ps_e_r3_a + ((self.y_ps_e_r3_m - self.y_ps_e_r3_a) / 2)

        # West PlayOff Spot Ys SC
        self.y_ps_sc = self.y_ps_w_r3_p + ((self.y_ps_w_r3_c - self.y_ps_w_r3_p) / 2)

        print(f"{self.x_ps_w_r1=}, {self.y_ps_wc_t_r1=}")
        print(f"{self.x_ps_w_r2=}, {self.y_ps_p1_r1=}")
        print(f"{self.x_ps_w_r3=}, {self.y_ps_p2_r1=}")
        print(f"{self.x_ps_w_r4=}, {self.y_ps_p3_r1=}")

        self.history_file = r"playoff chooser history.json"
        self.image_directory = r"C:\Users\abrig\Documents\Coding_Practice\Python\Hockey pool\Images"
        self.btn_images = {}
        self.res_images = {}
        self.res_img_to_t = {}
        self.res_pyimage_to_t = {}
        self.history = {}
        self.full_size_image = (200, 200)
        self.small_size_image = (self.w_ps, self.h_ps)

        self.load_history()
        self.load_images()
        print(f"{self.sorted_west=}")
        print(f"{self.sorted_east=}")

        print(f"{full_team_to_div=}\n{full_team_to_div_name=}\n{full_team_to_conf=}\n{west_teams=}\n{east_teams=}")

        # sample_west_teams = random.sample(west_teams, 8)
        sample_west_teams = [t for t, p in self.sorted_west]

        self.dragging = tkinter.BooleanVar(self, value=False)
        self.drag_team = tkinter.StringVar(self, value="")

        self.canvas = tkinter.Canvas(
            self,
            width=self.w_canvas,
            height=self.h_canvas,
            background=self.bg_canvas
        )

        # west team bank
        self.rect_w_bank = self.canvas.create_rectangle(
            *self.pos_bank_west,
            fill=self.bg_bank_west
        )

        # east team bank
        self.rect_e_bank = self.canvas.create_rectangle(
            *self.pos_bank_east,
            fill=self.bg_bank_east
        )

        self.drag_rect = self.canvas.create_image(
            0, 0,
            image=self.res_images[self.sorted_west[0][0]],
            state="hidden"
        )

        self.template_ps_data = {
            "x0": None,
            "y0": None,
            "x1": None,
            "y1": None,
            "image": None,
            "text": None,
            "tag_rect": None,
            "tag_text": None,
            "tag_image": None,
            "is_wc": None
        }
        self.ps_codes = {
            "west": {
                0: {k: self.template_ps_data.copy() for k in ["WC_t", "P1", "P2", "P3", "C3", "C2", "C1", "WC_b"]},
                1: {k: self.template_ps_data.copy() for k in ["P1", "P2", "C2", "C1"]},
                2: {k: self.template_ps_data.copy() for k in ["P", "C"]},
                3: {k: self.template_ps_data.copy() for k in ["W"]},
                4: {k: self.template_ps_data.copy() for k in ["SC"]}
            },
            "east": {
                0: {k: self.template_ps_data.copy() for k in ["WC_t", "A1", "A2", "A3", "M3", "M2", "M1", "WC_b"]},
                1: {k: self.template_ps_data.copy() for k in ["A1", "A2", "M2", "M1"]},
                2: {k: self.template_ps_data.copy() for k in ["A", "M"]},
                3: {k: self.template_ps_data.copy() for k in ["E"]}
            }
            # ,
            # "east": {"R1": {k: self.template_ps_data.copy() for k in ["WC_t", "A1", "A2", "A3", "M3", "M2", "M1", "WC_b"]}}
        }

        # Round 1

        # west wildcard top
        self.ps_codes["west"][0]["WC_t"].update({
            "x0": self.x_ps_w_r1,
            "y0": self.y_ps_wc_t_r1,
            "x1": self.x_ps_w_r1 + self.w_ps,
            "y1": self.y_ps_wc_t_r1 + self.h_ps,
            "text": "WC"
        })

        # pacific 1
        self.ps_codes["west"][0]["P1"].update({
            "x0": self.x_ps_w_r1,
            "y0": self.y_ps_p1_r1,
            "x1": self.x_ps_w_r1 + self.w_ps,
            "y1": self.y_ps_p1_r1 + self.h_ps,
            "text": "P1"
        })

        # pacific 2
        self.ps_codes["west"][0]["P2"].update({
            "x0": self.x_ps_w_r1,
            "y0": self.y_ps_p2_r1,
            "x1": self.x_ps_w_r1 + self.w_ps,
            "y1": self.y_ps_p2_r1 + self.h_ps,
            "text": "P2"
        })

        # pacific 3
        self.ps_codes["west"][0]["P3"].update({
            "x0": self.x_ps_w_r1,
            "y0": self.y_ps_p3_r1,
            "x1": self.x_ps_w_r1 + self.w_ps,
            "y1": self.y_ps_p3_r1 + self.h_ps,
            "text": "P3"
        })

        # central 3
        self.ps_codes["west"][0]["C3"].update({
            "x0": self.x_ps_w_r1,
            "y0": self.y_ps_c3_r1,
            "x1": self.x_ps_w_r1 + self.w_ps,
            "y1": self.y_ps_c3_r1 + self.h_ps,
            "text": "C3"
        })

        # central 2
        self.ps_codes["west"][0]["C2"].update({
            "x0": self.x_ps_w_r1,
            "y0": self.y_ps_c2_r1,
            "x1": self.x_ps_w_r1 + self.w_ps,
            "y1": self.y_ps_c2_r1 + self.h_ps,
            "text": "C2"
        })

        # central 1
        self.ps_codes["west"][0]["C1"].update({
            "x0": self.x_ps_w_r1,
            "y0": self.y_ps_c1_r1,
            "x1": self.x_ps_w_r1 + self.w_ps,
            "y1": self.y_ps_c1_r1 + self.h_ps,
            "text": "C1"
        })

        # west wild card bottom
        self.ps_codes["west"][0]["WC_b"].update({
            "x0": self.x_ps_w_r1,
            "y0": self.y_ps_w_wc_b_r1,
            "x1": self.x_ps_w_r1 + self.w_ps,
            "y1": self.y_ps_w_wc_b_r1 + self.h_ps,
            "text": "WC"
        })

        # Round 2

        # pacific seed 1
        self.ps_codes["west"][1]["P1"].update({
            "x0": self.x_ps_w_r2,
            "y0": self.y_ps_w_r2_p1,
            "x1": self.x_ps_w_r2 + self.w_ps,
            "y1": self.y_ps_w_r2_p1 + self.h_ps,
            "text": "P1"
        })

        # pacific seed 2
        self.ps_codes["west"][1]["P2"].update({
            "x0": self.x_ps_w_r2,
            "y0": self.y_ps_w_r2_p2,
            "x1": self.x_ps_w_r2 + self.w_ps,
            "y1": self.y_ps_w_r2_p2 + self.h_ps,
            "text": "P2"
        })

        # central seed 1
        self.ps_codes["west"][1]["C2"].update({
            "x0": self.x_ps_w_r2,
            "y0": self.y_ps_w_r2_c2,
            "x1": self.x_ps_w_r2 + self.w_ps,
            "y1": self.y_ps_w_r2_c2 + self.h_ps,
            "text": "C2"
        })

        # central seed 2
        self.ps_codes["west"][1]["C1"].update({
            "x0": self.x_ps_w_r2,
            "y0": self.y_ps_w_r2_c1,
            "x1": self.x_ps_w_r2 + self.w_ps,
            "y1": self.y_ps_w_r2_c1 + self.h_ps,
            "text": "C1"
        })

        # Round 3

        # pacific seed
        self.ps_codes["west"][2]["P"].update({
            "x0": self.x_ps_w_r3,
            "y0": self.y_ps_w_r3_p,
            "x1": self.x_ps_w_r3 + self.w_ps,
            "y1": self.y_ps_w_r3_p + self.h_ps,
            "text": "P"
        })

        # central seed
        self.ps_codes["west"][2]["C"].update({
            "x0": self.x_ps_w_r3,
            "y0": self.y_ps_w_r3_c,
            "x1": self.x_ps_w_r3 + self.w_ps,
            "y1": self.y_ps_w_r3_c + self.h_ps,
            "text": "C"
        })

        # Round 4

        # west seed
        self.ps_codes["west"][3]["W"].update({
            "x0": self.x_ps_w_r4,
            "y0": self.y_ps_w_r4_w,
            "x1": self.x_ps_w_r4 + self.w_ps,
            "y1": self.y_ps_w_r4_w + self.h_ps,
            "text": "W"
        })

        # Round 5

        # Stanley Cup Winner
        self.ps_codes["west"][4]["SC"].update({
            "x0": self.x_ps_sc,
            "y0": self.y_ps_sc,
            "x1": self.x_ps_sc + self.w_ps,
            "y1": self.y_ps_sc + self.h_ps,
            "text": "SC"
        })

        ################################################################

        # Round 1

        # east wildcard top
        self.ps_codes["east"][0]["WC_t"].update({
            "x0": self.x_ps_e_r1,
            "y0": self.y_ps_e_wc_t_r1,
            "x1": self.x_ps_e_r1 + self.w_ps,
            "y1": self.y_ps_e_wc_t_r1 + self.h_ps,
            "text": "WC"
        })

        # atlantic 1
        self.ps_codes["east"][0]["A1"].update({
            "x0": self.x_ps_e_r1,
            "y0": self.y_ps_a1_r1,
            "x1": self.x_ps_e_r1 + self.w_ps,
            "y1": self.y_ps_a1_r1 + self.h_ps,
            "text": "A1"
        })

        # atlantic 2
        self.ps_codes["east"][0]["A2"].update({
            "x0": self.x_ps_e_r1,
            "y0": self.y_ps_a2_r1,
            "x1": self.x_ps_e_r1 + self.w_ps,
            "y1": self.y_ps_a2_r1 + self.h_ps,
            "text": "A2"
        })

        # atlantic 3
        self.ps_codes["east"][0]["A3"].update({
            "x0": self.x_ps_e_r1,
            "y0": self.y_ps_a3_r1,
            "x1": self.x_ps_e_r1 + self.w_ps,
            "y1": self.y_ps_a3_r1 + self.h_ps,
            "text": "A3"
        })

        # metropolitan 3
        self.ps_codes["east"][0]["M3"].update({
            "x0": self.x_ps_e_r1,
            "y0": self.y_ps_m3_r1,
            "x1": self.x_ps_e_r1 + self.w_ps,
            "y1": self.y_ps_m3_r1 + self.h_ps,
            "text": "M3"
        })

        # metropolitan 2
        self.ps_codes["east"][0]["M2"].update({
            "x0": self.x_ps_e_r1,
            "y0": self.y_ps_m2_r1,
            "x1": self.x_ps_e_r1 + self.w_ps,
            "y1": self.y_ps_m2_r1 + self.h_ps,
            "text": "M2"
        })

        # metropolitan 1
        self.ps_codes["east"][0]["M1"].update({
            "x0": self.x_ps_e_r1,
            "y0": self.y_ps_m1_r1,
            "x1": self.x_ps_e_r1 + self.w_ps,
            "y1": self.y_ps_m1_r1 + self.h_ps,
            "text": "M1"
        })

        # east wild card bottom
        self.ps_codes["east"][0]["WC_b"].update({
            "x0": self.x_ps_e_r1,
            "y0": self.y_ps_e_wc_b_r1,
            "x1": self.x_ps_e_r1 + self.w_ps,
            "y1": self.y_ps_e_wc_b_r1 + self.h_ps,
            "text": "WC"
        })

        # Round 2

        # atlantic seed 1
        self.ps_codes["east"][1]["A1"].update({
            "x0": self.x_ps_e_r2,
            "y0": self.y_ps_e_r2_a1,
            "x1": self.x_ps_e_r2 + self.w_ps,
            "y1": self.y_ps_e_r2_a1 + self.h_ps,
            "text": "A1"
        })

        # atlantic seed 2
        self.ps_codes["east"][1]["A2"].update({
            "x0": self.x_ps_e_r2,
            "y0": self.y_ps_e_r2_a2,
            "x1": self.x_ps_e_r2 + self.w_ps,
            "y1": self.y_ps_e_r2_a2 + self.h_ps,
            "text": "A2"
        })

        # metropolitan seed 1
        self.ps_codes["east"][1]["M2"].update({
            "x0": self.x_ps_e_r2,
            "y0": self.y_ps_e_r2_m2,
            "x1": self.x_ps_e_r2 + self.w_ps,
            "y1": self.y_ps_e_r2_m2 + self.h_ps,
            "text": "M2"
        })

        # metropolitan seed 2
        self.ps_codes["east"][1]["M1"].update({
            "x0": self.x_ps_e_r2,
            "y0": self.y_ps_e_r2_m1,
            "x1": self.x_ps_e_r2 + self.w_ps,
            "y1": self.y_ps_e_r2_m1 + self.h_ps,
            "text": "M1"
        })

        # Round 3

        # atlantic seed
        self.ps_codes["east"][2]["A"].update({
            "x0": self.x_ps_e_r3,
            "y0": self.y_ps_e_r3_a,
            "x1": self.x_ps_e_r3 + self.w_ps,
            "y1": self.y_ps_e_r3_a + self.h_ps,
            "text": "A"
        })

        # metropolitan seed
        self.ps_codes["east"][2]["M"].update({
            "x0": self.x_ps_e_r3,
            "y0": self.y_ps_e_r3_m,
            "x1": self.x_ps_e_r3 + self.w_ps,
            "y1": self.y_ps_e_r3_m + self.h_ps,
            "text": "M"
        })

        # Round 4

        # east seed
        self.ps_codes["east"][3]["E"].update({
            "x0": self.x_ps_e_r4,
            "y0": self.y_ps_e_r4_e,
            "x1": self.x_ps_e_r4 + self.w_ps,
            "y1": self.y_ps_e_r4_e + self.h_ps,
            "text": "E"
        })

        ##############################################################

        for conf, conf_data in self.ps_codes.items():
            for rnd, round_data in conf_data.items():
                for ps_code, ps_data in round_data.items():
                    print(f"{conf=}, {rnd=}, {ps_code=}")

                    t_rect = self.canvas.create_rectangle(
                        ps_data["x0"],
                        ps_data["y0"],
                        ps_data["x1"],
                        ps_data["y1"],
                        fill=self.bg_empty_east if conf == "east" else self.bg_empty_west,
                        width=self.bw_ps_east if conf == "east" else self.bw_ps_west
                    )
                    t_text = self.canvas.create_text(
                        ps_data["x0"] + (self.w_ps / 2),
                        ps_data["y0"] + (self.h_ps / 2),
                        text=ps_data["text"]
                    )
                    t_img = self.canvas.create_image(
                        ps_data["x0"] + (self.w_ps / 2),
                        ps_data["y0"] + (self.h_ps / 2),
                        state="hidden"
                    )

                    if rnd > 0:
                        # spinbox
                        sb_w = 15
                        orientation = "vertical"
                        if conf == "east":
                            sb_x = ps_data["x1"]  # + sb_w
                            sb_y = ps_data["y0"]  # + (self.h_ps / 2)
                        else:
                            if ps_code == "SC":
                                orientation = "horizontal"
                                sb_x = ps_data["x0"]  # + (self.w_ps / 2)
                                sb_y = ps_data["y1"]  # + sb_w
                            else:
                                sb_x = ps_data["x0"] - (sb_w / 2)
                                sb_y = ps_data["y0"]  # + (self.h_ps / 2)

                        sb = SpinBox(
                            self.canvas,
                            "west",
                            sb_x,
                            sb_y,
                            self.h_ps,
                            orientation=orientation
                        )
                        sb.hide()
                        # self.canvas.create_window(sb_x, sb_y, window=sb)

                        lock_x = ps_data["x0"] + (self.w_ps / 2)
                        lock_y = ps_data["y0"] - 50
                    else:
                        sb = None
                        if conf == "east":
                            lock_x = ps_data["x1"] + 10
                            lock_y = ps_data["y0"] + (self.h_ps / 6)
                        else:
                            lock_x = ps_data["x0"] - 40
                            lock_y = ps_data["y0"] + (self.h_ps / 6)

                    # lock
                    lock = Lock(
                        self.canvas,
                        lock_x,
                        lock_y
                    )

                    self.ps_codes[conf][rnd][ps_code].update({
                        "tag_rect": t_rect,
                        "tag_text": t_text,
                        "tag_image": t_img,
                        "sb": sb,
                        "lock": lock
                    })
                    self.canvas.tag_bind(
                        t_img,
                        "<Button-1>",
                        lambda event, cc=conf, rc=rnd, pc=ps_code:
                        self.click_ps(event, cc, rc, pc)
                    )
                    self.canvas.tag_bind(
                        t_img,
                        "<B1-Motion>",
                        lambda event, cc=conf, rc=rnd, pc=ps_code:
                        self.motion_ps(event, cc, rc, pc)
                    )

        self.canvas.itemconfigure(
            self.ps_codes["west"][4]["SC"]["tag_rect"],
            fill=self.bg_empty_sc
        )

        # Lines
        self.lines = dict()

        # west R1 WC top to R2 P1
        self.lines[(("west", 0, "WC_t"), ("west", 1, "P1"))] = self.canvas.create_line(
            self.x_ps_w_r1 + self.w_ps,
            self.y_ps_wc_t_r1 + (self.h_ps / 2),
            self.x_ps_w_r2,
            self.y_ps_w_r2_p1 + (self.h_ps / 2)
        )

        # west R1 P1 to R2 P1
        self.lines[(("west", 0, "P1"), ("west", 1, "P1"))] = self.canvas.create_line(
            self.x_ps_w_r1 + self.w_ps,
            self.y_ps_p1_r1 + (self.h_ps / 2),
            self.x_ps_w_r2,
            self.y_ps_w_r2_p1 + (self.h_ps / 2)
        )

        # west R1 P2 to R2 P2
        self.lines[(("west", 0, "P2"), ("west", 1, "P2"))] = self.canvas.create_line(
            self.x_ps_w_r1 + self.w_ps,
            self.y_ps_p2_r1 + (self.h_ps / 2),
            self.x_ps_w_r2,
            self.y_ps_w_r2_p2 + (self.h_ps / 2)
        )

        # west R1 P3 to R2 P2
        self.lines[(("west", 0, "P3"), ("west", 1, "P2"))] = self.canvas.create_line(
            self.x_ps_w_r1 + self.w_ps,
            self.y_ps_p3_r1 + (self.h_ps / 2),
            self.x_ps_w_r2,
            self.y_ps_w_r2_p2 + (self.h_ps / 2)
        )

        # west R1 C3 to R2 C2
        self.lines[(("west", 0, "C3"), ("west", 1, "C2"))] = self.canvas.create_line(
            self.x_ps_w_r1 + self.w_ps,
            self.y_ps_c3_r1 + (self.h_ps / 2),
            self.x_ps_w_r2,
            self.y_ps_w_r2_c2 + (self.h_ps / 2)
        )

        # west R1 C2 to R2 C2
        self.lines[(("west", 0, "C2"), ("west", 1, "C2"))] = self.canvas.create_line(
            self.x_ps_w_r1 + self.w_ps,
            self.y_ps_c2_r1 + (self.h_ps / 2),
            self.x_ps_w_r2,
            self.y_ps_w_r2_c2 + (self.h_ps / 2)
        )

        # west R1 C1 to R2 C1
        self.lines[(("west", 0, "C1"), ("west", 1, "C1"))] = self.canvas.create_line(
            self.x_ps_w_r1 + self.w_ps,
            self.y_ps_c1_r1 + (self.h_ps / 2),
            self.x_ps_w_r2,
            self.y_ps_w_r2_c1 + (self.h_ps / 2)
        )

        # west R1 WC bottom to R2 C1
        self.lines[(("west", 0, "WC_b"), ("west", 1, "C1"))] = self.canvas.create_line(
            self.x_ps_w_r1 + self.w_ps,
            self.y_ps_w_wc_b_r1 + (self.h_ps / 2),
            self.x_ps_w_r2,
            self.y_ps_w_r2_c1 + (self.h_ps / 2)
        )

        # west R2 P1 to R3 P
        self.lines[(("west", 1, "P1"), ("west", 2, "P"))] = self.canvas.create_line(
            self.x_ps_w_r2 + self.w_ps,
            self.y_ps_w_r2_p1 + (self.h_ps / 2),
            self.x_ps_w_r3,
            self.y_ps_w_r3_p + (self.h_ps / 2)
        )

        # west R2 P2 to R3 P
        self.lines[(("west", 1, "P2"), ("west", 2, "P"))] = self.canvas.create_line(
            self.x_ps_w_r2 + self.w_ps,
            self.y_ps_w_r2_p2 + (self.h_ps / 2),
            self.x_ps_w_r3,
            self.y_ps_w_r3_p + (self.h_ps / 2)
        )

        # west R2 C2 to R3 C
        self.lines[(("west", 1, "C2"), ("west", 2, "C"))] = self.canvas.create_line(
            self.x_ps_w_r2 + self.w_ps,
            self.y_ps_w_r2_c2 + (self.h_ps / 2),
            self.x_ps_w_r3,
            self.y_ps_w_r3_c + (self.h_ps / 2)
        )

        # west R2 C1 to R3 C
        self.lines[(("west", 1, "C1"), ("west", 2, "C"))] = self.canvas.create_line(
            self.x_ps_w_r2 + self.w_ps,
            self.y_ps_w_r2_c1 + (self.h_ps / 2),
            self.x_ps_w_r3,
            self.y_ps_w_r3_c + (self.h_ps / 2)
        )

        # west R3 P to R4 W
        self.lines[(("west", 2, "P"), ("west", 3, "W"))] = self.canvas.create_line(
            self.x_ps_w_r3 + self.w_ps,
            self.y_ps_w_r3_p + (self.h_ps / 2),
            self.x_ps_w_r4,
            self.y_ps_w_r4_w + (self.h_ps / 2)
        )

        # west R3 C to R4 W
        self.lines[(("west", 2, "C"), ("west", 3, "W"))] = self.canvas.create_line(
            self.x_ps_w_r3 + self.w_ps,
            self.y_ps_w_r3_c + (self.h_ps / 2),
            self.x_ps_w_r4,
            self.y_ps_w_r4_w + (self.h_ps / 2)
        )

        # west R4 W to R5 SC
        self.lines[(("west", 3, "W"), ("west", 4, "SC"))] = self.canvas.create_line(
            self.x_ps_w_r4 + self.w_ps,
            self.y_ps_w_r4_w + (self.h_ps / 2),
            self.x_ps_sc,
            self.y_ps_sc + (self.h_ps / 2)
        )

        ######################################################################################

        # east R1 WC top to R2 A1
        self.lines[(("east", 0, "WC_t"), ("east", 1, "A1"))] = self.canvas.create_line(
            self.x_ps_e_r1,
            self.y_ps_e_wc_t_r1 + (self.h_ps / 2),
            self.x_ps_e_r2 + self.w_ps,
            self.y_ps_e_r2_a1 + (self.h_ps / 2)
        )

        # east R1 A1 to R2 A1
        self.lines[(("east", 0, "A1"), ("east", 1, "A1"))] = self.canvas.create_line(
            self.x_ps_e_r1,
            self.y_ps_a1_r1 + (self.h_ps / 2),
            self.x_ps_e_r2 + self.w_ps,
            self.y_ps_e_r2_a1 + (self.h_ps / 2)
        )

        # east R1 A2 to R2 A2
        self.lines[(("east", 0, "A2"), ("east", 1, "A2"))] = self.canvas.create_line(
            self.x_ps_e_r1,
            self.y_ps_a2_r1 + (self.h_ps / 2),
            self.x_ps_e_r2 + self.w_ps,
            self.y_ps_e_r2_a2 + (self.h_ps / 2)
        )

        # east R1 A3 to R2 A2
        self.lines[(("east", 0, "A3"), ("east", 1, "A2"))] = self.canvas.create_line(
            self.x_ps_e_r1,
            self.y_ps_a3_r1 + (self.h_ps / 2),
            self.x_ps_e_r2 + self.w_ps,
            self.y_ps_e_r2_a2 + (self.h_ps / 2)
        )

        # east R1 M3 to R2 M2
        self.lines[(("east", 0, "M3"), ("east", 1, "M2"))] = self.canvas.create_line(
            self.x_ps_e_r1,
            self.y_ps_m3_r1 + (self.h_ps / 2),
            self.x_ps_e_r2 + self.w_ps,
            self.y_ps_e_r2_m2 + (self.h_ps / 2)
        )

        # east R1 M2 to R2 M2
        self.lines[(("east", 0, "M2"), ("east", 1, "M2"))] = self.canvas.create_line(
            self.x_ps_e_r1,
            self.y_ps_m2_r1 + (self.h_ps / 2),
            self.x_ps_e_r2 + self.w_ps,
            self.y_ps_e_r2_m2 + (self.h_ps / 2)
        )

        # east R1 M1 to R2 M1
        self.lines[(("east", 0, "M1"), ("east", 1, "M1"))] = self.canvas.create_line(
            self.x_ps_e_r1,
            self.y_ps_m1_r1 + (self.h_ps / 2),
            self.x_ps_e_r2 + self.w_ps,
            self.y_ps_e_r2_m1 + (self.h_ps / 2)
        )

        # east R1 WC bottom to R2 M1
        self.lines[(("east", 0, "WC_b"), ("east", 1, "M1"))] = self.canvas.create_line(
            self.x_ps_e_r1,
            self.y_ps_e_wc_b_r1 + (self.h_ps / 2),
            self.x_ps_e_r2 + self.w_ps,
            self.y_ps_e_r2_m1 + (self.h_ps / 2)
        )

        # east R2 A1 to R3 A
        self.lines[(("east", 1, "A1"), ("east", 2, "A"))] = self.canvas.create_line(
            self.x_ps_e_r2,
            self.y_ps_e_r2_a1 + (self.h_ps / 2),
            self.x_ps_e_r3 + self.w_ps,
            self.y_ps_e_r3_a + (self.h_ps / 2)
        )

        # east R2 A2 to R3 A
        self.lines[(("east", 1, "A2"), ("east", 2, "A"))] = self.canvas.create_line(
            self.x_ps_e_r2,
            self.y_ps_e_r2_a2 + (self.h_ps / 2),
            self.x_ps_e_r3 + self.w_ps,
            self.y_ps_e_r3_a + (self.h_ps / 2)
        )

        # east R2 M2 to R3 M
        self.lines[(("east", 1, "M2"), ("east", 2, "M"))] = self.canvas.create_line(
            self.x_ps_e_r2,
            self.y_ps_e_r2_m2 + (self.h_ps / 2),
            self.x_ps_e_r3 + self.w_ps,
            self.y_ps_e_r3_m + (self.h_ps / 2)
        )

        # east R2 M1 to R3 M
        self.lines[(("east", 1, "M1"), ("east", 2, "M"))] = self.canvas.create_line(
            self.x_ps_e_r2,
            self.y_ps_e_r2_m1 + (self.h_ps / 2),
            self.x_ps_e_r3 + self.w_ps,
            self.y_ps_e_r3_m + (self.h_ps / 2)
        )

        # east R3 A to R4 E
        self.lines[(("east", 2, "A"), ("east", 3, "E"))] = self.canvas.create_line(
            self.x_ps_e_r3,
            self.y_ps_e_r3_a + (self.h_ps / 2),
            self.x_ps_e_r4 + self.w_ps,
            self.y_ps_e_r4_e + (self.h_ps / 2)
        )

        # east R3 M to R4 E
        self.lines[(("east", 2, "M"), ("east", 3, "E"))] = self.canvas.create_line(
            self.x_ps_e_r3,
            self.y_ps_e_r3_m + (self.h_ps / 2),
            self.x_ps_e_r4 + self.w_ps,
            self.y_ps_e_r4_e + (self.h_ps / 2)
        )

        # east R4 E to R5 SC
        self.lines[(("east", 3, "E"), ("west", 4, "SC"))] = self.canvas.create_line(
            self.x_ps_e_r4,
            self.y_ps_e_r4_e + (self.h_ps / 2),
            self.x_ps_sc + self.w_ps,
            self.y_ps_sc + (self.h_ps / 2)
        )

        ######################################################################################

        for k, line in self.lines.items():
            self.canvas.itemconfigure(
                line,
                fill=self.bg_line_west,
                width=self.w_line
            )
            self.canvas.tag_lower(line)

        # self.rect_ps_w_wc_b = self.canvas.create_rectangle(
        #     self.x_ps_w_r1,
        #     self.y_ps_w_wc_b_r1,
        #     self.x_ps_w_r1 + self.w_ps,
        #     self.y_ps_w_wc_b_r1 + self.h_ps,
        #     fill=self.bg_empty_west
        # )
        # self.text_ps_w_wc_b = self.canvas.create_text(
        #     self.x_ps_w_r1 + (self.w_ps / 2),
        #     self.y_ps_w_wc_b_r1 + (self.h_ps / 2),
        #     text="WC",
        #     fill=self.fg_empty_west,
        #     font=self.font_empty_west
        # )
        # self.img_ps_w_wc_b = self.canvas.create_image(
        #     self.x_ps_w_r1,
        #     self.y_ps_w_wc_b_r1,
        #     image=self.res_images[sample_west_teams[7]],
        #     anchor=tkinter.NW
        # )
        # self.west_images = [
        #     self.img_ps_w_wc_t,
        #     self.img_ps_w_p1,
        #     self.img_ps_w_p2,
        #     self.img_ps_w_p3,
        #     self.img_ps_w_c3,
        #     self.img_ps_w_c2,
        #     self.img_ps_w_c1,
        #     self.img_ps_w_wc_b
        # ]

        # # west wildcard top
        # self.rect_ps_w_wc_t = self.canvas.create_rectangle(
        #     self.x_ps_w_r1,
        #     self.y_ps_wc_t_r1,
        #     self.x_ps_w_r1 + self.w_ps,
        #     self.y_ps_wc_t_r1 + self.h_ps,
        #     fill=self.bg_empty_west
        # )
        # self.text_ps_w_wc_t = self.canvas.create_text(
        #     self.x_ps_w_r1 + (self.w_ps / 2),
        #     self.y_ps_wc_t_r1 + (self.h_ps / 2),
        #     text="WC",
        #     fill=self.fg_empty_west,
        #     font=self.font_empty_west
        # )
        # self.img_ps_w_wc_t = self.canvas.create_image(
        #     self.x_ps_w_r1,
        #     self.y_ps_wc_t_r1,
        #     image=self.res_images[sample_west_teams[0]],
        #     anchor=tkinter.NW
        # )
        #
        # # pacific 1
        # self.rect_ps_w_p1 = self.canvas.create_rectangle(
        #     self.x_ps_w_r1,
        #     self.y_ps_p1_r1,
        #     self.x_ps_w_r1 + self.w_ps,
        #     self.y_ps_p1_r1 + self.h_ps,
        #     fill=self.bg_empty_west
        # )
        # self.text_ps_w_p1 = self.canvas.create_text(
        #     self.x_ps_w_r1 + (self.w_ps / 2),
        #     self.y_ps_p1_r1 + (self.h_ps / 2),
        #     text="P1",
        #     fill=self.fg_empty_west,
        #     font=self.font_empty_west
        # )
        # self.img_ps_w_p1 = self.canvas.create_image(
        #     self.x_ps_w_r1,
        #     self.y_ps_p1_r1,
        #     image=self.res_images[sample_west_teams[1]],
        #     anchor=tkinter.NW
        # )
        #
        # # pacific 2
        # self.rect_ps_w_p2 = self.canvas.create_rectangle(
        #     self.x_ps_w_r1,
        #     self.y_ps_p2_r1,
        #     self.x_ps_w_r1 + self.w_ps,
        #     self.y_ps_p2_r1 + self.h_ps,
        #     fill=self.bg_empty_west
        # )
        # self.text_ps_w_p2 = self.canvas.create_text(
        #     self.x_ps_w_r1 + (self.w_ps / 2),
        #     self.y_ps_p2_r1 + (self.h_ps / 2),
        #     text="P2",
        #     fill=self.fg_empty_west,
        #     font=self.font_empty_west
        # )
        # self.img_ps_w_p2 = self.canvas.create_image(
        #     self.x_ps_w_r1,
        #     self.y_ps_p2_r1,
        #     image=self.res_images[sample_west_teams[2]],
        #     anchor=tkinter.NW
        # )
        #
        # # pacific 3
        # self.rect_ps_w_p3 = self.canvas.create_rectangle(
        #     self.x_ps_w_r1,
        #     self.y_ps_p3_r1,
        #     self.x_ps_w_r1 + self.w_ps,
        #     self.y_ps_p3_r1 + self.h_ps,
        #     fill=self.bg_empty_west
        # )
        # self.text_ps_w_p3 = self.canvas.create_text(
        #     self.x_ps_w_r1 + (self.w_ps / 2),
        #     self.y_ps_p3_r1 + (self.h_ps / 2),
        #     text="P3",
        #     fill=self.fg_empty_west,
        #     font=self.font_empty_west
        # )
        # self.img_ps_w_p3 = self.canvas.create_image(
        #     self.x_ps_w_r1,
        #     self.y_ps_p3_r1,
        #     image=self.res_images[sample_west_teams[3]],
        #     anchor=tkinter.NW
        # )
        #
        # # central 3
        # self.rect_ps_w_c3 = self.canvas.create_rectangle(
        #     self.x_ps_w_r1,
        #     self.y_ps_c3_r1,
        #     self.x_ps_w_r1 + self.w_ps,
        #     self.y_ps_c3_r1 + self.h_ps,
        #     fill=self.bg_empty_west
        # )
        # self.text_ps_w_c3 = self.canvas.create_text(
        #     self.x_ps_w_r1 + (self.w_ps / 2),
        #     self.y_ps_c3_r1 + (self.h_ps / 2),
        #     text="C3",
        #     fill=self.fg_empty_west,
        #     font=self.font_empty_west
        # )
        # self.img_ps_w_c3 = self.canvas.create_image(
        #     self.x_ps_w_r1,
        #     self.y_ps_c3_r1,
        #     image=self.res_images[sample_west_teams[4]],
        #     anchor=tkinter.NW
        # )
        #
        # # central 2
        # self.rect_ps_w_c2 = self.canvas.create_rectangle(
        #     self.x_ps_w_r1,
        #     self.y_ps_c2_r1,
        #     self.x_ps_w_r1 + self.w_ps,
        #     self.y_ps_c2_r1 + self.h_ps,
        #     fill=self.bg_empty_west
        # )
        # self.text_ps_w_c2 = self.canvas.create_text(
        #     self.x_ps_w_r1 + (self.w_ps / 2),
        #     self.y_ps_c2_r1 + (self.h_ps / 2),
        #     text="C2",
        #     fill=self.fg_empty_west,
        #     font=self.font_empty_west
        # )
        # self.img_ps_w_c2 = self.canvas.create_image(
        #     self.x_ps_w_r1,
        #     self.y_ps_c2_r1,
        #     image=self.res_images[sample_west_teams[5]],
        #     anchor=tkinter.NW
        # )
        #
        # # central 1
        # self.rect_ps_w_c1 = self.canvas.create_rectangle(
        #     self.x_ps_w_r1,
        #     self.y_ps_c1_r1,
        #     self.x_ps_w_r1 + self.w_ps,
        #     self.y_ps_c1_r1 + self.h_ps,
        #     fill=self.bg_empty_west
        # )
        # self.text_ps_w_c1 = self.canvas.create_text(
        #     self.x_ps_w_r1 + (self.w_ps / 2),
        #     self.y_ps_c1_r1 + (self.h_ps / 2),
        #     text="C1",
        #     fill=self.fg_empty_west,
        #     font=self.font_empty_west
        # )
        # self.img_ps_w_c1 = self.canvas.create_image(
        #     self.x_ps_w_r1,
        #     self.y_ps_c1_r1,
        #     image=self.res_images[sample_west_teams[6]],
        #     anchor=tkinter.NW
        # )
        #
        # # west wild card bottom
        # self.rect_ps_w_wc_b = self.canvas.create_rectangle(
        #     self.x_ps_w_r1,
        #     self.y_ps_w_wc_b_r1,
        #     self.x_ps_w_r1 + self.w_ps,
        #     self.y_ps_w_wc_b_r1 + self.h_ps,
        #     fill=self.bg_empty_west
        # )
        # self.text_ps_w_wc_b = self.canvas.create_text(
        #     self.x_ps_w_r1 + (self.w_ps / 2),
        #     self.y_ps_w_wc_b_r1 + (self.h_ps / 2),
        #     text="WC",
        #     fill=self.fg_empty_west,
        #     font=self.font_empty_west
        # )
        # self.img_ps_w_wc_b = self.canvas.create_image(
        #     self.x_ps_w_r1,
        #     self.y_ps_w_wc_b_r1,
        #     image=self.res_images[sample_west_teams[7]],
        #     anchor=tkinter.NW
        # )
        # self.west_images = [
        #     self.img_ps_w_wc_t,
        #     self.img_ps_w_p1,
        #     self.img_ps_w_p2,
        #     self.img_ps_w_p3,
        #     self.img_ps_w_c3,
        #     self.img_ps_w_c2,
        #     self.img_ps_w_c1,
        #     self.img_ps_w_wc_b
        # ]
        # self.east_images = [
        #     self.img_ps_e_wc_t,
        #     self.img_ps_e_a1,
        #     self.img_ps_e_a2,
        #     self.img_ps_e_a3,
        #     self.img_ps_e_m3,
        #     self.img_ps_e_m2,
        #     self.img_ps_e_m1,
        #     self.img_ps_e_wc_b
        # ]

        self.positions_ps_west = {
            rnd: {
                k: {
                    "rect": list(
                        map(lambda i_x: (i_x[1] + self.bw_ps_west) if (i_x[0] < 2) else (i_x[1] - self.bw_ps_west),
                            enumerate(self.canvas.bbox(dat["tag_rect"])))),
                    "text": self.canvas.bbox(dat["tag_text"])
                }
                for k, dat in rnd_dat.items()
            }
            for rnd, rnd_dat in self.ps_codes["west"].items()
        }
        self.positions_bank_west_teams = {}

        self.positions_ps_east = {
            rnd: {
                k: {
                    "rect": list(
                        map(lambda i_x: (i_x[1] + self.bw_ps_east) if (i_x[0] < 2) else (i_x[1] - self.bw_ps_east),
                            enumerate(self.canvas.bbox(dat["tag_rect"])))),
                    "text": self.canvas.bbox(dat["tag_text"])
                }
                for k, dat in rnd_dat.items()
            }
            for rnd, rnd_dat in self.ps_codes["east"].items()
        }
        self.ordered_positions = []
        for conf, conf_data in self.ps_codes.items():
            for rnd, rnd_data in conf_data.items():
                for pc, pc_data in rnd_data.items():
                    self.ordered_positions.append((conf, rnd, pc))
        self.ordered_positions.sort(key=lambda tup: (tup[1], tup[0]))
        print(f"{self.positions_ps_west[4]['SC']=}")
        self.positions_ps_east.update({4: {"SC": self.positions_ps_west[4]["SC"]}})

        self.positions_bank_east_teams = {}

        for i, t_pts in enumerate(self.sorted_west):
            t, pts = t_pts
            x = self.pos_bank_west[0] + 10 + (0 if (i % 2 == 0) else self.w_ps + 10)
            y = self.pos_bank_west[1] + ((i // 2) * (self.h_ps + 10)) + 5
            img = self.res_images[t]
            self.res_img_to_t[img] = t
            tag = self.canvas.create_image(
                x, y,
                image=img,
                anchor=tkinter.NW
            )
            self.res_pyimage_to_t[
                self.canvas.itemcget(
                    tag,
                    "image"
                )
            ] = t
            self.positions_bank_west_teams[t] = (x, y, img, tag)
            self.canvas.tag_bind(tag, "<Button-1>", lambda event, t_=t: self.click_bank_team(event, t_))

        for i, t_pts in enumerate(self.sorted_east):
            t, pts = t_pts
            x = self.pos_bank_east[0] + 10 + (0 if (i % 2 == 0) else self.w_ps + 10)
            y = self.pos_bank_east[1] + ((i // 2) * (self.h_ps + 10)) + 5
            img = self.res_images[t]
            self.res_img_to_t[img] = t
            tag = self.canvas.create_image(
                x, y,
                image=img,
                anchor=tkinter.NW
            )
            self.res_pyimage_to_t[
                self.canvas.itemcget(
                    tag,
                    "image"
                )
            ] = t
            self.positions_bank_east_teams[t] = (x, y, img, tag)
            self.canvas.tag_bind(tag, "<Button-1>", lambda event, t_=t: self.click_bank_team(event, t_))

        self.canvas.grid(row=0, column=0)
        # self.canvas.tag_bind(self.img_ps_w_wc_t, "<B1-Motion>", lambda event, rect=self.img_ps_w_wc_t: self.motion_rect(event, rect))
        # self.canvas.tag_bind(self.img_ps_w_p1, "<B1-Motion>", lambda event, rect=self.img_ps_w_p1: self.motion_rect(event, rect))
        # self.canvas.tag_bind(self.img_ps_w_p2, "<B1-Motion>", lambda event, rect=self.img_ps_w_p2: self.motion_rect(event, rect))
        # self.canvas.tag_bind(self.img_ps_w_p3, "<B1-Motion>", lambda event, rect=self.img_ps_w_p3: self.motion_rect(event, rect))
        # self.canvas.tag_bind(self.img_ps_w_c3, "<B1-Motion>", lambda event, rect=self.img_ps_w_c3: self.motion_rect(event, rect))
        # self.canvas.tag_bind(self.img_ps_w_c2, "<B1-Motion>", lambda event, rect=self.img_ps_w_c2: self.motion_rect(event, rect))
        # self.canvas.tag_bind(self.img_ps_w_c1, "<B1-Motion>", lambda event, rect=self.img_ps_w_c1: self.motion_rect(event, rect))
        # self.canvas.tag_bind(self.img_ps_w_wc_b, "<B1-Motion>", lambda event, rect=self.img_ps_w_wc_b: self.motion_rect(event, rect))
        #
        #
        # self.canvas.tag_bind(self.img_ps_w_wc_t, "<ButtonRelease-1>", lambda event, rect=self.img_ps_w_wc_t: self.release_rect(event, rect))

        # self.canvas.tag_bind(self.drag_rect, "<B1-Motion>", lambda event, rect=self.img_ps_w_wc_b: self.motion_rect(event, rect))

        self.valid_ps_codes_root_a = ["WC_t", "A1", "A2", "A3", "A"]
        self.valid_ps_codes_root_op_a = ["WC_b", "M1", "M"]
        self.valid_ps_codes_a = [*self.valid_ps_codes_root_a, *self.valid_ps_codes_root_op_a, "E", "SC"]

        self.valid_ps_codes_root_m = ["M3", "M2", "M1", "WC_b", "M"]
        self.valid_ps_codes_root_op_m = ["WC_t", "A1", "A"]
        self.valid_ps_codes_m = [*self.valid_ps_codes_root_m, *self.valid_ps_codes_root_op_m, "E", "SC"]

        self.valid_ps_codes_root_c = ["C3", "C2", "C1", "WC_b", "C"]
        self.valid_ps_codes_root_op_c = ["WC_t", "P1", "P"]
        self.valid_ps_codes_c = [*self.valid_ps_codes_root_c, *self.valid_ps_codes_root_op_c, "W", "SC"]

        self.valid_ps_codes_root_p = ["WC_t", "P1", "P2", "P3", "P"]
        self.valid_ps_codes_root_op_p = ["WC_b", "C1", "C"]
        self.valid_ps_codes_p = [*self.valid_ps_codes_root_p, *self.valid_ps_codes_root_op_p, "W", "SC"]

        self.valid_ps_codes_list_a = [self.valid_ps_codes_root_a, self.valid_ps_codes_root_op_a, self.valid_ps_codes_a]
        self.valid_ps_codes_list_m = [self.valid_ps_codes_root_m, self.valid_ps_codes_root_op_m, self.valid_ps_codes_m]
        self.valid_ps_codes_list_c = [self.valid_ps_codes_root_c, self.valid_ps_codes_root_op_c, self.valid_ps_codes_c]
        self.valid_ps_codes_list_p = [self.valid_ps_codes_root_p, self.valid_ps_codes_root_op_p, self.valid_ps_codes_p]

        self.frame_btn_bar = tkinter.Frame(self)
        self.frame_clear_options = tkinter.Frame(self.frame_btn_bar)
        self.tv_cb_clear, self.cb_clear = checkbox_factory(self.frame_clear_options, ["clear locks"])
        self.tv_btn_clear_ps, self.btn_clear_ps = button_factory(
            self.frame_clear_options,
            "clear",
            command=self.click_clear_ps
        )
        self.tv_btn_export_ps, self.btn_export_ps = button_factory(
            self.frame_btn_bar,
            "export",
            command=self.click_export_ps
        )
        self.tv_btn_sr1fs, self.btn_sr1fs = button_factory(
            self.frame_btn_bar,
            "set round 1 based on standings",
            command=self.click_sr1fs
        )
        self.tv_btn_random_complete, self.btn_random_complete = button_factory(
            self.frame_btn_bar,
            "complete bracket randomly",
            command=self.click_random_complete
        )
        self.tv_lbl_cb_history, self.lbl_cb_history, self.tv_cb_history, self.cb_history = combo_factory(
            self,
            "History",
            values=list(self.history.keys())
        )

        self.frame_btn_bar.grid()
        self.frame_clear_options.grid(row=0, column=0)
        self.cb_clear[0].grid(row=0, column=0)
        self.btn_clear_ps.grid(row=0, column=1)
        self.btn_export_ps.grid(row=0, column=1)
        self.btn_sr1fs.grid(row=0, column=2)
        self.btn_random_complete.grid(row=0, column=3)
        self.lbl_cb_history.grid()
        self.cb_history.grid()

        self.canvas.bind("<ButtonRelease-1>", self.release_click)
        self.canvas.bind("<ButtonRelease-3>", self.r_click_get_parents)
        self.canvas.bind("<B1-Motion>", self.motion)
        self.canvas.bind("<MouseWheel>", self.scroll)
        self.tv_cb_history.trace_variable("w", self.select_cb_history)

        # for img in self.west_images:
        #     self.canvas.itemconfigure(img, state="hidden")

        # self.lb = Lock(self.canvas, 750, 175)

    def select_cb_history(self, *args):
        h_key = self.tv_cb_history.get()
        print(f"select_cb_history {h_key=}")
        print(f"{self.history[h_key]=}")

        # TODO

    def get_children(self, conf_code, rnd_code, ps_code):
        if rnd_code <= 0:
            return []
        else:
            path = self.calc_path(conf_code, rnd_code, ps_code)
            s_path = [list(tup) for tup in (set([tuple(path_[-2]) for path_ in path]))]
            print(f"{s_path=}")
            return s_path

    def get_parents(self, conf_code, rnd_code, ps_code):

        if conf_code == "east":
            if ps_code in self.valid_ps_codes_root_c:
                drag_div = "C"
            else:
                drag_div = "P"
        else:
            if ps_code in self.valid_ps_codes_root_m:
                drag_div = "M"
            else:
                drag_div = "A"

        paths_ = self.calc_path(conf_code, rnd_code, ps_code)

        if rnd_code == 4:
            if drag_div == "P":
                paths_ = paths_[:5]
            elif drag_div == "C":
                paths_ = paths_[5:10]
            elif drag_div == "A":
                paths_ = paths_[10:15]
            else:
                paths_ = paths_[15:]

            # ensure that a west path to SC is considered
            paths_.insert(0, self.calc_path("west", 4, "SC")[0])
        else:
            if drag_div in ("P", "A"):
                paths_ = paths_[:5]
            # elif drag_div == "C":
            else:
                paths_ = paths_[5:10]

        # c_team = self.res_pyimage_to_t.get(
        #     self.canvas.itemcget(self.ps_codes[conf_code][rnd_code][ps_code]['tag_image'], 'image'), "no_child")
        # # print(f"{conf_code=}, {rnd_code=}, {ps_code=}, t='{c_team}'")
        # # print(f"B paths_=")
        # # for p in paths_:
        # #     print(f"{p}")
        if rnd_code == 0:
            return []
        else:
            return [list(tup) for tup in (set([tuple(path[-2]) for path in paths_]))]

    def r_click_get_parents(self, event):
        e_x, e_y = event.x, event.y
        all_positions = {"west": self.positions_ps_west}
        all_positions.update({"east": self.positions_ps_east})
        # drag_conf = "east" if drag_conf == "E" else "west"
        for conf, conf_data in all_positions.items():
            for rnd, rnd_data in conf_data.items():
                for pc, pc_data in rnd_data.items():
                    bbox = pc_data["rect"]
                    if self.collide_bbox_point(bbox, (e_x, e_y)):
                        if rnd == 4:
                            conf = "west"
                        print(f"{self.get_parents(conf, rnd, pc)=}")

    def get_teams_in_ps(self, conf_in=None, rnd_in=None, pc_in=None, assert_is_visible=True):

        inps = [conf_in, rnd_in, pc_in]
        if all(map(lambda v: v is not None, inps)):
            tag = self.ps_codes[conf_in][rnd_in][pc_in]["tag_image"]
            img = self.canvas.itemcget(tag, "image")
            t = self.res_pyimage_to_t.get(img, self.unk_team)
            v = self.canvas.itemcget(tag, "state") != "hidden"
            if assert_is_visible and not v:
                t = self.unk_team
            return {t: tuple(inps)} if (t != self.unk_team) else {}

        teams = {}
        for conf, rnd, pc in self.ordered_positions:
            tag = self.ps_codes[conf][rnd][pc]["tag_image"]
            img = self.canvas.itemcget(tag, "image")
            t = self.res_pyimage_to_t.get(img, self.unk_team)
            v = self.canvas.itemcget(tag, "state") != "hidden"
            if (t != self.unk_team) and ((v and assert_is_visible) or not assert_is_visible):
                teams[t] = (conf, rnd, pc)

        for i, v in enumerate(inps):
            if v is not None:
                teams = {t: crp for t, crp in teams.items() if crp[i] == v}

        return teams

    def click_random_complete(self):
        print(f"click_random_complete")

        self.click_clear_ps()

        east_in_ps = self.get_teams_in_ps(conf_in="east")
        west_in_ps = self.get_teams_in_ps(conf_in="west")
        rem_atl = []
        rem_met = []
        rem_cen = []
        rem_pac = []
        for t, div in full_team_to_div_name.items():
            match div:
                case "atlantic":
                    rem_atl.append(t)
                case "metropolitan":
                    rem_met.append(t)
                case "central":
                    rem_cen.append(t)
                case _:
                    rem_pac.append(t)
        for t, pc_data in east_in_ps.items():
            div = full_team_to_div_name[t]
            match div:
                case "atlantic":
                    rem_atl.remove(t)
                case _:
                    rem_met.remove(t)
        for t, pc_data in west_in_ps.items():
            div = full_team_to_div_name[t]
            match div:
                case "central":
                    rem_cen.remove(t)
                case _:
                    rem_pac.remove(t)

        # print(f"{rem_atl=}\n{rem_met=}\n{rem_cen=}\n{rem_pac=}")

        for conf, rnd, pc in self.ordered_positions:
            # print(f"{conf=}, {rnd=}, {pc=}, t=", end="")
            tag = self.ps_codes[conf][rnd][pc]["tag_image"]
            img = self.canvas.itemcget(tag, "image")
            t = self.res_pyimage_to_t.get(img, self.unk_team)
            v = self.canvas.itemcget(tag, "state") != "hidden"
            if not v:
                # not visible
                t = self.unk_team
            # print(f"{t=}", end="\n")

            if t == self.unk_team:
                if rnd == 0:
                    # select a team from the bank
                    if conf == "east":
                        if pc in self.valid_ps_codes_root_a:
                            rem_div = rem_atl
                        else:
                            rem_div = rem_met
                    else:
                        if pc in self.valid_ps_codes_root_c:
                            rem_div = rem_cen
                        else:
                            rem_div = rem_pac

                    rand_team = random.choice(rem_div)
                    rem_div.remove(rand_team)

                    # print(f"\t{rand_team=}, #{len(rem_div)}, {rem_div=}")
                else:
                    # select a team from parents
                    parents = self.get_parents(conf, rnd, pc)
                    rand_parent = random.choice(parents)
                    p_cc, p_rc, p_pc = rand_parent
                    tag = self.ps_codes[p_cc][p_rc][p_pc]["tag_image"]
                    img = self.canvas.itemcget(tag, "image")
                    # v = self.canvas.itemcget(tag, "state")
                    rand_team = self.res_pyimage_to_t[img]

                self.canvas.itemconfigure(
                    self.ps_codes[conf][rnd][pc]["tag_image"],
                    image=self.res_images[rand_team],
                    state="normal"
                )
                sb = self.ps_codes[conf][rnd][pc]["sb"]
                if sb is not None:
                    # rand_games = random.randrange(sb._min, sb._max)
                    rand_games = weighted_choice([(v_, v_) for v_ in range(sb._min, sb._max + 1)])
                    print(f"{rand_games=}")
                    sb.set(rand_games)
                    sb.show()

        #     if t == self.unk_team:
        #         # set a team here.
        #         if rnd > 2:
        #             # east / wset / SC
        #         else:
        #             if pc.upper().startswith("WC"):
        #                 # east / west
        #             else:
        #                 if pc in self.valid_ps_codes_root_a:
        #                     div = atlantic
        #                 elif pc in self.valid_ps_codes_root_m:
        #                     div = metropolitan
        #                 elif pc in self.valid_ps_codes_root_c:
        #                     div = central
        #                 else:
        #                     div = pacific
        #             teams_left = []
        # # self.ordered_positions
        # # positions = []
        # # for conf, conf_data in self.ps_codes.items():
        # #     for rnd, rnd_data in conf_data.items():
        # #         for pc, pc_data in rnd_data.items():
        # #             print(f"CRC {conf=}, {rnd=}, {pc=}")
        # #             # parents = self.get_parents()

    def click_sr1fs(self):
        self.click_clear_ps()
        top_p, top_c, top_a, top_m = [[] for _ in range(4)]
        for i, t_pts in enumerate(self.sorted_west):
            t, pts = t_pts
            d = full_team_to_div_name[t][0].upper()
            # print(f"{pts=}, {t=}, {d=}")
            if d == "P":
                top_p.append(t_pts)
            else:
                top_c.append(t_pts)
        top_p.sort(key=lambda tup: tup[1], reverse=True)
        top_c.sort(key=lambda tup: tup[1], reverse=True)
        wc_w = top_p[3:] + top_c[3:]
        wc_w.sort(key=lambda tup: tup[1], reverse=True)
        # print(f"{top_p=}, {top_c=}, {wc_w=}")
        t_p, t_c = top_p[0], top_c[0]
        if t_p[0] <= t_c[0]:
            w_ps_ordered = wc_w[1:2] + top_p[:3] + top_c[:3][::-1] + wc_w[:1]
        else:
            w_ps_ordered = wc_w[:1] + top_p[:3] + top_c[:3][::-1] + wc_w[1:2]

        for i, t_pts in enumerate(self.sorted_east):
            t, pts = t_pts
            d = full_team_to_div_name[t][0].upper()
            # print(f"{pts=}, {t=}, {d=}")
            if d == "A":
                top_a.append(t_pts)
            else:
                top_m.append(t_pts)
        top_a.sort(key=lambda tup: tup[1], reverse=True)
        top_m.sort(key=lambda tup: tup[1], reverse=True)
        wc_e = top_a[3:] + top_m[3:]
        wc_e.sort(key=lambda tup: tup[1], reverse=True)
        # print(f"{top_a=}, {top_m=}, {wc_e=}")
        t_a, t_m = top_a[0], top_m[0]
        if t_a[0] <= t_m[0]:
            e_ps_ordered = wc_e[1:2] + top_a[:3] + top_m[:3][::-1] + wc_e[:1]
        else:
            e_ps_ordered = wc_e[:1] + top_a[:3] + top_m[:3][::-1] + wc_e[1:2]

        w_ps_keys = self.valid_ps_codes_root_p[:4] + self.valid_ps_codes_root_c[:4]
        e_ps_keys = self.valid_ps_codes_root_a[:4] + self.valid_ps_codes_root_m[:4]

        for conf, zips in {
            "west": zip(w_ps_keys, w_ps_ordered),
            "east": zip(e_ps_keys, e_ps_ordered)
        }.items():
            for ps_c, t_pts in zips:
                self.canvas.itemconfigure(
                    self.ps_codes[conf][0][ps_c]["tag_image"],
                    state="normal",
                    image=self.res_images[t_pts[0]]
                )

        # print(f"{w_ps_ordered=}")
        # print(f"{e_ps_ordered=}")

    def click_export_ps(self):
        missing = {}
        for conf, conf_data in self.ps_codes.items():
            for rnd, rnd_data in conf_data.items():
                for pc, pc_data in rnd_data.items():
                    tag = self.ps_codes[conf][rnd][pc]["tag_image"]
                    img = self.canvas.itemcget(tag, "image")
                    v = self.canvas.itemcget(tag, "state")
                    t = self.res_pyimage_to_t.get(img, self.unk_team)
                    sb_text = ""
                    if v == "hidden":
                        t = self.unk_team
                    if rnd > 0:
                        sb = self.ps_codes[conf][rnd][pc]["sb"]
                        num = sb.num.get()
                        sb_text = f" #Games={num}"
                    print(f"C={conf[0].upper()}, R={rnd}, PC={pc.ljust(6)}, t={t}{sb_text}")
                    if t == self.unk_team:
                        missing.update({conf: {rnd: {pc: t}}})

        if missing:
            messagebox.showinfo(
                title=self.title_app,
                message=f"Please finish making selections."
            )

            for cc, c_data in missing.items():
                for rc, r_data in c_data.items():
                    for pc, p_data in r_data.items():
                        self.flash_ps(cc, rc, pc)
        else:
            # name and save
            self.tl_window = tkinter.Toplevel(self)
            self.tl_geometry = calc_geometry_tl(0.25, 0.1, parent=self, rtype=dict)
            self.tl_window.geometry(self.tl_geometry["geometry"])
            self.tl_tv_lbl_name_entry, \
                self.tl_lbl_name_entry, \
                self.tl_tv_name_entry, \
                self.tl_name_entry = entry_factory(
                self.tl_window,
                tv_label="Name this bracket:"
            )
            self.tl_name_entry.bind("<Return>", self.tl_name_entry_return)
            self.tl_lbl_name_entry.grid()
            self.tl_name_entry.grid()
            self.tl_window.grab_set()
            self.tl_name_entry.focus()
            self.wait_window(self.tl_window)

    def tl_name_entry_return(self, event):
        print(f"tl_name_entry_return")
        name = self.tl_tv_name_entry.get()
        if name:
            if name not in self.history:
                self.history.update({
                    name: {conf: {rnd: {ps: {k: v for k, v in ps_data.items()} for ps, ps_data in rnd_data.items()} for
                                  rnd, rnd_data in conf_data.items()} for conf, conf_data in self.ps_codes.items()}
                })

                with open(self.history_file, "w") as f:
                    # json.dump(jsonify(self.history), f)
                    f.write(jsonify(self.history, in_line=False))

                self.tl_window.destroy()

    def click_clear_ps(self):
        do_locks = self.tv_cb_clear[0].get()
        print(f"{do_locks=}")
        for conf, conf_data in self.ps_codes.items():
            for rnd, rnd_data in conf_data.items():
                for pc, pc_data in rnd_data.items():
                    tag = pc_data["tag_image"]
                    lock = pc_data["lock"]
                    if tag:
                        print(f"{conf=}, {rnd=}, {pc=}, {lock=}")
                        skip = False
                        # if rnd > 0:
                        if lock.state.get() and not do_locks:
                            continue
                        # else:
                        # before clearing, check that parent is not locked
                        # for p_cc, p_rc, p_pc in self.get_parents(conf, rnd, pc):
                        #     if self.ps_codes[p_cc][p_rc][p_pc]["lock"].state.get():
                        # locked
                        # skip = True
                        # if not skip:
                        self.canvas.itemconfigure(
                            tag,
                            state="hidden"
                        )
                    if do_locks:
                        lock.set_mode(False)
        if do_locks:
            self.tv_cb_clear[0].set(False)

    def collide_bbox_point(self, bbox_a, point):
        x0_a, y0_a, x1_a, y1_a = bbox_a
        x_p, y_p = point
        return all([
            x0_a <= x_p <= x1_a,
            y0_a <= y_p <= y1_a
        ])

    def scroll(self, event):
        e_x, e_y = event.x, event.y
        delta = event.delta
        point = e_x, e_y
        for conf, conf_data in self.ps_codes.items():
            for rnd_code, rnd_data in conf_data.items():
                for ps_code, dat in rnd_data.items():
                    sb = dat["sb"]
                    if sb is not None:
                        if self.collide_bbox_point(sb.bbox, point):
                            sb.scroll(event)

    def motion(self, event):
        self.canvas.tag_raise(self.drag_rect)
        if self.dragging.get():
            e_x, e_y = event.x, event.y
            # print(f"00 {e_x=}, {e_y=}")
            e_x = self.canvas.canvasx(e_x)
            e_y = self.canvas.canvasy(e_y)
            # print(f"11 {e_x=}, {e_y=}")
            point = (e_x, e_y)
            self.canvas.coords(self.drag_rect, e_x, e_y)
            self.revert_lines()
            # drag_team = self.res_img_to_t[self.canvas.itemcget(self.drag_rect, "image")]
            drag_team = self.drag_team.get()
            drag_div = full_team_to_div_name[drag_team].upper()[0]
            drag_conf = full_team_to_conf[drag_team].upper()[0]
            print(f"{drag_team=}, {drag_div=}, {drag_conf=}")
            positions = self.positions_ps_east if drag_conf == "E" else self.positions_ps_west
            drag_conf = "east" if drag_conf == "E" else "west"

            tol = 1e-10
            for rnd_code, rnd_dat in positions.items():
                for ps_code, dat in rnd_dat.items():
                    # for k, bbox in dat.items():
                    # k = "rect"
                    bbox = dat["rect"]
                    paths = []
                    p_y = ((e_y - bbox[1]) / self.h_ps)
                    if self.collide_bbox_point(bbox, point):
                        paths = self.calc_path(drag_conf, rnd_code, ps_code)
                        if rnd_code == 4:
                            # stanley cup finalist
                            p_y = int(p_y * (5 - tol))
                            if drag_div == "P":
                                paths = paths[:5]
                            elif drag_div == "C":
                                paths = paths[5:10]
                            elif drag_div == "A":
                                paths = paths[10:15]
                            else:
                                paths = paths[15:]
                        elif rnd_code == 3:
                            # conf finalist
                            p_y = int(p_y * (5 - tol))
                            if drag_div in ("P", "A"):
                                paths = paths[:5]
                            else:
                                paths = paths[5:]
                        elif rnd_code == 2:
                            # div finalist
                            p_y = int(p_y * (4 - tol))
                            # if ps_code not in self.valid_ps_codes_a

                            if drag_div == "C":
                                if ps_code in self.valid_ps_codes_root_op_c:
                                    paths = paths[:1]
                                    p_y = 0
                            else:
                                if ps_code in self.valid_ps_codes_root_op_p:
                                    paths = paths[-1:]
                                    p_y = 0
                        elif rnd_code == 1:
                            # quarter finalist
                            p_y = int(p_y * (2 - tol))
                            if drag_div == "C":
                                if ps_code in self.valid_ps_codes_root_op_c:
                                    paths = paths[:1]
                                    p_y = 0
                            else:
                                if ps_code in self.valid_ps_codes_root_op_p:
                                    paths = paths[-1:]
                                    p_y = 0
                        else:
                            # round 1
                            p_y = 0
                        print(f"{p_y=}, {rnd_code=}, {ps_code=}, {len(paths)=}, {paths=}")
                        # print(f"{point=}\n{self.h_ps=}\n{bbox=}\n{e_y-bbox[1]=}\n{(e_y-bbox[1])/self.h_ps=}\n{((e_y-bbox[1])/self.h_ps)*2=}")
                    if paths:
                        path = paths[p_y]
                        if path:
                            pth_0 = path.pop(0)
                        while path:
                            pth_1 = path.pop(0)
                            # cc_0, rc_0, pc_0 = pth_0
                            # cc_1, rc_1, pc_1 = pth_1
                            # if cc_0 == "west" and
                            match drag_div:
                                case "A":
                                    do_highlight = ps_code in self.valid_ps_codes_a
                                case "M":
                                    do_highlight = ps_code in self.valid_ps_codes_m
                                case "C":
                                    do_highlight = ps_code in self.valid_ps_codes_c
                                case _:
                                    do_highlight = ps_code in self.valid_ps_codes_p

                            if do_highlight:
                                print(f"\t{pth_0=}, {pth_1=}")
                                self.canvas.itemconfigure(
                                    self.lines[(tuple(pth_0), tuple(pth_1))],
                                    fill=self.bg_opt_ps_west
                                )
                            pth_0 = pth_1

    def revert_lines(self):
        for k, line in self.lines.items():
            conf = k[0][0]
            self.canvas.itemconfigure(
                line,
                fill=self.bg_line_east if conf == "east" else self.bg_line_west
            )

    def flash_ps(self, conf_code, rnd_code, ps_code):
        sc = "#FFFFFF"
        ec = "#000000"
        if conf_code == "east":
            cc = self.bg_empty_east
            bd = self.bd_empty_east
        else:
            cc = self.bg_empty_west
            bd = self.bd_empty_west
        grad_c = [gradient(i + 1, 10, sc, ec, rgb=False) for i in range(10)]
        grad_f = [gradient(i + 1, 10, sc, ec, rgb=False) for i in range(10)]
        for i, c_f in enumerate(zip(grad_c, grad_f)):
            c, f = c_f
            self.after(
                i * 100,
                lambda: self.canvas.itemconfigure(
                    self.ps_codes[conf_code][rnd_code][ps_code]["tag_rect"],
                    outline=c
                )
            )
            self.after(
                i * 100,
                lambda: self.canvas.itemconfigure(
                    self.ps_codes[conf_code][rnd_code][ps_code]["tag_text"],
                    fill=f
                )
            )

    def release_click(self, event):
        print(f"RELEASE ", end="")
        e_x, e_y = event.x, event.y
        point = (e_x, e_y)
        is_dragging = self.dragging.get()
        do_ps_check = True
        for conf, conf_data in self.ps_codes.items():
            for rnd_code, rnd_data in conf_data.items():
                for ps_code, dat in rnd_data.items():
                    sb = dat["sb"]
                    lock = dat["lock"]
                    if sb is not None:
                        if self.collide_bbox_point(sb.bbox, point):
                            # released on a game spinbox
                            do_ps_check = False

                    if lock is not None:
                        if self.collide_bbox_point(lock.bbox, point):
                            do_ps_check = False
                            locked = lock.state.get() == True
                            c_team = self.res_pyimage_to_t.get(self.canvas.itemcget(dat["tag_image"], "image"),
                                                               self.unk_team)
                            visible = self.canvas.itemcget(dat["tag_image"], "state") == "normal"
                            if not locked:
                                if visible:
                                    lock.set_mode(True)
                                    check_back = rnd_code > 0
                                    c_conf, c_rnd_code, c_ps_code = conf, rnd_code, ps_code
                                    while check_back:
                                        print(f"{check_back=}, {c_conf=}, {c_rnd_code=}, {c_ps_code=}")
                                        check_back = False
                                        for p_cc, p_rc, p_pc in self.get_children(c_conf, c_rnd_code, c_ps_code):
                                            p_tag = self.ps_codes[p_cc][p_rc][p_pc]["tag_image"]
                                            p_team = self.res_pyimage_to_t.get(
                                                self.canvas.itemcget(p_tag, "image"), self.unk_team)
                                            print(f"\t{p_cc=}, {p_rc=}, {p_pc=}, {p_team=}")
                                            if (p_team != self.unk_team) and (c_team == p_team):
                                                # lock parent too
                                                p_lock = self.ps_codes[p_cc][p_rc][p_pc]["lock"]
                                                p_lock.set_mode(True)
                                                c_conf, c_rnd_code, c_ps_code = p_cc, p_rc, p_pc
                                            check_back = p_rc > 0
                                        # check_back = check_back or bool(parents)

        if do_ps_check:
            tol = 1e-10
            drag_team = self.drag_team.get()
            drag_is_visible = self.canvas.itemcget(self.drag_rect, "state") == "normal"
            if drag_is_visible:
                drag_div = full_team_to_div_name[drag_team].upper()[0]
                drag_conf = full_team_to_conf[drag_team].upper()[0]
                positions = self.positions_ps_east if drag_conf == "E" else self.positions_ps_west
                drag_conf = "east" if drag_conf == "E" else "west"
                print(f"{drag_team=}, {drag_div=}, {drag_conf=}")
                # bbox_drag = self.canvas.bbox(self.drag_rect)
                if is_dragging:
                    print(f"DRAG ", end="")
                    for rnd_code, rnd_dat in positions.items():
                        for ps_code, dat in rnd_dat.items():
                            # for k, bbox in dat.items():
                            bbox = dat["rect"]
                            if self.collide_bbox_point(bbox, point):
                                print(f"COLLIDE cc='{drag_conf}', rc={rnd_code}, pc={ps_code} ", end="")
                                p_y = ((e_y - bbox[1]) / self.h_ps)
                                # # release in a ps spot
                                # print(f"Release {rnd_code=} {ps_code=}, {k=}")
                                # # check that previous spots not empty
                                # do_change = False

                                paths = self.calc_path(drag_conf, rnd_code, ps_code)
                                if rnd_code == 4:
                                    # stanley cup finalist
                                    p_y = int(p_y * (5 - tol))
                                    if drag_div == "P":
                                        paths = paths[:5]
                                    elif drag_div == "C":
                                        paths = paths[5:10]
                                    elif drag_div == "A":
                                        paths = paths[10:15]
                                    else:
                                        paths = paths[15:]
                                elif rnd_code == 3:
                                    # conf finalist
                                    p_y = int(p_y * (5 - tol))
                                    if drag_div in ("P", "A"):
                                        paths = paths[:5]
                                    else:
                                        paths = paths[5:]
                                elif rnd_code == 2:
                                    # div finalist
                                    p_y = int(p_y * (4 - tol))
                                    if drag_div == "C":
                                        if ps_code in self.valid_ps_codes_root_op_c:
                                            paths = paths[:1]
                                            p_y = 0
                                    else:
                                        if ps_code in self.valid_ps_codes_root_op_p:
                                            paths = paths[-1:]
                                            p_y = 0
                                elif rnd_code == 1:
                                    # quarter finalist
                                    p_y = int(p_y * (2 - tol))
                                    if drag_div == "C":
                                        if ps_code in self.valid_ps_codes_root_op_c:
                                            paths = paths[:1]
                                            p_y = 0
                                    else:
                                        if ps_code in self.valid_ps_codes_root_op_p:
                                            paths = paths[-1:]
                                            p_y = 0

                                else:
                                    # round 1
                                    p_y = 0

                                match drag_div:
                                    case "A":
                                        do_change = ps_code in self.valid_ps_codes_a
                                        if rnd_code == 0:
                                            do_change = ps_code in (
                                                        self.valid_ps_codes_root_a[:4] + self.valid_ps_codes_root_op_a[
                                                                                         :1])
                                    case "M":
                                        do_change = ps_code in self.valid_ps_codes_m
                                        if rnd_code == 0:
                                            do_change = ps_code in (
                                                        self.valid_ps_codes_root_m[:4] + self.valid_ps_codes_root_op_m[
                                                                                         :1])
                                    case "C":
                                        do_change = ps_code in self.valid_ps_codes_c
                                        if rnd_code == 0:
                                            do_change = ps_code in (
                                                        self.valid_ps_codes_root_c[:4] + self.valid_ps_codes_root_op_c[
                                                                                         :1])
                                    case _:
                                        do_change = ps_code in self.valid_ps_codes_p
                                        if rnd_code == 0:
                                            do_change = ps_code in (
                                                        self.valid_ps_codes_root_p[:4] + self.valid_ps_codes_root_op_p[
                                                                                         :1])

                                drag_img = self.canvas.itemcget(self.drag_rect, "image")

                                # check only one placement in conf bracket
                                if do_change:
                                    path = paths[p_y]
                                    # path = paths[p_y]
                                    # p_cc, p_rc, p_pc = path
                                    c = 0
                                    print(f"\nA DO CHANGE {paths=}")
                                    # for i, path_ in enumerate(paths):
                                    #     cc, rc, pc = path_[0]
                                    #     print(f"O1D: {cc=}, {rc=}, {pc=}, {path[0]=}")
                                    #     if ((cc != path[0][0]) or (rc != path[0][1]) or (pc != path[0][2])) \
                                    #             and self.canvas.itemcget(
                                    #         self.ps_codes[cc][rc][pc]["tag_image"],
                                    #         "image"
                                    #     ) == drag_img:
                                    #         # this team already has a round 1 placement
                                    #         print(f"Path already made")
                                    #         c += 1
                                    #         if c == 1:
                                    #             # do_change = False
                                    #             p_y = i
                                    #             break

                                    clear_path = []
                                    for pc in self.ps_codes[drag_conf][0]:
                                        cc = drag_conf
                                        rc = 0
                                        if ((cc != path[0][0]) or (rc != path[0][1]) or (pc != path[0][2])) \
                                                and (self.canvas.itemcget(
                                            self.ps_codes[cc][rc][pc]["tag_image"],
                                            "image"
                                        ) == drag_img) and (self.canvas.itemcget(self.ps_codes[cc][rc][pc]["tag_image"],
                                                                                 "state") == "normal"):
                                            # path already exists
                                            print(f"path already exists")
                                            clear_path = self.calc_path_2_sc(cc, rc, pc)
                                            break
                                            # do_change = False

                                    print(f"PAE {cc=}, {rc=}, {pc=} {clear_path=}")
                                    if clear_path:
                                        for cc, rc, pc in clear_path[0]:
                                            print(f"PAE {cc=}, {rc=}, {pc=}")
                                            # if rc <= rnd_code:
                                            #     print(f"BLANK")
                                            if self.canvas.itemcget(
                                                    self.ps_codes[cc][rc][pc]["tag_image"],
                                                    "image"
                                            ) == drag_img:
                                                self.canvas.itemconfigure(
                                                    self.ps_codes[cc][rc][pc]["tag_image"],
                                                    state="hidden"
                                                )
                                            # else:
                                            #     print(f"SKIP")

                                if do_change:
                                    # for ps in paths:
                                    print(f"DO CHANGE {p_y=}\n{path=}")
                                    cc, rc, pc = None, None, None
                                    for cc, rc, pc in path:
                                        self.canvas.itemconfigure(
                                            self.ps_codes[cc][rc][pc]["tag_image"],
                                            image=drag_img,
                                            state="normal"
                                        )
                                        sb = self.ps_codes[cc][rc][pc]["sb"]
                                        if sb is not None:
                                            sb.show()
                                        self.flash_ps(cc, rc, pc)

                                    # use the last path key to check the logic
                                    path_sc = self.calc_path_2_sc(cc, rc, pc)
                                    print(f"{path_sc[0]=}")
                                    for cc, rc, pc in path_sc[0]:
                                        if (cc == drag_conf) and (rc == rnd_code) and (pc == ps_code):
                                            break
                                        if self.canvas.itemcget(
                                                self.ps_codes[cc][rc][pc]["tag_image"],
                                                "image"
                                        ) != drag_img:
                                            print(f"\tA BLANK {cc=}, {rc=}, {pc=}\n")
                                            self.canvas.itemconfigure(
                                                self.ps_codes[cc][rc][pc]["tag_image"],
                                                state="hidden"
                                            )

                                    if 0 < rnd_code < 4:
                                        print(f"Start check path SC")
                                        for child in path_sc[0][1:]:
                                            c_cc, c_rc, c_pc = child
                                            parents = self.get_parents(c_cc, c_rc, c_pc)
                                            # paths_ = self.calc_path(c_cc, c_rc, c_pc)
                                            # print(f"A paths_=")
                                            # for p in paths_:
                                            #     print(f"{p}")
                                            #
                                            # # if 3 <= c_rc <= 4:
                                            # if c_rc == 4:
                                            #     if drag_div == "P":
                                            #         paths_ = paths_[:5]
                                            #     elif drag_div == "C":
                                            #         paths_ = paths_[5:10]
                                            #     elif drag_div == "A":
                                            #         paths_ = paths_[10:15]
                                            #     else:
                                            #         paths_ = paths_[15:]
                                            #
                                            #     # ensure that a west path to SC is considered
                                            #     paths_.insert(0, self.calc_path("west", 4, "SC")[0])
                                            # else:
                                            #     if drag_div in ("P", "A"):
                                            #         paths_ = paths_[:5]
                                            #     # elif drag_div == "C":
                                            #     else:
                                            #         paths_ = paths_[5:10]
                                            # # elif drag_div == "A":
                                            # #     paths_ = paths_[10:15]
                                            # # else:
                                            # #     paths_ = paths_[15:]
                                            #
                                            c_team = self.res_pyimage_to_t.get(
                                                self.canvas.itemcget(self.ps_codes[c_cc][c_rc][c_pc]['tag_image'],
                                                                     'image'), "no_child")
                                            # print(f"{c_cc=}, {c_rc=}, {c_pc=}, t='{c_team}'")
                                            # print(f"B paths_=")
                                            # for p in paths_:
                                            #     print(f"{p}")
                                            # # paths_ = [p[::-1] for p in paths_]
                                            # # paths_.reverse()
                                            # # print(f"B paths_=")
                                            # # for p in paths_:
                                            # #     print(f"{p}")
                                            # parents = [list(tup) for tup in (set([tuple(path[-2]) for path in paths_]))]
                                            print(f"{parents=}")
                                            # parents.remove(())
                                            if parents:
                                                # print(f"ME={self.res_pyimage_to_t[self.canvas.itemcget(self.ps_codes[c_cc][c_rc][c_pc]['tag_image'], 'image')]}")
                                                # print(f"ME={c_team}")
                                                # p_cc, p_rc, p_pc = parents[0]

                                                img_child = self.canvas.itemcget(
                                                    self.ps_codes[c_cc][c_rc][c_pc],
                                                    "image"
                                                )
                                                lp = len(parents)
                                                i = 0
                                                found_parent = False
                                                for p_cc, p_rc, p_pc in parents:
                                                    p_team = self.res_pyimage_to_t.get(self.canvas.itemcget(
                                                        self.ps_codes[p_cc][p_rc][p_pc]['tag_image'], 'image'),
                                                                                       'no_parent')
                                                    print(f"{p_cc=}, {p_rc=}, {p_pc=}, t='{p_team}', {i=}, {lp=}")
                                                    if (p_cc != path[-2][0]) or (p_rc != path[-2][1]) or (
                                                            p_pc != path[-2][2]):
                                                        par_vis = self.canvas.itemcget(
                                                            self.ps_codes[p_cc][p_rc][p_pc]["tag_image"],
                                                            "state"
                                                        )
                                                        # print(f"{par_vis=}")
                                                        # ((rnd_code + 1) < rc) and (
                                                        # if img_parents == img_child:
                                                        if (par_vis == "normal") and (p_team == c_team):
                                                            # print(f"\tB BLANK")
                                                            # self.canvas.itemconfigure(
                                                            #     self.ps_codes[c_cc][c_rc][c_pc]["tag_image"],
                                                            #     state="hidden"
                                                            # )
                                                            found_parent = True
                                                        else:
                                                            print(f"-B")

                                                    else:
                                                        print(f"-A")
                                                    i += 1
                                                print(f"{found_parent=}")
                                                if not found_parent:
                                                    self.canvas.itemconfigure(
                                                        self.ps_codes[c_cc][c_rc][c_pc]["tag_image"],
                                                        state="hidden"
                                                    )

                                    # if 0 < rnd_code < 4:
                                    #     print(f"Start check path SC")
                                    #     parents = [list(tup) for tup in (set([tuple(path[-2]) for path in paths]))]
                                    #     parents.remove(path[-2])
                                    #     if parents:
                                    #         p_cc, p_rc, p_pc = parents[0]
                                    #         img_parents = self.canvas.itemcget(
                                    #             self.ps_codes[p_cc][p_rc][p_pc],
                                    #             "image"
                                    #         )
                                    #         print(f"{p_cc=}, {p_rc=}, {p_pc=}")
                                    #         for child in path_sc[0][1:]:
                                    #             c_cc, c_rc, c_pc = child
                                    #             print(f"{c_cc=}, {c_rc=}, {c_pc=}", end="")
                                    #             img_child = self.canvas.itemcget(
                                    #                 self.ps_codes[c_cc][c_rc][c_pc],
                                    #                 "image"
                                    #             )
                                    #             # ((rnd_code + 1) < rc) and (
                                    #             if img_parents == img_child:
                                    #                 print(f"\tB BLANK", end="")
                                    #                 self.canvas.itemconfigure(
                                    #                     self.ps_codes[c_cc][c_rc][c_pc]["tag_image"],
                                    #                     state="hidden"
                                    #                 )
                                    #             print(f"")
                                    #
                                    # # self.canvas.itemconfigure(
                                    # #     self.ps_codes["west"][rnd_code][ps_code]["tag_image"],
                                    # #     image=self.canvas.itemcget(
                                    # #         self.drag_rect,
                                    # #         "image"
                                    # #     ),
                                    # #     state="normal"
                                    # # )
                                    # # self.flash_ps("west", rnd_code, ps_code)

        self.dragging.set(False)
        self.revert_lines()
        self.canvas.itemconfigure(self.drag_rect, state="hidden")

    def get_ps_parents(self, conf_code, rnd_code, ps_code):
        paths = self.calc_path(conf_code, rnd_code, ps_code)
        return [list(tup) for tup in (set([tuple(path[-2]) for path in paths]))]

    def calc_path_2_sc(self, conf_code, rnd_code, ps_code):
        inp = [conf_code, rnd_code, ps_code]
        sc = ["west", 4, "SC"]
        if rnd_code == 4:
            return [[inp]]
        elif rnd_code == 3:
            return [
                [inp, sc]
            ]
        elif rnd_code == 2:
            if conf_code == "east":
                return [
                    [inp, ["east", 3, "E"], sc]
                ]
            else:
                return [
                    [inp, ["west", 3, "W"], sc]
                ]
        elif rnd_code == 1:
            if conf_code == "east":
                if ps_code in self.valid_ps_codes_root_a:
                    return [
                        [inp, ["east", 2, "A"], ["east", 3, "E"], sc]
                    ]
                else:
                    return [
                        [inp, ["east", 2, "M"], ["east", 3, "E"], sc]
                    ]
            else:
                if ps_code in self.valid_ps_codes_root_p:
                    return [
                        [inp, ["west", 2, "P"], ["west", 3, "W"], sc]
                    ]
                else:
                    return [
                        [inp, ["west", 2, "C"], ["west", 3, "W"], sc]
                    ]
        else:
            if conf_code == "east":
                if ps_code in self.valid_ps_codes_root_a[:2]:
                    return [
                        [inp, ["east", 1, "A1"], ["east", 2, "A"], ["east", 3, "E"], sc]
                    ]
                elif ps_code in self.valid_ps_codes_root_a[2:4]:
                    return [
                        [inp, ["east", 1, "A2"], ["east", 2, "A"], ["east", 3, "E"], sc]
                    ]
                elif ps_code in self.valid_ps_codes_root_m[:2]:
                    return [
                        [inp, ["east", 1, "M2"], ["east", 2, "M"], ["east", 3, "E"], sc]
                    ]
                else:
                    return [
                        [inp, ["east", 1, "M1"], ["east", 2, "M"], ["east", 3, "E"], sc]
                    ]
            else:
                if ps_code in self.valid_ps_codes_root_p[:2]:
                    return [
                        [inp, ["west", 1, "P1"], ["west", 2, "P"], ["west", 3, "W"], sc]
                    ]
                elif ps_code in self.valid_ps_codes_root_p[2:4]:
                    return [
                        [inp, ["west", 1, "P2"], ["west", 2, "P"], ["west", 3, "W"], sc]
                    ]
                elif ps_code in self.valid_ps_codes_root_c[:2]:
                    return [
                        [inp, ["west", 1, "C2"], ["west", 2, "C"], ["west", 3, "W"], sc]
                    ]
                else:
                    return [
                        [inp, ["west", 1, "C1"], ["west", 2, "C"], ["west", 3, "W"], sc]
                    ]

    def calc_path(self, conf_code, rnd_code, ps_code):
        inp = [conf_code, rnd_code, ps_code]
        sc = ["west", 4, "SC"]
        if rnd_code == 4:
            # stanley cup finalist
            return [
                [["west", 0, "WC_t"], ["west", 1, "P1"], ["west", 2, "P"], ["west", 3, "W"], sc],
                [["west", 0, "P1"], ["west", 1, "P1"], ["west", 2, "P"], ["west", 3, "W"], sc],
                [["west", 0, "P2"], ["west", 1, "P2"], ["west", 2, "P"], ["west", 3, "W"], sc],
                [["west", 0, "P3"], ["west", 1, "P2"], ["west", 2, "P"], ["west", 3, "W"], sc],
                [["west", 0, "WC_b"], ["west", 1, "C1"], ["west", 2, "C"], ["west", 3, "W"], sc],

                [["west", 0, "WC_t"], ["west", 1, "P1"], ["west", 2, "P"], ["west", 3, "W"], sc],
                [["west", 0, "C3"], ["west", 1, "C2"], ["west", 2, "C"], ["west", 3, "W"], sc],
                [["west", 0, "C2"], ["west", 1, "C2"], ["west", 2, "C"], ["west", 3, "W"], sc],
                [["west", 0, "C1"], ["west", 1, "C1"], ["west", 2, "C"], ["west", 3, "W"], sc],
                [["west", 0, "WC_b"], ["west", 1, "C1"], ["west", 2, "C"], ["west", 3, "W"], sc],

                [["east", 0, "WC_t"], ["east", 1, "A1"], ["east", 2, "A"], ["east", 3, "E"], sc],
                [["east", 0, "A1"], ["east", 1, "A1"], ["east", 2, "A"], ["east", 3, "E"], sc],
                [["east", 0, "A2"], ["east", 1, "A2"], ["east", 2, "A"], ["east", 3, "E"], sc],
                [["east", 0, "A3"], ["east", 1, "A2"], ["east", 2, "A"], ["east", 3, "E"], sc],
                [["east", 0, "WC_b"], ["east", 1, "M1"], ["east", 2, "M"], ["east", 3, "E"], sc],

                [["east", 0, "WC_t"], ["east", 1, "A1"], ["east", 2, "A"], ["east", 3, "E"], sc],
                [["east", 0, "M3"], ["east", 1, "M2"], ["east", 2, "M"], ["east", 3, "E"], sc],
                [["east", 0, "M2"], ["east", 1, "M2"], ["east", 2, "M"], ["east", 3, "E"], sc],
                [["east", 0, "M1"], ["east", 1, "M1"], ["east", 2, "M"], ["east", 3, "E"], sc],
                [["east", 0, "WC_b"], ["east", 1, "M1"], ["east", 2, "M"], ["east", 3, "E"], sc]
            ]
        elif rnd_code == 3:
            # conf finalist
            match ps_code:
                case "W":
                    return [
                        [["west", 0, "WC_t"], ["west", 1, "P1"], ["west", 2, "P"], inp],
                        [["west", 0, "P1"], ["west", 1, "P1"], ["west", 2, "P"], inp],
                        [["west", 0, "P2"], ["west", 1, "P2"], ["west", 2, "P"], inp],
                        [["west", 0, "P3"], ["west", 1, "P2"], ["west", 2, "P"], inp],
                        [["west", 0, "WC_b"], ["west", 1, "C1"], ["west", 2, "C"], inp],

                        [["west", 0, "WC_t"], ["west", 1, "P1"], ["west", 2, "P"], inp],
                        [["west", 0, "C3"], ["west", 1, "C2"], ["west", 2, "C"], inp],
                        [["west", 0, "C2"], ["west", 1, "C2"], ["west", 2, "C"], inp],
                        [["west", 0, "C1"], ["west", 1, "C1"], ["west", 2, "C"], inp],
                        [["west", 0, "WC_b"], ["west", 1, "C1"], ["west", 2, "C"], inp]
                    ]
                case _:
                    return [
                        [["east", 0, "WC_t"], ["east", 1, "A1"], ["east", 2, "A"], inp],
                        [["east", 0, "A1"], ["east", 1, "A1"], ["east", 2, "A"], inp],
                        [["east", 0, "A2"], ["east", 1, "A2"], ["east", 2, "A"], inp],
                        [["east", 0, "A3"], ["east", 1, "A2"], ["east", 2, "A"], inp],
                        [["east", 0, "WC_b"], ["east", 1, "M1"], ["east", 2, "M"], inp],

                        [["east", 0, "WC_t"], ["east", 1, "A1"], ["east", 2, "A"], inp],
                        [["east", 0, "M3"], ["east", 1, "M2"], ["east", 2, "M"], inp],
                        [["east", 0, "M2"], ["east", 1, "M2"], ["east", 2, "M"], inp],
                        [["east", 0, "M1"], ["east", 1, "M1"], ["east", 2, "M"], inp],
                        [["east", 0, "WC_b"], ["east", 1, "M1"], ["east", 2, "M"], inp]
                    ]
        elif rnd_code == 2:
            # div finalist
            if conf_code == "west":
                match ps_code:
                    case "P":
                        return [
                            [["west", 0, "WC_t"], ["west", 1, "P1"], inp],
                            [["west", 0, "P1"], ["west", 1, "P1"], inp],
                            [["west", 0, "P2"], ["west", 1, "P2"], inp],
                            [["west", 0, "P3"], ["west", 1, "P2"], inp]
                        ]
                    case _:
                        return [
                            [["west", 0, "C3"], ["west", 1, "C2"], inp],
                            [["west", 0, "C2"], ["west", 1, "C2"], inp],
                            [["west", 0, "C1"], ["west", 1, "C1"], inp],
                            [["west", 0, "WC_b"], ["west", 1, "C1"], inp]
                        ]
            else:
                match ps_code:
                    case "A":
                        return [
                            [["east", 0, "WC_t"], ["east", 1, "A1"], inp],
                            [["east", 0, "A1"], ["east", 1, "A1"], inp],
                            [["east", 0, "A2"], ["east", 1, "A2"], inp],
                            [["east", 0, "A3"], ["east", 1, "A2"], inp]
                        ]
                    case _:
                        return [
                            [["east", 0, "M3"], ["east", 1, "M2"], inp],
                            [["east", 0, "M2"], ["east", 1, "M2"], inp],
                            [["east", 0, "M1"], ["east", 1, "M1"], inp],
                            [["east", 0, "WC_b"], ["east", 1, "M1"], inp]
                        ]
        elif rnd_code == 1:
            # quarter finalist
            if conf_code == "west":
                match ps_code:
                    case "P1":
                        return [
                            [["west", 0, "WC_t"], inp],
                            [["west", 0, "P1"], inp]
                        ]
                    case "P2":
                        return [
                            [["west", 0, "P2"], inp],
                            [["west", 0, "P3"], inp]
                        ]
                    case "C2":
                        return [
                            [["west", 0, "C3"], inp],
                            [["west", 0, "C2"], inp]
                        ]
                    case _:
                        return [
                            [["west", 0, "C1"], inp],
                            [["west", 0, "WC_b"], inp]
                        ]
            else:
                match ps_code:
                    case "A1":
                        return [
                            [["east", 0, "WC_t"], inp],
                            [["east", 0, "A1"], inp]
                        ]
                    case "A2":
                        return [
                            [["east", 0, "A2"], inp],
                            [["east", 0, "A3"], inp]
                        ]
                    case "M2":
                        return [
                            [["east", 0, "M3"], inp],
                            [["east", 0, "M2"], inp]
                        ]
                    case _:
                        return [
                            [["east", 0, "M1"], inp],
                            [["east", 0, "WC_b"], inp]
                        ]
        else:
            # round 1
            return [[inp]]

    def motion_ps(self, event, conf_code, rnd_code, ps_code):
        self.dragging.set(True)
        if self.canvas.itemcget(self.ps_codes[conf_code][rnd_code][ps_code]["tag_image"], "state") == "normal":
            self.drag_team.set(self.res_pyimage_to_t[
                                   self.canvas.itemcget(self.ps_codes[conf_code][rnd_code][ps_code]["tag_image"],
                                                        "image")])
        self.motion(event)

    def click_ps(self, event, conf_code, rnd_code, ps_code):
        print(f"click_ps {conf_code=}, {rnd_code=}, {ps_code=}")
        self.canvas.tag_raise(self.drag_rect)
        hidden = self.canvas.itemcget(
            self.ps_codes[conf_code][rnd_code][ps_code]["tag_image"],
            "state"
        ) == "hidden"
        if not hidden:
            self.canvas.itemconfigure(
                self.drag_rect,
                state="normal",
                image=self.canvas.itemcget(
                    self.ps_codes[conf_code][rnd_code][ps_code]["tag_image"],
                    "image"
                )
            )
            self.canvas.coords(
                self.drag_rect,
                event.x,
                event.y
            )

    def click_bank_team(self, event, team_name):
        try:
            b_x, b_y, b_img, b_tag = self.positions_bank_west_teams[team_name]
        except KeyError:
            try:
                b_x, b_y, b_img, b_tag = self.positions_bank_east_teams[team_name]
            except KeyError as ke:
                raise ke
        e_x, e_y = event.x, event.y
        self.canvas.itemconfigure(
            self.drag_rect,
            state="normal",
            image=b_img,
            anchor=tkinter.CENTER
        )
        self.canvas.coords(self.drag_rect, e_x, e_y)
        self.drag_team.set(team_name)
        self.dragging.set(True)

    # def motion_rect(self, event, rect):
    #     print(f"b1_motion {rect=}, {event=}")
    #     ex, ey = event.x, event.y
    #     ex -= (self.w_ps / 2)
    #     ey -= (self.h_ps / 2)
    #     self.canvas.tag_raise(rect)
    #     self.canvas.coords(rect, ex, ey)

    # def release_rect(self, event, rect):
    #     print(f"release_rect {rect=}, {event=}")

    def load_history(self):
        if not os.path.exists(os.path.join(os.getcwd(), self.history_file)):
            return
        with open(self.history_file, "r") as f:
            self.history = json.load(f)

    def load_images(self):

        if not os.path.exists(self.image_directory):
            self.image_directory = r"C:\Users\ABriggs\Documents\Coding Practice\Coding_Practice\Python\Hockey pool\Images"

        for pth in os.listdir(self.image_directory):
            team = pth.replace("logo", "").replace("_", " ").replace(".png", "").replace(".jpg", "").strip()
            if "division" in team or "conference" in team:
                continue
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


if __name__ == '__main__':
    # df = pd.read_excel(r"D:\NHL Standings 2024-03-22.xlsx")
    df = pd.read_excel(r"NHL Standings 2024-03-22.xlsx")
    df_sub = df[["Team", "PTS"]].copy()
    df_sub["Team"] = df_sub["Team"].str.lower().str.replace(".", "")
    # df_sub["Team"] = df_sub["Team"].apply(lambda t: t.lower().replace(".", ""))
    standings_20240322 = df_sub.set_index("Team")["PTS"].to_dict()

    print(f"{df_sub=}\n{standings_20240322=}")

    app = PlayoffChooser(standings_20240322)
    app.mainloop()

    # n_questions = 32
    # n_questions = 50
    # total_games = list(combinations(btn_images, 2))
    # shuffle(total_games)
    # total_games = sample(total_games, n_questions)
    # value, spq = 0, 1 / n_questions
    # print(f"{len(total_games)=}")
    # # for team_1, team_2 in total_games:
    # #     print(f"{team_1=}, {team_2=}")
    # choice_1 = total_games.pop(0)
    # team_1, team_2 = choice_1
    #
    # frame = tkinter.Frame(app)
    #
    # sp_q = n_questions
    # pb_frame = tkinter.Frame(frame)
    # pb_label = tkinter.Label(pb_frame, text="0 %")
    # progressbar = ttk.Progressbar(pb_frame, orient="horizontal", maximum=100, value=0, mode="determinate")
    #
    # # canvas_1 = tkinter.Canvas(frame, width=250, height=250)
    # # canvas_2 = tkinter.Canvas(frame, width=250, height=250)
    # #
    # # canvas_1.create_image(
    # #     10,
    # #     0,
    # #     anchor=tkinter.N,
    # #     image=btn_images[team_1]
    # # )
    # #
    # # canvas_2.create_image(
    # #     10,
    # #     10,
    # #     anchor=tkinter.N,
    # #     image=btn_images[team_2]
    # # )
    #
    # button_1 = tkinter.Button(frame, image=btn_images[team_1], command=lambda t1=team_1, t2=team_2: click(t1, t2))
    # button_2 = tkinter.Button(frame, image=btn_images[team_2], command=lambda t1=team_2, t2=team_1: click(t1, t2))
    #
    # frame.pack(side=tkinter.TOP)
    # pb_frame.pack(side=tkinter.TOP)
    # pb_label.pack(side=tkinter.LEFT)
    # progressbar.pack(side=tkinter.RIGHT)
    # # canvas_1.pack(side=tkinter.LEFT)
    # # canvas_2.pack(side=tkinter.RIGHT)
    # button_1.pack(side=tkinter.LEFT)
    # button_2.pack(side=tkinter.RIGHT)
    #
    # app.mainloop()
import os
import random
import tkinter

import pandas as pd
from PIL import ImageTk, Image
from itertools import combinations
from random import shuffle, sample
from tkinter import ttk

from colour_utility import gradient
from tkinter_utility import calc_geometry_tl

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
    'Buffalo': {'acr': 'BUF','mascot': 'Sabres', 'masc_short': 'Sabres', 'full': 'buffalo sabres'},
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
for div_n, div in {
    "pacific": pacific,
    "central": central,
    "metropolitan": metropolitan,
    "atlantic": atlantic
}.items():
    for t, t_dat in div.items():
        full_team_to_div[t_dat["full"].replace(".", "")] = div
        full_team_to_div_name[t_dat["full"].replace(".", "")] = div_n
full_team_to_conf = {t: ("w" if div_dat in (pacific, central) else "e") for t, div_dat in full_team_to_div.items()}
west_teams = [t for t, c in full_team_to_conf.items() if c == "w"]
east_teams = [t for t, c in full_team_to_conf.items() if c == "e"]


class PlayoffChooser(tkinter.Tk):

    def __init__(self, season_stats):
        super().__init__()
        self.season_stats = season_stats
        self.sorted_standings = sorted([(t, p) for t, p in self.season_stats.items()], key=lambda tup: tup[1], reverse=True)
        self.sorted_west = [tup for tup in self.sorted_standings if tup[0] in west_teams]
        self.sorted_east = [tup for tup in self.sorted_standings if tup[0] in east_teams]
        self.dims_root = 1500, 1000
        self.title("2024 Playoff Bracket Challenge")
        # self.calc_geometry = calc_geometry_tl(*self.dims_root, largest=2, rtype=dict)
        self.calc_geometry = calc_geometry_tl(*self.dims_root, largest=0, rtype=dict)
        self.geometry(self.calc_geometry["geometry"])

        self.bg_canvas = "#686868"
        self.bg_bank_west = "#7793EF"
        self.bg_empty_west = "#25339F"
        self.fg_empty_west = "#000000"
        self.font_empty_west = ("Arial", 14)
        self.bg_bank_east = "#e03535"
        self.bg_empty_east = "#8e1919"
        self.fg_empty_east = "#000000"
        self.font_empty_east = ("Arial", 14)
        self.bg_line_west = "#000000"
        self.bg_opt_ps_west = "#328944"
        self.bg_line_east = "#000000"
        self.bg_opt_ps_east = "#328944"
        self.w_line = 2
        self.bw_ps_west = 2

        self.w_ps = 75
        self.h_ps = 75
        self.w_space_between_rect = 35
        self.h_space_between_rect = 10
        self.pos_bank_west = (25, 25, 205, 25 + (8 * (self.h_ps + self.h_space_between_rect)))
        self.w_canvas, self.h_canvas = self.dims_root[0] * 0.9, self.dims_root[1] * 0.9


        #### NOTE ####
        # Stanley Cup Final PlayOff Spot is treated as though it is in the west conference


        # West PlayOff Spot Xs
        self.x_ps_w_r1 = self.pos_bank_west[2] + self.w_space_between_rect
        self.x_ps_w_r2 = self.x_ps_w_r1 + self.w_ps + self.w_space_between_rect
        self.x_ps_w_r3 = self.x_ps_w_r2 + self.w_ps + self.w_space_between_rect
        self.x_ps_w_r4 = self.x_ps_w_r3 + self.w_ps + self.w_space_between_rect
        self.x_ps_sc = self.x_ps_w_r4 + self.w_ps + self.w_space_between_rect

        # West PlayOff Spot Ys R1
        self.y_ps_wc_t_r1 = self.pos_bank_west[1] + (self.h_space_between_rect / 2)
        self.y_ps_p1_r1 = self.y_ps_wc_t_r1 + self.h_ps + self.h_space_between_rect
        self.y_ps_p2_r1 = self.y_ps_wc_t_r1 + (2 * (self.h_ps + self.h_space_between_rect))
        self.y_ps_p3_r1 = self.y_ps_wc_t_r1 + (3 * (self.h_ps + self.h_space_between_rect))
        self.y_ps_c3_r1 = self.y_ps_wc_t_r1 + (4 * (self.h_ps + self.h_space_between_rect))
        self.y_ps_c2_r1 = self.y_ps_wc_t_r1 + (5 * (self.h_ps + self.h_space_between_rect))
        self.y_ps_c1_r1 = self.y_ps_wc_t_r1 + (6 * (self.h_ps + self.h_space_between_rect))
        self.y_ps_wx_b_r1 = self.y_ps_wc_t_r1 + (7 * (self.h_ps + self.h_space_between_rect))

        # West PlayOff Spot Ys R1
        self.y_ps_w_r2_p1 = self.y_ps_wc_t_r1 + ((self.y_ps_p1_r1 - self.y_ps_wc_t_r1) / 2)
        self.y_ps_w_r2_p2 = self.y_ps_p2_r1 + ((self.y_ps_p3_r1 - self.y_ps_p2_r1) / 2)
        self.y_ps_w_r2_c2 = self.y_ps_c3_r1 + ((self.y_ps_c2_r1 - self.y_ps_c3_r1) / 2)
        self.y_ps_w_r2_c1 = self.y_ps_c1_r1 + ((self.y_ps_wx_b_r1 - self.y_ps_c1_r1) / 2)

        # West PlayOff Spot Ys R2
        self.y_ps_w_r3_p = self.y_ps_w_r2_p1 + ((self.y_ps_w_r2_p2 - self.y_ps_w_r2_p1) / 2)
        self.y_ps_w_r3_c = self.y_ps_w_r2_c1 + ((self.y_ps_w_r2_c2 - self.y_ps_w_r2_c1) / 2)

        # West PlayOff Spot Ys R3
        self.y_ps_w_r4_w = self.y_ps_w_r3_p + ((self.y_ps_w_r3_c - self.y_ps_w_r3_p) / 2)

        # West PlayOff Spot Ys SC
        self.y_ps_sc = self.y_ps_w_r3_p + ((self.y_ps_w_r3_c - self.y_ps_w_r3_p) / 2)

        print(f"{self.x_ps_w_r1=}, {self.y_ps_wc_t_r1=}")
        print(f"{self.x_ps_w_r2=}, {self.y_ps_p1_r1=}")
        print(f"{self.x_ps_w_r3=}, {self.y_ps_p2_r1=}")
        print(f"{self.x_ps_w_r4=}, {self.y_ps_p3_r1=}")

        self.image_directory = r"C:\Users\abrig\Documents\Coding_Practice\Python\Hockey pool\Images"
        self.btn_images = {}
        self.res_images = {}
        self.res_img_to_t = {}
        self.res_pyimage_to_t = {}
        self.history = {}
        self.full_size_image = (200, 200)
        self.small_size_image = (self.w_ps, self.h_ps)

        self.load_images()

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
            "y0": self.y_ps_wx_b_r1,
            "x1": self.x_ps_w_r1 + self.w_ps,
            "y1": self.y_ps_wx_b_r1 + self.h_ps,
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

        for conf, conf_data in self.ps_codes.items():
            for rnd, round_data in conf_data.items():
                for ps_code, ps_data in round_data.items():
                    print(f"{conf=}, {rnd=}, {ps_code=}")
                    t_rect = self.canvas.create_rectangle(
                        ps_data["x0"],
                        ps_data["y0"],
                        ps_data["x1"],
                        ps_data["y1"],
                        fill=self.bg_empty_west,
                        width=self.bw_ps_west
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
                    self.ps_codes[conf][rnd][ps_code].update({
                        "tag_rect": t_rect,
                        "tag_text": t_text,
                        "tag_image": t_img
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
            self.y_ps_wx_b_r1 + (self.h_ps / 2),
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

        for k, line in self.lines.items():
            self.canvas.itemconfigure(
                line,
                fill=self.bg_line_west,
                width=self.w_line
            )
            self.canvas.tag_lower(line)

        # self.rect_ps_w_wc_b = self.canvas.create_rectangle(
        #     self.x_ps_w_r1,
        #     self.y_ps_wx_b_r1,
        #     self.x_ps_w_r1 + self.w_ps,
        #     self.y_ps_wx_b_r1 + self.h_ps,
        #     fill=self.bg_empty_west
        # )
        # self.text_ps_w_wc_b = self.canvas.create_text(
        #     self.x_ps_w_r1 + (self.w_ps / 2),
        #     self.y_ps_wx_b_r1 + (self.h_ps / 2),
        #     text="WC",
        #     fill=self.fg_empty_west,
        #     font=self.font_empty_west
        # )
        # self.img_ps_w_wc_b = self.canvas.create_image(
        #     self.x_ps_w_r1,
        #     self.y_ps_wx_b_r1,
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
        #     self.y_ps_wx_b_r1,
        #     self.x_ps_w_r1 + self.w_ps,
        #     self.y_ps_wx_b_r1 + self.h_ps,
        #     fill=self.bg_empty_west
        # )
        # self.text_ps_w_wc_b = self.canvas.create_text(
        #     self.x_ps_w_r1 + (self.w_ps / 2),
        #     self.y_ps_wx_b_r1 + (self.h_ps / 2),
        #     text="WC",
        #     fill=self.fg_empty_west,
        #     font=self.font_empty_west
        # )
        # self.img_ps_w_wc_b = self.canvas.create_image(
        #     self.x_ps_w_r1,
        #     self.y_ps_wx_b_r1,
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
                    "rect": list(map(lambda i_x: (i_x[1] + self.bw_ps_west) if (i_x[0] < 2) else (i_x[1] - self.bw_ps_west), enumerate(self.canvas.bbox(dat["tag_rect"])))),
                    "text": self.canvas.bbox(dat["tag_text"])
                }
                for k, dat in rnd_dat.items()
            }
            for rnd, rnd_dat in self.ps_codes["west"].items()
        }
        self.positions_bank_west_teams = {}

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

        self.valid_ps_codes_root_a = ["A1", "A2", "A3", "WC_t", "A"]
        self.valid_ps_codes_root_op_a = ["WC_b", "M1", "M"]
        self.valid_ps_codes_a = [*self.valid_ps_codes_root_a, *self.valid_ps_codes_root_op_a, "E", "SC"]

        self.valid_ps_codes_root_m = ["M1", "M2", "M3", "WC_b", "M"]
        self.valid_ps_codes_root_op_m = ["WC_t", "A1", "A"]
        self.valid_ps_codes_m = [*self.valid_ps_codes_root_m, *self.valid_ps_codes_root_op_m, "E", "SC"]

        self.valid_ps_codes_root_c = ["C1", "C2", "C3", "WC_b", "C"]
        self.valid_ps_codes_root_op_c = ["WC_t", "P1", "P"]
        self.valid_ps_codes_c = [*self.valid_ps_codes_root_c, *self.valid_ps_codes_root_op_c, "W", "SC"]

        self.valid_ps_codes_root_p = ["P1", "P2", "P3", "WC_t", "P"]
        self.valid_ps_codes_root_op_p = ["WC_b", "C1", "C"]
        self.valid_ps_codes_p = [*self.valid_ps_codes_root_p, *self.valid_ps_codes_root_op_p, "W", "SC"]

        self.valid_ps_codes_list_a = [self.valid_ps_codes_root_a, self.valid_ps_codes_root_op_a, self.valid_ps_codes_a]
        self.valid_ps_codes_list_m = [self.valid_ps_codes_root_m, self.valid_ps_codes_root_op_m, self.valid_ps_codes_m]
        self.valid_ps_codes_list_c = [self.valid_ps_codes_root_c, self.valid_ps_codes_root_op_c, self.valid_ps_codes_c]
        self.valid_ps_codes_list_p = [self.valid_ps_codes_root_p, self.valid_ps_codes_root_op_p, self.valid_ps_codes_p]

        self.canvas.bind("<ButtonRelease-1>", self.release_click)
        self.canvas.bind("<B1-Motion>", self.motion)
        self.canvas.tag_raise(self.drag_rect)

        # for img in self.west_images:
        #     self.canvas.itemconfigure(img, state="hidden")

    def collide_bbox_point(self, bbox_a, point):
        x0_a, y0_a, x1_a, y1_a = bbox_a
        x_p, y_p = point
        return all([
            x0_a <= x_p <= x1_a,
            y0_a <= y_p <= y1_a
        ])

    def motion(self, event):
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
            print(f"{drag_team=}, {drag_div=}")

            tol = 1e-10
            for rnd_code, rnd_dat in self.positions_ps_west.items():
                for ps_code, dat in rnd_dat.items():
                    # for k, bbox in dat.items():
                    # k = "rect"
                    bbox = dat["rect"]
                    paths = []
                    p_y = ((e_y - bbox[1]) / self.h_ps)
                    if self.collide_bbox_point(bbox, point):
                        paths = self.calc_path("west", rnd_code, ps_code)
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
                            if drag_div == "P":
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
        grad = [gradient(i+1, 10, sc, ec, rgb=False) for i in range(10)]
        for i, c in enumerate(grad):
            self.after(
                i * 100,
                lambda: self.canvas.itemconfigure(
                    self.ps_codes[conf_code][rnd_code][ps_code]["tag_rect"],
                    outline=c
                )
            )

    def release_click(self, event):
        print(f"RELEASE ", end="")
        is_dragging = self.dragging.get()
        e_x, e_y = event.x, event.y
        point = (e_x, e_y)
        tol = 1e-10
        drag_team = self.drag_team.get()
        drag_div = full_team_to_div_name[drag_team].upper()[0]
        # bbox_drag = self.canvas.bbox(self.drag_rect)
        if is_dragging:
            print(f"DRAG ", end="")
            for rnd_code, rnd_dat in self.positions_ps_west.items():
                for ps_code, dat in rnd_dat.items():
                    # for k, bbox in dat.items():
                    bbox = dat["rect"]
                    if self.collide_bbox_point(bbox, point):
                        print(f"COLLIDE cc='west', rc={rnd_code}, pc={ps_code} ", end="")
                        p_y = ((e_y - bbox[1]) / self.h_ps)
                        # # release in a ps spot
                        # print(f"Release {rnd_code=} {ps_code=}, {k=}")
                        # # check that previous spots not empty
                        # do_change = False

                        paths = self.calc_path("west", rnd_code, ps_code)
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
                            if drag_div == "P":
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
                            case "M":
                                do_change = ps_code in self.valid_ps_codes_m
                            case "C":
                                do_change = ps_code in self.valid_ps_codes_c
                            case _:
                                do_change = ps_code in self.valid_ps_codes_p

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
                            for pc in self.ps_codes["west"][0]:
                                cc = "west"
                                rc = 0
                                if ((cc != path[0][0]) or (rc != path[0][1]) or (pc != path[0][2])) \
                                        and self.canvas.itemcget(
                                    self.ps_codes[cc][rc][pc]["tag_image"],
                                    "image"
                                ) == drag_img:
                                    # path already exists
                                    print(f"path already exists")
                                    clear_path = self.calc_path_2_sc(cc, rc, pc)
                                    # do_change = False

                            print(f"PAE {clear_path=}")
                            if clear_path:
                                for cc, rc, pc in clear_path[0]:
                                    if rc <= rnd_code:
                                        print(f"PAE {cc=}, {rc=}, {pc=}")
                                        self.canvas.itemconfigure(
                                            self.ps_codes[cc][rc][pc]["tag_image"],
                                            state="hidden"
                                        )


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
                                self.flash_ps(cc, rc, pc)

                            # use the last path key to check the logic
                            path_sc = self.calc_path_2_sc(cc, rc, pc)
                            print(f"{path_sc[0]=}")
                            for cc, rc, pc in path_sc[0]:
                                if (cc == "west") and (rc == rnd_code) and (pc == ps_code):
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
                                    paths_ = self.calc_path(c_cc, c_rc, c_pc)

                                    if drag_div == "P":
                                        paths_ = paths_[:5]
                                    elif drag_div == "C":
                                        paths_ = paths_[5:10]
                                    elif drag_div == "A":
                                        paths_ = paths_[10:15]
                                    else:
                                        paths_ = paths_[15:]

                                    print(f"{paths_=}")
                                    parents = [list(tup) for tup in (set([tuple(path[-2]) for path in paths_]))]
                                    print(f"{parents=}")
                                    # parents.remove(())
                                    if parents:
                                        # p_cc, p_rc, p_pc = parents[0]

                                        print(f"{c_cc=}, {c_rc=}, {c_pc=}", end="")
                                        img_child = self.canvas.itemcget(
                                            self.ps_codes[c_cc][c_rc][c_pc],
                                            "image"
                                        )
                                        for p_cc, p_rc, p_pc in parents:
                                            print(f"{p_cc=}, {p_rc=}, {p_pc=}", end="")
                                            if (p_cc != path[-2][0]) or (p_rc != path[-2][1]) or (p_pc != path[-2][2]):
                                                img_parents = self.canvas.itemcget(
                                                    self.ps_codes[p_cc][p_rc][p_pc],
                                                    "image"
                                                )
                                                # ((rnd_code + 1) < rc) and (
                                                if img_parents == img_child:
                                                    print(f"\tB BLANK")
                                                    self.canvas.itemconfigure(
                                                        self.ps_codes[c_cc][c_rc][c_pc]["tag_image"],
                                                        state="hidden"
                                                    )
                                                else:
                                                    print(f"-B")

                                            else:
                                                print(f"-A")

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
        if rnd_code == 4:
            return [[inp]]
        elif rnd_code == 3:
            return [
                [inp, [conf_code, 4, "SC"]]
            ]
        elif rnd_code == 2:
            if conf_code == "east":
                return [
                    [inp, [conf_code, 3, "E"], [conf_code, 4, "SC"]]
                ]
            else:
                return [
                    [inp, [conf_code, 3, "W"], [conf_code, 4, "SC"]]
                ]
        elif rnd_code == 1:
            if conf_code == "east":
                if ps_code in self.valid_ps_codes_root_a:
                    return [
                        [inp, [conf_code, 2, "A"], [conf_code, 3, "E"], [conf_code, 4, "SC"]]
                    ]
                else:
                    return [
                        [inp, [conf_code, 2, "M"], [conf_code, 3, "E"], [conf_code, 4, "SC"]]
                    ]
            else:
                if ps_code in self.valid_ps_codes_root_p:
                    return [
                        [inp, [conf_code, 2, "P"], [conf_code, 3, "W"], [conf_code, 4, "SC"]]
                    ]
                else:
                    return [
                        [inp, [conf_code, 2, "C"], [conf_code, 3, "W"], [conf_code, 4, "SC"]]
                    ]
        else:
            if conf_code == "east":
                if ps_code in self.valid_ps_codes_root_a[:2]:
                    return [
                        [inp, [conf_code, 1, "A1"], [conf_code, 2, "A"], [conf_code, 3, "E"], [conf_code, 4, "SC"]]
                    ]
                elif ps_code in self.valid_ps_codes_root_a[2:4]:
                    return [
                        [inp, [conf_code, 1, "A2"], [conf_code, 2, "A"], [conf_code, 3, "E"], [conf_code, 4, "SC"]]
                    ]
                elif ps_code in self.valid_ps_codes_root_m[:2]:
                    return [
                        [inp, [conf_code, 1, "M2"], [conf_code, 2, "M"], [conf_code, 3, "E"], [conf_code, 4, "SC"]]
                    ]
                else:
                    return [
                        [inp, [conf_code, 1, "M1"], [conf_code, 2, "M"], [conf_code, 3, "E"], [conf_code, 4, "SC"]]
                    ]
            else:
                if ps_code in self.valid_ps_codes_root_p[:2]:
                    return [
                        [inp, [conf_code, 1, "P1"], [conf_code, 2, "P"], [conf_code, 3, "W"], [conf_code, 4, "SC"]]
                    ]
                elif ps_code in self.valid_ps_codes_root_p[2:4]:
                    return [
                        [inp, [conf_code, 1, "P2"], [conf_code, 2, "P"], [conf_code, 3, "W"], [conf_code, 4, "SC"]]
                    ]
                elif ps_code in self.valid_ps_codes_root_c[:2]:
                    return [
                        [inp, [conf_code, 1, "C2"], [conf_code, 2, "C"], [conf_code, 3, "W"], [conf_code, 4, "SC"]]
                    ]
                else:
                    return [
                        [inp, [conf_code, 1, "C1"], [conf_code, 2, "C"], [conf_code, 3, "W"], [conf_code, 4, "SC"]]
                    ]

    def calc_path(self, conf_code, rnd_code, ps_code):
        inp = [conf_code, rnd_code, ps_code]
        if rnd_code == 4:
            # stanley cup finalist
            return [
                [[conf_code, 0, "WC_t"], [conf_code, 1, "P1"], [conf_code, 2, "P"], [conf_code, 3, "W"], inp],
                [[conf_code, 0, "P1"], [conf_code, 1, "P1"], [conf_code, 2, "P"], [conf_code, 3, "W"], inp],
                [[conf_code, 0, "P2"], [conf_code, 1, "P2"], [conf_code, 2, "P"], [conf_code, 3, "W"], inp],
                [[conf_code, 0, "P3"], [conf_code, 1, "P2"], [conf_code, 2, "P"], [conf_code, 3, "W"], inp],
                [[conf_code, 0, "WC_b"], [conf_code, 1, "C1"], [conf_code, 2, "C"], [conf_code, 3, "W"], inp],

                [[conf_code, 0, "WC_t"], [conf_code, 1, "P1"], [conf_code, 2, "P"], [conf_code, 3, "W"], inp],
                [[conf_code, 0, "C3"], [conf_code, 1, "C2"], [conf_code, 2, "C"], [conf_code, 3, "W"], inp],
                [[conf_code, 0, "C2"], [conf_code, 1, "C2"], [conf_code, 2, "C"], [conf_code, 3, "W"], inp],
                [[conf_code, 0, "C1"], [conf_code, 1, "C1"], [conf_code, 2, "C"], [conf_code, 3, "W"], inp],
                [[conf_code, 0, "WC_b"], [conf_code, 1, "C1"], [conf_code, 2, "C"], [conf_code, 3, "W"], inp],

                [[conf_code, 0, "WC_t"], [conf_code, 1, "A1"], [conf_code, 2, "A"], [conf_code, 3, "E"], inp],
                [[conf_code, 0, "A1"], [conf_code, 1, "A1"], [conf_code, 2, "A"], [conf_code, 3, "E"], inp],
                [[conf_code, 0, "A2"], [conf_code, 1, "A2"], [conf_code, 2, "A"], [conf_code, 3, "E"], inp],
                [[conf_code, 0, "A3"], [conf_code, 1, "A2"], [conf_code, 2, "A"], [conf_code, 3, "E"], inp],
                [[conf_code, 0, "WC_b"], [conf_code, 1, "M1"], [conf_code, 2, "M"], [conf_code, 3, "E"], inp],

                [[conf_code, 0, "WC_t"], [conf_code, 1, "A1"], [conf_code, 2, "A"], [conf_code, 3, "E"], inp],
                [[conf_code, 0, "M3"], [conf_code, 1, "M2"], [conf_code, 2, "M"], [conf_code, 3, "E"], inp],
                [[conf_code, 0, "M2"], [conf_code, 1, "M2"], [conf_code, 2, "M"], [conf_code, 3, "E"], inp],
                [[conf_code, 0, "M1"], [conf_code, 1, "M1"], [conf_code, 2, "M"], [conf_code, 3, "E"], inp],
                [[conf_code, 0, "WC_b"], [conf_code, 1, "M1"], [conf_code, 2, "M"], [conf_code, 3, "E"], inp]
            ]
        elif rnd_code == 3:
            # conf finalist
            match ps_code:
                case "W":
                    return [
                        [[conf_code, 0, "WC_t"], [conf_code, 1, "P1"], [conf_code, 2, "P"], inp],
                        [[conf_code, 0, "P1"], [conf_code, 1, "P1"], [conf_code, 2, "P"], inp],
                        [[conf_code, 0, "P2"], [conf_code, 1, "P2"], [conf_code, 2, "P"], inp],
                        [[conf_code, 0, "P3"], [conf_code, 1, "P2"], [conf_code, 2, "P"], inp],
                        [[conf_code, 0, "WC_b"], [conf_code, 1, "C1"], [conf_code, 2, "C"], inp],

                        [[conf_code, 0, "WC_t"], [conf_code, 1, "P1"], [conf_code, 2, "P"], inp],
                        [[conf_code, 0, "C3"], [conf_code, 1, "C2"], [conf_code, 2, "C"], inp],
                        [[conf_code, 0, "C2"], [conf_code, 1, "C2"], [conf_code, 2, "C"], inp],
                        [[conf_code, 0, "C1"], [conf_code, 1, "C1"], [conf_code, 2, "C"], inp],
                        [[conf_code, 0, "WC_b"], [conf_code, 1, "C1"], [conf_code, 2, "C"], inp]
                    ]
                case _:
                    return [
                        [[conf_code, 0, "WC_t"], [conf_code, 1, "A1"], [conf_code, 2, "A"], inp],
                        [[conf_code, 0, "A1"], [conf_code, 1, "A1"], [conf_code, 2, "A"], inp],
                        [[conf_code, 0, "A2"], [conf_code, 1, "A2"], [conf_code, 2, "A"], inp],
                        [[conf_code, 0, "A3"], [conf_code, 1, "A2"], [conf_code, 2, "A"], inp],
                        [[conf_code, 0, "WC_b"], [conf_code, 1, "M1"], [conf_code, 2, "M"], inp],

                        [[conf_code, 0, "WC_t"], [conf_code, 1, "A1"], [conf_code, 2, "A"], inp],
                        [[conf_code, 0, "M3"], [conf_code, 1, "M2"], [conf_code, 2, "M"], inp],
                        [[conf_code, 0, "M2"], [conf_code, 1, "M2"], [conf_code, 2, "M"], inp],
                        [[conf_code, 0, "M1"], [conf_code, 1, "M1"], [conf_code, 2, "M"], inp],
                        [[conf_code, 0, "WC_b"], [conf_code, 1, "M1"], [conf_code, 2, "M"], inp]
                    ]
        elif rnd_code == 2:
            # div finalist
            if conf_code == "west":
                match ps_code:
                    case "P":
                        return [
                            [[conf_code, 0, "WC_t"], [conf_code, 1, "P1"], inp],
                            [[conf_code, 0, "P1"], [conf_code, 1, "P1"], inp],
                            [[conf_code, 0, "P2"], [conf_code, 1, "P2"], inp],
                            [[conf_code, 0, "P3"], [conf_code, 1, "P2"], inp]
                        ]
                    case _:
                        return [
                            [[conf_code, 0, "C3"], [conf_code, 1, "C2"], inp],
                            [[conf_code, 0, "C2"], [conf_code, 1, "C2"], inp],
                            [[conf_code, 0, "C1"], [conf_code, 1, "C1"], inp],
                            [[conf_code, 0, "WC_b"], [conf_code, 1, "C1"], inp]
                        ]
            else:
                match ps_code:
                    case "A":
                        return [
                            [[conf_code, 0, "WC_t"], [conf_code, 1, "A1"], inp],
                            [[conf_code, 0, "A1"], [conf_code, 1, "A1"], inp],
                            [[conf_code, 0, "A2"], [conf_code, 1, "A2"], inp],
                            [[conf_code, 0, "A3"], [conf_code, 1, "A2"], inp]
                        ]
                    case _:
                        return [
                            [[conf_code, 0, "M3"], [conf_code, 1, "M2"], inp],
                            [[conf_code, 0, "M2"], [conf_code, 1, "M2"], inp],
                            [[conf_code, 0, "M1"], [conf_code, 1, "M1"], inp],
                            [[conf_code, 0, "WC_b"], [conf_code, 1, "M1"], inp]
                        ]
        elif rnd_code == 1:
            # quarter finalist
            if conf_code == "west":
                match ps_code:
                    case "P1":
                        return [
                            [[conf_code, 0, "WC_t"], inp],
                            [[conf_code, 0, "P1"], inp]
                        ]
                    case "P2":
                        return [
                            [[conf_code, 0, "P2"], inp],
                            [[conf_code, 0, "P3"], inp]
                        ]
                    case "C2":
                        return [
                            [[conf_code, 0, "C3"], inp],
                            [[conf_code, 0, "C2"], inp]
                        ]
                    case _:
                        return [
                            [[conf_code, 0, "C1"], inp],
                            [[conf_code, 0, "WC_b"], inp]
                        ]
            else:
                match ps_code:
                    case "A1":
                        return [
                            [[conf_code, 0, "WC_t"], inp],
                            [[conf_code, 0, "A1"], inp]
                        ]
                    case "A2":
                        return [
                            [[conf_code, 0, "A2"], inp],
                            [[conf_code, 0, "A3"], inp]
                        ]
                    case "M2":
                        return [
                            [[conf_code, 0, "M3"], inp],
                            [[conf_code, 0, "M2"], inp]
                        ]
                    case _:
                        return [
                            [[conf_code, 0, "M1"], inp],
                            [[conf_code, 0, "WC_b"], inp]
                        ]
        else:
            # round 1
            return [[inp]]

    def motion_ps(self, event, conf_code, rnd_code, ps_code):
        self.dragging.set(True)
        if self.canvas.itemcget(self.ps_codes[conf_code][rnd_code][ps_code]["tag_image"], "state") == "normal":
            self.drag_team.set(self.res_pyimage_to_t[self.canvas.itemcget(self.ps_codes[conf_code][rnd_code][ps_code]["tag_image"], "image")])
        self.motion(event)

    def click_ps(self, event, conf_code, rnd_code, ps_code):
        print(f"click_ps {conf_code=}, {rnd_code=}, {ps_code=}")
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
        b_x, b_y, b_img, b_tag = self.positions_bank_west_teams[team_name]
        e_x, e_y = event.x, event.y
        self.canvas.itemconfigure(
            self.drag_rect,
            state="normal",
            image=b_img,
            anchor=tkinter.CENTER
        )
        self.canvas.coords(self.drag_rect, e_x, e_y)
        self.dragging.set(True)
        self.drag_team.set(team_name)


    # def motion_rect(self, event, rect):
    #     print(f"motion {rect=}, {event=}")
    #     ex, ey = event.x, event.y
    #     ex -= (self.w_ps / 2)
    #     ey -= (self.h_ps / 2)
    #     self.canvas.tag_raise(rect)
    #     self.canvas.coords(rect, ex, ey)

    # def release_rect(self, event, rect):
    #     print(f"release_rect {rect=}, {event=}")

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
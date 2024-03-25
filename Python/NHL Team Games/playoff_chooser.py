import os
import random
import tkinter

import pandas as pd
from PIL import ImageTk, Image
from itertools import combinations
from random import shuffle, sample
from tkinter import ttk


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
for div_n, div in {
    "pacific": pacific,
    "central": central,
    "metropolitan": metropolitan,
    "atlantic": atlantic
}.items():
    for t, t_dat in div.items():
        full_team_to_div[t_dat["full"].replace(".", "")] = div
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
        self.geometry(f"{self.dims_root[0]}x{self.dims_root[0]}")

        self.bg_canvas = "#686868"
        self.bg_bank_west = "#7793EF"
        self.bg_empty_west = "#25339F"
        self.fg_empty_west = "#000000"
        self.font_empty_west = ("Arial", 14)
        self.bg_bank_east = "#e03535"
        self.bg_empty_east = "#8e1919"
        self.fg_empty_east = "#000000"
        self.font_empty_east = ("Arial", 14)

        self.w_ps = 50
        self.h_ps = 50
        self.w_space_between_rect = 25
        self.h_space_between_rect = 10
        self.pos_bank_west = (25, 25, 155, 25 + (8 * (self.h_ps + self.h_space_between_rect)))
        self.w_canvas, self.h_canvas = self.dims_root[0] * 0.9, self.dims_root[1] * 0.9
        self.x_ps_w_r1 = self.pos_bank_west[2] + self.w_space_between_rect
        self.x_ps_w_r2 = self.x_ps_w_r1 + self.w_ps + self.w_space_between_rect
        self.x_ps_w_r3 = self.x_ps_w_r2 + self.w_ps + self.w_space_between_rect
        self.x_ps_w_r4 = self.x_ps_w_r3 + self.w_ps + self.w_space_between_rect

        self.y_ps_wc_t_r1 = self.pos_bank_west[1] + (self.h_space_between_rect / 2)
        self.y_ps_p1_r1 = self.y_ps_wc_t_r1 + self.h_ps + self.h_space_between_rect
        self.y_ps_p2_r1 = self.y_ps_wc_t_r1 + (2 * (self.h_ps + self.h_space_between_rect))
        self.y_ps_p3_r1 = self.y_ps_wc_t_r1 + (3 * (self.h_ps + self.h_space_between_rect))
        self.y_ps_c3_r1 = self.y_ps_wc_t_r1 + (4 * (self.h_ps + self.h_space_between_rect))
        self.y_ps_c2_r1 = self.y_ps_wc_t_r1 + (5 * (self.h_ps + self.h_space_between_rect))
        self.y_ps_c1_r1 = self.y_ps_wc_t_r1 + (6 * (self.h_ps + self.h_space_between_rect))
        self.y_ps_wx_b_r1 = self.y_ps_wc_t_r1 + (7 * (self.h_ps + self.h_space_between_rect))

        print(f"{self.x_ps_w_r1=}, {self.y_ps_wc_t_r1=}")
        print(f"{self.x_ps_w_r2=}, {self.y_ps_p1_r1=}")
        print(f"{self.x_ps_w_r3=}, {self.y_ps_p2_r1=}")
        print(f"{self.x_ps_w_r4=}, {self.y_ps_p3_r1=}")

        self.image_directory = r"C:\Users\abrig\Documents\Coding_Practice\Python\Hockey pool\Images"
        self.btn_images = {}
        self.res_images = {}
        self.history = {}
        self.full_size_image = (200, 200)
        self.small_size_image = (self.w_ps, self.h_ps)

        self.load_images()

        # sample_west_teams = random.sample(west_teams, 8)
        sample_west_teams = [t for t, p in self.sorted_west]


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
            0, 0, image=self.res_images[self.sorted_west[0][0]],
            state="hidden"
        )

        # west wildcard top
        self.rect_ps_w_wc_t = self.canvas.create_rectangle(
            self.x_ps_w_r1,
            self.y_ps_wc_t_r1,
            self.x_ps_w_r1 + self.w_ps,
            self.y_ps_wc_t_r1 + self.h_ps,
            fill=self.bg_empty_west
        )
        self.text_ps_w_wc_t = self.canvas.create_text(
            self.x_ps_w_r1 + (self.w_ps / 2),
            self.y_ps_wc_t_r1 + (self.h_ps / 2),
            text="WC",
            fill=self.fg_empty_west,
            font=self.font_empty_west
        )
        self.img_ps_w_wc_t = self.canvas.create_image(
            self.x_ps_w_r1,
            self.y_ps_wc_t_r1,
            image=self.res_images[sample_west_teams[0]],
            anchor=tkinter.NW
        )

        # pacific 1
        self.rect_ps_w_p1 = self.canvas.create_rectangle(
            self.x_ps_w_r1,
            self.y_ps_p1_r1,
            self.x_ps_w_r1 + self.w_ps,
            self.y_ps_p1_r1 + self.h_ps,
            fill=self.bg_empty_west
        )
        self.text_ps_w_p1 = self.canvas.create_text(
            self.x_ps_w_r1 + (self.w_ps / 2),
            self.y_ps_p1_r1 + (self.h_ps / 2),
            text="P1",
            fill=self.fg_empty_west,
            font=self.font_empty_west
        )
        self.img_ps_w_p1 = self.canvas.create_image(
            self.x_ps_w_r1,
            self.y_ps_p1_r1,
            image=self.res_images[sample_west_teams[1]],
            anchor=tkinter.NW
        )

        # pacific 2
        self.rect_ps_w_p2 = self.canvas.create_rectangle(
            self.x_ps_w_r1,
            self.y_ps_p2_r1,
            self.x_ps_w_r1 + self.w_ps,
            self.y_ps_p2_r1 + self.h_ps,
            fill=self.bg_empty_west
        )
        self.text_ps_w_p2 = self.canvas.create_text(
            self.x_ps_w_r1 + (self.w_ps / 2),
            self.y_ps_p2_r1 + (self.h_ps / 2),
            text="P2",
            fill=self.fg_empty_west,
            font=self.font_empty_west
        )
        self.img_ps_w_p2 = self.canvas.create_image(
            self.x_ps_w_r1,
            self.y_ps_p2_r1,
            image=self.res_images[sample_west_teams[2]],
            anchor=tkinter.NW
        )

        # pacific 3
        self.rect_ps_w_p3 = self.canvas.create_rectangle(
            self.x_ps_w_r1,
            self.y_ps_p3_r1,
            self.x_ps_w_r1 + self.w_ps,
            self.y_ps_p3_r1 + self.h_ps,
            fill=self.bg_empty_west
        )
        self.text_ps_w_p3 = self.canvas.create_text(
            self.x_ps_w_r1 + (self.w_ps / 2),
            self.y_ps_p3_r1 + (self.h_ps / 2),
            text="P3",
            fill=self.fg_empty_west,
            font=self.font_empty_west
        )
        self.img_ps_w_p3 = self.canvas.create_image(
            self.x_ps_w_r1,
            self.y_ps_p3_r1,
            image=self.res_images[sample_west_teams[3]],
            anchor=tkinter.NW
        )

        # central 3
        self.rect_ps_w_c3 = self.canvas.create_rectangle(
            self.x_ps_w_r1,
            self.y_ps_c3_r1,
            self.x_ps_w_r1 + self.w_ps,
            self.y_ps_c3_r1 + self.h_ps,
            fill=self.bg_empty_west
        )
        self.text_ps_w_c3 = self.canvas.create_text(
            self.x_ps_w_r1 + (self.w_ps / 2),
            self.y_ps_c3_r1 + (self.h_ps / 2),
            text="C3",
            fill=self.fg_empty_west,
            font=self.font_empty_west
        )
        self.img_ps_w_c3 = self.canvas.create_image(
            self.x_ps_w_r1,
            self.y_ps_c3_r1,
            image=self.res_images[sample_west_teams[4]],
            anchor=tkinter.NW
        )

        # central 2
        self.rect_ps_w_c2 = self.canvas.create_rectangle(
            self.x_ps_w_r1,
            self.y_ps_c2_r1,
            self.x_ps_w_r1 + self.w_ps,
            self.y_ps_c2_r1 + self.h_ps,
            fill=self.bg_empty_west
        )
        self.text_ps_w_c2 = self.canvas.create_text(
            self.x_ps_w_r1 + (self.w_ps / 2),
            self.y_ps_c2_r1 + (self.h_ps / 2),
            text="C2",
            fill=self.fg_empty_west,
            font=self.font_empty_west
        )
        self.img_ps_w_c2 = self.canvas.create_image(
            self.x_ps_w_r1,
            self.y_ps_c2_r1,
            image=self.res_images[sample_west_teams[5]],
            anchor=tkinter.NW
        )

        # central 1
        self.rect_ps_w_c1 = self.canvas.create_rectangle(
            self.x_ps_w_r1,
            self.y_ps_c1_r1,
            self.x_ps_w_r1 + self.w_ps,
            self.y_ps_c1_r1 + self.h_ps,
            fill=self.bg_empty_west
        )
        self.text_ps_w_c1 = self.canvas.create_text(
            self.x_ps_w_r1 + (self.w_ps / 2),
            self.y_ps_c1_r1 + (self.h_ps / 2),
            text="C1",
            fill=self.fg_empty_west,
            font=self.font_empty_west
        )
        self.img_ps_w_c1 = self.canvas.create_image(
            self.x_ps_w_r1,
            self.y_ps_c1_r1,
            image=self.res_images[sample_west_teams[6]],
            anchor=tkinter.NW
        )

        # west wild card bottom
        self.rect_ps_w_wc_b = self.canvas.create_rectangle(
            self.x_ps_w_r1,
            self.y_ps_wx_b_r1,
            self.x_ps_w_r1 + self.w_ps,
            self.y_ps_wx_b_r1 + self.h_ps,
            fill=self.bg_empty_west
        )
        self.text_ps_w_wc_b = self.canvas.create_text(
            self.x_ps_w_r1 + (self.w_ps / 2),
            self.y_ps_wx_b_r1 + (self.h_ps / 2),
            text="WC",
            fill=self.fg_empty_west,
            font=self.font_empty_west
        )
        self.img_ps_w_wc_b = self.canvas.create_image(
            self.x_ps_w_r1,
            self.y_ps_wx_b_r1,
            image=self.res_images[sample_west_teams[7]],
            anchor=tkinter.NW
        )
        self.west_images = [
            self.img_ps_w_wc_t,
            self.img_ps_w_p1,
            self.img_ps_w_p2,
            self.img_ps_w_p3,
            self.img_ps_w_c3,
            self.img_ps_w_c2,
            self.img_ps_w_c1,
            self.img_ps_w_wc_b
        ]
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

        for i, t_pts in enumerate(self.sorted_west):
            t, pts = t_pts
            self.canvas.create_image(
                self.pos_bank_west[0] + 10 + (0 if (i % 2 == 0) else self.w_ps + 10),
                self.pos_bank_west[1] + ((i // 2) * (self.h_ps + 10)) + 5,
                image=self.res_images[t],
                anchor=tkinter.NW
            )

        self.canvas.grid(row=0, column=0)
        self.canvas.tag_bind(self.img_ps_w_wc_t, "<B1-Motion>", lambda event, rect=self.img_ps_w_wc_t: self.motion_rect(event, rect))
        self.canvas.tag_bind(self.img_ps_w_p1, "<B1-Motion>", lambda event, rect=self.img_ps_w_p1: self.motion_rect(event, rect))
        self.canvas.tag_bind(self.img_ps_w_p2, "<B1-Motion>", lambda event, rect=self.img_ps_w_p2: self.motion_rect(event, rect))
        self.canvas.tag_bind(self.img_ps_w_p3, "<B1-Motion>", lambda event, rect=self.img_ps_w_p3: self.motion_rect(event, rect))
        self.canvas.tag_bind(self.img_ps_w_c3, "<B1-Motion>", lambda event, rect=self.img_ps_w_c3: self.motion_rect(event, rect))
        self.canvas.tag_bind(self.img_ps_w_c2, "<B1-Motion>", lambda event, rect=self.img_ps_w_c2: self.motion_rect(event, rect))
        self.canvas.tag_bind(self.img_ps_w_c1, "<B1-Motion>", lambda event, rect=self.img_ps_w_c1: self.motion_rect(event, rect))
        self.canvas.tag_bind(self.img_ps_w_wc_b, "<B1-Motion>", lambda event, rect=self.img_ps_w_wc_b: self.motion_rect(event, rect))


        self.canvas.tag_bind(self.img_ps_w_wc_t, "<ButtonRelease-1>", lambda event, rect=self.img_ps_w_wc_t: self.release_rect(event, rect))
        for img in self.west_images:
            self.canvas.itemconfigure(img, state="hidden")

    def motion_rect(self, event, rect):
        print(f"motion {rect=}, {event=}")
        ex, ey = event.x, event.y
        ex -= (self.w_ps / 2)
        ey -= (self.h_ps / 2)
        self.canvas.tag_raise(rect)
        self.canvas.coords(rect, ex, ey)

    def release_rect(self, event, rect):
        print(f"release_rect {rect=}, {event=}")


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
    df_sub = df[["Team", "PTS"]]
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
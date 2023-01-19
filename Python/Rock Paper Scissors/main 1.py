

import math
import random
import tkinter

from utility import distance
from colour_utility import *
from tkinter_utility import *


def rows_cols(v):
    return (math.ceil(math.sqrt(v)), math.ceil(v / (math.ceil(math.sqrt(v)) if math.ceil(math.sqrt(v)) != 0 else 1)))


class RPSSim(tkinter.Tk):

    def __init__(
            self,
            n_people,
            p_s: tuple[float, float, float]=(1/3, 1/3, 1/3)
    ):
        super().__init__()

        self.radius = 18
        self.WIDTH, self.HEIGHT = 900, (900 * (9/16))
        self.geometry(f"{int(self.WIDTH)}x{int(self.HEIGHT)}")
        self.title("Rock Paper Scissors Battle Royale")
        self.width_canvas = int(self.WIDTH * 0.875)
        self.height_canvas = int(self.HEIGHT * 0.875)
        self.team_data = {
            "rock": {
                "colour": rgb_to_hex(BROWN_2),
                "prey": "scissors",
                "predator": "paper"
            },
            "paper": {
                "colour": rgb_to_hex(BLUE),
                "prey": "rock",
                "predator": "scissors"
            },
            "scissors": {
                "colour": rgb_to_hex(GREEN_3),
                "prey": "paper",
                "predator": "rock"
            }
        }

        self.reset_value_reset_random_move_counter = 25
        self.tv_random_reset_random_move_counter = tkinter.IntVar(self, value=self.reset_value_reset_random_move_counter)
        self.n_people = n_people
        self.p_s = p_s
        self.frame_controls = tkinter.Frame(self, background="black")
        self.canvas_board = tkinter.Canvas(self.frame_controls, width=self.width_canvas, height=self.height_canvas, background=rgb_to_hex(GRAY_66))

        self.entities = {}
        self.clan_rock = tkinter.Variable(self, value=list())
        self.clan_paper = tkinter.Variable(self, value=list())
        self.clan_scissors = tkinter.Variable(self, value=list())

        self.highlighted_neighbours = tkinter.Variable(self, value=list())

        # # Strategy Combo
        # self.tv_label_combo_strategy,\
        # self.label_combo_strategy,\
        # self.tv_combo_strategy,\
        # self.combo_strategy=\
        #     combo_factory(
        #         self.frame_controls,
        #         tv_label="Strategy",
        #         tv_combo="Random",
        #         kwargs_combo={
        #             "values": ["Greedy", "Random"],
        #             "state": "readonly"
        #         }
        # )

        # Strategy Radio
        self.tv_radio_strategy,\
        self.tv_lst_radio_strategy,\
        self.btn_lst_radio_strategy=\
            radio_factory(
                self.frame_controls,
                buttons=["Greedy", "Random"],
                # default_value="Random"
                default_value="Greedy"
        )

        # animation specific

        self.n_rows, self.n_cols = rows_cols(self.n_people)
        for i in range(self.n_people):
            # r_i = i // self.n_rows
            # c_i = i - (r_i * self.n_cols)
            # # x1, y1, x2, y2 =\
            # #     l_off + (c_i * (self.radius + sp)),\
            # #     t_off + (r_i * (self.radius + sp)),\
            # #     l_off + ((c_i + 1) * (self.radius + sp)),\
            # #     t_off + ((r_i + 1) * (self.radius + sp))
            team = self.gen_random_team_member()
            colour = self.get_team_colour(team)
            x1, y1, x2, y2 = self.generate_random_start_pos(radius=self.radius)
            # xd, yd = self.random_non_stationary_speed()
            key = self.canvas_board.create_oval(x1, y1, x2, y2, fill=colour)
            # print(f"NEW KEY {key=}")
            self.entities[key] = {
                "x1_y1_x2_y2": (x1, y1, x2, y2),
                "x": x1 + ((x2 - x1) / 2),
                "y": y1 + ((y2 - y1) / 2),
                "team": team
            }
            xd, yd = self.greedy_non_stationary_speed(key)
            self.entities[key].update({
                "xd": xd,
                "yd": yd
            })
            if team == "rock":
                # print(f"A1 {self.clan_rock.get()=}")
                clan_rock = self.clan_rock.get()
                if isinstance(clan_rock, str):
                    clan_rock = []
                if not isinstance(clan_rock, list):
                    clan_rock = list(clan_rock)
                clan_rock.append(i)
                # print(f"A2 {clan_rock=}")
                self.clan_rock.set(clan_rock)
            elif team == "paper":
                # print(f"B {self.clan_paper.get()=}")
                clan_paper = self.clan_paper.get()
                if isinstance(clan_paper, str):
                    clan_paper = []
                if not isinstance(clan_paper, list):
                    clan_paper = list(clan_paper)
                clan_paper.append(i)
                # print(f"A2 {clan_paper=}")
                self.clan_paper.set(clan_paper)
            else:
                # print(f"C {self.clan_scissors.get()=}")
                clan_scissors = self.clan_scissors.get()
                if isinstance(clan_scissors, str):
                    clan_scissors = []
                if not isinstance(clan_scissors, list):
                    clan_scissors = list(clan_scissors)
                clan_scissors.append(i)
                # print(f"A2 {clan_scissors=}")
                self.clan_scissors.set(clan_scissors)

        self.frame_controls.pack()
        for btn in self.btn_lst_radio_strategy:
            btn.pack()
        self.canvas_board.pack()

        print(f"# Rocks {len(self.clan_rock.get())}")
        print(f"# Papers {len(self.clan_paper.get())}")
        print(f"# Scissors {len(self.clan_scissors.get())}")

        self.canvas_board.bind("<Button-1>", self.click_canvas_board)
        self.canvas_board.bind("<ButtonRelease-1>", self.release_canvas_board)
        self.canvas_board.bind("<B1-Motion>", self.motion_canvas_board)

        self.after(1, self.tick)

    def tick(self):
        # greedy
        # random
        # survival
        
        hr = self.radius / 2
        min_x = hr
        min_y = hr
        max_x = self.width_canvas - hr
        max_y = self.height_canvas - hr
        for i, key_val in enumerate(self.entities.items()):
            key, val = key_val
            x, y = val["x"], val["y"]
            xd, yd = val["xd"], val["yd"]
            x = clamp(min_x, x + xd, max_x)
            y = clamp(min_y, y + yd, max_y)
            if x == min_x:
                print(f"{key=} bounce off left wall")
                self.entities[key]["xd"] = -1 * val["xd"]
            if y == min_y:
                print(f"{key=} bounce off top wall")
                self.entities[key]["yd"] = -1 * val["yd"]
            if x == max_x:
                print(f"{key=} bounce off right wall")
                self.entities[key]["xd"] = -1 * val["xd"]
            if y == max_y:
                print(f"{key=} bounce off bottom wall")
                self.entities[key]["yd"] = -1 * val["yd"]
            self.entities[key]["x"] += xd
            self.entities[key]["y"] += yd
            self.canvas_board.moveto(key, self.entities[key]["x"] - hr, self.entities[key]["y"] - hr)

        self.reset_speeds()
        self.after(1, self.tick)

    def reset_speeds(self):
        # print(f"reset speeds")
        tvrrmc = self.tv_random_reset_random_move_counter.get()
        self.tv_random_reset_random_move_counter.set(tvrrmc - 1)
        mode = self.tv_radio_strategy.get()
        if mode not in ["Random", "Greedy"]:
            raise Exception(f"Error strategy not recognized. '{mode}'")

        if mode == "Random" and tvrrmc > 0:
            # do not reset these speeds until the counter reaches zero
            print(f"early exit")
            return

        for key, val in self.entities.items():
            d_x, d_y = val["xd"], val["yd"]
            if mode == "Random":
                d_x, d_y = self.random_non_stationary_speed()
            elif mode == "Greedy":
                d_x, d_y = self.greedy_non_stationary_speed(key)
            self.entities[key]["xd"] = d_x
            self.entities[key]["yd"] = d_y

        self.tv_random_reset_random_move_counter.set(self.reset_value_reset_random_move_counter)

    def click_canvas_board(self, event, neighbours_in=None):
        # print(f"click_canvas_board")
        x, y = event.x, event.y
        if neighbours_in is None:
            k_neighbours = self.k_nearest_neighbours(x, y, 5)
        else:
            k_neighbours = list(neighbours_in)
        self.highlighted_neighbours.set(k_neighbours)
        for neighbour in k_neighbours:
            self.canvas_board.itemconfig(neighbour, fill="black")
        # print(f"{k_neighbours=}")

    def release_canvas_board(self, event):
        k_neighbours = self.highlighted_neighbours.get()
        for neighbour in k_neighbours:
            team = self.entities[neighbour]["team"]
            self.canvas_board.itemconfig(neighbour, fill=self.get_team_colour(team))

    def motion_canvas_board(self, event):
        x, y = event.x, event.y
        k_neighbours_new = set(self.k_nearest_neighbours(x, y, 5))
        k_neighbours_curr = set(self.highlighted_neighbours.get())
        if k_neighbours_curr.difference(k_neighbours_new):
            # list don't match, motion changed k-nearest neighbours
            self.release_canvas_board(event)
            self.click_canvas_board(event, neighbours_in=k_neighbours_new)

    def gen_random_team_member(self):
        # print(f"\nXX {self.clan_rock.get()=}, {type(self.clan_rock.get())=}")
        # print(f"XX {self.clan_paper.get()=}, {type(self.clan_paper.get())=}")
        # print(f"XX {self.clan_scissors.get()=}, {type(self.clan_scissors.get())=}")
        cr = self.clan_rock.get()
        cp = self.clan_paper.get()
        cs = self.clan_scissors.get()
        if not cr:
            cr = []
        # else:
        #     cr = eval(cr)
        if not cp:
            cp = []
        # else:
        #     cp = eval(cp)
        if not cs:
            cs = []
        # else:
        #     cs = eval(cs)
        l_r, l_p, l_s = len(cr), len(cp), len(cs)
        tot = l_r + l_p + l_s
        if tot == 0:
            tot = 1
        if tot > self.n_people:
            raise Exception("Error too many people already")
        p_r, p_p, p_s = self.p_s
        a_r, a_p, a_s = l_r / tot, l_p / tot, l_s / tot
        d_r = p_r - a_r
        d_p = p_p - a_p
        d_s = p_s - a_s
        if max([d_r, d_p, d_s]) == d_r:
            # rocks has the greatest differential
            return "rock"
        elif max([d_r, d_p, d_s]) == d_p:
            # paper has the greatest differential
            return "paper"
        else:
            # scissors has the greatest differential
            return "scissors"

    def k_nearest_neighbours(self, x, y, k, max_radius=None):
        # print(f"{x=}, {y=}")
        if max_radius is None:
            max_radius = float("inf")
        lst = []
        for i, ent_k_v in enumerate(self.entities.items()):
            key, val = ent_k_v
            xy_e = val["x"], val["y"]
            d = distance((x, y), xy_e)
            if d <= max_radius:
                lst.append((key, d))
        # key, distance
        lst.sort(key=lambda tup: tup[1])
        return [i_d[0] for i, i_d in enumerate(lst)][:k]

    def get_team_colour(self, team_in):
        return self.team_data[team_in]["colour"]

    def get_team_prey(self, team_in):
        return self.team_data[team_in]["prey"]

    def get_team_predator(self, team_in):
        return self.team_data[team_in]["predator"]

    def random_non_stationary_speed(self):
        xd, yd = random.randint(-1, 1), random.randint(-1, 1)
        if xd == 0 and yd == 0:
            return self.random_non_stationary_speed()
        else:
            return xd, yd

    def greedy_non_stationary_speed(self, key_in):
        team = self.entities[key_in]["team"]
        prey = self.get_team_prey(team)
        predator = self.get_team_predator(team)
        m_x, m_y = self.entities[key_in]["x"], self.entities[key_in]["y"]
        dat = {
            "rock": {
                "keys": [],
                "xs": [],
                "ys": []
            },
            "paper": {
                "keys": [],
                "xs": [],
                "ys": []
            },
            "scissors": {
                "keys": [],
                "xs": [],
                "ys": []
            }
        }
        for key, val in self.entities.items():
            if key != key_in:
                v_team = val["team"]
                v_x, v_y = val["x"], val["y"]
                d = distance((m_x, m_y), (v_x, v_y))
                dat[v_team]["keys"].append(key)
                dat[v_team]["xs"].append(v_x)
                dat[v_team]["ys"].append(v_y)

        ldpxs = len(dat[prey]["xs"])
        ldpys = len(dat[prey]["xs"])
        ldrxs = len(dat[predator]["xs"])
        ldrys = len(dat[predator]["xs"])
        x_avg_prey = sum(dat[prey]["xs"]) / (ldpxs if ldpxs != 0 else 1)
        y_avg_prey = sum(dat[prey]["ys"]) / (ldpys if ldpys != 0 else 1)
        x_avg_predator = sum(dat[predator]["xs"]) / (ldrxs if ldrxs != 0 else 1)
        y_avg_predator = sum(dat[predator]["ys"]) / (ldrys if ldrys != 0 else 1)

        d_x = x_avg_prey - m_x
        d_y = y_avg_prey - m_y

        s_x = 1 if d_x >= 0 else -1
        s_y = 1 if d_y >= 0 else -1

        p_x = d_x / (d_y if d_y != 0 else 1)
        p_y = d_y / (d_x if d_x != 0 else 1)

        # Ensure that 1 vector component has magnitude 1
        if abs(p_x - 1) >= abs(p_y - 1):
            pp_x = 1 / p_x
        else:
            pp_x = 1 / p_y
        p_x *= pp_x * s_x
        p_y *= pp_x * s_y

        # print(f"{ldpxs=}, {x_avg_prey=}")
        # print(f"{ldpys=}, {y_avg_prey=}")
        # print(f"{ldrxs=}, {x_avg_predator=}")
        # print(f"{ldrys=}, {y_avg_predator=}")
        # print(f"{d_x=}, {d_y=}, {p_x=}, {p_y=}, {pp_x=}")

        return p_x, p_y

    def generate_random_start_pos(self, radius=None):
        if radius is None:
            return random.randint(0, self.width_canvas - self.radius), random.randint(0, self.width_canvas - self.radius)
        else:
            hr = radius / 2
            x, y = random.randint(hr, self.width_canvas - hr), random.randint(hr, self.height_canvas - hr)
            x -= hr
            y -= hr
            return tuple(map(int, (x, y, x + radius, y + radius)))

if __name__ == '__main__':

    RPSSim(250).mainloop()
import tkinter

from siege_challenge.form_map import FormMap
from siege_challenge.form_map_selection import FormMapSelection
from siege_challenge.form_operator import FormOperator
from siege_challenge.form_operator_selection import FormOperatorSelection
from siege_challenge.form_type_selection import FormTypeSelection
from siege_challenge.siege_enums import *
from siege_challenge.base_form import Form
from siege_challenge.siege_game import Game
from siege_challenge.siege_utility import siege_acronym
from tkinter_utility import *


class FormGame(tkinter.Tk):
    def __init__(self, maps_in):

        # choose game mode      # Ranked
        # choose map            # House
        # choose type mode      # Bomb
        # round #               # 1
        # choose play mode      # ATK
        # map location          # 2F Room1, 2F Room2
        # Operator              # Sledge

        super().__init__()

        self.geometry(calc_geometry_tl(0.45, 0.6, largest=1))

        self.game_modes = list(GameMode)
        self.known_types = list(TypeMode)
        self.known_plays = list(PlayMode)
        self.known_maps = maps_in

        self.frame_playing = tkinter.Frame(self, name="f_playing")
        self.frame_atk_def_history = tkinter.Frame(self, name="f_history")
        self.frame_score_board = tkinter.Frame(self, name="f_score")
        self.frame_time_board = tkinter.Frame(self, name="f_time")
        self.frame_game_mode = tkinter.Frame(self, name="f_game_mode")

        self.tv_lbl_play_label_map_sel, self.lbl_play_label_map_sel = label_factory(self.frame_playing, tv_label="Map:")
        self.tv_lbl_play_label_map_loc_sel, self.lbl_play_label_map_loc_sel = label_factory(self.frame_playing, tv_label="Map Loc:")
        self.tv_lbl_play_label_gam_mode, self.lbl_play_label_gam_mode = label_factory(self.frame_playing, tv_label="Game Mode:")
        self.tv_lbl_play_label_pla_mode, self.lbl_play_label_pla_mode = label_factory(self.frame_playing, tv_label="Play Mode:")
        self.tv_lbl_play_label_typ_mode, self.lbl_play_label_typ_mode = label_factory(self.frame_playing, tv_label="Type Mode:")
        self.tv_lbl_play_label_round, self.lbl_play_label_round = label_factory(self.frame_playing, tv_label="Round")

        self.tv_lbl_play_map_sel, self.lbl_play_map_sel = label_factory(self.frame_playing, tv_label="_")
        self.tv_lbl_play_map_loc_sel, self.lbl_play_map_loc_sel = label_factory(self.frame_playing, tv_label="_")
        self.tv_lbl_play_gam_mode, self.lbl_play_gam_mode = label_factory(self.frame_playing, tv_label="_")
        self.tv_lbl_play_pla_mode, self.lbl_play_pla_mode = label_factory(self.frame_playing, tv_label="_")
        self.tv_lbl_play_typ_mode, self.lbl_play_typ_mode = label_factory(self.frame_playing, tv_label="_")
        self.tv_lbl_play_round, self.lbl_play_round = label_factory(self.frame_playing, tv_label="1")

        self.tv_game_mode, self.list_tv_btns_game_mode, self.list_btns_game_mode = radio_factory(
            self.frame_game_mode,
            buttons=list(GameMode)
        )

        self.tl_form_map_selection = None
        self.tl_form_type_selection = None

        self.frame_type_mode = tkinter.Frame(self)
        self.tv_type_mode, self.list_tv_btns_type_mode, self.list_btns_type_mode = radio_factory(
            self.frame_type_mode,
            buttons=list(TypeMode)
        )

        self.frame_round_number = tkinter.Frame(self)
        self.tv_round_number, self.list_tv_btns_round_number, self.list_btns_round_number = radio_factory(
            self.frame_round_number,
            buttons=list(map(str, range(1, 9)))
        )

        self.frame_play_mode = tkinter.Frame(self)
        self.tv_play_mode, self.list_tv_btns_play_mode, self.list_btns_play_mode = radio_factory(
            self.frame_play_mode,
            buttons=list(PlayMode)
        )

        self.tl_form_map_location_selection = None

        self.tl_form_operator_selection = None

        self.tl_ask_start_game = None
        self.tl_ask_attack_first = None

        # self.init_history_board()
        self.init_score_board()
        self.init_time_board()

        r, c, rs, cs, ix, iy, x, y, s = grid_keys()
        self.grid_args = {
            # .
            "frame_game_mode": {r: 0, c: 0},
            "frame_playing": {r: 0, c: 0},

            "frame_atk_def_history": {r: 2, c: 0},
            "frame_score_board": {r: 3, c: 0},
            "frame_time_board": {r: 3, c: 1},

            # frame_playing

            "lbl_play_label_map_sel": {r: 0, c: 0},
            "lbl_play_map_sel": {r: 0, c: 1},
            "lbl_play_label_map_loc_sel": {r: 1, c: 0},
            "lbl_play_map_loc_sel": {r: 1, c: 1},
            "lbl_play_label_gam_mode": {r: 0, c: 6},
            "lbl_play_gam_mode": {r: 0, c: 7},
            "lbl_play_label_pla_mode": {r: 0, c: 4},
            "lbl_play_pla_mode": {r: 0, c: 5},
            "lbl_play_label_typ_mode": {r: 1, c: 6},
            "lbl_play_typ_mode": {r: 1, c: 7},
            "lbl_play_label_round": {r: 0, c: 2},
            "lbl_play_round": {r: 0, c: 3}
        }

        self.init_grid_args = {
            "frame_game_mode",
            "frame_score_board",
            "frame_time_board",
            "frame_atk_def_history",

            "lbl_play_label_map_sel",
            "lbl_play_map_sel",
            "lbl_play_label_map_loc_sel",
            "lbl_play_map_loc_sel",
            "lbl_play_label_gam_mode",
            "lbl_play_gam_mode",
            "lbl_play_label_pla_mode",
            "lbl_play_pla_mode",
            "lbl_play_label_typ_mode",
            "lbl_play_typ_mode",
            "lbl_play_label_round",
            "lbl_play_round",
            "frame_atk_def_history",
            "frame_score_board",
            "frame_time_board"
        }

        self.grid_init()
        self.grid_frame_game_mode_radios()

        self.tv_game_mode.trace_variable("w", self.update_game_mode_selection)

        # # self.lbl_atk_def.pack()
        # # for btn in self.list_btns_atk_def:
        # #     btn.pack()
        # self.lbl_num_floors.pack()
        # for btn in self.list_btns_num_floors:
        #     btn.pack()
        # self.frame_radios.pack()
        # # self.frame_atk_def.pack(side=tkinter.LEFT)
        # self.frame_num_floors.pack(side=tkinter.LEFT)
        # self.combo_lbl_country.pack()
        # self.combo_country.pack()
        # self.lbl_entry_map_name.pack()
        # self.entry_map_name.pack()
        # self.frame_ctl_btns.pack()
        # self.btn_cancel.pack(side=tkinter.LEFT)
        # self.btn_submit.pack(side=tkinter.LEFT)

    def grid_init(self):
        for k in self.init_grid_args:
            args = self.grid_args[k]
            eval(f"self.{k}.grid(**{args})")

    def grid_frame_game_mode_radios(self):
        for btn in self.list_btns_game_mode:
            btn.grid()

    def ask_start_game(self):
        self.tl_ask_start_game = tkinter.Toplevel(self)
        self.tl_ask_start_game.geometry(calc_geometry_tl(0.1, 0.08, largest=1))
        master = self.tl_ask_start_game

        def click_start():
            print("click start")
            self.close_tl_ask_start_game()

        def click_restart():
            print("click restart")
            self.close_tl_ask_start_game()

        def click_quit():
            print("click quit")
            self.close_tl_ask_start_game()

        tv_btn_start, btn_start = button_factory(master, tv_btn="Start Game?", command=click_start)
        tv_btn_restart, btn_restart = button_factory(master, tv_btn="Restart", command=click_restart)
        tv_btn_quit, btn_quit = button_factory(master, tv_btn="Quit", command=click_quit)

        btn_start.pack()
        btn_restart.pack()
        btn_quit.pack()

        self.tl_ask_start_game.protocol("WM_DELETE_WINDOW", self.close_tl_ask_start_game)
        self.tl_ask_start_game.grab_set()

    def close_tl_ask_start_game(self):
        self.tl_ask_start_game.destroy()

    def update_game_type_selection(self, *args):
        self.select_game_type_mode(self.known_types[self.tl_form_type_selection.tv_var_types.get()])
        self.tl_form_type_selection.destroy()

    def select_game_type_mode(self, type_mode: TypeMode):
        self.tv_lbl_play_typ_mode.set(siege_acronym(type_mode))

    def update_game_mode_selection(self, *args):
        # now open map selection
        # self.able_game_mode_radios(False)

        gm = self.game_modes[self.tv_game_mode.get()]
        if gm == GameMode.CASUAL:
            # what game type then?
            self.tl_form_type_selection = FormTypeSelection(self.close_form_type_selection)
            self.tl_form_type_selection.geometry(calc_geometry_tl(0.25, 0.05, largest=1))
            self.tl_form_type_selection.tv_var_types.trace_variable("w", self.update_game_type_selection)
            self.tl_form_type_selection.protocol("WM_DELETE_WINDOW", self.close_form_type_selection)
            self.tl_form_type_selection.grab_set()
            self.wait_window(self.tl_form_type_selection)
            pm = self.known_types[self.tl_form_type_selection.tv_var_types.get()]
            # pm = TypeMode.SECURE
        else:
            pm = TypeMode.BOMB

        self.tv_lbl_play_typ_mode.set(siege_acronym(pm))
        self.tv_lbl_play_gam_mode.set(siege_acronym(gm))

        self.show_map_selection()

    def close_form_type_selection(self):
        self.select_game_type_mode(self.known_types[self.tl_form_type_selection.tv_var_types.get()])
        self.tl_form_type_selection.destroy()

    def able_game_mode_radios(self, state):
        s = "normal" if state else "disabled"
        for btn in self.list_btns_game_mode:
            btn.configure(state=s)

    def select_map_click_form(self, *args):
        # btn, tv = self.tl_form_map_selection.list_btn_types[idx], self.tl_form_map_selection.list_tv_btn_types[idx]
        print(f"MAP SELECTED {self.tl_form_map_selection.tv_var_maps.get()=}")
        self.tv_lbl_play_map_sel.set(self.known_maps[self.tl_form_map_selection.tv_var_maps.get()])
        self.close_form_map_selection(args)

    def show_map_selection(self):
        self.tl_form_map_selection = FormMapSelection(self.known_maps, self.close_form_map_selection)
        self.tl_form_map_selection.geometry(calc_geometry_tl(0.25, 0.1, largest=1))

        self.tl_form_map_selection.tv_var_maps.trace_variable("w", self.select_map_click_form)
        # for i, btn_tv in enumerate(zip(self.tl_form_map_selection.list_btn_types, self.tl_form_map_selection.list_tv_btn_types)):
        #     btn, tv = btn_tv
        #     btn.pack()
        #     tv.trace_variable("w", lambda *args, i_=i: self.select_map_click_form(self, args, idx=i_))

        self.tl_form_map_selection.protocol("WM_DELETE_WINDOW", self.close_form_map_selection)
        self.tl_form_map_selection.grab_set()
        # self.tl_form_map_selection = FormMap(self.known_maps, self.close_form_map_selection)
        # self.tl_form_map_selection.protocol("WM_DELETE_WINDOW", self.close_form_map_selection)
        # self.tl_form_map_selection.grab_set()

    def close_form_map_selection(self, *args):
        self.tl_form_map_selection.destroy()
        self.frame_game_mode.grid_forget()

        self.frame_playing.grid()
        self.ask_attacking_first()
        self.ask_operator_bans()
        self.init_history_board()
        self.ask_start_game()

    def init_history_board(self):
        print(f"init_HB")
        game_mode = self.game_modes[self.tv_game_mode.get()]
        play_mode = self.known_plays[self.tv_type_mode.get()]
        atk_first = play_mode == PlayMode.ATTACK
        print(f"{game_mode=}, {play_mode=}, {atk_first=}")
        play_mod = list(map(siege_acronym, ([PlayMode.ATTACK, PlayMode.DEFENCE] if atk_first else [PlayMode.DEFENCE, PlayMode.ATTACK])))
        mod_idx = 0
        list_tv_lbls_top, list_lbls_top = [], []
        list_tv_lbls_bot, list_lbls_bot = [], []
        if game_mode == GameMode.RANKED:
            # 4 Rounds Minimum, Win by 2, Max of 9 rounds
            n_rounds = 9
            mod_flips = [False, False, True, False, False, True, True, True, True]
        else:
            # 3 Rounds Minimum, Max of 5 rounds
            n_rounds = 5
            mod_flips = [False, True, False, True, True]

        for i in range(n_rounds):
            print(f"MY LABEL {play_mod[mod_idx]}, {mod_idx=}")
            tv_lbl_top, lbl_top = label_factory(
                self.frame_atk_def_history,
                tv_label=play_mod[mod_idx]
            )
            tv_lbl_bot, lbl_bot = label_factory(
                self.frame_atk_def_history,
                tv_label=play_mod[(mod_idx + 1) % 2]
            )
            if mod_flips[i]:
                mod_idx += 1
                mod_idx %= 2
            list_tv_lbls_top.append(tv_lbl_top)
            list_lbls_top.append(lbl_top)
            list_tv_lbls_bot.append(tv_lbl_bot)
            list_lbls_bot.append(lbl_bot)
            lbl_top.grid(row=0, column=i)
            lbl_bot.grid(row=4, column=i)


    def init_score_board(self):
        pass

    def init_time_board(self):
        pass

    # def valid_input(self):
    #     return True
        # name = self.tv_entry_map_name.get()
        # country = self.tv_combo_country.get()
        # num_floors = self.tv_var_num_floors.get()
        # num_floors_s = self.options_num_floors[num_floors]
        # # print(f"{name=}, {country=}, {atk_def=}")
        # if not country:
        #     self.flash_lbl(self.combo_lbl_country)
        #     self.combo_country.focus_set()
        # elif not name:
        #     self.flash_lbl(self.lbl_entry_map_name)
        #     self.entry_map_name.focus_set()
        #
        # inputs_valid = name and country
        # valid_map = not self.known_countries
        #
        # if inputs_valid:
        #     map_ = Map(name, country, num_floors)
        #     print(f"{map_}\n{self.known_countries=}")
        #     if map_ in self.known_countries:
        #         tkinter.messagebox.showerror("New Map", "Error a map with this name, country, number of floors, has already been created. Please edit your selection.")
        #         self.flash_lbl(self.lbl_entry_map_name)
        #         self.entry_map_name.focus_set()
        #     else:
        #         valid_map = True
        #
        # return inputs_valid and valid_map
    def ask_attacking_first(self):
        self.tl_ask_attack_first = tkinter.Toplevel(self)
        self.tl_ask_attack_first.geometry(calc_geometry_tl(0.1, 0.08, largest=1))

        def click_a():
            pm = PlayMode.ATTACK
            self.tv_type_mode.set(self.known_plays.index(pm))
            self.close_tl_ask_attack_first()
            self.tv_lbl_play_pla_mode.set(siege_acronym(pm))

        def click_b():
            pm = PlayMode.DEFENCE
            self.tv_type_mode.set(self.known_plays.index(pm))
            self.close_tl_ask_attack_first()
            self.tv_lbl_play_pla_mode.set(siege_acronym(pm))

        tv_lbl, lbl = label_factory(self.tl_ask_attack_first, tv_label="Attacking First Round?")
        tv_btn_a, btn_a = button_factory(self.tl_ask_attack_first, tv_btn=siege_acronym(PlayMode.ATTACK), command=click_a)
        tv_btn_b, btn_b = button_factory(self.tl_ask_attack_first, tv_btn=siege_acronym(PlayMode.DEFENCE), command=click_b)

        lbl.pack()
        btn_a.pack()
        btn_b.pack()

        self.tl_ask_attack_first.protocol("WM_DELETE_WINDOW", self.close_tl_ask_attack_first)
        self.tl_ask_attack_first.grab_set()
        self.wait_window(self.tl_ask_attack_first)

    def close_tl_ask_attack_first(self):
        self.tl_ask_attack_first.destroy()

    def ask_operator_bans(self):
        self.tl_ask_operator_bans = tkinter.Toplevel(self)
        f_ban_labels = tkinter.Frame(self.tl_ask_operator_bans)
        tv_lbl_q, lbl_q = label_factory(self.tl_ask_operator_bans, tv_label="")
        ban_labels = [
            label_factory(f_ban_labels) for _ in range(4)
        ]

        list_a = self.attackers_list()
        list_d = self.defenders_list()

        a = siege_acronym(PlayMode.ATTACK)
        d = siege_acronym(PlayMode.DEFENCE)
        order = [(f"1st {a}", list_a), (f"2nd {a}", list_a), (f"1st {d}", list_d), (f"2nd {d}", list_d)]

        f_lst_a = tkinter.Frame(self.tl_ask_operator_bans)
        

        def init_lst_a():



        for i, lbl_ord in enumerate(zip(ban_labels, order)):
            lbl_, ord_ = lbl_ord
            tv_lbl, lbl = lbl_
            o_lbl, o_lst = ord_
            tv_lbl_q.set(o_lbl)


        # atk_first = siege_acronym(self.tv_lbl_play_pla_mode.get()) == PlayMode.ATTACK
        #
        # if atk_first:
        #     order = [PlayMode.ATTACK]

        self.tl_ask_operator_bans.protocol("WM_DELETE_WINDOW", self.close_tl_ask_operator_bans)
        self.tl_ask_operator_bans.grab_set()
        self.wait_window(self.tl_ask_operator_bans)

        def close_form_op_selection():

        # ban 2 attackers then 2 defenders
        for i in range(4):
            ko = self.attackers_list() if i < 2 else self.defenders_list()
            self.tl_form_operator_selection = FormOperatorSelection(ko, close_form_op_selection)
            self.tl_ask_operator_bans.protocol("WM_DELETE_WINDOW", self.close_tl_ask_operator_bans)
            self.tl_ask_operator_bans.grab_set()
            self.wait_window(self.tl_ask_operator_bans)

    def attackers_list(self):
        return []

    def defenders_list(self):
        return []

    # def toggle_factory(self, master, buttons, def, tv_label=None, kwargs_lbl=None, kwargs_btn=None):
    #     tkinter.Tog
    #     if hasattr(buttons, '__iter__') and buttons:
    #         if not (isinstance(buttons, list) and isinstance(buttons, tuple)):
    #             buttons = list(buttons)
    #         if default_value is not None:
    #             # print(f"not None")
    #             if isinstance(default_value, tkinter.IntVar):
    #                 # print(f"is_var")
    #                 var = default_value
    #             elif isnumber(default_value):
    #                 # print(f"not var")
    #                 var = tkinter.IntVar(master, value=int(default_value))
    #             else:
    #                 raise ValueError(f"Error default value '{default_value}' is not a number.")
    #         else:
    #             print(f"is None")
    #             var = tkinter.IntVar(master, value=-1)
    #
    #         if 0 > var.get() >= len(buttons):
    #             raise IndexError("Error var index is out of range")
    #
    #         # print(f"CREATED {var.get()=}")
    #
    #         r_buttons = []
    #         tv_vars = []
    #         for i, btn in enumerate(buttons):
    #             # print(f"{i=}, {btn=}, name=rbtn_{str(btn).lower()}, {master=}, {master.winfo_parent()=}, {type(master)=}")
    #             if is_tk_var(btn):
    #                 tv_var = btn
    #             else:
    #                 tv_var = tkinter.StringVar(master, value=btn)
    #             tv_vars.append(tv_var)
    #             if kwargs_buttons is not None:
    #                 print(f"WARNING kwargs param is applied to each radio button")
    #                 r_buttons.append(
    #                     tkinter.Radiobutton(master, variable=var, textvariable=tv_var, **kwargs_buttons, value=i,
    #                                         name=f"rbtn_{btn.replace('.', '_')}"))
    #             else:
    #                 r_buttons.append(
    #                     tkinter.Radiobutton(master, variable=var, textvariable=tv_var, value=i,
    #                                         name=f"rbtn_{str(btn).lower().replace('.', '_')}")
    #                 )
    #
    #         # print(f"OUT {var.get()=}")
    #         return var, tv_vars, r_buttons
    #     else:
    #         raise Exception("Error, must pass a list of buttons.")
    #
    #         # tv_sort_direction = StringVar(WIN, value="descending")
    #         # tv_sort_dir_a = StringVar(WIN, value="ascending")
    #         # tv_sort_dir_d = StringVar(WIN, value="descending")
    #         # rb_sda = Radiobutton(frame_rb_group_3, variable=tv_sort_direction, value="ascending", textvariable=tv_sort_dir_a)
    #         # rb_sdd = Radiobutton(frame_rb_group_3, variable=tv_sort_direction, value="descending", textvariable=tv_sort_dir_d)


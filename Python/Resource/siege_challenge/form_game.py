import tkinter
from tkinter import messagebox

from siege_challenge.form_map import FormMap
from siege_challenge.siege_enums import *
from siege_challenge.base_form import Form
from siege_challenge.siege_game import Game
from siege_challenge.siege_utility import siege_acronym
from tkinter_utility import radio_factory, combo_factory, entry_factory, button_factory, label_factory


class FormGame(tkinter.Tk):
    def __init__(self, maps_in):
        super().__init__()

        # choose game mode      # Ranked
        # choose map            # House
        # choose type mode      # Bomb
        # round #               # 1
        # choose play mode      # ATK
        # map location          # 2F Room1, 2F Room2
        # Operator              # Sledge

        self.known_maps = maps_in

        self.frame_playing = tkinter.Frame(self)

        self.tv_lbl_play_map_sel, self.lbl_play_map_sel = label_factory(self.frame_playing, tv_label="Map")
        self.tv_lbl_play_map_loc_sel, self.lbl_play_map_loc_sel = label_factory(self.frame_playing, tv_label="Map Loc")
        self.tv_lbl_play_gam_mod, self.lbl_play_gam_mod = label_factory(self.frame_playing, tv_label="Game Mode")
        self.tv_lbl_play_pla_mod, self.lbl_play_pla_mod = label_factory(self.frame_playing, tv_label="Play Mode")
        self.tv_lbl_play_typ_mod, self.lbl_play_typ_mod = label_factory(self.frame_playing, tv_label="Type Mode")
        self.tv_lbl_play_round, self.lbl_play_round = label_factory(self.frame_playing, tv_label="Round")
        self.frame_atk_def_history = tkinter.Frame(self, name="f_history")
        self.frame_score_board = tkinter.Frame(self, name="f_score")
        self.frame_time_board = tkinter.Frame(self, name="f_time")

        self.frame_game_mode = tkinter.Frame(self, name="f_game_mode")

        self.tv_game_mode, self.list_tv_btns_game_mode, self.list_btns_game_mode = radio_factory(
            self.frame_game_mode,
            buttons=list(GameMode)
        )

        self.tl_form_map_selection = None

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

        self.init_history_board()
        self.init_score_board()
        self.init_time_board()

        self.frame_game_mode.grid()
        for btn in self.list_btns_game_mode:
            btn.grid()

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

    def update_game_mode_selection(self, *args):
        # now open map selection
        self.show_map_selection()

    def show_map_selection(self):
        self.tl_form_map_selection = FormMap(self.known_maps, self.close_form_map_selection)
        self.tl_form_map_selection.protocol("WM_DELETE_WINDOW", self.close_form_map_selection)
        self.tl_form_map_selection.grab_set()

    def close_form_map_selection(self, *args):
        self.tl_form_map_selection.destroy()

    def init_history_board(self):
        game_mode = self.tv_game_mode.get()
        play_mode = self.tv_type_mode.get()
        atk_first = play_mode == PlayMode.ATTACK
        play_mod = list(map(siege_acronym, ([PlayMode.ATTACK, PlayMode.DEFENCE] if atk_first else [PlayMode.DEFENCE, PlayMode.ATTACK])))
        mod_idx = 0
        list_tv_lbls_top, list_lbls_top = [], []
        list_tv_lbls_bot, list_lbls_bot = [], []
        if game_mode == GameMode.RANKED:
            # 4 Rounds Minimum, Win by 2, Max of 9 rounds
            n_rounds = 9
            mod_flips = [False, False, False, True, True, True, True, True, True]
        else:
            # 3 Rounds Minimum, Max of 5 rounds
            n_rounds = 5
            mod_flips = [False, False, True, True, True]

        for i in range(n_rounds):
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

    def valid_input(self):
        return True
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

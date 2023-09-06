import tkinter
from tkinter import messagebox

from siege_challenge.base_form import Form
from siege_challenge.siege_game import Game
from tkinter_utility import radio_factory, combo_factory, entry_factory, button_factory


class FormGame(Form):
    def __init__(self, maps_in, callback):
        super().__init__(callback)

        self.known_maps = maps_in
        self.known_countries = list(set([m.country for m in self.known_maps]))

        self.frame_radios = tkinter.Frame(self)
        # self.frame_atk_def = tkinter.Frame(self.frame_radios)
        self.frame_num_floors = tkinter.Frame(self.frame_radios)

        self.tv_lbl_num_floors = tkinter.StringVar(self, value="Num Floors:")
        self.lbl_num_floors = tkinter.Label(self.frame_num_floors, textvariable=self.tv_lbl_num_floors)
        self.options_num_floors = [1, 2, 3, 4]
        self.tv_var_num_floors,\
            self.list_tv_vars_num_floors,\
            self.list_btns_num_floors = \
            radio_factory(
                self.frame_num_floors,
                buttons=self.options_num_floors
            )

        self.tv_combo_lbl_country,\
            self.combo_lbl_country,\
            self.tv_combo_country,\
            self.combo_country = \
            combo_factory(
                self,
                tv_label="Country:",
                kwargs_combo={
                    "justify": tkinter.CENTER
                }
            )
        self.combo_country["values"] = self.known_countries

        self.tv_lbl_entry_map_name,\
            self.lbl_entry_map_name,\
            self.tv_entry_map_name,\
            self.entry_map_name = \
            entry_factory(
                self,
                tv_label="Map Name:",
                kwargs_entry={
                    "justify": tkinter.CENTER
                }
            )

        self.frame_ctl_btns = tkinter.Frame(self)
        self.tv_btn_cancel,\
            self.btn_cancel =\
            button_factory(
                self.frame_ctl_btns,
                tv_btn="cancel",
                command=self.click_cancel
            )

        self.tv_btn_submit,\
            self.btn_submit =\
            button_factory(
                self.frame_ctl_btns,
                tv_btn="submit",
                command=self.click_submit
            )

        self.btn_cancel.bind("<Return>", self.return_cancel)
        self.btn_submit.bind("<Return>", self.return_submit)

        # self.lbl_atk_def.pack()
        # for btn in self.list_btns_atk_def:
        #     btn.pack()
        self.lbl_num_floors.pack()
        for btn in self.list_btns_num_floors:
            btn.pack()
        self.frame_radios.pack()
        # self.frame_atk_def.pack(side=tkinter.LEFT)
        self.frame_num_floors.pack(side=tkinter.LEFT)
        self.combo_lbl_country.pack()
        self.combo_country.pack()
        self.lbl_entry_map_name.pack()
        self.entry_map_name.pack()
        self.frame_ctl_btns.pack()
        self.btn_cancel.pack(side=tkinter.LEFT)
        self.btn_submit.pack(side=tkinter.LEFT)

    def valid_input(self):
        name = self.tv_entry_map_name.get()
        country = self.tv_combo_country.get()
        num_floors = self.tv_var_num_floors.get()
        num_floors_s = self.options_num_floors[num_floors]
        # print(f"{name=}, {country=}, {atk_def=}")
        if not country:
            self.flash_lbl(self.combo_lbl_country)
            self.combo_country.focus_set()
        elif not name:
            self.flash_lbl(self.lbl_entry_map_name)
            self.entry_map_name.focus_set()

        inputs_valid = name and country
        valid_map = not self.known_countries

        if inputs_valid:
            map_ = Map(name, country, num_floors)
            print(f"{map_}\n{self.known_countries=}")
            if map_ in self.known_countries:
                tkinter.messagebox.showerror("New Map", "Error a map with this name, country, number of floors, has already been created. Please edit your selection.")
                self.flash_lbl(self.lbl_entry_map_name)
                self.entry_map_name.focus_set()
            else:
                valid_map = True

        return inputs_valid and valid_map

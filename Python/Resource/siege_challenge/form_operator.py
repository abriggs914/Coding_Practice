import tkinter
from tkinter import messagebox

from siege_challenge.base_form import Form
from siege_challenge.siege_operator import Operator
from tkinter_utility import radio_factory, combo_factory, entry_factory


class FormOperator(Form):
    def __init__(self, operators_in, callback):
        super().__init__(callback)

        self.known_operators = operators_in
        self.known_ctus = list(set([op.ctu for op in self.known_operators]))

        self.frame_radios = tkinter.Frame(self)
        self.frame_atk_def = tkinter.Frame(self.frame_radios)
        self.frame_sex = tkinter.Frame(self.frame_radios)

        self.tv_lbl_atk_def = tkinter.StringVar(self, value="Atk / Def")
        self.lbl_atk_def = tkinter.Label(self.frame_atk_def, textvariable=self.tv_lbl_atk_def)
        self.options_atk_def = ["Attacker", "Defender"]
        self.tv_var_atk_def,\
            self.list_tv_vars_atk_def,\
            self.list_btns_atk_def = \
            radio_factory(
                self.frame_atk_def,
                buttons=self.options_atk_def
            )

        self.tv_lbl_sex = tkinter.StringVar(self, value="Sex:")
        self.lbl_sex = tkinter.Label(self.frame_sex, textvariable=self.tv_lbl_sex)
        self.options_sex = ["Male", "Female"]
        self.tv_var_sex,\
            self.list_tv_vars_sex,\
            self.list_btns_sex = \
            radio_factory(
                self.frame_sex,
                buttons=self.options_sex
            )

        self.tv_combo_lbl_ctu,\
            self.combo_lbl_ctu,\
            self.tv_combo_ctu,\
            self.combo_ctu = \
            combo_factory(
                self,
                tv_label="CTU:",
                kwargs_combo={
                    "justify": tkinter.CENTER
                }
            )
        self.combo_ctu["values"] = self.known_ctus

        self.tv_lbl_entry_op_name,\
            self.lbl_entry_op_name,\
            self.tv_entry_op_name,\
            self.entry_op_name = \
            entry_factory(
                self,
                tv_label="Operator Name:",
                kwargs_entry={
                    "justify": tkinter.CENTER
                }
            )

        self.lbl_atk_def.pack()
        for btn in self.list_btns_atk_def:
            btn.pack()
        self.lbl_sex.pack()
        for btn in self.list_btns_sex:
            btn.pack()
        self.frame_radios.pack()
        self.frame_atk_def.pack(side=tkinter.LEFT)
        self.frame_sex.pack(side=tkinter.LEFT)
        self.combo_lbl_ctu.pack()
        self.combo_ctu.pack()
        self.lbl_entry_op_name.pack()
        self.entry_op_name.pack()
        self.frame_ctl_btns.pack()
        self.btn_cancel.pack(side=tkinter.LEFT)
        self.btn_submit.pack(side=tkinter.LEFT)

    def valid_input(self):
        name = self.tv_entry_op_name.get()
        ctu = self.tv_combo_ctu.get()
        atk_def = self.tv_var_atk_def.get()
        atk_def_s = self.options_atk_def[atk_def].lower()
        sex = self.tv_var_sex.get()
        sex_s = self.options_sex[sex]
        # print(f"{name=}, {country=}, {atk_def=}")
        if atk_def < 0:
            self.flash_lbl(self.lbl_atk_def)
            self.list_btns_atk_def[0].focus_set()
        elif not ctu:
            self.flash_lbl(self.combo_lbl_ctu)
            self.combo_ctu.focus_set()
        elif not name:
            self.flash_lbl(self.lbl_entry_op_name)
            self.entry_op_name.focus_set()

        inputs_valid = name and ctu and atk_def > -1
        valid_op = not self.known_operators

        if inputs_valid:
            op = Operator(name, ctu, atk_def_s, sex)
            print(f"{op}\n{self.known_operators=}")
            if op in self.known_operators:
                tkinter.messagebox.showerror("New Op", "Error an operator with this name, country, and side, has already been created. Please edit your selection.")
                self.flash_lbl(self.lbl_entry_op_name)
                self.entry_op_name.focus_set()
            else:
                valid_op = True

        return inputs_valid and valid_op

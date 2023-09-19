from tkinter_utility import *
from siege_challenge.base_form import Form
from siege_challenge.siege_enums import *


class FormTypeSelection(Form):

    def __init__(self, callback):
        super().__init__(callback)

        self.known_types = list(TypeMode)
        self.frame_radios = tkinter.Frame(self)
        self.tv_var_types, self.list_tv_btn_types, self.list_btn_types = radio_factory(
            self.frame_radios,
            buttons=self.known_types
        )

        self.frame_radios.pack()
        for btn in self.list_btn_types:
            btn.grid()

    def valid_input(self):
        return bool(self.tv_var_types.get())


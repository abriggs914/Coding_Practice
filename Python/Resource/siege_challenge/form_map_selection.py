from tkinter_utility import *
from siege_challenge.base_form import Form


class FormMapSelection(Form):

    def __init__(self, known_maps, callback):
        super().__init__(callback)

        self.known_maps = known_maps
        self.frame_radios = tkinter.Frame(self)
        self.tv_var_maps, self.list_tv_btn_maps, self.list_btn_maps = radio_factory(
            self.frame_radios,
            buttons=self.known_maps
        )

        self.frame_radios.pack()
        for btn in self.list_btn_maps:
            btn.grid()

    def valid_input(self):
        return bool(self.tv_var_maps.get())


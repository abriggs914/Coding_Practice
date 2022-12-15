import tkinter

from tkinter_utility import *


# ttk.Scale(master, command, cursor, length, orient, state, to, from_,class_,style, takefocus, variable, value)


class BooleanSwitch(ttk.Scale):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class SettingsPopUp(tkinter.Toplevel):
    def __init__(self, game):
        super().__init__()
        self.game = game

        self.frame_controls = tkinter.Frame(self)
        self.tv_label_title, self.label_title = label_factory(self.frame_controls, tv_label="Game Settings")

        # 2D or 3D
        # boolean switch

        # use mouse to control direction
        # boolean switch

        # draw player line of sight
        # boolean switch

        # draw textured walls
        # boolean switch

        # npc uses bfs
        # boolean switch

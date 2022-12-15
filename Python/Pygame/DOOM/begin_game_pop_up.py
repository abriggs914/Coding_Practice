import tkinter

from tkinter_utility import *


# ttk.Scale(master, command, cursor, length, orient, state, to, from_,class_,style, takefocus, variable, value)


class OnOffToggle(tkinter.Frame):
    def __init__(self, master, is_on: bool = True, label_on_text="The Switch is On!", label_off_text="The Switch is Off!",
                 button_foreground_on="green", button_foreground_off="grey", show_label=True):
        super().__init__()

        # Keep track of the button state on/off
        # global is_on
        self.master = master
        self.is_on = tkinter.BooleanVar(self.master, value=is_on)
        self.label_on_text = label_on_text
        self.label_off_text = label_off_text
        self.tv_label = tkinter.StringVar(self.master, value=label_on_text if is_on else label_off_text)
        self.button_foreground_on = button_foreground_on
        self.button_foreground_off = button_foreground_off
        self.show_label = show_label

        # Create Label
        self.my_label = tkinter.Label(self.master,
                              textvariable=self.tv_label,
                              fg=self.button_foreground_on,
                              font=("Helvetica", 32))

        if self.show_label:
            self.my_label.grid()

        # Define Our Images
        self.on = tkinter.PhotoImage(master=self.master, file="resources/tkinter/on.png")
        self.off = tkinter.PhotoImage(master=self.master, file="resources/tkinter/off.png")

        # Create A Button
        self.button = tkinter.Button(self.master, image=(self.on if self.is_on.get() else self.off), bd=0,
                             command=self.switch)
        # self.button.grid()

        # self.configure(background=random_colour(rgb=False))

        # Define our switch function

    def switch(self):
        # Determine is on or off
        if self.is_on.get():
            self.button.config(image=self.off)
            self.tv_label.set(self.label_off_text)
            self.my_label.config(fg=self.button_foreground_off)
            self.is_on.set(False)
        else:
            self.button.config(image=self.on)
            self.tv_label.set(self.label_on_text)
            self.my_label.config(fg=self.button_foreground_on)
            self.is_on.set(True)

#
# class BooleanSwitch(ttk.Scale):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)

#
# class SettingsPopUp(tkinter.Toplevel):
class SettingsPopUp(tkinter.Tk):
    def __init__(self, game):
        super().__init__()

        self.geometry("690x500")
        self.game = game

        self.configure(background=random_colour(rgb=False))

        self.frame_controls = tkinter.Frame(self)
        self.tv_label_title, self.label_title = label_factory(self.frame_controls, tv_label="Game Settings")

        # 2D or 3D
        self.tv_label_2d_or_3d, self.label_2d_or_3d = label_factory(self.frame_controls, tv_label="Render 3D (default 2D)")
        # boolean switch
        self.toggle_2d_or_3d = OnOffToggle(self.frame_controls, show_label=False)

        # use mouse to control direction
        self.tv_label_mouse_control, self.label_mouse_control = label_factory(self.frame_controls, tv_label="Control Direction with Mouse:")
        # boolean switch
        self.toggle_mouse_control = OnOffToggle(self.frame_controls, show_label=False)

        # draw player line of sight
        self.tv_label_plos, self.label_plos = label_factory(self.frame_controls, tv_label="Draw Player Line of Sight:")
        # boolean switch
        self.toggle_player_line_of_sight = OnOffToggle(self.frame_controls, show_label=False)

        # draw textured walls
        self.tv_label_textured_walls, self.label_textured_walls = label_factory(self.frame_controls, tv_label="Texture Walls:")
        # boolean switch
        self.toggle_textured_walls = OnOffToggle(self.frame_controls, show_label=False)

        # npc uses bfs
        self.tv_label_npc_bfs, self.label_npc_bfs = label_factory(self.frame_controls, tv_label="NPC uses BFS (default is Euclidean)")
        # boolean switch
        self.toggle_npc_path = OnOffToggle(self.frame_controls, show_label=False)

        self.frame_controls.grid()
        self.label_title.grid(row=0, column=0, rowspan=1, columnspan=2)

        for j, label_toggle in enumerate(
                zip(
                    [self.label_2d_or_3d, self.label_mouse_control, self.label_plos, self.label_textured_walls, self.label_npc_bfs],
                    [self.toggle_2d_or_3d, self.toggle_mouse_control, self.toggle_player_line_of_sight, self.toggle_textured_walls, self.toggle_npc_path]
                )):
            label, toggle = label_toggle
            label.grid(row=j + 1, column=0, rowspan=1, columnspan=1)
            toggle.button.grid(row=j + 1, column=1, rowspan=1, columnspan=1)



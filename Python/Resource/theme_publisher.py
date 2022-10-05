import os
import json
from colour_utility import *
from tkinter_utility import *


#######################################################################################################################
#######################################################################################################################
#######################################################################################################################

VERSION = \
    """	
        GUI for gui theme design
        Version.............1.60
        Date..........2022-09-27
        Author......Avery Briggs
    """


def VERSION_NUMBER():
    return float(VERSION.split("\n")[2].split(".")[-2] + "." + VERSION.split("\n")[2].split(".")[-1])


def VERSION_DATE():
    return VERSION.split("\n")[3].split(".")[-1]


def VERSION_AUTHOR():
    return VERSION.split("\n")[4].split(".")[-1]

#######################################################################################################################
#######################################################################################################################
#######################################################################################################################


class FontChooser(tkinter.Frame):

    def __init__(self, master):
        super().__init__(master)

        self.status = tkinter.Variable(self)

        self.fonts_list = list(tkinter.font.families())
        self.fonts_list.sort()
        self.font_sizes_list = list(map(str, [6, 8, 10, 12, 14, 16, 18, 20]))
        self.font_weights_list = ["normal", "bold", "italic", "roman"]
        # combo for font choice
        # spinner for font size
        # spinner for font weight
        self.tv_label_font_name, \
        self.label_font_name, \
        self.tv_combo_font_name, \
        self.combo_font_name, \
            = combo_factory(
            self,
            tv_label="Font Name:",
            kwargs_combo={
                "values": self.fonts_list
            }
        )

        self.tv_label_font_size = tkinter.StringVar(self, value="Font Size:")
        self.label_font_size = tkinter.Label(self, textvariable=self.tv_label_font_size)
        self.tv_font_size = tkinter.IntVar(self, value=12)
        self.spin_font_size = tkinter.Spinbox(self, values=self.font_sizes_list, textvariable=self.tv_font_size)

        self.tv_label_font_weight = tkinter.StringVar(self, value="Font Weight:")
        self.label_font_weight = tkinter.Label(self, textvariable=self.tv_label_font_weight)
        self.tv_font_weight = tkinter.StringVar(self)
        self.spin_font_weight = tkinter.Spinbox(self, values=self.font_weights_list, textvariable=self.tv_font_weight)

        self.tv_combo_font_name.trace_variable("w", self.update_name)
        self.tv_font_size.trace_variable("w", self.update_size)
        self.tv_font_weight.trace_variable("w", self.update_weight)

        self.label_font_name.grid(row=0, column=0)
        self.combo_font_name.grid(row=0, column=1)
        self.label_font_size.grid(row=1, column=0)
        self.spin_font_size.grid(row=1, column=1)
        self.label_font_weight.grid(row=2, column=0)
        self.spin_font_weight.grid(row=2, column=1)

    def update_name(self, *args):
        self.update_status()

    def update_size(self, *args):
        self.update_status()

    def update_weight(self, *args):
        self.update_status()

    def update_status(self):
        status = {
            "name": self.tv_combo_font_name.get(),
            "weight": self.tv_font_weight.get(),
            "size": self.tv_font_size.get()
        }
        self.status.set(status)


class Theme:

    def __init__(self):
        self.name = tkinter.StringVar()
        self.tv_text_box_object_back_colour = tkinter.StringVar()
        self.tv_text_box_object_border_colour = tkinter.StringVar()
        self.tv_text_box_text_font = tkinter.StringVar()
        self.tv_text_box_text_fore_colour = tkinter.StringVar()

        self.tv_label_object_back_colour = tkinter.StringVar()
        self.tv_label_object_border_colour = tkinter.StringVar()
        self.tv_label_text_font_name = tkinter.StringVar()
        self.tv_label_text_fore_colour = tkinter.StringVar()

        self.tv_list_box_object_back_colour = tkinter.StringVar()
        self.tv_list_box_object_border_colour = tkinter.StringVar()
        self.tv_list_box_text_font_name = tkinter.StringVar()
        self.tv_list_box_text_fore_colour = tkinter.StringVar()

        self.tv_combo_box_object_back_colour = tkinter.StringVar()
        self.tv_combo_box_object_border_colour = tkinter.StringVar()
        self.tv_combo_box_text_font_name = tkinter.StringVar()
        self.tv_combo_box_text_fore_colour = tkinter.StringVar()

        # self.tv_option_button_object_back_colour = tkinter.StringVar()
        self.tv_option_button_object_border_colour = tkinter.StringVar()
        # self.tv_option_button_text_font_name = tkinter.StringVar()
        # self.tv_option_button_text_fore_colour = tkinter.StringVar()

        self.tv_box_object_back_colour = tkinter.StringVar()
        self.tv_box_object_border_colour = tkinter.StringVar()

        self.tv_button_object_back_colour = tkinter.StringVar()
        self.tv_button_object_border_colour = tkinter.StringVar()
        self.tv_button_object_hover_colour = tkinter.StringVar()
        self.tv_button_text_fore_colour = tkinter.StringVar()
        self.tv_button_text_hover_colour = tkinter.StringVar()
        self.tv_button_text_font_name = tkinter.StringVar()

    def parse(self, data):
        theme = Theme()
        theme.name.set(data.get("Name", ""))
        theme.tv_text_box_object_back_colour.set(data.get("TextBox", {}).get("object", {}).get("Back Colour", {}))
        # theme.tv_text_box_object_border_colour = tkinter.StringVar()
        # theme.tv_text_box_text_font = tkinter.StringVar()
        # theme.tv_text_box_text_fore_colour = tkinter.StringVar()
        #
        # theme.tv_label_object_back_colour = tkinter.StringVar()
        # theme.tv_label_object_border_colour = tkinter.StringVar()
        # theme.tv_label_text_font_name = tkinter.StringVar()
        # theme.tv_label_text_fore_colour = tkinter.StringVar()
        #
        # theme.tv_list_box_object_back_colour = tkinter.StringVar()
        # theme.tv_list_box_object_border_colour = tkinter.StringVar()
        # theme.tv_list_box_text_font_name = tkinter.StringVar()
        # theme.tv_list_box_text_fore_colour = tkinter.StringVar()
        #
        # theme.tv_combo_box_object_back_colour = tkinter.StringVar()
        # theme.tv_combo_box_object_border_colour = tkinter.StringVar()
        # theme.tv_combo_box_text_font_name = tkinter.StringVar()
        # theme.tv_combo_box_text_fore_colour = tkinter.StringVar()
        #
        # # self.tv_option_button_object_back_colour = tkinter.StringVar()
        # theme.tv_option_button_object_border_colour = tkinter.StringVar()
        # # self.tv_option_button_text_font_name = tkinter.StringVar()
        # # self.tv_option_button_text_fore_colour = tkinter.StringVar()
        #
        # theme.tv_box_object_back_colour = tkinter.StringVar()
        # theme.tv_box_object_border_colour = tkinter.StringVar()
        #
        # theme.tv_button_object_back_colour = tkinter.StringVar()
        # theme.tv_button_object_border_colour = tkinter.StringVar()
        # theme.tv_button_object_hover_colour = tkinter.StringVar()
        # theme.tv_button_text_fore_colour = tkinter.StringVar()
        # theme.tv_button_text_hover_colour = tkinter.StringVar()
        # theme.tv_button_text_font_name = tkinter.StringVar()

        return theme

    def __repr__(self):
        return "\n".join([
            f"\t< THEME >",
            f"{self.name.get()=}",
            f"{self.tv_text_box_object_back_colour.get()=}",
            f"{self.tv_text_box_object_border_colour.get()=}",
            f"{self.tv_text_box_text_font.get()=}",
            f"{self.tv_text_box_text_fore_colour.get()=}",

            f"{self.tv_label_object_back_colour.get()=}",
            f"{self.tv_label_object_border_colour.get()=}",
            f"{self.tv_label_text_font_name.get()=}",
            f"{self.tv_label_text_fore_colour.get()=}",

            f"{self.tv_list_box_object_back_colour.get()=}",
            f"{self.tv_list_box_object_border_colour.get()=}",
            f"{self.tv_list_box_text_font_name.get()=}",
            f"{self.tv_list_box_text_fore_colour.get()=}",

            f"{self.tv_combo_box_object_back_colour.get()=}",
            f"{self.tv_combo_box_object_border_colour.get()=}",
            f"{self.tv_combo_box_text_font_name.get()=}",
            f"{self.tv_combo_box_text_fore_colour.get()=}",

            f"{self.tv_option_button_object_border_colour.get()=}",

            f"{self.tv_box_object_back_colour.get()=}",
            f"{self.tv_box_object_border_colour.get()=}",

            f"{self.tv_button_object_back_colour.get()=}",
            f"{self.tv_button_object_border_colour.get()=}",
            f"{self.tv_button_object_hover_colour.get()=}",
            f"{self.tv_button_text_fore_colour.get()=}",
            f"{self.tv_button_text_hover_colour.get()=}",
            f"{self.tv_button_text_font_name.get()=}"
        ])


class ThemePublisher(tkinter.Tk):

    def __init__(
            self,
            theme_dir="./Themes/Version1"
    ):
        super().__init__()
        self.geometry(f"1000x600")

        self.theme_dir = theme_dir
        self.loaded_themes = []
        self.theme = Theme()
        self.working_theme = Theme()
        self.theme_idx = tkinter.IntVar(self, value=0)

        # object type: {access_property: tkinter_property}

        # ttk.Combobox(b)

        self.customizable = {
            # "Form": {
            #     "object": {
            #         "Back Color": "fill"
            #     }
            # },
            "TextBox": {
                "object": {
                    "Back Color": "background",
                    # "Border Color": "border"
                },
                "text": {
                    "Font Name": "font",
                    "Fore Color": "foreground"
                }
            },
            "Label": {
                "object": {
                    "Back Color": "background",
                    # "Border Color": "border",
                },
                "text": {
                    "Font Name": "font",
                    "Fore Color": "foreground"
                }
            },
            "ListBox": {
                "object": {
                    "Back Color": "background",
                    "Border Color": "border"
                },
                "text": {
                    "Font Name": "font",
                    "Fore Color": "foreground"
                }
            },
            "ComboBox": {
                "object": {
                    "Back Color": "background",
                    # "Border Color": "outline"
                },
                "text": {
                    "Font Name": "font",
                    "Fore Color": "foreground"
                }
            },
            "OptionButton": {
                "object": {
                    "Border Color": "outline"
                }
            },
            "Box": {
                "object": {
                    "Back Color": "background",
                    # "Border Color": "bd"
                }
            },
            "Button": {
                "object": {
                    "Back Color": "background",
                    # "Border Color": "border",
                    "Hover Color": "activebackground"
                },
                "text": {
                    "Fore Color": "foreground",
                    "Hover Fore Color": "activeforeground",
                    # "Font Size": "font"
                }
            }
        }

        self.load_themes()
        self.dirty_themes = tkinter.Variable(self, value=[False for i in range(len(self.loaded_themes) + 1)])

        # tkinter.Frame(b)

        # btn = tkinter.Button(self)
        # btn.configure(activebackground=, activeforeground=, background=, borderwidth=, cursor=, disabledforeground=, font=,foreground=,highlightbackground=, highlightcolor=, justify=)

        self.tv_btn_prev_theme, \
        self.btn_prev_theme \
            = button_factory(
            self,
            tv_btn="<<",
            kwargs_btn={
                "command": self.click_prev_theme
            }
        )

        self.tv_btn_next_theme, \
        self.btn_next_theme \
            = button_factory(
            self,
            tv_btn=">>",
            kwargs_btn={
                "command": self.click_next_theme
            }
        )

        self.tv_label_theme_name, \
        self.label_theme_name, \
        self.tv_entry_theme_name, \
        self.entry_theme_name, \
            = entry_factory(
            self,
            tv_label="Theme Name:"
        )

        self.tv_label_combo_choice_1, \
        self.label_combo_choice_1, \
        self.tv_combo_choice_1, \
        self.combo_choice_1 \
            = combo_factory(
            self,
            tv_label="Customize:",
            tv_combo=tkinter.StringVar(name="tv_combo_1", value=""),
            kwargs_combo={
                "values": list(self.customizable)
            }
        )

        self.tv_label_combo_choice_2, \
        self.label_combo_choice_2, \
        self.tv_combo_choice_2, \
        self.combo_choice_2 \
            = combo_factory(
            self,
            tv_label="Option:",
            tv_combo=tkinter.StringVar(name="tv_combo_2", value=""),
            kwargs_combo={
                "state": "disabled"
            }
        )

        self.tv_label_combo_choice_3, \
        self.label_combo_choice_3, \
        self.tv_combo_choice_3, \
        self.combo_choice_3 \
            = combo_factory(
            self,
            tv_label="Attribute:",
            tv_combo=tkinter.StringVar(name="tv_combo_3", value=""),
            kwargs_combo={
                "state": "disabled"
            }
        )

        self.tv_combo_choice_1.trace_variable("w", self.combo_update)
        self.tv_combo_choice_2.trace_variable("w", self.combo_update)
        self.tv_combo_choice_3.trace_variable("w", self.combo_update)

        print(f"{self.tv_combo_choice_1.__dict__['_name']=}")

        self.tv_dc_frame_fill = tkinter.StringVar(self, value="")
        self.tv_dc_textbox_fill = tkinter.StringVar(self, value="")
        self.tv_dc_textbox_background = tkinter.StringVar(self, value="")

        self.demo_dat_names_list = [
            "Darth Vader",
            "Luke Skywalker",
            "Obi-wan Kenobi",
            "Leia Skywalker"
        ]
        self.demo_dat_label_title = "This is a Demo Form"
        self.demo_dat_entry_text = "This is some demo text. Type something here to see how it looks"
        self.demo_dat_label_entry_text = "Demo textBox:"
        self.demo_dat_btn_label = "Click Me!"
        self.demo_dat_combo_label = "Demo ComboBox:"
        self.demo_dat_label_list = "This is a demo List:"
        self.demo_dat_list_list = [
            ("Alderaan", "2 Billion"),
            ("Tatooine", "200 Thousand"),
            ("Mustafar", "20 Thousand")
        ]

        self.demo_form_frame = tkinter.Frame(self)
        self.demo_form_sub_frame = tkinter.Frame(self.demo_form_frame, background=random_colour(rgb=False))
        # self.demo_tv_label_title = tkinter.StringVar(self, value=self.demo_dat_label_title)
        # self.demo_label_title = tkinter.Label(self.demo_form_sub_frame, textvariable=self.demo_tv_label_title)
        self.demo_tv_label_title, self.demo_label_title = label_factory(self.demo_form_sub_frame,
                                                                        tv_label=self.demo_dat_label_title)
        self.demo_label_entry, self.demo_label_entry, self.demo_tv_entry, self.demo_entry = entry_factory(
            self.demo_form_sub_frame, tv_label=self.demo_dat_label_entry_text, tv_entry=self.demo_dat_entry_text)
        self.demo_tv_button, self.demo_button = button_factory(self.demo_form_sub_frame, tv_btn=self.demo_dat_btn_label,
                                                               kwargs_btn={"command": self.click_demo_btn})
        self.demo_tv_label_combo, self.demo_label_combo, self.demo_tv_combo, self.demo_combo = combo_factory(
            self.demo_form_sub_frame, tv_label=self.demo_dat_combo_label,
            kwargs_combo={"values": self.demo_dat_names_list})
        self.demo_tv_label_list, self.demo_label_list, self.demo_tv_list, self.demo_list = list_factory(
            self.demo_form_sub_frame, tv_label=self.demo_dat_label_list, tv_list=self.demo_dat_list_list)
        self.demo_radio_frame = tkinter.Frame(self.demo_form_sub_frame)
        self.tv_demo_radio = tkinter.IntVar(self)
        self.demo_radio_1 = tkinter.Radiobutton(self.demo_radio_frame, text="Popcorn", variable=self.tv_demo_radio,
                                                value=1, command=self.demo_radio_update)
        self.demo_radio_2 = tkinter.Radiobutton(self.demo_radio_frame, text="Hot Dog", variable=self.tv_demo_radio,
                                                value=2, command=self.demo_radio_update)
        self.demo_radio_3 = tkinter.Radiobutton(self.demo_radio_frame, text="Cotton Candy", variable=self.tv_demo_radio,
                                                value=3, command=self.demo_radio_update)

        self.tv_btn_publish_theme, self.btn_publish_theme = button_factory(self, tv_btn="publish", kwargs_btn={
            "command": self.click_publish_theme})

        self.btn_prev_theme.grid(row=0, column=0)
        self.btn_next_theme.grid(row=0, column=1)
        self.label_theme_name.grid(row=1, column=0)
        self.entry_theme_name.grid(row=1, column=1)
        self.label_combo_choice_1.grid(row=2, column=0)
        self.combo_choice_1.grid(row=2, column=1)
        self.label_combo_choice_2.grid(row=3, column=0)
        self.combo_choice_2.grid(row=3, column=1)
        self.label_combo_choice_3.grid(row=4, column=0)
        self.combo_choice_3.grid(row=4, column=1)

        self.rgb_slider = RGBSlider(self, show_result=True)
        self.rgb_slider.colour.trace_variable("w", self.rgb_update)
        self.rgb_slider.grid(row=5, column=0, columnspan=2)

        self.font_chooser = FontChooser(self)
        self.font_chooser.status.trace_variable("w", self.font_update)
        self.font_chooser.grid(row=5, column=0, columnspan=2)

        self.number_chooser = ttk.Scale(self, from_=0, to=100, orient=tkinter.HORIZONTAL)
        self.number_chooser.grid(row=5, column=0, columnspan=2)

        self.btn_publish_theme.grid(row=6, column=0)
        self.demo_form_frame.grid(row=7, column=0)

        self.demo_form_sub_frame.grid(row=0, column=0)
        self.demo_label_title.grid(row=0, column=0)
        self.demo_label_entry.grid(row=1, column=0)
        self.demo_entry.grid(row=1, column=1)
        self.demo_button.grid(row=2, column=0)
        self.demo_label_list.grid(row=3, column=0)
        self.demo_list.grid(row=3, column=1)
        self.demo_radio_frame.grid(row=4, column=0)
        self.demo_radio_1.grid(row=0, column=0)
        self.demo_radio_2.grid(row=1, column=0)
        self.demo_radio_3.grid(row=2, column=0)

        self.combo_update(None, None, None)

    def combo_choice_data(self):
        return {
            "object": self.tv_combo_choice_1.get(),
            "option": self.tv_combo_choice_2.get(),
            "attribute": self.tv_combo_choice_3.get()
        }

    def combo_update(self, var_name, index, mode, *rest):
        print(f"combo_update")
        message = ""
        # print(f"{var_name=}, {index=}, {mode=}, {rest=}")
        if var_name == "tv_combo_1":
            self.tv_combo_choice_2.set("")
            self.tv_combo_choice_3.set("")

        if var_name == "tv_combo_2":
            self.tv_combo_choice_3.set("")

        combo_data = self.combo_choice_data()
        # print(f"{len(combo_data)=}, {combo_data=}")
        obj = combo_data["object"]
        option = combo_data["option"]
        attribute = combo_data["attribute"]
        showing = (True, False, False)
        if obj:
            message += "A"
            options = list(self.customizable[obj])
            if option:
                message += "B"
                attributes = list(self.customizable[obj][option])
                if attribute:
                    message += "C"
                    if attributes:
                        message += "D"
                        match attribute:
                            case "Border" | "bd":
                                # self.number_chooser.configure(state="normal")
                                showing = (False, True, False)
                                self.number_chooser.grid(row=5, column=0, columnspan=2)
                                self.rgb_slider.grid_forget()
                            case "Font Name":
                                # self.font_chooser.configure(state="normal")
                                showing = (False, False, True)
                                self.font_chooser.grid(row=5, column=0, columnspan=2)
                                self.rgb_slider.grid_forget()
                            case _:  # colour
                                # self.font_chooser.configure(state="disabled")
                                # self.number_chooser.configure(state="disabled")
                                showing = (True, False, False)

                        # print(f"{options=}, {attribute=}")
                        # print(f"{attributes=}, {attribute=}")
                    else:
                        message += "E"
                        self.combo_choice_2.configure(state="disabled")
                else:
                    message += "F"
                    self.combo_choice_3.configure(state="active", values=attributes)

            else:
                message += "G"
                self.combo_choice_2.configure(state="active", values=options)
                self.combo_choice_3.configure(state="disabled")
                self.tv_combo_choice_3.set("")
        else:
            message += "H"
            self.combo_choice_2.configure(state="disabled")
            self.combo_choice_3.configure(state="disabled")
            self.tv_combo_choice_2.set("")
            self.tv_combo_choice_3.set("")
        # print(f"{combo_data=}")
        # print(f"{message=}")

        widget = None
        if showing[0]:
            self.number_chooser.grid_forget()
            self.font_chooser.grid_forget()
        if showing[1]:
            self.rgb_slider.grid_forget()
            self.font_chooser.grid_forget()
        if showing[2]:
            self.rgb_slider.grid_forget()
            self.number_chooser.grid_forget()
        print(f"{widget=}, {showing=}")
        if widget:
            widget.grid(row=5, column=0, columnspan=2)

    def load_themes(self):
        if not os.path.isdir(self.theme_dir):
            os.mkdir(self.theme_dir)
            return
        loaded_themes = []
        for file in os.listdir(self.theme_dir):
            if file.endswith(".json") and file.startswith("TKTheme_"):
                with open(f"{self.theme_dir}/{file}", "r") as f:
                    # loaded_themes.append(json.load(f))
                    theme = self.parse(json.load(f))
                    self.loaded_themes.append(theme)
                    print(f"LOADED THEME\n\n{theme}")

        print(f"Loaded {len(self.loaded_themes)} themes on start.")

    def click_demo_btn(self):
        tkinter.messagebox.showinfo(title="Thanks", message="Thank You!")

    def demo_radio_update(self):
        print(f"got {self.tv_demo_radio.get()}")

    def rgb_update(self, *args):
        data = self.combo_choice_data()
        c = self.rgb_slider.colour.get()
        if all(data.values()):
            print(f"updating demo\n\t{data=}\n\tcolour{self.rgb_slider.colour.get()}")
            d1 = data["object"]
            d2 = data["option"]
            d3 = data["attribute"]
            attr_name = {self.customizable[d1][d2][d3]: c}
            match d1:
                case "TextBox":
                    widgets = [self.demo_entry]
                case "Label":
                    widgets = [
                        self.demo_label_title,
                        self.demo_label_entry,
                        self.demo_label_list,
                        self.demo_label_combo
                    ]
                case "ComboBox":
                    widgets = [self.demo_combo]
                case "ListBox":
                    widgets = [self.demo_list]
                case "Box":
                    widgets = [self.demo_form_sub_frame]
                case "Button":
                    widgets = [self.demo_button]
                case "OptionButton":
                    widgets = [
                        self.demo_radio_1,
                        self.demo_radio_2,
                        self.demo_radio_3
                    ]
                case _:
                    widgets = None

            if widgets is not None:
                print(f"ABOUT TO UPDATE WIDGETS\n{widgets=}\n{data=}\n{attr_name=}")
                for widget in widgets:
                    widget.configure(**attr_name)

            self.dirty_current_theme()
            # for k1, v1 in self.customizable:
            #     if k1 == d1:
            #         for k2, v2 in v1.items():
            #             if k2 == d2:
            #                 for k3, v3 in v2.items():
            #                     if k3 == d3:
            #                         attr_name = v3

    def font_update(self, *args):

        data = self.combo_choice_data()
        f = eval(self.font_chooser.status.get())
        f_name = f["name"]
        f_weight = f["weight"]
        f_size = f["size"]
        f = (f_name, f_size, f_weight)

        if all(data.values()):
            print(f"updating demo\n\t{data=}\n\tcolour{self.rgb_slider.colour.get()}")
            d1 = data["object"]
            d2 = data["option"]
            d3 = data["attribute"]
            attr_name = {self.customizable[d1][d2][d3]: f}
            match d1:
                case "TextBox":
                    widgets = [self.demo_entry]
                case "Label":
                    widgets = [
                        self.demo_label_title,
                        self.demo_label_entry,
                        self.demo_label_list,
                        self.demo_label_combo
                    ]
                case "ComboBox":
                    widgets = [self.demo_combo]
                case "ListBox":
                    widgets = [self.demo_list]
                case "Box":
                    widgets = [self.demo_form_sub_frame]
                case "Button":
                    widgets = [self.demo_button]
                case "OptionButton":
                    widgets = [
                        self.demo_radio_1,
                        self.demo_radio_2,
                        self.demo_radio_3
                    ]
                case _:
                    widgets = None

            if widgets is not None:
                print(f"ABOUT TO UPDATE WIDGETS\n{widgets=}\n{data=}\n{attr_name=}")
                for widget in widgets:
                    widget.configure(**attr_name)

        self.dirty_current_theme()

    def click_prev_theme(self):
        v = self.theme_idx.get()
        print(f"click_prev_theme {v} -> {v - 1}")
        if v > 0:
            self.theme_idx.set(v - 1)
            self.demo_current_theme()
        else:
            messagebox.showinfo(title="Theme Publisher", message="Cannot go back any further.")

    def click_next_theme(self):
        v = self.theme_idx.get()
        print(f"click_next_theme {v} -> {v + 1}")
        if v < len(self.loaded_themes):
            self.theme_idx.set(v + 1)
            self.demo_current_theme()
        else:
            messagebox.showinfo(title="Theme Publisher", message="Cannot go any farther forward.")

    def demo_current_theme(self):
        idx = self.theme_idx.get()

        if idx < len(self.loaded_themes):
            theme = self.loaded_themes[idx]
        else:
            theme = self.working_theme

        print(f"{theme=}")

        v_01 = theme.tv_box_object_back_colour.get()
        if v_01:
            print(f"{v_01=}")
            self.demo_form_sub_frame.configure(background=v_01)
        else:
            print(f"theme.tv_box_object_back_colour is None")

        # v_02 = theme.tv_box_object_border_colour.get()
        # if v_02 is not None:
        #     print(f"{v_02=}")
        #     self.demo_entry.configure(background=v_02)
        # else:
        #     print(f"theme.tv_box_object_border_colour is None")

        v_03 = theme.tv_text_box_object_back_colour.get()
        if v_03:
            print(f"{v_03=}")
            self.demo_entry.configure(background=v_03)
        else:
            print(f"theme.tv_text_box_object_back_colour is None")

        # v_04 = theme.tv_text_box_object_border_colour.get()
        # if v_04 is not None:
        #     print(f"{v_04=}")
        #     self.demo_form_sub_frame.configure(background=v_04)
        # else:
        #     print(f"theme.tv_box_object_border_colour is None")

        v_05 = theme.tv_text_box_text_font.get()
        if v_05:
            print(f"{v_05=}")
            self.demo_entry.configure(font=v_05)
        else:
            print(f"theme.tv_box_object_border_colour is None")

        v_06 = theme.tv_text_box_text_fore_colour.get()
        if v_06:
            print(f"{v_06=}")
            self.demo_form_sub_frame.configure(background=v_06)
        else:
            print(f"theme.tv_box_object_border_colour is None")

        v_07 = theme.tv_label_object_back_colour.get()
        if v_07:
            print(f"{v_07=}")
            self.demo_form_sub_frame.configure(background=v_07)
        else:
            print(f"theme.tv_box_object_border_colour is None")

        v_08 = theme.tv_label_object_border_colour.get()
        if v_08:
            print(f"{v_08=}")
            self.demo_form_sub_frame.configure(background=v_08)
        else:
            print(f"theme.tv_box_object_border_colour is None")

        v_09 = theme.tv_label_text_font_name.get()
        if v_09:
            print(f"{v_09=}")
            self.demo_form_sub_frame.configure(background=v_09)
        else:
            print(f"theme.tv_box_object_border_colour is None")

        v_10 = theme.tv_label_text_fore_colour.get()
        if v_10:
            print(f"{v_10=}")
            self.demo_form_sub_frame.configure(background=v_10)
        else:
            print(f"theme.tv_box_object_border_colour is None")

        v_11 = theme.tv_list_box_object_back_colour.get()
        if v_11:
            print(f"{v_11=}")
            self.demo_form_sub_frame.configure(background=v_11)
        else:
            print(f"theme.tv_box_object_border_colour is None")

        v_12 = theme.tv_list_box_object_border_colour.get()
        if v_12:
            print(f"{v_12=}")
            self.demo_form_sub_frame.configure(background=v_12)
        else:
            print(f"theme.tv_box_object_border_colour is None")

        v_13 = theme.tv_list_box_text_font_name.get()
        if v_13:
            print(f"{v_13=}")
            self.demo_form_sub_frame.configure(background=v_13)
        else:
            print(f"theme.tv_box_object_border_colour is None")

        v_14 = theme.tv_list_box_text_fore_colour.get()
        if v_14:
            print(f"{v_14=}")
            self.demo_form_sub_frame.configure(background=v_14)
        else:
            print(f"theme.tv_box_object_border_colour is None")

        v_15 = theme.tv_combo_box_object_back_colour.get()
        if v_15:
            print(f"{v_15=}")
            self.demo_form_sub_frame.configure(background=v_15)
        else:
            print(f"theme.tv_box_object_border_colour is None")

        v_16 = theme.tv_combo_box_object_border_colour.get()
        if v_16:
            print(f"{v_16=}")
            self.demo_form_sub_frame.configure(background=v_16)
        else:
            print(f"theme.tv_box_object_border_colour is None")

        v_17 = theme.tv_combo_box_text_font_name.get()
        if v_17:
            print(f"{v_17=}")
            self.demo_form_sub_frame.configure(background=v_17)
        else:
            print(f"theme.tv_box_object_border_colour is None")

        v_18 = theme.tv_combo_box_text_fore_colour.get()
        if v_18:
            print(f"{v_18=}")
            self.demo_form_sub_frame.configure(background=v_18)
        else:
            print(f"theme.tv_box_object_border_colour is None")

        # v_19 = theme.tv_option_button_object_back_colour.get()
        # if v_19:
        #     print(f"{v_19=}")
        #     self.demo_form_sub_frame.configure(background=v_19)
        # else:
        #     print(f"theme.tv_box_object_border_colour is None")

        v_20 = theme.tv_option_button_object_border_colour.get()
        if v_20:
            print(f"{v_20=}")
            self.demo_form_sub_frame.configure(background=v_20)
        else:
            print(f"theme.tv_box_object_border_colour is None")

        # v_21 = theme.tv_option_button_text_font_name.get()
        # if v_21:
        #     print(f"{v_21=}")
        #     self.demo_form_sub_frame.configure(background=v_21)
        # else:
        #     print(f"theme.tv_box_object_border_colour is None")
        #
        # v_22 = theme.tv_option_button_text_fore_colour.get()
        # if v_22:
        #     print(f"{v_22=}")
        #     self.demo_form_sub_frame.configure(background=v_22)
        # else:
        #     print(f"theme.tv_box_object_border_colour is None")

        v_23 = theme.tv_box_object_back_colour.get()
        if v_23:
            print(f"{v_23=}")
            self.demo_form_sub_frame.configure(background=v_23)
        else:
            print(f"theme.tv_box_object_border_colour is None")

        v_24 = theme.tv_box_object_border_colour.get()
        if v_24:
            print(f"{v_24=}")
            self.demo_form_sub_frame.configure(background=v_24)
        else:
            print(f"theme.tv_box_object_border_colour is None")

        v_25 = theme.tv_button_object_back_colour.get()
        if v_25:
            print(f"{v_25=}")
            self.demo_form_sub_frame.configure(background=v_25)
        else:
            print(f"theme.tv_box_object_border_colour is None")

        v_26 = theme.tv_button_object_border_colour.get()
        if v_26:
            print(f"{v_26=}")
            self.demo_form_sub_frame.configure(background=v_26)
        else:
            print(f"theme.tv_box_object_border_colour is None")

        v_27 = theme.tv_button_object_hover_colour.get()
        if v_27:
            print(f"{v_27=}")
            self.demo_form_sub_frame.configure(background=v_27)
        else:
            print(f"theme.tv_box_object_border_colour is None")

        v_28 = theme.tv_button_text_fore_colour.get()
        if v_28:
            print(f"{v_28=}")
            self.demo_form_sub_frame.configure(background=v_28)
        else:
            print(f"theme.tv_box_object_border_colour is None")

        v_29 = theme.tv_button_text_hover_colour.get()
        if v_29:
            print(f"{v_29=}")
            self.demo_form_sub_frame.configure(background=v_29)
        else:
            print(f"theme.tv_box_object_border_colour is None")

        v_30 = theme.tv_button_text_font_name.get()
        if v_30:
            print(f"{v_30=}")
            self.demo_form_sub_frame.configure(background=v_30)
        else:
            print(f"theme.tv_box_object_border_colour is None")

        self.theme = theme

    def dirty_current_theme(self):
        dirty = list(self.dirty_themes.get())
        dirty[self.theme_idx.get()] = True
        self.dirty_themes.set(dirty)

    def click_publish_theme(self):
        print(f"publish")

    def parse(self, f_in):
        # theme = None

        parsed_theme = {}
        theme_keys_1 = set(self.customizable.keys())
        print(f"{theme_keys_1=}")
        theme_keys_2 = set(flatten([list(v.keys()) for v in self.customizable.values()]))
        print(f"{theme_keys_2=}")
        theme_keys_3 = set(flatten([[list(v2.keys()) for v2 in v1.values()] for v1 in self.customizable.values()]))
        print(f"{theme_keys_3=}")
        for k1, v1 in f_in.items():
            if k1 in theme_keys_1:
                for k2, v2 in v1.items():
                    if k2 in theme_keys_2:
                        for k3, v3 in v2.items():
                            if k2 in theme_keys_2:
                                # parsed_theme.get(k1, {}).get(k2, {}).get(k3, {})
                                parsed_theme.setdefault(k1, {}).setdefault(k2, {}).setdefault(k3, {})
                                parsed_theme[k1][k2][k3] = v3
                                # \
                                # = v3
        theme = Theme()
        theme = theme.parse(parsed_theme)
        print(f"theme={theme}")
        return theme
import tkinter

from colour_utility import *
from ctkinter import *
from orbiting_date_picker import OrbitingDatePicker
from tkinter_utility import *
from utility import Rect2


# class ToggleButton(tkinter.Frame):
#
#     def __init__(
#             self,
#             master,
#             label_text="Toggle",
#             state: bool = False,
#             width_label=25,
#             height_label=1,
#             width_canvas=100,
#             height_canvas=50,
#             colour_fg_true="#003000",
#             colour_bg_true="#29c164",
#             colour_fg_false="#300000",
#             colour_bg_false="#c12929",
#             *args, **kwargs):
#         super().__init__(master, width=width_canvas, height=height_canvas, *args, **kwargs)
#
#         self.tv_label = tkinter.StringVar(self, value=label_text)
#         self.label = tkinter.Label(self, textvariable=self.tv_label, width=width_label, height=height_label)
#         self.frame_canvas = tkinter.Frame(self, width=width_label + width_canvas)
#         self.canvas = tkinter.Canvas(self.frame_canvas, width=width_canvas, height=height_canvas)
#
#         self.colour_bg_true = colour_bg_true
#         self.colour_bg_false = colour_bg_false
#         self.colour_fg_true = colour_fg_true
#         self.colour_fg_false = colour_fg_false
#         self.width = width_canvas
#         self.height = height_canvas
#
#         self.state = tkinter.BooleanVar(self, value=state)
#         self.state.trace_variable("w", self.state_update)
#
#         self.sliding = tkinter.BooleanVar(self, value=False)
#
#         self.bind("<Button-1>", self.click)
#         self.label.bind("<Button-1>", self.click)
#         self.frame_canvas.bind("<Button-1>", self.click)
#         self.canvas.bind("<Button-1>", self.click)
#
#         x1, y1, x2, y2 = self.width * 0.15, self.height * 0.15, self.width * 0.85, self.height * 0.85
#         pts = [
#             (x1, y1),
#             (x2, y1),
#             (x2, y2),
#             (x1, y2)
#         ]
#         xs, ys = [[pt[i] for pt in pts] for i in range(2)]
#         self.round_rect = round_polygon(
#             self.canvas,
#             xs,
#             ys,
#             width=2,
#             sharpness=25,
#             outline=self.colour_fg_false,
#             fill=brighten(self.colour_bg_false, 0.25, rgb=False)
#         )
#         self.text_off = self.canvas.create_text(self.width * 0.25, self.height / 2, text="Off",
#                                                 fill=self.colour_fg_false)
#         self.text_on = self.canvas.create_text(self.width * 0.75, self.height / 2, text="On", fill=self.colour_fg_true)
#
#         self.state_update()
#
#     def state_update(self, *args):
#         slices = 10
#         state = self.state.get()
#         bg_start = self.colour_bg_true if not state else self.colour_bg_false
#         bg_end = self.colour_bg_false if not state else self.colour_bg_true
#         bg_gradient_colours = [gradient(i, slices, bg_start, bg_end) for i in range(slices)]
#         fg_start = self.colour_fg_true if not state else self.colour_fg_false
#         fg_end = self.colour_fg_false if not state else self.colour_fg_true
#         bg_gradient_colours = [gradient(i, slices, bg_start, bg_end, rgb=False) for i in range(slices)]
#         fg_gradient_colours = [gradient(i, slices, fg_start, fg_end, rgb=False) for i in range(slices)]
#
#         # print(f"Status Update: {state=}")
#
#         if state:
#             self.canvas.itemconfigure(self.text_on, state="normal")
#             self.canvas.itemconfigure(self.text_off, state="hidden")
#         else:
#             self.canvas.itemconfigure(self.text_on, state="hidden")
#             self.canvas.itemconfigure(self.text_off, state="normal")
#
#         def iter_update(i):
#             # print(f"\titer_{i=}")
#             if i == slices:
#                 self.sliding.set(False)
#                 return
#
#             bg_colour = bg_gradient_colours[i]
#             fg_colour = fg_gradient_colours[i]
#             fill_colour = brighten(bg_colour, 0.25, rgb=False) if not state else darken(bg_colour, 0.25, rgb=False)
#
#             # https://stackoverflow.com/questions/22838255/tkinter-canvas-resizing-automatically
#             self.configure(background=bg_colour, highlightthickness=0)
#             self.canvas.itemconfigure(
#                 self.round_rect,
#                 outline=fg_colour,
#                 fill=fill_colour
#             )
#
#             self.canvas.itemconfigure(self.text_on, fill=fg_colour)
#             self.canvas.itemconfigure(self.text_off, fill=fg_colour)
#             self.canvas.configure(background=bg_colour, highlightthickness=0)
#             self.label.configure(background=bg_colour, foreground=fg_colour, highlightthickness=0)
#
#             self.after(50, iter_update, i + 1)
#
#         iter_update(0)
#
#     def click(self, *args):
#         if not self.sliding.get():
#             self.sliding.set(True)
#             self.state.set(not self.state.get())
#
#     def get_objects(self):
#         return (
#             self,
#             (self.tv_label, self.label),
#             self.frame_canvas,
#             (self.state, self.canvas)
#         )


def click_cbutton():
    print(f"click_cbutton")


class ToggleButtonQuantity(ToggleButton):

    def __init__(
            self,
            master,
            start_val=0,
            init_val=0,
            stop_val=100,
            scale_kwargs=None,
            *args,
            **kwargs
    ):
        super().__init__(master, *args, **kwargs)

        print(f"Start state: {self.state.get()=}\n{self.switch_mode.get()=}")

        valid_scale_kwargs = {
            "row": 0,
            "column": 2,
            "rowspan": 1,
            "columnspan": 1,
            "ipadx": 0,
            "ipady": 0,
            "padx": 0,
            "pady": 0
        }
        if scale_kwargs is None:
            self.scale_kwargs = valid_scale_kwargs
        else:
            self.scale_kwargs = scale_kwargs
            for k, v in valid_scale_kwargs.items():
                if k not in self.scale_kwargs:
                    self.scale_kwargs.update({k: v})

        self.start_val = start_val
        self.init_val = init_val
        self.stop_val = stop_val
        self.tv_scale = tkinter.IntVar(self, value=self.init_val)
        self.scale = tkinter.Scale(
            self,
            variable=self.tv_scale,
            from_=self.start_val,
            to=self.stop_val,
            orient=tkinter.HORIZONTAL
        )

        # self.rowconfigure("all", weight=1, uniform='row')
        # self.columnconfigure("all", weight=1, uniform='column')
        # self.columnconfigure(0, weight=1, uniform='column')
        # self.columnconfigure(1, weight=1, uniform='column')
        # self.columnconfigure(2, weight=1, uniform='column')

    def show_question(self, *args):
        print(f"show_quantity {self.state.get()=}")
        if self.state.get():
            self.scale.grid(**self.scale_kwargs)
        else:
            self.scale.grid_forget()

    # def state_change(self, *args):
    #     state = self.state.get()
    #     if state:
    #         self.scale.grid()

    def get_objects(self):
        return (*super().get_objects(), (self.tv_scale, self.scale))


class ToggleButtonWiredLess(ToggleButton):

    def __init__(
            self,
            master,
            tb_kwargs=None,
            tb_label_kwargs=None,
            tb_frame_canvas_kwargs=None,
            tb_canvas_kwargs=None,
            *args,
            **kwargs
    ):
        super().__init__(master, *args, **kwargs)

        print(f"Start state: {self.state.get()=}\n{self.switch_mode.get()=}")

        valid_tb_kwargs = {
            "row": 0,
            "column": 2,
            "rowspan": 1,
            "columnspan": 1,
            "ipadx": 0,
            "ipady": 0,
            "padx": 0,
            "pady": 0
        }
        valid_label_kwargs = {
            "row": 0,
            "column": 0,
            "rowspan": 1,
            "columnspan": 1,
            "ipadx": 0,
            "ipady": 0,
            "padx": 0,
            "pady": 0
        }
        valid_frame_canvas_kwargs = {
            "row": 0,
            "column": 1,
            "rowspan": 1,
            "columnspan": 1,
            "ipadx": 0,
            "ipady": 0,
            "padx": 0,
            "pady": 0
        }
        valid_canvas_kwargs = {
            "row": 0,
            "column": 0,
            "rowspan": 1,
            "columnspan": 1,
            "ipadx": 0,
            "ipady": 0,
            "padx": 0,
            "pady": 0
        }

        if tb_kwargs is None:
            self.tb_kwargs = valid_tb_kwargs
        else:
            self.tb_kwargs = tb_kwargs
            for k, v in valid_tb_kwargs.items():
                if k not in self.tb_kwargs:
                    self.tb_kwargs.update({k: v})

        if tb_label_kwargs is None:
            self.tb_label_kwargs = valid_label_kwargs
        else:
            self.tb_label_kwargs = tb_label_kwargs
            for k, v in valid_label_kwargs.items():
                if k not in self.tb_label_kwargs:
                    self.tb_label_kwargs.update({k: v})

        if tb_frame_canvas_kwargs is None:
            self.tb_frame_canvas_kwargs = valid_frame_canvas_kwargs
        else:
            self.tb_frame_canvas_kwargs = tb_frame_canvas_kwargs
            for k, v in valid_frame_canvas_kwargs.items():
                if k not in self.tb_frame_canvas_kwargs:
                    self.tb_frame_canvas_kwargs.update({k: v})

        if tb_canvas_kwargs is None:
            self.tb_canvas_kwargs = valid_canvas_kwargs
        else:
            self.tb_canvas_kwargs = tb_canvas_kwargs
            for k, v in valid_canvas_kwargs.items():
                if k not in self.tb_canvas_kwargs:
                    self.tb_canvas_kwargs.update({k: v})

        self.tb__, \
        self.tb__label_data, \
        self.tb__frame_canvas, \
        self.tb__canvas_data \
            = ToggleButton(
            self,
            label_text="Wireless?",
            labels=("Yes", "No")
        ).get_objects()
        self.tb__tv_label, self.tb__label = self.tb__label_data
        self.tb__state, self.tb__canvas = self.tb__canvas_data

        print(f"##{self.switch_positions=}")
        try:
            print(f"##{self.switch_positions=}")
        except AttributeError:
            print(f"##self.switch_positions NOT FOUND")

        print(f"Start state: {self.tb__.state.get()=}\n{self.tb__.switch_mode.get()=}")

        # self.rowconfigure("all", weight=1, uniform='row')
        # self.columnconfigure("all", weight=1, uniform='column')
        # self.columnconfigure(1, weight=1, uniform='column')
        # self.columnconfigure(2, weight=1, uniform='column')
        # self.columnconfigure(3, weight=1, uniform='column')

    def show_question(self, *args):
        print(f"show_question {self.state.get()=}")
        if self.state.get():
            self.tb__.grid(**self.tb_kwargs)
            self.tb__label.grid(**self.tb_label_kwargs)
            self.tb__frame_canvas.grid(**self.tb_frame_canvas_kwargs)
            self.tb__canvas.grid(**self.tb_canvas_kwargs)
        else:
            self.tb__.grid_forget()
            self.tb__label.grid_forget()
            self.tb__frame_canvas.grid_forget()
            self.tb__canvas.grid_forget()

    # def state_change(self, *args):
    #     state = self.state.get()
    #     if state:
    #         self.scale.grid()

    # def get_objects(self):
    #     return (*super().get_objects(), (self.tv_scale, self.scale))


def testt_b1():
    win = tkinter.Tk()
    win.geometry(f"600x600")

    tb = ToggleButton(win)

    tb.pack()

    tb2 = CButton(
        win,
        text="Click Me",
        fg="white",
        width=100,
        height=50,
        command=click_cbutton,
        rounded_corners="round"
    )

    # c = tkinter.Canvas(win, width_canvas=250, height_canvas=250, background="#666666")
    # c.pack(fill="both")
    #
    # c.create_text(50, 50, text="Hello")

    tb2.pack()

    win.mainloop()


class HardwareFormApp(tkinter.Tk):

    def __init__(self):
        super().__init__()
        self.geometry(f"800x600")

        q = "quantity"
        w = "wired(less)"

        self.frame_top_controls = tkinter.Frame(self, name="top_controls")
        self.frame_software = tkinter.Frame(self, name="fame_software", background="#141441")
        self.frame_hardware = tkinter.Frame(self, name="fame_hardware", background="#411414")
        self.frame_comp_choice = tkinter.Frame(self.frame_hardware, name="fame_comp_choice")
        self.frame_toggle_buttons = tkinter.Frame(self.frame_hardware, background=random_colour(rgb=False))

        self.tv_label_comp_choice = tkinter.StringVar(self, value="Select Hardware:", name="tv_label_comp_choice")
        self.tv_comp_choice = tkinter.StringVar(self, name="tv_comp_choice")
        self.tv_label_company_choice = tkinter.StringVar(self, value="Select Company:", name="tv_label_company_choice")
        self.tv_company_choice = tkinter.StringVar(self, name="tv_company_choice")
        self.tv_label_objective_choice = tkinter.StringVar(self, value="What would you like help with?",
                                                           name="tv_label_objective_choice")
        self.tv_objective_choice = tkinter.StringVar(self, name="tv_objective_choice")

        # self.frame_hardware_software_toggles = tkinter.Frame(self)
        self.tb_allow_hardware = ToggleButton(self.frame_hardware, label_text="Hardware:", labels=None, state=False)
        self.tb_allow_software = ToggleButton(self.frame_software, label_text="Software:", labels=None, state=False)

        self.tv_label_odp, self.label_odp = label_factory(self.frame_top_controls, tv_label="Due Date:")
        self.odp = OrbitingDatePicker(self.frame_top_controls)

        self.list_of_objectives = [
            "New Employee Hire",
            "New Position for Existing Employee",
            "Employee Departure",
            "Installations",
            "Removals",
            "Travelling / Sick Day Lending",
            "License Renewals"
        ]
        self.list_of_computers = [
            "Laptop",
            "Desktop",
            "Printer",
            "Mobile Phone",
            "Landline",
            "tablet"
        ]
        self.list_of_companies = [
            "BWS",
            "Stargate",
            "Lewis",
            "Hugo"
        ]

        self.tv_label_objective_choice, \
        self.label_objective_choice, \
        self.tv_objective_choice, \
        self.combo_objective_choice = \
            combo_factory(
                self.frame_top_controls,
                tv_label=self.tv_label_objective_choice,
                tv_combo=self.tv_objective_choice,
                kwargs_combo={
                    "justify": tkinter.CENTER,
                    "values": self.list_of_objectives,
                    "width": 50
                }
            )

        self.tv_label_comp_choice, \
        self.label_comp_choice, \
        self.tv_comp_choice, \
        self.combo_comp_choice = \
            combo_factory(
                self.frame_comp_choice,
                tv_label=self.tv_label_comp_choice,
                tv_combo=self.tv_comp_choice,
                kwargs_combo={
                    "justify": tkinter.CENTER,
                    "values": self.list_of_computers
                }
            )

        self.tv_label_company_choice, \
        self.label_company_choice, \
        self.tv_company_choice, \
        self.combo_company_choice = \
            combo_factory(
                self.frame_top_controls,
                tv_label=self.tv_label_company_choice,
                tv_combo=self.tv_company_choice,
                kwargs_combo={
                    "justify": tkinter.CENTER,
                    "values": self.list_of_companies
                }
            )

        self.questions_software = [
            ("Email Outlook", None, tkinter.StringVar(self, name="outlook")),
            ("Access", None, tkinter.StringVar(self, name="access")),
            ("Syspro8", None, tkinter.StringVar(self, name="syspro8")),
            ("ShopClock", None, tkinter.StringVar(self, name="shopclock")),
            ("SolidWorks", None, tkinter.StringVar(self, name="solidworks")),
            ("Inventor", None, tkinter.StringVar(self, name="inventor")),
            ("SGVault", None, tkinter.StringVar(self, name="sgvault")),
        ]

        self.questions_hardware = [
            ("Extra Charger(s)", None, tkinter.StringVar(self, name="extra_chargers")),
            ("Monitor(s)", (q, (1, 3)), tkinter.StringVar(self, name="monitors")),
            # ("Peripheral Cable(s)", None, tkinter.StringVar(win, name="peripheral_cables")),
            ("Dock", None, tkinter.StringVar(self, name="dock")),
            ("Keyboard", w, tkinter.StringVar(self, name="keyboard")),
            ("Mouse", w, tkinter.StringVar(self, name="mouse")),
            ("Mouse pad", None, tkinter.StringVar(self, name="mouse_pad")),
            ("Camera", None, tkinter.StringVar(self, name="camera")),
            ("Microphone", None, tkinter.StringVar(self, name="microphone"))
        ]
        self.questions_hardware = {
            k.lower().replace("(", "").replace(")", ""): dict(zip(["text", "follow_up", "var"], [k, f, v])) for
            k, f, v in self.questions_hardware}

        for q_title, q_data in self.questions_hardware.items():
            q_text, q_follow_up, q_var = list(q_data.values())
            follow_up_style = None if q_follow_up is None else (
                q_follow_up if not isinstance(q_follow_up, tuple) else q_follow_up[0])
            if follow_up_style == q:
                style, data = q_follow_up
            # elif follow_up_style == w:
            #     style, data = q_follow_up if q_follow_up
            else:
                style, data = (w, (None, None))

            print(f"\n{follow_up_style=}, {style=}, {data=}")

            if follow_up_style == w:
                print(f"WIREDLESS  {q_text=}")
                tb, label_data, \
                frame_canvas, \
                btn_data = \
                    ToggleButtonWiredLess(
                        self.frame_toggle_buttons,
                        label_text=q_text,
                        labels=None
                    ).get_objects()
                quantity_data = None, None
            else:
                print(f"QUANTITY  {q_text=}")
                tb, label_data, \
                frame_canvas, btn_data, \
                quantity_data = \
                    ToggleButtonQuantity(
                        self.frame_toggle_buttons,
                        label_text=q_text,
                        labels=None,
                        start_val=data[0],
                        stop_val=data[1]
                    ).get_objects()

            tv_label, label = label_data
            var, canvas = btn_data
            q_var, scale = quantity_data
            self.questions_hardware[q_title].update({
                "button": tb,
                "tv_label": tv_label,
                "label": label,
                "var": var,
                "frame_canvas": frame_canvas,
                "canvas": canvas,
                "q_var": q_var,
                "scale": scale
            })

            if q_follow_up is not None:
                if style == q:
                    var.trace_variable("w", tb.show_question)
                if style == w:
                    var.trace_variable("w", tb.show_question)

            label.grid(row=0, column=0, columnspan=1, rowspan=1)
            canvas.grid(row=0, column=1, columnspan=1, rowspan=1)
            frame_canvas.grid(row=0, column=1, columnspan=1, rowspan=1)
            tb.grid()

        self.tv_comp_choice.trace_variable("w", self.update_comp_choice)

        # ================================================================
        # ================================================================
        # ================================================================

        self.grid_args = {
            "frame_toggle_buttons": {"row": 2, "column": 0, "ipadx": 12, "ipady": 12},
            "frame_comp_choice": {"row": 1, "column": 0, "ipadx": 12, "ipady": 12},
            "frame_software": {"row": 1, "column": 1, "ipadx": 12, "ipady": 12},
            "frame_hardware": {"row": 1, "column": 0, "ipadx": 12, "ipady": 12},
            "frame_top_controls": {"row": 0, "column": 0, "ipadx": 12, "ipady": 12},
            "label_objective_choice": {"row": 0, "column": 0, "ipadx": 12, "ipady": 12},
            "combo_objective_choice": {"row": 0, "column": 1, "ipadx": 12, "ipady": 12},
            "label_company_choice": {"row": 1, "column": 0, "ipadx": 12, "ipady": 12},
            "combo_company_choice": {"row": 1, "column": 1, "ipadx": 12, "ipady": 12},
            "label_comp_choice": {"row": 2, "column": 0, "ipadx": 12, "ipady": 12},
            "combo_comp_choice": {"row": 2, "column": 1, "ipadx": 12, "ipady": 12},
            "label_odp": {"row":3, "column":0, "ipadx":12, "ipady":12},
            "odp": {"row":3, "column":1, "ipadx":12, "ipady":12}
        }

        self.label_objective_choice.grid(**self.grid_args["label_objective_choice"])
        self.combo_objective_choice.grid(**self.grid_args["combo_objective_choice"])
        self.label_company_choice.grid(**self.grid_args["label_company_choice"])
        self.combo_company_choice.grid(**self.grid_args["combo_company_choice"])
        self.label_comp_choice.grid(**self.grid_args["label_company_choice"])
        self.combo_comp_choice.grid(**self.grid_args["combo_company_choice"])
        self.label_odp.grid(**self.grid_args["label_odp"])
        self.odp.grid(**self.grid_args["odp"])

        tb, label_data, canvas_frame, canvas_data = self.tb_allow_hardware.get_objects()
        tb.grid(row=0, column=0)
        label_data[1].grid(row=0, column=0)
        canvas_frame.grid(row=0, column=1)
        canvas_data[1].grid(row=0, column=0)
        tb, label_data, canvas_frame, canvas_data = self.tb_allow_software.get_objects()
        tb.grid(row=2, column=2)
        label_data[1].grid(row=0, column=0)
        canvas_frame.grid(row=0, column=1)
        canvas_data[1].grid(row=0, column=0)

        self.frame_top_controls.grid(**self.grid_args["frame_top_controls"])

        self.tb_allow_hardware.state.trace_variable("w", self.update_allow_hardware)
        self.tb_allow_hardware.state.trace_variable("w", self.update_allow_software)

        self.frame_hardware.grid(**self.grid_args["frame_hardware"])
        self.frame_software.grid(**self.grid_args["frame_software"])
        # self.frame_comp_choice.grid(**self.grid_args["frame_comp_choice"])
        # self.frame_toggle_buttons.grid(**self.grid_args["frame_toggle_buttons"])

    def update_comp_choice(self, *args):
        val = self.tv_comp_choice.get()
        if val not in self.list_of_computers[:3]:
            self.frame_toggle_buttons.grid_forget()
        else:
            self.frame_toggle_buttons.grid(**self.grid_args["frame_toggle_buttons"])

    def update_allow_hardware(self, *args):
        allow = self.tb_allow_hardware.state.get()
        if allow:
            self.show_hardware_section()
        else:
            self.hide_hardware_section()

    def update_allow_software(self, *args):
        allow = self.tb_allow_hardware.state.get()
        if allow:
            self.show_software_section()
        else:
            self.hide_software_section()

    def show_hardware_section(self):
        self.frame_comp_choice.grid(**self.grid_args["frame_comp_choice"])
        self.frame_toggle_buttons.grid(**self.grid_args["frame_toggle_buttons"])

    def hide_hardware_section(self):
        self.frame_comp_choice.grid_forget()
        self.frame_toggle_buttons.grid_forget()

    def show_software_section(self):
        pass

    def hide_software_section(self):
        pass

def test_form():
    app = HardwareFormApp()
    app.mainloop()
    # win.geometry(f"600x600")
    #
    # q = "quantity"
    # w = "wired(less)"
    #
    # frame_comp_choice = tkinter.Frame(name="fame_comp_choice")
    # tv_label_comp_choice = tkinter.StringVar(win, value="Select Hardware:", name="tv_label_comp_choice")
    # tv_comp_choice = tkinter.StringVar(win, name="tv_comp_choice")
    #
    # tv_label_comp_choice, \
    # label_comp_choice, \
    # tv_comp_choice, \
    # combo_comp_choice = \
    #     combo_factory(
    #         frame_comp_choice,
    #         tv_label=tv_label_comp_choice,
    #         tv_combo=tv_comp_choice,
    #         kwargs_combo={
    #             "justify": tkinter.CENTER,
    #             "values": [
    #                 "Laptop",
    #                 "Desktop"
    #             ]
    #         }
    #     )
    #
    # questions_hardware = [
    #     ("Extra Charger(s)", None, tkinter.StringVar(win, name="extra_chargers")),
    #     ("Monitor(s)", (q, 3), tkinter.StringVar(win, name="monitors")),
    #     # ("Peripheral Cable(s)", None, tkinter.StringVar(win, name="peripheral_cables")),
    #     ("Dock", None, tkinter.StringVar(win, name="dock")),
    #     ("Keyboard", w, tkinter.StringVar(win, name="keyboard")),
    #     ("Mouse", w, tkinter.StringVar(win, name="mouse")),
    #     ("Mouse pad", None, tkinter.StringVar(win, name="mouse_pad")),
    #     ("Camera", None, tkinter.StringVar(win, name="camera")),
    #     ("Microphone", None, tkinter.StringVar(win, name="microphone"))
    # ]
    # questions_hardware = {k.lower().replace("(", "").replace(")", ""): dict(zip(["text", "follow_up", "var"], [k, f, v])) for
    #              k, f, v in questions_hardware}
    #
    # frame_toggle_buttons = tkinter.Frame(win, background=random_colour(rgb=False))
    # for q_title, q_data in questions_hardware.items():
    #     q_text, q_follow_up, q_var = list(q_data.values())
    #     tb, label_data, \
    #     frame_canvas, btn_data,\
    #     quantity_data = \
    #         ToggleButtonQuantity(
    #             frame_toggle_buttons,
    #             label_text=q_text,
    #             labels=None
    #             # ,
    #             # t_animation_time=100,
    #             # n_slices=1000000
    #         ).get_objects()
    #     tv_label, label = label_data
    #     var, canvas = btn_data
    #     q_var, scale = quantity_data
    #     questions_hardware[q_title].update({
    #         "button": tb,
    #         "tv_label": tv_label,
    #         "label": label,
    #         "var": var,
    #         "frame_canvas": frame_canvas,
    #         "canvas": canvas,
    #         "q_var": q_var,
    #         "scale": scale
    #     })
    #
    #     if q_follow_up is not None:
    #         if q_follow_up == q:
    #             var.trace_variable("w", tb.show_quantity)
    #
    #     label.grid(row=0, column=0)
    #     canvas.grid(row=0, column=1)
    #     frame_canvas.grid(row=0, column=1)
    #     tb.grid()
    #
    # label_comp_choice.grid(row=0, column=0, ipadx=12, ipady=12)
    # combo_comp_choice.grid(row=0, column=1, ipadx=12, ipady=12)
    # frame_comp_choice.grid()
    # frame_toggle_buttons.grid()
    #
    # # tbq = ToggleButtonQuantity(win)


def test_grid():
    app = tkinter.Tk()
    app.geometry(f"600x400")
    a = tkinter.Frame(app, name="frame_a", background="red", width=40, height=40)

    b = tkinter.Frame(app, name="frame_b", background="green", width=40, height=40)
    c = tkinter.Frame(app, name="frame_c", background="blue", width=40, height=40)
    d = tkinter.Frame(app, name="frame_d", background="indigo", width=40, height=40)

    e = tkinter.Frame(app, name="frame_e", background="violet", width=40, height=40)
    f = tkinter.Frame(app, name="frame_f", background="teal", width=40, height=40)
    g = tkinter.Frame(app, name="frame_g", background="orange", width=40, height=40)

    i = tkinter.Frame(d, name="frame_i", background="black", width=40, height=40)
    h = tkinter.Frame(d, name="frame_h", background="olive", width=40, height=40)

    a.grid(row=0, column=0, ipadx=12, ipady=12)
    b.grid(row=0, column=1, ipadx=12, ipady=12)
    c.grid(row=1, column=0, ipadx=12, ipady=12)
    d.grid(row=1, column=1, ipadx=12, ipady=12)

    e.grid(row=2, column=0, ipadx=12, ipady=12)
    f.grid(row=2, column=1, ipadx=12, ipady=12)
    g.grid(row=2, column=2, ipadx=12, ipady=12)

    h.grid(row=0, column=1, ipadx=12, ipady=12)
    i.grid(row=0, column=0, ipadx=12, ipady=12)

    var = tkinter.BooleanVar(app, value=False)

    def clicked(*event):
        print(f"clicked")
        var.set(not var.get())
        if var.get():
            h.grid_forget()
        else:
            h.grid(row=0, column=1, ipadx=12, ipady=12)

    tv_btn, btn = button_factory(app, tv_btn="click me", kwargs_btn={"command": clicked})
    tv_lbl, lbl, tv_entry, entry = entry_factory(app, tv_label="Var:", tv_entry=var)

    btn.grid()
    lbl.grid()
    entry.grid()

    app.mainloop()


if __name__ == '__main__':
    # test_tb1()
    test_form()
    # test_grid()

#
# class ToggleButton(tkinter.Frame):
#
#     def __init__(
#             self,
#             master,
#             label_text="Toggle",
#             state: bool = False,
#             width_label=25,
#             height_label=1,
#             width_canvas=100,
#             height_canvas=50,
#             colour_fg_true="#003000",
#             colour_bg_true="#29c164",
#             colour_fg_false="#300000",
#             colour_bg_false="#c12929",
#             *args, **kwargs):
#         super().__init__(master, width=width_canvas, height=height_canvas, *args, **kwargs)
#
#         self.tv_label = tkinter.StringVar(self, value=label_text)
#         self.label = tkinter.Label(self, textvariable=self.tv_label, width=width_label, height=height_label)
#         self.frame_canvas = tkinter.Frame(self, width=width_label + width_canvas)
#         self.canvas = tkinter.Canvas(self.frame_canvas, width=width_canvas, height=height_canvas)
#
#         self.colour_bg_true = colour_bg_true
#         self.colour_bg_false = colour_bg_false
#         self.colour_fg_true = colour_fg_true
#         self.colour_fg_false = colour_fg_false
#         self.width = width_canvas
#         self.height = height_canvas
#
#         self.state = tkinter.BooleanVar(self, value=state)
#         self.state.trace_variable("w", self.state_update)
#
#         self.sliding = tkinter.BooleanVar(self, value=False)
#
#         self.bind("<Button-1>", self.click)
#         self.label.bind("<Button-1>", self.click)
#         self.frame_canvas.bind("<Button-1>", self.click)
#         self.canvas.bind("<Button-1>", self.click)
#
#         self.text_off = self.canvas.create_text(self.width * 0.25, self.height / 2, text="Off", fill=self.colour_fg_false)
#         self.text_on = self.canvas.create_text(self.width * 0.75, self.height / 2, text="On", fill=self.colour_fg_true)
#         # self.round_rect = self.canvas.create_rectangle(self.width * 0.15, self.height * 0.15, self.width * 0.85, self.height * 0.85, outline=self.colour_fg_false, fill="")
#         self.round_rect = rounded_rect(self.canvas, self.width * 0.15, self.height * 0.15, self.width * 0.7, self.height * 0.7, 5)
#         for line in self.round_rect:
#             self.canvas.itemconfigure(line, fill=self.colour_fg_false)
#         # , width = 2, outline = self.colour_fg_false, fill = ""
#
#         self.state_update()
#
#     def state_update(self, *args):
#         slices = 10
#         state = self.state.get()
#         bg_start = self.colour_bg_true if not state else self.colour_bg_false
#         bg_end = self.colour_bg_false if not state else self.colour_bg_true
#         bg_gradient_colours = [gradient(i, slices, bg_start, bg_end) for i in range(slices)]
#         fg_start = self.colour_fg_true if not state else self.colour_fg_false
#         fg_end = self.colour_fg_false if not state else self.colour_fg_true
#         bg_gradient_colours = [gradient(i, slices, bg_start, bg_end, rgb=False) for i in range(slices)]
#         fg_gradient_colours = [gradient(i, slices, fg_start, fg_end, rgb=False) for i in range(slices)]
#
#         # print(f"Status Update: {state=}")
#
#         if state:
#             self.canvas.itemconfigure(self.text_on, state="normal")
#             self.canvas.itemconfigure(self.text_off, state="hidden")
#         else:
#             self.canvas.itemconfigure(self.text_on, state="hidden")
#             self.canvas.itemconfigure(self.text_off, state="normal")
#
#         def iter_update(i):
#             # print(f"\titer_{i=}")
#             if i == slices:
#                 self.sliding.set(False)
#                 return
#
#             bg_colour = bg_gradient_colours[i]
#             fg_colour = fg_gradient_colours[i]
#
#             # https://stackoverflow.com/questions/22838255/tkinter-canvas-resizing-automatically
#             self.configure(background=bg_colour, highlightthickness=0)
#             for line in self.round_rect:
#                 tp = self.canvas.type(line)
#                 if tp == "line":
#                     self.canvas.itemconfigure(line, fill=fg_colour)
#                 elif tp == "arc":
#                     self.canvas.itemconfigure(line, outline=fg_colour)
#
#             self.canvas.itemconfigure(self.text_on, fill=fg_colour)
#             self.canvas.itemconfigure(self.text_off, fill=fg_colour)
#             self.canvas.configure(background=bg_colour, highlightthickness=0)
#             self.label.configure(background=bg_colour, foreground=fg_colour, highlightthickness=0)
#
#             self.after(50, iter_update, i + 1)
#
#         iter_update(0)
#
#     def click(self, *args):
#         if not self.sliding.get():
#             self.sliding.set(True)
#             self.state.set(not self.state.get())
#
#     def get_objects(self):
#         return (
#             self,
#             (self.tv_label, self.label),
#             self.frame_canvas,
#             (self.state, self.canvas)
#         )

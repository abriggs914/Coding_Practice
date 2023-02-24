import os
import re
import tkinter

from colour_utility import *
from ctkinter import *
from orbiting_date_picker import OrbitingDatePicker
from tkinter_utility import *
from pyodbc_connection import connect
from location_utility import company_from_location
from utility import dict_print
from datetime_utility import *


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
            label_scale_kwargs=None,
            *args,
            **kwargs
    ):
        super().__init__(master, *args, **kwargs)

        print(f"Start state: {self.state.get()=}\n{self.switch_mode.get()=}")

        valid_label_scale_kwargs = {
            "row": 0,
            "column": 2,
            "rowspan": 1,
            "columnspan": 1,
            "ipadx": 0,
            "ipady": 0,
            "padx": 0,
            "pady": 0
        }
        valid_scale_kwargs = {
            "row": 0,
            "column": 3,
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

        if label_scale_kwargs is None:
            self.label_scale_kwargs = valid_label_scale_kwargs
        else:
            self.label_scale_kwargs = scale_kwargs
            for k, v in valid_label_scale_kwargs.items():
                if k not in self.label_scale_kwargs:
                    self.label_scale_kwargs.update({k: v})

        self.start_val = start_val if start_val is not None else 0
        self.stop_val = stop_val if stop_val is not None else 0
        self.init_val = clamp(self.start_val, init_val, self.stop_val)
        self.tv_scale = tkinter.IntVar(self, value=self.init_val)
        self.tv_scale.trace_variable("w", self.update_scale)
        self.tv_label_scale = tkinter.StringVar(self, value=f"x {self.tv_scale.get()}")
        self.scale = tkinter.Scale(
            self,
            variable=self.tv_scale,
            from_=self.start_val,
            to=self.stop_val,
            orient=tkinter.HORIZONTAL,
            width=self.height * 0.3,
            length=self.width,
            showvalue=0
        )
        self.label_scale = tkinter.Label(
            self,
            textvariable=self.tv_label_scale,
            background=self.colour_bg_true,
            foreground=self.colour_fg_true,
            font=self.label_font
        )

        self.rowconfigure("all", weight=1, uniform='row')
        self.columnconfigure([0, 1, 2, 3], minsize=100)
        self.columnconfigure([0, 1], weight=1, uniform='column')
        # self.columnconfigure(1, weight=1, uniform='column')
        # self.columnconfigure(2, weight=1, uniform='column')

    def show_question(self, *args):
        print(f"show_quantity {self.state.get()=}")
        if self.state.get():
            self.label_scale.grid(**self.label_scale_kwargs)
            self.scale.grid(**self.scale_kwargs)
            self.animate_number()
        else:
            self.label_scale.grid_forget()
            self.scale.grid_forget()

    def animate_number(self):
        s = self.n_slices
        t = self.after_time
        g = self.gradients[1]
        b, f = g

        def iter_update(i):
            if i == s:
                return
            cf = f[i]
            cb = b[i]
            self.label_scale.configure(background=cb, foreground=cf)
            self.after(t, iter_update, (i + 1))

        iter_update(0)

    def update_scale(self, *args):
        self.tv_label_scale.set(f"x {self.tv_scale.get()}")

    # def state_change(self, *args):
    #     state = self.state.get()
    #     if state:
    #         self.scale.grid()

    def get_objects(self):
        return (*super().get_objects(), (self.tv_scale, self.label_scale, self.scale))


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
            "columnspan": 2,
            "ipadx": 0,
            "ipady": 0,
            "padx": 0,
            "pady": 0,
            "sticky": "nsew"
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
            labels=("Yes", "No"),
            height_canvas=self.height,
            height_label=self.height_label,
            label_font=self.label_font,
            width_canvas=100,
            width_label=10,
            auto_grid=False
        ).get_objects()
        self.tb__tv_label, self.tb__label = self.tb__label_data
        self.tb__state, self.tb__canvas = self.tb__canvas_data

        print(f"##{self.switch_positions=}")
        try:
            print(f"##{self.switch_positions=}")
        except AttributeError:
            print(f"##self.switch_positions NOT FOUND")

        print(f"Start state: {self.tb__.state.get()=}\n{self.tb__.switch_mode.get()=}")

        self.rowconfigure("all", weight=1, uniform='row')
        self.columnconfigure([0, 1, 2, 3], minsize=100)
        self.columnconfigure([0, 1], weight=1, uniform='column')

        # self.rowconfigure("all", weight=1, uniform='row')
        # self.columnconfigure("all", weight=1, uniform='column')
        # self.columnconfigure(1, weight=1, uniform='column')
        # self.columnconfigure(2, weight=1, uniform='column')
        # self.columnconfigure(3, weight=1, uniform='column')

    def grid_widgets(self):
        super(ToggleButtonWiredLess, self).grid_widgets()
        self.show_widgets()

    def grid_forget_widgets(self):
        super(ToggleButtonWiredLess, self).grid_forget_widgets()
        self.hide_widgets()

    def show_question(self, *args):
        print(f"show_question {self.state.get()=}")
        if self.state.get():
            self.show_widgets()
        else:
            self.hide_widgets()

    def show_widgets(self):
        self.tb__.grid(**self.tb_kwargs)
        self.tb__label.grid(**self.tb_label_kwargs)
        self.tb__frame_canvas.grid(**self.tb_frame_canvas_kwargs)
        self.tb__canvas.grid(**self.tb_canvas_kwargs)

    def hide_widgets(self):
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
        # self.geometry(f"800x600")
        self.state("zoomed")

        q = "quantity"
        w = "wired(less)"
        d = "databaseSelection"

        self.default_data = {
            "start_of_day_hour": 8,
            "start_of_day_minute": 0,
            "start_of_day_format": "%A %a %d %Y"
        }

        self.flags = {
            "-odbc": self.flag_odbc,
            "-outlook": self.flag_outlook,
            "-outlook_archive": self.flag_outlook_archive,
            "-g_drive": self.flag_g_drive,
            "-u_drive": self.flag_u_drive
        }

        self.frame_top_controls = tkinter.Frame(self, name="top_controls")
        self.frame_top_controls_a = tkinter.Frame(self.frame_top_controls, name="top_controls_a", background="#171717")
        # self.frame_top_controls_a_a = tkinter.Frame(self.frame_top_controls_a, name="top_controls_a_a")
        self.frame_top_controls_b = tkinter.Frame(self.frame_top_controls, name="top_controls_b")
        self.frame_top_controls_c = tkinter.Frame(self.frame_top_controls, name="top_controls_c", background="#171717")
        self.frame_top_controls_d = tkinter.Frame(self.frame_top_controls, name="top_controls_d", background="#171717")
        self.frame_software = tkinter.Frame(self, name="fame_software", background="#141441", width=200)
        self.frame_hardware = tkinter.Frame(self, name="fame_hardware", background="#411414", width=200)
        self.frame_comp_choice = tkinter.Frame(self.frame_hardware, name="fame_comp_choice")
        self.frame_hardware_toggle_buttons = tkinter.Frame(self.frame_hardware, background=random_colour(rgb=False))
        self.frame_software_toggle_buttons = tkinter.Frame(self.frame_software, background=random_colour(rgb=False))
        self.frame_auto_reports = tkinter.Frame(self, name="frame_auto_reports", background="#54CE98")

        self.tv_label_auto_desc_text, \
        self.label_auto_desc_text, \
        self.tv_auto_desc_text, \
        self.auto_desc_text, \
            = text_factory(
                self.frame_auto_reports,
                tv_label="Auto-Generated Objective:",
                tv_text="Please select an objective from above.",
                kwargs_text={
                    "width": 100
                }
        )

        self.tv_label_comp_choice = tkinter.StringVar(self, value="Select Hardware:", name="tv_label_comp_choice")
        self.tv_comp_choice = tkinter.StringVar(self, name="tv_comp_choice")
        self.tv_label_company_choice = tkinter.StringVar(self, value="Select Company:", name="tv_label_company_choice")
        self.tv_company_choice = tkinter.StringVar(self, name="tv_company_choice", value=company_from_location())
        self.tv_label_objective_choice = tkinter.StringVar(self, value="What would you like help with?",
                                                           name="tv_label_objective_choice")
        self.tv_objective_choice = tkinter.StringVar(self, name="tv_objective_choice")

        # self.frame_hardware_software_toggles = tkinter.Frame(self)

        self.list_of_objectives = {
            "New Employee Hire": {
                "obj": """
New employee {new_emp_name}, will be starting {new_start_date} at {new_company}.
They will be reporting to {new_boss}.
They will require the following Hardware and Software prepared and installed.
{new_hardware}
{new_software}

Please notify {new_follow_up} once this has been completed

Comments:
{new_comments}
                    """,
                "flags": {
                    "auto": {
                        True: [
                            "-odbc",
                            "-outlook",
                            "-outlook_archive",
                            "-g_drive",
                            "-u_drive"
                        ]
                    },
                    "other": []
                }
            },
            "New Position for Existing Employee": {},
            "Employee Departure": {},
            "Installations": {},
            "Removals": {},
            "Travelling / Sick Day Lending": {},
            "License Renewals": {}
        }
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

        # Begin factories #

        self.tv_label_objective_choice, \
        self.label_objective_choice, \
        self.tv_objective_choice, \
        self.combo_objective_choice = \
            combo_factory(
                self.frame_top_controls_b,
                tv_label=self.tv_label_objective_choice,
                tv_combo=self.tv_objective_choice,
                kwargs_combo={
                    "justify": tkinter.CENTER,
                    "values": list(self.list_of_objectives.keys()),
                    "width": 50
                }
            )

        self.tv_label_entry_user_name, \
        self.label_entry_user_name, \
        self.tv_entry_user_name, \
        self.entry_user_name = \
            entry_factory(
                self.frame_top_controls_b,
                tv_label="Username:",
                tv_entry=os.getlogin(),
                # tv_text=os.environ.get('USERNAME'),
                kwargs_entry={
                    "justify": tkinter.CENTER,
                    "state": "disabled",
                    "width": 30
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
                self.frame_top_controls_b,
                tv_label=self.tv_label_company_choice,
                tv_combo=self.tv_company_choice,
                kwargs_combo={
                    "justify": tkinter.CENTER,
                    "values": self.list_of_companies
                }
            )

        self.tv_label_odp, self.label_odp = \
            label_factory(
                self.frame_top_controls_b,
                tv_label="Due Date:"
        )

        self.tv_button_submit_form,\
        self.tv_button_submit_form\
            = button_factory(
                self.frame_top_controls_d,
                tv_btn="Submit Form",
                kwargs_btn={
                    "command": self.click_submit_form
                }
        )

        # End factories #

        # Begin Other Control Widgets #

        self.tb_allow_hardware = ToggleButton(
            self.frame_hardware,
            label_text="Hardware:",
            labels=None,
            state=False,
            auto_grid=True
        )

        self.tb_allow_software = ToggleButton(
            self.frame_software,
            label_text="Software:",
            labels=None,
            state=False,
            auto_grid=True
        )

        self.odp = OrbitingDatePicker(self.frame_top_controls_b)

        sql = """
            SELECT
                [ITR Customers].[Name]
                , [ITR Customers].[Company]
                , [Dept].[Dept] AS [Department]
            FROM
                [ITR Customers]
            INNER JOIN
                [Dept]
            ON
                [ITR Customers].[Department] = [Dept].[DeptID]
            WHERE
                [Active] = 1
            ORDER BY
                [Name]
        """
        self.df_itr_customers = connect(sql=sql, server="server3", database="BWSdb", uid="user5", pwd="M@gic456")
        self.df_itr_departments = self.df_itr_customers["Department"].unique()
        self.df_itr_companies = self.df_itr_customers["Company"].unique()
        self.df_itr_employees = self.df_itr_customers["Name"].unique()
        # self.tv_label_mc_emp_selection, self.label_mc_emp_selection = label_factory(
        #     self.frame_top_controls_a_a,
        #     tv_label="Who is this for?"
        # )
        self.tb_same_user_as_for = ToggleButton(
            self.frame_top_controls_a,
            label_text="Who is this for?",
            state=True,
            labels=("Me", ""),
            auto_grid=True
        )
        self.mc_emp_selection = MultiComboBox(
            self.frame_top_controls_a,
            data=self.df_itr_customers,
            viewable_column_names=[
                "Name",
                "Company",
                "Department"
            ],
            indexable_column="Name",
            # tv_label="Who is this for?",
            limit_to_list=False,
            lock_result_col="Name",
            auto_grid=False
        )
        self.mc_emp_selection.res_tv_entry.set(self.tv_entry_user_name.get())

        self.tb_same_user_as_follow_up = ToggleButton(
            self.frame_top_controls_c,
            label_text="Follow up with you?",
            state=True,
            labels=None,
            auto_grid=True
        )
        self.mc_follow_up_selection = MultiComboBox(
            self.frame_top_controls_c,
            data=self.df_itr_customers,
            viewable_column_names=[
                "Name",
                "Company",
                "Department"
            ],
            indexable_column="Name",
            # tv_label="Who is this for?",
            limit_to_list=False,
            lock_result_col="Name",
            auto_grid=False
        )
        self.mc_follow_up_selection.res_tv_entry.set(self.tv_entry_user_name.get())

        self.tv_btn_open_tl_comments, \
        self.btn_open_tl_comments \
            = button_factory(
            self.frame_top_controls_b,
            tv_btn="Edit Comments",
            kwargs_btn={
                "command": self.click_open_comments
            }
        )
        self.tl_comments_input = None
        self.tl_frame_comments_btns = None
        self.tl_tv_label_text_comments = None
        self.tl_label_text_comments = None
        self.tl_tv_text_comments = tkinter.StringVar(self, value="", name="tv_comments")
        self.test_id = id(self.tl_tv_text_comments)
        self.tl_text_comments = None
        self.tl_tv_btn_submit_comment = None
        self.tl_btn_submit_comment = None
        self.tl_tv_btn_cancel_comment = None
        self.tl_btn_cancel_comment = None
        self.tl_tv_btn_clear_comment = None
        self.tl_btn_clear_comment = None
        self.tl_tv_btn_undo_comment = None
        self.tl_btn_undo_comment = None

        # End Other Control Widgets #

        r, c, rs, cs, ix, iy, x, y, s = self.grid_keys()

        # Begin Software #

        self.questions_software = [
            ("Outlook Email", None, tkinter.StringVar(self, name="outlook")),
            ("Outlook Archive", None, tkinter.StringVar(self, name="outlook")),
            ("Access", d, tkinter.StringVar(self, name="access")),
            ("ODBC", None, tkinter.StringVar(self, name="odbc")),
            ("G-Drive (Public)", None, tkinter.StringVar(self, name="g_drive")),
            ("U-Drive (Private)", None, tkinter.StringVar(self, name="u_drive")),
            ("Syspro8", None, tkinter.StringVar(self, name="syspro8")),
            ("ShopClock", None, tkinter.StringVar(self, name="shopclock")),
            ("SolidWorks", None, tkinter.StringVar(self, name="solidworks")),
            ("Inventor", None, tkinter.StringVar(self, name="inventor")),
            ("SGVault", None, tkinter.StringVar(self, name="sgvault"))
        ]
        self.questions_software = {
            k.lower().replace("(", "").replace(")", ""): dict(zip(["text", "follow_up", "var"], [k, f, v])) for
            k, f, v in self.questions_software}

        for j, q_title_q_data in enumerate(self.questions_software.items()):
            q_title, q_data = q_title_q_data
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
                        self.frame_software_toggle_buttons,
                        label_text=q_text,
                        labels=None,
                        width_label=20,
                        width_canvas=50,
                        height_canvas=30,
                        auto_grid=False
                    ).get_objects()
                quantity_data = None, None, None
            else:
                print(f"QUANTITY  {q_text=}")
                tb, label_data, \
                frame_canvas, btn_data, \
                quantity_data = \
                    ToggleButtonQuantity(
                        self.frame_software_toggle_buttons,
                        label_text=q_text,
                        labels=None,
                        start_val=data[0],
                        stop_val=data[1],
                        width_label=20,
                        width_canvas=50,
                        height_canvas=30,
                        auto_grid=False
                    ).get_objects()

            tv_label, label = label_data
            var, canvas = btn_data
            q_var, label_scale, scale = quantity_data
            self.questions_software[q_title].update({
                "tb": tb,
                "tv_label": tv_label,
                "label": label,
                "var": var,
                "frame_canvas": frame_canvas,
                "canvas": canvas,
                "q_var": q_var,
                "scale": scale,
                "showing": True,
                "grid_args": {
                    "label": {r: 0, c: 0, cs: 1, rs: 1},
                    "canvas": {r: 0, c: 1, cs: 1, rs: 1},
                    "frame_canvas": {r: 0, c: 1, cs: 1, rs: 1},
                    "tb": {r: j, c: 0, cs: 1, rs: 1}
                }
            })

            tb.grid(**self.questions_software[q_title]["grid_args"]["tb"])
            canvas.grid(**self.questions_software[q_title]["grid_args"]["canvas"])
            frame_canvas.grid(**self.questions_software[q_title]["grid_args"]["frame_canvas"])
            label.grid(**self.questions_software[q_title]["grid_args"]["label"])

            if q_follow_up is not None:
                if style == q:
                    var.trace_variable("w", tb.show_question)
                if style == w:
                    var.trace_variable("w", tb.show_question)

            # label.grid(row=0, column=0, columnspan=1, rowspan=1)
            # canvas.grid(row=0, column=1, columnspan=1, rowspan=1)
            # frame_canvas.grid(row=0, column=1, columnspan=1, rowspan=1)
            # tb.grid()

        # End Software #

        # Begin Hardware #

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

        for j, q_title_q_data in enumerate(self.questions_hardware.items()):
            q_title, q_data = q_title_q_data
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
                        self.frame_hardware_toggle_buttons,
                        label_text=q_text,
                        labels=None,
                        width_label=20,
                        width_canvas=50,
                        height_canvas=30,
                        auto_grid=False
                    ).get_objects()
                quantity_data = None, None, None
            else:
                print(f"QUANTITY  {q_text=}")
                tb, label_data, \
                frame_canvas, btn_data, \
                quantity_data = \
                    ToggleButtonQuantity(
                        self.frame_hardware_toggle_buttons,
                        label_text=q_text,
                        labels=None,
                        start_val=data[0],
                        stop_val=data[1],
                        width_label=20,
                        width_canvas=50,
                        height_canvas=30,
                        auto_grid=False
                    ).get_objects()

            tv_label, label = label_data
            var, canvas = btn_data
            q_var, label_scale, scale = quantity_data
            self.questions_hardware[q_title].update({
                "tb": tb,
                "tv_label": tv_label,
                "label": label,
                "var": var,
                "frame_canvas": frame_canvas,
                "canvas": canvas,
                "q_var": q_var,
                "scale": scale,
                "showing": True,
                "grid_args": {
                    "label": {r: 0, c: 0, cs: 1, rs: 1},
                    "canvas": {r: 0, c: 1, cs: 1, rs: 1},
                    "frame_canvas": {r: 0, c: 1, cs: 1, rs: 1},
                    "tb": {r: j, c: 0, cs: 1, rs: 1}
                }
            })

            tb.grid(**self.questions_hardware[q_title]["grid_args"]["tb"])
            canvas.grid(**self.questions_hardware[q_title]["grid_args"]["canvas"])
            frame_canvas.grid(**self.questions_hardware[q_title]["grid_args"]["frame_canvas"])
            label.grid(**self.questions_hardware[q_title]["grid_args"]["label"])

            if q_follow_up is not None:
                if style == q:
                    var.trace_variable("w", tb.show_question)
                if style == w:
                    var.trace_variable("w", tb.show_question)
            # canvas.grid(row=0, column=1, columnspan=1, rowspan=1)
            # .grid(row=0, column=1, columnspan=1, rowspan=1)

        print(f"{dict_print(self.questions_hardware, 'Hardware')}")
        print(f"{dict_print(self.questions_software, 'Software')}")

        # ================================================================
        # ===================        Griding       =======================
        # ================================================================

        ipad_x_1, ipad_y_1 = 0, 0
        self.grid_args = {

            # self
            "frame_top_controls": {r: 0, c: 0, cs: 3, ix: ipad_x_1, iy: ipad_y_1},
            "frame_hardware": {r: 1, c: 0, ix: ipad_x_1, iy: ipad_y_1},
            "frame_software": {r: 1, c: 1, ix: ipad_x_1, iy: ipad_y_1},
            "frame_auto_reports": {r: 2, c: 0, rs: 1, cs: 3, ix: ipad_x_1, iy: ipad_y_1, s: "nswe"},

            # frame_top_controls
            "frame_top_controls_a": {r: 0, c: 0, rs: 1, cs: 1, ix: ipad_x_1, iy: ipad_y_1},
            "frame_top_controls_b": {r: 0, c: 1, rs: 1, cs: 1, ix: ipad_x_1, iy: ipad_y_1},
            "frame_top_controls_c": {r: 0, c: 2, rs: 1, cs: 1, ix: ipad_x_1, iy: ipad_y_1},
            "frame_top_controls_d": {r: 0, c: 3, rs: 1, cs: 1, ix: ipad_x_1, iy: ipad_y_1},

            # frame_top_controls_a
            # "frame_top_controls_a_a": {r: 0, c: 0},
            "mc_emp_selection": {r: 1, c: 0, rs: 1, cs: 1},
            #
            # # frame_top_controls_a_a
            # "label_mc_emp_selection": {r: 0, c: 0, rs: 1, cs: 1},

            # frame_top_controls_b
            "label_entry_user_name": {r: 0, c: 0, rs: 1, cs: 1, ix: ipad_x_1, iy: ipad_y_1},
            "entry_user_name": {r: 0, c: 1, rs: 1, cs: 1, ix: ipad_x_1, iy: ipad_y_1},
            "label_objective_choice": {r: 1, c: 0, ix: ipad_x_1, iy: ipad_y_1},
            "combo_objective_choice": {r: 1, c: 1, ix: ipad_x_1, iy: ipad_y_1},
            "label_company_choice": {r: 2, c: 0, ix: ipad_x_1, iy: ipad_y_1},
            "combo_company_choice": {r: 2, c: 1, ix: ipad_x_1, iy: ipad_y_1},
            "label_odp": {r: 3, c: 0, ix: ipad_x_1, iy: ipad_y_1},
            "odp": {r: 3, c:1, ix: ipad_x_1, iy: ipad_y_1},
            "btn_open_tl_comments": {r: 4, c: 1, ix: ipad_x_1, iy: ipad_y_1},

            # frame_top_controls_c
            # "frame_top_controls_a_a": {r: 0, c: 0},
            "mc_follow_up_selection": {r: 1, c: 0, rs: 1, cs: 1},

            # frame_top_controls_d
            "tv_button_submit_form": {r: 0, c: 0, ix: ipad_x_1, iy: ipad_y_1, cs: 1, rs: 1},

            # frame_hardware
            "frame_comp_choice": {r: 1, c: 0, ix: ipad_x_1, iy: ipad_y_1},
            "frame_hardware_toggle_buttons": {r: 2, c: 0, ix: ipad_x_1, iy: ipad_y_1},

            # frame_software
            "frame_software_toggle_buttons": {r: 2, c: 0, ix: ipad_x_1, iy: ipad_y_1},

            # frame_comp_choice
            "label_comp_choice": {r: 2, c: 0, ix: ipad_x_1, iy: ipad_y_1},
            "combo_comp_choice": {r: 2, c: 1, ix: ipad_x_1, iy: ipad_y_1},

            # frame_auto_reports
            "label_auto_desc_text": {r: 0, c: 0, rs: 1, cs: 3, ix: ipad_x_1, iy: ipad_y_1},
            "auto_desc_text": {r: 1, c: 0, rs: 1, cs: 3, ix: ipad_x_1, iy: ipad_y_1, s: "nswe"}
        }

        self.init_grid = {
            "frame_top_controls",
            "frame_hardware",
            "frame_software",
            "frame_auto_reports",
            "frame_top_controls_a",
            "frame_top_controls_b",
            "frame_top_controls_c",
            # "frame_top_controls_a_a",
            "label_auto_desc_text",
            "auto_desc_text",
            "mc_emp_selection",
            "mc_follow_up_selection",
            # "label_mc_emp_selection",
            "label_entry_user_name",
            "entry_user_name",
            "label_objective_choice",
            "combo_objective_choice",
            "label_company_choice",
            "combo_company_choice",
            "label_odp",
            "odp",
            "btn_open_tl_comments",
            "label_comp_choice",
            "combo_comp_choice"
        }

        for k in self.init_grid:
            v = self.grid_args[k]
            eval(f"self.{k}.grid(**{v})")

        # self.tb_allow_hardware.grid_widgets()
        # self.tb_allow_software.grid_widgets()
        # self.tb_same_user_as_for.grid_widgets()
        # self.tb_same_user_as_follow_up.grid_widgets()

        # for k, v in self.grid_args.items():
        #     eval(f"self.{k}.grid(**{v})")

        # self.mc_emp_selection.grid(**self.grid_args["mc_emp_selection"])
        #
        # self.label_entry_user_name.grid(**self.grid_args["label_entry_user_name"])
        # self.entry_user_name.grid(**self.grid_args["entry_user_name"])
        # self.label_objective_choice.grid(**self.grid_args["label_objective_choice"])
        # self.combo_objective_choice.grid(**self.grid_args["combo_objective_choice"])
        # self.label_company_choice.grid(**self.grid_args["label_company_choice"])
        # self.combo_company_choice.grid(**self.grid_args["combo_company_choice"])
        # self.label_comp_choice.grid(**self.grid_args["label_company_choice"])
        # self.combo_comp_choice.grid(**self.grid_args["combo_company_choice"])
        # self.label_odp.grid(**self.grid_args["label_odp"])
        # self.odp.grid(**self.grid_args["odp"])
        # self.frame_auto_reports.grid(**self.grid_args["frame_auto_reports"])
        # self.label_auto_desc_text.grid(**self.grid_args["label_auto_desc_text"])
        # self.auto_desc_text.grid(**self.grid_args["auto_desc_text"])

        # tb, label_data, canvas_frame, canvas_data = self.tb_allow_hardware.get_objects()
        # tb.grid(row=0, column=0)
        # label_data[1].grid(row=0, column=0)
        # canvas_frame.grid(row=0, column=1)
        # canvas_data[1].grid(row=0, column=0)
        # tb, label_data, canvas_frame, canvas_data = self.tb_allow_software.get_objects()
        # tb.grid(row=0, column=0)
        # label_data[1].grid(row=0, column=0)
        # canvas_frame.grid(row=0, column=1)
        # canvas_data[1].grid(row=0, column=0)
        # tb, label_data, canvas_frame, canvas_data = self.tb_same_user_as_for.get_objects()
        # tb.grid(row=0, column=0)
        # label_data[1].grid(row=0, column=0)
        # canvas_frame.grid(row=0, column=1)
        # canvas_data[1].grid(row=0, column=0)
        # tb, label_data, canvas_frame, canvas_data = self.tb_same_user_as_follow_up.get_objects()
        # tb.grid(row=0, column=0)
        # label_data[1].grid(row=0, column=0)
        # canvas_frame.grid(row=0, column=1)
        # canvas_data[1].grid(row=0, column=0)

        # self.label_mc_emp_selection.grid(**self.grid_args["label_mc_emp_selection"])
        #
        # self.frame_top_controls.grid(**self.grid_args["frame_top_controls"])
        # self.frame_top_controls_a.grid(**self.grid_args["frame_top_controls_a"])
        # self.frame_top_controls_a_a.grid(**self.grid_args["frame_top_controls_a_a"])
        # self.frame_top_controls_b.grid(**self.grid_args["frame_top_controls_b"])

        # self.frame_hardware.grid(**self.grid_args["frame_hardware"])
        # self.frame_software.grid(**self.grid_args["frame_software"])
        # self.frame_comp_choice.grid(**self.grid_args["frame_comp_choice"])
        # self.frame_hardware_toggle_buttons.grid(**self.grid_args["frame_hardware_toggle_buttons"])

        # End Griding #

        # Begin Configurations #

        self.tb_same_user_as_for.state.trace_variable("w", self.update_who_for_me)
        self.tb_same_user_as_follow_up.state.trace_variable("w", self.update_follow_up_me)
        self.tv_comp_choice.trace_variable("w", self.update_comp_choice)
        self.tv_objective_choice.trace_variable("w", self.update_objective)
        self.tb_allow_hardware.state.trace_variable("w", self.update_allow_hardware)
        self.tb_allow_software.state.trace_variable("w", self.update_allow_software)
        self.frame_top_controls.columnconfigure([0, 1, 2], minsize=450)
        self.frame_top_controls.rowconfigure([0], minsize=150)

        # End Configurations #

    def na_if_none(self, val):
        if (val is None) or (not val and (isinstance(val, str) or isinstance(val, list) or isinstance(val, tuple) or isinstance(val, dict))):
            return "N/A"
        return val

    def update_objective(self, *args):
        val = self.tv_objective_choice.get()
        if val in self.list_of_objectives:
            print(f"{val=}\n{self.list_of_objectives[val]=}")
            obj = self.list_of_objectives[val]["obj"]
            data = self.form_data(val)

            kwargs = {
                "new_emp_name": data["new_emp_name"],
                "new_start_date": data["new_due_date"],
                "new_company": data["new_company"],
                "new_boss": data["new_boss"],
                "new_hardware": data["new_hardware"],
                "new_software": data["new_software"],
                "new_user_name": data["new_user_name"],
                "new_follow_up": data["new_follow_up"],
                "new_comments": data["new_comments"]
            }

            # msg = re.sub("\s+", ' ', obj.format(**kwargs))
            msg = obj.format(**kwargs)
            print(f"\n\tResult\n{msg}\n")

            self.tv_auto_desc_text.set(msg)

        else:
            # New objective
            pass
        print(f"objective='{val}'")

    def get_frame_hardware_toggles(self):
        result = []
        print(f"BEGIN get_frame_hardware_toggles: {result}")
        for q in self.questions_hardware:
            tb = self.questions_hardware[q]["tb"]
            print(f"{q=}, {tb=}, {tb.state.get()=}")
            if tb.state.get():
                result.append(q)
        print(f"END get_frame_hardware_toggles: {result}")
        return result

    def get_frame_software_toggles(self):
        result = []
        print(f"BEGIN get_frame_software_toggles: {result}")
        for q in self.questions_software:
            tb = self.questions_software[q]["tb"]
            print(f"{q=}, {tb=}, {tb.state.get()=}")
            if tb.state.get():
                result.append(q)
        print(f"END get_frame_software_toggles: {result}")
        return result

    def update_follow_up_me(self, *args):
        val = self.tb_same_user_as_follow_up.state.get()
        if val:
            self.mc_follow_up_selection.grid_forget()
            self.mc_follow_up_selection.res_tv_entry.set(self.tv_entry_user_name.get())
        else:
            self.mc_follow_up_selection.grid_widget()
            self.mc_follow_up_selection.grid(**self.grid_args["mc_follow_up_selection"])

    def update_who_for_me(self, *args):
        val = self.tb_same_user_as_for.state.get()
        if val:
            self.mc_emp_selection.grid_forget()
            self.mc_emp_selection.res_tv_entry.set(self.tv_entry_user_name.get())
        else:
            self.mc_emp_selection.grid_widget()
            self.mc_emp_selection.grid(**self.grid_args["mc_emp_selection"])

    def update_comp_choice(self, *args):
        val = self.tv_comp_choice.get()
        if val not in self.list_of_computers[:2]:
            for k in self.questions_hardware:
                # self.questions_hardware[k]["showing"] = False
                self.questions_hardware[k]["tb"].grid_forget()
        else:

            for k in self.questions_hardware:
                # if self.questions_hardware[k]["showing"]:
                grid_args = self.questions_hardware[k]["grid_args"]["tb"]
                self.questions_hardware[k]["tb"].grid(**grid_args)

            show_chargers = True
            showing_chargers = self.questions_hardware["extra chargers"]["showing"]
            match val:
                case "Desktop":
                    # hide charger + dock question for desktop users
                    show_chargers = False
            if show_chargers:
                if not showing_chargers:
                    # self.questions_hardware["extra chargers"]["tb"].grid_widgets()
                    self.questions_hardware["extra chargers"]["tb"].grid(**self.questions_hardware["extra chargers"]["grid_args"]["tb"])
                    self.questions_hardware["extra chargers"]["showing"] = True

                    self.questions_hardware["dock"]["tb"].grid(**self.questions_hardware["dock"]["grid_args"]["tb"])
                    self.questions_hardware["dock"]["showing"] = True
            else:
                if showing_chargers:
                    self.questions_hardware["extra chargers"]["tb"].grid_forget()
                    self.questions_hardware["extra chargers"]["showing"] = False

                    self.questions_hardware["dock"]["tb"].grid_forget()
                    self.questions_hardware["dock"]["showing"] = False

            self.frame_hardware_toggle_buttons.grid(**self.grid_args["frame_hardware_toggle_buttons"])

    def update_allow_hardware(self, *args):
        """When hardware switch is clicked, update showing section"""
        allow = self.tb_allow_hardware.state.get()
        if allow:
            self.show_hardware_section()
        else:
            self.hide_hardware_section()

    def update_allow_software(self, *args):
        """When software switch is clicked, update showing section"""
        allow = self.tb_allow_software.state.get()
        if allow:
            self.show_software_section()
        else:
            self.hide_software_section()

    def show_hardware_section(self):
        self.frame_comp_choice.grid(**self.grid_args["frame_comp_choice"])
        self.frame_hardware_toggle_buttons.grid(**self.grid_args["frame_hardware_toggle_buttons"])

    def hide_hardware_section(self):
        self.frame_comp_choice.grid_forget()
        self.frame_hardware_toggle_buttons.grid_forget()

    def show_software_section(self):
        self.frame_software_toggle_buttons.grid(**self.grid_args["frame_software_toggle_buttons"])

    def hide_software_section(self):
        self.frame_software_toggle_buttons.grid_forget()

    def click_open_comments(self, *event):
        print(f"click_open_comments")
        r, c, rs, cs, ix, iy, x, y, s = self.grid_keys()
        if self.tl_comments_input is None:
            self.tl_comments_input = tkinter.Toplevel(self)
            self.tl_comments_input.title("Edit Comments")
            self.tl_frame_comments_btns = tkinter.Frame(self.tl_comments_input)
            self.tl_tv_label_text_comments, \
            self.tl_label_text_comments, \
            self.tl_tv_text_comments, \
            self.tl_text_comments \
                = text_factory(
                self.tl_comments_input,
                tv_label="Enter Comments:",
                tv_text=self.tl_tv_text_comments
            )
            self.tl_tv_btn_submit_comment, \
            self.tl_btn_submit_comment \
                = button_factory(
                self.tl_frame_comments_btns,
                tv_btn="submit",
                kwargs_btn={
                    "command": self.tl_click_submit_comments
                }
            )
            self.tl_tv_btn_cancel_comment, \
            self.tl_btn_cancel_comment \
                = button_factory(
                self.tl_frame_comments_btns,
                tv_btn="cancel",
                kwargs_btn={
                    "command": self.tl_click_cancel_comments
                }
            )
            self.tl_tv_btn_clear_comment, \
            self.tl_btn_clear_comment \
                = button_factory(
                self.tl_frame_comments_btns,
                tv_btn="clear",
                kwargs_btn={
                    "command": self.tl_click_clear_comments
                }
            )
            self.tl_tv_btn_undo_comment, \
            self.tl_btn_undo_comment \
                = button_factory(
                self.tl_frame_comments_btns,
                tv_btn="undo",
                kwargs_btn={
                    "command": self.tl_click_undo_comments
                }
            )

            print(f"TEST '{self.test_id == id(self.tl_text_comments.text)}'")

            # self.tl_label_text_comments.grid(**{r: 0, c: 0, cs: 4})
            self.tl_text_comments.grid(**{r: 1, c: 2, cs: 4})
            self.tl_frame_comments_btns.grid(**{r: 2, c: 0, cs: 4})
            self.tl_btn_submit_comment.grid(**{r: 0, c: 0})
            # self.tl_btn_undo_comment.grid(**{r: 0, c: 1})  # TODO fix the undo function.
            self.tl_btn_clear_comment.grid(**{r: 0, c: 2})
            self.tl_btn_cancel_comment.grid(**{r: 0, c: 3})

            self.tl_comments_input.protocol("WM_DELETE_WINDOW", self.tl_close_comments)
            # self.wait_window(self.tl_comments_input)
            # self.tl_comments_input.wait_window()
            self.tl_comments_input.grab_set()
        else:
            print(f"Cant open another top level before closing the previous.")

    def tl_close_comments(self, *event):
        print(f"close_tl_comments")
        self.tl_comments_input.destroy()
        self.tl_comments_input = None

    def tl_click_submit_comments(self, *event):
        print(f"click_submit_comments")
        self.tl_close_comments(event)

    def tl_click_cancel_comments(self, *event):
        print(f"click_cancel_comments")
        ans = messagebox.askokcancel("Quit?", "Aru you sure you want to exit without saving?")
        if ans:
            self.tl_close_comments(event)

    def tl_click_clear_comments(self, *event):
        print(f"click_clear_comments")
        self.tl_tv_text_comments.set("")

    def tl_click_undo_comments(self, *event):
        print(f"click_undo_comments")
        self.tl_text_comments.undo()

    def flag_open_software(self):
        """Call this whenever an internal software switch needs to be shown.
        Ensures that toggle_buttons_frame is visible"""
        if not self.tb_allow_software.state.get():
            self.tb_allow_software.click()

    def flag_open_hardware(self):
        """Call this whenever an internal hardware switch needs to be shown.
        Ensures that toggle_buttons_frame is visible"""
        if not self.tb_allow_hardware.state.get():
            self.tb_allow_hardware.click()

    def flag_odbc(self, state=None):
        # set odbc flag
        self.flag_helper("software", "odbc", state)

    def flag_outlook(self, state=None):
        # set outlook flag
        self.flag_helper("software", "outlook email", state)

    def flag_outlook_archive(self, state=None):
        self.flag_helper("software", "outlook archive", state)

    def flag_g_drive(self, state=None):
        self.flag_helper("software", "g-drive public", state)

    def flag_u_drive(self, state=None):
        self.flag_helper("software", "u-drive private", state)

    def flag_helper(self, sh, k, state):
        if sh == "software":
            tb = self.questions_software[k]["tb"]
        else:
            tb = self.questions_hardware[k]["tb"]
        if state is None:
            tb.click()
            state = tb.state.get()
        else:
            s = tb.state.get()
            if state and not s:
                tb.click()
            elif not state and s:
                tb.click()
        if state:
            if sh == "software":
                self.flag_open_software()
            else:
                self.flag_open_hardware()

    def click_submit_form(self, *event):
        print(f"click_submit_form")
        if data := self.ready_to_submit():
            print(f"{data=}")

    def form_data(self, key=None):
        if key is not None:
            if key not in self.list_of_objectives:
                raise KeyError(f"Error, key '{key}' is not in the list of objectives.")

            full_obj = self.list_of_objectives[key]
            obj = full_obj["obj"]
            flags = full_obj["flags"]
            flags_auto = flags["auto"]
            flags_other = flags["other"]

            for k, flags_list in flags_auto.items():
                if k:
                    for flag in flags_list:
                        self.flags[flag]()

            new_user_name = self.na_if_none(self.tv_entry_user_name.get())
            new_emp_name = self.na_if_none(self.mc_emp_selection.res_tv_entry.get())
            date = self.odp.date
            start_hour, \
            start_minute = \
                self.default_data["start_of_day_hour"], \
                self.default_data["start_of_day_minute"]
            date = datetime.datetime(date.year, date.month, date.day, start_hour, start_minute)
            date_s = date_str_format(date, include_time=True)
            new_due_date = self.na_if_none(date_s)
            new_company = self.na_if_none(self.tv_company_choice.get())
            new_hardware = self.na_if_none(self.get_frame_hardware_toggles())
            new_software = self.na_if_none(self.get_frame_software_toggles())
            new_follow_up = self.na_if_none(self.mc_follow_up_selection.res_tv_entry.get())
            new_boss = self.na_if_none(None)

            if self.tl_text_comments is not None:
                new_comments = self.na_if_none(self.tl_text_comments.text.get())
            else:
                new_comments = self.na_if_none(None)

            data = {
                "flags": flags,
                "flags_auto": flags_auto,
                "flags_other": flags_other,
                "new_user_name": new_user_name,
                "new_emp_name": new_emp_name,
                "new_due_date": new_due_date,
                "new_follow_up": new_follow_up,
                "new_hardware": new_hardware,
                "new_software": new_software,
                "new_comments": new_comments,
                "new_company": new_company,
                "new_boss": new_boss
            }
            print(f"{dict_print(data, 'Data')}")

            return data
        return {}

    def ready_to_submit(self):
        val = self.tv_objective_choice.get()
        data = self.form_data(val)
        if all([val, *list(data.items())]):
            return data
        return {}

    def grid_keys(self):
        return "row", "column", "rowspan", "columnspan", "ipadx", "ipady", "padx", "pady", "sticky"


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
    # frame_hardware_toggle_buttons = tkinter.Frame(win, background=random_colour(rgb=False))
    # for q_title, q_data in questions_hardware.items():
    #     q_text, q_follow_up, q_var = list(q_data.values())
    #     tb, label_data, \
    #     frame_canvas, btn_data,\
    #     quantity_data = \
    #         ToggleButtonQuantity(
    #             frame_hardware_toggle_buttons,
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
    # frame_hardware_toggle_buttons.grid()
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

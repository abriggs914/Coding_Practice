import tkinter
from tkinter import messagebox

import customtkinter as ctk
import pandas as pd
from CTkTable import CTkTable
from colour_utility import *
from datetime_utility import date_str_format, is_date
from pyodbc_connection import connect
from tkinter_utility import calc_geometry_tl
from customtkinter_utility import CtkTableExt, CtkEntryDate, CTkTable
from utility import get_windows_user


class App(ctk.CTk):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.title_app_long = f"IT Request Maintenance"
        self.title_app_short = f"IT Request Maintenance"
        self.text_sw_all_follow_up = ""
        self.user_windows_name = get_windows_user(2).split("\\")[-1]
        self.user_full_name = get_windows_user(2).split("\\")[-1]
        self.allow_list_edits = False

        self.default_cb_width = 120
        self.default_cb_height = 25
        self.default_cb_corner_radius = 10
        self.default_cb_justify = ctk.CENTER

        self.colour_default_cb_bg_colour = Colour("#69A3C3")
        self.colour_default_cb_fg_colour = Colour("#092373")
        self.colour_default_cb_border_colour = Colour("#092373")
        self.colour_default_cb_dropdown_fg_color = self.colour_default_cb_fg_colour.brightened(0.05)
        self.colour_default_table_header = Colour("#12A5FF")

        self.sql_template_sp_predict_labour = """EXEC [sp_ITREstimateLabour] @company={A}, @department={B}, @requestType={C}, @requestSubType={D};"""
        self.sql_df_requests = {
            "sql": "[IT Requests]"
        }
        self.sql_df_customers = {
            "sql": """
SELECT
	[Company] AS [Comp]
	,[Department] AS [Dept]
	,[C].[Employee Name] AS [Name],
	*
FROM
	[v_ITRCustomersWithDepartments] [C]
;
"""
        }
        self.sql_df_departments = {
            "sql": """
SELECT
    MIN(Dept.DeptID) AS [MinOfDeptID],
    [Dept].[Dept]
FROM
    [Dept]
GROUP BY
    [Dept].[Dept] 
HAVING
    [Dept].[Dept]<>''
;
"""
        }
        self.sql_df_hardware = {
            "sql": "[ITR Hardware]"
        }
        self.sql_df_software = {
            "sql": "[ITR Software]"
        }
        self.sql_df_training = {
            "sql": "[ITR Training]"
        }
        self.df_requests: pd.DataFrame = None
        self.df_customers: pd.DataFrame = None
        self.df_departments: pd.DataFrame = None
        self.df_req_hardware: pd.DataFrame = None
        self.df_req_software: pd.DataFrame = None
        self.df_req_training: pd.DataFrame = None
        self.load_dfs()

        self.list_companies = [
            "BWS",
            "STG",
            "HUGO",
            "LEWIS"
        ]
        if self.df_departments is None:
            self.list_departments = [
                "IT",
                "Admin",
                "Sales",
                "Warranty",
                "Production",
                "Parts",
                "Engineering",
                "Finish Off"
            ]
        else:
            self.list_departments = sorted(self.df_departments["Dept"].values.tolist())
        if any([
            self.df_req_hardware is None,
            self.df_req_software is None,
            self.df_req_training is None
        ]):
            self.dict_req_types = {
                "Hardware": [
                    "Hardware_a",
                    "Hardware_b",
                    "Hardware_c",
                    "Hardware_d",
                    "Hardware_e",
                    "Hardware_f",
                    "Hardware_g",
                ],
                "Software": [
                    "Software_a",
                    "Software_b",
                    "Software_c",
                    "Software_d",
                    "Software_e",
                    "Software_f",
                    "Software_g"
                ],
                "Training": [
                    "Training_a",
                    "Training_b",
                    "Training_c",
                    "Training_d",
                    "Training_e",
                    "Training_f",
                    "Training_g"
                ]
            }
        else:
            self.dict_req_types = {
                k: df[k].values.tolist()
                for k, df in zip(
                    ["Hardware", "Software", "Training"],
                    [self.df_req_hardware, self.df_req_software, self.df_req_training]
                )
            }
        self.list_req_types = list(self.dict_req_types)
        self.list_req_sub_types = []
        self.list_priorities = list(range(1, 12))
        self.header_follow_up = ["Comp", "Dept", "Name"]
        if self.df_customers is None:
            self.data_follow_up = [
                self.header_follow_up,
                ["BWS", "IT", "Avery"],
                ["BWS", "IT", "James"],
                ["BWS", "IT", "Jamie"],
                ["BWS", "Sales", "Shelley"],
                ["BWS", "Purchasing", "Lori"],
                ["BWS", "Production", "Lance"],
                ["BWS", "Production", "Lester"],
                ["BWS", "Sales", "Jason"],
                ["BWS", "Purchasing", "Jason"]
            ]
        else:
            self.data_follow_up = [
                self.header_follow_up,
                *self.df_customers[self.header_follow_up].values.tolist()
            ]
        self.og_table_follow_up_values = [[v for v in row] for row in self.data_follow_up]
        self.data_rev_follow_up = {k: None for k in self.header_follow_up}
        self.header_predict_labour = ["", "Average", "Total", "# Requests", ""]
        self.data_predict_labour = [self.header_predict_labour] + [["" for _ in range(4)] for _ in range(2)]
        self.data_predict_labour[1][0] = "Actual"
        self.data_predict_labour[2][0] = "Budget"
        self.data_predict_labour[1][3] = "% Total Requests"
        self.data_predict_labour[2][3] = "% Total Budget"

        self.c_cb_new = "+"
        if self.allow_list_edits:
            for lst in (
                self.list_companies,
                self.list_departments,
                self.list_req_types,
                self.list_req_sub_types
            ):
                lst.append(self.c_cb_new)

        # ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        # self.pack_propagate(False)
        self.geometry(calc_geometry_tl(0.6, 0.3))
        # self.state("zoomed")
        self.title(self.title_app_long)

        self.default_cb_config = {
            "bg_color": self.colour_default_cb_bg_colour.hex_code,
            "fg_color": self.colour_default_cb_fg_colour.hex_code,
            "border_color": self.colour_default_cb_border_colour.hex_code,
            "dropdown_fg_color": self.colour_default_cb_dropdown_fg_color.hex_code,
            "corner_radius": self.default_cb_corner_radius,
            "width": self.default_cb_width,
            "height": self.default_cb_height,
            "justify": self.default_cb_justify
        }
        self.default_tb_config = {
            "width": 400,
            "height": 175,
            "font": ("Calibri", 16)
        }
        self.default_btn_config = {
        }
        self.default_lbl_config = {
            "font": ("Calibri", 18, "bold")
        }

        # frames
        self.f_controls_a = ctk.CTkFrame(self)
        self.f_controls_b = ctk.CTkFrame(self)
        self.f_controls_c = ctk.CTkFrame(self)
        self.f_controls_d = ctk.CTkFrame(self)
        self.f_labour_est = ctk.CTkFrame(self.f_controls_a)
        self.f_control_btns = ctk.CTkFrame(self.f_controls_d)

        # vars
        self.v_lbl_dp_due_date = ctk.StringVar(self, value=f"Due Date:")
        self.v_lbl_cb_company = ctk.StringVar(self, value=f"Company:")
        self.v_lbl_cb_department = ctk.StringVar(self, value=f"Department:")
        self.v_lbl_cb_req_type = ctk.StringVar(self, value=f"Requesting help with:")
        self.v_lbl_cb_req_sub_type = ctk.StringVar(self, value=f"Specifically:")
        self.v_lbl_tb_request = ctk.StringVar(self, value=f"Request:")
        self.v_lbl_tb_comment = ctk.StringVar(self, value=f"Comments:")
        self.v_lbl_table_follow_up = ctk.StringVar(self, value=f"Request follow-up personnel:")
        self.v_lbl_s_priority = ctk.StringVar(self, value=f"Priority:")

        self.v_lbl_sw_submit_request = ctk.StringVar(self, value=f"Submit Requests?")
        self.v_sw_submit_request = ctk.StringVar(self)
        self.v_lbl_sw_mark_complete = ctk.StringVar(self, value=f"Mark Complete?")
        self.v_sw_mark_complete = ctk.StringVar(self)

        self.v_btn_date_stamp_request = ctk.StringVar(self, value="Date Stamp")
        self.v_btn_date_stamp_comment = ctk.StringVar(self, value="Date Stamp")

        self.v_btn_clear_fields = ctk.StringVar(self, value=f"Clear Fields")
        self.v_btn_go_back = ctk.StringVar(self, value=f"Go Back")
        self.v_btn_submit = ctk.StringVar(self, value=f"Submit")

        self.v_cb_department = ctk.StringVar(self, name="request_department")
        self.v_cb_company = ctk.StringVar(self, name="request_company")
        self.v_cb_req_type = ctk.StringVar(self, name="request_type")
        self.v_cb_req_sub_type = ctk.StringVar(self, name="request_sub_type")
        self.v_s_priority = ctk.IntVar(self, name="request_priority")
        self.v_table_selected_rows = list()
        self.tv_sw_all_follow_up = ctk.StringVar(self, name="switch_all_follow_up", value=self.text_sw_all_follow_up)

        # widgets
        self.sw_submit_requests = ctk.CTkSwitch(
            self.f_controls_a,
            textvariable=self.v_lbl_sw_submit_request,
            variable=self.v_sw_submit_request
        )
        self.sw_mark_complete = ctk.CTkSwitch(
            self.f_controls_a,
            textvariable=self.v_lbl_sw_mark_complete,
            variable=self.v_sw_mark_complete
        )

        self.lbl_dp_due_date = ctk.CTkLabel(
            self.f_controls_b,
            textvariable=self.v_lbl_dp_due_date,
            **self.default_lbl_config
        )
        self.dp_due_date = CtkEntryDate(
            self.f_controls_b
        )

        self.lbl_cb_company = ctk.CTkLabel(
            self.f_controls_b,
            textvariable=self.v_lbl_cb_company,
            **self.default_lbl_config
        )
        self.cb_company = ctk.CTkComboBox(
            master=self.f_controls_b,
            values=self.list_companies,
            command=self.update_cb_company,
            variable=self.v_cb_company,
            **self.default_cb_config
        )
        self.lbl_cb_department = ctk.CTkLabel(
            self.f_controls_b,
            textvariable=self.v_lbl_cb_department,
            **self.default_lbl_config
        )
        self.cb_department = ctk.CTkComboBox(
            master=self.f_controls_b,
            values=self.list_departments,
            command=self.update_cb_department,
            variable=self.v_cb_department,
            **self.default_cb_config
        )
        self.lbl_cb_req_type = ctk.CTkLabel(
            self.f_controls_b,
            textvariable=self.v_lbl_cb_req_type,
            **self.default_lbl_config
        )
        self.cb_req_type = ctk.CTkComboBox(
            master=self.f_controls_b,
            values=self.list_req_types,
            command=self.update_cb_req_type,
            variable=self.v_cb_req_type,
            **self.default_cb_config
        )
        self.lbl_cb_req_sub_type = ctk.CTkLabel(
            self.f_controls_b,
            textvariable=self.v_lbl_cb_req_sub_type,
            **self.default_lbl_config
        )
        self.cb_req_sub_type = ctk.CTkComboBox(
            master=self.f_controls_b,
            values=self.list_req_sub_types,
            command=self.update_cb_req_sub_type,
            variable=self.v_cb_req_sub_type,
            **self.default_cb_config
        )

        self.lbl_tb_request = ctk.CTkLabel(
            self.f_controls_c,
            textvariable=self.v_lbl_tb_request,
            **self.default_lbl_config
        )
        self.btn_date_stamp_request = ctk.CTkButton(
            self.f_controls_c,
            textvariable=self.v_btn_date_stamp_request,
            command=self.click_date_stamp_request,
            **self.default_btn_config
        )
        self.tb_request_text = ctk.CTkTextbox(
            self.f_controls_c,
            **self.default_tb_config
        )
        self.lbl_tb_comment = ctk.CTkLabel(
            self.f_controls_c,
            textvariable=self.v_lbl_tb_comment,
            **self.default_lbl_config
        )
        self.btn_date_stamp_comment = ctk.CTkButton(
            self.f_controls_c,
            textvariable=self.v_btn_date_stamp_comment,
            command=self.click_date_stamp_comment,
            **self.default_btn_config
        )
        self.tb_comment_text = ctk.CTkTextbox(
            self.f_controls_c,
            **self.default_tb_config
        )

        # self.table_follow_up = CTkTable(
        #     master=self.f_bottom_controls,
        #     header_color="#019822",
        #     values=self.data_follow_up,
        #     command=self.update_table_follow_up
        # )

        self.lbl_table_follow_up = ctk.CTkLabel(
            self.f_controls_d,
            textvariable=self.v_lbl_table_follow_up,
            **self.default_lbl_config
        )
        self.table_follow_up = CtkTableExt(
            master=self.f_controls_d,
            table_data=self.data_follow_up,
            width=450,
            kwargs_table={
                "header_color": "#019822",
                "command": self.update_table_follow_up
            }
        )

        self.lbl_s_priority = ctk.CTkLabel(
            self.f_controls_d,
            textvariable=self.v_lbl_s_priority,
            **self.default_lbl_config
        )
        self.s_priority = ctk.CTkSlider(
            master=self.f_controls_d,
            from_=self.list_priorities[0],
            to=self.list_priorities[-1],
            number_of_steps=(self.list_priorities[-1] - self.list_priorities[0]),
            variable=self.v_s_priority,
            command=self.update_sl_priority
        )

        self.btn_clear_fields = ctk.CTkButton(
            self.f_control_btns,
            textvariable=self.v_btn_clear_fields,
            command=self.click_clear_fields,
            **self.default_btn_config
        )

        self.btn_go_back = ctk.CTkButton(
            self.f_control_btns,
            textvariable=self.v_btn_go_back,
            command=self.click_go_back,
            **self.default_btn_config
        )

        self.btn_submit = ctk.CTkButton(
            self.f_control_btns,
            textvariable=self.v_btn_submit,
            command=self.click_submit,
            **self.default_btn_config
        )

        self.table_predict_labour = CTkTable(
            self.f_labour_est,
            values=self.data_predict_labour
            # ,            header_color=self.colour_default_table_header.hex_code
        )
        self.select_legend_cols_predict_labour()

        self.v_s_labour_est_is_large = ctk.BooleanVar(self)
        self.v_s_labour_est_is_neg = ctk.BooleanVar(self)
        self.v_s_labour_est = ctk.DoubleVar(self)
        self.s_labour_est = ctk.CTkSlider(
            self.f_labour_est,
            from_=0,
            to=2,
            number_of_steps=20,
            variable=self.v_s_labour_est
        )
        self.list_v_sb_labour_est_is_large = [["0 - 2.5 H", "2.5 H+"], [0, 2.5, 20], [2.5, 30, 60]]
        self.sb_labour_ext_is_large = ctk.CTkSegmentedButton(
            self.f_labour_est,
            values=self.list_v_sb_labour_est_is_large[0],
            command=self.update_labour_est_is_large
        )
        self.list_v_sb_labour_est_is_neg = ["-", "+"]
        self.sb_labour_ext_is_neg = ctk.CTkSegmentedButton(
            self.f_labour_est,
            values=self.list_v_sb_labour_est_is_neg,
            command=self.update_labour_est_is_neg
        )
        self.sb_labour_ext_is_large.set(self.list_v_sb_labour_est_is_large[0][0])
        self.sb_labour_ext_is_neg.set(self.list_v_sb_labour_est_is_neg[1])

        # self.sw_all_follow_up = ctk.CTkSwitch(
        #     master=self.f_controls_a,
        #     textvariable=self.tv_sw_all_follow_up
        #
        # )

        self.f_controls_a.grid(row=0, column=0, rowspan=1, columnspan=1, sticky=tkinter.NSEW)
        self.f_controls_b.grid(row=1, column=0, rowspan=1, columnspan=1, sticky=tkinter.NSEW)
        self.f_controls_c.grid(row=2, column=0, rowspan=1, columnspan=1, sticky=tkinter.NSEW)
        self.f_controls_d.grid(row=3, column=0, rowspan=1, columnspan=1, sticky=tkinter.NSEW)

        # self.f_controls_a
        self.sw_submit_requests.grid(row=0, column=0, rowspan=1, columnspan=1)
        self.sw_mark_complete.grid(row=1, column=0, rowspan=1, columnspan=1)
        self.f_labour_est.grid(row=0, column=1, rowspan=2, columnspan=1)

        # self.f_controls_b
        self.lbl_dp_due_date.grid(row=0, column=0, rowspan=1, columnspan=1, sticky=tkinter.NSEW)
        self.dp_due_date.grid(row=0, column=1, rowspan=1, columnspan=1, sticky=tkinter.NSEW)
        self.lbl_cb_company.grid(row=1, column=0, rowspan=1, columnspan=1, sticky=tkinter.NSEW)
        self.cb_company.grid(row=1, column=1, rowspan=1, columnspan=1, sticky=tkinter.NSEW)
        self.lbl_cb_department.grid(row=2, column=0, rowspan=1, columnspan=1, sticky=tkinter.NSEW)
        self.cb_department.grid(row=2, column=1, rowspan=1, columnspan=1, sticky=tkinter.NSEW)
        self.lbl_cb_req_type.grid(row=1, column=2, rowspan=1, columnspan=1, sticky=tkinter.NSEW)
        self.cb_req_type.grid(row=1, column=3, rowspan=1, columnspan=1, sticky=tkinter.NSEW)
        self.lbl_cb_req_sub_type.grid(row=2, column=2, rowspan=1, columnspan=1, sticky=tkinter.NSEW)
        self.cb_req_sub_type.grid(row=2, column=3, rowspan=1, columnspan=1, sticky=tkinter.NSEW)

        # self.f_controls_c
        self.lbl_tb_request.grid(row=0, column=0, rowspan=1, columnspan=1, sticky=tkinter.NSEW)
        self.btn_date_stamp_request.grid(row=0, column=1, rowspan=1, columnspan=1, sticky=tkinter.NSEW)
        self.tb_request_text.grid(row=1, column=0, rowspan=1, columnspan=2, sticky=tkinter.NSEW)
        self.lbl_tb_comment.grid(row=0, column=2, rowspan=1, columnspan=1, sticky=tkinter.NSEW)
        self.btn_date_stamp_comment.grid(row=0, column=3, rowspan=1, columnspan=1, sticky=tkinter.NSEW)
        self.tb_comment_text.grid(row=1, column=2, rowspan=1, columnspan=2, sticky=tkinter.NSEW)

        # self.f_controls_d
        self.lbl_table_follow_up.grid(row=0, column=0, rowspan=1, columnspan=1, sticky=tkinter.NSEW)
        self.table_follow_up.grid(row=1, column=0, rowspan=1, columnspan=1, sticky=tkinter.NSEW)
        self.lbl_s_priority.grid(row=0, column=1, rowspan=1, columnspan=1)
        self.s_priority.grid(row=1, column=1, rowspan=1, columnspan=1)
        self.f_control_btns.grid(row=0, column=4, rowspan=1, columnspan=1, sticky=tkinter.NSEW)

        # self.f_control_btns
        self.btn_clear_fields.grid(row=0, column=0, rowspan=1, columnspan=1)
        self.btn_go_back.grid(row=1, column=0, rowspan=1, columnspan=1)
        self.btn_submit.grid(row=2, column=0, rowspan=1, columnspan=1)

        # self.f_labour_est
        self.table_predict_labour.grid(row=0, column=0, rowspan=1, columnspan=3)
        self.sb_labour_ext_is_neg.grid(row=1, column=0, rowspan=1, columnspan=1)
        self.sb_labour_ext_is_large.grid(row=1, column=1, rowspan=1, columnspan=1)
        self.s_labour_est.grid(row=1, column=2, rowspan=1, columnspan=1)

        # bindings
        self.v_s_labour_est_is_large.trace_variable("w", self.update_v_labour_est_is_large)
        self.v_s_labour_est_is_neg.trace_variable("w", self.update_v_labour_est_is_neg)

        # call init functions
        self.update_predict_labour()

    def department_name_to_id(self, department) -> None | int:
        dfd = self.df_departments
        df: pd.DataFrame = dfd.loc[dfd["Dept"].str.lower() == department.lower()]
        if df.empty:
            return
        else:
            return df.iloc[0]["MinOfDeptID"]

    def select_legend_cols_predict_labour(self):
        self.table_predict_labour.select(0, 0)
        self.table_predict_labour.select(0, 1)
        self.table_predict_labour.select(0, 2)
        self.table_predict_labour.select(0, 3)
        self.table_predict_labour.select_column(0)
        self.table_predict_labour.select_column(3)

    def get_field_company(self):
        return self.v_cb_company.get().strip().replace("'", "''").removesuffix(";").upper()

    def get_field_due_date(self):
        return self.dp_due_date.var_date_picker.get().strip().replace("'", "''").removesuffix(";")

    def get_field_department(self):
        return self.v_cb_department.get().strip().replace("'", "''").removesuffix(";")

    def get_field_req_type(self):
        return self.v_cb_req_type.get().strip().replace("'", "''").removesuffix(";")

    def get_field_req_sub_type(self):
        return self.v_cb_req_sub_type.get().strip().replace("'", "''").removesuffix(";")

    def get_field_request_text(self):
        return self.tb_request_text.get("0.0", tkinter.END).strip().replace("'", "''").removesuffix(";")

    def get_field_comment_text(self):
        return self.tb_comment_text.get("0.0", tkinter.END).strip().replace("'", "''").removesuffix(";")

    def get_field_priority(self):
        return self.v_s_priority.get()

    def get_field_labour_est(self):
        return self.v_s_labour_est.get()

    def update_labour_est_is_large(self, is_large):
        self.v_s_labour_est_is_large.set(is_large == self.list_v_sb_labour_est_is_large[0][1])

    def update_labour_est_is_neg(self, is_neg):
        self.v_s_labour_est_is_neg.set(is_neg == self.list_v_sb_labour_est_is_neg[0])

    def update_v_labour_est_is_neg(self, *args):
        print(f"update_v_labour_est_is_neg")

    def update_v_labour_est_is_large(self, *args):
        """trace variable"""
        is_large = self.v_s_labour_est_is_large.get()
        if is_large:
            values = self.list_v_sb_labour_est_is_large[2]
        else:
            values = self.list_v_sb_labour_est_is_large[1]

        self.s_labour_est.configure(
            from_=values[0],
            to=values[1],
            number_of_steps=values[2]
        )
        self.v_s_labour_est.set(clamp(values[0], self.v_s_labour_est.get(), values[1]))

    def update_predict_labour(self):
        company = self.get_field_company()
        department = self.get_field_department()
        req_type = self.get_field_req_type()
        req_sub_type = self.get_field_req_sub_type()
        department_id = self.department_name_to_id(department)

        sql = self.sql_template_sp_predict_labour

        print(f"{company=}, {department=}, {department_id=}, {req_type=}, {req_sub_type=}")
        if company:
            sql = sql.format(A=f"'{company}'", B="{B}", C="{C}", D="{D}")
        if department_id:
            sql = sql.format(B=department_id, A="{A}", C="{C}", D="{D}")
        if req_type:
            sql = sql.format(C=f"'{req_type}'", A="{A}", B="{B}", D="{D}")
        if req_sub_type:
            sql = sql.format(D=f"'{req_sub_type}'", A="{A}", B="{B}", C="{C}")

        sql = sql.format(A="NULL", B="NULL", C="NULL", D="NULL")
        print(f"{sql=}")
        df = connect(sql)
        if not df.empty:
            row = df.iloc[0]
            self.table_predict_labour.insert(0, 4, row["# Reqs"])
            self.table_predict_labour.insert(1, 1, row["Act / Req"])
            self.table_predict_labour.insert(2, 1, row["Bud / Req"])
            self.table_predict_labour.insert(1, 2, row["Act"])
            self.table_predict_labour.insert(2, 2, row["Bud"])
            self.table_predict_labour.insert(1, 4, row["% Ttl Reqs"])
            self.table_predict_labour.insert(2, 4, row["% Total Bud"])

    def update_cb_department(self, department):
        print(f"update_cb_department {department=}")
        if department == self.c_cb_new:
            print(f"Add new department")
        self.update_predict_labour()

    def update_cb_company(self, company):
        print(f"update_cb_company {company=}")
        if company == self.c_cb_new:
            print(f"Add new company")
        self.update_predict_labour()

    def update_cb_req_type(self, req_type):
        print(f"update_cb_req_type {req_type=}")
        if req_type == self.c_cb_new:
            print(f"Add new req_type")
        else:
            self.cb_req_sub_type.values = self.dict_req_types[req_type]
            self.cb_req_sub_type.configure(values=self.dict_req_types[req_type])
            self.v_cb_req_sub_type.set("")
        self.update_predict_labour()

    def update_cb_req_sub_type(self, re_sub_type):
        print(f"update_cb_req_sub_type {re_sub_type=}")
        if re_sub_type == self.c_cb_new:
            print(f"Add new re_sub_type")
        self.update_predict_labour()

    def update_sl_priority(self, priority):
        print(f"update_s_priority {priority=}")

    def update_sw_all_follow_up(self, new_val):
        print(f"update_sw_all_follow_up {new_val=}")

    def update_table_follow_up(self, data_follow_up):
        print(f"update_table_follow_up {data_follow_up=}")
        # self.unselect_follow_up_table_rows()
        # t_values = self.table_follow_up.values
        # print(f"{t_values=}")
        # row = data_follow_up.get("row")
        # col = data_follow_up.get("column")
        # val = data_follow_up.get("value")
        # args = data_follow_up.get("args")
        # if row == 0:
        #     self.sort_follow_up_table(row, col)
        # else:
        #     follow_up_name = t_values[row][self.header_follow_up.index("Name")]
        #     print(f"{follow_up_name=}")
        #     self.table_follow_up.select_row(row)
        #     self.v_table_selected_rows.append(row)

    def click_date_stamp_request(self):
        print(f"click_date_stamp_request")
        text = self.tb_request_text.get("0.0", ctk.END).strip()
        text += "\n" if text else ""
        # text += f"{datetime.datetime.now():%Y-%m-%d} -- {self.user_windows_name}: "
        str_time = date_str_format(datetime.datetime.now(), include_time=True)
        text += f"{str_time} -- {self.user_windows_name}: "
        self.tb_request_text.delete("0.0", ctk.END)
        self.tb_request_text.insert("0.0", text)

    def click_date_stamp_comment(self):
        print(f"click_date_stamp_comment")
        text = self.tb_comment_text.get("0.0", ctk.END).strip()
        text += "\n" if text else ""
        # text += f"{datetime.datetime.now():%Y-%m-%d} -- {self.user_windows_name}: "
        str_time = date_str_format(datetime.datetime.now(), include_time=True)
        text += f"{str_time} -- {self.user_windows_name}: "
        self.tb_comment_text.delete("0.0", ctk.END)
        self.tb_comment_text.insert("0.0", text)

    def click_clear_fields(self):
        print(f"click_clear_fields")
        # due_date = self.dp_due_date.var_date_picker.set()
        self.v_cb_company.set("")
        self.v_cb_department.set("")
        self.v_cb_req_type.set("")
        self.v_cb_req_sub_type.set("")
        self.tb_request_text.insert("0.0", "")
        self.tb_comment_text.insert("0.0", "")
        # req_follow_up = self.table_follow_up.selection_get()
        # if self.table_follow_up.sortable:
        #     self.table_follow_up.table.clear_selected_rows()
        #     self.table_follow_up.table.clear_selected_cols()
        self.table_follow_up.clear_all_selected()
        if self.table_follow_up.searchable:
            self.table_follow_up.clear_search_idxs()

        self.v_s_priority.get()

    def click_go_back(self):
        print(f"click_go_back")

    def focus_widget(self, widget, msg):
        messagebox.showinfo(
            title=self.title_app_short,
            message=msg
        )
        widget.focus()

    def click_submit(self):
        print(f"click_submit")

        # due_date = self.dp_due_date.selection_get()
        # due_date = self.dp_due_date.date
        # due_date = self.dp_due_date.var_date_picker.get()
        due_date = self.get_field_due_date()
        company = self.get_field_company()
        department = self.get_field_department()
        req_type = self.get_field_req_type()
        req_sub_type = self.get_field_req_sub_type()
        request_text = self.get_field_request_text()
        comment_text = self.get_field_comment_text()
        # req_follow_up = self.table_follow_up.selection_get()
        req_follow_up = self.table_follow_up.table.get_selected_row()
        priority = self.get_field_priority()
        o_due_date = due_date
        labour_est = self.get_field_labour_est()

        print(f"{due_date=}\n{company=}\n{department=}\n{req_type=}\n{req_sub_type=}\n{request_text=}\n{comment_text=}\n{req_follow_up=}\n{priority=}")

        for val, widget, msg in (
            (due_date, self.dp_due_date.entry, f"Enter a due date first."),
            (company, self.cb_company, f"Select a company first."),
            (department, self.cb_department, f"Select a department first."),
            (req_type, self.cb_req_type, f"Select a request type first."),
            (req_sub_type, self.cb_req_sub_type, f"Select a request sub-type first."),
            (request_text, self.tb_request_text, f"Enter some details about your request first."),
            (priority, self.s_priority, f"Select a priority first.")
        ):
            if not val:
                self.focus_widget(widget, msg)
                return

        # TODO calculate this as per Access
        #  ' Change subpriority when an ordering is selected
        # Private Sub Frame31_AfterUpdate()
        #     If Not validate(False, False, True, False, False, False, False, False) Then
        #         Exit Sub
        #     End If
        #     Dim p As Integer
        #     If Me.Frame31 = 1 Then
        #         p = 0
        #     Else
        #         Dim UserName As String
        #         UserName = GetUserFullName()
        #         Dim priorityLevel As Integer
        #         priorityLevel = Me.Priority
        #         Dim rs As DAO.Recordset
        #         Set rs = CurrentDb.OpenRecordset("SELECT COUNT(*) AS [# Queued] FROM [ITRequests] WHERE LCASE([RequestedBy]) = LCASE('" & UserName & "') AND [Priority] = " & priorityLevel & " AND LCASE([Status]) = 'queued'", dbOpenSnapshot)
        #         Dim n As Integer
        #         If Not rs.EOF Then
        #             n = rs(0) + 1
        #         Else
        #             n = 0
        #         End If
        #         p = n
        #         rs.Close
        #         Set rs = Nothing
        #     End If
        #     Me.SubPriority = p
        # End Sub
        sub_priority = 0
        status = "Queued"  # place directly in the queue
        personnel_assigned_id = 1  # Unknown assignment code
        due_date = is_date(due_date)
        if isinstance(due_date, bool):
            due_date = o_due_date
        str_due_date = f"'{due_date:%x %X}'"
        str_now = f"'{datetime.datetime.now():%x %X}'"

        insert_sql = f"INSERT INTO [IT Requests]"
        insert_sql += f" ([RequestDate], [DueDate], [Priority]"
        insert_sql += f", [SubPriority], [Request], [RequestedBy]"
        insert_sql += f", [Department], [Company], [RequestType]"
        insert_sql += f", [RequestSubType], [Comments], [Status]"
        insert_sql += f", [ITPersonAssignedID], [LabourEstimate], [LastStatusUpdater]"
        insert_sql += ") VALUES ("
        insert_sql += f"{str_now}, {due_date}, {priority}"
        insert_sql += f", {sub_priority}, '{request_text}', '{requested_by}'"
        insert_sql += f", {department_id}, '{company}', '{req_type}'"
        insert_sql += f", '{req_sub_type}', '{comment_text}', '{status}'"
        insert_sql += f", {personnel_assigned_id}, {labour_est}, '{self.user_full_name}'"
        insert_sql += f")"


        update_sql = f"UPDATE [IT Requests] SET"
        update_sql += f" [RequestDate] = {str_now}"
        update_sql += f", [DueDate] = {due_date}"
        update_sql += f", [Priority] = {priority}"
        update_sql += f", [SubPriority] = {sub_priority}"
        update_sql += f", [Request] = '{request_text}'"
        update_sql += f", [RequestedBy] = '{requested_by}'"
        update_sql += f", [Department] = {department_id}"
        update_sql += f", [Company] = '{company}'"
        update_sql += f", [RequestType] = '{req_type}'"
        update_sql += f", [RequestSubType] = '{req_sub_type}'"
        update_sql += f", [Comments] = '{comment_text}'"
        update_sql += f", [Status] = '{status}'"
        update_sql += f", [ITPersonAssignedID] = {personnel_assigned_id}"
        update_sql += f", [LabourEstimate] = {labour_est}"
        update_sql += f", [LastStatusUpdater] = '{self.user_full_name}'"
        update_sql += f" WHERE [ITRequestID#] = {self.request_id}"


    # def unselect_follow_up_table_rows(self):
    #     for row in self.v_table_selected_rows:
    #         self.table_follow_up.deselect_row(row)
    #     self.v_table_selected_rows.clear()

    # def sort_follow_up_table(self, row, col):
    #     col_name = self.header_follow_up[col]
    #     rev = self.data_rev_follow_up[col_name]
    #     if rev is None:
    #         rev = False
    #     elif rev:
    #         rev = None
    #     else:
    #         rev = True
    #     self.data_rev_follow_up = {k: None for k in self.header_follow_up}
    #     self.data_rev_follow_up[col_name] = rev
    #     print(f"{row=}, {col=}, {col_name=}, {rev=}")
    #     if rev is None:
    #         # original values
    #         s_values = [[v for v in r] for r in self.og_table_follow_up_values[1:]]
    #     else:
    #         s_values = sorted(
    #             self.table_follow_up.values[1:],
    #             key=lambda r: r[col],
    #             reverse=rev
    #         )
    #     s_values.insert(0, self.header_follow_up)
    #     self.table_follow_up.update_values(s_values)
    def load_dfs(self):
        self.df_requests = connect(**self.sql_df_requests)
        self.df_customers = connect(**self.sql_df_customers)
        self.df_departments = connect(**self.sql_df_departments)
        self.df_req_hardware = connect(**self.sql_df_hardware)
        self.df_req_software = connect(**self.sql_df_software)
        self.df_req_training = connect(**self.sql_df_training)


if __name__ == '__main__':

    app = App()
    app.mainloop()

import customtkinter as ctk
from CTkTable import CTkTable
from colour_utility import *
from tkinter_utility import calc_geometry_tl
from customtkinter_utility import CtkTableExt


class App(ctk.CTk):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.title_app_long = f"IT Request Maintenance"
        self.text_sw_all_follow_up = ""

        self.default_cb_width = 120
        self.default_cb_height = 25
        self.default_cb_corner_radius = 10
        self.default_cb_justify = ctk.CENTER

        self.colour_default_cb_bg_colour = Colour("#69A3C3")
        self.colour_default_cb_fg_colour = Colour("#092373")
        self.colour_default_cb_border_colour = Colour("#092373")
        self.colour_default_cb_dropdown_fg_color = self.colour_default_cb_fg_colour.brightened(0.05)

        self.list_companies = [
            "BWS",
            "STG",
            "Lewis"
        ]
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
        self.list_req_types = list(self.dict_req_types)
        self.list_req_sub_types = []
        self.list_priorities = list(range(1, 12))
        self.header_follow_up = ["Comp", "Dept", "Name"]
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
        self.og_table_follow_up_values = [[v for v in row] for row in self.data_follow_up]
        self.data_rev_follow_up = {k: None for k in self.header_follow_up}

        self.c_cb_new = "+"
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
            "height": 75
        }

        self.f_top_controls = ctk.CTkFrame(self)
        self.f_bottom_controls = ctk.CTkFrame(self)
        self.v_cb_department = ctk.StringVar(self, name="request_department")
        self.v_cb_company = ctk.StringVar(self, name="request_company")
        self.v_cb_req_type = ctk.StringVar(self, name="request_type")
        self.v_cb_req_sub_type = ctk.StringVar(self, name="request_sub_type")
        self.v_s_priority = ctk.IntVar(self, name="request_priority")
        self.v_table_selected_rows = list()
        self.tv_sw_all_follow_up = ctk.StringVar(self, name="switch_all_follow_up", value=self.text_sw_all_follow_up)
        self.cb_department = ctk.CTkComboBox(
            master=self.f_top_controls,
            values=self.list_departments,
            command=self.update_cb_department,
            variable=self.v_cb_department,
            **self.default_cb_config
        )
        self.cb_company = ctk.CTkComboBox(
            master=self.f_top_controls,
            values=self.list_companies,
            command=self.update_cb_company,
            variable=self.v_cb_company,
            **self.default_cb_config
        )
        self.cb_req_type = ctk.CTkComboBox(
            master=self.f_top_controls,
            values=self.list_req_types,
            command=self.update_cb_req_type,
            variable=self.v_cb_req_type,
            **self.default_cb_config
        )
        self.cb_req_sub_type = ctk.CTkComboBox(
            master=self.f_top_controls,
            values=self.list_req_sub_types,
            command=self.update_cb_req_sub_type,
            variable=self.v_cb_req_sub_type,
            **self.default_cb_config
        )

        self.s_priority = ctk.CTkSlider(
            master=self.f_top_controls,
            from_=self.list_priorities[0],
            to=self.list_priorities[-1],
            number_of_steps=(self.list_priorities[-1] - self.list_priorities[0]),
            variable=self.v_s_priority,
            command=self.update_sl_priority
        )

        # self.table_follow_up = CTkTable(
        #     master=self.f_bottom_controls,
        #     header_color="#019822",
        #     values=self.data_follow_up,
        #     command=self.update_table_follow_up
        # )

        self.table_follow_up = CtkTableExt(
            master=self.f_bottom_controls,
            table_data=self.data_follow_up,
            width=450,
            kwargs_table={
                "header_color": "#019822",
                "command": self.update_table_follow_up
            }
        )

        self.tb_request_text = ctk.CTkTextbox(
            self.f_bottom_controls,
            **self.default_tb_config
        )

        self.tb_comments_text = ctk.CTkTextbox(
            self.f_bottom_controls,
            **self.default_tb_config
        )

        # self.sw_all_follow_up = ctk.CTkSwitch(
        #     master=self.f_controls_a,
        #     textvariable=self.tv_sw_all_follow_up
        #
        # )

        self.f_top_controls.pack()
        self.cb_company.pack()
        self.cb_department.pack()
        self.cb_req_type.pack()
        self.cb_req_sub_type.pack()
        self.s_priority.pack()

        self.f_bottom_controls.pack()
        self.table_follow_up.pack()
        self.tb_request_text.pack()
        self.tb_comments_text.pack()

    def update_cb_department(self, department):
        print(f"update_cb_department {department=}")
        if department == self.c_cb_new:
            print(f"Add new department")

    def update_cb_company(self, company):
        print(f"update_cb_company {company=}")
        if company == self.c_cb_new:
            print(f"Add new company")

    def update_cb_req_type(self, req_type):
        print(f"update_cb_req_type {req_type=}")
        if req_type == self.c_cb_new:
            print(f"Add new req_type")
        else:
            self.cb_req_sub_type.values = self.dict_req_types[req_type]
            self.cb_req_sub_type.configure(values=self.dict_req_types[req_type])
            self.v_cb_req_sub_type.set("")

    def update_cb_req_sub_type(self, re_sub_type):
        print(f"update_cb_req_sub_type {re_sub_type=}")
        if re_sub_type == self.c_cb_new:
            print(f"Add new re_sub_type")

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


if __name__ == '__main__':

    app = App()
    app.mainloop()

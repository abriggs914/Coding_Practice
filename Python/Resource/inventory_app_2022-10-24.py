import tkinter

import pandas

from grid_manager import GridManager
from tkinter_utility import *
from stg_queries import *
from menus import AddItemMenu
from utility import alpha_seq


class InventoryApp(tkinter.Tk):

    def __init__(self):
        super().__init__()

        self.df_inventory_master = None
        self.df_uom = None
        self.df_type = None
        self.df_status = None
        self.df_condition = None
        self.df_computer = None
        self.df_peripherals = None
        self.df_network = None
        self.df_wire = None
        self.df_unknown = None

        self.populate_data()

        assert all(
            [isinstance(v, pandas.DataFrame) and not v.empty for v in [
                self.df_inventory_master,
                self.df_uom,
                self.df_type,
                self.df_status,
                self.df_condition,
                self.df_computer,
                self.df_peripherals,
                self.df_network,
                self.df_wire,
                self.df_unknown
            ]
        ]), "Error loading some data."

        self.WIDTH, self.HEIGHT = 500, 500
        self.geometry(f"{self.WIDTH}x{self.HEIGHT}")
        self.title("BWS Inventory Manager")
        self.state("zoomed")

        self.namer = alpha_seq(1000, prefix="w_IA_")

        self.level_add_menu = None
        self.new_item_save_state = tkinter.Variable(self, value={})

        # self.tv_l1, self.l1 = label_factory(self, tv_label="Label 1")
        self.frame_button_bar_1 = tkinter.Frame(self, name=next(self.namer))
        self.frame_treeview = tkinter.Frame(self, name=next(self.namer), width=self.WIDTH * 0.95)
        self.frame_drillview = tkinter.Frame(self, name=next(self.namer))

        self.tv_btn_add_new_item,\
        self.btn_add_new_item\
            = button_factory(
                self.frame_button_bar_1,
                tv_btn="+",
                kwargs_btn={
                    "name": next(self.namer),
                    "command": self.click_add_new_item
                }
        )

        self.chosen_columns = ["Equip_Desc", "Class", "Category", "Current_location", "Status", "Availability"]
        self.column_display_width = [250, 100, 100, 150, 50, 75]
        self.treeview_items_columns = list(self.df_inventory_master.columns)
        self.treeview_items_display_columns = [(self.treeview_items_columns.index(i), i) for i in self.chosen_columns]
        self.treeview_items = None
        self.scrollbar_y_items = None
        self.scrollbar_x_items = None
        self.tv_label_treeview = tkinter.StringVar(self, value="v_Tools&Equip")
        self.label_treeview_name = tkinter.Label(self.frame_treeview, textvariable=self.tv_label_treeview, anchor=tkinter.CENTER)
        self.set_treeview()

        self.gm1 = GridManager()
        self.gm1.grid_widgets([
            [
                self.frame_button_bar_1
            ],
            [
                self.frame_treeview
            ],
            [
                self.frame_drillview
            ]
        ])
        self.gm2 = GridManager()
        self.gm2.grid_widgets([
            [
                self.btn_add_new_item
            ]
        ])
        self.gm3 = GridManager()
        self.gm3.grid_widgets([
            [
                self.label_treeview_name
            ],
            [
                {
                    "widget": self.scrollbar_x_items,
                    "sticky": "ew"
                }
            ],
            [
                self.treeview_items,
                {
                    "widget": self.scrollbar_y_items,
                    "sticky": "ns"
                }
            ]
        ])

    def populate_data(self):
        self.df_inventory_master = connect(**SQL_V_TOOLSANDEQUIP)
        self.df_uom = connect(**SQL_UOM)
        self.df_type = connect(**SQL_TYPE)
        self.df_status = connect(**SQL_STATUS)
        self.df_condition = connect(**SQL_CONDITION)
        self.df_computer = connect(**SQL_COMPUTER)
        self.df_peripherals = connect(**SQL_PERIPHERALS)
        self.df_network = connect(**SQL_NETWORK)
        self.df_wire = connect(**SQL_WIRE)
        self.df_unknown = connect(**SQL_UNKNOWN)

    def submit_new_item(self, *args):
        print(f"New Item Submission:")
        all_keys = self.level_add_menu.valid_status_keys
        data_status = eval(self.level_add_menu.status.get())
        data_valid = eval(self.level_add_menu.valid.get())
        if not all_keys.difference(data_status.keys()) and data_status["submission"]:
            # all valid
            print(f"all valid")
            msg = f"Are you sure you want to add '{data_status['name']}' to ITI Items?"
            ans = messagebox.askyesnocancel(title="Inventory Addition", message=msg)
            if ans:
                insert_new_item(data_status)
                msg = f"Successfully added '{data_status['name']}' to ITI Items."
                messagebox.showinfo(title="Inventory Added", message=msg)
                self.new_item_save_state.set({})
            else:
                # save unfinished work for next opening
                print(f"save unfinished work for next opening")
                self.new_item_save_state.set(data_valid)
        else:
            # save unfinished work for next opening
            print(f"save unfinished work for next opening")
            self.new_item_save_state.set(data_valid)
        print(f"{data_status=}\n{data_valid=}")

    def get_values_spin_uom(self):
        res = []
        for i, row in self.df_uom.iterrows():
            iid = row["ID"]
            name = row["Name"]
            suffix = row["Suffix"]
            res.append("||".join(list(map(str, [iid, name, suffix]))))
        return res

    def get_values_spin_type(self):
        res = []
        for i, row in self.df_type.iterrows():
            iid = row["ID"]
            name = row["Name"]
            res.append("||".join(list(map(str, [iid, name]))))
        return res

    def get_values_spin_cond(self):
        res = []
        for i, row in self.df_condition.iterrows():
            iid = row["ID"]
            name = row["Name"]
            res.append("||".join(list(map(str, [iid, name]))))
        return res

    def get_values_spin_computer(self):
        res = []
        for i, row in self.df_computer.iterrows():
            iid = row["ID"]
            name = row["Name"]
            res.append("||".join(list(map(str, [iid, name]))))
        return res

    def get_values_spin_peripherals(self):
        res = []
        for i, row in self.df_peripherals.iterrows():
            iid = row["ID"]
            name = row["Name"]
            res.append("||".join(list(map(str, [iid, name]))))
        return res

    def get_values_spin_network(self):
        res = []
        for i, row in self.df_network.iterrows():
            iid = row["ID"]
            name = row["Name"]
            res.append("||".join(list(map(str, [iid, name]))))
        return res

    def get_values_spin_wire(self):
        res = []
        for i, row in self.df_wire.iterrows():
            iid = row["ID"]
            name = row["Name"]
            res.append("||".join(list(map(str, [iid, name]))))
        return res

    def get_values_spin_unknown(self):
        res = []
        for i, row in self.df_unknown.iterrows():
            iid = row["ID"]
            name = row["Name"]
            res.append("||".join(list(map(str, [iid, name]))))
        return res

    def click_add_new_item(self):
        values_uom = self.get_values_spin_uom()
        values_type = self.get_values_spin_type()
        values_condition = self.get_values_spin_cond()
        values_computer = self.get_values_spin_computer()
        values_peripherals = self.get_values_spin_peripherals()
        values_network = self.get_values_spin_network()
        values_wire = self.get_values_spin_wire()
        values_unknown = self.get_values_spin_unknown()
        save_state = eval(self.new_item_save_state.get())
        # print(f"{values_uom=}, {values_type}")
        self.level_add_menu = AddItemMenu(
            self,
            spin_values_uom=values_uom,
            spin_values_type=values_type,
            spin_values_cond=values_condition,
            spin_values_computer=values_computer,
            spin_values_peripherals=values_peripherals,
            spin_values_network=values_network,
            spin_values_wire=values_wire,
            spin_values_unknown=values_unknown,
            save_state=save_state
        )
        self.level_add_menu.status.trace_variable("w", self.submit_new_item)
        self.level_add_menu.mainloop()

    def select_treeview_items(self, event):
        tree = event.widget
        selection = [tree.item(item)["text"] for item in tree.selection()]
        print("selected items:", selection)
        # messagebox.showinfo(title='Information', message=','.join(selection))

    def set_treeview(self):
        print(f"{self.chosen_columns=}")
        self.treeview_items = ttk.Treeview(
            self.frame_treeview,
            name=next(self.namer),
            columns=self.chosen_columns
            , displaycolumns=[tup[1] for tup in self.treeview_items_display_columns]
        )

        print(f"columns {self.treeview_items['columns']=}")

        #self.treeview_items["columns"] = [tup[1] for tup in self.treeview_items_columns]

        self.treeview_items.column("#0", width=0, stretch=tkinter.NO)
        self.treeview_items.heading("#0", text="", anchor=tkinter.CENTER)

        for i, tup in enumerate(self.treeview_items_display_columns):
            idx, col = tup
            # print(f"A {i=}, {col=}")
            # coln = self.treeview_items_columns[col]
            # self.treeview_items.heading(col, f"column_{i}")
            # self.treeview_items.heading(col, col)
            # self.treeview_items.heading(f"column_{i}", col)
            # self.treeview_items.heading(f"column_{i}", f"column_{i}")
            # self.treeview_items.heading(i, text=f"column_{i}")

            # row and columns
            # self.treeview_items.heading(i, text=f"col={col}, {i}")
            # self.treeview_items.column(i, width=10)

            # column names
            # print(f"B {i=}, {col=}, {coln=}")
            # col_name = f"col={coln}"
            col_name = col
            c_width = self.column_display_width[i]
            self.treeview_items.column(col_name, width=c_width, anchor=tkinter.CENTER)
            self.treeview_items.heading(col_name, text=col_name, anchor=tkinter.CENTER)

        self.treeview_items.bind("<<TreeviewSelect>>", self.select_treeview_items)
        self.scrollbar_y_items = ttk.Scrollbar(self.frame_treeview, orient=tkinter.VERTICAL, command=self.treeview_items.yview)
        self.scrollbar_x_items = ttk.Scrollbar(self.frame_treeview, orient=tkinter.HORIZONTAL, command=self.treeview_items.xview)
        self.treeview_items.configure(yscrollcommand=self.scrollbar_y_items.set, xscrollcommand=self.scrollbar_x_items.set)

        data = []
        for i in range(100):
            # data.append([f"A_{i}_{j}" for j in range(len(self.df_inventory_master.columns))])
            assert isinstance(self.df_inventory_master, pandas.DataFrame)
            row = []
            # for j in range(len(self.treeview_items_columns)):
            for j, tup in enumerate(self.treeview_items_display_columns):
                idx, col = tup
                val = self.df_inventory_master.iloc[i][idx]
                print(f"{i=}, {j=}, {tup=}, {val=}")
                # val = self.df_inventory_master[j].tolist()[j]
                row.append(val)
            data.append(row)
            # data.append([f"A_{i}_{j}" for j in range(len(self.df_inventory_master.columns))])

        print(f"{data=}")

        for i, dat in enumerate(data):
            print(f"{dat=}")
            self.treeview_items.insert("", tkinter.END, text=f"B_{i}", iid=f"C_{i}", values=dat)

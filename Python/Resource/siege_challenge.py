import json

from json_utility import jsonify
from siege_challenge.form_map import FormMap
from siege_challenge.form_operator import FormOperator
from siege_challenge.siege_map import Map
from siege_challenge.siege_operator import Operator
from tkinter_utility import *


# game_mode 1
# every operator in order
# pick Map, Atk/Def, then op

# game_mode 2
# every operator random
# pick Map, Atk/Def, then op

class App(tkinter.Tk):
    def __init__(self, width=600, height=400):
        super().__init__()
        # self.geometry(f"{width}x{height}")
        self.state("zoomed")

        self.save_file = "saved_siege_challenge_data.json"

        self.list_maps = []
        self.list_operators = []
        self.list_defenders = []
        self.list_attackers = []
        self.list_game_modes = []
        self.df_attackers = pandas.DataFrame(columns=["Name", "CTU", "Sex", "Completed"])
        self.df_defenders = pandas.DataFrame(columns=["Name", "CTU", "Sex", "Completed"])
        self.df_maps = pandas.DataFrame(columns=["Name", "Country", "Num Floors", "Completed"])
        self.df_games = pandas.DataFrame(columns=["Date", "Mode", "Rnds", "Res", "Map"])

        self.load_data()

        self.tl_form_operator = None
        self.tl_form_map = None
        self.tl_form_game = None
        self.tv_btn_new_op,\
            self.btn_new_op = \
            button_factory(
                self,
                tv_btn="New Op",
                command=self.click_new_op
            )

        self.tv_btn_new_map,\
            self.btn_new_map = \
            button_factory(
                self,
                tv_btn="New Map",
                command=self.click_new_map
            )

        self.tv_btn_new_game,\
            self.btn_new_game = \
            button_factory(
                self,
                tv_btn="New Game",
                command=self.click_new_game
            )

        self.tv_btn_save,\
            self.btn_save = \
            button_factory(
                self,
                tv_btn="Save",
                command=self.save
            )

        self.frame_operators = tkinter.Frame(self)
        self.frame_maps = tkinter.Frame(self)
        self.frame_games = tkinter.Frame(self)
        self.frame_attackers = tkinter.Frame(self.frame_operators)
        self.frame_defenders = tkinter.Frame(self.frame_operators)
        print(f"{self.list_defenders=}")
        print(f"{self.list_attackers=}")

        self.mc_attackers = MultiComboBox(
            self.frame_attackers,
            data=self.df_attackers,
            tv_label="Known Attackers:",
            lock_result_col="Name",
            allow_insert_ask=False,
            limit_to_list=False,
            include_aggregate_row=False,
            drop_down_is_clicked=True,
            viewable_column_widths=[100, 75, 50],
            exhaustive_filtering=True
        )

        self.mc_attackers.set_cell_colours("0", "0", Colour(ORANGE_3).hex_code, Colour(CRIMSON_RED).hex_code)
        self.mc_attackers.set_cell_colours("0", "1", Colour(PURPLE).hex_code, Colour(YELLOW).hex_code)
        self.mc_attackers.set_cell_colours("1", "1", Colour(DODGERBLUE).hex_code, Colour(ORANGE_3).hex_code)
        print(f"{self.mc_attackers.tree_treeview.tag_has(f'0{self.mc_attackers.tree_controller.cell_tag_delim}0')=}")
        # print(f"{self.mc_attackers.tree_treeview.tag_names()}")

        all_tags = self.mc_attackers.tree_treeview.get_children()
        print(f"{all_tags=}")
        print(f"all_tags0=|{self.mc_attackers.tree_treeview.item('0')}|")
        print(f"all_tags1=|{self.mc_attackers.tree_treeview.item('1')}|")
        print(f"all_tags2=|{self.mc_attackers.tree_treeview.item('2')}|")
        print(f"all_tags3=|{self.mc_attackers.tree_treeview.item('3')}|")

        self.mc_defenders = MultiComboBox(
            self.frame_defenders,
            data=self.df_defenders,
            tv_label="Known Defenders:",
            lock_result_col="Name",
            allow_insert_ask=False,
            limit_to_list=False,
            include_aggregate_row=False,
            drop_down_is_clicked=True,
            include_searching_widgets=0,
            viewable_column_widths=[100, 75, 50],
            exhaustive_filtering=True
        )

        self.mc_maps = MultiComboBox(
            self.frame_maps,
            data=self.df_maps,
            tv_label="Known Maps:",
            lock_result_col="Name",
            allow_insert_ask=False,
            limit_to_list=False,
            include_aggregate_row=False,
            drop_down_is_clicked=True,
            include_searching_widgets=0,
            viewable_column_widths=[100, 75, 50],
            exhaustive_filtering=True
        )

        self.mc_games = MultiComboBox(
            self.frame_games,
            data=self.df_games,
            tv_label="Games:",
            # lock_result_col="Name",
            allow_insert_ask=False,
            limit_to_list=False,
            include_aggregate_row=False,
            drop_down_is_clicked=True,
            include_searching_widgets=0,
            viewable_column_widths=[100, 75, 50]
            # ,
            # exhaustive_filtering=True
        )

        # self.count_down_timer = CountDownTimer()

        # self.res_tv_lbl_lst_atk, \
        #     self.res_lbl_lst_atk, \
        #     self.res_tv_list_lst_atk, \
        #     self.res_list_lst_atk = \
        #     list_factory(
        #         self.frame_attackers,
        #         tv_label="Known Attackers:",
        #         tv_list=self.list_attackers,
        #         kwargs_list={
        #             "state": "disabled",
        #             "justify": tkinter.CENTER,
        #             "width": 30
        #         }
        #     )
        # self.res_tv_lbl_lst_def, \
        #     self.res_lbl_lst_def, \
        #     self.res_tv_list_lst_def, \
        #     self.res_list_lst_def = \
        #     list_factory(
        #         self.frame_defenders,
        #         tv_label="Known Defenders:",
        #         tv_list=self.list_defenders,
        #         kwargs_list={
        #             "state": "disabled",
        #             "justify": tkinter.CENTER,
        #             "width": 30
        #         }
        #     )

        self.frame_operators.pack(side=tkinter.LEFT)
        self.frame_maps.pack(side=tkinter.LEFT)
        self.frame_games.pack(side=tkinter.LEFT)
        self.frame_attackers.pack(side=tkinter.TOP)
        self.frame_defenders.pack(side=tkinter.TOP)
        # self.res_lbl_lst_atk.pack()
        # self.res_lbl_lst_def.pack()
        # self.res_list_lst_atk.pack()
        # self.res_list_lst_def.pack()
        self.btn_new_op.pack(side=tkinter.BOTTOM)
        self.btn_new_map.pack(side=tkinter.BOTTOM)
        self.btn_save.pack(side=tkinter.BOTTOM)
        self.protocol("WM_DELETE_WINDOW", self.close_app)

    def load_data(self):
        file = self.save_file
        with open(file, "r") as f:
            data = json.load(f)
        ops = data["known_operators"]
        maps = data["known_maps"]
        for i, op in enumerate(ops):
            name = op.get("name", "")
            ctu = op.get("ctu", "")
            atk_def = op.get("atk_def", "")
            sex = op.get("sex", "")
            completed = op.get("competed", "")
            new_op = Operator(name, ctu, atk_def, sex)
            self.list_operators.append(new_op)
            if atk_def == "attacker":
                self.list_attackers.append(new_op)
                # print(f"{self.df_attackers=}\n{self.df_attackers.size=}")
                self.df_attackers.loc[len(self.df_attackers)] = [name, ctu, sex, completed]
                # self.df_attackers.index += 1
            else:
                self.list_defenders.append(new_op)
                self.df_defenders.loc[len(self.df_defenders)] = [name, ctu, sex, completed]
                # self.df_defenders.index += 1
            print(f"{i=}, {op=}")
            print(self.df_attackers)

        for i, map_ in enumerate(maps):
            name = map_.get("name", "")
            country = map_.get("country", "")
            num_floors = map_.get("num_floors", "")
            completed = map_.get("competed", "")
            new_map = Map(name, country, num_floors)
            self.list_maps.append(new_map)
            self.df_maps.loc[len(self.df_maps)] = [name, country, num_floors, completed]

    def click_new_op(self, event=None):
        self.tl_form_operator = FormOperator(self.list_operators, self.close_form_operator)
        self.tl_form_operator.protocol("WM_DELETE_WINDOW", self.close_form_operator)
        self.tl_form_operator.grab_set()

    def click_new_map(self, event=None):
        self.tl_form_map = FormMap(self.list_maps, self.close_form_map)
        self.tl_form_map.protocol("WM_DELETE_WINDOW", self.close_form_map)
        self.tl_form_map.grab_set()

    def click_new_game(self, event=None):
        self.tl_form_game = FormGame(self.list_maps, self.close_form_game)
        self.tl_form_game.protocol("WM_DELETE_WINDOW", self.close_form_game)
        self.tl_form_game.grab_set()

    def close_form_game(self):
        pass

    def close_form_operator(self, event=None):
        assert isinstance(self.tl_form_operator, FormOperator)
        new_status = self.tl_form_operator.tv_status.get()
        new_name = self.tl_form_operator.tv_entry_op_name.get()
        new_ctu = self.tl_form_operator.tv_combo_ctu.get()
        new_atk_def = self.tl_form_operator.options_atk_def[self.tl_form_operator.tv_var_atk_def.get()].lower()
        new_sex = self.tl_form_operator.options_sex[self.tl_form_operator.tv_var_sex.get()].lower().title()
        if new_status == "submit":
            op = Operator(new_name, new_ctu, new_atk_def, new_sex)
            self.list_operators.append(op)
            if new_atk_def == "attacker":
                self.list_attackers.append(op)
                print(f"{len(self.df_attackers)=}")
                self.mc_attackers.add_new_item(op.name, "Name", {"CTU": op.ctu, "Sex": op.sex})
            else:
                self.list_defenders.append(op)
                self.mc_defenders.add_new_item(op.name, "Name", {"CTU": op.ctu, "Sex": op.sex})

        print(f"{new_status=}, {new_name=}, {new_ctu=}, {new_atk_def=}")
        for key, callback in self.tl_form_operator.after_callbacks.items():
            print(f"{key=}")
            self.tl_form_operator.after_cancel(callback)
        self.tl_form_operator.after_callbacks.clear()
        self.tl_form_operator.destroy()
        self.tl_form_operator = None

    def close_form_map(self, event=None):
        assert isinstance(self.tl_form_map, FormMap)
        new_status = self.tl_form_map.tv_status.get()
        new_name = self.tl_form_map.tv_entry_map_name.get()
        new_country = self.tl_form_map.tv_combo_country.get().title()
        new_num_floors = self.tl_form_map.options_num_floors[self.tl_form_map.tv_var_num_floors.get()]
        if new_status == "submit":
            map = Map(new_name, new_country, new_num_floors)
            self.list_maps.append(map)
            self.mc_maps.add_new_item(map.name, "Name", {"Country": map.country, "Num Floors": map.num_floors})

        print(f"{new_status=}, {new_name=}, {new_country=}")
        for key, callback in self.tl_form_map.after_callbacks.items():
            print(f"{key=}")
            self.tl_form_map.after_cancel(callback)
        self.tl_form_map.after_callbacks.clear()
        self.tl_form_map.destroy()
        self.tl_form_map = None

    def save(self):
        file = self.save_file
        data = {}
        data["known_operators"] = [op.to_json() for op in self.list_operators]
        data["known_maps"] = [m.to_json() for m in self.list_maps]

        with open(file, "w") as f:
            # json.dump(data, f)
            f.write(jsonify(data, in_line=False))

    def close_app(self):
        self.save()
        self.destroy()


if __name__ == '__main__':

    app = App()
    app.mainloop()

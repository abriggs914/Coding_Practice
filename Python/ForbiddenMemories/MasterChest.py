import json
import os

import pandas as pd
from collections import OrderedDict
from player import *


root_path_master_chests = r"C:\Users\abrig\Documents\Coding_Practice\Python\ForbiddenMemories"
if not os.path.exists(root_path_master_chests):
    root_path_master_chests = root_path_master_chests.replace("abrig", "abriggs")
if not os.path.exists(root_path_master_chests):
    raise NotADirectoryError(f"Couldn't find the root location for master chest JSON files.")


combinations_file = r"C:\Users\abrig\Documents\Coding_Practice\Java\ForbiddenMemories\combinations.txt"
if not os.path.exists(combinations_file):
    combinations_file = combinations_file.replace("abrig", "abriggs")
if not os.path.exists(combinations_file):
    raise FileNotFoundError(f"Couldn't find the combinations file 'combinations.txt'.")


rituals_file = r"C:\Users\abrig\Documents\Coding_Practice\Java\ForbiddenMemories\ritual_details.json"
if not os.path.exists(rituals_file):
    rituals_file = rituals_file.replace("abrig", "abriggs")
if not os.path.exists(rituals_file):
    raise FileNotFoundError(f"Couldn't find the combinations file 'ritual_details.json'.")


def next_id():
    return len([
        f for f in os.listdir(root_path_master_chests)
        if f.lower().endswith(".json") and f.lower().startswith("master_chest_")
    ])


def parse_card_line(line):
    # raw example
    # "= 031  Koumori Dragon                        Dr  D    4  1500  1200  Mo  J\n"
    w_line = line.removeprefix("+").removeprefix("=").strip()
    s_line = [word for word in w_line.split(" ") if word]

    if len(s_line) >= 9:
        num = int(s_line[0])
        name = " ".join(s_line[1: -7])
        type_ = s_line[-7]
        attribute = s_line[-6]
        cost = s_line[-5]
        atk_points = int(s_line[-4])
        def_points = int(s_line[-3])
        planet_1 = s_line[-2]
        planet_2 = s_line[-1]
        data = [
            num,
            name,
            type_,
            attribute,
            cost,
            atk_points,
            def_points,
            planet_1,
            planet_2
        ]
    elif len(s_line) > 2:
        data = [
            int(s_line[0]),
            " ".join(s_line[1: -1]),
            s_line[-1]
        ]
        # print(f"{data=}")
    else:
        # print(f"COULD NOT MAKE CARD:")
        # print(f"UNKNOWN CARD {line=}")
        data = []

    c = Card(*data)
    # # if c.type_simple != "Monster":
    # #     print(f"AA {c}")
    # num = c.num
    # # kc = st.session_state.get("known_cards")
    # d = max(0, (1 + num - len(kc)))
    # while d > 0:
    #     # kc.append(None)
    #     d -= 1
    # # print(f"{d=}, {num=}, {len(kc)=}, {line=}")
    # # if kc[num] is None:
    # #     kc[num] = c
    # #     st.session_state.update({"known_cards": kc})
    # # print(f"NEW CARD MADE:")
    # # print(f"{c=}")
    # # return c.num
    return c


def parse_combinations_file():
    cards_2 = OrderedDict()
    with open(combinations_file, "r") as f:
        in_section = True
        section_card: Optional[Card] = None
        a: Optional[Card] = None
        b: Optional[Card] = None
        for i, line in enumerate(f.readlines()):
            # check line is not separator '----'
            line_sep = line.strip()
            # st.write(f"A {i=}, {line_sep=}")
            while line_sep.startswith("-"):
                line_sep = line_sep.removeprefix("-")

            if line_sep:
                # this is not a separator line
                card = parse_card_line(line)

                if section_card is None:
                     section_card = card
                     # print(f"SEC {i=}, {line=}")
                     cards_2[section_card] = {}
                else:
                    if line.startswith("+"):
                        a = card
                    if line.startswith("="):
                        b = card
                    if (a is not None) and (b is not None):
                        # if section_card not in cards_2:
                        #     cards_2[section_card] = {}
                        cards_2[section_card][a] = b
                        a = None
                        b = None
                    # else:
                    #     print(f"{i=}, {line=}, {a=}, {b=}")

                # print(f"{card=}")
            else:
                # print(f"SEP {i=}, {line=}")
                in_section = False
                section_card = None

    return cards_2


def parse_rituals_file():
    with open(rituals_file, "r") as f:
        df = pd.read_json(f)
        df["n_Ritual_Monster"] = None
        df["n_Ritual_Card"] = None
        df["n_Sacrifices"] = None
        for i, row in df.iterrows():
            ritual_monster = row["Ritual Monster"]
            ritual_card = row["Ritual Card"]
            sacrifices = row["Sacrifices"]
            num_rm = int(ritual_monster.split(" ")[0].removeprefix("#"))
            num_rc = int(ritual_card.split(" ")[0].removeprefix("#"))
            nums_sac = [int(c.split(" ")[0].removeprefix("#")) for c in sacrifices]
            df.loc[i, "n_Ritual_Monster"] = num_rm
            df.loc[i, "n_Ritual_Card"] = num_rc
            df.loc[i, "n_Sacrifices"] = ";".join(map(str, nums_sac))
        return df


class MasterChest:

    def __init__(self, id_num: Optional[int] = None):

        self.id_num = next_id()
        self.path_data = os.path.join(root_path_master_chests, f"master_chest_{str(self.id_num).rjust(3, '0')}.json")

        self.data_combinations = parse_combinations_file()
        self.data_rituals = parse_rituals_file()
        self.df_card_data = self.init_card_df()

        self.player_chests = self.load_master_chest_data()

    def load_master_chest_data(self):
        """
        file contents are expected to follow format:

        player_chests: dict of player ids and deck_type keys
        {
            "player_chests": {
                "0": {
                    "deck": [1, 2, 3, ... 122, 122, 371, 612, 612]  # total of 40 cards, duplicates allowed
                    "chest": [1, 18, 18, 19, 19, ....] all cards not in the deck - AS A LIST.
                    ### ALSO ACCEPTED:
                    "chest": {1: 1, 18: 2, 19: 2, ....} all cards not in the deck - AS A DICT.
                }
            }
        }

        :return:
        """
        loaded_data = {}
        if os.path.exists(self.path_data):
            with open(self.path_data, "r") as f:
                loaded_data = json.load(f)

        player_datas = loaded_data.get("player_data", {})
        list_players = list(player_datas)
        for i, player_id in enumerate(list_players):
            player_data = player_datas.get(player_id, {})
            player_name = player_data.get("name", "UNKNOWN")
            player_deck = player_data.get("deck", [])
            player_chest = player_data.get("chest", {})

            if isinstance(player_deck, dict):
                deck = []
                for j, c_id in enumerate(player_deck):
                    c_qty = player_deck.get(c_id, 1)
                    for k in range(c_qty):
                        deck.append(self.num_2_card(c_id))
                player_deck = deck

            if not isinstance(player_deck, list):

            if pl

            if isinstance(player_chest, list):
                player_chest = {c: player_chest.count(c.num) for c in self.data_combinations}

            p = Player(
                name=player_name,
                deck=player_deck
            )




    def init_card_df(self):
        def compile_card_data(card: Card):
            ring_0 = star_sign_ring_0 if (card.planet_0 in star_sign_ring_0) else star_sign_ring_1
            ring_1 = star_sign_ring_0 if (card.planet_1 in star_sign_ring_0) else star_sign_ring_1
            c_combos = self.data_combinations.get(card, {})
            data = {
                "num": card.num,
                "name": card.name,
                "type": card.type_,
                "type_s": card.type_simple,
                "atk": card.atk_points,
                "def": card.def_points,
                "cost": card.cost,
                "n_combos": len(c_combos),

                "p0": None,
                "p0_strong_against": None,
                "p0_weak_against": None,
                "p1": None,
                "p1_strong_against": None,
                "p1_weak_against": None,
                "in_ring_0": None,
                "in_ring_1": None,

                "RitualIdx": None,
                "RitualMonster": None,
                "RitualCard": None,
                "RitualSacrificeCard": None
            }
            if card.type_simple == "Monster":
                data.update({
                    "p0": card.planet_0,
                    "p0_strong_against": ring_0[(ring_0.index(card.planet_0) + 1) % len(ring_0)],
                    "p0_weak_against": ring_0[(ring_0.index(card.planet_0) - 1) % len(ring_0)],
                    "p1": card.planet_1,
                    "p1_strong_against": ring_1[(ring_1.index(card.planet_1) + 1) % len(ring_1)],
                    "p1_weak_against": ring_1[(ring_1.index(card.planet_1) - 1) % len(ring_1)],
                    "in_ring_0": (ring_0 == star_sign_ring_0) or (ring_1 in star_sign_ring_0),
                    "in_ring_1": (ring_0 == star_sign_ring_1) or (ring_1 in star_sign_ring_1)
                })

            return data

        def set_ritual_data(df, card):
            df_ritual_monster: pd.DataFrame = self.data_rituals.loc[self.data_rituals["n_Ritual_Monster"] == card.num]
            df_ritual_card: pd.DataFrame = self.data_rituals.loc[self.data_rituals["n_Ritual_Card"] == card.num]
            # df_sacrifices: pd.DataFrame = self.data_rituals.loc[f"{card.num}" in self.data_rituals["n_Sacrifices"].str.split(";")]
            # df_sacrifices: pd.DataFrame = pd.DataFrame()
            df_sacrifices: pd.DataFrame = self.data_rituals.loc[self.data_rituals["n_Sacrifices"].map(lambda lst: card.num in map(int, lst.split(";")))]
            is_rm = not df_ritual_monster.empty
            is_rc = not df_ritual_card.empty
            is_s = not df_sacrifices.empty
            if card.num == 1:
                print(f"card {card.num=}")
                print(f"{card}")
                print(f"df_ritual_monster")
                print(df_ritual_monster)
                print(f"df_ritual_card")
                print(df_ritual_card)
                print(f"df_sacrifices")
                print(df_sacrifices)
                print(f"{df_ritual_monster.index=}, {type(df_ritual_monster.index)=}")
                print(f"{df_ritual_card.index=}, {type(df_ritual_card.index)=}")
                print(f"{df_sacrifices.index=}, {type(df_sacrifices.index)=}")
                # print(f"{df_ritual_monster.index.item()=}, {type(df_ritual_monster.index.item())=}")
                # print(f"{df_ritual_card.index.item()=}, {type(df_ritual_card.index.item())=}")
                # print(f"{df_sacrifices.index.item()=}, {type(df_sacrifices.index.item())=}")
            df.loc[0, "RitualIdx"] = (df_ritual_monster.index.item() if is_rm else (
                df_ritual_card.index.item() if is_rc else (df_sacrifices.index.item() if is_s else None)))
            df.loc[0, "RitualMonster"] = is_rm
            df.loc[0, "RitualCard"] = is_rc
            df.loc[0, "RitualSacrificeCard"] = is_s

        dfs = []
        checked_cards = []
        for i, card in enumerate(self.data_combinations):
            c_combos = self.data_combinations[card]
            if card.num not in checked_cards:
                data = compile_card_data(card)
                dfs.append(pd.DataFrame([data]))

                # # df_ritual_monster: pd.DataFrame = self.data_rituals.loc[self.data_rituals["n_Ritual_Monster"] == card.num]
                # # df_ritual_card: pd.DataFrame = self.data_rituals.loc[self.data_rituals["n_Ritual_Card"] == card.num]
                # # # df_sacrifices: pd.DataFrame = self.data_rituals.loc[f"{card.num}" in self.data_rituals["n_Sacrifices"].str.split(";")]
                # # df_sacrifices: pd.DataFrame = pd.DataFrame()
                # # is_rm = not df_ritual_monster.empty
                # # is_rc = not df_ritual_card.empty
                # # is_s = not df_sacrifices.empty
                # # dfs[-1].loc[i, "RitualIdx"] = (df_ritual_monster.index.item() if is_rm else (df_ritual_card.index.item() if is_rc else (df_sacrifices.index.item() if is_s else None)))
                # # dfs[-1].loc[i, "RitualMonster"] = is_rm
                # # dfs[-1].loc[i, "RitualCard"] = is_rc
                # # dfs[-1].loc[i, "RitualSacrificeCard"] = is_s
                set_ritual_data(dfs[-1], card)

                checked_cards.append(card.num)
            for j, c_card in enumerate(c_combos):
                if c_card.num not in checked_cards:
                    c_data = compile_card_data(c_card)
                    dfs.append(pd.DataFrame([c_data]))
                    set_ritual_data(dfs[-1], c_card)
                    checked_cards.append(c_card.num)
                r_card = c_combos[c_card]
                if r_card.num not in checked_cards:
                    r_data = compile_card_data(r_card)
                    dfs.append(pd.DataFrame([r_data]))
                    set_ritual_data(dfs[-1], r_card)
                    checked_cards.append(r_card.num)
        return pd.concat(dfs, ignore_index=True)

    def num_2_card(self, num) -> Card:
        """
        num is expected to be the card.num attr, and therefor needs offset by 1
        :param num: Card.num attr
        :return: Card
        """
        return list(self.data_combinations)[num - 1]

    #     if not os.path.exists(self.path_data):
    #         self.initialize_data_file()
    #
    # def initialize_data_file(self):
    #     pth = self.path_data
    #     cards = self.get_avail_cards(min_of_each=6)
    #
    # def get_avail_cards(self, min_of_each: int = 1):
    #
    #

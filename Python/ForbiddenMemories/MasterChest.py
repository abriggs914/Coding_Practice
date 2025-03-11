import json
import os
import random

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


def parse_combinations_file(max_cards: Optional[int] = None):
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
            if (max_cards is not None) and (len(cards_2) >= max_cards):
                break

    if (max_cards is not None) and (len(cards_2) != max_cards):
        cards_2 = {c: cards_2[c] for i, c in enumerate(cards_2) if i <= max_cards}

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


# def random_deck(size: int = 40):
#     """
#     The player starts with a Deck of 40 cards, which are randomly selected from seven pools.
#
#     The 40 cards will be made up of:
#
#     16 monsters with ATK + DEF < 1100           # Grp 0
#     16 monsters with 1100 ≤ ATK + DEF < 1600    # grp 1
#     4 monsters with 1600 ≤ ATK + DEF < 2100     # grp 2
#     1 monster with 2100 ≤ ATK + DEF             # grp 3
#     1 pure Magic Card                           # grp 4
#     1 Field Magic Card                          # grp 5
#     1 Equip Card                                # grp 6
#     """
#     # return random.sample(known_cards[1:]*3, size)
#     print(f"random deck")
#     deck = []
#     groups = [[] for i in range(7)]
#     grp_sizes = [16, 16, 4, 1, 1, 1, 1]
#     for i, card in enumerate(known_cards[1:]):
#
#         if (card == known_cards[336]) or (card == known_cards[337]):
#             # dark hole and raigeki
#             continue
#         elif card in [known_cards[17], known_cards[18], known_cards[19], known_cards[20], known_cards[21]]:
#             # exodia pieces
#             groups[0].append(card)
#         else:
#
#             if card.type_simple == "Monster":
#                 ttl = card.atk_points + card.def_points
#                 print(f"{ttl=}, {card=}")
#                 if ttl < 1100:
#                     groups[0].extend([card]*3)
#                 elif 1100 <= ttl < 1600:
#                     groups[1].extend([card]*3)
#                 elif 1600 <= ttl < 2100:
#                     groups[2].extend([card]*3)
#                 else:
#                     groups[3].extend([card]*3)
#             elif (card.type_simple == "Magic") or (card.type_simple == "Trap"):
#                 groups[5].extend([card]*3)
#             elif card.type_simple == "Equip":
#                 groups[6].extend([card]*3)
#
#     groups[4].extend([known_cards[336], known_cards[337]])
#     for i, g_size in enumerate(grp_sizes):
#         deck += random.sample(groups[i], g_size)
#
#     # st.write(deck)
#     # print(deck)
#     # print(f"{list(map(len, groups))=}")
#
#     return deck

class MasterChest:

    def __init__(self, id_num: Optional[int] = None, load_max_cards: Optional[int] = None):

        self.id_num = next_id()
        self.path_data = os.path.join(root_path_master_chests, f"master_chest_{str(self.id_num).rjust(3, '0')}.json")
        
        self.load_max_cards = load_max_cards

        self.list_players = list()
        self.gener_card_ids = (i for i in range(1000000))

        self.data_combinations = parse_combinations_file(max_cards=self.load_max_cards)
        self.data_rituals = parse_rituals_file()
        self.df_card_data = self.init_card_df()

        self.load_master_chest_data()

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
        print(f"{list_players=}")
        for i, player_id in enumerate(list_players):
            player_data = player_datas.get(player_id, {})
            player_name = player_data.get("name", "UNKNOWN")
            player_description = player_data.get("description", "")
            player_deck = player_data.get("deck", [])
            player_chest = player_data.get("chest", {})

            print(f"{player_name=}")
            print(f"{player_deck=}")
            print(f"{player_chest=}")

            if isinstance(player_deck, dict):
                deck = []
                for j, c_id in enumerate(player_deck):
                    c_qty = player_deck.get(c_id, 1)
                    for k in range(c_qty):
                        # deck.append(self.num_2_card(c_id))
                        try:
                            deck.append(self.num_2_card(c_id))
                        except Exception:
                            pass
                player_deck = deck

            if isinstance(player_deck, list):
                player_deck_ = []
                for n in player_deck:
                    try:
                        player_deck_.append(self.num_2_card(n))
                    except Exception:
                        pass
                player_deck = player_deck_

            if isinstance(player_chest, list):
                player_chest = {c: player_chest.count(c.num) for c in self.data_combinations}

            p = Player(
                name=player_name,
                deck=player_deck,
                chest=player_chest
            )
            self.list_players.append(p)
            # print(f"{p=}")
            # print(f"{self.list_players=}")

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
        c = list(self.data_combinations)[num - 1]
        c = c.new_copy()
        c.master_chest_card_id = next(self.gener_card_ids)
        return c

    def process_possible_combos(self, hand: list[Card], do_test: bool = False):
        # print(f"\n{datetime.datetime.now():%Y-%m-%d %H:%M:%S}\n\n")

        def helper(nest, hand_):
            if nest >= 30:
                return []
            # print(f"{nest=}")
            new_combos = []
            hand_c = [c for c in hand_]
            for i, card_0_str in enumerate(hand_):
                if card_0_str is not None:
                    if do_test:
                        print(f"{card_0_str=}, {type(card_0_str)=}")
                    # card_0 = str_to_card(card_0_str)
                    card_0 = card_0_str
                    # p_combos = data_parsed_combinations_2[card_0]
                    p_combos = self.data_combinations[card_0]
                    for j, card_1_str in enumerate(hand_c):
                        # card_1 = str_to_card(card_1_str)
                        card_1 = card_1_str
                        if i != j:
                            # print(f"\t--{card_1}")
                            if card_1 in p_combos:
                                # combo_res = data_parsed_combinations[card_0][card_1]
                                combo_res = p_combos[card_1]
                                # print(f"\t\t{card_1} => {combo_res}")
                                pair_0 = [nest, combo_res, [card_0, card_1]]
                                pair_1 = [nest, combo_res, [card_1, card_0]]
                                # print(f"{pair_0=}\n{pair_1=}\n=>", end="")
                                if (pair_0 not in new_combos) and (pair_1 not in new_combos):
                                    # print("AAA")
                                    new_combos.append(pair_0)
                                # else:
                                #     print("BBB")
            # # if new_combos:
            # print(f"{new_combos=}, {hand_=}")
            new_new_combos = []
            for nest_, cr_, pr_ in new_combos:
                # new_hand = [c for c in hand_ if c not in pr_] + [cr_]
                new_hand = [c for c in hand_]
                if do_test:
                    print(f"\t\t{new_hand=}, {pr_=}, {cr_=}, {type(new_hand)}, {type(pr_)}, {type(cr_)}")
                    print(f"\t\t{list(map(type, new_hand))}, {list(map(type, pr_))}, {type(cr_)}")
                new_hand.remove(pr_[0])
                new_hand.remove(pr_[1])
                new_hand.append(cr_)
                # print(f"{new_hand=}")
                new_new_combos += helper(nest_ + 1, new_hand)
            return new_combos + new_new_combos

        combos = helper(0, hand)

        filtered_combos = []
        for nest_, cr_, pr_ in combos:
            pair_0 = [cr_, [pr_[0], pr_[1]], nest_]
            pair_1 = [cr_, [pr_[1], pr_[0]], nest_]
            if (pair_0 not in filtered_combos) and (pair_1 not in filtered_combos):
                filtered_combos.append(pair_0)
        combos = filtered_combos

        combos.sort(key=lambda tup: tup[0].atk_points, reverse=True)

        return combos

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


if __name__ == '__main__':
    chest = MasterChest(load_max_cards=None)
    p0, p1 = chest.list_players[-1], chest.list_players[0]
    print("p0.deck")
    print(p0.deck)

    p0.draw(5)
    print("p0.hand")
    print(p0.hand)

    print("combos")
    print(chest.process_possible_combos(p0.hand))

from typing import Optional

import streamlit as st


combinations_file = r"C:\Users\abrig\Documents\Coding_Practice\Java\ForbiddenMemories\combinations.txt"
known_cards = st.session_state.setdefault("known_cards", [])

gen_unkown_ids = (i for i in range(1000, 7001))


class Card:
    def __init__(
            self,
            num: Optional[int] = None,
            name: str = "UNKNOWN",
            type_: str = "UNKNOWN",
            attribute: str = "UNKNOWN",
            cost: int = 0,
            atk_points: int = 0,
            def_points: int = 0,
            planet_1: str = "UNKNOWN",
            planet_2: str = "UNKNOWN"
    ):
        if num is None:
            num = -next(gen_unkown_ids)
        self.num = num
        self.name = name
        self.type_ = type_
        self.attribute = attribute
        self.cost = cost
        self.atk_points = atk_points
        self.def_points = def_points
        self.planet_1 = planet_1
        self.planet_2 = planet_2

    def data(self):
        return [
            self.num,
            self.name,
            self.type_,
            self.attribute,
            self.cost,
            self.atk_points,
            self.def_points,
            self.planet_1,
            self.planet_2
        ]

    def __hash__(self):
        return self.num

    def __str__(self):
        return f"#{self.num} - {self.name}"

    def __repr__(self):
        return f"#{self.num} - {self.name}"


@st.cache_data()
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
    else:
        # print(f"COULD NOT MAKE CARD:")
        # print(f"UNKNOWN CARD {line=}")
        data = []

    c = Card(*data)
    num = c.num
    kc = st.session_state.get("known_cards")
    d = max(0, (num - len(kc)))
    while d > 0:
        kc.append(None)
        d -= 1
    # print(f"{d=}, {num=}, {len(kc)=}, {line=}")
    if kc[num - 1] is None:
        kc[num - 1] = c
        st.session_state.update({"known_cards": kc})
    # print(f"NEW CARD MADE:")
    # print(f"{c=}")
    # return c.num
    return c


@st.cache_data(ttl=None, show_spinner=True)
def parse_combinations_file():
    cards = {}
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
                if card.num not in cards:
                    cards[card.num] = {"combos": {}}

                if section_card is None:
                     section_card = card
                else:
                    if line.startswith("+"):
                        a = card
                    if line.startswith("="):
                        b = card
                    if (a is not None) and (b is not None):
                        cards[section_card.num]["combos"][a.num] = b.num
                        a = None
                        b = None

                # print(f"{card=}")
            else:
                # print(f"SEP")
                in_section = False
                section_card = None

    return cards


#         # cards = {}
#         # in_section = True
#         # a, b = None, None
#         # for i, line in enumerate(f.readlines()[:600]):
#         #     # check line is not separator '----'
#         #     line_sep = line.strip()
#         #     # st.write(f"A {i=}, {line_sep=}")
#         #     while line_sep.startswith("-"):
#         #         line_sep = line_sep.removeprefix("-")
#         #     # st.write(f"B {i=}, {line_sep=}")
#         #
#         #     # if in_section is None:
#         #     #     in_section = line
#         #
#         #     if line_sep:
#         #         # this is not a separator line
#         #         card = parse_card_line(line)
#         #         # print(f"{card_idx=}")
#         #         # card = known_cards[card_idx]
#         #
#         #         if in_section:
#         #             if card not in cards:
#         #                 cards[card] = {"id": i, "combos": {}}
#         #             in_section = False
#         #             sec_line = card
#         #         else:
#         #             if line.startswith("+"):
#         #                 a = card
#         #             else:
#         #                 b = card
#         #             if a is not None and b is not None:
#         #                 cards[sec_line]["combos"][a] = b
#         #     else:
#         #         in_section = True
#         #         sec_line = line
#         # return cards
#
#
# data_combinations = parse_combinations_file()
#
#
# if __name__ == '__main__':
#     st.write(data_combinations)
#     st.write(known_cards[:10])
#


data_parsed_combinations = parse_combinations_file()
st.write(len(data_parsed_combinations))
st.subheader("CARDS:")
st.write(len(known_cards))
st.write([str(c) for c in known_cards])

chains = []
rr = 0
for i, card in enumerate(known_cards[:3]):
    curr_card = card
    # chain = [card]
    nest = 1
    # to_check = [[card.num, c_.num] for c_ in data_parsed_combinations[curr_card.num]["combos"]]
    c_items = {}
    for k, v in data_parsed_combinations[card.num]["combos"].items():
        if v not in c_items.values():
            c_items[k] = v
    to_check = [[[card.num, k], v] for k, v in c_items.items()]
    # to_check = list()
    while to_check:
        rr += 1
        pth, curr = to_check.pop(0)
        # if data_parsed_combinations[curr]["combos"]:

        c_items = {}
        for k, v in data_parsed_combinations[curr]["combos"].items():
            if v not in c_items.values():
                c_items[k] = v
        for k, v in c_items.items():
            to_check.append([[*pth, curr, k], v])
        if not c_items:
            if (len(pth) + 1) >= 3:
                chains.append([*pth, curr])
        #     to_check.extend(list(set(data_parsed_combinations[curr_card]["combos"].values())))
        print(f"{i=}, {to_check=}")
        # n_, p_, lst = to_check.pop(0)
        # for j, c_ in enumerate(lst):
        #     if data_parsed_combinations[c_]["combos"]:
        #         to_check.append((n_ + 1, [*p_, c_], list(data_parsed_combinations[c_]["combos"].keys())))
        # if n_ > 2:
        #     chains.append(p_.copy())

        if rr >= 1000:
            print(f"rr quit")
            break

st.write("chains")
st.write(chains)

# for i in range(5):
#     c = known_cards[i]
#     st.write(f"{i=} {c=}")
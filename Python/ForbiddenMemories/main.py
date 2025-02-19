import os
import datetime
import random
from typing import Optional

import streamlit as st

from match import *
from player import *



deck_output = """["#241 - Dark Assailant 1200/1200","#197 - Mech Mole Zombie 500/400","#50 - Basic Insect 500/700","#609 - Bladefly 600/700","#547 - Griggle 350/300","#410 - Mechanical Spider 400/500","#156 - Hard Armor 300/1200","#387 - Mystic Lamp 400/300","#102 - Mask of Darkness 900/400","#283 - Holograh 1100/700","#190 - Akakieisu 1000/800","#137 - Mystery Hand 500/500","#579 - Abyss Flower 750/400","#402 - Monster Eye 250/350","#398 - Ooguchi 300/250","#214 - Kagemusha of the Blue Flame 800/400","#475 - Sinister Serpent 300/250","#475 - Sinister Serpent 300/250","#336 - Dark Hole M","#148 - The Shadow Who Controls the Dark 800/700","#276 - Ray & Temperature 1000/1000","#586 - Greenkappa 650/900","#524 - Star Boy 550/500","#335 - Yami 0/0","#101 - Wings of Wicked Flame 700/600","#421 - Cyber Commander 750/700","#202 - Air Marmot of Nefariousness 400/600","#202 - Air Marmot of Nefariousness 400/600","#226 - Skull Stalker 900/800","#134 - Mystical Capture Chain 700/700","#240 - The Drdek 700/800","#191 - LaLa Li-oon 600/600","#105 - Tomozaurus 500/400","#135 - Fiend's Hand 600/600","#547 - Griggle 350/300"]"""



app_title = "YU-GI-OH! Forbidden Memories"
unknown_card = Card(0)


st.set_page_config(page_title=app_title, layout="wide")


combinations_file = r"C:\Users\abrig\Documents\Coding_Practice\Java\ForbiddenMemories\combinations.txt"
if not os.path.exists(combinations_file):
    combinations_file = r"C:\Users\abriggs\Documents\Coding_Practice\Java\ForbiddenMemories\combinations.txt"
known_cards = st.session_state.setdefault("known_cards", [unknown_card])


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
        # print(f"{data=}")
    else:
        # print(f"COULD NOT MAKE CARD:")
        # print(f"UNKNOWN CARD {line=}")
        data = []

    c = Card(*data)
    # if c.type_simple != "Monster":
    #     print(f"AA {c}")
    num = c.num
    kc = st.session_state.get("known_cards")
    d = max(0, (1 + num - len(kc)))
    while d > 0:
        kc.append(None)
        d -= 1
    # print(f"{d=}, {num=}, {len(kc)=}, {line=}")
    if kc[num] is None:
        kc[num] = c
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


@st.cache_data(ttl=None, show_spinner=True)
def process_reverse_combinations():
    rcs = {}
    # n = 100
    # ww = len(data_parsed_combinations)
    # wwi = 0
    # # p0 = st.progress(0)
    # # p1 = st.progress(0)
    for card_0_num, card_0_data in data_parsed_combinations.items():
        # print(f"{card_0_num=}")
        card_0 = known_cards[card_0_num]
        lst_combos = card_0_data["combos"]
        gg = len(lst_combos)
        # p1.progress(0, text=str(card_0))
        for i, card_1 in enumerate(lst_combos):
            combo_result_num = data_parsed_combinations[card_0_num]["combos"][card_1]
            combo_result = known_cards[combo_result_num]
            # if (card_0_num == 571) or (card_1 == 571) or (combo_result_num == 571):
            #     st.write(f"Found {card_0}")
            if combo_result_num not in rcs:
                rcs[combo_result_num] = []
            pair_0 = (card_0_num, card_1)
            pair_1 = (card_1, card_0_num)
            if (pair_0 not in rcs[combo_result_num]) and (pair_1 not in rcs[combo_result_num]):
                rcs[combo_result_num].append(pair_0)
            # p1.progress(i / gg)
        # n -= 1
        # wwi += 1
        # # p0.progress(wwi / ww)
        # # if n <= 0:
        # #     break

    return rcs


@st.dialog(title=app_title, width="large")
def select_hand(size: int = 5, fresh: bool = True, deck_in: list[Card] = None):

    if deck_in is None:
        deck = [c for c in (known_cards[1:] if fresh else st.session_state.get(k_my_deck))]
    else:
        deck = deck_in
    curr_hand = [] if fresh else st.session_state.get(k_my_hand, [])

    k_multiselect_cards = "multiselect_cards"
    st.session_state.setdefault({
        f"kd_{k_multiselect_cards}": curr_hand[:size]
    })
    if not fresh:
        # your hand isnt in the deck if you arent drawing from a fresh deck
        deck.extend(curr_hand)

    # st.write(f"curr_hand")
    # st.write(curr_hand)
    # st.write([type(c) for c in curr_hand])
    # st.write("deck[300:311]")
    # st.write(deck[300:311])
    # st.write([type(c) for c in deck[300:311]])
    # st.write(f"kd_{k_multiselect_cards}")
    # st.write(st.session_state[f"kd_{k_multiselect_cards}"])
    # st.write([type(c) for c in st.session_state[f"kd_{k_multiselect_cards}"]])

    multiselect_cards = st.multiselect(
        label="Cards in Deck:",
        key=f"kd_{k_multiselect_cards}",
        options=deck,
        max_selections=size,
        placeholder=f"select {size} card(s)"
    )

    if st.button(
        label="save",
        key="kd_btn_save"
    ):
        st.session_state.update({
            k_my_hand: [c for c in st.session_state.get(f"kd_{k_multiselect_cards}", [])]
        })
        st.rerun()


def draw_hand(size: int = 5, clear: bool = True):

    deck = st.session_state.get(k_my_deck)[1:]
    hand = random.sample(deck, size)

    if clear:
        st.session_state.update({k_my_hand: hand})
    else:
        st.session_state.update({k_my_hand: st.session_state.get(k_my_hand, []) + hand})

    for i, card in enumerate(hand):
        deck.remove(card)

    st.session_state.update({k_my_deck: deck})


def reset_deck():
    st.session_state.update({
        k_my_deck: [c for c in known_cards],
        k_my_hand: []
    })


def process_possible_combos(hand: list[Card]):
    # print(f"\n{datetime.datetime.now():%Y-%m-%d %H:%M:%S}\n\n")

    def helper(nest, hand_):
        if nest >= 30:
            return []
        # print(f"{nest=}")
        new_combos = []
        hand_c = [c for c in hand_]
        for i, card_0_str in enumerate(hand_):
            print(f"{card_0_str=}, {type(card_0_str)=}")
            card_0 = str_to_card(card_0_str)
            p_combos = data_parsed_combinations[card_0.num]["combos"]
            for j, card_1_str in enumerate(hand_c):
                card_1 = str_to_card(card_1_str)
                if i != j:
                    # print(f"\t--{card_1}")
                    if card_1.num in p_combos:
                        combo_res = known_cards[data_parsed_combinations[card_0.num]["combos"][card_1.num]]
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
        pair_0 = [cr_, [pr_[0], pr_[1]]]
        pair_1 = [cr_, [pr_[1], pr_[0]]]
        if (pair_0 not in filtered_combos) and (pair_1 not in filtered_combos):
            filtered_combos.append(pair_0)
    combos = filtered_combos

    combos.sort(key=lambda tup: tup[0].atk_points, reverse=True)

    return combos


def set_my_hand():
    deck = st.session_state.get(k_my_deck, known_cards[1:]*3)
    select_hand(deck_in=deck)
    hand = st.session_state.get(k_my_hand)
    print(f"{hand=}")
    me.hand = hand
    st.session_state.update({k_player_0: me})


def update_merge_list(idx):
    keys = [f"k_toggle_merge_{i}" for i in range(len(my_hand))]
    do_merge = st.session_state.get(f"k_toggle_merge_{idx}", False)
    # for i in range(len(my_hand)):


@st.dialog(title=app_title, width="large")
def ask_deck(selected: Optional[list[Card]] = None):

    k_multiselect_deck_input = "multiselect_deck_input"
    k_list_in_deck_input = "list_in_deck_input"
    k_toggle_combine_ms_ta = "toggle_combine_ms_ta"
    options = list(map(str, sorted(known_cards[1:]*3, key=lambda c: str(c))))
    selected = [] if selected is None else selected
    stored = st.session_state.get(f"kd_{k_multiselect_deck_input}", [])
    st.session_state.update({f"kd_{k_multiselect_deck_input}": list(map(str, stored + (selected if selected else [])))})
    # st.write(st.session_state.get(f"kd_{k_multiselect_deck_input}"))
    # # st.write(type(st.session_state.get(f"kd_{k_multiselect_deck_input}")[0]))
    # st.write([c for c in known_cards[1:] if str(c).startswith("#544")])
    # st.write([c for c in options if "annon" in str(c)])
    # st.write([c for c in options if str(c).startswith("#544")])
    # st.write([type(c) for c in options if str(c).startswith("#544")])
    # st.write([type(c) for c in selected if str(c).startswith("#544")])
    # st.write([type(c) for c in options if "annon" in str(c)])
    # for c in selected[:1]:
    #     st.write(f"{type(c)}, {c} in options: {c in options}")
    #     for c2 in options[1300:1550]:
    #         print(f"{c} => {c2} == {c == c2}, {type(c)}, {type(c2)}")
    #         if c == c2:
    #             raise ValueError(f"FOUND {c}, {c2}")

    if st.button(
        label="START WITH DEMO DECK 2025-02-18",
        key="kd_btn_start_with_demo_deck_20250215"
    ):
        st.session_state.update({
            f"kd_{k_list_in_deck_input}": deck_output,
            f"kd_{k_multiselect_deck_input}": list(map(str, [known_cards[326], known_cards[635], known_cards[544]])),
            f"kd_{k_toggle_combine_ms_ta}": True
        })        

    multiselect_deck_input = st.multiselect(
        label="Select your deck:",
        key=f"kd_{k_multiselect_deck_input}",
        options=options,
        max_selections=40
    )

    list_in_deck_input = st.text_area(
        label="Paste a list:",
        key=f"kd_{k_list_in_deck_input}"
    )

    toggle_combine_ms_ta = st.toggle(
        label="Combine multi-select input with text-area input?",
        key=f"kd_{k_toggle_combine_ms_ta}"
    )

    parsed = []
    if toggle_combine_ms_ta:
        p = []
        st.write("Interpreted:")
        try:
            p = eval(list_in_deck_input)
            # for i, crd in enumerate(parsed):
            #     num = int(crd.split(" ")[0].removeprefix("#"))
            #     parsed.append(known_cards[num])

        except Exception as e:
            p = []
        parsed = multiselect_deck_input + p
        st.write(parsed)
    else:
        if len(st.session_state.get(f"kd_{k_multiselect_deck_input}")) == 40:
            parsed = multiselect_deck_input
        elif list_in_deck_input:
            parsed = []
            st.write("Interpreted:")
            try:
                parsed = eval(list_in_deck_input)
                # for i, crd in enumerate(parsed):
                #     num = int(crd.split(" ")[0].removeprefix("#"))
                #     parsed.append(known_cards[num])

            except Exception as e:
                parsed = []
                st.error(e)

            st.write(parsed)

    st.write(f"{len(parsed)} / 40 Card(s) chosen")
    if 5 <= len(parsed) <= 40:
        if st.button(
            label="save",
            key=f"k_btn_save_deck_input"
        ):
            st.session_state.update({
                k_my_deck: [c for c in parsed]
            })
            st.rerun()


def random_deck(size: int = 40):
    return random.sample(known_cards[1:]*3, size)


def str_to_card(card_str: str) -> Card:

    if not isinstance(card_str, str):
        # msg = [
        #     f"{card_str=}",
        #     f"{card_str.__class__=}",
        #     f"{type(card_str)=}",
        #     f"{isinstance(card_str, Card)=}",
        #     f"{type(unknown_card)=}",
        #     f"{(type(card_str) == type(unknown_card))=}",
        #     f"{(type(card_str) == Card)=}",
        #     f"{(Card)=}",
        #     f"{(Card.__class__)=}",
        #     f"{id(card_str)=}",
        #     f"{id(Card)=}"
        # ]
        # st.write(msg)
        # print(msg)

        # if isinstance(card_str, Card):
        # This doesnt work due to streamlit?

        # st.write(f"{str(card_str.__class__)=}")
        # st.write(f"{str(Card)=}")
        if str(card_str.__class__) == str(Card):
            # print(f"\t\tAAA")
            return card_str
        else:
            raise ValueError(f"A ERROR CONVERTING '{card_str}' to card, {type(card_str)=}.")
            st.stop()

    try:
        # Card __repr__ pattern: "#XXX - CardName Atk/Def"
        spl = card_str.split(" ")
        # print(f"{card_str=}, {spl=}")
        num = int(spl[0].removeprefix("#"))
        return known_cards[num]
    except Exception as e:
        st.write(f"B ERROR CONVERTING '{card_str}' to card.")
        st.error(e)
        st.stop()



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
reverse_combos = process_reverse_combinations()

k_my_deck = "my_game_deck"
k_my_hand = "my_game_hand"
k_btn_draw_hand = "btn_draw_hand"
k_btn_select_hand = "btn_select_hand"

k_player_0 = "player_0"
k_player_1 = "player_1"
k_match = "match"

k_opp_deck = "opp_game_deck"

if k_my_deck not in st.session_state:
    ask_deck()
if k_opp_deck not in st.session_state:
    st.session_state.update({k_opp_deck: random_deck()})


if st.sidebar.button(
    label="Edit Deck",
    key="btn_edit_deck"
):
    ask_deck(selected=st.session_state.get(k_my_deck, []))

me, cpu, match = [None] * 3
my_deck = list(map(str_to_card, st.session_state.get(k_my_deck, [])))

if my_deck:


    # st.session_state.setdefault(k_my_deck, random_deck())
    # my_deck = [known_cards[16], known_cards[16], known_cards[425], known_cards[425], known_cards[4]]
    # n_cards_in_deck = len(st.session_state.get(k_my_deck, []))
    draw_size = 5

    if not st.session_state.get(k_player_0):
        me = Player("ME", deck=st.session_state.get(k_my_deck), card_parser=str_to_card)
        print(f"1 create k_player_0, {me}")
        me = st.session_state.update({k_player_0: me})
        print(f"2 create k_player_0, {me}")
    if not st.session_state.get(k_player_1):
        cpu = Player("CPU", deck=st.session_state.get(k_opp_deck), card_parser=str_to_card)
        print(f"1 create k_player_1, {cpu}")
        cpu = st.session_state.update({k_player_1: cpu})
        print(f"create k_player_1, {cpu}")

    me = st.session_state[k_player_0]
    cpu = st.session_state[k_player_1]

    if not st.session_state.get(k_match):
        print(f"create match")
        match = Match(me, cpu)
        match = st.session_state.update({k_match: match})

    match = st.session_state[k_match]

    st.write("me")
    st.write(me)
    st.write("cpu")
    st.write(cpu)
    st.write("match")
    st.write(match)

    if not match.started:
        if st.button(
            label="start new match",
            key="k_btn_new_game"
        ):
            st.session_state.pop(k_match)

    is_my_turn = match.turn == me
    turn_phase = match.turn_phase
    cpu_hand = cpu.hand
    my_hand = me.hand
    my_monsters = me.monsters
    my_magic = me.magic
    my_deck = me.deck

    
    # Draw Board
    header_columns = st.columns([0.8, 0.05, 0.15])
    col_scoreboard = header_columns[2]
    col_turn_info = header_columns[1]
    cont_score_cpu = col_scoreboard.container(border=1)
    cont_score_me = col_scoreboard.container(border=1)

    cols_score_details_cpu = cont_score_cpu.columns([0.35, 0.65])
    cols_score_details_me = cont_score_me.columns([0.35, 0.65])

    col_turn_info.write(f"Match #{match.id_num}")
    col_turn_info.write(f"Turn #{match.turn_num + 1}")
    col_turn_info.write(f"{turn_phase}")
    pref_me = f"{' * ' if is_my_turn else ''}"
    pref_cpu = f"{' * ' if not is_my_turn else ''}"
    cols_score_details_cpu[0].write(f"{pref_cpu}{cpu.name}")
    cols_score_details_cpu[1].write(cpu.hp)
    cols_score_details_me[0].write(f"{pref_me}{me.name}")
    cols_score_details_me[1].write(me.hp)

    grid_opp_hand = st.columns(5, border=1)
    grid_columns = st.columns(5)
    grid_field = [[col.container(border=1) for col in grid_columns] for i in range(4)]
    grid_my_hand = st.columns(5, border=1)

    # my_hand = st.session_state.get(k_my_hand)
    # st.write(my_hand)

    k_btn_end_turn = "btn_end_turn"
    btn_end_turn = st.button(
        label="end turn",
        key=f"k_{k_btn_end_turn}",
        on_click=match.next_turn
    )

    st.write(my_deck)

    k_btn_set_my_hand = "btn_set_my_hand"
    btn_set_my_hand = st.sidebar.button(
        label="set my hand",
        key=f"k_{k_btn_set_my_hand}",
        on_click=set_my_hand
    )

    for i, card in enumerate(cpu_hand):
        grid_opp_hand[i].write(card)

    for i in range(5):
        if (len(cpu.magic) > i) and (cpu.magic[i] is not None):
            card = cpu.magic[i]
            grid_field[0][i].write(card)
        else:
            grid_field[0][i].write(f"{i=}")

    for i in range(5):
        if (len(cpu.monsters) > i) and (cpu.monsters[i] is not None):
            card = cpu.monsters[i]
            grid_field[1][i].write(card)
        else:
            grid_field[1][i].write(f"{i=}")

    for i in range(5):
        if (len(me.monsters) > i) and (me.monsters[i] is not None):
            card = me.monsters[i]
            grid_field[2][i].write(card)
            k_btn_shift_mode = "btn_shift_mode"
            btn_shift_mode = grid_field[2][i].button(
                label="flip",
                key=f"k_{k_btn_shift_mode}",
                on_click=flip_card
            )
        else:
            grid_field[2][i].write(f"{i=}")

    for i in range(5):
        if (len(me.magic) > i) and (me.magic[i] is not None):
            card = me.magic[i]
            grid_field[3][i].write(card)
        else:
            grid_field[3][i].write(f"{i=}")

    # for i in range(4):
    #     for j in range(5):
    #         grid_field[i][j].write(f"{i=}, {j=}")

    cm = sum([st.session_state.get(f"k_toggle_merge_{i}", False) for i in range(len(my_hand))])
    for i, card in enumerate(my_hand):
        grid_my_hand[i].write(card)
        btn_play_card = grid_my_hand[i].button(
            label="play",
            key=f"k_btn_play_card_{i}",
            on_click=lambda c=card: me.play_card(str_to_card(c))
        )
        # if st.session_state.get(f"k_toggle_merge_{i}", False):
        #     st.write()
        # toggle_merge_card = grid_my_hand[i].toggle(
        #     label=f"merge {cm + 1}",
        #     key=f"k_toggle_merge_{i}",
        #     on_change=lambda: update_merge_list(i)
        # )

    st.write("Hand & Monsters:")
    avail_combo_cards = list(map(str_to_card, my_hand + me.monsters))
    st.write(my_hand + me.monsters)
    
    st.write("avail_combo_cards")
    st.write(avail_combo_cards)
    st.write(list(map(type, avail_combo_cards)))
    possible_combos = process_possible_combos(avail_combo_cards)
    st.write("possible_combos")
    st.write(possible_combos)


    cards_available = st.multiselect(
        label="Cards",
        key="k_multiselect_cards_available",
        options=known_cards[1:],
        max_selections=10
    )

    if cards_available:
        st.write("Combos available:")
        st.write(process_possible_combos(cards_available))

    selectbox_investigate_card = st.selectbox(
        label="investigate card",
        key="k_selectbox_investigate_card",
        options=known_cards[1:]
    )
    if selectbox_investigate_card:
        cl = [[known_cards[k], known_cards[v]] for k, v in data_parsed_combinations[selectbox_investigate_card.num]["combos"].items()]
        cl.sort(key=lambda tup: tup[1].atk_points, reverse=True)
        cl = [[str(c0), str(c1)] for c0, c1 in cl]
        st.write(cl)


    # Handle Moves

    if not is_my_turn:
        if turn_phase == turn_phases[0]:
            # START
            # do nothing
            pass
        elif turn_phase == turn_phases[1]:
            # DRAW
            # draw up to 5 cards
            n_to_draw = draw_size - len(cpu_hand)
            cpu.draw(n=n_to_draw)
        elif turn_phase == turn_phases[2]:
            # PLAY1
            # by default force a random play, then skip 'ATTACK' & 'PLAY2'
            cpu.play_random_card()
        elif turn_phase == turn_phases[3]:
            # Attack
            pass
        elif turn_phase == turn_phases[4]:
            # PLAY2
            pass
        elif turn_phase == turn_phases[5]:
            # END
            match.next_turn()
        else:
            st.error(f"Unkown turn phase {turn_phase}")
            st.stop()

        match.advance_phase()
        st.rerun()

    else:
        do_rerun = True
        if turn_phase == turn_phases[0]:
            # START
            # do nothing
            pass
        if turn_phase == turn_phases[1]:
            # DRAW
            # draw up to 5 cards
            n_to_draw = draw_size - len(my_hand)
            me.draw(n=n_to_draw)
        elif turn_phase == turn_phases[2]:
            # PLAY1
            # by default force a random play, then skip 'ATTACK' & 'PLAY2'
            # wait for input
            do_rerun = False
        elif turn_phase == turn_phases[3]:
            # Attack
            # wait for input
            do_rerun = False
        elif turn_phase == turn_phases[4]:
            # PLAY2
            # wait for input
            do_rerun = False
        elif turn_phase == turn_phases[5]:
            # END
            match.next_turn()
        else:
            st.error(f"Unkown turn phase {turn_phase}")
            st.stop()
        
        if do_rerun:
            match.advance_phase()
            st.rerun()

    # cont_deck = st.container(border=1)
    # cont_deck.write(f"{n_cards_in_deck} card(s) left")
    # cont_deck_cols = cont_deck.columns(2)
    # btn_reset_deck = cont_deck_cols[0].button(
    #     label="reset deck",
    #     key="k_btn_reset_deck",
    #     on_click=reset_deck
    # )
    #
    #
    # if n_cards_in_deck >= draw_size:
    #     btn_draw_hand = cont_deck_cols[1].button(
    #         label="Draw",
    #         key=f"k_{k_btn_draw_hand}",
    #         on_click=lambda: draw_hand(size=draw_size, clear=True)
    #     )
    #     btn_select_hand = cont_deck_cols[1].button(
    #         label="Select your Hand",
    #         key=f"k_{k_btn_select_hand}",
    #         on_click=lambda: select_hand(deck_in=my_deck)
    #     )
    # else:
    #     st.write("Not enough cards left to draw!")

    # st.write(list(set([c.type_ for c in known_cards])))

    

else:
    st.write("?")

st.session_state.update({
    k_player_0: me,
    k_player_1: cpu,
    k_match: match
})

# # st.write("len(data_parsed_combinations)")
# # st.write(len(data_parsed_combinations))
# # st.subheader("CARDS:")
# # st.write(len(known_cards))
# # st.write([str(c) for c in known_cards])
# #
# #
# # # def validate():
# # #     k0 = "k_selectbox_card_0"
# # #     k1 = "k_selectbox_card_1"
# # #     if st.session_state.get(k0):
#
#
#
# selectbox_card_0 = st.selectbox(
#     label="Choose a card:",
#     key="k_selectbox_card_0",
#     options=known_cards[310:316]
#     # ,
#     # on_change=validate
# )
#
# if selectbox_card_0:
#     st.write("selectbox_card_0")
#     st.write(selectbox_card_0)
#     combo_options = data_parsed_combinations[selectbox_card_0.num]["combos"]
#     combo_options = [known_cards[n] for n in combo_options]
#     st.write("combo_options")
#     st.write(combo_options)
#
#     if combo_options:
#         selectbox_card_1 = st.selectbox(
#             label="Choose another card:",
#             key="k_selectbox_card_1",
#             options=combo_options
#         )
#
#         st.write(data_parsed_combinations[selectbox_card_0.num]["combos"])
#         result = data_parsed_combinations[selectbox_card_0.num]["combos"][selectbox_card_1.num]
#         result = known_cards[result]
#         st.write("Result:")
#         st.write(result)
#
#
# # st.write("reverse_combos")
# # st.write(reverse_combos)
# st.write("reverse_combos 2")
# st.write(list(reverse_combos.keys()))
#
# num_in_q = 314
# # num_in_q = 663
# st.write(f"{len(reverse_combos[num_in_q])}")
# st.write(f"{reverse_combos[num_in_q]}")
# st.write(f"{known_cards[num_in_q]} = {known_cards[reverse_combos[num_in_q][0][0]]} + {known_cards[reverse_combos[num_in_q][0][1]]}")
# # st.write(f"{known_cards[num_in_q]} = {known_cards[reverse_combos[num_in_q][0][0] - 1]} + {known_cards[reverse_combos[num_in_q][0][1] - 1]}")
# # st.write(f"{known_cards[num_in_q + 1]} = {known_cards[reverse_combos[num_in_q][0][0] - 1]} + {known_cards[reverse_combos[num_in_q][0][1] - 1]}")
#
# # chains = []
# # rr = 0
# # for i, card in enumerate(known_cards[:3]):
# #     curr_card = card
# #     # chain = [card]
# #     nest = 1
# #     # to_check = [[card.num, c_.num] for c_ in data_parsed_combinations[curr_card.num]["combos"]]
# #     c_items = {}
# #     for k, v in data_parsed_combinations[card.num]["combos"].items():
# #         if v not in c_items.values():
# #             c_items[k] = v
# #     to_check = [[[card.num, k], v] for k, v in c_items.items()]
# #     # to_check = list()
# #     while to_check:
# #         rr += 1
# #         pth, curr = to_check.pop(0)
# #         # if data_parsed_combinations[curr]["combos"]:
# #
# #         c_items = {}
# #         for k, v in data_parsed_combinations[curr]["combos"].items():
# #             if v not in c_items.values():
# #                 c_items[k] = v
# #         for k, v in c_items.items():
# #             to_check.append([[*pth, curr, k], v])
# #         if not c_items:
# #             if (len(pth) + 1) >= 3:
# #                 chains.append([*pth, curr])
# #         #     to_check.extend(list(set(data_parsed_combinations[curr_card]["combos"].values())))
# #         print(f"{i=}, {to_check=}")
# #         # n_, p_, lst = to_check.pop(0)
# #         # for j, c_ in enumerate(lst):
# #         #     if data_parsed_combinations[c_]["combos"]:
# #         #         to_check.append((n_ + 1, [*p_, c_], list(data_parsed_combinations[c_]["combos"].keys())))
# #         # if n_ > 2:
# #         #     chains.append(p_.copy())
# #
# #         if rr >= 1000:
# #             print(f"rr quit")
# #             break
# #
# # st.write("chains")
# # st.write(chains)
# #
# # # for i in range(5):
# # #     c = known_cards[i]
# # #     st.write(f"{i=} {c=}")
import os
import random

from match import *
from player import *



deck_output_20250218 = """["#241 - Dark Assailant 1200/1200","#197 - Mech Mole Zombie 500/400","#50 - Basic Insect 500/700","#609 - Bladefly 600/700","#547 - Griggle 350/300","#410 - Mechanical Spider 400/500","#156 - Hard Armor 300/1200","#387 - Mystic Lamp 400/300","#102 - Mask of Darkness 900/400","#283 - Holograh 1100/700","#190 - Akakieisu 1000/800","#137 - Mystery Hand 500/500","#579 - Abyss Flower 750/400","#402 - Monster Eye 250/350","#398 - Ooguchi 300/250","#214 - Kagemusha of the Blue Flame 800/400","#475 - Sinister Serpent 300/250","#475 - Sinister Serpent 300/250","#336 - Dark Hole M","#148 - The Shadow Who Controls the Dark 800/700","#276 - Ray & Temperature 1000/1000","#586 - Greenkappa 650/900","#524 - Star Boy 550/500","#335 - Yami 0/0","#101 - Wings of Wicked Flame 700/600","#421 - Cyber Commander 750/700","#202 - Air Marmot of Nefariousness 400/600","#202 - Air Marmot of Nefariousness 400/600","#226 - Skull Stalker 900/800","#134 - Mystical Capture Chain 700/700","#240 - The Drdek 700/800","#191 - LaLa Li-oon 600/600","#105 - Tomozaurus 500/400","#135 - Fiend's Hand 600/600","#547 - Griggle 350/300"]"""
deck_output_20250220 = """["#579 - Abyss Flower 750/400","#202 - Air Marmot of Nefariousness 400/600","#411 - Bat 300/350","#609 - Bladefly 600/700","#548 - Bone Mouse 400/300","#178 - Claw Reacher 1000/800","#539 - Corroding Shark 1100/700","#395 - Dancing Elf 300/200","#336 - Dark Hole M","#120 - Dream Clown 1200/900","#154 - Fire Reaper 700/500","#154 - Fire Reaper 700/500","#644 - Flame Viper 400/450","#210 - Hinotama Soul 600/500","#227 - Hitodenchak 600/700","#306 - Insect Armor with Laser Cannon E","#107 - Kageningen 800/600","#58 - Kuriboh 300/200","#58 - Kuriboh 300/200","#158 - Man Eater 800/600","#501 - Man-eater Bug 450/600","#501 - Man-eater Bug 450/600","#102 - Mask of Darkness 900/400","#197 - Mech Mole Zombie 500/400","#245 - Meda Bat 800/400","#212 - Meotoko 700/600","#222 - Midnight Fiend 800/600","#516 - Muka Muka 600/300","#8 - Mushroom Man 800/600","#143 - Necrolancer the Timelord 800/900","#604 - Obese Marmot of Nefariousness 750/800","#398 - Ooguchi 300/250","#398 - Ooguchi 300/250","#333 - Sogen M","#444 - Turu-Purun 450/500","#606 - Twin Long Rods #2 850/700","#231 - Wood Clown 800/1200","#563 - Wretched Ghost of the Attic 550/400","#452 - Zarigun 600/700","#395 - Dancing Elf 300/200"]"""
deck_output_20250222 = """["#202 - Air Marmot of Nefariousness 400/600","#167 - Ancient Jar 400/200","#289 - Change Slime 400/300","#421 - Cyber Commander 750/700","#395 - Dancing Elf 300/200","#336 - Dark Hole M","#123 - Dark Plant 300/400","#109 - Goddess with the Third Eye 1200/1000","#547 - Griggle 350/300","#422 - Jinzo #7 500/400","#214 - Kagemusha of the Blue Flame 800/400","#107 - Kageningen 800/600","#211 - Kaminarikozou 700/600","#192 - Key Mace 400/300","#485 - Korogashi 550/400","#58 - Kuriboh 300/200","#191 - LaLa Li-oon 600/600","#397 - Leghul 300/350","#397 - Leghul 300/350","#158 - Man Eater 800/600","#182 - Masked Clown 500/700","#212 - Meotoko 700/600","#222 - Midnight Fiend 800/600","#402 - Monster Eye 250/350","#282 - Mystical Sheep #2 800/1000","#129 - Nemuriko 800/700","#208 - Petit Angel 600/900","#208 - Petit Angel 600/900","#203 - Phantom Ghost 600/800","#9 - Shadow Specter 500/200","#524 - Star Boy 550/500","#309 - Steel Shell E","#257 - Stone Armadiller 800/1200","#257 - Stone Armadiller 800/1200","#265 - The Furious Sea King 800/700","#152 - The Melting Red Shadow 500/700","#224 - Trap Master 500/1100","#606 - Twin Long Rods #2 850/700","#334 - Umi M","#130 - Weather Control 600/400"]"""
deck_output_memory_card_original = """["#35 - Dark Magician 2500/2100","#35 - Dark Magician 2500/2100","#35 - Dark Magician 2500/2100","#308 - Beast Fangs E","#385 - Bickuribox 2300/2000","#39 - Curse of Dragon 2000/1500","#463 - Electric Snake 800/900","#690 - Fake Trap T","#690 - Fake Trap T","#38 - Gaia the Fierce Knight 2300/2100","#38 - Gaia the Fierce Knight 2300/2100","#38 - Gaia the Fierce Knight 2300/2100","#427 - Kaiser Dragon 2300/2000","#458 - Kaminari Attack 1900/1400","#458 - Kaminari Attack 1900/1400","#458 - Kaminari Attack 1900/1400","#211 - Kaminarikozou 700/600","#366 - Labyrinth Wall 0/3000","#652 - Magical Labyrinth E","#409 - Metal Dragon 1850/1700","#713 - Meteor B. Dragon 3500/2000","#713 - Meteor B. Dragon 3500/2000","#713 - Meteor B. Dragon 3500/2000","#712 - Meteor Dragon 1800/2000","#332 - Mountain M","#332 - Mountain M","#45 - Oscillo Hero #2 1000/500","#45 - Oscillo Hero #2 1000/500","#45 - Oscillo Hero #2 1000/500","#337 - Raigeki M","#337 - Raigeki M","#82 - Red-eyes B. Dragon 2400/2000","#82 - Red-eyes B. Dragon 2400/2000","#82 - Red-eyes B. Dragon 2400/2000","#358 - Seiyaryu 2500/2300","#358 - Seiyaryu 2500/2300","#707 - Skull Knight 2650/2250","#707 - Skull Knight 2650/2250","#707 - Skull Knight 2650/2250","#335 - Yami M"]"""



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
    cards_2 = {}
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
                    cards_2[card] = {}

                if section_card is None:
                     section_card = card
                else:
                    if line.startswith("+"):
                        a = card
                    if line.startswith("="):
                        b = card
                    if (a is not None) and (b is not None):
                        if section_card not in cards_2:
                            cards_2[section_card] = {}
                        cards[section_card.num]["combos"][a.num] = b.num
                        cards_2[section_card][a.num] = b.num
                        a = None
                        b = None

                # print(f"{card=}")
            else:
                # print(f"SEP")
                in_section = False
                section_card = None

    return cards, cards_2


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

    n_cards = len(st.session_state.get(f"kd_{k_multiselect_cards}", []))
    if n_cards == size:
        if st.button(
            label="save",
            key="kd_btn_save"
        ):
            st.session_state.update({
                k_my_hand: [c for c in st.session_state.get(f"kd_{k_multiselect_cards}", [])]
            })
            st.rerun()
    else:
        st.write(f"{size - n_cards} card(s) left to choose.")


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


def process_possible_combos(hand: list[Card], do_test: bool = False):
    # print(f"\n{datetime.datetime.now():%Y-%m-%d %H:%M:%S}\n\n")

    def helper(nest, hand_):
        if nest >= 30:
            return []
        # print(f"{nest=}")
        new_combos = []
        hand_c = [c for c in hand_]
        for i, card_0_str in enumerate(hand_):
            if do_test:
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
    hand = st.session_state.get(k_my_hand, [None for i in range(5)])
    print(f"{hand=}")
    me.hand = hand
    st.session_state.update({k_player_0: me})
    st.rerun()


# def update_merge_list(idx):
#     keys = [f"k_toggle_merge_{i}" for i in range(len(my_hand))]
#     do_merge = st.session_state.get(f"k_toggle_merge_{idx}", False)
#     # for i in range(len(my_hand)):


def play_random_card(player: Player):
    if do_test:
        print(f"Player.play_random_card")
    card = random.choice(player.get_hand())
    card.planet = random.choice([card.planet_0, card.planet_1])
    card.atk_mode = random.choice([0, 1]) == 0

    # completely random - if the selected card happens to be a non-monster, then it may try to play it automatically
    if card.type_simple == "Trap":
        # by default trap cards must be set before they can be activated.
        card.face_down = True
    else:
        card.face_down = random.choice([0, 1]) == 0

    play_card(player, card)


def play_card(player: Player, card: Card):
    # if do_test:
    print(f"play_card")
    print(f"{cpu}")
    print(f"{player}")
    print(f"{cpu.name}")
    print(f"{player.name}")
    print(f"{player.get_hand()=}")
    print(list(map(type, player.get_hand())))
    print(f"{card=}")
    player.get_hand().remove(card)
    card_type = card.type_
    k0 = k_cpu_combo_play_cards
    k1 = k_my_combo_play_cards
    print(f"{k0=}, {st.session_state.get(k0)=}")
    print(f"{k1=}, {st.session_state.get(k1)=}")
    k = k_cpu_combo_play_cards if player == cpu else k_my_combo_play_cards
    lst = st.session_state.setdefault(k, [])
    print(f"{k=}")
    print(f"{lst=}")

    if lst:
        c1 = lst[0]
        c2 = None
        for i, c2 in enumerate(lst[1:], start=1):
            c_2 = c2
            combination = known_cards[data_parsed_combinations.get(c1, {}).get("combos", {}).get(c2, None)]
            print(f"{i=}, {c2=}, {c_2=}, {combination=}")
            if combination:
                player.get_hand().remove(c1)
                c1 = combination
            else:
                c1 = c2
        # if c2 is not None:
        #     player.get_hand().append(c1)
        card = c1

    st.session_state.update({k: []})

    if card.type_simple == "Monster":
        ask_sign(player, card)
        k_slider = f"slider_sign_{card.num}"
        k_toggle_facedown = f"toggle_facedown_{card.num}"
        k_toggle_attack_mode = f"toggle_attack_mode_{card.num}"
        idx = player.next_monster_idx()
        player.monsters.insert(idx, {
            "card": card,
            "planet": st.session_state.get(k_slider, card.planet_0),
            "face_down": st.session_state.get(k_toggle_facedown, False),
            "attack_mode": st.session_state.get(k_toggle_attack_mode, True)
        })
    else:
        idx = player.next_magic_idx()
        player.magic.insert(idx, {
            "card": card,
            "face_down": False
        })


@st.dialog(title=f"Select Sign")
def ask_sign(player: Player, card: Card):
    if do_test:
        print(f"Player.ask_sign")
    st.write(f"Select a sign for {card}:")
    options = [card.planet_0, card.planet_1]
    card.planet = card.planet_0
    cols = st.columns([0.75, 0.25])
    k_slider = f"slider_sign_{card.num}"
    cols[0].select_slider(
        label="Signs",
        options=options,
        key=f"k_{k_slider}"
    )

    k_toggle_facedown = "toggle_facedown"
    k_toggle_attack_mode = f"toggle_attack_mode_{card.num}"
    st.session_state.setdefault(k_toggle_facedown, False)
    st.session_state.setdefault(k_toggle_attack_mode, True)
    toggle_facedown = st.toggle(
        label="Facedown:",
        key=f"k_{k_toggle_facedown}"
    )
    toggle_attack_mode = st.toggle(
        label="Attack Mode:",
        key=f"k_{k_toggle_attack_mode}"
    )

    st.session_state.update({
        k_toggle_facedown: f"k_{k_toggle_facedown}",
        k_toggle_attack_mode: f"k_{k_toggle_attack_mode}",
        k_slider: f"k_{k_slider}"
    })

    if cols[1].button(
        label="save",
        key=f"k_btn_save_sign_{card.num}"
    ):
        card.planet = st.session_state.get(f"k_{k_slider}", card.planet_0)
        card.face_down = st.session_state.get(f"k_{k_toggle_facedown}", card.face_down)
        card.attack_mode = st.session_state.get(f"k_{k_toggle_attack_mode}", card.attack_mode)
        st.rerun()


def new_game():
    match: Match = st.session_state.get(k_match, None)
    if match:
        match_id = match.id_num
        me: Player = st.session_state.get(k_player_0, None)
        if me:
            me.end_match(match_id)
        cpu: Player = st.session_state.get(k_player_1, None)
        if cpu:
            cpu.end_match(match_id)

    st.session_state.update({
        k_match: None,
        k_player_0: None,
        k_player_1: None
    })
    st.rerun()


@st.dialog(title=app_title, width="large")
def ask_deck2(selected: Optional[list[Card]] = None):

    k_multiselect_deck_input = "multiselect_deck_input"
    k_list_in_deck_input = "list_in_deck_input"
    k_toggle_combine_ms_ta = "toggle_combine_ms_ta"
    # options = list(map(str, sorted(known_cards[1:]*3, key=lambda c: str(c))))
    options = sorted(known_cards[1:]*3, key=lambda c: str(c))
    selected = [] if selected is None else selected
    stored = st.session_state.get(f"kd_{k_multiselect_deck_input}", [])
    st.session_state.update({f"kd_{k_multiselect_deck_input}": stored + (selected if selected else [])})

    try:
        st.write(f"{stored[:3]=}, {list(map(type, stored[:3]))=}")
        st.write(f"{selected[:3]=}, {list(map(type, selected[:3]))=}")
        st.write(f"{options[833:838]=}, {list(map(type, options[833:838]))=}")
        st.write(f"{known_cards[:3]=}, {list(map(type, known_cards[:3]))=}")
        st.write(f"{len(options)=}")
        st.write(f"{len(known_cards)=}")
        st.write(f"{stored[0] in options=}")
    except Exception:
        pass

    # # st.write(st.session_state.get(f"kd_{k_multiselect_deck_input}"))
    # # # st.write(type(st.session_state.get(f"kd_{k_multiselect_deck_input}")[0]))
    # # st.write([c for c in known_cards[1:] if str(c).startswith("#544")])
    # # st.write([c for c in options if "annon" in str(c)])
    # # st.write([c for c in options if str(c).startswith("#544")])
    # # st.write([type(c) for c in options if str(c).startswith("#544")])
    # # st.write([type(c) for c in selected if str(c).startswith("#544")])
    # # st.write([type(c) for c in options if "annon" in str(c)])
    # # for c in selected[:1]:
    # #     st.write(f"{type(c)}, {c} in options: {c in options}")
    # #     for c2 in options[1300:1550]:
    # #         print(f"{c} => {c2} == {c == c2}, {type(c)}, {type(c2)}")
    # #         if c == c2:
    # #             raise ValueError(f"FOUND {c}, {c2}")
    #
    # cols_demo_decks = st.columns(3)
    # with cols_demo_decks[0]:
    #     if st.button(
    #         label="START WITH DEMO DECK 2025-02-18",
    #         key="kd_btn_start_with_demo_deck_20250215"
    #     ):
    #         st.session_state.update({
    #             f"kd_{k_list_in_deck_input}": deck_output_20250218,
    #             f"kd_{k_multiselect_deck_input}": list(map(str, [known_cards[326], known_cards[635], known_cards[544]])),
    #             f"kd_{k_toggle_combine_ms_ta}": True
    #         })
    # with cols_demo_decks[1]:
    #     if st.button(
    #         label="START WITH DEMO DECK 2025-02-20",
    #         key="kd_btn_start_with_demo_deck_20250220"
    #     ):
    #         st.session_state.update({
    #             f"kd_{k_list_in_deck_input}": deck_output_20250220,
    #             f"kd_{k_multiselect_deck_input}": [],
    #             f"kd_{k_toggle_combine_ms_ta}": True
    #         })
    # with cols_demo_decks[2]:
    #     if st.button(
    #         label="START WITH DEMO DECK 2025-02-22",
    #         key="kd_btn_start_with_demo_deck_20250222"
    #     ):
    #         st.session_state.update({
    #             f"kd_{k_list_in_deck_input}": deck_output_20250222,
    #             f"kd_{k_multiselect_deck_input}": [],
    #             f"kd_{k_toggle_combine_ms_ta}": True
    #         })

    if st.button(
            label="START FROM ORIGINAL MEMORY CARD"
    ):
        st.session_state.update({
            k_my_deck2: list(map(str_to_card, eval(deck_output_memory_card_original)))
        })
        st.rerun()

    multiselect_deck_input = st.multiselect(
        label="Select your deck:",
        # key=f"kd_{k_multiselect_deck_input}",
        options=options,
        max_selections=40
    )
    deck = multiselect_deck_input
    #
    # list_in_deck_input = st.text_area(
    #     label="Paste a list:",
    #     key=f"kd_{k_list_in_deck_input}"
    # )
    #
    # toggle_combine_ms_ta = st.toggle(
    #     label="Combine multi-select input with text-area input?",
    #     key=f"kd_{k_toggle_combine_ms_ta}"
    # )
    #
    # parsed = []
    # if toggle_combine_ms_ta:
    #     p = []
    #     st.write("Interpreted:")
    #     try:
    #         p = eval(list_in_deck_input)
    #         # for i, crd in enumerate(parsed):
    #         #     num = int(crd.split(" ")[0].removeprefix("#"))
    #         #     parsed.append(known_cards[num])
    #
    #     except Exception as e:
    #         p = []
    #     parsed = multiselect_deck_input + p
    #     st.write(parsed)
    # else:
    #     if len(st.session_state.get(f"kd_{k_multiselect_deck_input}")) == 40:
    #         parsed = multiselect_deck_input
    #     elif list_in_deck_input:
    #         parsed = []
    #         st.write("Interpreted:")
    #         try:
    #             parsed = eval(list_in_deck_input)
    #             # for i, crd in enumerate(parsed):
    #             #     num = int(crd.split(" ")[0].removeprefix("#"))
    #             #     parsed.append(known_cards[num])
    #
    #         except Exception as e:
    #             parsed = []
    #             st.error(e)
    #
    #         st.write(parsed)

    st.write(f"{len(deck)} / 40 Card(s) chosen")
    if 5 <= len(deck) <= 40:
        if st.button(
            label="save",
            key=f"k_btn_save_deck_input"
        ):
            st.session_state.update({
                k_my_deck2: deck
            })
            st.rerun()


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

    cols_demo_decks = st.columns(3)
    with cols_demo_decks[0]:
        if st.button(
            label="START WITH DEMO DECK 2025-02-18",
            key="kd_btn_start_with_demo_deck_20250215"
        ):
            st.session_state.update({
                f"kd_{k_list_in_deck_input}": deck_output_20250218,
                f"kd_{k_multiselect_deck_input}": list(map(str, [known_cards[326], known_cards[635], known_cards[544]])),
                f"kd_{k_toggle_combine_ms_ta}": True
            })
    with cols_demo_decks[1]:
        if st.button(
            label="START WITH DEMO DECK 2025-02-20",
            key="kd_btn_start_with_demo_deck_20250220"
        ):
            st.session_state.update({
                f"kd_{k_list_in_deck_input}": deck_output_20250220,
                f"kd_{k_multiselect_deck_input}": [],
                f"kd_{k_toggle_combine_ms_ta}": True
            })
    with cols_demo_decks[2]:
        if st.button(
            label="START WITH DEMO DECK 2025-02-22",
            key="kd_btn_start_with_demo_deck_20250222"
        ):
            st.session_state.update({
                f"kd_{k_list_in_deck_input}": deck_output_20250222,
                f"kd_{k_multiselect_deck_input}": [],
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


def rem_card_to_combos_list(player: Player, card: Card):
    k = k_cpu_combo_play_cards if player == cpu else k_my_combo_play_cards
    lst = st.session_state.setdefault(k, [])
    if card not in lst:
        return
    lst.remove(card)
    st.session_state.update({k: lst})


def add_card_to_combos_list(player: Player, card: Card):
    k = k_cpu_combo_play_cards if player == cpu else k_my_combo_play_cards
    lst = st.session_state.setdefault(k, [])
    if card in lst:
        return
    st.session_state.update({k: lst + [card]})


@st.dialog(title=app_title, width="large")
def battle(card: Card):
    # choose a card to battle against
    st.write("BATTLE!")
    if st.button(
        label="DONE BATTLING",
        key=f"kd_btn_done_battle"
    ):
        st.rerun()


def random_deck(size: int = 40):
    """
    The player starts with a Deck of 40 cards, which are randomly selected from seven pools.

    The 40 cards will be made up of:

    16 monsters with ATK + DEF < 1100           # Grp 0
    16 monsters with 1100 ≤ ATK + DEF < 1600    # grp 1
    4 monsters with 1600 ≤ ATK + DEF < 2100     # grp 2
    1 monster with 2100 ≤ ATK + DEF             # grp 3
    1 pure Magic Card                           # grp 4
    1 Field Magic Card                          # grp 5
    1 Equip Card                                # grp 6
    """
    # return random.sample(known_cards[1:]*3, size)
    print(f"random deck")
    deck = []
    groups = [[] for i in range(7)]
    grp_sizes = [16, 16, 4, 1, 1, 1, 1]
    for i, card in enumerate(known_cards[1:]):

        if (card == known_cards[336]) or (card == known_cards[337]):
            # dark hole and raigeki
            continue
        elif card in [known_cards[17], known_cards[18], known_cards[19], known_cards[20], known_cards[21]]:
            # exodia pieces
            groups[0].append(card)
        else:

            if card.type_simple == "Monster":
                ttl = card.atk_points + card.def_points
                print(f"{ttl=}, {card=}")
                if ttl < 1100:
                    groups[0].extend([card]*3)
                elif 1100 <= ttl < 1600:
                    groups[1].extend([card]*3)
                elif 1600 <= ttl < 2100:
                    groups[2].extend([card]*3)
                else:
                    groups[3].extend([card]*3)
            elif (card.type_simple == "Magic") or (card.type_simple == "Trap"):
                groups[5].extend([card]*3)
            elif card.type_simple == "Equip":
                groups[6].extend([card]*3)

    groups[4].extend([known_cards[336], known_cards[337]])
    for i, g_size in enumerate(grp_sizes):
        deck += random.sample(groups[i], g_size)

    # st.write(deck)
    # print(deck)
    # print(f"{list(map(len, groups))=}")

    return deck


def str_to_card(card_str: str | Card) -> Card | None:

    if card_str is None:
        return None

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
        elif isinstance(card_str, int):
            return known_cards[card_str]
        else:
            raise ValueError(f"A ERROR CONVERTING '{card_str}' to card, {type(card_str)=}.")

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

img_w_planet = 36

data_parsed_combinations, data_parsed_combinations_2 = parse_combinations_file()
reverse_combos = process_reverse_combinations()

k_my_deck = "my_game_deck"
k_my_hand = "my_game_hand"
k_btn_draw_hand = "btn_draw_hand"
k_btn_select_hand = "btn_select_hand"

k_player_0 = "player_0"
k_player_1 = "player_1"
k_match = "match"

k_opp_deck = "opp_game_deck"

k_operation_mode = "operation_mode"
options_operation_mode = ["Build", "Play"]

selectbox_operation_mode = st.selectbox(
    label="Operation Mode:",
    key=f"kd_{k_operation_mode}",
    options=options_operation_mode
)

k_my_deck2 = f"my_deck_2"

if selectbox_operation_mode == options_operation_mode[0]:
    # Build

    if st.session_state.get(k_my_deck2) is None:
        ask_deck2()
    deck = st.session_state.setdefault(k_my_deck2, [])
    st.write("deck")
    st.write(deck)

    lst_monsters = [c for c in deck if c.type_simple == "Monster"]
    n_monsters = len(lst_monsters)
    lst_traps = [c for c in deck if c.type_simple == "Trap"]
    n_traps = len(lst_traps)
    lst_magics = [c for c in deck if (c.type_simple == "Magic") or (c.type_simple == "Ritual") or (c.type_simple == "Equip")]
    n_magics = len(lst_magics)
    cols_breakdown = st.columns(3)
    with cols_breakdown[0]:
        st.metric(
            label="Monsters",
            value=n_monsters,
            delta=n_monsters / 40,
            border=1
        )
        ttl_atk, min_atk, max_atk = 0, None, None
        ttl_def, min_def, max_def = 0, None, None
        for i, card in enumerate(lst_monsters):
            atk_ = card.atk_points
            def_ = card.def_points
            ttl_atk += atk_
            ttl_def += def_
            if (min_atk is None) or (atk_ < min_atk[0]):
                min_atk = [atk_, i]
            if (max_atk is None) or (atk_ > max_atk[0]):
                max_atk = [atk_, i]
            if (min_def is None) or (def_ < min_def[0]):
                min_def = [def_, i]
            if (max_def is None) or (def_ > max_def[0]):
                max_def = [def_, i]

        data_atk = {
            "min": lst_monsters[min_atk[1]],
            "max": lst_monsters[max_atk[1]],
            "avg": ttl_atk / (1 if n_monsters == 0 else n_monsters)
        }
        data_def = {
            "min": lst_monsters[min_def[1]],
            "max": lst_monsters[max_def[1]],
            "avg": ttl_def / (1 if n_monsters == 0 else n_monsters)
        }
        st.write("data_atk")
        st.write(data_atk)
        st.write("data_def")
        st.write(data_def)
    with cols_breakdown[1]:
        st.metric(
            label="Magics",
            value=n_magics,
            delta=n_magics / 40,
            border=1
        )
    with cols_breakdown[2]:
        st.metric(
            label="Traps",
            value=n_traps,
            delta=n_traps / 40,
            border=1
        )

    p_combos = []
    p_combo_txts = {}
    print(f"{len(data_parsed_combinations_2)=}")
    print(f"{list(map(type, list(data_parsed_combinations_2.keys())[:10]))=}")
    for i, card in enumerate(deck):
        print(f"{i=}, {card=}, {type(card)=}")
        c_combos = data_parsed_combinations_2[card]
        # c_combos = [c for c in c_combos if (c in deck) and (c != card)]
        c_combos = [c for c in c_combos if (c in deck)]
        p_combos.append(c_combos)
        p_combo_txts[f"{card}"] = [f"{known_cards[c]} => {known_cards[data_parsed_combinations_2[card][c]]}" for c in c_combos]

    st.write("p_combos")
    st.write(p_combos)
    st.write("p_combo_txts")
    st.write(p_combo_txts)

elif selectbox_operation_mode == options_operation_mode[1]:
    # Play

    if k_my_deck not in st.session_state:
        ask_deck()
    if k_opp_deck not in st.session_state:
        st.session_state.update({k_opp_deck: random_deck()})

    if st.sidebar.button(
        label="New Game",
        key="btn_new_game"
    ):
        new_game()
    if st.sidebar.button(
        label="Edit Deck",
        key="btn_edit_deck"
    ):
        ask_deck(selected=st.session_state.get(k_my_deck, []))

    me, cpu, match = [None, None, None]
    # st.write(f"--A {len(st.session_state.get(k_my_deck))=}")
    # print(f"--A {len(st.session_state.get(k_my_deck))=}")
    my_deck = list(map(str_to_card, st.session_state.get(k_my_deck, [])))
    # st.write(f"--B {len(st.session_state.get(k_my_deck))=}")
    # print(f"--B {len(st.session_state.get(k_my_deck))=}")

    if my_deck:


        # st.session_state.setdefault(k_my_deck, random_deck())
        # my_deck = [known_cards[16], known_cards[16], known_cards[425], known_cards[425], known_cards[4]]
        # n_cards_in_deck = len(st.session_state.get(k_my_deck, []))
        draw_size = 5

        if not st.session_state.get(k_player_0):
            me = Player("ME", deck=my_deck, card_parser=str_to_card)
            print(f"1 create k_player_0, {me}, {len(my_deck)=}")
            st.session_state.update({k_player_0: me})
        if not st.session_state.get(k_player_1):
            cpu_deck = st.session_state.get(k_opp_deck)
            cpu = Player("CPU", deck=cpu_deck, card_parser=str_to_card, place_order="rtl")
            print(f"1 create k_player_1, {cpu}")
            st.session_state.update({k_player_1: cpu})

        me = st.session_state[k_player_0]
        cpu = st.session_state[k_player_1]
        st.write(f"-A {len(me.deck)=}")
        print(f"-A {len(me.deck)=}")
        st.write(f"-B {len(st.session_state.get(k_my_deck))=}")
        print(f"-B {len(st.session_state.get(k_my_deck))=}")

        if not st.session_state.get(k_match):
            print(f"create match")
            match = Match(me, cpu)
            st.session_state.update({k_match: match})

        match: Match = st.session_state[k_match]
        if not match.started:
            match.start(player_turn_in=cpu)

        # st.write("me")
        # st.write(me)
        # st.write(me.__dict__)
        # st.write("cpu")
        # st.write(cpu)
        # st.write(cpu.__dict__)
        # st.write("match")
        # st.write(match)

        if not match.started:
            if st.button(
                label="start new match",
                key="k_btn_new_game"
            ):
                st.session_state.pop(k_match)

        is_my_turn = match.turn == me
        turn_phase = match.turn_phase
        cpu_deck = cpu.deck
        cpu_hand = cpu.get_hand()
        my_hand = me.get_hand()
        my_monsters = me.monsters
        my_magic = me.magic
        st.write(f"A {len(me.deck)=}")
        print(f"A {len(me.deck)=}")
        my_deck = me.deck
        st.write(f"B {len(my_deck)=}")
        print(f"B {len(my_deck)=}")


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
        grid_columns_opp = st.columns(5)
        grid_field = [
            [col.container(border=1) for col in grid_columns_opp]
            for i in range(2)
        ]
        st.divider()
        grid_columns_me = st.columns(5)
        grid_field += [
            [col.container(border=1) for col in grid_columns_me]
            for i in range(2)
        ]
        grid_my_hand = st.columns(5, border=1)

        # my_hand = st.session_state.get(k_my_hand)
        # st.write(my_hand)

        k_btn_end_turn = "btn_end_turn"
        btn_end_turn = st.button(
            label="end turn",
            key=f"k_{k_btn_end_turn}",
            on_click=match.next_turn
        )

        st.write("my_deck")
        st.write(f"FF {len(my_deck)=}")
        st.write(my_deck)

        k_btn_set_my_hand = "btn_set_my_hand"
        btn_set_my_hand = st.sidebar.button(
            label="set my hand",
            key=f"k_{k_btn_set_my_hand}",
            on_click=set_my_hand
        )
        my_hand = me.get_hand()

        # CPU HAND
        for i, card in enumerate(cpu_hand):
            grid_opp_hand[i].write(card)

        # CPU MAGIC & TRAPS
        for i in range(5):
            if (len(cpu.magic) > i) and (cpu.magic[i] is not None):
                card: Card = cpu.magic[i]["card"]
                if card.face_down:
                    grid_field[0][i].write(f"?")
                else:
                    grid_field[0][i].write(card)
            else:
                grid_field[0][i].write(f"{i=}")

        # CPU MONSTERS
        for i in range(5):
            if (len(cpu.monsters) > i) and (cpu.monsters[i] is not None):
                card: Card = cpu.monsters[i]["card"]
                atk_mode = card.attack_mode
                planet = card.planet
                p_idx = card.ring.index(planet)
                planet_sym = card.ring_sym[p_idx]
                planet_path = card.ring_path[p_idx]
                if card.face_down:
                    grid_field[1][i].write(f"? {'D' if not atk_mode else 'A'}, {planet}, {planet_sym}")
                    grid_field[1][i].image(
                        image=planet_path,
                        caption=planet,
                        width=img_w_planet
                    )
                else:
                    grid_field[1][i].write(card)
            else:
                grid_field[1][i].write(f"{i=}")

        # MY MONSTERS
        for i in range(5):
            if (len(me.monsters) > i) and (me.monsters[i] is not None):
                card: Card = me.monsters[i]["card"]
                atk_mode = card.attack_mode
                planet = card.planet
                p_idx = card.ring.index(planet)
                planet_sym = card.ring_sym[p_idx]
                planet_path = card.ring_path[p_idx]
                if card.face_down:
                    grid_field[2][i].write("?")
                grid_field[2][i].write(card)
                grid_field[2][i].image(
                    image=planet_path,
                    caption=planet,
                    width=img_w_planet
                )

                if is_my_turn:
                    if card.face_down:
                        k_btn_flip_card = "btn_flip_card"
                        btn_flip_card = grid_field[2][i].button(
                            label="flip",
                            key=f"k_{k_btn_flip_card}_{i}",
                            on_click=card.flip_card
                        )

                    k_btn_shift_mode = "btn_shift_mode"
                    btn_shift_mode = grid_field[2][i].button(
                        label="DEF" if atk_mode else "ATK",
                        key=f"k_{k_btn_shift_mode}_{i}",
                        on_click=card.toggle_mode
                    )
                    if (match.turn_num > 0) and cpu.monsters:
                        k_btn_attack = "btn_attack"
                        btn_attack = grid_field[2][i].button(
                            label="Attack",
                            key=f"k_{k_btn_attack}_{i}",
                            on_click=lambda c_=card: battle(c_)
                        )
            else:
                grid_field[2][i].write(f"{i=}")

        # MY MAGIC & TRAPS
        for i in range(5):
            if (len(me.magic) > i) and (me.magic[i] is not None):
                card: Card = me.magic[i]["card"]
                grid_field[3][i].write(card)
            else:
                grid_field[3][i].write(f"{i=}")

        # for i in range(4):
        #     for j in range(5):
        #         grid_field[i][j].write(f"{i=}, {j=}")

        k_my_combo_play_cards = "my_combo_play_cards"
        k_cpu_combo_play_cards = "cpu_combo_play_cards"
        my_combo_play_cards = st.session_state.setdefault(k_my_combo_play_cards, [])
        cm = sum([st.session_state.get(f"k_toggle_merge_{i}", False) for i in range(len(my_hand))])
        for i, card in enumerate(my_hand):
            grid_my_hand[i].write(card)
            if str_to_card(card) in my_combo_play_cards:
                c_idx = my_combo_play_cards.index(str_to_card(card)) + 1
                btn_rem_combo_card = grid_my_hand[i].button(
                    label=f"-{c_idx}",
                    key=f"k_btn_rem_combo_card_{i}",
                    on_click=lambda c=card: rem_card_to_combos_list(player=me, card=str_to_card(c))
                )
            else:
                btn_add_combo_card = grid_my_hand[i].button(
                    # label=f"+{len(my_combo_play_cards) + 1}",
                    label=f"++",
                    key=f"k_btn_add_combo_card_{i}",
                    on_click=lambda c=card: add_card_to_combos_list(player=me, card=str_to_card(c))
                )
            if (not my_combo_play_cards) or (str_to_card(card) in my_combo_play_cards):
                btn_play_card = grid_my_hand[i].button(
                    label="play",
                    key=f"k_btn_play_card_{i}",
                    on_click=lambda c=card: play_card(me, str_to_card(c))
                )
            # if st.session_state.get(f"k_toggle_merge_{i}", False):
            #     st.write()
            # toggle_merge_card = grid_my_hand[i].toggle(
            #     label=f"merge {cm + 1}",
            #     key=f"k_toggle_merge_{i}",
            #     on_change=lambda: update_merge_list(i)
            # )

        st.write("Hand & Monsters:")

        my_avail_combo_cards = [c for c in list(map(str_to_card, [
            (cd["card"] if isinstance(cd, dict) else cd)
              for cd in my_hand + me.monsters
        ])) if c is not None]
        st.write("my_avail_combo_cards")
        st.write(my_avail_combo_cards)

        # st.write(list(map(type, my_avail_combo_cards)))
        my_possible_combos = process_possible_combos(my_avail_combo_cards)
        st.write("MY possible_combos")
        st.write(my_possible_combos)

        cpu_avail_combo_cards = [c for c in list(map(str_to_card, [
            (cd["card"] if isinstance(cd, dict) else cd)
              for cd in cpu_hand + cpu.monsters
        ])) if c is not None]
        st.write("cpu_avail_combo_cards")
        st.write(cpu_avail_combo_cards)

        cpu_possible_combos = process_possible_combos(cpu_avail_combo_cards)
        st.write("CPU possible_combos")
        st.write(cpu_possible_combos)
        st.write("cpu.deck_og")
        st.write(cpu.deck_og)

        cards_available = st.multiselect(
            label="Cards",
            key="k_multiselect_cards_available",
            options=known_cards[1:],
            max_selections=10
        )

        if cards_available:
            st.write("Combos available:")
            st.write(process_possible_combos(cards_available))

        # with st.container(border=1):
        #     # DON'T!
        #     st.write("All possible deck combos available:")
        #     st.write(process_possible_combos(me.deck_og))

        selectbox_investigate_card = st.selectbox(
            label="investigate card",
            key="k_selectbox_investigate_card",
            options=known_cards[1:]*3
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
                play_random_card(cpu)
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
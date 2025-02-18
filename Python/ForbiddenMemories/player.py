import random
from typing import Optional

import streamlit as st

from card import Card


app_title = "YU-GI-OH! Forbidden Memories"
gen_player_ids = (i for i in range(1000))


class Player:

    def __init__(
            self,
            name: str,
            deck: list[Card],
            chest: Optional[list[Card]] = None,
            default_hp=8000
    ):
        self.id_num = next(gen_player_ids)
        self.name = name
        self.deck_og = deck.copy()
        self.deck = deck
        self.chest = chest if chest is not None else []
        self.default_hp = default_hp

        self.hp = default_hp
        self.in_match = False
        self.hand = []
        self.graveyard = []
        self.monsters = []
        self.magic = []

        self.wins = 0
        self.losses = 0
        self.draws = 0
        self.hp_lost = 0
        self.hp_gained = 0
        self.game_history = []

    def valid_deck(self) -> bool:
        if len(self.deck) != 40:
            return False
        set_cards = set(self.deck)
        for i, card in enumerate(set_cards):
            if self.deck.count(card) > 3:
                return False
        # Number of card type rule??
        return True

    def new_match(self, match_id):
        self.hp = self.default_hp
        self.in_match = True
        self.game_history.append(match_id)
        self.hand.clear()
        self.deck = self.deck_og.copy()
        random.shuffle(self.deck)
        self.draw(n=5)
        # elif match_id != self.game_history[-1]:
        #     raise ValueError("You are currently ")

    def end_match(self, match_id):
        self.in_match = False
        if not self.game_history:
            raise ValueError("Not in a game currently")

    def change_hp(self, change):
        if change < 0:
            # lost
            self.hp_lost += change
        elif change > 0:
            self.hp_gained += change

        self.hp += change

    def draw(self, n=1):
        chxs = random.sample(self.deck, n)
        for chx in chxs:
            self.deck.remove(chx)
        self.hand.extend(chxs)

    def play_card(self, card: Card):
        self.hand.remove(card)
        card_type = card.type_
        if card.type_simple == "Monster":
            self.ask_sign(card)
            self.monsters.append(card)
        else:
            self.magic.append(card)

    @st.dialog(title=f"Select Sign")
    def ask_sign(self, card: Card):
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

        if cols[1].button(
            label="save",
            key=f"k_btn_save_sign_{card.num}"
        ):
            card.planet = st.session_state.get(f"k_{k_slider}", card.planet_0)
            st.rerun()

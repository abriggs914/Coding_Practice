import datetime
import random
from typing import Literal

import streamlit as st

from card import *


app_title: str = "YU-GI-OH! Forbidden Memories"
gen_player_ids: Generator[int, None, None] = (i for i in range(1000))
do_test: bool = False


class Player:

    def __init__(
            self,
            name: str,
            deck: list[Card],
            # card_parser: callable,
            # gen_chest_id: callable,
            chest: Optional[dict[Card: int]] = None,
            default_hp: int = 8000,
            place_order: Literal["ltr", "rtl"] = "ltr"
    ):
        self.id_num = next(gen_player_ids)
        self.name = name
        self.deck_og = [c for c in deck]
        # self.card_parser = card_parser
        # self.gen_chest_id = gen_chest_id
        self.deck = deck
        self.chest = chest if chest is not None else {}
        self.default_hp = default_hp
        self.place_order = place_order

        self.hp = default_hp
        self.in_match = False
        self.hand = [None for i in range(5)]
        self.graveyard = []
        self.monsters = [None for i in range(5)]
        self.magic = [None for i in range(5)]

        self.wins = 0
        self.losses = 0
        self.draws = 0
        self.hp_lost = 0
        self.hp_gained = 0
        self.game_history = []

    def valid_deck(self) -> bool:
        if do_test:
            print(f"Player.valid_deck")
        if len(self.deck) != 40:
            return False
        set_cards = set(self.deck)
        for i, card in enumerate(set_cards):
            if self.deck.count(card) > 3:
                return False
        # Number of card type rule??
        return True

    def new_match(self, match_id):
        if do_test:
            print(f"Player.new_match")
        self.hp = self.default_hp
        self.in_match = True
        self.game_history.append(match_id)
        self.hand.clear()
        self.deck = [c for c in self.deck_og]
        if do_test:
            print(f"A {len(self.deck)=}, {self.deck[0]=}")
        random.shuffle(self.deck)
        if do_test:
            print(f"B {len(self.deck)=}, {self.deck[0]=}")
        # self.deck = [self.card_parser(c) for c in self.deck]
        if do_test:
            print(f"C {len(self.deck)=}, {self.deck[0]=}")       
        self.draw(n=5)
        # elif match_id != self.game_history[-1]:
        #     raise ValueError("You are currently ")

    def end_match(self, match_id):
        if do_test:
            print(f"Player.end_match")
        self.in_match = False
        self.hand.clear()
        self.deck = self.deck_og.copy()
        if not self.game_history:
            raise ValueError("Not in a game currently")

    def change_hp(self, change):
        if do_test:
            print(f"Player.change_hp")
        if change < 0:
            # lost
            self.hp_lost += change
        elif change > 0:
            self.hp_gained += change

        self.hp += change

    def draw(self, n=1):
        if do_test:
            print(f"Player.draw")
            print(f"A D {len(self.deck)=}")
        chxs = random.sample(self.deck, n)
        # chxs = [self.card_parser(c) for c in chxs]
        for chx in chxs:
            self.deck.remove(chx)
        i = 0
        while i < len(self.hand):
            if self.hand[i] is None:
                self.hand.pop(i)
            else:
                i += 1
        self.hand.extend(chxs)
        if do_test:
            print(f"B D {len(self.deck)=}")

    def next_avail_idx(self, lst_in):
        lst = [d for d in lst_in]
        rtl = self.place_order == "rtl"
        # if self.place_order == "rtl":
            # lst.reverse()
        print(f"Player.next_avail_idx {self.name=}, {rtl=}, {self.place_order=}")
        print(f"{len(lst)=}, {lst=}")
        if rtl:
            i = len(lst) - 1
            while i >= 0:
                c = lst[i]
                if (c is None) or (len(c) == 0) or (c["card"] is None):
                    print(f"A {i=}")
                    return i
                i -= 1
            print(f"B {len(lst) - 1=}")
            return len(lst) - 1
        else:
            for i, c in enumerate(lst):
                if (c is None) or (len(c) == 0) or (c["card"] is None):
                    print(f"C {i=}")
                    return i
            print(f"D 0")
            return 0

    def next_monster_idx(self):
        return self.next_avail_idx(self.monsters)

    # def get_hand(self):
    #     # lst = [None if (c is None) else self.card_parser(c) for c in self.hand]
    #     lst = [None if (c is None) else c for c in self.hand]
    #     self.hand = lst
    #     return self.hand

    def __eq__(self, other):
        return isinstance(other, Player) and (self.id_num == other.id_num)

    def next_magic_idx(self):
        return self.next_avail_idx(self.magic)

    def get_deck(self):
        return getattr(self, "_deck", [])

    def set_deck(self, deck_in: list[Card]):
        self._deck = deck_in
        self.deck_og = [c for c in deck_in]
        # pass
        # if do_test:
        #     print(f"Player.set_deck")
        #     print(f"A SD {len(self.deck)=}", end=f", {self.deck[0]=}\n" if self.deck else "\n")
        # self._deck = deck_in
        # for c in self.deck:
        #     c.into_play(chest_id=next(self.gen_chest_id))
        # if do_test:
        #     print(f"B SD {len(self.deck)=}, {self.deck[0]=}")
        # self.deck_og = [c for c in deck_in]

    def del_deck(self):
        del self._deck
        del self.deck_og

    def __repr__(self):
        return f"{{P#{self.id_num} - {self.name}}}"
    
    deck = property(get_deck, set_deck, del_deck)

import random

from player import Player

gen_match_id = (i for i in range(10000))


turn_phases = [
    "START",
    "DRAW",
    "PLAY1",
    "ATTACK",
    "PLAY2",
    "END"
]


class Match:

    def __init__(self, player_0: Player, player_1: Player):
        self.id_num = next(gen_match_id)
        self.player_0 = player_0
        self.player_1 = player_1

        if self.player_0.in_match:
            raise ValueError(f"Player {self.player_0} is already in a match")
        if self.player_1.in_match:
            raise ValueError(f"Player {self.player_1} is already in a match")

        self.player_0.new_match(self.id_num)
        self.player_1.new_match(self.id_num)

        self.started = False
        self.turn_phase = turn_phases[0]
        self.turn_num = 0
        self.turn = None
        self.start()

    def start(self):
        print("Match.start")
        if self.started:
            raise ValueError(f"This match has already started!")
        self.turn = self.player_0 if (random.choice([0, 1]) == 0) else self.player_1
        self.started = True

    def next_turn(self):
        print("Match.next_turn")
        self.turn = self.player_0 if (self.turn == self.player_1) else self.player_1
        self.turn_num += 1
        self.turn_phase = turn_phases[0]
    
    def advance_phase(self):
        print("Match.advance_phase")
        if self.turn_phase != turn_phases[-1]:
            self.turn_phase = turn_phases[turn_phases.index(self.turn_phase) + 1]

    def is_turn_over(self) -> bool:
        print("Match.is_turn_over")
        return self.turn_phase == turn_phases[-1]

    def has_drawn_turn(self) -> bool:
        print("Match.has_drawn_turn")
        return turn_phases.index(self.turn_phase) > turn_phases.index["DRAW"]

# sim/signals.py
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, List, Set, Optional

@dataclass
class Phase:
    name: str
    green_movements: Set[str]      # e.g. {"N_through", "S_through"}
    duration_s: float
    yellow_s: float = 3.0
    all_red_s: float = 1.0

@dataclass
class SignalPlan:
    phases: List[Phase]
    start_phase_index: int = 0

@dataclass
class TrafficLightController:
    plan: SignalPlan
    movement_to_lanes: Dict[str, List[str]]  # movement key -> lane ids
    phase_index: int = 0
    phase_time_s: float = 0.0
    state: str = "GREEN"  # GREEN / YELLOW / ALL_RED

    def reset(self):
        self.phase_index = self.plan.start_phase_index
        self.phase_time_s = 0.0
        self.state = "GREEN"

    def current_phase(self) -> Phase:
        return self.plan.phases[self.phase_index]

    def step(self, dt: float):
        # simple fixed-time cycle (you can upgrade later)
        self.phase_time_s += dt
        phase = self.current_phase()

        if self.state == "GREEN" and self.phase_time_s >= phase.duration_s:
            self.state = "YELLOW"
            self.phase_time_s = 0.0
        elif self.state == "YELLOW" and self.phase_time_s >= phase.yellow_s:
            self.state = "ALL_RED"
            self.phase_time_s = 0.0
        elif self.state == "ALL_RED" and self.phase_time_s >= phase.all_red_s:
            self.state = "GREEN"
            self.phase_time_s = 0.0
            self.phase_index = (self.phase_index + 1) % len(self.plan.phases)

    def movement_is_green(self, movement: str) -> bool:
        if self.state != "GREEN":
            return False
        return movement in self.current_phase().green_movements

    def lane_is_controlled_by(self, lane_id: str) -> bool:
        for lanes in self.movement_to_lanes.values():
            if lane_id in lanes:
                return True
        return False
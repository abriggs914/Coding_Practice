# sim/vehicles.py
from __future__ import annotations
from dataclasses import dataclass
from typing import Optional
import math

import pygame.rect


@dataclass
class Vehicle:
    id: int
    lane_id: str
    s_m: float
    speed_mps: float
    model: VehicleModel
    route: list[str]                     # list of lane_ids to follow
    route_index: int = 0

    # runtime signals/flags
    is_waiting: bool = False
    spawned_time_s: float = 0.0
    finished_time_s: Optional[float] = None
    color: Optional[tuple[int]] = None
    rect: Optional[pygame.rect.Rect] = None


@dataclass
class VehicleModel:
    length_m: float = 4.5
    desired_speed_mps: float = 13.9
    max_accel_mps2: float = 1.6
    comfortable_decel_mps2: float = 2.2
    min_gap_m: float = 2.0
    time_headway_s: float = 1.2
    delta: float = 4.0  # acceleration exponent

def idm_accel(
    v: float,                 # ego speed
    v0: float,                # desired speed
    gap: float,               # net distance to leader (front bumper to rear bumper)
    dv: float,                # ego - leader speed (positive if closing in)
    a: float,
    b: float,
    s0: float,
    T: float,
    delta: float = 4.0
) -> float:
    """
    IDM acceleration.
    gap is "net" gap (distance between vehicles, excluding lengths).
    """
    # avoid divide-by-zero / negative gaps
    gap = max(0.1, gap)
    v = max(0.0, v)
    v0 = max(0.1, v0)

    # desired dynamic gap
    s_star = s0 + max(0.0, v*T + (v*dv) / (2.0 * math.sqrt(a*b)))

    accel_free = (v / v0) ** delta
    accel_int = (s_star / gap) ** 2
    return a * (1.0 - accel_free - accel_int)
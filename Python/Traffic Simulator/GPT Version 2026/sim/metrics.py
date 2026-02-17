# sim/metrics.py
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, List
import math

@dataclass
class LaneStats:
    density_vpkm: float = 0.0
    mean_speed_mps: float = 0.0
    queue_count: int = 0
    vehicle_count: int = 0
    congestion_0_1: float = 0.0

@dataclass
class LiveMetrics:
    lane_stats: Dict[str, LaneStats] = field(default_factory=dict)

    # global summary
    throughput_completed: int = 0
    avg_travel_time_s: float = 0.0
    avg_delay_s: float = 0.0

    def ensure_lane(self, lane_id: str):
        if lane_id not in self.lane_stats:
            self.lane_stats[lane_id] = LaneStats()

def clamp01(x: float) -> float:
    return max(0.0, min(1.0, x))

def congestion_score(
    density_vpkm: float,
    mean_speed_ratio: float,
    queue_ratio: float,
) -> float:
    # Simple weighted score; tune later.
    # density ~ 0..150+ veh/km typical urban; cap at 150
    d = clamp01(density_vpkm / 150.0)
    s = clamp01(1.0 - mean_speed_ratio)  # slower => higher congestion
    q = clamp01(queue_ratio)             # already 0..1
    return clamp01(0.45 * d + 0.35 * s + 0.20 * q)

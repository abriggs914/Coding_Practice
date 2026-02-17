# sim/network.py
from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Dict, Tuple, Optional

Vec2 = Tuple[float, float]

@dataclass(frozen=True)
class LaneId:
    id: str

@dataclass
class Lane:
    id: LaneId
    name: str
    centerline: List[Vec2]           # polyline points in world coords (meters)
    width_m: float                   # lane "size"
    speed_limit_mps: float
    allowed_movements: List[str]     # e.g. ["through", "left", "right"]
    connects_to: List[LaneId]        # outbound lane options (lane graph edges)
    stopline_s: Optional[float] = None  # s distance of stop line if controlled

    movement_key: Optional[str] = None   # <-- ADD THIS

    # cached
    length_m: float = 0.0

@dataclass
class RoadNetwork:
    lanes: Dict[str, Lane] = field(default_factory=dict)

    def lane(self, lane_id: str) -> Lane:
        return self.lanes[lane_id]

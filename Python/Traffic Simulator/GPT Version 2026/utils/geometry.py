# utils/geometry.py
from typing import List, Tuple
import math
Vec2 = Tuple[float, float]

def polyline_length(points: List[Vec2]) -> float:
    if len(points) < 2:
        return 0.0
    total = 0.0
    for i in range(1, len(points)):
        x1, y1 = points[i-1]
        x2, y2 = points[i]
        total += math.hypot(x2 - x1, y2 - y1)
    return total

def point_at_s(points: List[Vec2], s: float) -> Tuple[float, float]:
    # returns approximate point along polyline at distance s
    if not points:
        return (0.0, 0.0)
    if len(points) == 1:
        return points[0]
    remaining = s
    for i in range(1, len(points)):
        x1, y1 = points[i-1]
        x2, y2 = points[i]
        seg = math.hypot(x2 - x1, y2 - y1)
        if seg <= 1e-9:
            continue
        if remaining <= seg:
            t = remaining / seg
            return (x1 + (x2 - x1) * t, y1 + (y2 - y1) * t)
        remaining -= seg
    return points[-1]

def quarter_arc(center: Vec2, radius: float, start_angle: float, end_angle: float, n: int = 12) -> List[Vec2]:
    """Generate points along an arc."""
    cx, cy = center
    pts = []
    for i in range(n + 1):
        t = i / n
        ang = start_angle + (end_angle - start_angle) * t
        pts.append((cx + radius * math.cos(ang), cy + radius * math.sin(ang)))
    return pts
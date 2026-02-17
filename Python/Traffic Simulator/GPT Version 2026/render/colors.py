# render/colors.py
from __future__ import annotations
from typing import Tuple

Color = Tuple[int, int, int]

def lerp(a: float, b: float, t: float) -> float:
    return a + (b - a) * t

def lerp_color(c1: Color, c2: Color, t: float) -> Color:
    return (int(lerp(c1[0], c2[0], t)),
            int(lerp(c1[1], c2[1], t)),
            int(lerp(c1[2], c2[2], t)))

def congestion_to_color(x: float) -> Color:
    # x in [0..1]
    x = max(0.0, min(1.0, x))
    green = (30, 200, 60)
    yellow = (240, 200, 40)
    red = (230, 60, 50)
    if x < 0.5:
        return lerp_color(green, yellow, x / 0.5)
    return lerp_color(yellow, red, (x - 0.5) / 0.5)

# render/colors.py
# from __future__ import annotations
from typing import Tuple
from random import randint

Color = Tuple[int, int, int]

def lerp(a: float, b: float, t: float) -> float:
    return a + (b - a) * t

def lerp_color(c1: Color, c2: Color, t: float) -> Color:
    return (int(lerp(c1[0], c2[0], t)),
            int(lerp(c1[1], c2[1], t)),
            int(lerp(c1[2], c2[2], t)))

def random_rgb(l_bound=10, h_bound=245):
    """Return random RGB color using bounds."""
    l_bound = max(0, min(l_bound, 255))
    h_bound = max(l_bound, min(h_bound, 255))
    return (
        randint(l_bound, h_bound),
        randint(l_bound, h_bound),
        randint(l_bound, h_bound)
    )

def congestion_to_color(x: float) -> Color:
    # x in [0..1]
    x = max(0.0, min(1.0, x))
    green = (30, 200, 60)
    yellow = (240, 200, 40)
    red = (230, 60, 50)
    if x < 0.5:
        return lerp_color(green, yellow, x / 0.5)
    return lerp_color(yellow, red, (x - 0.5) / 0.5)

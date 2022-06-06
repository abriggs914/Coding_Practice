import dataclasses
from typing import List

import pygame
from dataclasses import dataclass


@dataclass
class Ball:
    id_num: int
    rect: pygame.Rect
    colour: tuple
    radius: int
    speed: float
    points: List[float] = dataclasses.field(default_factory=list)
    frame: int = 0
    direction: bool = True

    def __repr__(self):
        return f"Ball #{(f'00{self.id_num}'[-2:])}, pos: ({self.rect.center})"

    def next_frame(self):
        if self.direction:
            self.frame += 1
        else:
            self.frame -= 1

        if self.frame >= len(self.points):
            self.frame = len(self.points) - 1
            self.direction = False
        elif self.frame < 0:
            self.direction = True
            self.frame = 0

        # self.rect = pygame.Rect(self.points[self.frame], self.rect.top, self.rect.width, self.rect.height)
        # print(f"XXX: {self.points[self.frame]}")
        self.rect = pygame.Rect(*self.points[self.frame], self.rect.width, self.rect.height)
        # self.rect = pygame.Rect(self.rect.left + 1, self.rect.top, self.rect.width, self.rect.height)

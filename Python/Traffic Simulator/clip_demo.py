import pygame
import keyboard as kbd
from colour_utility import *
from utility import *

pygame.init()
display = pygame.display.set_mode((900, 600))

def colliderect_offset(r1, r2, offset=0, l=True, r=True):
    assert isinstance(r1, pygame.Rect)
    assert isinstance(r2, pygame.Rect)
    print("")
    if l and r:
        print("l & r:\n\t{}\n\t{}".format(pygame.Rect(r1.left - offset, r1.top - offset, r1.width + (2 * offset),
                           r1.height + (2 * offset)), pygame.Rect(r2.left - offset, r2.top - offset, r2.width + (2 * offset), r2.height + (2 * offset))))
        return pygame.Rect(r1.left - offset, r1.top - offset, r1.width + (2 * offset),
                           r1.height + (2 * offset)).colliderect(
            pygame.Rect(r2.left - offset, r2.top - offset, r2.width + (2 * offset), r2.height + (2 * offset)))
    elif l:
        print("l & !r:\n\t{}\n\t{}".format(pygame.Rect(r1.left, r1.top, r1.width,
                           r1.height), pygame.Rect(r2.left - offset, r2.top - offset, r2.width + (2 * offset), r2.height + (2 * offset))))
        return pygame.Rect(r1.left - offset, r1.top - offset, r1.width + (2 * offset),
                           r1.height + (2 * offset)).colliderect(
            pygame.Rect(r2.left, r2.top, r2.width, r2.height))
    elif r:
        print("!l & r:\n\t{}\n\t{}".format(pygame.Rect(r1.left - offset, r1.top - offset, r1.width + (2 * offset),
                           r1.height + (2 * offset)), pygame.Rect(r2.left, r2.top, r2.width, r2.height)))
        return pygame.Rect(r1.left, r1.top, r1.width,
                           r1.height).colliderect(pygame.Rect(r2.left - offset, r2.top - offset, r2.width + (2 * offset), r2.height + (2 * offset)))
    else:
        return r1.colliderect(r2)


# n dashes, n splits, spaceing
def dashed_line(game, display, colour, start, end, width, n_segments=10, seg_proportion=0.8):
    seg_proportion = 1 - seg_proportion
    s_e = [start, end]
    s_e.sort(key=lambda tup: tup[0])
    start, end = s_e

    dx = end[0] - start[0]
    dy = end[1] - start[1]
    dxs = dx / n_segments
    dys = dy / n_segments
    p1 = start
    for i in range(n_segments):
        p2 = (p1[0] + dxs, p1[1] + dys)
        # game.draw.circle(display, colour, p1, 3)
        game.draw.line(display, colour, (p1[0] + (dxs * (seg_proportion / 2)), p1[1] + (dys * (seg_proportion / 2))),
                       (p2[0] - (dxs * (seg_proportion / 2)), p2[1] - (dys * (seg_proportion / 2))), width)
        lx = (p2[0] - p1[0])
        ly = (p2[1] - p1[1])
        p1 = p2


a = pygame.Rect(100, 0, 100, 300)
b = pygame.Rect(0, 100, 200, 100)
c = pygame.Rect.clip(a, b)
l1 = a.clipline((0, 0, 100, 100))
d = pygame.Rect(199, 0, 200, 200)
e = pygame.Rect.clip(a, d)
print("e:", e, "size:", e.size, 'sum:', sum(e.size))
f = pygame.Rect(100, 0, 100, 300)
g = pygame.Rect(200, 150, 200, 100)
print("COLLISION:", f.colliderect(g))
print("COLLISION A (t, f):", colliderect_offset(f, g, 1, True, False))  # check
print("COLLISION B (f, t):", colliderect_offset(f, g, 2, False, True))
print("COLLISION C (f, f):", colliderect_offset(f, g, 1, False, False))
print("COLLISION D (t, t):", colliderect_offset(f, g, 1))
print("f:", f)
print("g:", g)


# pygame.draw.circle(display, GREEN, (50, 50), 6)


pygame.draw.rect(display, GREEN, Rect(0, 0, 100, 100).tupl)
pygame.draw.rect(display, YELLOW_2, Rect(0, 100, 100, 100).tupl)
r1 = Rect(0, 0, 100, 100)
r2 = Rect(0, 100, 100, 100)
l1 = Line(0, -4, 140, 60)
print("r1:", r1)
print("r2:", r2)
print("l1:", l1)
print("li intersects r1:", r1.collide_line(l1))
print("li intersects r2:", r2.collide_line(l1))




allow_kbd_ctrls = True
is_playing = True

while is_playing:
    events = pygame.event.get()
    kbd_w, kbd_ua, kbd_a, kbd_la, kbd_s, kbd_da, kbd_d, kbd_ra = False, False, False, False, False, False, False, False
    if allow_kbd_ctrls:
        kbd_w = kbd.is_pressed('w')
        kbd_ua = kbd.is_pressed('up')
        kbd_a = kbd.is_pressed('a')
        kbd_la = kbd.is_pressed('left')
        kbd_s = kbd.is_pressed('s')
        kbd_da = kbd.is_pressed('down')
        kbd_d = kbd.is_pressed('d')
        kbd_ra = kbd.is_pressed('right')
        str_dir_keys = ["kbd_w", "kbd_ua", "kbd_a", "kbd_la", "kbd_s", "kbd_da", "kbd_d", "kbd_ra"]
        dir_keys = [kbd_w, kbd_ua, kbd_a, kbd_la, kbd_s, kbd_da, kbd_d, kbd_ra]
        a_dir_keys = any(dir_keys)
        kbd_q = kbd.is_pressed('q')
    for event in events:
        pos = pygame.mouse.get_pos()
        if kbd_q or event.type == pygame.QUIT:
            is_playing = False
        # pygame.draw.rect(display, (255, 0, 0), a)
        # pygame.draw.rect(display, (0, 0, 255), b)
        # pygame.draw.rect(display, (0, 255, 0), c)
        # pygame.draw.rect(display, (0, 255, 255), d)

        pygame.draw.rect(display, GREEN, Rect(0, 0, 100, 100).tupl)
        pygame.draw.rect(display, YELLOW_2, Rect(0, 100, 100, 100).tupl)
        pygame.draw.line(display, ORANGE, *Line(0, -4, 140, 60).tupl)

        # dashed_line(pygame, display, ORANGE, (15, 45), (250, 364), 5, 60)
        pygame.display.update()

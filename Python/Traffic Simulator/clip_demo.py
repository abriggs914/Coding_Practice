import pygame
import keyboard as kbd
pygame.init()

a = pygame.Rect(100, 0, 100, 300)
b = pygame.Rect(0, 100, 200, 100)
c = pygame.Rect.clip(a, b)
l1 = a.clipline((0,0,100,100))
d = pygame.Rect(199, 0, 200, 200)
e = pygame.Rect.clip(a, d)
print("e:", e, "size:", e.size, 'sum:', sum(e.size))
f = pygame.Rect(100, 0, 100, 300)
g = pygame.Rect(199, 300, 200, 100)
print("COLLISION:", f.colliderect(g))

display = pygame.display.set_mode((900, 600))
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
        pygame.draw.rect(display, (255, 0, 0), a)
        pygame.draw.rect(display, (0, 0, 255), b)
        pygame.draw.rect(display, (0, 255, 0), c)
        pygame.draw.rect(display, (0, 255, 255), d)

        pygame.draw.rect(display, (255, 255, 255), f)
        pygame.draw.rect(display, (255, 255, 255), g)
        pygame.display.update()

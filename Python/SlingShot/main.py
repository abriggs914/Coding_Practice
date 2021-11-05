from pygame_utility import *

if __name__ == '__main__':
    w, h = 750, 500
    app = PygameApplication("Slingshot", w, h)
    game = app.get_game()
    display = app.display
    rect = game.Rect(0, 0, w, h)
    btn_area_rect = game.Rect(w * 0.675, h * 0.05, w * 0.3, h * 0.08)

    detect_collisions = True
    left_post = (w * 0.35, h * 0.65)
    right_post = (w * 0.65, h * 0.65)
    dragging = False
    firing = False
    acceleration = (0, 0)
    speed = (0, 0)
    CR = 0.25
    click_pos = (0, 0)
    proj_pos = (0, 0)
    half_pos = ((right_post[0] + left_post[0]) / 2, (right_post[1] + left_post[1]) / 2)


    def draw_length():
        return distance(click_pos, half_pos)


    def collide_1d(cr, via, vib, ma, mb):
        assert ma > 0 and mb > 0, "Masses must be non-negative"
        return ((cr * mb * (vib - via)) + (ma * via) + (mb * vib)) / (ma + mb)


    def collide(cr, va, vb, ma, mb):
        return (collide_1d(cr, va[0], vb[0], ma, mb), collide_1d(cr, va[1], vb[1], ma, mb)), (
            collide_1d(cr, vb[0], va[0], mb, ma), collide_1d(cr, vb[1], va[1], mb, ma))


    while app.is_playing:
        display.fill(BLACK)

        # draw widgets and objects here
        game.draw.circle(display, GRAY_60, left_post, 5)
        game.draw.circle(display, GRAY_60, right_post, 5)
        game.draw.rect(display, WHITE, btn_area_rect)
        game.draw.rect(display, BLACK,
                       game.Rect(btn_area_rect.x + 1, btn_area_rect.y + 1, btn_area_rect.w - 2, btn_area_rect.h - 2))

        event_queue = app.run()
        for event in event_queue:

            # handle events

            click_pos = game.mouse.get_pos()
            if event.type == game.MOUSEBUTTONDOWN:
                click_val = game.mouse.get_pressed()
                if rect.collidepoint(click_pos):
                    if click_val[0]:
                        dragging = not dragging
                        break
            elif event.type == game.MOUSEBUTTONUP:
                if dragging:
                    dragging = False
                    firing = True
                    x_diff = (half_pos[0] - click_pos[0]) / w
                    y_diff = (half_pos[1] - click_pos[1]) / h
                    acceleration = (x_diff * draw_length(), y_diff * draw_length())

        if dragging:
            proj_pos = click_pos
            game.draw.line(display, RED, left_post, click_pos, 2)
            game.draw.line(display, RED, click_pos, right_post, 2)
            game.draw.circle(display, BLUE, proj_pos, 5)
            game.draw.line(display, RED_3, click_pos, half_pos, 3)
            acceleration = (0, 0)
            speed = (0, 0)
        elif firing:
            if detect_collisions:
                speed = (round(speed[0] + acceleration[0], 3), round(speed[1] + acceleration[1], 3))
                # proj_pos = (proj_pos[0] + speed[0], proj_pos[1] + speed[1])
                next_pos = (round(proj_pos[0] + speed[0], 3), round(proj_pos[1] + speed[1], 3))
                line_proj = Line(*proj_pos, *next_pos)
                line_top = Line(*rect.topleft, *rect.topright)
                line_right = Line(*rect.topright, *rect.bottomright)
                line_bottom = Line(*rect.bottomleft, *rect.bottomright)
                line_left = Line(*rect.topleft, *rect.bottomleft)
                print("p: {}, n: {}".format(proj_pos, next_pos))
                if not rect.collidepoint(next_pos):
                    print("line_proj: {}, ptd: {}".format(line_proj, flatten(list(line_proj))))
                    print("line_top: {}, p1: {}, p2: {}".format(line_top, line_top.p1, line_top.p2))
                    print("line_right: {}, p1: {}, p2: {}".format(line_right, line_right.p1, line_right.p2))
                    print("line_bottom: {}, p1: {}, p2: {}".format(line_bottom, line_bottom.p1, line_bottom.p2))
                    print("line_left: {}, p1: {}, p2: {}".format(line_left, line_left.p1, line_left.p2))
                    # if line_proj.collide_line(line_top, rounding=0):
                    if next_pos[1] <= rect.top:
                        print("hit top")
                        next_pos = (next_pos[0], rect.top)
                        # speed = (speed[0], -speed[1])
                        pt, wall = collide(CR, speed, (-1 * speed[0], -1 * speed[1]), 1, 1)
                        print("speed:", speed, "pt:", pt, "acceleration:", acceleration)
                        # speed = pt[0], -1 * pt[1]
                        speed = round(pt[0], 3), round(pt[1], 3)
                        next_pos = (round(next_pos[0] + speed[0], 3), round(next_pos[1] + speed[1], 3))
                        if speed[0] == 0 and speed[1] == 0:
                            firing = False
                            proj_pos = (0, 0)
                            acceleration = (0, 0)
                            speed = (0, 0)
                    # elif line_proj.collide_line(line_right, rounding=0):
                    elif next_pos[0] >= rect.right:
                        print("hit right")
                        # firing = False
                        proj_pos = (rect.right, proj_pos[1])
                        # acceleration = (0, 0)
                        speed = (-speed[0], speed[1])
                    # elif line_proj.collide_line(line_bottom, rounding=0):
                    elif next_pos[1] >= rect.bottom:
                        print("hit bottom")
                        proj_pos = (proj_pos[0], rect.bottom)
                        speed = (speed[0], -speed[1])
                    # elif line_proj.collide_line(line_left, rounding=0):
                    elif next_pos[0] <= rect.left:
                        print("hit left")
                        proj_pos = (rect.left, proj_pos[1])
                        speed = (-speed[0], speed[1])
                    elif Rect2(rect.x, rect.y, rect.w, rect.h).collide_line(line_proj) is None:
                        print("COMPLETELY OUTSIDE???")
                        firing = False
                        proj_pos = (0, 0)
                        acceleration = (0, 0)
                        speed = (0, 0)
                    else:
                        print("ELSE")
                        firing = False
                        proj_pos = (0, 0)
                        acceleration = (0, 0)
                        speed = (0, 0)
                else:
                    print("inside")
                proj_pos = next_pos
                game.draw.circle(display, BLUE, proj_pos, 5)
            else:
                speed = (speed[0] + acceleration[0], speed[1] + acceleration[1])
                proj_pos = (proj_pos[0] + speed[0], proj_pos[1] + speed[1])
                game.draw.circle(display, BLUE, proj_pos, 5)
                if not rect.collidepoint(proj_pos):
                    firing = False
                    proj_pos = (0, 0)
                    acceleration = (0, 0)
                    speed = (0, 0)

        game.display.flip()

        app.clock.tick(30)

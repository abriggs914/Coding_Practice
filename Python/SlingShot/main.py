from pygame_utility import *


if __name__ == '__main__':
    w, h = 750, 500
    app = PygameApplication("Slingshot", w, h)
    game = app.get_game()
    display = app.display
    rect = game.Rect(0, 0, w, h)
    btn_area_rect = game.Rect(w * 0.675, h * 0.05, w * 0.3, h * 0.08)

    left_post = (w * 0.35, h * 0.65)
    right_post = (w * 0.65, h * 0.65)
    dragging = False
    firing = False
    acceleration = (0, 0)
    speed = (0, 0)
    click_pos = (0, 0)
    proj_pos = (0, 0)
    half_pos = ((right_post[0] + left_post[0]) / 2, (right_post[1] + left_post[1]) / 2)

    def draw_length():
        return distance(click_pos, half_pos)

    while app.is_playing:
        display.fill(BLACK)

        # draw widgets and objects here
        game.draw.circle(display, GRAY_60, left_post, 5)
        game.draw.circle(display, GRAY_60, right_post, 5)
        game.draw.rect(display, WHITE, btn_area_rect)
        game.draw.rect(display, BLACK, game.Rect(btn_area_rect.x + 1, btn_area_rect.y + 1, btn_area_rect.w - 2, btn_area_rect.h - 2))

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
        elif firing:
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

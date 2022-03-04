import pygame
from colour_utility import *
from solitaire import *

if __name__ == '__main__':

    # s.columns[0].append(Card(13, Suit.HEARTS))
    # print("s.can_stack_col(0, Card(12, Card.HEARTS)):", s.can_stack_col(0, Card(12, Suit.HEARTS)))
    # print("s.can_stack_col(0, Card(13, Card.HEARTS)):", s.can_stack_col(0, Card(13, Suit.HEARTS)))
    # print("s.can_stack_col(0, Card(11, Card.HEARTS)):", s.can_stack_col(0, Card(11, Suit.HEARTS)))
    # print("s.can_stack_col(0, Card(12, Card.SPADES)):", s.can_stack_col(0, Card(12, Suit.SPADES)))
    #
    # print("s.can_stack_foundation(Suit.HEARTS, Card(12, Card.SPADES)):", s.can_stack_foundation(Suit.HEARTS, Card(12, Suit.SPADES)))
    # print("s.can_stack_foundation(Suit.HEARTS, Card(1, Card.HEARTS)):", s.can_stack_foundation(Suit.HEARTS, Card(1, Suit.HEARTS)))
    # print("s.can_stack_foundation(Suit.HEARTS, Card(13, Card.HEARTS)):", s.can_stack_foundation(Suit.HEARTS, Card(13, Suit.HEARTS)))

    pygame.init()
    s = Solitaire()
    # s.shuffle()
    # s.draw_card()

    WIDTH, HEIGHT = 900, 600
    W_CARD, H_CARD = 75, 135
    W_CARD, H_CARD = 178, 267
    F_W_CARD, F_H_CARD = 2 * 0.045, 6 * 0.05

    LEFT_MOST, TOP_MOST = 35, 35
    X_SHIFT = -10
    Y_SHIFT = 35
    COL_OFFSET = 0  # cards behind the top_card's rect will be shifted this many in thr x direction
    SPACE = 35  # space between card piles. needs to be large enough to support (7 + 13) * COL_OFFSET to prevent
    #             cards from one column overlapping another.
    RECT_DRAW_PILE = pygame.Rect(LEFT_MOST, TOP_MOST, W_CARD, H_CARD)
    RECT_DISCARD_PILE = pygame.Rect(RECT_DRAW_PILE.left + (1 * (RECT_DRAW_PILE.width + (2 * SPACE) + X_SHIFT)),
                                    TOP_MOST, W_CARD, H_CARD)
    RECT_FOUNDATION_1 = pygame.Rect(RECT_DRAW_PILE.left + (4 * (RECT_DRAW_PILE.width + SPACE)), TOP_MOST, W_CARD,
                                    H_CARD)
    RECT_FOUNDATION_2 = pygame.Rect(RECT_DRAW_PILE.left + (5 * (RECT_DRAW_PILE.width + SPACE)), TOP_MOST, W_CARD,
                                    H_CARD)
    RECT_FOUNDATION_3 = pygame.Rect(RECT_DRAW_PILE.left + (6 * (RECT_DRAW_PILE.width + SPACE)), TOP_MOST, W_CARD,
                                    H_CARD)
    RECT_FOUNDATION_4 = pygame.Rect(RECT_DRAW_PILE.left + (7 * (RECT_DRAW_PILE.width + SPACE)), TOP_MOST, W_CARD,
                                    H_CARD)
    COL_TOP = TOP_MOST + RECT_FOUNDATION_1.height + SPACE
    N_COLS = 7
    RECT_COLUMN_1 = pygame.Rect(RECT_DRAW_PILE.left + (1 * (RECT_DRAW_PILE.width + SPACE)), COL_TOP, W_CARD, H_CARD)
    RECT_COLUMN_2 = pygame.Rect(RECT_DRAW_PILE.left + (2 * (RECT_DRAW_PILE.width + SPACE)), COL_TOP, W_CARD, H_CARD)
    RECT_COLUMN_3 = pygame.Rect(RECT_DRAW_PILE.left + (3 * (RECT_DRAW_PILE.width + SPACE)), COL_TOP, W_CARD, H_CARD)
    RECT_COLUMN_4 = pygame.Rect(RECT_DRAW_PILE.left + (4 * (RECT_DRAW_PILE.width + SPACE)), COL_TOP, W_CARD, H_CARD)
    RECT_COLUMN_5 = pygame.Rect(RECT_DRAW_PILE.left + (5 * (RECT_DRAW_PILE.width + SPACE)), COL_TOP, W_CARD, H_CARD)
    RECT_COLUMN_6 = pygame.Rect(RECT_DRAW_PILE.left + (6 * (RECT_DRAW_PILE.width + SPACE)), COL_TOP, W_CARD, H_CARD)
    RECT_COLUMN_7 = pygame.Rect(RECT_DRAW_PILE.left + (7 * (RECT_DRAW_PILE.width + SPACE)), COL_TOP, W_CARD, H_CARD)

    # Load images once
    CARD_IMAGES = dict(
        zip(list(map(str, s.deck.cards)), [pygame.image.load(_img) for _img in [img.image for img in s.deck.cards]]))
    print(f"[img.image for img in s.deck.cards]{len([img.image for img in s.deck.cards])}:",
          [img.image for img in s.deck.cards])
    DECK_IMAGE = pygame.image.load(s.deck.image)

    CARD_SELECTED = {}

    def update_window_dims(w, h):
        global WIDTH, HEIGHT, W_CARD, H_CARD, COL_TOP, RECT_DRAW_PILE, RECT_DISCARD_PILE, RECT_FOUNDATION_1, RECT_FOUNDATION_2, RECT_FOUNDATION_3, RECT_FOUNDATION_4, RECT_COLUMN_1, RECT_COLUMN_2, RECT_COLUMN_3, RECT_COLUMN_4, RECT_COLUMN_5, RECT_COLUMN_6, RECT_COLUMN_7, DECK_IMAGE, CARD_IMAGES, CARD_SELECTED
        WIDTH, HEIGHT = w, h
        W_CARD, H_CARD = int(F_W_CARD * WIDTH), int(F_H_CARD * HEIGHT)
        RECT_DRAW_PILE = pygame.Rect(LEFT_MOST, TOP_MOST, W_CARD, H_CARD)
        RECT_DISCARD_PILE = pygame.Rect(RECT_DRAW_PILE.left + (1 * (RECT_DRAW_PILE.width + (2 * SPACE) + X_SHIFT)),
                                        TOP_MOST, W_CARD, H_CARD)
        RECT_FOUNDATION_1 = pygame.Rect(RECT_DRAW_PILE.left + (4 * (RECT_DRAW_PILE.width + SPACE)), TOP_MOST, W_CARD,
                                        H_CARD)
        RECT_FOUNDATION_2 = pygame.Rect(RECT_DRAW_PILE.left + (5 * (RECT_DRAW_PILE.width + SPACE)), TOP_MOST, W_CARD,
                                        H_CARD)
        RECT_FOUNDATION_3 = pygame.Rect(RECT_DRAW_PILE.left + (6 * (RECT_DRAW_PILE.width + SPACE)), TOP_MOST, W_CARD,
                                        H_CARD)
        RECT_FOUNDATION_4 = pygame.Rect(RECT_DRAW_PILE.left + (7 * (RECT_DRAW_PILE.width + SPACE)), TOP_MOST, W_CARD,
                                        H_CARD)
        COL_TOP = TOP_MOST + RECT_FOUNDATION_1.height + SPACE
        RECT_COLUMN_1 = pygame.Rect(RECT_DRAW_PILE.left + (1 * (RECT_DRAW_PILE.width + SPACE)), COL_TOP, W_CARD, H_CARD)
        RECT_COLUMN_2 = pygame.Rect(RECT_DRAW_PILE.left + (2 * (RECT_DRAW_PILE.width + SPACE)), COL_TOP, W_CARD, H_CARD)
        RECT_COLUMN_3 = pygame.Rect(RECT_DRAW_PILE.left + (3 * (RECT_DRAW_PILE.width + SPACE)), COL_TOP, W_CARD, H_CARD)
        RECT_COLUMN_4 = pygame.Rect(RECT_DRAW_PILE.left + (4 * (RECT_DRAW_PILE.width + SPACE)), COL_TOP, W_CARD, H_CARD)
        RECT_COLUMN_5 = pygame.Rect(RECT_DRAW_PILE.left + (5 * (RECT_DRAW_PILE.width + SPACE)), COL_TOP, W_CARD, H_CARD)
        RECT_COLUMN_6 = pygame.Rect(RECT_DRAW_PILE.left + (6 * (RECT_DRAW_PILE.width + SPACE)), COL_TOP, W_CARD, H_CARD)
        RECT_COLUMN_7 = pygame.Rect(RECT_DRAW_PILE.left + (7 * (RECT_DRAW_PILE.width + SPACE)), COL_TOP, W_CARD, H_CARD)
        print(f"WIDTH: {WIDTH}, HEIGHT: {HEIGHT}\nW_CARD: {W_CARD}, H_CARD: {H_CARD}\nRECT_DRAW_PILE: {RECT_DRAW_PILE}\nRECT_DISCARD_PILE: {RECT_DISCARD_PILE}\nRECT_FOUNDATION_1: {RECT_FOUNDATION_1}\nRECT_FOUNDATION_2: {RECT_FOUNDATION_2}\nRECT_FOUNDATION_3: {RECT_FOUNDATION_3}\nRECT_FOUNDATION_4: {RECT_FOUNDATION_4}\nCOL_TOP: {COL_TOP}\nRECT_COLUMN_1: {RECT_COLUMN_1}\nRECT_COLUMN_2: {RECT_COLUMN_2}\nRECT_COLUMN_3: {RECT_COLUMN_3}\nRECT_COLUMN_4: {RECT_COLUMN_4}\nRECT_COLUMN_5: {RECT_COLUMN_5}\nRECT_COLUMN_6: {RECT_COLUMN_6}\nRECT_COLUMN_7: {RECT_COLUMN_7}")

        # resize the images
        for img in CARD_IMAGES.keys():
            # print(f"img: {img}, W_CARD: {W_CARD}, H_CARD: {H_CARD}")
            CARD_IMAGES[img] = pygame.transform.scale(CARD_IMAGES[img], (W_CARD, H_CARD))
        DECK_IMAGE = pygame.transform.scale(DECK_IMAGE, (W_CARD, H_CARD))


    update_window_dims(WIDTH, HEIGHT)
    dict_print(CARD_IMAGES, "Card-images")

    WIN = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
    pygame.display.set_caption("Solitaire")
    FONT = pygame.font.SysFont("comicsans", 16)


    def draw_drawing_pile(do_flip=False):
        drawing_pile = s.deck.cards
        # print("drawing_pile:", drawing_pile)
        if drawing_pile:
            top_card = drawing_pile[-1]
            if top_card.show:
                image = CARD_IMAGES[str(top_card)]
            else:
                image = DECK_IMAGE

            for i in range(min(3, len(s.deck)) - 1, -1, -1):
                shift_rect = pygame.Rect((i * X_SHIFT) + RECT_DRAW_PILE.left, RECT_DRAW_PILE.top, RECT_DRAW_PILE.width,
                                         RECT_DRAW_PILE.height)
                WIN.blit(image, shift_rect)  # to represent deck
            WIN.blit(image, RECT_DRAW_PILE)  # draw_pile
        else:
            pygame.draw.rect(WIN, GRAY_27, RECT_DRAW_PILE, 15, 30)
            pygame.draw.circle(WIN, GRAY_27, RECT_DRAW_PILE.center, 60, 15)

        if do_flip:
            pygame.display.flip()


    def draw_discard_pile(do_flip=False):
        discard_pile = s.deck.discarded
        # print("discard_pile:", discard_pile)
        # print(f"CARD_IMAGES{len(CARD_IMAGES)}:", CARD_IMAGES)
        if discard_pile:
            top_card = discard_pile[-1]
            top_card.show = True
            if top_card.show or 1:
                image = CARD_IMAGES[str(top_card)]

                for i in range(min(3, len(s.deck.discarded)) - 1, -1, -1):
                    shift_rect = pygame.Rect((i * X_SHIFT) + RECT_DISCARD_PILE.left, RECT_DISCARD_PILE.top,
                                             RECT_DISCARD_PILE.width, RECT_DISCARD_PILE.height)
                    WIN.blit(image, shift_rect)  # to represent deck
                if not CARD_SELECTED or top_card != CARD_SELECTED["card"]:
                    WIN.blit(image, RECT_DISCARD_PILE)  # discard_pile
                else:
                    WIN.blit(image, CARD_SELECTED["rect"])  # discard_pile
            else:
                # dont draw if nothing
                pass

        if do_flip:
            pygame.display.flip()


    def draw_foundations(do_flip=False):
        founds = s.foundations
        for i, found in founds.items():
            if found:
                top_card = found[-1]
                top_card.show = True
                image = CARD_IMAGES[str(top_card)]
                WIN.blit(image, eval(f"RECT_FOUNDATION_{i + 1}"))  # discard_pile
        if do_flip:
            pygame.display.flip()


    def draw_columns(do_flip=False):
        columns = s.columns
        for i, cols in enumerate(columns):
            # print(f"i: {i}, c: {cols}")
            if cols:
                image = DECK_IMAGE
                rect = eval(f"RECT_COLUMN_{i + 1}")
                ys = len(cols) - 1
                top_card = cols[-1]
                for j in range(ys):
                    # print(f"{j * ' '}ys: {ys}, j: {j}, (j * Y_SHIFT): {j * Y_SHIFT}")
                    shift_rect = pygame.Rect(rect.left + ((ys - j) * COL_OFFSET), (j * Y_SHIFT) + rect.top,
                                             rect.width, rect.height)
                    if CARD_SELECTED and top_card == CARD_SELECTED["card"]:
                        # shift_rect = pygame.Rect(CARD_SELECTED["rect"].left, (((ys - 1 - j) + 0) * Y_SHIFT) + (CARD_SELECTED["rect"].top - (CARD_SELECTED["rect"].height / 2)), CARD_SELECTED["rect"].width, CARD_SELECTED["rect"].height)
                        # shift_rect = pygame.Rect(CARD_SELECTED["rect"].left + ((ys - j) * COL_OFFSET), (j * Y_SHIFT) + (CARD_SELECTED["rect"].top - (CARD_SELECTED["rect"].height / 2)), CARD_SELECTED["rect"].width, CARD_SELECTED["rect"].height)
                        shift_rect = pygame.Rect(CARD_SELECTED["rect"].left + ((ys - j) * COL_OFFSET), (j * Y_SHIFT) + CARD_SELECTED["rect"].top,
                                                 CARD_SELECTED["rect"].width, CARD_SELECTED["rect"].height)
                    WIN.blit(image, shift_rect)
                    # pygame.draw.rect(WIN, INDIGO, shift_rect)

                top_card.show = True
                image = CARD_IMAGES[str(top_card)]
                rect.top += (Y_SHIFT * (len(cols) - 1))
                if not CARD_SELECTED or top_card != CARD_SELECTED["card"]:
                    WIN.blit(image, rect)  # discard_pile
                else:
                    WIN.blit(image, pygame.Rect(CARD_SELECTED["rect"].left, CARD_SELECTED["rect"].top + (Y_SHIFT * (len(cols) - 1)),
                                                CARD_SELECTED["rect"].width, CARD_SELECTED["rect"].height))
                # WIN.blit(image, rect)
                # rect.top = COL_TOP
        if do_flip:
            pygame.display.flip()


    def clicked_deck():
        if s.can_draw():
            cards = s.draw_card()[0]
        # elif s.can_reset():
        else:
            s.reset()
            cards = s.draw_card()[0]

        pygame.display.flip()


    def reset_column_heights():
        for i in range(N_COLS):
            if CARD_SELECTED:
                if CARD_SELECTED["col_idx"] == i:
                    # print("skipping:", i)
                    continue
            rect = eval(f"RECT_COLUMN_{i + 1}")
            rect.top = COL_TOP


    run = True
    clock = pygame.time.Clock()
    s.init_new_game()

    while run:
        clock.tick(60)
        reset_column_heights()
        WIN.fill(BLACK)

        if CARD_SELECTED:
            pass
            # print("CARD_SELECTED:", CARD_SELECTED["card"])

        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if RECT_DRAW_PILE.collidepoint(*mouse_pos):
                    # clicked deck
                    clicked_deck()
                for i in range(N_COLS):
                    rect = eval(f"RECT_COLUMN_{i + 1}")
                    if rect.collidepoint(*mouse_pos):
                        # clicked_column
                        CARD_SELECTED.update({
                            "card": s.get_top_card(i),
                            "col_idx": i,
                            "rect": pygame.Rect(rect.left, rect.top, rect.width, rect.height),
                            "og_rect": rect
                        })
                if RECT_DISCARD_PILE.collidepoint(*mouse_pos):
                    CARD_SELECTED.update({
                        "card": s.deck.discarded[-1],
                        "col_idx": None,
                        "og_rect": RECT_DISCARD_PILE,
                        "rect": pygame.Rect(RECT_DISCARD_PILE.left, RECT_DISCARD_PILE.top,
                                               RECT_DISCARD_PILE.width, RECT_DISCARD_PILE.height)
                        # "og_rect": pygame.Rect(CARD_SELECTED["og_rect"].left, CARD_SELECTED["og_rect"].top,
                        #                        CARD_SELECTED["og_rect"].width, CARD_SELECTED["og_rect"].height)
                    })
            elif event.type == pygame.MOUSEMOTION:
                if CARD_SELECTED:
                    n_rect = CARD_SELECTED["rect"]
                    n_rect.center = mouse_pos
                    CARD_SELECTED.update({
                        # "card": CARD_SELECTED["card"],
                        # "col_idx": CARD_SELECTED["col_idx"],
                        "rect": n_rect
                        # "og_rect": pygame.Rect(CARD_SELECTED["og_rect"].left, CARD_SELECTED["og_rect"].top,
                        #                        CARD_SELECTED["og_rect"].width, CARD_SELECTED["og_rect"].height)
                    })
                    # pygame.display.update(CARD_SELECTED["rect"])

            elif event.type == pygame.MOUSEBUTTONUP:
                if CARD_SELECTED:
                    print("returning rect: <{}> to <{}>".format(CARD_SELECTED["rect"], CARD_SELECTED["og_rect"]))
                    CARD_SELECTED.update({"rect": CARD_SELECTED["og_rect"]})
                    CARD_SELECTED = {}

            elif event.type == pygame.VIDEORESIZE:
                w, h = event.dict["size"]
                update_window_dims(w, h)

        draw_drawing_pile()
        draw_discard_pile()
        draw_foundations()
        draw_columns()
        pygame.display.flip()

    pygame.quit()

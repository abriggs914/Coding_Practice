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

    ALLOW_TESTING = True
    WIDTH, HEIGHT = 900, 600
    W_CARD, H_CARD = 75, 135
    W_CARD, H_CARD = 178, 267
    W_CARD_SMALL, H_CARD_SMALL = W_CARD * 0.1, H_CARD * 0.1
    F_W_CARD, F_H_CARD = 2 * 0.04, 6 * 0.04
    F_W_CARD_SMALL, F_H_CARD_SMALL = F_W_CARD * 0.185, F_H_CARD * 0.185
    WIDTH_BUTTONBAR, HEIGHT_BUTTONBAR = 80, 150

    LEFT_MOST, TOP_MOST = 35, 35
    X_SHIFT = -10
    Y_SHIFT = 45
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

    MARGIN_BUTTON_BAR = 10
    BUTTON_BAR_SPACE = 5
    RECT_BUTTON_BAR = pygame.Rect(RECT_DRAW_PILE.left, COL_TOP, WIDTH_BUTTONBAR, HEIGHT_BUTTONBAR)
    RECT_SETTINGS = pygame.Rect(
        RECT_BUTTON_BAR.left + MARGIN_BUTTON_BAR,
        COL_TOP + MARGIN_BUTTON_BAR + (0 * BUTTON_BAR_SPACE),
        WIDTH_BUTTONBAR - (2 * MARGIN_BUTTON_BAR),
        (HEIGHT_BUTTONBAR - ((2 * MARGIN_BUTTON_BAR) + BUTTON_BAR_SPACE)) / 2)
    RECT_TEST_RESHUFFLE = pygame.Rect(
        RECT_BUTTON_BAR.left + MARGIN_BUTTON_BAR,
        RECT_SETTINGS.bottom + BUTTON_BAR_SPACE,
        WIDTH_BUTTONBAR - (2 * MARGIN_BUTTON_BAR),
        (HEIGHT_BUTTONBAR - ((2 * MARGIN_BUTTON_BAR) + BUTTON_BAR_SPACE)) / 2)

    # Load images once
    CARD_IMAGES = dict(
        zip(list(map(str, s.deck.cards)), [pygame.image.load(_img) for _img in [img.image for img in s.deck.cards]]))
    # Load small images once
    CARD_IMAGES_SMALL = dict(
        zip(list(map(str, s.deck.cards)), [pygame.image.load(_img) for _img in [img.image for img in s.deck.cards]]))
    print(f"[img.image for img in s.deck.cards]{len([img.image for img in s.deck.cards])}:",
          [img.image for img in s.deck.cards])
    DECK_IMAGE = pygame.image.load(s.deck.image)

    CARD_SELECTED = {
        "card": None,
        "col_idx": None,
        "rect": None,
        "og_rect": None,
        "offset": None
    }

    STYLES = [
        {
            "win_back_colour": BLACK,
            "draw_pile_reset_rect": GRAY_27,
            "draw_pile_reset_circle": GRAY_27,
            "card_selected_outline": GOLDENROD,
            "deck_back": (r"""C:\Users\ABriggs\Documents\Coding Practice\Coding_Practice\Resources\Cards\back_blue_&_yellow_diamonds.png""", r"""C:\Users\abrig\Documents\Coding_Practice\Resources\Cards\back_blue_&_yellow_diamonds.png"""),
            "test_button_reshuffle": {
                "back_colour": RED_4__DARKRED_
            },
            "buttonbar": {
                "back_colour": GRAY_99
            },
            "button_settings": {
                "back_colour": GRAY_27
            }
        },
        {
            "win_back_colour": BLACK,
            "draw_pile_reset_rect": GRAY_27,
            "draw_pile_reset_circle": GRAY_27,
            "card_selected_outline": GOLDENROD,
            "deck_back": (r"""C:\Users\ABriggs\Documents\Coding Practice\Coding_Practice\Resources\Cards\back_blue_&_yellow_diamonds.png""", r"""C:\Users\abrig\Documents\Coding_Practice\Resources\Cards\back_blue_&_yellow_diamonds.png"""),
            "test_button_reshuffle": {
                "back_colour": RED_4__DARKRED_
            },
            "buttonbar": {
                "back_colour": GRAY_99
            },
            "button_settings": {
                "back_colour": GREEN_4
            }
        }
    ]
    STYLE_INDEX = 0

    def set_style(index):
        global STYLE_INDEX
        index = index % len(STYLES)
        STYLE_INDEX = index

    def check_card_selected(*keys):
        checked = None
        for k in keys:
            if k not in CARD_SELECTED:
                checked = False
                break
            checked = (checked if checked is not None else True) and (CARD_SELECTED[k] is not None)
        if checked is not None:
            return checked
        return any([v is not None for v in CARD_SELECTED.items()])

    def update_window_dims(w, h):
        global WIDTH, HEIGHT, W_CARD, H_CARD, W_CARD_SMALL, H_CARD_SMALL, COL_TOP,\
            RECT_DRAW_PILE, RECT_DISCARD_PILE,\
            RECT_FOUNDATION_1, RECT_FOUNDATION_2, RECT_FOUNDATION_3, RECT_FOUNDATION_4,\
            RECT_COLUMN_1, RECT_COLUMN_2, RECT_COLUMN_3, RECT_COLUMN_4,\
            RECT_COLUMN_5, RECT_COLUMN_6, RECT_COLUMN_7,\
            DECK_IMAGE, CARD_IMAGES, CARD_IMAGES_SMALL, CARD_SELECTED,\
            RECT_TEST_RESHUFFLE, RECT_BUTTON_BAR, RECT_SETTINGS
        WIDTH, HEIGHT = w, h
        W_CARD, H_CARD = int(F_W_CARD * WIDTH), int(F_H_CARD * HEIGHT)
        W_CARD_SMALL, H_CARD_SMALL = int(F_W_CARD_SMALL * WIDTH), int(F_H_CARD_SMALL * HEIGHT)
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

        RECT_BUTTON_BAR = pygame.Rect(RECT_DRAW_PILE.left, COL_TOP, WIDTH_BUTTONBAR, HEIGHT_BUTTONBAR)
        RECT_SETTINGS = pygame.Rect(
            RECT_BUTTON_BAR.left + MARGIN_BUTTON_BAR,
            COL_TOP + MARGIN_BUTTON_BAR + (0 * BUTTON_BAR_SPACE),
            WIDTH_BUTTONBAR - (2 * MARGIN_BUTTON_BAR),
            (HEIGHT_BUTTONBAR - ((2 * MARGIN_BUTTON_BAR) + BUTTON_BAR_SPACE)) / 2)
        RECT_TEST_RESHUFFLE = pygame.Rect(
            RECT_BUTTON_BAR.left + MARGIN_BUTTON_BAR,
            RECT_SETTINGS.bottom + BUTTON_BAR_SPACE,
            WIDTH_BUTTONBAR - (2 * MARGIN_BUTTON_BAR),
            (HEIGHT_BUTTONBAR - ((2 * MARGIN_BUTTON_BAR) + BUTTON_BAR_SPACE)) / 2)

        # resize the images
        for img in CARD_IMAGES.keys():
            # print(f"img: {img}, W_CARD: {W_CARD}, H_CARD: {H_CARD}")
            CARD_IMAGES[img] = pygame.transform.scale(CARD_IMAGES[img], (W_CARD, H_CARD))
        DECK_IMAGE = pygame.transform.scale(DECK_IMAGE, (W_CARD, H_CARD))

        # resize the small images
        for img in CARD_IMAGES_SMALL.keys():
            # print(f"img: {img}, W_CARD: {W_CARD}, H_CARD: {H_CARD}")
            CARD_IMAGES_SMALL[img] = pygame.transform.scale(CARD_IMAGES_SMALL[img], (W_CARD_SMALL, H_CARD_SMALL))


    update_window_dims(WIDTH, HEIGHT)
    dict_print(CARD_IMAGES, "Card-images")

    WIN = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
    pygame.display.set_caption("Solitaire")
    FONT = pygame.font.SysFont("comicsans", 16)


    def draw_buttonbar(do_flip=False):
        pygame.draw.rect(WIN, STYLES[STYLE_INDEX]["buttonbar"]["back_colour"], RECT_BUTTON_BAR, 2)
        if do_flip:
            pygame.display.flip()
        draw_style_change_button(do_flip)
        draw_test_reshuffle(do_flip)


    def draw_style_change_button(do_flip=False):
        pygame.draw.rect(WIN, STYLES[STYLE_INDEX]["button_settings"]["back_colour"], RECT_SETTINGS)
        textBitmap = FONT.render("settings", True, BLACK)
        w = textBitmap.get_width()
        h = textBitmap.get_height()
        WIN.blit(textBitmap, (RECT_SETTINGS.x + ((RECT_SETTINGS.width - w) / 2), (RECT_SETTINGS.y + ((RECT_SETTINGS.height - h) / 2))))
        if do_flip:
            pygame.display.flip()


    def draw_test_reshuffle(do_flip=False):
        pygame.draw.rect(WIN, STYLES[STYLE_INDEX]["test_button_reshuffle"]["back_colour"], RECT_TEST_RESHUFFLE)
        textBitmap = FONT.render("reshuffle", True, BLACK)
        w = textBitmap.get_width()
        h = textBitmap.get_height()
        WIN.blit(textBitmap, (RECT_TEST_RESHUFFLE.x + ((RECT_TEST_RESHUFFLE.width - w) / 2), (RECT_TEST_RESHUFFLE.y + ((RECT_TEST_RESHUFFLE.height - h) / 2))))
        if do_flip:
            pygame.display.flip()


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
            pygame.draw.rect(WIN, STYLES[STYLE_INDEX]["draw_pile_reset_rect"], RECT_DRAW_PILE, 15, 30)
            pygame.draw.circle(WIN, STYLES[STYLE_INDEX]["draw_pile_reset_circle"], RECT_DRAW_PILE.center, 60, 15)

        if do_flip:
            pygame.display.flip()


    def draw_discard_pile(do_flip=False):
        discard_pile = s.deck.discarded
        # print("discard_pile:", discard_pile)
        # print(f"CARD_IMAGES{len(CARD_IMAGES)}:", CARD_IMAGES)
        if discard_pile:
            top_card = discard_pile[-1]
            if not top_card.show:
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
                if not top_card.show:
                    top_card.show = True
                image = CARD_IMAGES[str(top_card)]
                WIN.blit(image, eval(f"RECT_FOUNDATION_{i + 1}"))  # discard_pile
        if do_flip:
            pygame.display.flip()


    def draw_columns(do_flip=False):
        columns = s.columns
        # print(f"columns: {columns}")
        for i, cols in enumerate(columns):
            # print(f"i: {i}, c: {cols}")
            if cols:
                image = DECK_IMAGE
                rect = eval(f"RECT_COLUMN_{i + 1}")
                n_shown = len([c for c in cols if c.show])
                # print(f"n_shown: {n_shown}")
                ys = len(cols) - n_shown
                top_cards = cols[-n_shown:]
                if check_card_selected("offset"):
                    offset = CARD_SELECTED["offset"]
                    print(f"offset: {offset}, ys: {ys}")
                for j in range(ys):
                    # col_card = cols[j]
                    # print(f"{j * ' '}ys: {ys}, j: {j}, (j * Y_SHIFT): {j * Y_SHIFT}")
                    shift_rect = pygame.Rect(rect.left + ((ys - j) * COL_OFFSET), (j * Y_SHIFT) + rect.top,
                                             rect.width, rect.height)
                    if check_card_selected("card", "rect") and CARD_SELECTED["card"] in top_cards and CARD_SELECTED["offset"] - 1 <= j:
                        # shift_rect = pygame.Rect(CARD_SELECTED["rect"].left, (((ys - 1 - j) + 0) * Y_SHIFT) + (CARD_SELECTED["rect"].top - (CARD_SELECTED["rect"].height / 2)), CARD_SELECTED["rect"].width, CARD_SELECTED["rect"].height)
                        # shift_rect = pygame.Rect(CARD_SELECTED["rect"].left + ((ys - j) * COL_OFFSET), (j * Y_SHIFT) + (CARD_SELECTED["rect"].top - (CARD_SELECTED["rect"].height / 2)), CARD_SELECTED["rect"].width, CARD_SELECTED["rect"].height)
                        shift_rect = pygame.Rect(CARD_SELECTED["rect"].left + ((ys - j) * COL_OFFSET), (j * Y_SHIFT) + CARD_SELECTED["rect"].top,
                                                 CARD_SELECTED["rect"].width, CARD_SELECTED["rect"].height)
                    # else:
                    #     shift_rect =
                    WIN.blit(image, shift_rect)
                    # pygame.draw.rect(WIN, INDIGO, shift_rect)

                top_card_list = top_cards[-max(1, n_shown):]
                for j, top_card in enumerate(top_card_list):
                    if not top_card.show:
                        # print(f"\tsetting top_card: {top_card}, n_shown: {n_shown}, top_cards: {top_cards}")
                        top_card.show = True
                    image = CARD_IMAGES[str(top_card)]
                    image_small = CARD_IMAGES_SMALL[str(top_card)]
                    # rect.top += (Y_SHIFT * ys)
                    if not CARD_SELECTED or top_card != CARD_SELECTED["card"]:
                        top_rect = pygame.Rect(rect)
                        top_rect.top = top_rect.top + (Y_SHIFT * (j + ys))
                        top_right_rect = pygame.Rect(top_rect)
                        top_right_rect.width = W_CARD_SMALL
                        top_right_rect.height = H_CARD_SMALL
                        top_right_rect.left = top_rect.right - (2 * top_right_rect.width)
                        top_right_rect.top += H_CARD_SMALL / 2
                        WIN.blit(image, top_rect)
                        WIN.blit(image_small, top_right_rect)
                    else:
                        # print(f"top: {CARD_SELECTED['rect'].top} calc: {CARD_SELECTED['rect'].top + (Y_SHIFT * ys)}, ((len(cols) - 1) - j): {((len(top_card_list) - 1) - j)}")
                        fan_rect = pygame.Rect(CARD_SELECTED["rect"].left, CARD_SELECTED["rect"].top + (Y_SHIFT * ys),
                                                    CARD_SELECTED["rect"].width, CARD_SELECTED["rect"].height)
                        WIN.blit(image, fan_rect)
                        # pygame.draw.rect(WIN, TURQUOISE, fan_rect)
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


    def clicked_settings():
        print("clicked settings")
        set_style(STYLE_INDEX + 1)


    def clicked_reshuffle():
        print("clicked reshuffle")
        s.init_new_game()


    def reset_column_heights():
        for i in range(N_COLS):
            if check_card_selected():
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

        if check_card_selected():
            pass
            # print("CARD_SELECTED:", CARD_SELECTED["card"])

        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:

                # clicked settings
                if ALLOW_TESTING and RECT_SETTINGS.collidepoint(*mouse_pos):
                    clicked_settings()

                # clicked reshuffle
                if ALLOW_TESTING and RECT_TEST_RESHUFFLE.collidepoint(*mouse_pos):
                    clicked_reshuffle()

                # clicked deck
                if RECT_DRAW_PILE.collidepoint(*mouse_pos):
                    clicked_deck()

                # clicked column
                for i in range(N_COLS):
                    rect = eval(f"RECT_COLUMN_{i + 1}")
                    offset = len(s.columns[i])
                    top_rect = pygame.Rect(rect)
                    top_rect.top += ((offset - 1) * Y_SHIFT)
                    if top_rect.collidepoint(*mouse_pos):
                        # clicked_column
                        CARD_SELECTED.update({
                            "card": s.get_top_card(i),
                            "col_idx": i,
                            "rect": pygame.Rect(top_rect),
                            "og_rect": top_rect,
                            "offset": offset,
                            "from_col": i
                        })
                    else:
                        for j in range(offset):
                            col_rect = pygame.Rect(top_rect)
                            col_rect.height = Y_SHIFT
                            col_rect.top -= j * Y_SHIFT
                            if col_rect.collidepoint(*mouse_pos):
                                # clicked_column
                                CARD_SELECTED.update({
                                    "card": s.get_top_card(i),
                                    "col_idx": i,
                                    "rect": pygame.Rect(rect),
                                    "og_rect": rect,
                                    "offset": offset - j,
                                    "from_col": i
                                })
                                break

                # clicked discard pile
                if RECT_DISCARD_PILE.collidepoint(*mouse_pos):
                    CARD_SELECTED.update({
                        "card": s.deck.discarded[-1],
                        "col_idx": None,
                        "og_rect": RECT_DISCARD_PILE,
                        "rect": pygame.Rect(RECT_DISCARD_PILE.left, RECT_DISCARD_PILE.top,
                                               RECT_DISCARD_PILE.width, RECT_DISCARD_PILE.height),
                        "from_col": "discard_pile"
                        # "og_rect": pygame.Rect(CARD_SELECTED["og_rect"].left, CARD_SELECTED["og_rect"].top,
                        #                        CARD_SELECTED["og_rect"].width, CARD_SELECTED["og_rect"].height)
                    })
            elif event.type == pygame.MOUSEMOTION:
                if check_card_selected("rect"):
                    n_rect = CARD_SELECTED["rect"]
                    CARD_SELECTED.update({
                        # "card": CARD_SELECTED["card"],
                        # "col_idx": CARD_SELECTED["col_idx"],
                        "rect": n_rect
                        # "og_rect": pygame.Rect(CARD_SELECTED["og_rect"].left, CARD_SELECTED["og_rect"].top,
                        #                        CARD_SELECTED["og_rect"].width, CARD_SELECTED["og_rect"].height)
                    })
                    # pygame.display.update(CARD_SELECTED["rect"])

            elif event.type == pygame.MOUSEBUTTONUP:
                if check_card_selected("rect"):
                    print("returning rect: <{}> to <{}>".format(CARD_SELECTED["rect"], CARD_SELECTED["og_rect"]))
                    card_rect = pygame.Rect(CARD_SELECTED["rect"])
                    card = CARD_SELECTED["card"]
                    from_col = CARD_SELECTED["from_col"]
                    if from_col == "discard_pile":
                        print("pulling from the draw pile")

                    for i in range(N_COLS):
                        col_rect = eval(f"RECT_COLUMN_{i + 1}")
                        col_offset = len(s.columns[i])
                        col_rect.top += (i * Y_SHIFT)
                        if i != from_col:
                            if card_rect.colliderect(col_rect):
                                if s.can_stack_col(i, card):
                                    print(f"successfully placed a card on column {i}")
                                    s.stack(from_col, i, card)

                    CARD_SELECTED.update({"rect": CARD_SELECTED["og_rect"]})
                    CARD_SELECTED = {}

            elif event.type == pygame.VIDEORESIZE:
                w, h = event.dict["size"]
                update_window_dims(w, h)

        if check_card_selected("rect"):
            CARD_SELECTED["rect"].center = mouse_pos
            if check_card_selected("offset"):
                CARD_SELECTED["rect"].top -= (CARD_SELECTED["offset"] * Y_SHIFT)

        draw_drawing_pile()
        draw_discard_pile()
        draw_foundations()
        draw_columns()
        draw_buttonbar()

        # this goes last to show all the above drawings
        pygame.display.flip()

        if check_card_selected("rect"):
            rect = pygame.Rect(CARD_SELECTED["rect"])
            if check_card_selected("offset"):
                offset = CARD_SELECTED["offset"] - 1
            else:
                offset = 0
            rect.top += (offset * Y_SHIFT)
            # pygame.draw.rect(WIN, RED, rect)
            WIN.blit(CARD_IMAGES[str(CARD_SELECTED["card"])], rect)
            pygame.display.update(rect)

    pygame.quit()

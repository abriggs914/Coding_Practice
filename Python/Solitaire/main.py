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

    WIDTH, HEIGHT = 1600, 1000
    WIN = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Solitaire")
    FONT = pygame.font.SysFont("comicsans", 16)

    W_CARD, H_CARD = 75, 135
    W_CARD, H_CARD = 178, 267
    LEFT_MOST, TOP_MOST = 25, 25
    SPACE = 15
    RECT_DRAW_PILE = pygame.Rect(LEFT_MOST, TOP_MOST, W_CARD, H_CARD)
    RECT_DISCARD_PILE = pygame.Rect(RECT_DRAW_PILE.left + (1 * (RECT_DRAW_PILE.width + SPACE)), TOP_MOST, W_CARD, H_CARD)
    RECT_FOUNDATION_1 = pygame.Rect(RECT_DRAW_PILE.left + (4 * (RECT_DRAW_PILE.width + SPACE)), TOP_MOST, W_CARD, H_CARD)
    RECT_FOUNDATION_2 = pygame.Rect(RECT_DRAW_PILE.left + (5 * (RECT_DRAW_PILE.width + SPACE)), TOP_MOST, W_CARD, H_CARD)
    RECT_FOUNDATION_3 = pygame.Rect(RECT_DRAW_PILE.left + (6 * (RECT_DRAW_PILE.width + SPACE)), TOP_MOST, W_CARD, H_CARD)
    RECT_FOUNDATION_4 = pygame.Rect(RECT_DRAW_PILE.left + (7 * (RECT_DRAW_PILE.width + SPACE)), TOP_MOST, W_CARD, H_CARD)
    RECT_COLUMN_1 = pygame.Rect(RECT_DRAW_PILE.left + (1 * (RECT_DRAW_PILE.width + SPACE)), TOP_MOST + RECT_FOUNDATION_1.height + SPACE, W_CARD, H_CARD)
    RECT_COLUMN_2 = pygame.Rect(RECT_DRAW_PILE.left + (2 * (RECT_DRAW_PILE.width + SPACE)), TOP_MOST + RECT_FOUNDATION_1.height + SPACE, W_CARD, H_CARD)
    RECT_COLUMN_3 = pygame.Rect(RECT_DRAW_PILE.left + (3 * (RECT_DRAW_PILE.width + SPACE)), TOP_MOST + RECT_FOUNDATION_1.height + SPACE, W_CARD, H_CARD)
    RECT_COLUMN_4 = pygame.Rect(RECT_DRAW_PILE.left + (4 * (RECT_DRAW_PILE.width + SPACE)), TOP_MOST + RECT_FOUNDATION_1.height + SPACE, W_CARD, H_CARD)
    RECT_COLUMN_5 = pygame.Rect(RECT_DRAW_PILE.left + (5 * (RECT_DRAW_PILE.width + SPACE)), TOP_MOST + RECT_FOUNDATION_1.height + SPACE, W_CARD, H_CARD)
    RECT_COLUMN_6 = pygame.Rect(RECT_DRAW_PILE.left + (6 * (RECT_DRAW_PILE.width + SPACE)), TOP_MOST + RECT_FOUNDATION_1.height + SPACE, W_CARD, H_CARD)
    RECT_COLUMN_7 = pygame.Rect(RECT_DRAW_PILE.left + (7 * (RECT_DRAW_PILE.width + SPACE)), TOP_MOST + RECT_FOUNDATION_1.height + SPACE, W_CARD, H_CARD)

    CARD_IMAGES = dict(zip(list(map(str, s.deck.cards)), [pygame.image.load(_img) for _img in [img.image for img in s.deck.cards]]))
    print(f"[img.image for img in s.deck.cards]{len([img.image for img in s.deck.cards])}:", [img.image for img in s.deck.cards])
    DECK_IMAGE = pygame.image.load(s.deck.image)

    # resize the images
    for img in CARD_IMAGES.keys():
        CARD_IMAGES[img] = pygame.transform.scale(CARD_IMAGES[img], (W_CARD, H_CARD))
    DECK_IMAGE = pygame.transform.scale(DECK_IMAGE, (W_CARD, H_CARD))

    dict_print(CARD_IMAGES, "Card-images")

    def draw_drawing_pile(do_flip=False):
        drawing_pile = s.deck.cards
        print("drawing_pile:", drawing_pile)
        if drawing_pile:
            top_card = drawing_pile[-1]
            if top_card.show:
                image = CARD_IMAGES[str(top_card)]
            else:
                image = DECK_IMAGE
            WIN.blit(image, RECT_DRAW_PILE)  # draw_pile

        if do_flip:
            pygame.display.flip()

    def draw_discard_pile(do_flip=False):
        discard_pile = s.deck.discarded
        print("discard_pile:", discard_pile)
        # print(f"CARD_IMAGES{len(CARD_IMAGES)}:", CARD_IMAGES)
        if discard_pile:
            top_card = discard_pile[-1]
            top_card.show = True
            if top_card.show or 1:
                image = CARD_IMAGES[str(top_card)]
                WIN.blit(image, RECT_DISCARD_PILE)  # discard_pile
            else:
                # dont draw if nothing
                pass
                # image = DECK_IMAGE

        if do_flip:
            pygame.display.flip()

    def draw_foundations(do_flip=False):
        # found_1 = s.foundations[Suit.HEARTS["name"]]
        # found_2 = s.foundations[Suit.SPADES["name"]]
        # found_3 = s.foundations[Suit.DIAMONDS["name"]]
        # found_4 = s.foundations[Suit.CLUBS["name"]]
        # founds = [found_1, found_2, found_3, found_4]
        founds = s.foundations
        for i, found in founds.items():
            if found:
                top_card = found[-1]
                top_card.show = True
                image = CARD_IMAGES[str(top_card)]
                WIN.blit(image, eval(f"RECT_FOUNDATION_{i+1}"))  # discard_pile
        if do_flip:
            pygame.display.flip()

    def draw_columns(do_flip=False):
        columns = s.columns
        for i, cols in enumerate(columns):
            # print(f"i: {i}, c: {cols}")
            if cols:
                top_card = cols[-1]
                top_card.show = True
                image = CARD_IMAGES[str(top_card)]
                WIN.blit(image, eval(f"RECT_COLUMN_{i+1}"))  # discard_pile
        if do_flip:
            pygame.display.flip()

    run = True
    clock = pygame.time.Clock()
    s.init_new_game()

    while run:
        clock.tick(60)
        WIN.fill(BLACK)

        draw_drawing_pile()
        draw_discard_pile()
        draw_foundations()
        draw_columns()
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        pygame.display.update()

    pygame.quit()
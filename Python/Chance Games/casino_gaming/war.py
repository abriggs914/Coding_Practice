import random
from styles import BORDER

def gen_new_deck() :
    return {"hearts" : [x for x in range(2, 15)],
            "diamonds" : [x for x in range(2, 15)],
            "clubs" : [x for x in range(2, 15)],
            "spades" : [x for x in range(2, 15)]}

def draw_card(deck) :
    suit = random.choice(list(deck.keys()))
    while len(deck[suit]) == 0 :
        suit = random.choice(list(deck.keys()))
    val = random.choice(deck[suit])
    # print(deck)
    # print(suit)
    # print(val)
    deck[suit].remove(val)
    return suit, val

def adjust_card_val(card) :
    if card < 11 :
        return card
    elif card % 11 == 0 :
        return "J"
    elif card % 12 == 0 :
        return "Q"
    elif card % 13 == 0 :
        return "K"
    elif card % 14 == 0 :
        return "A"

def need_new_deck(deck) :
    cards = 0
    for suit in deck.keys() :
        cards += len(deck[suit])
    if cards < 2 :
        print("\n\tHang - on. Getting a new deck!\n")
        return True
    return False

def war(bet, deck=None) :
    print("\n" + BORDER)
    deck = gen_new_deck() if deck is None else deck
    if need_new_deck(deck) :
        deck = gen_new_deck()
    card_A_suit, card_A_val = draw_card(deck)
    card_B_suit, card_B_val = draw_card(deck)
    result = "3... 2... 1... War!\n"
    if card_A_val == card_B_val :
        result += "\tTie!"
        earned = 0
    else :
        if card_A_val > card_B_val :
            result += "\tYou win!"
            earned = bet
        else :
            result += "\tYou lose"
            earned = -1 * bet
    card_A_val = adjust_card_val(card_A_val)
    card_B_val = adjust_card_val(card_B_val)
    result += "\nyour card:\t" + str(card_A_val) + " of " + str(card_A_suit)
    result += "\nCPU card:\t" + str(card_B_val) + " of " + str(card_B_suit)
    result += "\n"
    print(result + "\nearning you: $ " + str(earned))
    print(BORDER + "\n")
    return earned
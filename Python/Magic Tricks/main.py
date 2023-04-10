from utility import *
from random import shuffle, randint

class Suit:
    HEARTS = {"name": "Hearts", "_image": None, "colour": "red"}
    SPADES = {"name": "Spades", "_image": None, "colour": "black"}
    DIAMONDS = {"name": "Diamonds", "_image": None, "colour": "red"}
    CLUBS = {"name": "Clubs", "_image": None, "colour": "black"}

class Card:

    VALID_FACE = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
    VALID_SUIT = [Suit.HEARTS, Suit.SPADES, Suit.DIAMONDS, Suit.CLUBS]

    def __init__(self, value, suit, image=None, show=False):
        assert suit in self.VALID_SUIT
        self._value = self.normalize_input_value(value)
        self._suit = suit
        self._image = image if image is not None else self.gen_image_url()
        self._show = show

    def set_value(self, value):
        if value not in self.VALID_FACE:
            raise TypeError("value parameter must be valid.")
        self._value = value

    def set_suit(self, value):
        if value not in self.VALID_SUIT:
            raise TypeError("suit parameter must be a suit.")
        self._suit = value

    def set_image(self, value):
        self._image = value

    def set_show(self, value):
        if value:
            print(f"showing {self}")
        self._show = value

    def get_value(self):
        return self._value

    def get_suit(self):
        return self._suit

    def get_image(self):
        print(f"\timg:<{self._image}>")
        return self._image

    def get_show(self):
        return self._show

    def del_value(self):
        del self._value

    def del_suit(self):
        del self._suit

    def del_image(self):
        del self._image

    def del_show(self):
        del self._show

    def is_red(self):
        return self.suit in [Suit.HEARTS, Suit.DIAMONDS]

    def is_black(self):
        return self.suit in [Suit.SPADES, Suit.CLUBS]

    def same_suit(self, other):
        return isinstance(other, Card) and self.suit == other.suit

    def same_face(self, other):
        return isinstance(other, Card) and self.value == other.value

    def same_value(self, other):
        return self.same_face(other)

    def same_card(self, other):
        return isinstance(other, Card) and self.same_face(other) and self.same_suit(other)

    def gen_image_url(self):
        # Location on work computer
        url = r"""C:\Users\ABriggs\Documents\Coding Practice\Coding_Practice\Resources\Cards\{}""".format(self.suit["name"].lower() + "_" + self.value + ".png")
        if not os.path.exists(url):
            # location on home computer
            url = r"""C:\Users\abrig\Documents\Coding_Practice\Resources\Cards\cropped\{}""".format(self.suit["name"].lower() + "_" + self.value + ".png")
            if not os.path.exists(url):
                raise FileNotFoundError(f"Cant find image file: \"{url}\"")
        return url

    def __eq__(self, other):
        return isinstance(other, Card) and all([
            self.value == other.value
            , self.suit == other.suit
        ])

    def __lt__(self, other):
        assert isinstance(other, Card)
        a = self.VALID_FACE.index(self.value)
        b = self.VALID_FACE.index(other.value)
        return a < b

    def __gt__(self, other):
        assert isinstance(other, Card)
        a = self.VALID_FACE.index(self.value)
        b = self.VALID_FACE.index(other.value)
        return a > b

    def __le__(self, other):
        assert isinstance(other, Card)
        a = self.VALID_FACE.index(self.value)
        b = self.VALID_FACE.index(other.value)
        return a <= b

    def __int__(self):
        v = self.value
        if v.isnumeric():
            return int(v)
        return (["J", "Q", "K", "", "A"].index(v) + 11) % 14

    def normalize_input_value(self, value, default="A"):
        # print("CALC B:", value)
        valid = list(range(1, 14)) + [str(i) for i in range(1, 14)]
        valid_w = ["ACE", "JACK", "QUEEN", "KING", "A", "J", "Q", "K"]
        v_l = {"1": "A", "11": "J", "12": "Q", "13": "K"}
        valid = valid + valid_w
        if isinstance(value, str):
            value = value.upper()
        if value not in valid:
            return self.normalize_input_value(default, "A") # double check that the default _value is valid too
        if value in valid_w:
            idx = valid_w.index(value)
            if idx < 4:
                idx += 4
            value = valid_w[idx]
        value = str(value)
        if value in v_l:
            value = v_l[value]
        # print("CALC A:", value)
        assert value in self.VALID_FACE
        return value

    def __repr__(self):
        return "{} of {}".format(self.value, self.suit["name"])

    value = property(get_value, set_value, del_value)
    suit = property(get_suit, set_suit, del_suit)
    image = property(get_image, set_image, del_image)
    show = property(get_show, set_show, del_show)


class Deck:

    def __init__(
            self,
            name,
            image=None,
            size=52,
            suits=(Suit.HEARTS, Suit.SPADES, Suit.DIAMONDS, Suit.CLUBS)):
        self.name = name
        self.image = image if image is not None else self.gen_image_url()
        self.size = size
        self.suits = suits

        self.cards = []
        self.og_cards = []
        self.discarded = []

        self.init_cards()

    def __len__(self):
        return len(self.cards)

    def gen_image_url(self):
        # Location on work computer
        url = r"""C:\Users\ABriggs\Documents\Coding Practice\Coding_Practice\Resources\Cards\back_blue_&_yellow_diamonds.png"""
        if not os.path.exists(url):
            # location on home computer
            url = r"""C:\Users\abrig\Documents\Coding_Practice\Resources\Cards\back_blue_&_yellow_diamonds.png"""
            if not os.path.exists(url):
                raise FileNotFoundError(f"Cant find image file: \"{url}\"")
        return url

    def init_cards(self):
        suits = self.suits
        p = int(self.size / len(suits))
        self.cards = [Card((i % p) + 1, suits[i // p]) for i in range(self.size)]
        self.og_cards = [Card((i % p) + 1, suits[i // p]) for i in range(self.size)]
        # print("self.cards:", self.cards)

    def shuffle(self):
        shuffle(self.cards)

    def use_card(self, card, discard=True):
        assert card in self.cards
        # print(f"FROM<{id(self.cards)}>")
        # print(f"REMOVING CARD <{card}>")
        # print(f"CARDS BEF <{len(self.cards)}>: <{self.cards}>")
        if discard:
            self.discarded.append(card)
        self.cards.remove(card)
        # print(f"CARDS AFT <{len(self.cards)}>: <{self.cards}>")

    def return_card(self, card, reshuffle=True):
        assert isinstance(card, Card), f"Error, param 'card' must be an instance of Card, got '{type(card)}.' "
        if card not in self.discarded:
            raise ValueError(f"Error, cannot return card '{card}', because it has not been discarded from this deck yet.")
        self.discarded.remove(card)
        self.cards.append(card)
        if reshuffle:
            self.shuffle()

    def draw(self, q=1, remove=True):
        hand = ()
        for i in range(q):
            if len(self.cards) == 0:
                raise ValueError("Out of cards to draw.")
            chx = choice(self.cards)
            hand = (*hand, chx)
            if remove:
                self.use_card(chx)
        return list(hand)

    def reset(self):
        self.cards = [card for card in self.og_cards]
        self.discarded = []
        for card in self.cards:
            card.show = False
        self.shuffle()

    def get_cards(self):
        return self.cards


def diff_to_13(card):
    assert isinstance(card, Card), "Error not a card"
    return 13 - int(card)


def pile_print(message=None):
    pile_res = ""
    ld = 15
    if message:
        pile_res += f"\n\n\t{message}\n\n"
    for j in range(mpl):
        for i, pile in enumerate(piles):
            if j < len(pile):
                pile_res += str(pile[j]).ljust(ld)
            else:
                pile_res += " " * ld
        pile_res += "\n"
    return pile_res


if __name__ == '__main__':
    d = Deck("a")
    hand = d.draw(5)
    print(f"{hand=}")
    piles = [[c] for c in hand]
    mpl = 0
    for i, c in enumerate(hand):
        d13 = 13 - int(c)
        print(f"{c=}, {c.value=}, i={int(c)}, d={d13}")
        for j in range(d13):
            piles[i].append(d.draw(1)[0])
        mpl = max(mpl, len(piles[i]))

    print(f"\nCards dealt in the initial 5 piles = {52 - len(d)}")
    print(f"\nCards in deck = {len(d)}")

    print(pile_print("Initial:"))

    i_1 = randint(0, 4)
    i_2 = i_1
    while i_2 == i_1:
        i_2 = randint(0, 4)

    print(f"Random piles to remove:\n\t\t1: {i_1 + 1}\n\t\t2: {i_2 + 1}\n")

    for c in piles[i_1] + piles[i_2]:
        print(f"returning card= {c}")
        d.return_card(c)
    del piles[i_1]
    del piles[clamp(0, i_2 - 1, 4)]

    print(pile_print("After removal:"))
    print(f"Cards in deck: {len(d)}")

    order = list(range(3))
    shuffle(order)
    piles = [piles[i] for i in order]

    print(f"{order=}")
    print(pile_print("After shuffling:"))

    sum_l_r = int(piles[0][0]) + int(piles[-1][0]) + 10
    print(f"sum L + R + 10 = {sum_l_r}")
    print(f"Cards in deck: {len(d)}")



# See PyCharm help at https://www.jetbrains.com/help/pycharm/

from utility import *

class Suit:
    HEARTS = {"name": "Hearts", "_image": None, "colour": "red"}
    SPADES = {"name": "Spades", "_image": None, "colour": "black"}
    DIAMONDS = {"name": "Diamonds", "_image": None, "colour": "red"}
    CLUBS = {"name": "Clubs", "_image": None, "colour": "black"}

class Card:

    VALID_FACE = ["A", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
    VALID_SUIT = [Suit.HEARTS, Suit.SPADES, Suit.DIAMONDS, Suit.CLUBS]

    def __init__(self, value, suit, image=None):
        assert suit in self.VALID_SUIT
        self._value = self.normalize_input_value(value)
        self._suit = suit
        self._image = image

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

    def get_value(self):
        return self._value

    def get_suit(self):
        return self._suit

    def get_image(self):
        return self._image

    def del_value(self):
        del self._value

    def del_suit(self):
        del self._suit

    def del_image(self):
        del self._image

    def is_red(self):
        return self._suit in [Suit.HEARTS, Suit.DIAMONDS]

    def is_black(self):
        return self._suit in [Suit.SPADES, Suit.CLUBS]

    def same_suit(self, other):
        return isinstance(other, Card) and self._suit == other._suit

    def same_face(self, other):
        return isinstance(other, Card) and self._value == other._value

    def same_value(self, other):
        return self.same_face(other)

    def same_card(self, other):
        return isinstance(other, Card) and self.same_face(other) and self.same_suit(other)

    def __eq__(self, other):
        return isinstance(other, Card) and all([
            self._value == other._value
            # , self._suit == other._suit
        ])

    def __lt__(self, other):
        assert isinstance(other, Card)
        a = self.VALID_FACE.index(self._value)
        b = self.VALID_FACE.index(other._value)
        return a < b

    def __gt__(self, other):
        assert isinstance(other, Card)
        a = self.VALID_FACE.index(self._value)
        b = self.VALID_FACE.index(other._value)
        return a > b

    def __le__(self, other):
        assert isinstance(other, Card)
        a = self.VALID_FACE.index(self._value)
        b = self.VALID_FACE.index(other._value)
        return a <= b

    def normalize_input_value(self, value, default="A"):
        valid = list(range(13)) + [str(i) for i in range(13)]
        valid_w = ["ACE", "JACK", "QUEEN", "KING", "A", "J", "Q", "K"]
        v_l = {"0": "A", "11": "J", "12": "Q", "13": "K"}
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
        assert value in self.VALID_FACE
        return value

    def __repr__(self):
        return "{} of {}".format(self._value, self._suit["name"])

    value = property(get_value, set_value, del_value)
    suit = property(get_suit, set_suit, del_suit)
    image = property(get_image, set_image, del_image)

class Deck:

    def __init__(
            self,
            name,
            image,
            size=52,
            suits=(Suit.HEARTS, Suit.SPADES, Suit.DIAMONDS, Suit.CLUBS)):
        self.name = name
        self.image = image
        self.size = size
        self.suits = suits

        self.cards = []
        self.discarded = []

        self.init_cards()

    def init_cards(self):
        suits = self.suits
        p = int(self.size / len(suits))
        self.cards = [Card(i % p, suits[i // p]) for i in range(self.size)]
        print("self.cards:", self.cards)

    def use_card(self, card, discard=True):
        assert card in self.cards
        if discard:
            self.discarded.append(card)
        self.cards.remove(card)

    def draw(self, q=1, remove=True):
        hand = []
        for i in range(q):
            if len(self.cards) == 0:
                raise ValueError("Out of cards to draw.")
            chx = choice(self.cards)
            hand.append(chx)
            if remove:
                self.use_card(chx)
        return hand


class Solitaire:
    def __init__(self):
        print("hey")
        self.deck = Deck("name", "image")
        hand = self.deck.draw(52)
        print(f"hand {len(hand)} :", hand)

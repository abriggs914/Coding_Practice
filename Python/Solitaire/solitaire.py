from utility import *
from random import shuffle

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
            self._value == other._value
            , self._suit == other._suit
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
        return "{} of {}".format(self._value, self._suit["name"])

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
        print("self.cards:", self.cards)

    def shuffle(self):
        shuffle(self.cards)

    def use_card(self, card, discard=True):
        assert card in self.cards
        print(f"FROM<{id(self.cards)}>")
        print(f"REMOVING CARD <{card}>")
        print(f"CARDS BEF <{len(self.cards)}>: <{self.cards}>")
        if discard:
            self.discarded.append(card)
        self.cards.remove(card)
        print(f"CARDS AFT <{len(self.cards)}>: <{self.cards}>")

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


class SolitaireGameOverError(Exception):
    pass

class Solitaire:
    def __init__(
            self,
            n_resets=3,
            n_cols=7
    ):
        print("hey")
        self.deck = Deck("name")
        # hand = self.deck.draw(52)
        # print(f"hand {len(hand)} :", hand)

        self.n_resets = n_resets
        self.n_resets_used = 0
        self.n_cols = n_cols

        self.discard_pile = []

        self.foundations = {
            Suit.HEARTS["name"]: [],
            Suit.SPADES["name"]: [],
            Suit.DIAMONDS["name"]: [],
            Suit.CLUBS["name"]: []
        }

        self.columns = [[] for i in range(self.n_cols)]

    def shuffle(self):
        self.deck.shuffle()

    def init_new_game(self):
        self.deck.reset()
        self.shuffle()
        self.foundations = {
            Suit.HEARTS["name"]: [],
            Suit.SPADES["name"]: [],
            Suit.DIAMONDS["name"]: [],
            Suit.CLUBS["name"]: []
        }
        print("[self.draw_card(i) for i in range(len(self.columns))]", [i for i in range(len(self.columns))])
        self.columns = []
        for i in range(self.n_cols):
            cards = self.draw_card(i + 1, False)
            self.columns.append(cards)
            cards = []

        for col in self.columns:
            col[-1].show = True
        print(f"self.cols:", "\n" + "\n".join([str(col) for col in self.columns]))

    def draw_card(self, qty=1, remove=True, random_draw=False):
        if len(self.deck) == 0:
            raise ValueError("No cards left to draw")
        print(f"cards left <{len(self.deck)}> pulling <{qty}> self.deck.cards[-1:]: <{self.deck.cards[-qty:]}>")
        if random_draw:
            cards = self.deck.draw(qty, remove)
            self.discard_pile += cards
        else:
            cards = self.deck.cards[-qty:]
            print(f"MATC<{id(self.deck.cards)}>")
            for card in cards:
                self.deck.use_card(card, remove)
            # cards = ()
            # for i in range(qty):
            #     card = self.deck.get_cards()[-1]
            #     if remove:
            #         self.deck.use_card(card)
            #     cards = (*cards, card)
            #     print(f"using c: <{card}>")
        return cards

    def can_stack_col(self, col_idx, card):
        assert isinstance(card, Card)
        col = self.columns[col_idx]
        print(f"col_idx: {col_idx}, card: {card}, col: {col}")
        if len(col) == 0 and card.value == "K":
            return True
        top_card = col[-1]
        if card.value == Card.VALID_FACE[Card.VALID_FACE.index(top_card.value) - 1]:
            if card.is_red() and top_card.is_black():
                return True
            elif card.is_black() and top_card.is_red():
                return True
        return False

    def can_stack_foundation(self, foundation_suit, card):
        assert isinstance(card, Card)
        assert foundation_suit in Card.VALID_SUIT
        foundation = self.foundations[foundation_suit["name"]]
        if len(foundation) == 0:
            if card.value == "A":
                return True
            return False
        top_card = foundation[-1]
        if card.suit == foundation_suit:
            if card.value == Card.VALID_FACE[Card.VALID_FACE.index(top_card.value) + 1]:
                return True
        return False

    def can_draw(self):
        return len(self.deck) > 0

    def can_reset(self):
        return self.n_resets > self.n_resets_used

    def stack(self, from_col, to_col, card):
        assert self.can_stack_col(to_col, card)
        print(f"self.discard_pile: {self.discard_pile}")
        print(f"self.deck.discarded: {self.deck.discarded}")
        print(f"self.deck: {self.deck}")
        if from_col in range(self.n_cols):
            self.columns[to_col].append(card)
            self.columns[from_col].remove(card)
        elif from_col == "discard_pile":
            self.columns[to_col].append(card)
            self.deck.discarded.remove(card)
        # card.show = True
        print(f"self.cols: {self.columns}")

    def reset(self, do_shuffle=True):
        self.n_resets_used += 1
        if self.n_resets_used > self.n_resets:
            raise SolitaireGameOverError("You are out of resets.")
        self.deck.cards = self.deck.discarded
        for card in self.deck.cards:
            card.show = False
        self.deck.discarded = []
        if do_shuffle:
            self.shuffle()

    def get_top_card(self, col_idx):
        assert col_idx in range(self.n_cols)
        col = self.columns[col_idx]
        if col:
            return col[-1]
        return None

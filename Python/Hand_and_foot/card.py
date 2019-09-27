
import random

card_suits = ["hearts", "spades", "diamonds", "clubs"]
face_values = ["A", "1", "2", "3", "4", "5", "6", "7", "8", "9", "J", "Q", "K"]

class Card:

    def __init__(self, suit=None, val=None):
        if not suit or not val:
            suit, val = self.gen_card()
            self.suit = suit
            self.val = val

        self.suit = suit
        self.val = val
        self.card_id = self.gen_card_id()
        self.num_val = self.gen_num_val()

    def __repr__(self):
        repr = self.get_val() + " of " + self.get_suit() + "\t[ " + str(self.get_num_val()) + " ]"
        return repr

    def get_suit(self):
        return self.suit

    def get_val(self):
        return self.val

    def get_num_val(self):
        return self.num_val

    def get_card_id(self):
        return self.card_id

    def gen_card(self):
        id = random.randint(0,12)
        val = random.randint(0,3)
        return card_suits[val], face_values[id]

    def gen_card_id(self):
        suit = self.get_suit()
        val = self.get_val()
        id = 0
        for suitVal in card_suits:
            if suit == suitVal:
                break
            id += 13
        for face_value in face_values:
            if val == face_value:
                break
            id += 1
        return id

    def gen_num_val(self):
        id = self.get_card_id()
        # ace
        val = 0
        res = id % 13
        if res == 0:
            val = 20
        elif res > 0:
            if res > 6:
                val = 10
            else:
                val = 5
        if val == 10 or val == 20:
            return val
        if res == 2:
            val = 20
        if res == 3:
            if id == 16 or id == 42:
                val = -5
            elif id == 3 or id == 29:
                val = -500
        return val
            # if (id % 12) == 0:
            #     return 10
            # elif id % 11:
            #     return 10
            # elif id % 10:
            #     return 10
            # elif id % 9:
            #     return 10
            # elif id %

# c = Card()
# print(c)
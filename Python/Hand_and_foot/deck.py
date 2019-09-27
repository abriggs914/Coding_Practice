import card
import random

class Deck():

    def __init__(self):
        self.deckOfCards = self.gen_deck()

    def __repr__(self):
        res = ""
        for cardInDeck in self.get_deck():
            res += str(cardInDeck) + "\n"
        return res

    def get_deck(self):
        return self.deckOfCards

    def get_top_n_cards(self, n):
        return self.get_deck()[:n + 1]

    def shuffle_deck(self):
        cards = self.get_deck()
        # choices = [i for i in range(len(cards))]
        shuffled_deck = []
        indexs_used = []
        while len(shuffled_deck) != 52:
            idx = random.randint(0, 51)
            if idx not in indexs_used:
                # deck_index_selected = choices[choices.index[idx]]
                selected_card = cards[idx]
                shuffled_deck.append(selected_card)
                indexs_used.append(idx)
                # choices = choices[:choices.index(idx)] + choices[choices.index(idx + 1):]
        self.deckOfCards = shuffled_deck
        return self.get_deck()

    def gen_deck(self):
        deck_of_cards = []
        for suit in card.card_suits:
            for val in card.face_values:
                deck_of_cards.append(card.Card(suit, val))
        return deck_of_cards

# d = deck()
# print(d)
# print(d.shuffle_deck())
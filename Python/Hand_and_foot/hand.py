import deck
import card
class Hand:

    def __init__(self, hand_size, originating_deck):
        self.deck_taken_from = originating_deck.get_deck()
        self.hand_size = hand_size
        self.hand_of_cards = self.gen_hand()

    def __repr__(self):
        res = ""
        hand_of_cards = self.get_hand()
        for i in range(self.get_hand_size()):
            res += str(i) + ":\t" + str(hand_of_cards[i]) + "\n"
        return res

    def get_card_at_idx_data(self, idx):
        curr_hand = self.get_hand()
        # print(curr_hand)
        l = len(curr_hand)
        # print(l)
        # print(type(curr_hand))
        # raise ValueError("STOP HERE")
        if type(idx) == card.Card:
            return idx.get_num_val()
        if -1 < idx < l:
            return curr_hand[idx].get_num_val()
        else:
            raise ValueError("INCORRECT VALUED INDEX PASSED IN:\t" + str(idx))

    def gen_hand(self):
        deck_of_cards = self.get_this_deck()
        return deck_of_cards[:(self.get_hand_size() + 1)]

    def get_this_deck(self):
        return self.deck_taken_from

    def get_hand_size(self):
        return self.hand_size

    def get_hand(self):
        return self.hand_of_cards

    def sort_hand_by_face_value(self):
        curr_hand = self.get_hand()
        sorted_hand = []
        # sorted_hand = sorted(curr_hand, )
        for card in curr_hand:
            sorted_hand.append(card)
            sorted_hand = self.insertion_sort(sorted_hand)
        self.hand_of_cards = sorted_hand

    def insertion_sort(self, lst):
        res = []
        for i in range(len(lst)):
            num = self.get_card_at_idx_data(lst[i])
            c = 0
            for j in range(len(res)):
                if num > self.get_card_at_idx_data(res[j]):
                    c += 1
            res = res[:c] + [lst[i]] + res[c:]
        return res

    # try:
    #     nums = input()
    # except:
    #     nums = ""
    # nums = list(map(int, nums.split()))

deck_of_cards = deck.Deck()
deck_of_cards.shuffle_deck()
h = Hand(10, deck_of_cards)
print(h)
print("\n\n")
h.sort_hand_by_face_value()
print(h)
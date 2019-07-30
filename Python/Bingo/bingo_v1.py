import random

class Card:
    
    def __init__(self):
        self.card_id = self.gen_card_id()
        self.board = self.populate_card()
        self.called_status = self.init_card(self.board)
        
    def __repr__(self):
        show_call_status = True
        res = ''
        border = ''.join(['_' for i in range(26)])
        cols = ['O', 'G', 'N', 'I', 'B']
        top_border = border
        top_border += '\n|  '
        for i in range(22):
            if i % 5 == 0:
                top_border += cols.pop()# + '  '
            else:
                top_border += ' '
        top_border += '|'
        res += top_border + '\n|' + border[1:-1] + '|\n'
        # print(top_border)
        print(self.board)
        for row in self.board:
            if show_call_status:
                new_row = []
                for num in row:
                    if self.called_status[num]:
                        new_row.append('__')
                    else:
                        new_row.append(num)
                row = new_row
            temp = [' ' + x if len(x) < 2 else x for x in list(map(str, row))]
            row = '| ' + ' | '.join(temp) + ' |\n'
            res += row
        res += '|' + border[1:-1] + '|'
        return res
        
    def init_card(self, card):
        res = {}
        for i in range(len(card)):
            for j in range(len(card[i])):
                res[card[i][j]] = False
        res[card[2][2]] = True
        return res
        
    def gen_card_id(self):
        card_number = 1
        yield card_number
        card_number += 1
        
    def rotate(self, board):
        order = []
        # for item in input().split(" "):
            # order.append(int(item))
        m,n = 5, 5
        matrix = board
        # for i in range(m):
            # temp = input().split(" ")
            # matrix.append(temp)
        new_matrix = []
        for i in range(n):
            temp = []
            for j in range(m):
                temp.append(matrix[(m-1)-j][i])
            temp.reverse()
            new_matrix.append(temp)
        # for item in new_matrix:
            # print(" ".join(item))
        return new_matrix
    
    def populate_card(self):
        board = []
        for i in range(5):
            bounds = list(range(((i * 15) + 1), ((i * 15) + 16)))
            row = []
            # print('BOUNDS:\t\t' + str(bounds))
            for j in range(5):
                # print('BOUNDS:\t' + str(bounds))
                choice = random.choice(bounds)
                row.append(choice)
                del bounds[bounds.index(choice)]
            board.append(row)
        # print(board)
        rotated_board = self.rotate(board)
        rotated_board[2][2] = '__'
        return rotated_board
        
class Bingo:
    
    def __init__(self, cards_in_play, game_type):
        self.called_numbers = []
        self.playing_cards = cards_in_play
        self.game_type = check_game_type(game_type)
        
    def check_game_type(self, type_in):
        available_games = {'regular' : check_regular_bingo(),
            'postage_stamp': check_postage_stamp_bingo(),
            'four_corners': check_four_corners_bingo(),
            'letter_v': check_letter_v_bingo(),
            'small_x': check_small_x_bingo(),
            'large_x':check_large_x_bingo(),
            'small_picture_frame': check_small_picture_frame_bingo(),
            'large_picture_frame': check_large_picture_frame_bingo(),
            'five_in_corner': check_five_in_corner_bingo(),
            'two_lines': check_two_lines_bingo(),
            'sputnik': check_sputnik_bingo()}
    
    def call_number(self):
        if len(self.called_numbers) == 75:
            raise ValueError('NO MORE NUMBERS LEFT TO BE CALLED')
        num = random.randint(1, 75)
        while num in self.called_numbers:
            num = random.randint(1, 75)
        self.mark_cards(num)
        self.called_numbers.append(num)
        
    def mark_cards(self, num):
        for card in self.playing_cards:
            if num in card.called_status.keys():
                card.called_status[num] = True


num_cards = 5
list_of_cards = [Card() for _ in range(num_cards)]

print('CARDS AFTER CREATION')
for card in list_of_cards:
    print(card)

print('BINGO GAME START')    
bingo = Bingo(list_of_cards)
for i in range(75):
    bingo.call_number()
called_nums = list(set(bingo.called_numbers))
called_nums.sort()
print('CALLED NUMBERS:\t' + str(called_nums))
for card in list_of_cards:
    print(card)

# for i in range(3):
    # print(populate_card())
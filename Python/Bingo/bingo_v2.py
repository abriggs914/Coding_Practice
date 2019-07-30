import random

class Card:
    
    def __init__(self, id_in):
        # id_gen = self.gen_card_id()
        self.card_id = id_in # next(id_gen)
        self.board = self.populate_card()
        self.called_status = self.init_card(self.board)
        
    def __repr__(self):
        show_call_status = True
        res = ''
        border = ''.join(['_' for i in range(26)])
        cols = ['O', 'G', 'N', 'I', 'B']
        top_border = '\tCARD #' + str(self.card_id) + '\n' + border
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
        while True:
            yield card_number
            # card_number += 1
        
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
        self.game_type = self.check_game_type(game_type)
        self.bingo_found = False
        self.switch = self.switch_gen()
        
    def switch_gen(self):
        val = True
        while True:
            yield val
            val = not val
        
    def check_game_type(self, type_in):
        available_games = {'regular' : lambda x,y : self.check_regular_bingo(x,y)
            # 'postage_stamp': lambda x,y : self.check_postage_stamp_bingo(x,y),
            # 'four_corners': lambda x,y : self.check_four_corners_bingo(x,y),
            # 'letter_v': lambda x,y : self.check_letter_v_bingo(x,y),
            # 'small_x': lambda x,y : self.check_small_x_bingo(x,y),
            # 'large_x': lambda x,y : self.check_large_x_bingo(x,y),
            # 'small_picture_frame': lambda x,y : self.check_small_picture_frame_bingo(x,y),
            # 'large_picture_frame': lambda x,y : self.check_large_picture_frame_bingo(x,y),
            # 'five_in_corner': lambda x,y : self.check_five_in_corner_bingo(x,y),
            # 'two_lines': lambda x,y : self.check_two_lines_bingo(x,y),
            # 'sputnik': lambda x,y : self.check_sputnik_bingo(x,y)
        }
        if type_in == 'anyway':
            return available_games
        game_types = {}
        for game_type in type_in:
            if game_type in list(available_games.keys()):
                game_types[game_type] = available_games[game_type]
        if len(game_types) == 0:
            return {'regular': available_games['regular']}
        else:
            return game_types
    
    def call_number(self):
        if not self.bingo_found:
            if len(self.called_numbers) == 75:
                raise ValueError('NO MORE NUMBERS LEFT TO BE CALLED')
            num = random.randint(1, 75)
            while num in self.called_numbers:
                num = random.randint(1, 75)
            self.mark_cards(num)
            self.called_numbers.append(num)
            self.bingo_found = self.check_possible_bingo()
        else:
            print('\n\tBINGO\n')
        
    def check_possible_bingo(self):
        bingo = False
        winning_cards = []
        for card in self.playing_cards:
            for game_type, check_bingo_func in self.game_type.items():
                bingo = check_bingo_func(card, card.board)
                # print('BINGO FOUND')
                if bingo:
                    winning_cards.append(card)
                    break
            bingo = False
        winners = len(winning_cards) > 0
        if winners:
            print('\n\tWINNING CARDS\n')
            for winning_card in winning_cards:
                print(winning_card.board)
        return winners
                
        
    def mark_cards(self, num):
        for card in self.playing_cards:
            if num in card.called_status.keys():
                card.called_status[num] = True
                
    def check_regular_bingo(self, card_obj, card):
        for i in range(len(card)):
            if '__' in card[i]:
                idx = card[i].index('__')
                if idx == 0:
                    row = list(set(card[i]))
                    if len(row) == 1:
                        # horizontal bingo
                        return True
        #need to only do once
        if next(self.switch):
            rotated_card = card_obj.rotate(card)
            self.check_regular_bingo(card_obj, rotated_card)
        else:
            return False
                # for j in range(len(card[i])):
                    # while j < 5 and card[i][j + 1] == '__':
        


num_cards = 5
list_of_cards = [Card(x) for x in range(1, num_cards + 1)]

print('CARDS AFTER CREATION')
for card in list_of_cards:
    print(card)

print('BINGO GAME START')    
bingo = Bingo(list_of_cards, ['regular'])
for i in range(75):
    bingo.call_number()
called_nums = list(set(bingo.called_numbers))
called_nums.sort()
print('CALLED NUMBERS:\t' + str(called_nums))
for card in list_of_cards:
    print(card)

# for i in range(3):
    # print(populate_card())
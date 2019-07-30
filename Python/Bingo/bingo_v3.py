import random
from functools import reduce
import math

class Card:
    
    def __init__(self, id_in):
        # id_gen = self.gen_card_id()
        self.card_id = id_in # next(id_gen)
        self.board = self.populate_card()
        self.called_status = self.init_card(self.board)
        self.marked_order = []
        self.win_type = None
        
    def __repr__(self):
        show_call_status = True
        res = '\n'
        border = ''.join(['_' for i in range(26)])
        cols = ['O', 'G', 'N', 'I', 'B']
        top_border = '\tCARD #' + str(self.card_id)
        if self.win_type:
            top_border += '\nWIN RESULT:\t' + str(self.win_type)
        top_border += '\n' + 'CALL ORDER:\t' + str(self.marked_order) + '\n' + border
        top_border += '\n|  '
        for i in range(22):
            if i % 5 == 0:
                top_border += cols.pop()# + '  '
            else:
                top_border += ' '
        top_border += '|'
        res += top_border + '\n|' + border[1:-1] + '|\n'
        # print(top_border)
        # print(self.board)
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
        
    def list_card_nums(self):
        card = self.board
        horizontal = reduce(lambda x, y : x + y, card)
        vert_rotation = self.rotate(card)
        vertical = reduce(lambda x, y : x + y, vert_rotation)
        return (horizontal, vertical)
        
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
        available_games = {'regular' : lambda x,y : self.check_regular_bingo(x,y),
            'postage_stamp': lambda x,y : self.check_postage_stamp_bingo(x,y),
            'four_corners': lambda x,y : self.check_four_corners_bingo(x,y),
            'letter_v': lambda x,y : self.check_letter_v_bingo(x,y),
            'small_x': lambda x,y : self.check_small_x_bingo(x,y),
            'large_x': lambda x,y : self.check_large_x_bingo(x,y),
            'small_picture_frame': lambda x,y : self.check_small_picture_frame_bingo(x,y)
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
            cols = {0:'B',1:'I',2:'N',3:'G',4:'O'}
            call = '\t' + cols[(num - 1) // 15] + ' ' + str(num)
            print(call)
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
                if bingo:
                    print(game_type.upper() + ' BINGO FOUND')
                    print('WINNER ID:\t' + str(card.card_id))
                    card.win_type = game_type.title()
                    winning_cards.append(card)
                    break
            bingo = False
        winners = len(winning_cards) > 0
        if winners:
            print('\n\tNUM WINNERS:\t' + str(len(winning_cards)) + '\n\tWINNING CARDS\n')
            for winning_card in winning_cards:
                print(winning_card)
        return winners
                
        
    def mark_cards(self, num):
        for card in self.playing_cards:
            if num in card.called_status.keys():
                h, v = card.list_card_nums()
                num_idx = h.index(num)
                row_idx, col_idx = divmod(num_idx, 5)
                # row_idx = math.floor(num / 15)
                # col_idx = card.board[row_idx].index(num)
                # print('row_idx:\t'+str(row_idx)+', col_idx:\t'+str(col_idx))
                # print('NUM:\t' + str(num) + ', ROW_IDX:\t' + str(card.board[row_idx]) + ', NUM_IDX:\t' + str(card.board[row_idx][col_idx]))
                card.board[row_idx][col_idx] = '__'
                card.called_status[num] = True
                card.marked_order.append(num)
            # print(card)
                
    def check_regular_bingo(self, card_obj, card):
        line_bingo = '__ __ __ __ __'
        horizontal, vertical = card_obj.list_card_nums()
        # print('\tFLATTENED LISTS:\n' + str(horizontal) + '\n' + str(vertical))
        h_idx = horizontal.index('__')
        v_idx = vertical.index('__')
        if h_idx == 12 and v_idx == 12:
            return False
        adj_horizontal = [str(num) if len(str(num)) == 2 else '0' + str(num) for num in horizontal]
        adj_vertical = [str(num) if len(str(num)) == 2 else '0' + str(num) for num in vertical]
        h_lst = ' '.join(adj_horizontal)
        v_lst = ' '.join(adj_vertical)
        if line_bingo in h_lst:
            idx = h_lst.find(line_bingo)
            # print('FOUND h_lst IDX:\t' + str(idx) + '\n' + str(h_lst))
            if idx % 15 == 0:
                return True
        if line_bingo in v_lst:
            idx = v_lst.find(line_bingo)
            # print('FOUND v_lst IDX:\t' + str(idx) + '\n' + str(v_lst))
            if idx % 15 == 0:
                return True
        marked_indicies = [i for i in range(25) if horizontal[i] == '__']
        # checking \ diagonal
        if 0 in marked_indicies and 24 in marked_indicies:
            if 6 in marked_indicies and 18 in marked_indicies:
                return True
        # checking / diagonal
        if 4 in marked_indicies and 20 in marked_indicies:
            if 8 in marked_indicies and 16 in marked_indicies:
                return True
        return False
        
    def check_postage_stamp_bingo(self, card_obj, card):
        line_bingo = '__ __'
        horizontal, vertical = card_obj.list_card_nums()
        h_lst = ' '.join(list(map(str, horizontal)))
        v_lst = ' '.join(list(map(str, vertical)))
        # print('horizontal:\t' + str(horizontal))
        marked = '__'
        if marked in horizontal:
            idx = horizontal.index(marked)
            # locate top left of postage stamp
            if (idx + 1) % 5 > 0 and horizontal[idx + 1] == marked:
                # if top left idx is above last row
                if idx < 20:
                    # check bottom indexes of postage stamp
                    if horizontal[idx + 5] == marked and horizontal[idx + 6] == marked:
                        # ensure free space is not used in postage stamp
                        if (idx != 12) and ((idx + 1) != 12) and ((idx + 5) != 12) and ((idx + 6) != 12):
                            return True
        return False
        
    def check_four_corners_bingo(self, card_obj, card):
        marked = '__'
        if card[0][0] == marked:
            if card[0][4] == marked:
                if card[4][0] == marked:
                    if card[4][4] == marked:
                        return True
        return False
        
    def check_letter_v_bingo(self, card_obj, card):
        marked = '__'
        # checking v
        if card[0][0] == marked and card[0][4] == marked:
            if card[1][1] == marked and card[1][3] == marked:
                return True
        # checking <
        elif card[0][4] == marked and card[4][4] == marked:
            if card[1][3] == marked and card[3][3] == marked:
                return True
        #  checking ^
        elif card[4][0] == marked and card[4][4] == marked:
            if card[3][1] == marked and card[3][3] == marked:
                return True
        # checking >
        elif card[0][0] == marked and card[4][0] == marked:
            if card[1][1] == marked and card[3][1] == marked:
                return True
        return False
        
    def check_small_x_bingo(self, card_obj, card):
        marked = '__'
        if card[1][1] == marked:
            if card[1][3] == marked:
                if card[3][1] == marked:
                    if card[3][3] == marked:
                        return True
        return False
        
    def check_large_x_bingo(self, card_obj, card):
        if self.check_small_x_bingo(card_obj, card):
            if self.check_four_corners_bingo(card_obj, card):
                return True
        return False
        
    def check_small_picture_frame_bingo(self, card_obj, card):
        marked = '__'
        if self.check_small_x_bingo(card_obj, card):
            if card[1][2] == marked:
                if card[2][1] == marked:
                    if card[2][3] == marked:
                        if card[3][2] == marked:
                            return True
        return False
            
        
#####################################################################################

# START OF GAME

num_cards = 5000
list_of_cards = [Card(x) for x in range(1, num_cards + 1)]

print('CARDS AFTER CREATION')
# for card in list_of_cards:
    # print(card)

print('BINGO GAME START')    
bingo = Bingo(list_of_cards,    ['small_picture_frame',
                                'small_x',
                                'large_x',
                                'four_corners',
                                'regular',
                                'letter_v',
                                'postage_stamp'
                                ])
for i in range(75):
    if not bingo.bingo_found:
        bingo.call_number()
called_nums = bingo.called_numbers
print('CALLED NUMBERS ORDERED:\t' + str(called_nums))
called_nums_sort = sorted(called_nums.copy())
print('CALLED NUMBERS SORTED:\t' + str(called_nums_sort) + '\n\n\n\tREST OF CARDS\n')
for card in list_of_cards:
    print(card)

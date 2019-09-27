import random as rand
import time

"""
 Sept. 22 /19
  Program  to simulate Hexapawn game.
"""

class MatchBox:

    def __init__(self, id, black_squares_idxs, white_squares_idxs, moves):
        self.id = id

        self.blackSquares = black_squares_idxs
        self.whiteSquares = white_squares_idxs
        self.moves = moves
        self.board = self.mark_board()

    def __repr__(self):
        res = "\tId " + str(self.id) + "\n\t_______\n"
        board = self.board
        for i in range(0, 9, 3):
            res += "\t|" + str(board[i]) + "|"
            res += str(board[i + 1]) + "|"
            res += str(board[i + 2]) + "|\n"

        res += "\n\tboard:\t" + str(board) + "\n"
        res += "\tmoves:\t" + str(self.moves) + "\n"
        return res

    def mark_board(self):
        board = [" " for i in range(9)]
        for square in self.blackSquares:
            board[square] = "B"
        for square in self.whiteSquares:
            board[square] = "W"
        return board

    def punish_move(self, move_index):
        moves = self.moves
        print("punishing move:\t" + str(moves[move_index]))
        if len(moves) > 2:
            moves = moves[:move_index] + moves[(move_index + 1):]
            print("new_moves:\t" + str(moves))
            self.moves = moves

    def reward_move(self, move_index):
        moves = self.moves
        print("rewarding move:\t" + str(moves[move_index]))
        if len(moves) < 9:
            moves.append(moves[move_index])
            print("new_moves:\t" + str(moves))
            self.moves = moves

    def select_move(self):
        possibilities = []
        for square in self.blackSquares:
            possible_moves = get_possible_moves(None, square)
            possibilities.append(possible_moves)
        print("\tpossibilities:\n" + str(possibilities))
        print("self.moves:\t" + str(self.moves))
        # num_moves = len(self.moves)
        # rnd_n = rand.randint(0, len(possibilities) - 1)
        # chosen_move = self.moves[rnd_n]
        rnd_n = -1
        new_number = True
        while new_number:
            rnd_n = rand.randint(0, len(self.blackSquares) - 1)
            print("rnd_n:\t" + str(rnd_n))
            if len(possibilities[rnd_n]) > 0:
                for move in self.moves:
                    if game_board.board[move[1]] == "B" and move[2] in possibilities[rnd_n]:
                        if game_board.board[move[2]] == " " or (move[1] % 3 != move[2] % 3):
                            new_number = False
                            break
            # available = possibilities[rnd_n]
            # for possibility in possibilities:
            #     for move_square in possibility:
            #         if move_square == self.moves[rnd_n][2]:
            #             if len(possibilities[rnd_n]) > 0:
            #                 if game_board.board[self.moves[rnd_n][2]] == " " or \
            #                         (game_board.board[self.moves[rnd_n][2]] != game_board.board[self.moves[rnd_n][1]]
            #                          and (self.moves[rnd_n][2] % 3 != self.moves[rnd_n][1] % 3)):
            #                     new_number = False
            #                     break
            #     if not new_number:
            #         break
        chosen_move = self.moves[rnd_n]
        return [self.id] + list(chosen_move)

    def adjust_moves_for_symmetry(self):
        moves = self.moves
        new_moves = []
        for move in moves:
            from_idx = move[1]
            if from_idx % 3 == 0:
                from_idx += 2
            elif from_idx % 3 == 2:
                from_idx -= 2

            to_idx = move[2]
            if to_idx % 3 == 0:
                to_idx += 2
            elif to_idx % 3 == 2:
                to_idx -= 2
            new_move = (move[0], from_idx, to_idx)
            new_moves.append(new_move)
        print("ADJ_moves:\t" + str(new_moves))
        # print("new_moves:\t" + str(new_moves))
        self.moves = new_moves



move_boards = {"1": [2,
                     [0, 1, 2],
                     [3, 7, 8],
                     [("G", 1, 3),
                      ("B", 1, 4),
                      ("P", 2, 5)]],
               "2": [2,
                     [0, 1, 2],
                     [4, 6, 8],
                     [("G", 0, 3),
                      ("B", 0, 4)]],
               "3": [4,
                     [0, 2, 3],
                     [4, 8],
                     [("G", 0, 4),
                      ("B", 2, 4),
                      ("O", 3, 6),
                      ("P", 2, 5)]],
               "4": [4,
                     [1, 2, 4],
                     [3, 8],
                     [("G", 2, 5),
                      ("P", 1, 3),
                      ("B", 4, 7),
                      ("O", 4, 8)]],
               "5": [4,
                     [0, 2],
                     [3, 4, 7],
                     [("G", 2, 4),
                      ("B", 0, 4),
                      ("P", 2, 5)]],
               "6": [4,
                     [0, 1],
                     [3, 5, 8],
                     [("G", 1, 4),
                      ("B", 1, 5),
                      ("P", 1, 3)]],
               "7": [4,
                     [1, 2, 4],
                     [5, 6],
                     [("G", 1, 5),
                      ("B", 4, 6),
                      ("P", 4, 7)]],
               "8": [4,
                     [1, 2, 3],
                     [4, 5, 6],
                     [("G", 2, 4),
                      ("P", 1, 5)]],
               "9": [4,
                     [0, 2, 3],
                     [5, 7],
                     [("G", 3, 6),
                      ("B", 3, 7)]],
               "10": [4,
                      [0, 1, 5],
                      [3, 4, 8],
                      [("B", 1, 3),
                       ("P", 0, 4)]],
               "11": [4,
                      [1, 2],
                      [4, 8],
                      [("G", 2, 5),
                       ("P", 2, 4)]],
               "12": [4,
                      [1, 2],
                      [4, 6],
                      [("O", 2, 4),
                       ("P", 2, 5)]],
               "13": [4,
                      [0, 2],
                      [3, 8],
                      [("O", 2, 5)]],
               "14": [6,
                      [2, 3, 4],
                      [5],
                      [("O", 4, 7),
                       ("P", 3, 6)]],
               "15": [6,
                      [0],
                      [3, 4, 5],
                      [("G", 0, 4)]],
               "16": [6,
                      [1, 3],
                      [4, 5],
                      [("O", 1, 5),
                       ("P", 3, 6)]],
               "17": [6,
                      [1, 5],
                      [3, 4],
                      [("O", 1, 3),
                       ("P", 5, 8)]],
               "18": [6,
                      [0, 3, 4],
                      [5],
                      [("B", 3, 6),
                       ("P", 4, 7)]],
               "19": [6,
                      [2, 4, 5],
                      [3],
                      [("O", 4, 7),
                       ("G", 5, 8)]],
               "20": [6,
                      [2, 3],
                      [4],
                      [("O", 2, 4),
                       ("P", 3, 6),
                       ("G", 2, 5)]],
               "21": [6,
                      [1, 4],
                      [3],
                      [("G", 1, 3),
                       ("P", 4, 7)]],
               "22": [6,
                      [1, 4],
                      [5],
                      [("B", 4, 7),
                       ("P", 1, 5)]],
               "23": [6,
                      [0, 3],
                      [4],
                      [("O", 3, 6),
                       ("P", 0, 4)]],
               "24": [6,
                      [2, 5],
                      [4],
                      [("G", 2, 4),
                       ("B", 5, 8)]],
               }


MatchBoxes = []
idN = 1
for matchbox in move_boards:
    data = move_boards[matchbox]
    blackSquares = data[1]
    whiteSquares = data[2]
    moves = data[3]
    MatchBoxes.append(MatchBox(int(matchbox), blackSquares, whiteSquares, moves))
    idN += 1


def print_board(board):
    res = "\tId " + str(board.id) + "\n"
    board = board.board
    for i in range(0, 9, 3):
        res += str(board[i]) + "|"
        res += str(board[i + 1]) + "|"
        res += str(board[i + 2]) + "\n"
    res += "\n"
    return res


def print_match_boxes():
    for matchbox in MatchBoxes:
        print(matchbox)


def get_matching_game_board():
    # print(str(game_board.board) + "\n")
    for matchbox in MatchBoxes:
        # print(matchbox.board)
        if matchbox.board == game_board.board:
            return matchbox
    symm_board = get_symm_board()
    # print("board:" + str(game_board.board))
    # print("symm:\t" + str(symm_board))
    for matchbox in MatchBoxes:
        # print(matchbox.board)
        if matchbox.board == symm_board:
            # print("ADJUSTING")
            matchbox.adjust_moves_for_symmetry()
            return matchbox
    return None

def get_symm_board():
    res = []
    for i in range(0,9,3):
        res_l = []
        res_l.append(game_board.board[i])
        res_l.append(game_board.board[i + 1])
        res_l.append(game_board.board[i + 2])
        res.append(res_l)
    flat_res = []
    for lst in res:
        lst.reverse()
        for val in lst:
            flat_res.append(val)
    return flat_res

def board_move(move):
    print("\nMOVE:\t" + str(move))
    board = game_board.board
    moving_piece = move[0]
    if moving_piece == "W":
        piece_index_list = game_board.whiteSquares
        other_team_list = game_board.blackSquares
    else:
        print("not w")
        piece_index_list = game_board.blackSquares
        other_team_list = game_board.whiteSquares
    print("piece_index_list:\t" + str(piece_index_list))
    print("other_team_list:\t" + str(other_team_list))
    a = move[1]
    b = move[2]
    t = board[a]
    # take piece condition
    if board[b] != moving_piece and board[b] != " ":
        other_team_list.remove(b)
        board[a] = " "
    piece_index_list.remove(a)
    piece_index_list.append(b)
    board[a] = " "
    board[b] = t
    if moving_piece == "W":
        game_board.whiteSquares = piece_index_list
        game_board.blackSquares = other_team_list
    else:
        game_board.blackSquares = piece_index_list
        game_board.whiteSquares = other_team_list
    game_board.mark_board()
    game_board.board = board


def check_for_winner(turn_number):
    pw = "Player Wins"
    cpuw = "CPU Wins"
    if game_board.board.count("B") == 0:
        return pw + " you took all the computer\'s pawns."
    if game_board.board.count("W") == 0:
        return cpuw + " you lost all of your pawns."
    if "W" in game_board.board[:3]:
        return pw + " you made it all the way to the other side."
    if "B" in game_board.board[6:]:
        return cpuw + " the computer made it all the way to your side."
    if black_cant_move() and turn_number % 2 == 0:
        return pw + " the computer can\'t move on it\'s turn."
    if white_cant_move() and turn_number % 2 == 1:
        return cpuw + " you can\'t move on your turn."
    else:
        return False


def white_cant_move():
    for white_square in game_board.whiteSquares:
        if white_square > 2 and game_board.board[white_square - 3] == " ":
            return False
        if white_square > 2:
            if (white_square % 3) < 2 and game_board.board[white_square - 2] == "B":
                return False
            if (white_square % 3) > 0 and game_board.board[white_square - 4] == "B":
                return False
            if white_square % 3 == 1:
                if game_board.board[white_square - 4] == "B" or game_board.board[white_square - 2] == "B":
                    return False
    # print("WHITE CAN\'T MOVE")
    return True


def black_cant_move():
    for black_square in game_board.blackSquares:
        if black_square < 6 and game_board.board[black_square + 3] == " ":
            return False
        if black_square < 6:
            if (black_square % 3) < 2 and game_board.board[black_square + 4] == "W":
                return False
            if (black_square % 3) > 0 and game_board.board[black_square + 2] == "W":
                return False
            if black_square % 3 == 1:
                if game_board.board[black_square + 4] == "W" or game_board.board[black_square + 2] == "W":
                    return False
    # print("BLACK CAN\'T MOVE")
    return True


def player_turn():
    print(game_board)
    if not white_cant_move() or len(game_board.whiteSquares) == 0:
        print("options:\t" + str(game_board.whiteSquares))
        white_index = int(input("\tType the index of the white peg you want to move:\n"))
        while white_index not in game_board.whiteSquares:
            print("\n\tPlease enter a valid index (0 - 8).")
            print(game_board)
            print("options:\t" + str(game_board.whiteSquares))
            white_index = int(input("\tType the index of the white peg you want to move:\n"))

        possible_moves = get_possible_moves(white_index)
        print("\n")
        print(game_board)
        print("possible moves:\t" + str(possible_moves))
        move_to_index = int(input("\tType the index of the board that you want to move to\n" +
                                  "\tYou may only move to a space directly infront of you,\n" +
                                  "\tor you can move diagonally 1 space to take a black peg:\n"))
        if len(possible_moves) == 0:
            print("Sorry the white peg at index " + str(white_index) + ", does not have any valid moves.")
            return player_turn()
        while move_to_index in game_board.whiteSquares and move_to_index not in possible_moves:
            print("\n\tPlease enter a valid index (0 - 8).")
            print(game_board)
            print("possible moves:\t" + str(possible_moves))
            move_to_index = int(input("\tType the index of the board that you want to move to\n" +
                                      "\tYou may only move to a space directly infront of you,\n" +
                                      "\tor you can move diagonally 1 space to take a black peg:\n"))
        return ["W", white_index, move_to_index]
    return "player loses"


def get_possible_moves(w_idx, b_idx=None):
    space = " "
    b_square = "B"
    w_square = "W"
    moving_symbol = "W"  # by default
    moving_piece = w_idx  # default
    takeable_piece = b_square  # default
    board = game_board.board
    if w_idx is None and b_idx is not None:
        moving_symbol = "B"
        moving_piece = b_idx
        takeable_piece = w_square
    can_go_n = True if (moving_piece > 2 and board[moving_piece - 3] == space) else False
    can_go_ne = True if ((moving_piece > 2 and moving_piece % 3 < 2) and board[
        moving_piece - 2] == takeable_piece) else False
    can_go_se = True if ((moving_piece < 6 and moving_piece % 3 < 2) and board[
        moving_piece + 4] == takeable_piece) else False
    can_go_s = True if (moving_piece < 6 and board[moving_piece + 3] == space) else False
    can_go_sw = True if ((moving_piece < 6 and moving_piece % 3 > 0) and board[
        moving_piece + 2] == takeable_piece) else False
    can_go_nw = True if ((moving_piece > 2 and moving_piece % 3 > 0) and board[
        moving_piece - 4] == takeable_piece) else False

    # possibilities
    move_space = []
    if moving_symbol == "W":
        if can_go_nw:
            move_space.append(moving_piece - 4)
        if can_go_n:
            move_space.append(moving_piece - 3)
        if can_go_ne:
            move_space.append(moving_piece - 2)
    elif moving_symbol == "B":
        if can_go_sw:
            move_space.append(moving_piece + 2)
        if can_go_s:
            move_space.append(moving_piece + 3)
        if can_go_se:
            move_space.append(moving_piece + 4)
    return move_space


# print("\tv- MatchBoxes -v\n")
# print_match_boxes()
# print("\t^- MatchBoxes -^\n")


def gen_start_matchbox():
    id = -1
    black_squares_idxs = [i for i in range(3)]
    white_squares_idxs = [i for i in range(6, 9)]
    moves = {}  # player must go first so computer has no moves at the beginning
    start_board = MatchBox(id, black_squares_idxs, white_squares_idxs, moves)
    return start_board

def improve_matchboxes(move_sequence):
    winner = move_sequence[-1][1]
    print("winner:\t" + str(winner))
    untreated_moves = []
    cpu_moves = [i for i in move_sequence if move_sequence.index(i) % 2 == 0]
    for i in range(len(move_sequence)):
        move = move_sequence[i][1:]
        if i % 2 == 1:
            # cpu turn
            print("move:\t" + str(move))
            matchbox = MatchBoxes[move_sequence[i][0] - 1]
            moves = matchbox.moves
            print("moves:\t" + str(moves))
            for p_move in moves:
                if tuple(move) == p_move:
                    print("gotcha")
                    if winner != "W":
                        matchbox.reward_move(moves.index(tuple(move)))
                    else:
                        matchbox.punish_move(moves.index(tuple(move)))
                    break
                else:
                    print("check untreated")
                    untreated_moves.append(tuple(move))
    if untreated_moves:
        # try shifting
        for i in range(len(untreated_moves)):
            move = untreated_moves[i]
            # cpu turn
            print("untreated_move:\t" + str(move))
            matchbox = MatchBoxes[untreated_moves[i][1] - 1]
            matchbox.adjust_moves_for_symmetry()
            moves = matchbox.moves
            print("moves:\t" + str(moves))
            for p_move in moves:
                if move == p_move:
                    print("gotcha")
                    if winner != "W":
                        matchbox.reward_move(moves.index(move))
                    else:
                        matchbox.punish_move(moves.index(move))
                    break




desired_num_games = 35
game_tracker = 1
game_stats = []
num_player_wins = 0

while desired_num_games > 0:
    game_board = gen_start_matchbox()  # MatchBox object
    print("\n\n\tGAME # " + str(game_tracker) + "\n")
    move_sequence = []
    turn_number = 1

    # play
    print("Turn:\t" + str(turn_number))
    print("You go first:")
    player_first_turn = player_turn()
    board_move(player_first_turn)
    move_sequence.append([game_board.id] + player_first_turn)
    print(game_board)
    board_status = get_matching_game_board()
    print(board_status)
    winner_status = check_for_winner(turn_number)
    turn_number += 1
    while not winner_status:
        print("Turn:\t" + str(turn_number))
        board_status = get_matching_game_board()
        if board_status is None and turn_number % 2 == 1:
            # print("Turn:\t" + str(turn_number))
            # turn_number += 1
            player_turn_res = player_turn()
            if type(player_turn_res) is not str:
                board_move(player_turn_res)
                move_sequence.append([game_board.id] + player_turn_res)
                board_status = get_matching_game_board()
        elif turn_number % 2 == 0:
            # game_board.id = board_status.id if board_status is not None else -5
            game_board.id = board_status.id
            board_status = get_matching_game_board()
            move_selected = board_status.select_move()
            move_sequence.append(move_selected)
            # colour, a, b = move_selected
            print("move selected:\t" + str(move_selected))
            board_move(move_selected[1:])
        turn_number += 1
        winner_status = check_for_winner(turn_number)
        print("winner_status:\t" + str(winner_status))
        print(game_board)

    print("\n\nMOVE SEQUENCE:\n" + str(move_sequence))
    improve_matchboxes(move_sequence)
    desired_num_games -= 1
    game_tracker += 1
    if desired_num_games > 0:
        print("Ready to play again?")
        # print("\tv- MatchBoxes -v\n")
        # print_match_boxes()
        # print("\t^- MatchBoxes -^\n")
        time.sleep(2)
    if "Player" in winner_status[:9]:
        num_player_wins += 1
    game_stats.append([game_tracker, winner_status, move_sequence])

print("\tv- MatchBoxes -v\n")
print_match_boxes()
print("\t^- MatchBoxes -^\n")

for game in game_stats:
    game_number = game[0]
    winner_status = game[1]
    move_sequence = game[2]
    print("\n\tGame # " + str(game_number) + "\nWinner:\t" +
          str(winner_status) + "\nMove_Sequence:\t" +
          str(move_sequence))

print("num_player_wins:\t" + str(num_player_wins))
# import importlib
#
# puzzles_list = input('puzzles_list.py')
# importlib.import_module(puzzles_list)
#import get_list_of_puzzles
#import puzzles_list
from puzzle import puzzleify

from puzzles_list import list_of_puzzles
# def define_puzzles_list():
#     return puzzles_list.get_list_of_puzzles()


# list_of_puzzles = get_list_of_puzzles()



list_of_puzzles = puzzleify(list_of_puzzles)


def begin_scoring():
    print('Begin scoring')
    score = 0
    for i in list_of_puzzles.keys():
        if list_of_puzzles[i].solved:  # list_of_puzzles[i].puzzle_board == list_of_puzzles[i].solved_puzzle_board:
            score += 1
            print('puzzle is solved!',list_of_puzzles[i])
    print('currently',score,'out of',len(list_of_puzzles),'puzzles are solved.')


begin_scoring()
# end Puzzle_Board

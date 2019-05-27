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


# end Puzzle_Board

from battleship import *


def main():
    print("repl_main")
    battleship = Battleship(16, 7)
    print("lines:\n\t", battleship.lines(1))
    # print("lines:\n\t", battleship.lines(1, 1))
    # print("lines:\n\t", battleship.lines(0, 1))
    print("lines:\n\t", battleship.lines(filter_unique=1))

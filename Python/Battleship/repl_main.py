from battleship import *
from test_suite import *


def main():
    print("repl_main")
    battleship = Battleship(2, 2)
    print("lines:\n\t", battleship.lines(1))
    # print("lines:\n\t", battleship.lines(1, 1))
    # print("lines:\n\t", battleship.lines(0, 1))
    print("lines:\n\t", battleship.lines(filter_unique=1))

    TS1 = TestSuite("Battleship lines")
    TS1.set_func(lambda x, *args: x.lines(*args))
    TS1.add_test("Test1 - removing the hit space at (1, 1)", [[battleship, False, False, Battleship.SYM_HIT, False], [1,2,3,4,5]])
    TS1.execute()

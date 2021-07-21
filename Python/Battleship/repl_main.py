from battleship import *
from test_suite import *


def main():
    print("repl_main")
    battleship = Battleship(2, 2)
    print("lines:\n\t", battleship.lines(1))
    # print("lines:\n\t", battleship.lines(1, 1))
    # print("lines:\n\t", battleship.lines(0, 1))
    print("lines:\n\t", battleship.lines(filter_unique=1))

    TS_lines = TestSuite("Battleship lines")
    TS_lines.set_func(lambda x, *args: len(x.lines(*args)))
    TS_lines.add_test("Test1 - Removing the Nones (all spaces except (1, 1))", [[battleship, True, False, None, False], 4])
    TS_lines.add_test("Test2 - Removing the hit space at (1, 1)", [[battleship, False, False, Battleship.SYM_HIT, False], 9])
    TS_lines.add_test("Test3 - Unique lines", [[battleship, False, False, None, True], 4])
    TS_lines.add_test("Test4 - Removing non-Nones. Same as filter_symbols by \"Hits\"", [[battleship, False, True, None, True], 9])
    TS_lines.execute()

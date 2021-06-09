from utility import *
from test_suite import *

# test area and scratch pad

test_lists = [
    ([[1, 2], [3, 4]], [1, 2, 3, 4]),
    ([[[1], 2], [[3, 4]]], [1, 2, 3, 4]),
    ([1, 2, 3, 4], [1, 2, 3, 4]),
    ([[[[[[[[[[[1]], 2]], 3]], 4]]]]], [1, 2, 3, 4]),
    (None, [None]),
    ([], []),
    (0, [0]),
    (1, [1]),
    (dict(), [dict()]),
    (tuple(), [tuple()]),
    (list(), list()),
    (int(), [int()]),
    (float(), [float()]),
    (True, [True]),
    (False, [False]),
    (bool(), [bool()]),
    ({1: [1, 2]}, [{1: [1, 2]}]),
    (print, [print])
]


correct_answers = []
for i, vals in enumerate(test_lists[:30]):
    lst, ans = vals
    res = flatten(lst)
    right = ans == res
    correct_answers.append(right)
    print("\n\n\t\t{}\n\n\tIN:\n".format(i + 1) + str(lst))
    print("\tOUT:\n" + str(res))
    print("\tANS:\n" + str(ans))
    print("\tRIGHT:\n" + str(right))

all_right = all(correct_answers)
print("all correct", all_right)

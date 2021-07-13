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


if __name__ == "__main__":
    def rotate_matrix(grid, n=None, m=None, filter_none=False):
        """Return a list of all possible cell lines."""
        PAD = "PAD"
        n = n if n is not None else len(grid)
        m = m if m is not None else len(grid[0]) if n else -1
        res = [row.copy() for row in grid]
        temp_grid = [[grid[j][i] for j in range(n)] for i in range(m)]
        print("1 grid     :", grid)
        print("1 temp_grid:", temp_grid)
        if m < n:
            grid, temp_grid = temp_grid, grid
            n, m = m, n
        print("2 grid     :", grid)
        print("2 temp_grid:", temp_grid)
        res += temp_grid
        oo = (n + m) % 2
        di = abs(n - m) + 1 + oo
        ts = int(((n + m - 1) - di) / 2) + oo
        a = ts - 1

        lc = 0
        cc = 0
        e = 0
        t = (3 * n) + (3 * m) - 2
        temp = [[] for i in range(t)]
        print("3 grid     :", grid)
        print("3 temp_grid:", temp_grid)
        print("3 temp:", temp)
        # print("len[]({}), len[0]({})".format(len(temp), len(temp[0])))

        print("N x M: ({} x {})".format(n, m))
        for i in range(n):
            for j in range(m):
                v = grid[i][j]
                s = min(i, j)
                npl = i - s, j - s
                d1 = n + m + (npl[0] + npl[1])
                if (j - s) == 0 and (i - s) != 0:
                    d1 += m - 1

                f = max(0, min(i, m - j - 1))
                npr = i - f, j + f
                d2 = n + m + (npr[0] + npr[1])
                print("npr:", npr, "f:", f)
                if (j + f) == m and (i - f) != 0:
                    d2 += m - 1
                d2 += (n + m - 1)
                print("i:", i, "| j:", j, "| v:", v, "| d1:", d1, "| d2:", d2, "| di:", (n+m-1))
                temp[i].append((i, j, v))
                temp[j + n].append((i, j, v))
                temp[d1].append((i, j, v))
                temp[d2].append((i, j, v))
        print("4 grid     :", grid)
        print("4 temp_grid:", temp_grid)
        print("4 temp:", temp)

        return temp

    g1 = []
    print(rotate_matrix())

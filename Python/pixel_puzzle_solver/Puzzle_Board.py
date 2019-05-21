class Puzzle:
    def __init__(self, puzzle):
        if not self.verify(puzzle):
            print('Error Invalid puzzle dimensions')
        else:
            print('else')
        self.puzzle_board = puzzle
        self.rows = len(puzzle)
        self.cols = len(puzzle[0])
        self.verticle_hints = self.gen_verticle_hints()
        self.horizontle_hints = self.gen_horizontle_hints()

    def __repr__(self):
        board = self.presentify()
        res = '\n'
        for line in board:
            string = '\t'
            for val in line:
                string += str(val)
            res += string + '\n'
        res += '\n'
        return res

    def verify(self, puzzle):
        if type(puzzle) is not list:
            print('Error not a puzzle')
        sub_list_lens = [len(x) for x in puzzle]
        print(sub_list_lens)
        lst = list(set(sub_list_lens))
        if (len(lst) > 1) or (lst[0] < 2) or (len(puzzle) < 2):
            return False
        return True

    def gen_verticle_hints(self):
        board = self.puzzle_board
        rows = self.rows
        cols = self.cols
        res = [[] for i in range(cols)]
        for r in range(rows):
            for c in range(cols):
                if (board[r][c] == 1 and r == 0) or (board[r][c] == 1 and board[r - 1][c] == 0):
                    temp = r
                    count = 1
                    while (r < rows - 1) and (board[r + 1][c] == 1):
                        count += 1
                        r += 1
                    r = temp
                    res[c].append(count)
        for c in range(cols):
            if len(res[c]) == 0:
                res[c] = [0]
        print(res)
        return res

    def gen_horizontle_hints(self):
        board = self.puzzle_board
        rows = self.rows
        cols = self.cols
        res = [[] for i in range(rows)]
        for r in range(rows):
            for c in range(cols):
                if (board[r][c] == 1 and c == 0) or (board[r][c] == 1 and board[r][c - 1] == 0):
                    count = 1
                    temp = c
                    while c < cols - 1 and board[r][c + 1] == 1:
                        count += 1
                        c += 1
                    c = temp
                    res[r].append(count)
        for r in range(rows):
            if len(res[r]) == 0:
                res[r] = [0]
        print(res)
        return res

    def presentify(self):
        board = self.puzzle_board
        rows = self.rows
        cols = self.cols
        res = [[] for i in range(rows)]
        for r in range(rows):
            for c in range(cols):
                if board[r][c] == 1:
                    res[r].append('#')
                else:
                    res[r].append(' ')
        return res




puzzle1 = Puzzle([[0, 0, 0, 0, 0], [0, 1, 1, 1, 0], [0, 1, 0, 1, 0], [0, 1, 1, 1, 0], [0, 0, 0, 0, 0]])
print(puzzle1)

puzzle2 = Puzzle([[0, 0, 0, 0, 0], [1, 1, 1, 1, 1], [0, 1, 1, 1, 0], [0, 1, 0, 1, 0], [0, 1, 1, 1, 0], [0, 0, 0, 0, 0]])
print(puzzle2)

puzzle3 = Puzzle([[1, 0, 0, 0, 0], [1, 1, 1, 1, 1], [1, 1, 1, 1, 0], [1, 1, 0, 1, 0], [1, 1, 1, 1, 0], [1, 0, 0, 0, 0]])
print(puzzle3)

puzzle4 = Puzzle([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                   0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0,
                   0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
                  [0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0,
                   0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0],
                  [0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0,
                   0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0],
                  [0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0,
                   0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0],
                  [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0,
                   0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0],
                  [0, 1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0,
                   0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0],
                  [0, 1, 0, 0, 1, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0,
                   0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0],
                  [0, 1, 0, 0, 1, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0,
                   0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0],
                  [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                   1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]])
print(puzzle4)

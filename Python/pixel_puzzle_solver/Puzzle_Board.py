class Puzzle:
    def __init__(self, puzzle):
        if not self.verify(puzzle):
            print('Error Invalid puzzle dimensions')
        else:
            print('else')
        self.puzzle_board = puzzle
        self.rows = len(puzzle)
        self.cols = len(puzzle[0])
        self.vertical_hints = self.gen_vertical_hints()
        self.horizontal_hints = self.gen_horizontal_hints()
        self.horizontal_spacer = self.gen_horizontal_spacer()
        self.vertical_divider = self.gen_vertical_divider()
        self.vertical_hints_height = self.get_vertical_height()

    def __repr__(self):
        board = self.presentify()
        res = '\n'
        res += self.vertical_hint_presentation()
        h_hints = self.horizontal_hint_presentation()
        length = len(self.horizontal_spacer)
        for i in range(len(board)):
            # print('self.height', self.vertical_hints_height)
            hint = h_hints[i]
            string = ''
            # print('lenght', length, ' len(hint', len(hint))
            string += hint + ' '
            line = board[i]
            for val in line:
                string += str(val)
            res += string + ' |\n'
        # res += '|' + self.vertical_divider + '|'
        # bottom line
        line = '|'
        for i in range(length - 1):
            line += '_'
        # res += self.horizontal_spacer[:-1] + '|' + self.vertical_divider + '|'
        res += line + '|' + self.vertical_divider + '|'
        res += '\n'
        return res

    def verify(self, puzzle):
        if type(puzzle) is not list:
            print('Error not a puzzle')
        sub_list_lens = [len(x) for x in puzzle]
        # print(sub_list_lens)
        lst = list(set(sub_list_lens))
        if (len(lst) > 1) or (lst[0] < 2) or (len(puzzle) < 2):
            return False
        return True

    def gen_vertical_hints(self):
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

    def gen_horizontal_hints(self):
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

    def vertical_hint_presentation(self):
        hints = self.vertical_hints
        cols = self.cols
        # size = max([len(hints[x]) for x in range(cols)])
        size = self.vertical_hints_height
        c = 0
        divider = self.vertical_divider
        # Top line of vertical hints
        string = '  ' + self.horizontal_spacer[:-1] + divider + '\n'
        length = len(self.horizontal_spacer)
        line = ' '
        double_digit = ['_', '_']
        for i in range(length - 1):
            line += '_'
        while c in range(cols):
            # print('c', c)
            string += ' ' + self.horizontal_spacer
            for t in range(cols):
                print('double_digit', double_digit)
                #print('hints[t]:', hints[t], ' t: ', t)
                if t == 0 and size > 0:
                    string += ' '
                if len(double_digit) > 0 and (len(hints[t]) > 0 and max(hints[t]) // 10 > 0):
                    filler = double_digit.pop()
                    if filler == '_':
                        if len(double_digit) > 0:
                            first_digit = max(hints[t]) // 10
                            second_digit = max(hints[t]) % 10
                            double_digit.append(second_digit)
                            double_digit.append(first_digit)
                    string += str(filler)
                    if len(double_digit) == 0:
                        hints[t].pop()
                        # if len(hints[t]) == 0:
                        #     hints[t] = [0]
                        print('hints:', hints)
                        double_digit = ['_', '_']
                elif len(hints[t]) > 0 and len(hints[t]) == size:
                    string += str(hints[t][size - 1])
                    if hints[t] != 0:
                        hints[t].pop()
                elif size != 0:
                    string += ' '
                if (t == cols - 1) and size >= 1:
                    string += ' |\n'
            #c += 1
            # if c == height:
            #     string += line
            size -= 1
            # print('size', size)
            if size < 1:
                break
        # left cover of horizontal hint table
        string += line + '|' + divider + '|\n'
        return string

    # def vertical_hint_presectation_rec(self, size):
    #     cols = self.cols
    def gen_horizontal_spacer(self):
        hints = self.horizontal_hints
        width = max([((len(hints[x]) + 1) * 2) for x in range(len(hints))])
        res = ' '
        for i in range(width):
            res += ' '
        res += ' |'
        # print('\tres:', len(res))
        return res

    def gen_vertical_divider(self):
        cols = self.cols + 2
        divider = ''
        for i in range(cols):
            divider += '_'
        return divider

    def get_vertical_height(self):
        hints = self.vertical_hints
        cols = self.cols
        size = max([len(hints[x]) for x in range(cols)])
        new_hints = [max(hints[y]) for y in range(len(hints))]
        new_hints = [4 if ((new_hints[x] // 10) > 0) else 1 for x in range(len(new_hints))]
        max_run = max(new_hints)
        max_run_index = new_hints.index(max_run)
        max_run += len(hints[max_run_index])
        # print('new_hints', new_hints, ' size', size, ' max_run', max_run)
        size = max(size, max_run)
        return size

    # Issue with the presentation, it doesnt print double digits very well


    def horizontal_hint_presentation(self):
        hints = self.horizontal_hints
        res = []
        for row in hints:
            # res.append(str(row) + '\n')
            string = self.stringify_list(row)  # + '\n'
            length = len(string)
            ab = '|'
            # print('len', len(self.horizontal_spacer), ' len', length)
            while ((len(self.horizontal_spacer) - length) - 3) > 0:
                length += 1
                ab += ' '
            res.append(ab + string + '  |')
        return res

    def stringify_list(self, row):
        res = '|'
        for el in row:
            res += str(el) + '|'
        return res


puzzle1 = Puzzle([[0, 0, 0, 0, 0], [0, 1, 1, 1, 0], [0, 1, 0, 1, 0], [0, 1, 1, 1, 0], [0, 0, 0, 0, 0]])
print(puzzle1)

puzzle2 = Puzzle([[0, 0, 0, 0, 0], [1, 1, 1, 1, 1], [0, 1, 1, 1, 0], [0, 1, 0, 1, 0], [0, 1, 1, 1, 0], [0, 0, 0, 0, 0]])
print(puzzle2)

puzzle3 = Puzzle([[1, 0, 0, 0, 0], [1, 1, 1, 1, 1], [1, 1, 1, 1, 0], [1, 1, 0, 1, 0], [1, 1, 1, 1, 0], [1, 0, 0, 0, 0]])
print(puzzle3)

puzzle4 = Puzzle([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                   0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                  [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0,
                   0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1],
                  [0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0,
                   0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1],
                  [0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0,
                   0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1],
                  [0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0,
                   0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1],
                  [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0,
                   0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1],
                  [0, 1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0,
                   0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1],
                  [0, 1, 0, 0, 1, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0,
                   0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1],
                  [0, 1, 0, 0, 1, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0,
                   0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1],
                  [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                   1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]])
print(puzzle4)

puzzle5 = Puzzle([[0, 1, 0, 1, 0], \
                  [0, 1, 0, 1, 0], \
                  [0, 0, 1, 0, 0], \
                  [0, 1, 0, 1, 0], \
                  [0, 1, 0, 1, 0], \
                  [0, 1, 0, 1, 0], \
                  [0, 1, 0, 1, 0], \
                  [0, 1, 0, 1, 0], \
                  [0, 1, 0, 1, 0], \
                  [0, 1, 0, 1, 0], \
                  [0, 1, 0, 1, 0], \
                  [0, 1, 0, 1, 0], \
                  [0, 1, 0, 1, 0], \
                  [0, 1, 0, 1, 0], \
                  [0, 1, 0, 1, 0]])
print(puzzle5)

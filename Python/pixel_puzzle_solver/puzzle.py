class Puzzle:
    def __init__(self, name, id, puzzle):
        if not verify(puzzle):
            print('Error Invalid puzzle dimensions')
            puzzle = self.pad_puzzle(puzzle)
            # raise ValueError('Error Invalid puzzle dimensions')
        # else:
        #     print('else')
        # print('puzzle_in:',puzzle)
        self.name = name.title()
        self.id = id
        self.puzzle_board = puzzle  # stores the parameter value
        self.rows = len(puzzle)  # num rows in puzzle
        self.cols = len(puzzle[0])  # num cols in puzzle
        self.num_pixels = self.count_num_pixels(puzzle)  # number of pixels coloured in pixel
        self.vertical_hints = self.gen_vertical_hints()  # list of lists containing the v_hints to puzzle
        self.horizontal_hints = self.gen_horizontal_hints()  # list of lists containing the h_hints to puzzle
        self.horizontal_spacer = self.gen_horizontal_spacer()  # string storing space based on max len of sublists in h_hints
        self.vertical_divider = self.gen_vertical_divider()
        self.vertical_hints_height = self.get_vertical_height()
        self.solution_board = self.gen_solution_board()
        self.solved_puzzle_board = self.gen_solved_puzzle()

    def __repr__(self):
        return self.solution_board

    def get_name(self):
        return self.name

    def gen_solution_board(self):
        board = self.presentify()
        name = self.name
        id = self.id
        res = '\n\tPuzzle: ' + name + ', id: ' + str(id) + '\n\t\t\t' + str(self.rows) + ' X ' + str(self.cols) + '\n'
        res += self.vertical_hint_presentation()
        h_hints = self.horizontal_hint_presentation()
        length = len(self.horizontal_spacer)
        for i in range(len(board)):
            # print('self.height', self.vertical_hints_height)
            hint = h_hints[i]
            string = ''
            # print('length', length, ' len(hint', len(hint))
            string += hint + ' '
            line = board[i]
            for val in line:
                string += str(val)
            res += string + ' |\n'
        # bottom line
        line = '|'
        for i in range(length - 1):
            line += '_'
        res += line + '|' + self.vertical_divider + '|'
        res += '\n'
        return res

    def pad_puzzle(self, puzzle):
        # new_puzzle = []
        # rows = 0
        # cols = 0
        if type(puzzle) == list:
            rows = len(puzzle)
            # row_len = len(rows)
            if rows > 2:
                cols = max([len(puzzle[x]) for x in range(rows)])
                new_puzzle = [[0 for y in range(cols)] for x in range(rows)]
                # print('new_puzzle', new_puzzle)
                i = rows - 1
                j = cols - 1
                while i >= 0:
                    row_len = len(puzzle[i])
                    while j >= 0:
                        p = row_len - j
                        # print('i:', i, ', j:', j, ', row_len:', row_len, ', p:', p)
                        if j < row_len:
                            new_puzzle[i][j] = puzzle[i][j]
                            # using { if p < row_len: new_puzzle[i][j] = puzzle[i][p] }
                            # instead of the above will horizontally flip the puzzle
                        j -= 1
                    i -= 1
                    j = cols - 1
                # print('new_puzzle', new_puzzle)
            else:
                new_puzzle = sample_smiley
        else:
            new_puzzle = sample_smiley
        return new_puzzle

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
                    while temp < cols - 1 and board[r][temp + 1] == 1:
                        count += 1
                        temp += 1
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
        divider = self.vertical_divider
        # Top line of vertical hints
        string = '  ' + self.horizontal_spacer[:-1] + divider + '\n'
        length = len(self.horizontal_spacer)
        line = ' '
        for i in range(length - 1):
            line += '_'
        hint_table = [[None for j in range(size)] for i in range(cols)]
        single_digit_hints = []
        for r in range(len(hint_table)):
            lst = hints[r]
            new_lst = []
            for c in range(len(lst)):
                el = lst[c]
                # print('el',el)
                if type(el) == int and el // 10 > 0:
                    # print('el:',el,', el // 10:', (el // 10))
                    first_digit = el // 10
                    second_digit = el % 10
                    new_lst += ['_', first_digit, second_digit, '_']
                    # print('sub_a', sub_a, ', sub_b:', sub_b)
                elif type(el) != int or (type(el) == int and el // 10 <= 0):
                    new_lst.append(el)
            new_lst.reverse()
            single_digit_hints.append(new_lst)
        print('single_digits_hints', single_digit_hints)
        hints = single_digit_hints
        # print('hint_table', hint_table)
        c = 0
        while c in range(cols):
            # print('c', c)
            string += ' ' + self.horizontal_spacer
            for t in range(cols):
                # print('double_digit', double_digit)
                # print('hints[t]:', hints[t], ' t: ', t)
                if t == 0 and size > 0:
                    string += ' '
                if len(hints[t]) > 0 and len(hints[t]) == size:
                    string += str(hints[t][size - 1])
                    if len(hints[t]) != 1:
                        hints[t].pop()
                elif size != 0:
                    string += ' '
                if (t == cols - 1) and size >= 1:
                    string += ' |\n'
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
        width = max([((len(hints[x]) + 3) * 2) for x in range(len(hints))])
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

    def count_num_pixels(self, puzzle):
        num_pixels = 0
        for i in range(len(puzzle)):
            # print('val',val)
            if type(puzzle[i]) != list:
                # print('puzzle[i]',puzzle[i])
                num_pixels += puzzle[i]
            else:
                for j in range(len(puzzle[i])):
                    num_pixels += puzzle[i][j]
        return num_pixels

    def transpose_puzzle(self, board):

    #     public static void matrixTransposeRecursive(int[][] A, int r, int c, int s){
    #         if (s == 1){
    #             return;
    #         }
    #         else {
    #             int
    #             x = (int)
    #             Math.floor(s / 2);
    #             matrixTransposeRecursive(A, r, c, x);
    #             matrixTransposeRecursive(A, r + x, c + x, s - x);
    #             matrixTransposeSwap(A, r, c + x, r + x, c, x, s - x);
    #         }
    #     }
    #
    # public static void matrixTransposeSwap(int[][] A, int r1, int c1, int r2, int c2, int s1, int s2){
    #     if (s1 < s2){
    #         matrixTransposeSwap(A, r2, c2, r1, c1, s2, s1);
    #     }
    #     else if (s1 == 1){
    #         int temp = A[r1][c1];
    #         A[r1][c1] = A[r2][c2];
    #         A[r2][c2] = temp;
    #     }
    #     else {
    #         int x = (int)
    #         Math.floor(s1 / 2);
    #         matrixTransposeSwap(A, r2, c2, r1, c1, s2, x);
    #         matrixTransposeSwap(A, r2, c2 + x, r1 + x, c1, s2, s1 - x);
    #     }
    # }


        r = 0
        c = 0
        new_board = [[0 for c in range(len(board))] for r in range(len(board[r]))]
        # printA('board',board)
        while r in range(len(board)):
            while c in range(len(board[r])):
                new_board[c][r] = board[r][c]
                c += 1
            r += 1
            c = 0
        # printA('newBoard', new_board)
        return new_board

    def gen_solved_puzzle(self):
        n_rows = self.rows
        n_cols = self.cols
        v_hints = self.vertical_hints
        h_hints = self.horizontal_hints
        num_pixels = self.num_pixels
        print('n_rows:', n_rows, ', n_cols:', n_cols, ', num_pixels:', num_pixels)
        # printA('v_hints:', v_hints)
        # printA('h_hints:', h_hints)
        board = [[0 for i in range(n_cols)] for x in range(n_rows)]
        t_board = self.transpose_puzzle(board.copy())
        i = 0
        while i in range(len(board)):
            print('using hints:',h_hints)
            board[i] = self.horizontal_row_fill(board[i], h_hints[i])
            i += 1
        printA('horizontal_board', board)
        i = 0
        while i in range(len(t_board)):
            print('using hints:',v_hints)
            t_board[i] = self.horizontal_row_fill(t_board[i], v_hints[i])
            i += 1
        t_board = self.transpose_puzzle(t_board)
        printA('vertical_board', t_board)
        i = 0
        j = 0
        while i in range(len(board)):
            while j in range(len(board[i])):
                if t_board[i][j] == 1:
                    board[i][j] = 1
                j += 1
            j = 0
            i += 1
        printA('resulting board',board)
        if board == self.puzzle_board:
            print('\n\nfinished puzzle!\n\n')
            return board

        i = 0
        j = 0
        while i in range(len(board)):
            board[i] = self.row_continuity(board[i], h_hints, i)
            i += 1

        printA('row_continuity',board)
        if board == self.puzzle_board:
            print('\n\nfinished puzzle!\n\n')
            return board

        i = 0
        j = 0
        t_board = self.transpose_puzzle(board)
        while i in range(len(t_board)):
            t_board[i] = self.row_continuity(t_board[i], v_hints, i)
            i += 1

        board = self.transpose_puzzle(t_board)
        printA('col_continuity',board)
        if board == self.puzzle_board:
            print('\n\nfinished puzzle!\n\n')
            return board

        return board

    def len_hints(self, arr):
        return sum(arr) + len(arr) - 1

    # def how_many_counted(self, arr):
    #     seen = False
    #     blanks = 0
    #     for el in arr:
    #         if el == 0:
    #             if not seen:
    #                 blanks += 1
    #         else:
    #             if not seen:
    #                 blanks += 1
    #             seen = True
    #     # print('returning blanks:',blanks)
    #     return blanks

    # def usable_space(self, space):
    #     res = []
    #     space_sum = sum(space)
    #     if space_sum == 0:
    #         return space, space_sum
    #     i = len(space) - 1
    #     while i in range(len(space)):
    #         if space[i] == 1:
    #             i += 1
    #             break
    #         i -= 1
    #     if i >= 0:
    #         i += 1
    #     space_sum += self.how_many_counted(space[:i + 1])
    #     # print('returning i:',i)
    #     # print(space[i:])
    #     return space[i:], space_sum

    # def calc_diff(self, arr, space, index):
    #     length = len(arr)
    #     if length <= index:
    #         # print('already finished!')
    #         return -1
    #     print('fitting ' + str(arr) + ' into ' + str(space) + ' starting at ' + str(arr[index]))
    #     new_space, space_to_remove = self.usable_space(space)
    #     spaces_len = len(new_space)
    #     v = (sum(arr[:index]))
    #     # print('v',v)
    #     covered_space = sum(space)
    #     to_be_covered = sum(arr)
    #     space_left_to_cover = self.len_hints(arr[index:])
    #     arr_len = space_left_to_cover
    #     if covered_space == to_be_covered:
    #         # print('base')
    #         return -1
    #     # print('new_space',new_space)
    #     # print('space_to_remove',space_to_remove)
    #     # print('spaces_len',spaces_len)
    #     # print('arr_len',arr_len)
    #     return spaces_len - arr_len

    def fill_row(self, row, hints, index, ext_buff):
        hint = hints[index]
        new_row = row  # .copy()
        left_hints = hints[:index]
        right_hints = hints[index + 1:]
        left = self.len_hints(left_hints) + 1
        right = self.len_hints(right_hints) + 1
        remainder = len(row)
        start = -1
        end = -1
        if index == 0:
            if hint > ext_buff:
                remainder = hint - ext_buff
                start = ext_buff
                end = ext_buff + remainder
        elif index == (len(hints) - 1):
            if hint > ext_buff:
                remainder = hint - ext_buff
                start = len(row) - remainder - ext_buff
                end = len(row) - ext_buff
        else:
            remainder = len(row) - left - right - hint
            if hint > remainder:
                start = left + remainder
                end = len(row) - right - remainder
        # print('left_hints:',left_hints,' right_hints:',right_hints,' left:',left,' right:', right, ' remainder:',remainder)
        i = 0
        # print('start:',start,'end:',end)
        while i in range(len(row)):
            if start <= i < end:
                new_row[i] = 1
            i += 1
        return new_row

    def horizontal_row_fill(self, puzzle_row, hints):
        i = 0
        temp_row = puzzle_row.copy()
        while i in range(len(hints)):
            ext_buffer = len(puzzle_row) - self.len_hints(hints)  # calc_diff(hints, puzzle_row, i)
            print('fitting ' + str(hints) + ' into ' + str(puzzle_row) + ' starting at ' + str(
                hints[i]) + ' buffer_space: ' + str(ext_buffer))
            temp_row = self.fill_row(puzzle_row, hints, i, ext_buffer)
            i += 1
        return temp_row

    def row_continuity(self, row, hints, index):
        n_cols = len(row)
        row_sum = sum(row)
        hints_sum = sum([sum(hints[i]) for i in range(len(hints))])
        if row_sum == hints_sum:
            return row
        c = 0
        curr_hint = 0
        while c in range(n_cols):
            # print('c',c)
            if row[c] == 1:
                if c == 0:
                    # print('ends')
                    t = c
                    seen = False
                    while t in range(hints[index][curr_hint]):
                        if row[t] == 0:
                            print('adding', t)
                            seen = True
                        row[t] = 1
                        if c == n_cols - 1:
                            t -= 1
                        else:
                            t += 1
                    c = t
                    curr_hint += 1
                    if seen:
                        print('to', c)
                        seen = False
                elif c == n_cols - 1:
                    # print('ends')
                    t = c
                    seen = False
                    hint = hints[index][-1]
                    # print('hint',hint)
                    while (len(row) - t) in range(hints[index][-1]):
                        if row[t] == 0:
                            print('adding',t)
                            seen = True
                        row[t - 1] = 1
                        if c == n_cols - 1:
                            t -= 1
                        else:
                            t += 1
                    curr_hint += 1
                    if seen:
                        print('to',c)
                        seen = False
            c += 1
        print('row:',row)
        return row


# def sum_rest_lst(lst, val):
#     res = 0
#     for i in range(len(lst)):
#         if lst[i] != val:
#             res += lst[i]
#     return res


def puzzleify(list_of_puzzles):
    new_list = {}
    for puzzle in list_of_puzzles:
        # print('a:',puzzle,'b',list_of_puzzles[puzzle][1],'c:',list_of_puzzles[puzzle][2])
        temp = Puzzle(puzzle, list_of_puzzles[puzzle][1], list_of_puzzles[puzzle][2])
        print(temp)
        new_list[temp.get_name()] = temp
    return new_list


def verify(puzzle):
    if type(puzzle) is not list or len(puzzle) == 0 or type(puzzle[0] != list):
        print('Error not a puzzle')
        return False
    sub_list_lens = [len(puzzle[x]) for x in range(len(puzzle))]
    # print('sub_lst',sub_list_lens)
    lst = list(set(sub_list_lens))
    # print('lst',lst)
    if (len(lst) > 1) or (lst[0] < 3) or (len(puzzle) < 3):
        return False
    return True


def printA(name='arrIn', arr=None):
    if arr is None or len(arr) == 1:
        arr = [[]]
        print('nothing given to print', arr)
        return
    string = name + '\n\t    '
    for i in range(len(arr[0])):
        b = (i + 1) % 5
        if i > 0 and i % 5 == 0:
            string += ' ' + str((i + 1) // 5)
        else:
            string += ' '
    string += '\n['
    for i in range(len(arr)):
        in_string = '\t' + str(i) + ':\t['
        for j in range(len(arr[i])):
            if j < len(arr[i]) - 1:
                in_string += str(arr[i][j])  # + ', '
            else:
                in_string += str(arr[i][j])
            if j > 0 and (j + 1) % 5 == 0:
                in_string += '|'
        if i < len(arr) - 1:
            in_string += '],\n'
        else:
            in_string += ']'
        string += in_string
    string += ']\n'
    print(string)


def truthy_list(lst):
    if type(lst) == list and len(lst) > 0:
        b = 0
        for el in lst:
            # print('el',el, 'lst', lst)
            if type(el) != list:
                return False
            if len(el) > b:
                b = len(el)
            for val in el:
                if type(val) != int:
                    return False
        return True and b != 0
    return False


sample_smiley = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0],
                 [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
                 [0, 1, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 1, 0],
                 [0, 1, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 1, 0],
                 [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
                 [0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0],
                 [0, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0],
                 [0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0],
                 [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0]]

sample_smiley_puzzle = Puzzle('sample_smiley', 0, sample_smiley)

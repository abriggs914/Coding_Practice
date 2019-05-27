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
        r = 0
        c = 0
        while r in range(len(h_hints)):
            row_hint = h_hints[r]
            curr_puzzle_row = board[r]
            row_spaces = self.determine_row_spaces(board[r])
            num_row_pixels = self.count_num_pixels(row_hint)
            num_row_occupied = num_row_pixels + len(row_hint) - 1
            row_hint_tracker = 0
            for hint in row_hint:
                col_index = 0
                for space in row_spaces:
                    diff = space - num_row_occupied
                    print('r:',r,', hint:',hint,', space:',space, ', num_row_p', num_row_pixels, ', num_row_occ:', num_row_occupied,', diff',diff, ', row_hint_tracker:',row_hint_tracker)
                    if hint > diff:
                        temp_row = self.sim_row_horizontal_filling(curr_puzzle_row, row_hint, hint, row_hint_tracker, n_cols)
                        temp_row_row = temp_row[0]
                        temp_row_sum_left = 0 if temp_row[1] == 0 else temp_row[1] + 1
                        temp_row_sum_right = 0 if temp_row[2] == 0 else temp_row[2] + 1
                        buffer = self.determine_row_spaces(temp_row_row)
                        check_var = buffer[0] - hint
                        offset_space = 0 if check_var <= 0 else check_var  # (buffer[0] - 1) - hint  #+ temp_row_sum_left + temp_row_sum_right - hint
                        space_to_fill = (hint - (space - num_row_pixels)) // 2
                        # index = col_index + buffer[0]
                        i = 0
                        print('\tbuffer',buffer,'temp_row', temp_row, 'col_index', col_index, 'offset_space', offset_space)
                        low_bound = -1
                        up_bound = -1
                        while i in range(len(temp_row_row)):
                            if ((buffer[0] - len(row_hint) - 1) // 2) <= (hint - 1):
                                low_bound = temp_row_sum_left + offset_space
                                x = (temp_row_sum_right + offset_space)
                                up_bound = (n_cols - x)
                                if low_bound <= i < up_bound:
                                    print('\t\tfilling i:', i)
                                    board[r][i] = 1
                                    print('\t\tlow_bound:',low_bound, ', up_bound:',up_bound, ', board[r]:',board[r])
                            i += 1
                        # if low_bound > -1 and up_bound > -1:

                row_hint_tracker += 1
                        # if col_index < n_cols - 2:
                        #     board[r][col_index + buffer[0]] = 9
                        #
            row_hint_tracker = 0
            r += 1
            # print('\nrow:', r, 'row_hint:', row_hint, ',row_spaces', row_spaces, ',num_row_pixels', num_row_pixels,
            #       ',num_row_occupied:', num_row_occupied)
            # if num_row_occupied > (n_cols // 2):
            #     for i in range(len(row_hint)):
            #         hint = row_hint[i]
            #         if 0 < r < len(row_hint) - 1:
            #             hint += 2
            #         left_over = num_row_occupied - hint
            #         print('fitting hint:', hint, ',left_over:', left_over)
            #         c_index = 0
            #         for space in row_spaces:
            #             offset = 0 if space % 2 == 0 else 1
            #             offset += ((space - 1) // 2) - 1
            #             rest_of_row = self.rest_hint_vals(row_hint, hint)
            #             print('space:', space, ',c_index', c_index, ',offset:',offset, 'rest_row:', rest_of_row)
            #             rest_of_row = self.rest_hint_vals(row_hint, hint)
            #             if left_over <= (space - rest_of_row) and hint > offset:
            #                 index = c_index + (space // 2)
            #                 space_to_fill = (index - offset, index + offset)
            #                 print('\tindex', index, 'space_to_fill:' ,space_to_fill)
            #                 board[r][index] = 1
            #                 if space % 2 == 0:
            #                     board[r][index - 1] = 1
            #             if 0 < c_index < n_cols:
            #                 c_index += 2
            #             c_index += space
            #         temp = hint // 2
            # r += 1

            # row_spaces = self.determine_row_spaces(board[r])
            # num_row_pixels = self.count_num_pixels(row_hint)
            # num_row_occupied = num_row_pixels + len(row_hint) - 1
            # print('row:', r, 'row_hint:', row_hint, ',row_spaces', row_spaces, ',num_row_pixels',num_row_pixels, ',num_row_occupied:', num_row_occupied)

        # while r in range(n_rows):
        #     row_spaces = self.determine_row_spaces(board[r])
        #     num_row_pixels = self.count_num_pixels(h_hints[r])
        #     num_row_occupied = num_row_pixels + len(h_hints[r]) - 1
        #     print('\tnum_row_pixels',num_row_pixels, ',num_row_occupied:', num_row_occupied)
        #     print('\trow_spaces', row_spaces)
        #     for space in row_spaces:
        #         col_tracker = 0
        #         for val in h_hints[r]:
        #             added_one = False
        #             if col_tracker > 0 and col_tracker < len(h_hints[r]) - 1:
        #                 val += 2
        #                 added_one = True
        #                 if len(h_hints[r]) < 3:
        #                     val -= 1
        #                     added_one = False
        #                 #space -= 2
        #             # if 0 < val < len(h_hints[r]) - 1:
        #             #     val += 2
        #             row_space_without_val = num_row_occupied - val
        #             print('row_space_without_val',row_space_without_val)
        #             diff = space - val
        #             buffer = 0
        #             if added_one:
        #                 if diff % 2 == 1:
        #                     diff += 1
        #                 buffer = diff
        #             #else:
        #
        #             # print('row_spaces', row_spaces, ',r', r, ',col_tracker', col_tracker, ',space:', space, ',val:', val, ',diff:', diff, 'buffer', buffer, ',h_hints[r]',
        #             #       h_hints[r])
        #             #if 0 <= x < y:
        #             if diff < val:
        #                 # space = n_cols - sum_rest_lst(h_hints[r], val)
        #                 mid_space_index = space // 2
        #                 if space % 2 == 0:
        #                     mid_space_index -= 1
        #                 buffer = mid_space_index - (diff - 1 if diff > 0 else 0)
        #                 print('color in space,', 'mid_space_index', mid_space_index, 'buffer:', buffer)
        #                 print('row_spaces', row_spaces, ',r', r, ',col_tracker', col_tracker, ',space:', space, ',val:', val, ',diff:', diff, 'buffer', buffer, ',h_hints[r]',h_hints[r])
        #                 # divide col_tracker /2
        #                 board[r][mid_space_index] = 1
        #                 count = 1
        #                 while buffer > 1:
        #                     if buffer < 3:
        #                         # print('mid_space_index - buffer', mid_space_index - buffer)
        #                         board[r][mid_space_index - buffer] = 9
        #                     # elif buffer <= 2:
        #                     # print('mid_space_index + buffer', mid_space_index + buffer)
        #                     # print('mid_space_index - buffer', mid_space_index - buffer)
        #                     board[r][mid_space_index + buffer] = 9
        #                     board[r][mid_space_index - buffer] = 9
        #                     buffer -= 1
        #                     count += 1
        #             col_tracker += 1
        #
        #     r += 1

        # while c in range(c_cols):
        printA('board:', board)
        return 1

    def look_horizontal(self):
        pass

    def determine_row_spaces(self, row):
        res = []
        curr_count = 0
        for el in range(len(row)):
            # print('row[el]:',row[el])
            if row[el] == 0:
                curr_count += 1
            else:
                if curr_count > 0:
                    res.append(curr_count)
                curr_count = 0
        res.append(curr_count)
        if len(res) > 1 and res[-1] == 0:
            res.pop()
        return res

    def rest_hint_vals(self, row, hint):
        res = 0
        seen = False
        for i in range(len(row)):
            if 0 < i < len(row) - 1:
                res += 1
            if row[i] != hint or seen:
                res += row[i]
            else:
                seen = True
        return res

    def get_name(self):
        return self.name

    def sim_row_horizontal_filling(self, puzzle_row, row_hint, hint, index, orig_cols):
        orig_puzzle = puzzle_row
        puzzle_row, counted = self.row_trim(puzzle_row)
        print('trim_row:',puzzle_row,', counted:', counted)
        n_cols = len(puzzle_row)
        x = n_cols - counted
        if x < 0:
            x = 0
        new_row = [1 if puzzle_row[i] == 1 else 0 for i in range(x)]
        i = 0
        mid_index = n_cols // 2
        hint_space = hint // 2
        offset = 0 if n_cols % 2 == 0 else 1
        bounds = [i for i in range((mid_index - hint_space), (mid_index + hint_space + offset))]
        sum_left = 0
        sum_right = 0
        left_side = []
        right_side = []
        if len(row_hint) == 1 or counted >= len(puzzle_row):
            return (new_row, sum_left, sum_right)
        elif len(row_hint) == 2:
            order_placement = row_hint[index]  #row_hint.index(hint)
            other_index = 1 if index == 0 else 0
            print('order_placement',order_placement,'other_index',other_index)
            other_hint = row_hint[other_index]
            size = len(new_row)
            if index < other_index:
                right_side = [row_hint[1]]
                sum_right = row_hint[1] + 1
            else:
                left_side = [row_hint[0]]
                sum_left = row_hint[0] + 1
            # sum_left = 0 if index < other_index else row_hint[0]
            # sum_right = row_hint[1] if index < other_index else 0
            if n_cols != orig_cols:
                i = orig_cols - n_cols + 1
                if i < 0:
                    i = 0
            while i in range(size):
                if order_placement > other_index:
                    if n_cols - i - 1 <= other_hint:
                        new_row[i] = -2
                else:
                    if i < other_hint:
                        new_row[i] = -3
                i += 1
        else:
            order_placement = row_hint.index(hint)
            left_side = row_hint[:order_placement]
            right_side = row_hint[order_placement + 1:]
            sum_left = self.rest_hint_vals(left_side, 0)
            sum_right = self.rest_hint_vals(right_side, 0)
            size = len(new_row)
            if n_cols != orig_cols:
                i = orig_cols - n_cols
                if i < 0:
                    i = 0
            while i in range(size):
                if sum_left > 0 and i <= sum_left:
                    new_row[i] = -4
                elif sum_right > 0 and (n_cols - i - 1) <= sum_right:
                    print('i',i)
                    new_row[i] = -5
                i += 1
        print('row_hint:',row_hint,', left_side:',left_side,', sum_left:',sum_left,', right_side:',right_side,', sum_right:',sum_right)
        print('new_row', new_row)
        if n_cols != orig_cols:
            new_row = orig_puzzle[:len(new_row) + 1] + new_row
        res = (new_row, sum_left, sum_right)
        return res

    def row_trim(self, puzzle_row):
        print('puzzle_row:', puzzle_row)
        temp = []
        i = 0
        while i in range(len(puzzle_row)):
            if puzzle_row[i] == 1:
                i += 1
                print('\n\n\n\n\n\n\n\n\n\nn\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n')
                continue
            else:
                return puzzle_row[i:], i + (0 if i == 0 else 2)
        return puzzle_row, i  #  + (0 if i == 0 else 2)


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
    string = name + '\t'
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
                 [0, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0],
                 [0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0],
                 [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0]]

sample_smiley_puzzle = Puzzle('sample_smiley', 0, sample_smiley)

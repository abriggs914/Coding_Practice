def solve_sudoku(board):
    def is_valid(x, y, num):
        # Check if the given number num is valid at the given
        # position x, y on the sudoku board
        for i in range(9):
            if board[x][i] == num:
                return False
        for i in range(9):
            if board[i][y] == num:
                return False
        x0 = (x // 3) * 3
        y0 = (y // 3) * 3
        for i in range(3):
            for j in range(3):
                if board[x0 + i][y0 + j] == num:
                    return False
        return True

    def solve():
        for x in range(9):
            for y in range(9):
                if board[x][y] == 0:
                    for num in range(1, 10):
                        if is_valid(x, y, num):
                            board[x][y] = num
                            if solve():
                                return True
                            else:
                                board[x][y] = 0
                    return False
        return True

    if solve():
        return board
    else:
        return None
# To use this code, simply call the solve_sudoku() function and pass in the sudoku board as a list of lists. For example:

# Copy code
board = [    [3, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 8, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 4, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [2, 3, 4, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0]
]
solved_board = solve_sudoku(board)
print(f"{solved_board=}")
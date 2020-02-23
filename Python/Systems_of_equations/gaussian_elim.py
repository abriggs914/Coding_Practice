'''

Systems of equations solver using gaussian elimination and parital pivoting.
currently an error when solving matrix_l. This is an example of catastrophic
cancellation.

February 2020

'''

class Matrix() :
    
    def __init__(self, grid, solutions=None) :
        self.grid = grid
        self.solutions = solutions
        self.n_rows = max(0, len(grid))
        if self.n_rows > 0 :
            self.n_cols = max(0, len(grid[0]))
        else :
            self.n_cols = 0
        self.diagonally_dominant_matrix = None
        self.diagonally_dominant_solutions = None
        self.upper_triangular_matrix = None
        self.upper_triangular_solutions = None
        self.hasSolutions = True if solutions else False
        self.solved_system = None
            
    def __repr__(self) :
        return self.stringify_system(self.grid, self.solutions)
        
    def print_solved_system(self) :
        if not self.solved_system : 
            self.solved_system = self.solve_system()
        print(self.stringify_system(self.upper_triangular_matrix, self.upper_triangular_solutions, self.solved_system))
        
    def stringify_system(self, grid, solutions=None, key_vals=None) :
        res = "\n"
        add_ans = True if solutions else False
        for row in grid :
            res += "\t" + str(row) 
            if add_ans :
                res += "\t| " + str(solutions[grid.index(row)])
            res += "\n"
        if key_vals:
            labels = [str(chr(65 + i)) for i in range(len(grid))]
            # print("key_vals: " + str(key_vals) + ", labels: " + str(labels))
            res += "y = "
            for label in labels :
                res += "(" + str(key_vals[label]) + ")" + str(label) + " "
            res += "\n"
        return res
    
    def solve_diagonally_dominant(self, grid=None) :
        wasNone = False
        if not grid :
            wasNone = True
            grid = copy_grid(self.grid)
        new_grid = copy_grid(grid)
        res = []
        index = 0
        to_check = [i for i in range(self.n_rows)]
        for c in range(self.n_cols) :
            if to_check :
                # print("toCheck: " + str(to_check))
                row_vals_at_cols = [new_grid[r][c] for r in to_check]
                max_val = max(row_vals_at_cols)
                max_index = row_vals_at_cols.index(max_val)
                to_remove = to_check[max_index]
                to_check.remove(to_remove)
                res.append(new_grid[to_remove])
        if to_check :
            for i in to_check :
                res.append(new_grid[i])
        if wasNone :
            self.diagonally_dominant_matrix = copy_grid(res)
            self.diagonal_solutions()
        else :
            return copy_grid(res)
            
    def diagonal_solutions(self) :
        res = []
        for r in range(len(self.diagonally_dominant_matrix)) :
            row = self.diagonally_dominant_matrix[r]
            index = self.grid.index(row)
            # index -> r
            res.append(self.solutions[index])
        self.diagonally_dominant_solutions = copy_grid(res)
        
    def get_col_multiplier(self, grid, r, c) :
        if r > 0 :
            # if c > 0 :
            rc = grid[r][c]
            upper = grid[c][c]
            # print("rc: " + str(rc) + ", upper: " + str(upper))
            return rc / upper if upper != 0 else 0
        # print("returning 1")
        return 1
            
    def upper_triangular(self) :
        grid = self.diagonally_dominant_matrix
        # col = 0
        if not grid :
            self.solve_diagonally_dominant()
            grid = copy_grid(self.diagonally_dominant_matrix)
        for col in range(self.n_cols) :
            temp = copy_grid(grid[:col + 1])
            sequence = list(range(col, self.n_rows))
            sequence.remove(col)
            for r in sequence :
                row = grid[r]
                compare_row = grid[col]
                multiplier = self.get_col_multiplier(grid, r, col)
                # print("\nBEFORE\n\trow: " + str(row) + "\n\tcompare_row: " + str(compare_row) + "\n\tmultiplier: " + str(multiplier))
                # print(print_grid(temp, "temp BEFORE\n"))
                row = [row[x] - (compare_row[x] * multiplier) for x in range(len(row))]
                # print("\nAFTER\n\trow: " + str(row) + "\n\tcol: " + str(col) + "\n\tr: " + str(r)) # "\n\tcompare_row: " + str(compare_row) + "\n\tmultiplier: " + str(multiplier))
                temp.append(row)
                self.modify_solutions(r, col, multiplier)
                # print(print_grid(temp, "temp AFTER\n"))
            grid = copy_grid(self.solve_diagonally_dominant(temp))
            # print(print_grid(grid, "AFTER temp addition\n"))
        print(print_grid(grid, "\n\tSOLVED\n"))
        print(self.stringify_system(grid, self.upper_triangular_solutions))
        self.upper_triangular_matrix = copy_grid(grid) 
        
    def modify_solutions(self, r, col, multiplier) :
        if not self.upper_triangular_solutions :
            res = copy_grid(self.diagonally_dominant_solutions)
        else :
            res = copy_grid(self.upper_triangular_solutions)
        a = res[r][0]
        b = res[col][0]
        # print("\n\tr: " + str(r) + "\n\tcol: " + str(col) + "\n\tmultiplier: " + str(multiplier) + "\n\ta: " + str(a) + "\n\tb: " + str(b) + "\n\tres: " + str(res))
        res[r] = [a - (b * multiplier)]
        self.upper_triangular_solutions = copy_grid(res)
        
    def solve_system(self, gridIn=None) :
        res = {}
        wasNone = False
        grid = None
        if not gridIn :
            wasNone = True
            if not self.upper_triangular_matrix :
                self.upper_triangular()
            grid = copy_grid(self.upper_triangular_matrix)
        else :
            grid = copy_grid(gridIn)
        n_rows = len(grid)
        sequence = list(range(65, (65 + n_rows)))
        sequence.reverse()
        # res = self.gen_system_labels(grid, res)
        for i in sequence :
            label = chr(i)
            res[label] = self.solve_row(label, res, grid)
        print("\n\tRes:\n")
        for key, val in res.items() :
            print(str(key) + "\t:\t" + str(val))
        if not wasNone :
            self.solved_system = res
        return res
        
    def solve_row(self, label, solns, grid) :
        row_index = ord(label) - 65
        row = grid[row_index]
        # print("solving row: " + str(row) + ", looking for " + str(label) + ", using: " + str(solns) + ", on: " + str(grid))
        n_zeros = row.count(0)
        n_cols = len(row)
        if abs(n_zeros - n_cols) == 1 :
            val = [x for x in row if x != 0][0]
            sol = self.upper_triangular_solutions[row_index][0]
            # print("val: " + str(val) + ", sol: " + str(sol))
            return sol / val
        else :
            # if abs(n_zeros - n_cols) == 2 :
            indices_to_check = [i for i in range(len(row)) if row[i] != 0]
            offset = copy_grid(indices_to_check)
            res = 0
            # print("indices_to_check BEFORE: " + str(indices_to_check))
            for i in indices_to_check :
                new_label = str(chr(65 + i))
                # print("CHECKING new_label: " + str(new_label) + ", i: " + str(i))
                if new_label in solns :
                    res += solns[new_label] * row[i]
                    # print("\tadding " + str(new_label) + ", res: " + str(res))
                    offset.remove(i)
                # else :
                    # print("\tWE DON\'t KNOW " + str(new_label) + " YET!!!")
            # print("RES: " + str(res))
            # print("indices_to_check AFTER: " + str(indices_to_check))
            if len(offset) == 1 :
                val = [x for x in row if x != 0][0]
                sol = self.upper_triangular_solutions[row_index][0] - res
                # print("\n\tWIDDLED DOWN\nval: " + str(val) + ", solBefore: " + str(sol + res) + ", res: " + str(res) + ", solAfter: " + str(sol))
                return sol / val
            
        # print("\tn_cols: " + str(n_cols) + "\n\tn_zeros: " + str(n_zeros) + "\n\tlabel: " + str(label) + "\n\trow: " + str(row) + "\n\trow_index: " + str(row_index))
        return 0
        
def copy_grid(grid_a) :
    # print("grid_a: " + str(grid_a))
    res = []
    for r in range(0, len(grid_a)) :
        if type(grid_a[r]) is list :
            res_row = []
            # print("\tgrid_a["+str(r)+"]: " + str(grid_a[r]))
            for c in range(0, len(grid_a[r])) :
                res_row.append(grid_a[r][c])
        else :
            res_row = grid_a[r]
        res.append(res_row)
    # print("COPIED RES: " + str(res)) # + str(Grid("COPIED: ", res)))
    return res

def print_grid(grid, line=None) :
    if line :
        res = line
    else :
        res = "\n"
    for row in grid :
        res += "\t" + str(row) + "\n"
    return res
    
g = [   [0, 1, 2]]

h = [   [0],
        [1],
        [2]]
        
i = [   [0, -1, 0, 0, 0],
        [1, -6, 0, 0, 0],
        [2, 15, 16, 17, 48]]
        
j = [   [5, 1, 0, 155],
        [2, 5, 1, 22],
        [0, 4, 3, 35],
        [3, 3, 2, 171]]
j_solns =   [[397],
            [295],
            [244],
            [451]]
        
k = [   [5, 1, 0, 155],
        [2, 5, 1, 22],
        [0, 4, 3, 35],
        [3, 3, 2, 171],
        [0, 8, 3, 30]] 
k_solns =   [[397],
            [295],
            [244],
            [451],
            [367]]
        
l = [   [(5 / (4 * 2**0.5)), (-3 / (4 * 2**0.5)), 0],
        [(3 / (4 * 2**0.5)), (5 / (4 * 2**0.5)), 0],
        [(6 / 4), (6 / 4), -1]] 
l_solns =   [[0],
            [500],
            [0]]
        
# print(copy_grid(g))
# print(copy_grid(h))
# print(copy_grid(i))

# matrix_g = Matrix(g)
# print(str(matrix_g))
# matrix_g.solve_diagonally_dominant()
# print(print_grid(matrix_g.diagonally_dominant_matrix, "\n\tDIAGONALLY DOMINANT\n"))

# matrix_h = Matrix(h)
# print(str(matrix_h))
# matrix_h.solve_diagonally_dominant()
# print(print_grid(matrix_h.diagonally_dominant_matrix, "\n\tDIAGONALLY DOMINANT\n"))

# matrix_i = Matrix(i)
# print(str(matrix_i))
# matrix_i.solve_diagonally_dominant()
# print(print_grid(matrix_i.diagonally_dominant_matrix, "\n\tDIAGONALLY DOMINANT\n"))


# matrix_j = Matrix(j, j_solns)
# print(str(matrix_j))
# matrix_j.print_solved_system()

# matrix_k = Matrix(k, k_solns)
# print(str(matrix_k))
# matrix_k.print_solved_system()

matrix_l = Matrix(l, l_solns)
print(str(matrix_l))
matrix_l.print_solved_system()
grid_1 = [[5,3,0,0,7,0,0,0,0],
        [6,0,0,1,9,5,0,0,0],
        [0,9,8,0,0,0,0,6,0],
        [8,0,0,0,6,0,0,0,3],
        [4,0,0,8,0,3,0,0,1],
        [7,0,0,0,2,0,0,0,6],
        [0,6,0,0,0,0,2,8,0],
        [0,0,0,4,1,9,0,0,5],
        [0,0,0,0,8,0,0,7,9]]
		
grid_2 = [[2,9,5,7,4,3,8,6,1],
		  [4,3,1,8,6,5,9,0,0],
		  [8,7,6,1,9,2,5,4,3],
		  [3,8,7,4,5,9,2,1,6],
		  [6,1,2,3,8,7,4,9,5],
		  [5,4,9,2,1,6,7,3,8],
		  [7,6,3,5,2,4,1,8,9],
		  [9,2,8,6,7,1,3,5,4],
		  [1,5,4,9,3,8,6,0,0]]
		  
grid_3 = [[8,4,3,0,0,0,0,0,5],
		  [0,1,6,4,2,5,0,0,0],
		  [0,5,0,0,0,0,0,6,0],
		  [0,0,2,0,1,8,0,4,0],
		  [7,8,4,5,0,3,6,1,2],
		  [0,9,0,2,6,0,8,0,0],
		  [0,2,0,0,0,0,0,5,0],
		  [0,0,0,8,4,2,1,3,0],
		  [6,0,0,0,0,0,9,2,4]]
        
count = 0

class Grid :
    
    def __init__(self, idString, gridIn) :
        self.idString = idString
        self.grid = gridIn
        
    def __repr__(self) :
        border = "_______________"
        string = "\n\n\tBoard: " + str(self.idString) 
        string += "\n\n\t" + border + "\n"
        i = 0
        for row in self.grid :
            string += "\t"
            for n in range(0, len(row), 3) :
                string += "|" + str(row[n]) + str(row[n + 1]) + str(row[n + 2]) + "|"
            i += 1
            if (i % 3) == 0 :
                string += "\n\t" + border
            string += "\n"
        return string + "\n"
        
class Sudoku :
    
    def __init__(self, idString, grid) :
        self.idString = idString
        self.found_solution = False
        self.grid_solution = None
        self.grid = grid
        
    def __repr__(self) :
        string = "\n\t" + str(Grid(self.get_idString(), self.get_grid()))
        soln = "UNKOWN" if not self.grid_solution else str(Grid("solution " + self.get_idString(), self.get_grid_solution()))
        string += "\n\n\tsolution: " + soln
        return string
        
    def get_grid(self) :
        return self.grid
    
    def get_grid_solution(self) :
        return self.grid_solution

    def set_grid(self, gridIn) :
         self.grid = gridIn
		 
    def get_idString(self) :
        return self.idString
        
    def possible_moves(self, grid, y, x) :
        return [i for i in range(1, 10) if self.valid_move(grid, y, x, i)]
        
    def valid_move(self, grid, y, x, n, p=False) :
        if p :
            print("Trying " + str(n) + " at (" + str(y) + ", " + str(x) + ")")
        if n in grid[y] :
            if p :
                print("found in row")
            return False
        for idx in range(0, len(grid)) :
            if grid[idx][x] == n :
                if p :
                    print("found in column")
                return False
            if (idx % 3) == 1:
                u = idx - 1
                d = idx + 1
                l = idx - 1
                r = idx + 1
                if (y in range(u, d + 1)) and (x in range(l, r + 1)) :
                    square = [grid[u][l], grid[u][idx], grid[u][r],
                              grid[idx][l], grid[idx][idx], grid[idx][r],
                              grid[d][l], grid[d][idx], grid[d][r]]
                    if p :
                        print("\tidx: " + str(idx) + "\tu: " + str(u) + "\td: " + str(d) + "\tl: " + str(l) + "\tr: " + str(r))
                        print("square about: (" + str(idx) + ", " + str(idx) + "): " + str(square))
                    if n in square :
                        if p :
                            print("found in square")
                        return False
        return True
        
    def solve_one_wave(self, grid) :
        new_grid = []
        for r in range(len(grid)) :
            new_row = []
            for c in range(len(grid[r])) :
                if grid[r][c] == 0 :
                    possible = self.possible_moves(grid, r, c)
                else :
                    possible = []
                # print("grid["+str(r)+"]["+str(c)+"]: " + str(possible))
                if len(possible) == 1 and grid[r][c] == 0:
                    print("placing " + str(possible[0]) + " at (" + str(r) + ", " + str(c) + ")")
                    new_row.append(possible[0])
                else :
                    new_row.append(grid[r][c])
            new_grid.append(new_row)
        return new_grid
        
    def solve_multiple_waves(self, grid) :
        solve = True
        waves = 1
        curr_grid = grid
        while solve :
            solved_grid = self.solve_one_wave(curr_grid)
            different = False
            for r in range(len(solved_grid)) :
                for c in range(len(solved_grid)) :
                    if solved_grid[r][c] != curr_grid[r][c] :
                        different == True
            if different :
                curr_grid = solved_grid
            else :
                solve = False
            waves += 1
        print("solved " + str(waves) + " wave(s).")
        return curr_grid
        
    def first_level_solve(self, grid) :
        return self.solve_multiple_waves(grid)
        
    def get_working_index(self, grid, offset) :
        o = 0
        for r in range(0, len(grid)) :
            for c in range(0, len(grid[r])) :
                if grid[r][c] == 0 :
                    if o >= offset :
                        return (r, c)
                    else :
                        o += 1
        return (-1, -1)
        
    def check_same(self, grid_a, grid_b) :
        for r in range(0, len(grid_a)) :
            for c in range(0, len(grid_a[r])) :
                if grid_a[r][c] != grid_b[r][c] :
                    return False
        return True
        
    def copy_grid(self, grid_a) :
        res = []
        for r in range(0, len(grid_a)) :
            res_row = []
            for c in range(0, len(grid_a[r])) :
                res_row.append(grid_a[r][c])
            res.append(res_row)
        # print("COPIED RES: " + str(Grid("COPIED: ", res)))
        return res
		
    def is_solved(self, grid) :
        return not self.unsolved(grid)
        
    def unsolved(self, grid) :
        for r in range(0, len(grid)) :
            for c in range(0, len(grid[r])) :
                if grid[r][c] == 0 :
                    return True
        return False
        
    # def solve(self, grid) :
    #     sol = True
    #     self.first_level_solve(grid)
    #     curr_grid = grid
    #     solved_grid = curr_grid
    #     offset = 0
    #     untouched = True
    #     while sol :
    #         y, x = self.get_working_index(grid, offset)
    #         if y == -1 and x == -1 :
    #             sol = False
    #             print("offset: " + str(offset))
    #             break
    #         possible = self.possible_moves(grid, y, x)
    #         print("possible moves (" + str(y) + ", " + str(x) + "): " + str(possible))
    #         for n in possible :
    #             curr_grid[y][x] = n
    #             print("Trying " + str(n) + " at (" + str(y) + ", " + str(x) + ")")
    #             b = False
    #             while b :
    #                 solved_grid = self.first_level_solve(curr_grid)
    #                 if self.check_same(curr_grid, solved_grid) :
    #                     untouched = False
    #                     break
    #                 else :
    #                     curr_grid = solved_grid
    #                 b = self.unsolved(curr_grid)
    #             if not b :
    #                 print("backtracking n: " + str(n) + ", at (" + str(y) + ", " + str(x) + ")")
    #                 curr_grid[y][x] = 0
    #             else :
    #                 print("solved!")
    #                 sol = False
    #                 break
    #         if untouched :
    #             offset += 1
    #             untouched = True
	
    def solve_and_save(self, p=False) :
        self.solve(self.grid, p)
	
	# recursive solve function, also sets the objects grid_solution.
    def solve(self, grid, p=False) :
        # global count
        # count += 1
        # print("called: " + str(count))
        if not self.found_solution :
            for y in range(9) :
                for x in range(9) :
                    if grid[y][x] == 0 :
                        for n in range(1, 10) :
                            if self.valid_move(grid, y, x, n, p) :
                                #print("Trying n: " + str(n) + ", at (" + str(y) + ", " + str(x) + ")")
                                grid[y][x] = n
                                self.solve(grid, p)
                                grid[y][x] = 0
                        #print("early exit grid: " + str(Grid("early exit: ", grid)))
                        return # grid if self.is_solved(grid) else None
            print("solved grid: " + str(Grid("solved grid", grid)))
            self.grid_solution = self.copy_grid(grid)
            self.found_solution = True
            return
        #return grid
    
'''	
    def solve(self, grid) :
        # if not self.unsolved(grid) :
        #     return grid
        # else :
        # print("grid: " + str(Grid("solving:", grid)))
        y, x = self.get_working_index(grid, 0)
        if y < 0 and x < 0 :
            print("BASE: " + str(Grid("Base grid:", grid)))
            return grid
        possibilities = self.possible_moves(grid, y, x)
        for p in possibilities :
            print("Trying " + str(p) + " at (" + str(y) + ", " + str(x) + ")")
            grid[y][x] = p
            grid = self.solve(self.copy_grid(grid))
            if self.unsolved(grid) :
                self.solve(grid)
            else :
                return grid
        return grid
            #grid[y][x] = 0
            #print("backtracking")
'''     

        
# print(Grid("grid 1", grid_1))
# sudoku_1.solve_one_wave()

sudoku_1 = Sudoku("Sudoku 1", grid_1)
sudoku_1.solve_and_save()
print(sudoku_1)

sudoku_2 = Sudoku("Sudoku 2", grid_2)
sudoku_2.solve_and_save()
print(sudoku_2)

sudoku_3 = Sudoku("Sudoku 3", grid_3)
sudoku_3.solve_and_save()
print(sudoku_3)

#print(sudoku_1.valid_move(sudoku_1.get_grid(), 0, 2, 1, False))
#print(sudoku_1.valid_move(sudoku_1.get_grid(), 0, 2, 2, False))
#print(sudoku_1.valid_move(sudoku_1.get_grid(), 0, 2, 3, False))
#print(sudoku_1.valid_move(sudoku_1.get_grid(), 0, 2, 4, False))
#print(sudoku_1.valid_move(sudoku_1.get_grid(), 0, 2, 5, False))
#print(sudoku_1.valid_move(sudoku_1.get_grid(), 0, 2, 6, False))
#print(sudoku_1.valid_move(sudoku_1.get_grid(), 0, 2, 7, False))
#print(sudoku_1.valid_move(sudoku_1.get_grid(), 0, 2, 8, False))
#print(sudoku_1.valid_move(sudoku_1.get_grid(), 0, 2, 9, False))
#print("possible moves: " + str(sudoku_1.possible_moves(sudoku_1.get_grid(), 0, 2)))            
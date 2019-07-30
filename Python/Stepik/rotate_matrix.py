# put your python code here

def get_matrix(dims):
    rows = dims[0]
    cols = dims[1]
    matrix = []
    for i in range(rows):
        inp = input().strip()
        row = str(inp).split(' ')
        if '' in row:
            raise ValueError('{' + str(inp) + '}\n' + str(row_lst))
        row_nums = [int(x) for x in row]
        matrix.append(row_nums)
    return matrix

def rotate_clockwise(matrix):
    n = len(matrix)
    m = len(matrix[n])
    new_matrix = []
    for row in range(n - 1, -1, -1):
        for col in range(m - 1, -1, -1):
            new_matrix.append(matrix[row][col])
            
    
dims = input().split(' ')
matrix = get_matrix(dims)

matrix_at_90_deg = rotate_clockwise(matrix)

print(matrix_at_90_deg)

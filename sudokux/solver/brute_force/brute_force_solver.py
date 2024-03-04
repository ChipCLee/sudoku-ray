class BruteForceSolver:
    M=9
    def __init__(self, grid) -> None:
        self.init(grid)

    def init(self, grid):
        self.grid = grid

    def print_puzzle(self):
        for i in range(BruteForceSolver.M):
            for j in range(BruteForceSolver.M):
                # print("i={},j={}".format(i,j))
                print(self.grid[i][j],end = " ")
            print()
    def check(self,row, col, num):
        for x in range(9):
            if self.grid[row][x] == str(num):
                return False
                
        for x in range(9):
            if self.grid[x][col] == str(num):
                return False
    
    
        startRow = row - row % 3
        startCol = col - col % 3
        for i in range(3):
            for j in range(3):
                if self.grid[i + startRow][j + startCol] == str(num):
                    return False
        return True
    def solve(self, row=0, col=0):
    
        if (row == BruteForceSolver.M - 1 and col == BruteForceSolver.M):
            return True
        if col == BruteForceSolver.M:
            row += 1
            col = 0

        # print("row: {}, col: {}".format(row, col))
        if self.grid[row][col] != '0':
            return self.solve(row, col + 1)
        for num in range(1, BruteForceSolver.M + 1, 1): 
        
            if self.check( row, col, num):
            
                self.grid[row][col] = str(num)
                if self.solve(row, col + 1):
                    return True
            self.grid[row][col] = '0'
        return False
 
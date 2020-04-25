__author__ = 'Jie'
"""
37. Sudoku Solver
Hard

Write a program to solve a Sudoku puzzle by filling the empty cells.

A sudoku solution must satisfy all of the following rules:
Each of the digits 1-9 must occur exactly once in each row.
Each of the digits 1-9 must occur exactly once in each column.
Each of the the digits 1-9 must occur exactly once in each of the 9 3x3 sub-boxes of the grid.
Empty cells are indicated by the character '.'.

Note:
The given board contain only digits 1-9 and the character '.'.
You may assume that the given Sudoku puzzle will have a single unique solution.
The given board size is always 9x9.
"""
class Solution:
    def solveSudoku(self, board) -> None:
        """
        Do not return anything, modify board in-place instead.
        """
        ##### use the backTracking algothrim, a kind of recursive
        # 1) pick empty
        # 2) try all the numbers 1-9
        # 3) find one that works
        # 4) repeat and backtracing
        # print (board)
        find=self.find_empty(board)
        if not find:
            return True
        else:
            row,col=find
        for i in range(1,10):
            i=str(i)
            if self.valid(board,i,(row,col)):
                board[row][col]=i
                if self.solveSudoku(board):
                    return True
                board[row][col]="."
        return False

    def valid(self,bo,num,pos):
        # check if the board array can be a real sudoku
        # check the row
        # bo is the board array, num is the insert number, and pos is the insert index, (i,j)
        for i in range(len(bo[0])):
            # along each column
            if bo[pos[0]][i]==num and pos[1]!=i:
                #here num should be a string
                return False
        # check the column
        for j in range(len(bo)):
            # along each row
            if bo[j][pos[1]]==num and pos[0]!=j:
                return False
        # check the squre box
        box_x=pos[1]//3  # the column of box number
        box_y=pos[0]//3  # the row of box number
        for i in range(box_y*3,box_y*3+3):
            for j in range(box_x*3,box_x*3+3):
                if bo[i][j]==num and pos!=(i,j):
                    return False
        return True

    def print_board(self,bo):
        ## output the input matrix
        for i in range(len(bo)):
            # every 3 rows, output a _ mark
            if i%3==0 and i!=0:
                print ("- - - - - - - - - - -")
            for j in range(len(bo[0])):
                # every 3 columns, output a | mark
                if j%3==0 and j!=0:
                    # the "end=" means output data followed by nothing, instead of the default "/N".
                    print ("|",end="")
                if j==8:
                    # every row after 9 elements, change to another line
                    print (bo[i][j])
                else:
                    print (str(bo[i][j])+" ",end="")
    def find_empty(self,bo):
        for i in range(len(bo)):
            for j in range(len(bo[0])):
                if bo[i][j]== ".":
                    return (i,j)  # row, column
        return None

    def str_int(self,bo):
        pass

solution=Solution()
board=[["5","3",".",".","7",".",".",".","."],
       ["6",".",".","1","9","5",".",".","."],
       [".","9","8",".",".",".",".","6","."],
       ["8",".",".",".","6",".",".",".","3"],
       ["4",".",".","8",".","3",".",".","1"],
       ["7",".",".",".","2",".",".",".","6"],
       [".","6",".",".",".",".","2","8","."],
       [".",".",".","4","1","9",".",".","5"],
       [".",".",".",".","8",".",".","7","9"]]

# board=[[5,3,0,0,7,0,0,0,0],
#        [6,0,0,1,9,5,0,0,0],
#        [0,9,8,0,0,0,0,6,0],
#        [8,0,0,0,6,0,0,0,3],
#        [4,0,0,8,0,3,0,0,1],
#        [7,0,0,0,2,0,0,0,6],
#        [0,6,0,0,0,0,2,8,0],
#        [0,0,0,4,1,9,0,0,5],
#        [0,0,0,0,8,0,0,7,9]]

print_b=solution.print_board(board)
print ("-------------------")
solution.solveSudoku(board)
print_b1=solution.print_board(board)


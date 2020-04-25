__author__ = 'Jie'
"""
36. Valid Sudoku
Medium

Determine if a 9x9 Sudoku board is valid. Only the filled cells need to be validated according to the following rules:
Each row must contain the digits 1-9 without repetition.
Each column must contain the digits 1-9 without repetition.
Each of the 9 3x3 sub-boxes of the grid must contain the digits 1-9 without repetition.
The Sudoku board could be partially filled, where empty cells are filled with the character '.'

Example 1:
Input:
[
  ["5","3",".",".","7",".",".",".","."],
  ["6",".",".","1","9","5",".",".","."],
  [".","9","8",".",".",".",".","6","."],
  ["8",".",".",".","6",".",".",".","3"],
  ["4",".",".","8",".","3",".",".","1"],
  ["7",".",".",".","2",".",".",".","6"],
  [".","6",".",".",".",".","2","8","."],
  [".",".",".","4","1","9",".",".","5"],
  [".",".",".",".","8",".",".","7","9"]
]
Output: true
"""
class Solution:
    def isValidSudoku(self, board) -> bool:
        return  self.isValidSquare(board) and self.isValidRow(board) and self.isValidColumn(board)

    def isValidRow(self,board):
        for row in board:
            if not self.isValidUnit(row):
                return False
        return True

    def isValidColumn(self,board):
        for column in zip(*board):
            if not self.isValidUnit(column):
                return False
        return True

    def isValidSquare(self,board):

        for i in (0,3,6):
            for j in (0,3,6):
                # squre_copy=squre_seq.copy()
                squre_copy=[board[x][y] for x in range(i,i+3)  for y in range(j,j+3)]
                # print (squre_copy)
                if not self.isValidUnit(squre_copy):
                    return False
        return True

    def isValidUnit(self,nums):
        nums=[elem for elem in nums if elem != "."]
        if len(nums)==len(set(nums)):
            return True
        else:
            return False
        # return len(set(nums))==len(nums)

solution=Solution()
board=[
  ["5","3",".",".","7",".",".",".","."],
  ["6",".",".","1","9","5",".",".","."],
  [".","9","8",".",".",".",".","6","."],
  ["8",".",".",".","6",".",".",".","3"],
  ["4",".",".","8",".","3",".",".","1"],
  ["7",".",".",".","2",".",".",".","6"],
  [".","6",".",".",".",".","2","8","."],
  [".",".",".","4","1","9",".",".","5"],
  [".",".",".",".","8",".",".","7","9"]
]
ans=solution.isValidSudoku(board)
print (ans)


# lists=[(1, 2, 3), (4, 5, 6)]
# print (lists[0])
# print (list(zip(*lists)))
# matrix=[[1,2,3],[4,5,6],[7,8,9]]
#
# squre=[matrix[x][y] for x in range(3) for y in range(3)]
# print (squre)
# print (len(set(squre)))
import sys          #just used for the .exc_info() function for reading our error messages
from matrix import Matrix

class Connect4Game():

    def __init__(self):
        self.board = Matrix([['-', '-', '-', '-', '-', '-'],['-', '-', '-', '-', '-', '-'],['-', '-', '-', '-', '-', '-'],['-', '-', '-', '-', '-', '-'],['-', '-', '-', '-', '-', '-'],['-', '-', '-', '-', '-', '-']])
        self.playerSymbols = ['X','O']                          
        self.turn = 0                                                           #used for the AI players to tell if it is their turn
        self.winner = None                                                      #once this is set, the game is over, also it holds the result of the match
        self.numMoves = 0                                                       #if numMoves == 36 and no winner than the game is a draw as the board is filled
        
    def makeMove(self, column):                                                 #enter in a column number and this function goes about determining which row that piece will go then updates the board
        if self.winner != None:
            raise ValueError("Game is already over, player %d won" % (self.winner + 1))     #throw an error if the game is over
        if column > 5 or column < 0 or not isinstance(column, int):                         #just checking for valid plays
            raise ValueError('Invalid move: %d by player %d' % (column, self.turn))
        self.numMoves += 1                                                                  #keeping track of moves, incase of a draw scenario
        openCol = False                                                                     #used to check if the column is too full to play, will be set true if an open row is found
        for i, row in enumerate(list(reversed(self.board))):                                              #here we both check if the column is open and what row the piece would fall in
            if row[column] == '-':
                openCol = True
                row[column] = self.playerSymbols[self.turn]                                 #updating the board
                row = 5 - i                                              #keeping track of the row for when we check if that move won the game
                break
            
        if not openCol:                                                                     #if the column is full, raise an error
            raise ValueError('Invalid move %d by player %d, not an open column' % (column, self.turn))
                 
        gameOver = self.checkWin(row, column)                                               #checking for a win, returns true if so
        if gameOver:                                                                        #set winner to the current players turn
            self.winner = self.turn 
        elif self.numMoves == 36:                                                           #if no win and the moves is 36 than we have a draw
            self.winner = "DRAW"    
        self.turn = int(not self.turn)                                                      #just switching our turn, if it is 0 it becomes 1 and vice versa
        

    def checkHorizontal(self, row, column):                                                 #checks for a horizontal group of 4, returns true if found
        sym = self.board[row][column]
        if column > 2:                                                              #checking three to the left, if the column isnt farther than three from the edge, this cant happen
            if self.board[row][column - 1] == sym and self.board[row][column - 2] == sym and self.board[row][column - 3] == sym:
                return True
        else:                                                                       #checking three to the right, if the above statement isn't true than we can assume its within the first three columns and can safely check three on the right
            if self.board[row][column + 1] == sym and self.board[row][column + 2] == sym and self.board[row][column + 3] == sym:
                return True

        if column > 2 and column < 5:                                               #checking two left one right, column must farther than two from the edge and not the final column for this to work
            if self.board[row][column - 1] == sym and self.board[row][column - 2] == sym and self.board[row][column + 1] == sym:
                return True
        elif column < 4 and column > 0:                                             #checking two right and one left, column must not be the first column and farther than two from the last column for this to work            
            if self.board[row][column + 1] == sym and self.board[row][column + 2] == sym and self.board[row][column - 1] == sym:
                return True
        
        return False    #no wins == False
    
    def checkVertical(self, row, column):                       #checking for a verticl group of 4, returning true if one is found
        sym = self.board[row][column]
        if row < 3:                                 #check 3 below, row = 0 is a the top, so the only way for there to be three below is for row to be less than row 3 as the rows range from 0 to 5
            if self.board[row + 1][column] == sym and self.board[row + 2][column] == sym and self.board[row + 3][column] == sym:
                return True
        
        return False   #three below is the only win condition as you cant place a peice in the middle of a stack or on bottom of a stack
        
    def checkDiagnols(self, row, column):                   #calls both diagnol functions
        if self.checkLeftDiagnol(row, column):
            return True
        if self.checkRightDiagnol(row, column):
            return True
        return False
    
    def checkRightDiagnol(self, row, column):               #searches for a diagnol group of 4 on the right diagnol
        sym = self.board[row][column]
        if row > 2 and column < 3:                          #up right three, so the column needs to be three away from the end and at least three rows down from the top
            if self.board[row - 1][column + 1] == sym and self.board[row - 2][column + 2] == sym and self.board[row - 3][column + 3] == sym:
                return True
        if row > 1 and row < 5 and column > 0 and column < 4:                   #up right 2 and down left one, so it must be at least two columns away from the edge, and one from the first edge and at least two rows from the top and one up from the bottom
            if self.board[row + 1][column - 1] == sym and self.board[row - 1][column + 1] == sym and self.board[row - 2][column + 2] == sym:
                return True

        if row < 3 and column > 2:                  #down left three, so we must be at least more than three columns from the beginning and more than three rows up from the bottom
            if self.board[row + 1][column - 1] == sym and self.board[row + 2][column - 2] == sym and self.board[row + 3][column - 3] == sym:
                return True

        if row < 4 and row > 0 and column < 5 and column > 1:   #down left two up right one, we must be more than two rows from the start and one away from the end, and two rows from the bottom and one down from the top
            if self.board[row - 1][column + 1] == sym and self.board[row + 1][column - 1] == sym and self.board[row + 2][column - 2] == sym:
                return True
            
        return False
        
    def checkLeftDiagnol(self, row, column):                #searches for a diagnol group of 4 on the left diagnol
        sym = self.board[row][column]

        if row > 2 and column > 2:          #up left 3, virtually identical to above right diagnol just the column requirments are basically switched so check that function
            if self.board[row - 1][column - 1] == sym and self.board[row - 2][column - 2] == sym and self.board[row - 3][column - 3] == sym:
                return True
        if row > 1 and row < 5 and column < 5 and  column > 1:                                             #up left 2, bottom right 1
            if self.board[row + 1][column + 1] == sym and self.board[row - 1][column - 1] == sym and self.board[row - 2][column - 2] == sym:
                return True

        if row < 3 and column < 3:      #down right three
            if self.board[row + 1][column + 1] == sym and self.board[row + 2][column + 2] == sym and self.board[row + 3][column + 3] == sym:
                return True

        if row < 4 and row > 0 and column < 4 and column > 0:               #down right two, up left one
            if self.board[row - 1][column - 1] == sym and self.board[row + 1][column + 1] == sym and self.board[row + 2][column + 2] == sym:
                return True
            
        return False
    
    def checkWin(self, row, column):                                    #calls all our checkXXX functions and returns whether or not the game is won
        if self.checkHorizontal(row, column):
            return True
        if self.checkVertical(row, column):
            return True
        if self.checkDiagnols(row, column):
            return True
        return False
    
    def __str__(self):          #just how the board prints itself, one row at a time then a new line, then numbers under each column that start at 1 not zero for easy of testing 
        boardStr = str(self.board)
        boardStr += '\n'
        for x in range(1,7):
            boardStr += " " + str(x) + "  "
        return boardStr
    
if __name__ == "__main__":              #simple test code for playing the game hotseat or with yourself to test it
    newGame = Connect4Game()
    print(newGame)
    while newGame.winner == None:
            move = int(input('\n>> '))
            newGame.makeMove(move - 1)
            print(newGame)

        
    print(newGame)
##    for x in range(7):
##        if x % 2 == 0:
##            newGame.makeMove(int(x / 2),0)
##        else:
##            newGame.makeMove(int(x / 2),1)
            
    print(newGame)
    print("Winner: Player", newGame.winner)

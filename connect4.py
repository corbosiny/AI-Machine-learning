import sys          #just used for the .exc_info() function for reading our error messages

class Connect4Game():

    playerSymbols = ['X','O']

    def __init__(self):
        self.board = [['-' for x in range(6)] for y in range(6)]                          
        self.turn = 0                                                           #used for the AI players to tell if it is their turn
        self.winner = None                                                      #once this is set, the game is over, also it holds the result of the match
        self.numMoves = 0                                                       #if numMoves == 36 and no winner than the game is a draw as the board is filled
        self.lastMove = []

    
    def makeMove(self, column):                                                 
        self.raiseErrorIfInvalidMove(column)
        self.numMoves += 1
        
        row = 5
        while self.board[row][column] != '-':
            row -= 1

        self.lastMove = [row, column]
        self.board[row][column] = Connect4Game.playerSymbols[self.turn]
        self.winner = self.checkIfGameOver()
        self.turn = int(not self.turn)                                                      
    
    def raiseErrorIfInvalidMove(self, column):
        if self.winner != None:
            raise ValueError("Game is already over, player %d won" % (self.winner + 1))     #throw an error if the game is over

        if column > 5 or column < 0 or not isinstance(column, int):                         #just checking for valid plays
            raise ValueError('Invalid move: %d by player %d' % (column, self.turn))

        if self.board[0][column] != '-':
            raise ValueError('Invalid move %d by player %d, not an open column' % (column, self.turn))

    def checkIfGameOver(self):
        if self.checkWin():
            return self.turn 
        elif self.numMoves == len(self.board) * len(self.board[0]):     
            return "DRAW"
        else:
            return None


    def checkWin(self):                                    #calls all our checkXXX functions and returns whether or not the game is won
        if self.checkHorizontal():
            return True
        if self.checkVertical():
            return True
        if self.checkDiagnols():
            return True
        return False

    def checkHorizontal(self):                                                 
        results = []
        currentColumn = self.lastMove[1]
        if currentColumn < 3:
            results.append(self.checkThreeInARow(0, 1))

        if currentColumn > 2:
            results.append(self.checkThreeInARow(0, -1))

        if currentColumn < 4 and currentColumn != 0:
            results.append(self.checkIfInMiddleOfFour(0, 1))

        if currentColumn > 1 and currentColumn != 5:
            results.append(self.checkIfInMiddleOfFour(0, -1))	

        return max(results)

    
    def checkVertical(self):                       #checking for a verticl group of 4, returning true if one is found
        if self.lastMove[0] > 2:
            return False
        else:
            return self.checkThreeInARow(1, 0)
        

    def checkDiagnols(self):
        return max(self.checkLeftDiagnols(), self.checkRightDiagnols())
    
    def checkRightDiagnols(self):              
        return max(self.checkUpperRightDiagnol(), self.checkLowerRightDiagnol())

    def checkUpperRightDiagnol(self):
        results = [False]
        currentRow, currentColumn = self.lastMove
    
        if currentRow > 2 and currentColumn < 3:
            results.append(self.checkThreeInARow(-1, 1))

        if (currentRow > 1 and currentRow != 5) and (currentColumn < 4 and currentColumn != 0):
            results.append(self.checkIfInMiddleOfFour(-1, 1))
        
        return max(results)

    def checkLowerRightDiagnol(self):
        results = [False]
        currentRow, currentColumn = self.lastMove
        
        if currentRow < 3 and currentColumn < 3:
            results.append(self.checkThreeInARow(1, 1))

        if (currentRow < 4 and currentRow != 0) and (currentColumn < 4 and currentColumn != 0):
            results.append(self.checkIfInMiddleOfFour(1, 1))

        return max(results)
        
    def checkLeftDiagnols(self):                
        return max(self.checkUpperLeftDiagnol(), self.checkLowerLeftDiagnol())

    def checkUpperLeftDiagnol(self):
        results = [False]
        currentRow, currentColumn = self.lastMove
        if currentRow > 2 and currentColumn > 2:
            results.append(self.checkThreeInARow(-1, -1))
            
        if (currentRow > 1 and currentRow != 5) and (currentColumn > 1 and currentColumn != 5):
            results.append(self.checkIfInMiddleOfFour(-1, -1))

        return max(results)
    
    def checkLowerLeftDiagnol(self):
        results = [False]
        currentRow, currentColumn = self.lastMove
        if currentRow < 3 and currentColumn > 2:
            results.append(self.checkThreeInARow(1, -1))

        if (currentRow < 4 and currentRow != 0) and (currentColumn > 1 and currentColumn != 5):
            results.append(self.checkIfInMiddleOfFour(1, -1))
            
        return max(results)


    def checkThreeInARow(self, rowOffset, columnOffset):
        sym = Connect4Game.playerSymbols[self.turn]
        for i in range(1, 4):
            if self.board[self.lastMove[0] + rowOffset * i][self.lastMove[1] + columnOffset * i] != sym:
                print()
                return False
        return True
            
    
    def checkIfInMiddleOfFour(self, rowOffset, columnOffset):
        sym = Connect4Game.playerSymbols[self.turn]
        for i in range(-1, 3):
            if self.board[self.lastMove[0] + rowOffset * i][self.lastMove[1] + columnOffset * i] != sym:
                return False
        return True
    
    
    
    def __str__(self):         
        boardStr = ''
        for row in self.board:
            boardStr += str(row)
            boardStr += '\n'
        boardStr += "[ 1    2    3    4    5    6 ]"
        return boardStr
    
if __name__ == "__main__":              #simple test code for playing the game hotseat or with yourself to test it
    newGame = Connect4Game()
    print(newGame)
    while newGame.winner == None:
            move = int(input('\n>> '))
            newGame.makeMove(move - 1)
            print(newGame)

            
    print(newGame)
    print("Winner: Player", newGame.winner)

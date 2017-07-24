import sys
import connect4PlayerRandom

class Connect4Game():

    playerSymbols = ['X','O']

    def __init__(self, viewGame = False):
        self.players = []
        self.prepareForNewGame()
        self.viewGame = viewGame 
        
    def prepareForNewGame(self):
        self.waitForPlayersToLeaveGame()
        self.clearBoard()
        self.resetPlayers()
        self.turn = 0
        self.numMoves = 0
        self.lastMove = []
        self.winner = None

    def waitForPlayersToLeaveGame(self):
        for player in self.players:
            if player.game is self:
                self.waitForPlayerToLeaveGame(player)

    def waitForPlayerToLeaveGame(self, player):
        if self.isHumanPlayer(player):
            pass
        
        self.turn = player.playerNum
        while player.game is self:
            pass

    def isHumanPlayer(self, player):
        return isinstance(player, str)
    
    def resetPlayers(self):
        self.numPlayers = 0
        self.players = []
                  

    def addPlayer(self, player):
        playerNumber = self.numPlayers
        playerSymbol = Connect4Game.playerSymbols[playerNumber]
        self.players.append(player)
        self.numPlayers += 1
        return playerNumber, playerSymbol
    
    def makeMove(self, column):
        if self.checkIfInvalidMove(column):
            return
        
        row = self.calculateLastMovesRow(column)
        self.board[row][column] = Connect4Game.playerSymbols[self.turn]
        self.lastMove = [row, column]

        self.updateGameState()
        self.displayBoard()

    
    def checkIfInvalidMove(self, column):
        if self.winner != None:
            print("Game is already over, player %d won" % (self.winner + 1))     
            return True

        if column > 5 or column < 0 or not isinstance(column, int):                     
            print('Invalid move: %d by player %d' % (column, self.turn))
            return True

        if self.board[0][column] != '-':
            print('Invalid move %d by player %d, not an open column' % (column, self.turn))
            return True
        
        return False

    def calculateLastMovesRow(self, column):
        row = 5
        while self.board[row][column] != '-':
            row -= 1
        return row
        

    def updateGameState(self):
        self.numMoves += 1
        self.winner = self.checkIfGameOver()
        self.turn = int(not self.turn)


    def checkIfGameOver(self):
        if self.checkWin():
            self.awardPlayerTheWin(self.turn)
            return self.turn 
        elif self.numMoves == len(self.board) * len(self.board[0]):     
            return "DRAW"
        else:
            return None

    def awardPlayerTheWin(self, playerNum):
        try:
            self.players[playerNum].wins += 1
        except:             #will trigger for human players
            pass

    def checkWin(self):                                    
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

    
    def checkVertical(self):                       
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
    
    def clearBoard(self):
        self.board = [['-' for x in range(6)] for y in range(6)]


    def displayBoard(self):
        if self.viewGame:
            print(self)
            if self.winner != None:
                print("\n\nWinner: Player %d\n" % self.winner)

    def gameIsNotOver(self):
        return self.winner == None
    
    def __str__(self):         
        boardStr = ''
        for row in self.board:
            boardStr += str(row)
            boardStr += '\n'
        boardStr += "[ 1    2    3    4    5    6 ]\n\n"
        return boardStr
    
if __name__ == "__main__":              
    newGame = Connect4Game(True)

##    print(newGame)                            #uncomment for hotset game test
##    while newGame.winner == None:
##            move = int(input('\n>> '))
##            newGame.makeMove(move - 1)
##            print(newGame)

    AIplayer = connect4PlayerRandom.Connect4PlayerRandom()      #uncomment to play against random AI

    while True:
        newGame.displayBoard()
        newGame.addPlayer("Corey")
        AIplayer.joinNewGame(newGame)

        while newGame.winner == None:
            while newGame.turn != 0:
                pass
            move = int(input('\n>> '))
            newGame.makeMove(move - 1)
        
        print("Winner: Player", newGame.winner)
        newGame.prepareForNewGame()
    

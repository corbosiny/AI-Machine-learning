import connect4 #Only for testing purposes
import random
import math
import numpy
from connect4HumanPlayer import Connect4HumanPlayer
from connect4PlayerShell import Connect4PlayerShell

class Connect4ProbabilityPlayer(Connect4PlayerShell):

    URGENT_MOVE_SCORE = -1

    def __init__(self, playerID):
        self.numberOfMyPieces = 0
        self.numberOfOpponentPieces = 0
        super(Connect4ProbabilityPlayer, self).__init__(playerID)

    def generateMove(self, board):
        self.board = board
        self.boardLength = board.boardLength
        self.boardHeight = board.boardHeight
        self.openColumns = self.determineOpenColumns()
        self.correspondingRows = self.determineOpenRows()

        movesAndScores = self.calculateMoveScores()
        movesAndProbs = self.convertScoresToProbability(movesAndScores)

        if isinstance(movesAndProbs, int):     #if urgent move detected, only an int of that move will be returned
            return movesAndProbs
        else:
            return self.makeWeightedRandomChoice(movesAndProbs)


    def determineOpenColumns(self):
        openColumns = []
        for column in range(self.boardLength):
            if self.board[0][column] == '-':
                openColumns.append(column)

        return openColumns


    def determineOpenRows(self):
        openRows = []
        for column in self.openColumns:
            openRows.append(self.determineOpenRow(column))

        return openRows

    def determineOpenRow(self, columnOfMove):
        rowNumber = self.boardHeight - 1
        while self.board[rowNumber][columnOfMove] != '-':
            rowNumber -= 1
        return rowNumber

    

    def calculateMoveScores(self):
        moveScores = []
        for possibleMove in zip(self.openColumns, self.correspondingRows):
            self.possibleMove = possibleMove
            if self.isWinningMove(self.playerSymbol) or self.isWinningMoveForOpponent():
                moveScores.append(Connect4ProbabilityPlayer.URGENT_MOVE_SCORE)
            else:
                self.possibleMove = possibleMove
                numberOfMyPieces, numberOfOpponentPieces = self.countPiecesAroundSpot()
                moveScore = self.calculateMoveScore(numberOfMyPieces, numberOfOpponentPieces)
                moveScores.append(moveScore)

        return list(zip(self.openColumns, moveScores))

    def isWinningMove(self, symbol):
        actualLastMove = [coordinate for coordinate in self.board.lastMove]
        columnOfMove, rowOfMove = self.possibleMove
        
        self.board.lastMove = [rowOfMove, columnOfMove]
        self.board.rows[rowOfMove][columnOfMove] = symbol
        
        isWinningMove = self.board.checkWin()
        
        self.board.rows[rowOfMove][columnOfMove] = '-'
        self.board.lastMove = actualLastMove
        return isWinningMove

    def isWinningMoveForOpponent(self):
        allSymbols = [symbol for symbol in connect4.Connect4Game.playerSymbols]
        allSymbols.remove(self.playerSymbol)
        opponentSymbol = allSymbols[0]
        return self.isWinningMove(opponentSymbol)

    def countPiecesAroundSpot(self):
        piecesCount = numpy.array([0, 0]) 
        piecesCount += self.countPiecesInRow()
        piecesCount += self.countPiecesInColumn()
        piecesCount += self.countPiecesInDiagnols()
        return piecesCount
        
    def countPiecesInRow(self):
        rowPieceCount = self.countPiecesGivenRowAndColumnOffsets(0, 1)
        rowPieceCount += self.countPiecesGivenRowAndColumnOffsets(0, -1)
        return rowPieceCount

    
    def countPiecesInColumn(self):
        columnPieceCount = self.countPiecesGivenRowAndColumnOffsets(1, 0)
        columnPieceCount += self.countPiecesGivenRowAndColumnOffsets(-1, 0)
        return columnPieceCount

        
    def countPiecesInDiagnols(self):
        leftDiagnolCount = self.countPiecesInLeftDiagnol()
        rightDiagnolCount = self.countPiecesInRightDiagnol()
        return leftDiagnolCount + rightDiagnolCount

    def countPiecesInLeftDiagnol(self):
        leftDiagnolCount = self.countPiecesGivenRowAndColumnOffsets(-1, -1)
        leftDiagnolCount += self.countPiecesGivenRowAndColumnOffsets(1, 1)
        return leftDiagnolCount


    def countPiecesInRightDiagnol(self):
        rightDiagnolCount = self.countPiecesGivenRowAndColumnOffsets(1, -1)
        rightDiagnolCount += self.countPiecesGivenRowAndColumnOffsets(-1, 1)
        return rightDiagnolCount

    def countPiecesGivenRowAndColumnOffsets(self, rowOffset, columnOffset):
        columnOfMove, rowOfMove = self.possibleMove
        columnAdjust, rowAdjust = 0, 0

        while self.withinBounds(rowOfMove + rowAdjust, columnOfMove + columnAdjust) and (abs(columnAdjust) < 3 and abs(rowAdjust) < 3):  
            self.countPieces(piece = self.board[rowOfMove + rowAdjust][columnOfMove + columnAdjust])
            rowAdjust += rowOffset
            columnAdjust += columnOffset

        return self.countPieces(doneCounting = True)


    def withinBounds(self, row, column):
        if row >= 0 and row <= self.boardHeight - 1:
            if column >= 0 and column <= self.boardLength - 1:
                return True

        return False


    def countPieces(self, piece= None, doneCounting = False):
        if doneCounting:
            countOfPieces = numpy.array([self.numberOfMyPieces, self.numberOfOpponentPieces])
            self.numberOfMyPieces, self.numberOfOpponentPieces = 0, 0
            return countOfPieces

        if piece is self.playerSymbol:
            self.numberOfMyPieces += 1
        elif piece is not connect4.Connect4Game.emptySpotSymbol:
            self.numberOfOpponentPieces += 1


    
    def calculateMoveScore(self, numberOfMyPieces, numberOfOpponentPieces):
        return math.exp(numberOfMyPieces -  numberOfOpponentPieces)


    def convertScoresToProbability(self, movesAndScores):
        for move, score in movesAndScores:
            if score == Connect4ProbabilityPlayer.URGENT_MOVE_SCORE:
                return move
            
        moves = [pair[0] for pair in movesAndScores]
        scores = [pair[1] for pair in movesAndScores]
        total = sum(scores)

        probabilities = [score / total for score in scores]
        movesAndProbabilities = list(zip(moves, probabilities))
        return movesAndProbabilities
    

    def makeWeightedRandomChoice(self, movesAndProbs):
        moves, probs = [], []
        for move, prob in movesAndProbs:
            moves.append(move)
            probs.append(prob)
            
        move = numpy.random.choice(moves, p= probs)
        return move


if __name__ == "__main__":
    import connect4PlayerTester
    tester = connect4PlayerTester.PlayerTester(Connect4ProbabilityPlayer)
    assert(tester.testPlayers() == True)
    print("Initial Diagnostics Passed!\n\n")
    
    newGame = connect4.Connect4Game(True)
    newGame.start()

    player1 = Connect4HumanPlayer(1)
    player2 = Connect4ProbabilityPlayer(2)

    while True:
        player1.joinGame(newGame)
        player2.joinGame(newGame)
    
        while newGame.gameIsNotOver():
            pass

        newGame.prepareForNewGame()
        
    print('Winner: %d' % newGame.winner.playerID)

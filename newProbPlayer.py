import connect4
import random
import math
import numpy
from connect4PlayerShell import Connect4PlayerShell

class Connect4ProbabilityPlayer(Connect4PlayerShell):

    URGENT_MOVE_SCORE = -1

    def __init__(self, playerID):
        self.wins = 0
        self.numberOfMyPieces
        super(Connect4ProbabilityPlayer, self).__init__(playerID)

    def generateMove(self, board):
        self.board = board

        self.openColumns = self.determineOpenColumns()
        self.correspondingRows = self.determineOpenRows()

        movesAndScores = self.calculateMoveScores()
        movesAndProbs = self.convertScoresToProbability(movesAndScores)

        if len(movesAndProbs) == 0:     #only happens if an urgent move is detected
            return movesAndProbs[0]
        else:
            return self.makeWeightedRandomChoice(movesAndProbs)


    def determineOpenColumns(self):
        openColumns = []
        for column in range(6):
            if self.board[0][column] == '-':
                openColumns.append(column)

        return openColumns


    def determineOpenRows(self):
        openRows = []
        for column in self.openColumns:
            openRows.append(self.determineOpenRow(column))

        return openRows

    def determineOpenRow(self, columnOfMove):
        rowNumber = 5
        while self.board[rowNumber][columnOfMove] != '-':
            rowNumber -= 1
        return rowNumber

    

    def calculateMoveScores(self):
        moveScores = []
        for possibleMove in zip(self.openColumns, self.correspondingRows):
            if self.isWinningMove(self.possibleMove) or self.isWinningMoveForOpponent(self.possibleMove):
                moveScores.append(Connect4ProbabilityPlayer.URGENT_MOVE_SCORE)
            else:
                self.possibleMove = possibleMove
                numberOfMyPieces, numberOfOpponentPieces = self.countPiecesAroundSpot()
                moveScore = self.calculateMoveScore(numberOfMyPieces, numberOfOpponentPieces)
                moveScores.append(moveScore)

        return zip(self.openColumns, moveScores)


    def isWinningMove(self, potentialMove, symbol = self.playerSymbol):
        actualLastMove = [coordinate for coordinate in self.board.lastMove]
        columnOfMove, rowOfMove = potentialMove
        
        self.board.lastMove = potentialMove
        self.board.rows[rowOfMove][columnOfMove] = symbol
        
        isWinningMove = self.board.checkWin()
        
        self.board.rows[rowOfMove][columnOfMove] = '-'
        self.board.lastMove = actualLastMove
        return isWinningMove

    def isWinningMoveForOpponent(self, possibleMove):
        allSymbols = [symbol for symbol in connect4.Connect4Game.playerSymbols]
        allSymbols.remove(self.playerSymbol)
        opponentSymbol = allSymbols[0]
        return self.isWinningMove(possibleMove, opponentSymbol)

    def countPiecesAroundSpot(self)
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

    def countPiecesInLeftDiagnol(self, possibleMove):
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

        while self.withinBounds(rowOfMove + rowAdjusts, columnOfMove + columnAdjusts):  
            self.countPiece(self.board[rowOfMove + rowAdjust][columnOfMove + columnAdjust])
            rowAdjust += rowOffset
            columnAdjust += columnOffset

        return self.countPieces(True)


    def withinBounds(self, row, column):
        if row >= 0 and row <= 5:
            if column >= 0 and column <= 5:
                return True

        return False


    def countPiece(self, doneCounting = False):
        if doneCounting:
            countOfPieces = numpy.array([self.numberOfMyPieces, self.numberOfOpponentPieces])
            self.numberOfMyPieces, self.numberOfOpponentPieces = 0, 0
            return countOfPieces

        if piece is self.playerSymbol:
            self.numberOfMypieces += 1
        elif piece is not connect4.Connect4Game.emptySpotSymbol:
            self.numberOfOpponentPieces += 1


    
    def calculateMoveScore(self, numberOfMyPieces, numberOfOpponentPieces):
        return math.exp(numberOfMypieces - numberOfOpponentPieces)


    def convertScoresToProbability(movesAndScores):
        for move, score in movesAndScores:
            if score == Connect4ProbabilityPlayer.URGENT_MOVE_SCORE:
                return move
            
        moves = [pair[0] for pair in movesAndScores]
        scores = [pair[1] for pair in movesAndScores]
        total = sum(scores)

        probabilities = [score / total for score in scores]
        movesAndProbabilities = zip(moves, probabilities)
        return movesAndProbabilities
    

    def makeWeightedRandomChoice(self, movesAndProbs):
        moves, probs = [], []
        for move, prob in movesAndProbs:
            moves.append(move)
            probs.append(prob)
            
        move = numpy.random.choice(moves, p= probs)    
        return move


if __name__ == "__main__":
    newGame = connect4.Connect4Game(True)
    #newGame.start()
    
    players = [Connect4ProbabilityPlayer(x) for x in range(2)]
    for player in players:
        player.joinGame(newGame)

    newGame.board[5][0] = "X"
    newGame.board[4][1] = "O"
    newGame.board[5][1] = "O"
    newGame.board[0][5] = "X"
    print(list(players[0].generateMove(newGame.board)))

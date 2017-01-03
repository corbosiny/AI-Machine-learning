import connect4
import threading
import random
import numpy
import time
import connect4PlayerRandom

class Connect4Player(threading.Thread):

    def __init__(self, game, playerNum):
        self.game = game
        self.playerNum = playerNum
        self.wins = 0
        self.sym = self.game.playerSymbols[playerNum]
        super(Connect4Player, self).__init__()

    def makeMove(self, move):
        while self.game.turn != self.playerNum:
            pass
        
        if self.game.winner != None:
            return None
        else:
            self.game.makeMove(move)

    def generateMove(self):
        movesAndProbsRows = self.analyzeRows()
        moves = [x[1] for x in movesAndProbsRows]
        probsRows = [x[0] for x in movesAndProbsRows]
        if -1 in probsRows:
            move = moves[probsRows.index(-1)]
            self.makeMove(move)
            return None
        probsRows = [x / sum(probsRows) for x in probsRows]

        movesAndProbsCol = self.analyzeColumns()
        probsCol = [x[0] for x in movesAndProbsCol]
        if -1 in probsCol:
            move = moves[probsCol.index(-1)]
            self.makeMove(move)
            return None
        probsCol = [x / sum(probsCol) for x in probsCol]

        movesAndProbsDiag = self.analyzeDiagnols()
        probsDiag = [x[0] for x in movesAndProbsDiag]
        if -1 in probsDiag:
            move = moves[probsDiag.index(-1)]
            self.makeMove(move)
            return None
        probsDiag = [x / sum(probsDiag) for x in probsDiag]        

        probs = [(x + y + z) / 3 for x,y,z in list(zip(probsRows, probsCol, probsDiag))]
        while True:
            prob = random.random()
            move = random.randint(0, 5)
            if prob < probs[move]:
                move = moves[move]
                break
        self.makeMove(move)

    def analyzeRows(self):
        moves = []
        for column in range(6):
            row = 0
            while self.game.board[row][column] == "-" and row < 5:
                row += 1

            if row == 0:
                moveViability = 0
                moves.append([moveViability, column])
                continue 
            elif self.game.board[row][column] != '-':
                row -= 1

            moveViability = 1
            
            if column < 3:
                numMySyms = 0
                numNotMySyms = 0
                for y in range(1, 4):
                    if self.game.board[row][column + y] == self.sym:
                        moveViability *= 2
                        numMySyms += 1
                    elif self.game.board[row][column + y] != self.sym and self.game.board[row][column + y] != '-':
                        moveViability /= 3
                        numNotMySyms += 1
                if numMySyms == 3 or numNotMySyms == 3:
                    moves.append([-1, column])
                    continue

            if column < 4 and column > 0:
                numMySyms = 0
                numNotMySyms = 0
                for y in range(1, 3):
                    if self.game.board[row][column + y] == self.sym:
                        moveViability *= 2
                        numMySyms += 1
                    elif self.game.board[row][column + y] != self.sym and self.game.board[row][column + y] != '-':
                        moveViability /= 3
                        numNotMySyms += 1
                if self.game.board[row][column - 1] == self.sym:
                    moveViability *= 2
                    numMySyms += 1
                elif self.game.board[row][column - 1] != self.sym and self.game.board[row][column - 1] != '-':
                    moveViability /= 3
                    numNotMySyms += 1
                    
                if numMySyms == 3 or numNotMySyms == 3:
                    moves.append([-1, column])
                    continue
                
            if column > 2:
                numMySyms = 0
                numNotMySyms = 0
                for y in range(1, 4):
                    if self.game.board[row][column - y] == self.sym:
                        moveViability *= 2
                        numMySyms += 1
                    elif self.game.board[row][column - y] != self.sym and self.game.board[row][column - y] != '-':
                        moveViability /= 3
                        numNotMySyms += 1
                if numMySyms == 3 or numNotMySyms == 3:
                    moves.append([-1, column])
                    continue
                    
            if column > 1 and column < 5:
                numMySyms = 0
                numNotMySyms = 0
                for y in range(1, 3):
                    if self.game.board[row][column - y] == self.sym:
                        moveViability *= 2
                        numMySyms += 1
                    elif self.game.board[row][column - y] != self.sym and self.game.board[row][column - y] != '-':
                        moveViability /= 3
                        numNotMySyms += 1
                if self.game.board[row][column + 1] == self.sym:
                    moveViability *= 2
                    numMySyms += 1
                elif self.game.board[row][column + 1] != self.sym and self.game.board[row][column + 1] != '-':
                    moveViability /= 3
                    numNotMySyms += 1
                    
                if numMySyms == 3 or numNotMySyms == 3:
                    moves.append([-1, column])
                    continue
            moves.append([moveViability, column])
        return moves
    
    def analyzeColumns(self):
        moves = []
        for column in range(6):
            row = 0
            while self.game.board[row][column] == "-" and row < 5:
                row += 1

            if row == 0:
                moveViability = 0
                moves.append([moveViability, column])
                continue 
            elif self.game.board[row][column] != '-':
                row -= 1

            moveViability = 1
            if row < 5:
                tempRow = row + 1
                numMySyms = 0
                numNotMySyms = 0
                while tempRow < 6 and tempRow < row + 4:
                    if self.game.board[tempRow][column] == self.sym:
                        numMySyms += 1
                        moveViability *= 2
                    elif self.game.board[tempRow][column] != self.sym and self.game.board[tempRow][column] != '-':
                        numNotMySyms += 1
                        moveViability /= 3
                    tempRow += 1

                if numMySyms == 3 or numNotMySyms == 3:
                    moves.append([-1, column])
                else:
                    moves.append([moveViability, column])
            else:
                moves.append([1, column])

        return moves

    def analyzeDiagnols(self):
        movesAndProbs = self.analyzeRightDiagnols()
        movesAndProbs2 = self.analyzeLeftDiagnols()

        moves = [x[1] for x in movesAndProbs]
        
        probs0 = [x[0] for x in movesAndProbs]
        probs2 = [x[0] for x in movesAndProbs2]
        probs = [(x + y) / 2 for x,y in zip(probs0, probs2)]
        moves = [[x,y] for x,y in zip(probs, moves)]
        if -1 in probs0:
            moves[probs0.index(-1)] = [-1, moves[probs0.index(-1)][1]]
        if -1 in probs2:
            moves[probs2.index(-1)] = [-1, moves[probs2.index(-1)][1]]
        return moves
        #movesAndProbsLeft = self.analyzeLeftDiagnols()
        

    def analyzeRightDiagnols(self):
        moves = []
        for column in range(6):
            row = 0
            while self.game.board[row][column] == "-" and row < 5:
                row += 1

            if row == 0:
                moveViability = 0
                moves.append([moveViability, column])
                continue 
            elif self.game.board[row][column] != '-':
                row -= 1


            moveViability = 1
            
            if column < 3 and row > 2:
                numMySyms = 0
                numNotMySyms = 0
                for y in range(1,4):
                    if self.game.board[row - y][column + y] == self.sym:
                        moveViability *= 2
                        numMySyms += 1
                    elif self.game.board[row - y][column + y] != '-':
                        moveViability /= 3
                        numNotMySyms += 1
                        
                if numMySyms == 3 or numNotMySyms == 3:
                    moves.append([-1, column])
                    continue
                
            if column < 4 and column > 0 and row > 1 and row < 5:
                numMySyms = 0
                numNotMySyms = 0
                for y in range(1, 3):
                    if self.game.board[row - y][column + y] == self.sym:
                        moveViability *= 2
                        numMySyms += 1
                    elif self.game.board[row - y][column + y] != '-':
                        moveViability /= 3
                        numNotMySyms += 1

                if self.game.board[row + 1][column - 1] == self.sym:
                    moveViability *= 2
                    numMySyms += 1
                elif self.game.board[row + 1][column - 1] != '-':
                    moveViability /= 3
                    numNotMySyms += 1
                    
                if numMySyms == 3 or numNotMySyms == 3:
                    moves.append([-1, column])
                    continue
                
            if column > 2 and row < 3:
                numMySyms = 0
                numNotMySyms = 0

                for y in range(1, 4):
                    if self.game.board[row + y][column - y] == self.sym:
                        moveViability *= 2
                        numMySyms += 1
                    elif self.game.board[row + y][column - y] != '-':
                        moveViability /= 3
                        numNotMySyms += 1
                
                if numMySyms == 3 or numNotMySyms == 3:
                    moves.append([-1, column])
                    continue
                
            if column > 1 and column < 5 and row < 4 and row > 0:
                numMySyms = 0
                numNotMySyms = 0

                for y in range(1, 3):
                    if self.game.board[row + y][column - y] == self.sym:
                        moveViability *= 2
                        numMySyms += 1
                        
                    elif self.game.board[row + y][column - y] != '-':
                        moveViability /= 3
                        numNotMySyms += 1
                        
                if self.game.board[row - 1][column + 1] == self.sym:
                    moveViability *= 2
                    numMySyms += 1
                elif self.game.board[row][column + 1] != '-':
                    moveViability /= 3
                    numNotMySyms += 1
    
                
                if numMySyms == 3 or numNotMySyms == 3:
                    moves.append([-1, column])
                    continue
                
            moves.append([moveViability, column])
        return moves

    def analyzeLeftDiagnols(self):
        moves = []
        for column in range(6):
            row = 0
            while self.game.board[row][column] == "-" and row < 5:
                row += 1

            if row == 0:
                moveViability = 0
                moves.append([moveViability, column])
                continue 
            elif self.game.board[row][column] != '-':
                row -= 1


            moveViability = 1
            
            if column > 2 and row > 2:
                numMySyms = 0
                numNotMySyms = 0
                for y in range(1,4):
                    if self.game.board[row - y][column - y] == self.sym:
                        moveViability *= 2
                        numMySyms += 1
                    elif self.game.board[row - y][column - y] != '-':
                        moveViability /= 3
                        numNotMySyms += 1
                        
                if numMySyms == 3 or numNotMySyms == 3:
                    moves.append([-1, column])
                    continue
                
            if column > 1 and column < 5 and row > 1 and row < 5:
                numMySyms = 0
                numNotMySyms = 0
                for y in range(1, 3):
                    if self.game.board[row - y][column - y] == self.sym:
                        moveViability *= 2
                        numMySyms += 1
                    elif self.game.board[row - y][column - y] != '-':
                        moveViability /= 3
                        numNotMySyms += 1

                if self.game.board[row + 1][column + 1] == self.sym:
                    moveViability *= 2
                    numMySyms += 1
                elif self.game.board[row + 1][column + 1] != '-':
                    moveViability /= 3
                    numNotMySyms += 1
                    
                if numMySyms == 3 or numNotMySyms == 3:
                    moves.append([-1, column])
                    continue
                
            if column < 3 and row < 3:
                numMySyms = 0
                numNotMySyms = 0

                for y in range(1, 4):
                    if self.game.board[row + y][column + y] == self.sym:
                        moveViability *= 2
                        numMySyms += 1
                    elif self.game.board[row + y][column + y] != '-':
                        moveViability /= 3
                        numNotMySyms += 1
                
                if numMySyms == 3 or numNotMySyms == 3:
                    moves.append([-1, column])
                    continue
                
            if column < 4 and column > 0 and row < 4 and row > 0:
                numMySyms = 0
                numNotMySyms = 0

                for y in range(1, 3):
                    if self.game.board[row + y][column + y] == self.sym:
                        moveViability *= 2
                        numMySyms += 1
                        
                    elif self.game.board[row + y][column + y] != '-':
                        moveViability /= 3
                        numNotMySyms += 1
                        
                if self.game.board[row - 1][column - 1] == self.sym:
                    moveViability *= 2
                    numMySyms += 1
                elif self.game.board[row][column - 1] != '-':
                    moveViability /= 3
                    numNotMySyms += 1
    
                
                if numMySyms == 3 or numNotMySyms == 3:
                    moves.append([-1, column])
                    continue
                
            moves.append([moveViability, column])
        return moves
    
    def run(self):
        while True:
            while self.game.winner == None:
                while self.game.turn != self.playerNum:
                    pass
                self.generateMove()

            if self.game.winner == self.playerNum:
                self.wins += 1        
            self.game = None
            while self.game == None:
                pass
            
if __name__ == "__main__":
    newGame = connect4.Connect4Game()
    player1 = Connect4Player(newGame, 0)
    player2 = connect4PlayerRandom.Connect4PlayerRandom(newGame, 1)
    player1.start()
    player2.start()

    for x in range(100):
        while newGame.winner == None:
            currentTurn = newGame.turn
        try:
            print("Winner: Player %d" % newGame.winner)
        except:
            print("Winner: Player %s" % newGame.winner)
        newGame = connect4.Connect4Game()
        player1.game = newGame
        player2.game = newGame

    print(player1.wins)
##    player1 = Connect4Player(newGame, 0)
##    player1.start()
##    while newGame.winner == None:
##        while newGame.turn == 0:
##            pass
##        time.sleep(.1)
##        print(newGame)
##        move = int(input('\n>>>>'))
##        newGame.makeMove(move)
        

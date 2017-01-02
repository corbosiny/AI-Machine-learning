import connect4
import threading
import random
import numpy
import time
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


        print(probsRows, end = '\n\n')
        print(probsCol, end = '\n\n')
        probs = [(x + y) / 2 for x,y in list(zip(probsRows, probsCol))]
        while True:
            prob = random.random()
            move = random.randint(0, 5)
            if prob < probs[move]:
                move = moves[move]
                break
        print(probs, end = '\n\n')
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

            if row > 5:
                print("Row:", row)
                raise ValueError('testing')
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

            elif column < 4:
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
                elif self.game.board[row][column - y] != self.sym and self.game.board[row][column - y] != '-':
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
                    
            elif column > 1:
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
                elif self.game.board[row][column + y] != self.sym and self.game.board[row][column + y] != '-':
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
        pass
    
    def run(self):
        while self.game.winner == None:
            while self.game.turn != self.playerNum:
                pass
            self.generateMove()

        if self.game.winner == self.playerNum:
            self.wins += 1        
    
if __name__ == "__main__":
    newGame = connect4.Connect4Game()
##    player1 = Connect4Player(newGame, 0)
##    player2 = Connect4Player(newGame, 1)
##    player1.start()
##    player2.start()
##    
##    while newGame.winner == None:
##        pass
##    print("Winner: Player %d" % newGame.winner)
    player1 = Connect4Player(newGame, 0)
    player1.start()
    while newGame.winner == None:
        while newGame.turn == 0:
            pass
        time.sleep(.1)
        move = int(input('\n>>>>'))
        newGame.makeMove(move)
        

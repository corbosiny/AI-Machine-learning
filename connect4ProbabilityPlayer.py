import connect4                                         
import random                                                                                       
import math                                            
from connect4PlayerShell import Connect4PlayerShell


class Connect4ProbabilityPlayer(Connect4PlayerShell):                 

    def __init__(self, playerID):
        self.wins = 0                                   
        super(Connect4ProbabilityPlayer, self).__init__(playerID)

    def generateMove(self, board): #recieves recomendations for moves from analyzing rows, columns, and diganols then averages all their move scores, then picks a move and plays it
        self.board = board
        movesAndProbsRows = self.analyzeRows()          #recieve row recomendations
        moves = [x[1] for x in movesAndProbsRows]
        probsRows = [x[0] for x in movesAndProbsRows] #seperate our moves and their probabilities
        if -1 in probsRows:                           #checking if we have the PLAY NOW flag
            move = moves[probsRows.index(-1)]
            return move
        probsRows = [x / sum(probsRows) for x in probsRows] #turns all scores in probabilties

        movesAndProbsCol = self.analyzeColumns()            #repeat with columns
        probsCol = [x[0] for x in movesAndProbsCol]
        if -1 in probsCol:
            move = moves[probsCol.index(-1)]
            return move
        probsCol = [x / sum(probsCol) for x in probsCol]

        movesAndProbsDiag = self.analyzeDiagnols()          #repeat with diagnols
        probsDiag = [x[0] for x in movesAndProbsDiag]
        if -1 in probsDiag:
            move = moves[probsDiag.index(-1)]
            return move
        probsDiag = [x / sum(probsDiag) for x in probsDiag]        

        probs = [(x + y + z) / 3 for x,y,z in list(zip(probsRows, probsCol, probsDiag))] #average all scores/probabities to find the best move overall
        while True:                         #this essentially is us picking a move at random but moves with higher probabilties are more likely to be picked
            prob = random.random()          #pick number between 1 and 0
            move = random.randint(0, 5)     #pick random move
            if prob < probs[move]:          #if my random number between 0 and 1 is less than the probabiltiy of that move then play it, else pick again
                move = moves[move]          #^this results in higher probability moves being picked more and vice versa
                break
        return move

    def analyzeRows(self):                  #analyzes which move sets the agent up best to win in the rows
        moves = []
        for column in range(6): #goes through each column
            row = 0             #stores the row the move puts the peice in
            while self.board[row][column] == "-" and row < 5:  #go until we find a row with that peice
                row += 1      

            if row == 0:                                            #if the top row is full we cant play here so we return a move score of zero
                moveViability = 0
                moves.append([moveViability, column])
                continue 
            elif self.board[row][column] != '-':               #otherwisew we subtract one from the row to put us on the open row
                row -= 1

            moveViability = 1                                       #default score of 1
            
            if column < 3:              #checking three spots to the right
                numMySyms = 0
                numNotMySyms = 0
                for y in range(1, 4):                       #keeps track of how many of our pieces and how many of the opponents peices are there
                    if self.board[row][column + y] == self.playerSymbol:
                        numMySyms += 1
                    elif self.board[row][column + y] != self.playerSymbol and self.board[row][column + y] != '-':
                        numNotMySyms += 1
                if numMySyms == 3 or numNotMySyms == 3:     #if there are three of our or their peices we must play here to win or avoid loosing
                    moves.append([-1, column])
                    continue
                else:
                    moveViability *= math.exp(numMySyms - numNotMySyms) #otherwise we put e ^ number of our peieces - their peices to calculate a move score, more of our peices == better move
                    
            if column < 4 and column > 0:           #checking two spaces to the right and one to the left
                numMySyms = 0
                numNotMySyms = 0
                for y in range(1, 3):
                    if self.board[row][column + y] == self.playerSymbol:
                        numMySyms += 1
                    elif self.board[row][column + y] != self.playerSymbol and self.board[row][column + y] != '-':
                        numNotMySyms += 1
                if self.board[row][column - 1] == self.playerSymbol:
                    numMySyms += 1
                elif self.board[row][column - 1] != self.playerSymbol and self.board[row][column - 1] != '-':
                    numNotMySyms += 1
                    
                if numMySyms == 3 or numNotMySyms == 3:
                    moves.append([-1, column])
                    continue
                else:
                    moveViability *= math.exp(numMySyms - numNotMySyms)
                    
            if column > 2:                      #checking three to the left
                numMySyms = 0
                numNotMySyms = 0
                for y in range(1, 4):
                    if self.board[row][column - y] == self.playerSymbol:
                        numMySyms += 1
                    elif self.board[row][column - y] != self.playerSymbol and self.board[row][column - y] != '-':
                        numNotMySyms += 1
                if numMySyms == 3 or numNotMySyms == 3:
                    moves.append([-1, column])
                    continue
                else:
                    moveViability *= math.exp(numMySyms - numNotMySyms)
                    
            if column > 1 and column < 5:           #checking two to the left and one to the right
                numMySyms = 0
                numNotMySyms = 0
                for y in range(1, 3):
                    if self.board[row][column - y] == self.playerSymbol:
                        numMySyms += 1
                    elif self.board[row][column - y] != self.playerSymbol and self.board[row][column - y] != '-':
                        numNotMySyms += 1
                if self.board[row][column + 1] == self.playerSymbol:
                    numMySyms += 1
                elif self.board[row][column + 1] != self.playerSymbol and self.board[row][column + 1] != '-':
                    numNotMySyms += 1
                    
                if numMySyms == 3 or numNotMySyms == 3:
                    moves.append([-1, column])
                    continue
                else:
                    moveViability *= math.exp(numMySyms - numNotMySyms)
                    
            moves.append([moveViability, column]) #append the move and its move score to the moves list
        return moves                              #return the moves and their scores
    
    def analyzeColumns(self):                   #analyzes which moves set the agent up to win best with regards to columns
        moves = []
        for column in range(6):                 #goes through each column and evaluates move
            row = 0                             #figures out which row the move will put it in, same as other anaylze functions, see analyazeRows for more details
            while self.board[row][column] == "-" and row < 5: 
                row += 1

            if row == 0:
                moveViability = 0
                moves.append([moveViability, column])
                continue 
            elif self.board[row][column] != '-':
                row -= 1

            moveViability = 1                   #see analyze rows for info on the scoring method for moves
            if row < 5:                         #checks three below as its not possible to have peices on top of us, may add less score the higher up we are
                tempRow = row + 1
                numMySyms = 0
                numNotMySyms = 0
                while tempRow < 6 and tempRow < row + 4:
                    if self.board[tempRow][column] == self.playerSymbol:
                        numMySyms += 1
                    elif self.board[tempRow][column] != self.playerSymbol and self.board[tempRow][column] != '-':
                        numNotMySyms += 1
                    tempRow += 1

                if numMySyms == 3 or numNotMySyms == 3:
                    moves.append([-1, column])
                else:
                    moveViability *= math.exp(numMySyms - numNotMySyms)
                    moves.append([moveViability, column])
            else:
                moves.append([1, column])

        return moves

    def analyzeDiagnols(self):                              #calls both analyzeXXXDiagnols and averages their move scores before returning them
        movesAndProbs = self.analyzeRightDiagnols()     #analyzes right
        movesAndProbs2 = self.analyzeLeftDiagnols()     #analyzes left

        moves = [x[1] for x in movesAndProbs]           #seperates out moves
        
        probs0 = [x[0] for x in movesAndProbs]          #seperates out probs for each
        probs2 = [x[0] for x in movesAndProbs2]
        probs = [(x + y) / 2 for x,y in zip(probs0, probs2)] #averages them
        moves = [[x,y] for x,y in zip(probs, moves)]    #puts them back together for the generate move function
        if -1 in probs0:                                                #checks for the PLAY NOW FLAG and replaces that probability with the flag before returning
            moves[probs0.index(-1)] = [-1, moves[probs0.index(-1)][1]]
        if -1 in probs2:
            moves[probs2.index(-1)] = [-1, moves[probs2.index(-1)][1]]
        return moves
        #movesAndProbsLeft = self.analyzeLeftDiagnols()
        

    def analyzeRightDiagnols(self):                     #analyze the best moves with regards to right diagnols 
        moves = []
        for column in range(6):
            row = 0
            while self.board[row][column] == "-" and row < 5:      #finding the row the last move in this column is in
                row += 1

            if row == 0:                                                #if at the top then the column is full
                moveViability = 0
                moves.append([moveViability, column])
                continue 
            elif self.board[row][column] != '-':                   #otherwise we move up a row to get to the free space
                row -= 1


            moveViability = 1                                           #see analyze rows for info on move scoring, its the same here
            
            if column < 3 and row > 2:                                  #checking three to the upper right
                numMySyms = 0
                numNotMySyms = 0
                for y in range(1,4):
                    if self.board[row - y][column + y] == self.playerSymbol:
                        numMySyms += 1
                    elif self.board[row - y][column + y] != '-':
                        numNotMySyms += 1
                        
                if numMySyms == 3 or numNotMySyms == 3:
                    moves.append([-1, column])
                    continue
                else:
                    moveViability *= math.exp(numMySyms - numNotMySyms)
                    
            if column < 4 and column > 0 and row > 1 and row < 5:   #checking two the upper right and one to the bottom left
                numMySyms = 0
                numNotMySyms = 0
                for y in range(1, 3):
                    if self.board[row - y][column + y] == self.playerSymbol:
                        numMySyms += 1
                    elif self.board[row - y][column + y] != '-':
                        numNotMySyms += 1

                if self.board[row + 1][column - 1] == self.playerSymbol:
                    numMySyms += 1
                elif self.board[row + 1][column - 1] != '-':
                    numNotMySyms += 1
                    
                if numMySyms == 3 or numNotMySyms == 3:
                    moves.append([-1, column])
                    continue
                else:
                    moveViability *= math.exp(numMySyms - numNotMySyms)
                
            if column > 2 and row < 3:                              #checking three to the bottom left
                numMySyms = 0
                numNotMySyms = 0

                for y in range(1, 4):
                    if self.board[row + y][column - y] == self.playerSymbol:
                        numMySyms += 1
                    elif self.board[row + y][column - y] != '-':
                        numNotMySyms += 1
                
                if numMySyms == 3 or numNotMySyms == 3:
                    moves.append([-1, column])
                    continue
                else:
                    moveViability *= math.exp(numMySyms - numNotMySyms)
                
            if column > 1 and column < 5 and row < 4 and row > 0: #checking two to the bottom left and one to the upper right
                numMySyms = 0
                numNotMySyms = 0

                for y in range(1, 3):
                    if self.board[row + y][column - y] == self.playerSymbol:
                        numMySyms += 1
                        
                    elif self.board[row + y][column - y] != '-':
                        numNotMySyms += 1
                        
                if self.board[row - 1][column + 1] == self.playerSymbol:
                    numMySyms += 1
                elif self.board[row][column + 1] != '-':
                    numNotMySyms += 1
    
                
                if numMySyms == 3 or numNotMySyms == 3:
                    moves.append([-1, column])
                    continue
                else:
                    moveViability *= math.exp(numMySyms - numNotMySyms)
                
            moves.append([moveViability, column])
        return moves

    def analyzeLeftDiagnols(self):                                  #analyzes the best moves with regards to left diagnols
        moves = []
        for column in range(6):     #going through each column
            row = 0
            while self.board[row][column] == "-" and row < 5:      #finding row the move we make will place us im
                row += 1

            if row == 0:
                moveViability = 0
                moves.append([moveViability, column])
                continue 
            elif self.board[row][column] != '-':
                row -= 1


            moveViability = 1
            
            if column > 2 and row > 2:                              #checking three to the upper left
                numMySyms = 0
                numNotMySyms = 0
                for y in range(1,4):
                    if self.board[row - y][column - y] == self.playerSymbol:
                        numMySyms += 1
                    elif self.board[row - y][column - y] != '-':
                        numNotMySyms += 1
                        
                if numMySyms == 3 or numNotMySyms == 3:
                    moves.append([-1, column])
                    continue
                else:
                    moveViability *= math.exp(numMySyms - numNotMySyms)
                    
            if column > 1 and column < 5 and row > 1 and row < 5:   #checking two to the upper left and one to the bottom right
                numMySyms = 0
                numNotMySyms = 0
                for y in range(1, 3):
                    if self.board[row - y][column - y] == self.playerSymbol:
                        numMySyms += 1
                    elif self.board[row - y][column - y] != '-':
                        numNotMySyms += 1

                if self.board[row + 1][column + 1] == self.playerSymbol:
                    numMySyms += 1
                elif self.board[row + 1][column + 1] != '-':
                    numNotMySyms += 1
                    
                if numMySyms == 3 or numNotMySyms == 3:
                    moves.append([-1, column])
                    continue
                else:
                    moveViability *= math.exp(numMySyms - numNotMySyms)
                
            if column < 3 and row < 3:                          #checking three to the bottom right
                numMySyms = 0
                numNotMySyms = 0

                for y in range(1, 4):
                    if self.board[row + y][column + y] == self.playerSymbol:
                        numMySyms += 1
                    elif self.board[row + y][column + y] != '-':
                        numNotMySyms += 1
                
                if numMySyms == 3 or numNotMySyms == 3:
                    moves.append([-1, column])
                    continue
                else:
                    moveViability *= math.exp(numMySyms - numNotMySyms)
                    
            if column < 4 and column > 0 and row < 4 and row > 0: #checking two the bottom right and one to the upper left
                numMySyms = 0
                numNotMySyms = 0

                for y in range(1, 3):
                    if self.board[row + y][column + y] == self.playerSymbol:
                        numMySyms += 1
                        
                    elif self.board[row + y][column + y] != '-':
                        numNotMySyms += 1
                        
                if self.board[row - 1][column - 1] == self.playerSymbol:
                    numMySyms += 1
                elif self.board[row][column - 1] != '-':
                    numNotMySyms += 1
    
                
                if numMySyms == 3 or numNotMySyms == 3:
                    moves.append([-1, column])
                    continue
                else:
                    moveViability *= math.exp(numMySyms - numNotMySyms)
                    
            moves.append([moveViability, column])
        return moves

            
if __name__ == "__main__":                              
    newGame = connect4.Connect4Game(True)                   


    player1 = Connect4ProbabilityPlayer(1)              
    player2 = Connect4ProbabilityPlayer(2)

    newGame.start()

    for x in range(10):
        player1.joinGame(newGame)
        player2.joinGame(newGame)

        while newGame.gameIsNotOver():
            pass

        print("Winner: %d" % newGame.winner.playerID)
        newGame.prepareForNewGame()
        

    print(player1.wins)

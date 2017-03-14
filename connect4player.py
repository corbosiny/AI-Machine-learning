import connect4                                         #our game object
import threading
import random                                           #used for move probability choice
import time                                             #used to give the time for the AI to make its move before we display the board
import connect4PlayerRandom                             #used for our agent to play against as a benchmark
import max                                              #just used for square roots and such


#if confused on the requirments we put on columns and rows to check moves, look at the connect4 game code where I explain why we need to check those before checking certain moves
class Connect4Player(threading.Thread):                 #inherits from thread so we can run multiple agents playing in the background

    def __init__(self, game, playerNum):
        self.game = game                                #we give it a game obejct to play
        self.playerNum = playerNum                      #tell it its turn number
        self.wins = 0                                   #keeps track of wins
        self.sym = self.game.playerSymbols[playerNum]   #keeps track of its own symbol for when its determining good moves
        super(Connect4Player, self).__init__()          #calls the thread init function to prepare the threads normal abilities

    def makeMove(self, move):                           #checks if the game is over and if its the agents turn, if so then it sends the move to the game object
        while self.game.turn != self.playerNum:
            pass
        
        if self.game.winner != None:
            return None
        else:
            self.game.makeMove(move)

    def generateMove(self):                             #recieves recomendations for moves from analyzing rows, columns, and diganols then averages all their move scores, then picks a move and plays it
        movesAndProbsRows = self.analyzeRows()          #recieve row recomendations
        moves = [x[1] for x in movesAndProbsRows]
        probsRows = [x[0] for x in movesAndProbsRows] #seperate our moves and their probabilities
        if -1 in probsRows:                           #checking if we have the PLAY NOW flag
            move = moves[probsRows.index(-1)]
            self.makeMove(move)
            return None
        probsRows = [x / sum(probsRows) for x in probsRows] #turns all scores in probabilties

        movesAndProbsCol = self.analyzeColumns()            #repeat with columns
        probsCol = [x[0] for x in movesAndProbsCol]
        if -1 in probsCol:
            move = moves[probsCol.index(-1)]
            self.makeMove(move)
            return None
        probsCol = [x / sum(probsCol) for x in probsCol]

        movesAndProbsDiag = self.analyzeDiagnols()          #repeat with diagnols
        probsDiag = [x[0] for x in movesAndProbsDiag]
        if -1 in probsDiag:
            move = moves[probsDiag.index(-1)]
            self.makeMove(move)
            return None
        probsDiag = [x / sum(probsDiag) for x in probsDiag]        

        probs = [(x + y + z) / 3 for x,y,z in list(zip(probsRows, probsCol, probsDiag))] #average all scores/probabities to find the best move overall
        while True:                         #this essentially is us picking a move at random but moves with higher probabilties are more likely to be picked
            prob = random.random()          #pick number between 1 and 0
            move = random.randint(0, 5)     #pick random move
            if prob < probs[move]:          #if my random number between 0 and 1 is less than the probabiltiy of that move then play it, else pick again
                move = moves[move]          #^this results in higher probability moves being picked more and vice versa
                break
        self.makeMove(move)

    def analyzeRows(self):                  #analyzes which move sets the agent up best to win in the rows
        moves = []
        for column in range(6): #goes through each column
            row = 0             #stores the row the move puts the peice in
            while self.game.board[row][column] == "-" and row < 5:  #go until we find a row with that peice
                row += 1      

            if row == 0:                                            #if the top row is full we cant play here so we return a move score of zero
                moveViability = 0
                moves.append([moveViability, column])
                continue 
            elif self.game.board[row][column] != '-':               #otherwisew we subtract one from the row to put us on the open row
                row -= 1

            moveViability = 1                                       #default score of 1
            
            if column < 3:              #checking three spots to the right
                numMySyms = 0
                numNotMySyms = 0
                for y in range(1, 4):                       #keeps track of how many of our pieces and how many of the opponents peices are there
                    if self.game.board[row][column + y] == self.sym:
                        numMySyms += 1
                    elif self.game.board[row][column + y] != self.sym and self.game.board[row][column + y] != '-':
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
                    if self.game.board[row][column + y] == self.sym:
                        numMySyms += 1
                    elif self.game.board[row][column + y] != self.sym and self.game.board[row][column + y] != '-':
                        numNotMySyms += 1
                if self.game.board[row][column - 1] == self.sym:
                    numMySyms += 1
                elif self.game.board[row][column - 1] != self.sym and self.game.board[row][column - 1] != '-':
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
                    if self.game.board[row][column - y] == self.sym:
                        numMySyms += 1
                    elif self.game.board[row][column - y] != self.sym and self.game.board[row][column - y] != '-':
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
                    if self.game.board[row][column - y] == self.sym:
                        numMySyms += 1
                    elif self.game.board[row][column - y] != self.sym and self.game.board[row][column - y] != '-':
                        numNotMySyms += 1
                if self.game.board[row][column + 1] == self.sym:
                    numMySyms += 1
                elif self.game.board[row][column + 1] != self.sym and self.game.board[row][column + 1] != '-':
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
            while self.game.board[row][column] == "-" and row < 5: 
                row += 1

            if row == 0:
                moveViability = 0
                moves.append([moveViability, column])
                continue 
            elif self.game.board[row][column] != '-':
                row -= 1

            moveViability = 1                   #see analyze rows for info on the scoring method for moves
            if row < 5:                         #checks three below as its not possible to have peices on top of us, may add less score the higher up we are
                tempRow = row + 1
                numMySyms = 0
                numNotMySyms = 0
                while tempRow < 6 and tempRow < row + 4:
                    if self.game.board[tempRow][column] == self.sym:
                        numMySyms += 1
                    elif self.game.board[tempRow][column] != self.sym and self.game.board[tempRow][column] != '-':
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
            while self.game.board[row][column] == "-" and row < 5:      #finding the row the last move in this column is in
                row += 1

            if row == 0:                                                #if at the top then the column is full
                moveViability = 0
                moves.append([moveViability, column])
                continue 
            elif self.game.board[row][column] != '-':                   #otherwise we move up a row to get to the free space
                row -= 1


            moveViability = 1                                           #see analyze rows for info on move scoring, its the same here
            
            if column < 3 and row > 2:                                  #checking three to the upper right
                numMySyms = 0
                numNotMySyms = 0
                for y in range(1,4):
                    if self.game.board[row - y][column + y] == self.sym:
                        numMySyms += 1
                    elif self.game.board[row - y][column + y] != '-':
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
                    if self.game.board[row - y][column + y] == self.sym:
                        numMySyms += 1
                    elif self.game.board[row - y][column + y] != '-':
                        numNotMySyms += 1

                if self.game.board[row + 1][column - 1] == self.sym:
                    numMySyms += 1
                elif self.game.board[row + 1][column - 1] != '-':
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
                    if self.game.board[row + y][column - y] == self.sym:
                        numMySyms += 1
                    elif self.game.board[row + y][column - y] != '-':
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
                    if self.game.board[row + y][column - y] == self.sym:
                        numMySyms += 1
                        
                    elif self.game.board[row + y][column - y] != '-':
                        numNotMySyms += 1
                        
                if self.game.board[row - 1][column + 1] == self.sym:
                    numMySyms += 1
                elif self.game.board[row][column + 1] != '-':
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
            while self.game.board[row][column] == "-" and row < 5:      #finding row the move we make will place us im
                row += 1

            if row == 0:
                moveViability = 0
                moves.append([moveViability, column])
                continue 
            elif self.game.board[row][column] != '-':
                row -= 1


            moveViability = 1
            
            if column > 2 and row > 2:                              #checking three to the upper left
                numMySyms = 0
                numNotMySyms = 0
                for y in range(1,4):
                    if self.game.board[row - y][column - y] == self.sym:
                        numMySyms += 1
                    elif self.game.board[row - y][column - y] != '-':
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
                    if self.game.board[row - y][column - y] == self.sym:
                        numMySyms += 1
                    elif self.game.board[row - y][column - y] != '-':
                        numNotMySyms += 1

                if self.game.board[row + 1][column + 1] == self.sym:
                    numMySyms += 1
                elif self.game.board[row + 1][column + 1] != '-':
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
                    if self.game.board[row + y][column + y] == self.sym:
                        numMySyms += 1
                    elif self.game.board[row + y][column + y] != '-':
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
                    if self.game.board[row + y][column + y] == self.sym:
                        numMySyms += 1
                        
                    elif self.game.board[row + y][column + y] != '-':
                        numNotMySyms += 1
                        
                if self.game.board[row - 1][column - 1] == self.sym:
                    numMySyms += 1
                elif self.game.board[row][column - 1] != '-':
                    numNotMySyms += 1
    
                
                if numMySyms == 3 or numNotMySyms == 3:
                    moves.append([-1, column])
                    continue
                else:
                    moveViability *= math.exp(numMySyms - numNotMySyms)
                    
            moves.append([moveViability, column])
        return moves
    
    def run(self):
        while True:                                         #while the agent has a game object it will wait for its turn and play
            while self.game.winner == None:                 #while the game has no winner keep playing
                while self.game.turn != self.playerNum:     #waiting for turn
                    pass
                self.generateMove()                         #generate move when its turn is up

            if self.game.winner == self.playerNum:          #keeps track of its wins
                self.wins += 1        
            self.game = None                                #sets game object to None and waits for new game to be given to play
            while self.game == None:
                pass
            
if __name__ == "__main__":                              
    newGame = connect4.Connect4Game()                   #initialize a game

        #test code 1:
##    player1 = Connect4Player(newGame, 0)              #this code is for pitting the agent in 100 games against the benchmark random player
##    player2 = connect4PlayerRandom.Connect4PlayerRandom(newGame, 1)
##    player1.start()
##    player2.start()
##
##    for x in range(100):
##        while newGame.winner == None:
##            currentTurn = newGame.turn
##        try:
##            print("Winner: Player %d" % newGame.winner)
##        except:
##            print("Winner: Player %s" % newGame.winner)
##        newGame = connect4.Connect4Game()
##        player1.game = newGame
##        player2.game = newGame
##
##    print(player1.wins)

##------------------------------------------------------------------
    #test code: 2
    player1 = Connect4Player(newGame, 0)            #this code pits you against the agent
    player1.start()
    while newGame.winner == None:
        while newGame.turn == 0:
            pass
        time.sleep(.1)
        print(newGame)
        move = int(input('\n>>>>'))
        newGame.makeMove(move - 1)
    try:
        print("\nWinner: Player %d" % newGame.winner)
    except:
        print('\nDRAW')

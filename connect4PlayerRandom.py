import connect4
import threading
import random

class Connect4PlayerRandom(threading.Thread):   #inherits from thread so we can have multiple agents playing at once

    def __init__(self, game, playerNum):
        self.game = game                                #it is given a connect4 game object to play
        self.playerNum = playerNum                      #it is told its turn number
        self.wins = 0                                   #keeps track of its win percentage
        super(Connect4PlayerRandom, self).__init__()    #used to also call the thread init to set up all the proper needs of a thread

    def makeMove(self):                                 #simply picks a random column and plays there if it isn't empty
        while self.game.turn != self.playerNum:         #waits for its turn
            pass

        move = random.randint(0, 5)                     #generates move and test if column is open
        while self.game.board[0][move] != '-':
            move = random.randint(0, 5)
        
        if self.game.winner != None:                    #if the game is won abort move, otherwise make the move
            return None
        else:
            self.game.makeMove(move)

    def run(self):                                      #simply plays the game, when the game is over it waits to be given a new game object to play
        while True:
            while self.game.winner == None:
                self.makeMove()

            if self.game.winner == self.playerNum:
                self.wins += 1        

            self.game = None
            while self.game == None:
                pass
            
if __name__ == "__main__":                              #test code that pits two random players against one another
    newGame = connect4.Connect4Game()
    player1 = Connect4Player(newGame, 0)
    player2 = Connect4Player(newGame, 1)
    player1.start()
    player2.start()
    
    while newGame.winner == None:
        pass
    print("Winner: Player %d" % newGame.winner)

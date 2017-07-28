import connect4
from connect4PlayerShell import Connect4PlayerShell
import threading
import random
import time

class Connect4PlayerRandom(Connect4PlayerShell):   #the template most of our functionality comes from

    def __init__(self):
        super(Connect4PlayerRandom, self).__init__()    #calling superclass constructor
        self.start()


    def generateMove(self):
        move = random.randint(0, 5)                     
        while self.game.board[0][move] != '-':
            move = random.randint(0, 5)
        return move

    
if __name__ == "__main__":                              #test code that pits two random players against one another
    newGame = connect4.Connect4Game(True)

    while True:
        newGame.displayBoard()
        player1 = Connect4PlayerRandom()
        player2 = Connect4PlayerRandom()
        newGame.addPlayer(player1)
        newGame.addPlayer(player2)
    
        while newGame.winner == None:
            pass

        newGame.players[newGame.winner].wins += 1
        newGame.prepareForNewGame()

import connect4
from connect4PlayerShell import Connect4PlayerShell
import threading
import random
import time

class Connect4PlayerRandom(Connect4PlayerShell):   #the template most of our functionality comes from

    def __init__(self, playerID = None):
        super(Connect4PlayerRandom, self).__init__(playerID)    #calling superclass constructor


    def generateMove(self):
        move = random.randint(0, 5)                     
        while self.game.board[0][move] != '-':
            move = random.randint(0, 5)
        return move

    
if __name__ == "__main__":                              #test code that pits two random players against one another
    newGame = connect4.Connect4Game(True)
    
    
    player1 = Connect4PlayerRandom()
    player2 = Connect4PlayerRandom()

    newGame.start()
    while True:
        player1.joinGame(newGame)
        player2.joinGame(newGame)

        while newGame.gameIsNotOver():
            pass

        print(player1.wins)
        print(player2.wins)
        newGame.prepareForNewGame()

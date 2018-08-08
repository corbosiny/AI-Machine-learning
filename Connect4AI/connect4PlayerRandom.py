import connect4 #Only for testing purposes
from connect4PlayerShell import Connect4PlayerShell
import threading
import random
import time

class Connect4PlayerRandom(Connect4PlayerShell):   #the template most of our functionality comes from

    def __init__(self, playerID = None):
        super(Connect4PlayerRandom, self).__init__(playerID)    #calling superclass constructor


    def generateMove(self, board):
        move = random.randint(0, board.boardLength - 1)                     
        return move

    
if __name__ == "__main__":                              #test code that pits two random players against one another
    import connect4PlayerTester
    tester = connect4PlayerTester.PlayerTester(Connect4PlayerRandom)
    assert(tester.testPlayers() == True)
    print("Initial Diagnostics Passed!\n\n")
    
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

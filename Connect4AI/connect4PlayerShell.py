import connect4
import threading
import random

class Connect4PlayerShell():

    def __init__(self, playerID = None):
        self.playerID = playerID
        self.wins = 0
        self.prepareForNewGame()
        self.doneTraining = True
        
    def prepareForNewGame(self):
        self.playerSymbol = None


    def joinGame(self, game):
        self.playerSymbol = game.addPlayer(self)
        
    def generateMove(self, board):
        move = random.randint(0, board.boardLength - 1)                     
        return move

    def train(self):
        self.doneTraining = False
        self.doneTraining = True
        
if __name__ == "__main__":
    newGame = connect4.Connect4Game(True)

    player1 = Connect4PlayerShell(1)
    player2 = Connect4PlayerShell(2)

    newGame.start()

    player1.joinGame(newGame)
    player2.joinGame(newGame)

    while newGame.gameIsNotOver():
        pass

    print("Done")

    

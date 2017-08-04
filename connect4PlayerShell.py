import connect4
import threading

class Connect4PlayerShell():

    def __init__(self, playerID = None):
        self.playerID = playerID
        self.wins = 0
        self.game = None

    def prepareForNewGame(self):
        self.playerSymbol = None


    def joinGame(self, game):
        self.playerSymbol = game.addPlayer(self)
        self.game = game

    def generateMove(self, board):
        pass                #decendant classes will fill this in



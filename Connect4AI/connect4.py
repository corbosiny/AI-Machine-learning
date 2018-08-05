import sys
import threading
from connect4Board import *
import connect4PlayerRandom
from connect4HumanPlayer import Connect4HumanPlayer

DEFAULT_BOARD_LENGTH = 7
DEFAULT_BOARD_HEIGHT = 6

class Connect4Game(threading.Thread):

    playerSymbols = ['X','O']
    emptySpotSymbol = '-'

    def __init__(self, displayGame = False, boardLength= DEFAULT_BOARD_LENGTH, boardHeight= DEFAULT_BOARD_HEIGHT):
        self.displayGame = displayGame
        self.boardLength = DEFAULT_BOARD_LENGTH
        self.boardHeight = DEFAULT_BOARD_HEIGHT
        self.initializeGame()
        super(Connect4Game, self).__init__()


    def initializeGame(self):
        self.board = Connect4Board(self.boardLength, self.boardHeight)
        self.players = []
        self.resetGameState()

    def resetGameState(self):
        self.turn = 0
        self.numMoves = 0
        self.winner = None
        self.gameOver = False


        

    def run(self):
        while True:
            self.waitForPlayersToJoin()
            self.playGame()
            self.waitToBeReset()

    def waitForPlayersToJoin(self):
        while len(self.players) < 2:
            pass


    def playGame(self):
        while self.winner is None:

            if self.displayGame:
                print(self)

            columnOfMove = self.players[self.turn].generateMove(self.board)
            self.makeMove(columnOfMove)

        
    def gameIsNotOver(self):
        return self.gameOver == False


    def makeMove(self, column):
        currentPlayerSymbol = Connect4Game.playerSymbols[self.turn]
        try:
            self.board.updateBoard(column, currentPlayerSymbol)
            self.updateGameState()
        except InvalidMoveError as error:
            return

        
    def updateGameState(self):
        self.numMoves += 1
        self.checkIfGameOver()
        self.turn = int(not self.turn)


    def checkIfGameOver(self):
        if self.board.checkWin():
            self.winner = self.players[self.turn]
            self.winner.wins += 1
        elif self.numMoves == len(self.board) * len(self.board[0]):     
            self.winner = "DRAW"
        


    def waitToBeReset(self):
        self.gameOver = True
        while self.gameOver:
            pass
    
    
    def prepareForNewGame(self):
        self.removePlayersFromGame()
        self.board.clearBoard()
        self.resetGameState()
        
    def removePlayersFromGame(self):
        listOfPlayers = [player for player in self.players]
        for player in listOfPlayers:
            self.players.remove(player)




    def addPlayer(self, player):
        newPlayersSymbol = Connect4Game.playerSymbols[len(self.players)]
        self.players.append(player)
        return newPlayersSymbol

        
    
    def __str__(self):         
        return str(self.board)
    
if __name__ == "__main__":              
    newGame = Connect4Game(True)

    HumanPlayer = Connect4HumanPlayer(1)
    AIplayer = connect4PlayerRandom.Connect4PlayerRandom(2)      #uncomment to play against random AI
    newGame.start()
    while True:
        HumanPlayer.joinGame(newGame)
        AIplayer.joinGame(newGame)

        while newGame.gameIsNotOver():
            pass

        newGame.prepareForNewGame()
        

import sys
from connect4Board import *
import connect4PlayerRandom

class Connect4Game():

    playerSymbols = ['X','O']

    def __init__(self, printGameAfterMove = False):
        self.board = Connect4Board()
        self.printGameAfterMove = printGameAfterMove
        self.players = []
        
        self.prepareForNewGame()
        
    def prepareForNewGame(self):        
        self.waitForPlayersToLeaveGame()
        self.board.clearBoard()
        self.resetGameState()
        self.displayBoard()
        
    def waitForPlayersToLeaveGame(self):
        for player in self.players:
            self.waitForPlayerToLeaveGame(player)

    def waitForPlayerToLeaveGame(self, player):
        if self.isHumanPlayer(player):              #human players are represetned as strings
            return
        
        self.turn = player.playerNum
        while player.game is self:
            pass

    def isHumanPlayer(self, player):
        return isinstance(player, str)

                  
    def resetGameState(self):
        self.resetPlayers()
        self.turn = 0
        self.numMoves = 0
        self.winner = None
    
    def resetPlayers(self):
        self.numPlayers = 0
        self.players = []






    def addPlayer(self, player):
        try:
            player.playerNum = self.numPlayers
            player.playerSymbol = Connect4Game.playerSymbols[self.numPlayers]
            player.game = self
        except:                 #triggers for human players
            pass
        
        self.players.append(player)
        self.numPlayers += 1



    

    def makeMove(self, column):
        currentPlayerSymbol = Connect4Game.playerSymbols[self.turn]
        try:
            self.board.updateBoard(column, currentPlayerSymbol)
            self.updateGameState()
            self.displayBoard()
        except InvalidMoveError as e:
            print(e)
            return
        

    def updateGameState(self):
        self.numMoves += 1
        self.winner = self.checkIfGameOver()
        self.turn = int(not self.turn)


    def checkIfGameOver(self):
        if self.board.checkWin():
            self.awardPlayerTheWin(self.turn)
            return self.turn 
        elif self.numMoves == len(self.board) * len(self.board[0]):     
            return "DRAW"
        else:
            return None


    def awardPlayerTheWin(self, playerNum):
        try:
            self.players[playerNum].wins += 1
        except:             #will trigger for human players
            pass




    def displayBoard(self):
        if self.printGameAfterMove:
            print(self.board)
        
        
    def gameIsNotOver(self):
        return self.winner == None
    
    def __str__(self):         
        return str(self.board)
    
if __name__ == "__main__":              
    newGame = Connect4Game(True)

##    print(newGame)                            #uncomment for hotset game test
##    while newGame.winner == None:
##            move = int(input('\n>> '))
##            newGame.makeMove(move - 1)
##            print(newGame)

    AIplayer = connect4PlayerRandom.Connect4PlayerRandom()      #uncomment to play against random AI

    while True:
        newGame.addPlayer("Corey")
        newGame.addPlayer(AIplayer)
        
        while newGame.winner == None:
            while newGame.turn != 0:
                pass
            move = int(input('\n>> '))
            newGame.makeMove(move - 1)
        
        newGame.prepareForNewGame()
    

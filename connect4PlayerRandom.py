import connect4
import threading
import random

class Connect4PlayerRandom(threading.Thread):   #is a thread so we can run multiple agents

    def __init__(self):
        self.wins = 0
        self.game = None
        super(Connect4PlayerRandom, self).__init__()    #calling thread constructor
        self.start()

    def prepareForNewGame(self):                        
        self.playerNum = None
        self.playerSymbol = None
        self.game = None
        
    def joinNewGame(self, game):
        self.playerNum, self.playerSymbol = game.addPlayer(self)
        self.game = game

    def playGame(self):
        while self.game.gameIsNotOver():
                self.waitForTurn()
                self.takeTurn()

    def waitForTurn(self):
        while self.game.turn != self.playerNum and self.game.gameIsNotOver():         
            pass
    
    def takeTurn(self):
        if self.game.gameIsNotOver(): 
            move = self.generateMove()                   
            self.game.makeMove(move)


    def generateMove(self):
        move = random.randint(0, 5)                     
        while self.game.board[0][move] != '-':
            move = random.randint(0, 5)
        return move
    
    def run(self):                                      
        while True:
            self.waitToBePutInANewGame()
            self.playGame()   
            self.leaveGame()
        
    
    def waitToBePutInANewGame(self):
        self.prepareForNewGame()
        while self.game == None:
                pass

    def leaveGame(self):
        self.game = None

    
if __name__ == "__main__":                              #test code that pits two random players against one another
    newGame = connect4.Connect4Game(True)

    while True:
        newGame.displayBoard()
        player1 = Connect4PlayerRandom()
        player2 = Connect4PlayerRandom()
        player1.joinNewGame(newGame)
        player2.joinNewGame(newGame)
    
        while newGame.winner == None:
            pass

        newGame.players[newGame.winner].wins += 1
        newGame.prepareForNewGame()

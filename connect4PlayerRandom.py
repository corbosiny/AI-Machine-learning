import connect4
import threading
import random

class Connect4PlayerRandom(threading.Thread):   #is a thread so we can run multiple agents

    def __init__(self, game):
        self.wins = 0
        super(Connect4PlayerRandom, self).__init__()    #calling thread constructor
        self.start()

    def prepareForNewGame(self):
        self.playerNum = None
        self.playerSymbol = None
        
    def joinNewGame(self, game):
        self.playerNum, self.playerSymbol = game.addPlayer(self)
        self.game = game


    def gameIsNotOver(self):
        return self.game.winner == None
    
    def takeTurn(self):                                 
        move = self.generateMove()
        if self.gameIsNotOver():                    
            self.game.makeMove(move)

    def waitForTurn(self):
        while self.game.turn != self.playerNum:         
            pass

    def generateMove(self):
        move = random.randint(0, 5)                     
        while self.game.board[0][move] != '-':
            move = random.randint(0, 5)
        return move
    
    def run(self):                                      
        while True:
            self.waitToBePutInANewGame()
            self.playGame()

            if self.game.winner == self.playerNum:
                self.wins += 1        

            self.waitForGameLobbyToClose()

    def playGame(self):
        while self.gameIsNotOver():
                self.waitForTurn()
                self.takeTurn()
                
    def waitForGameLobbyToClose(self):
        while self.game != None:
            pass
    
    def waitToBePutInANewGame(self):
        self.prepareForNewGame()
        while self.game == None:
                pass
        
if __name__ == "__main__":                              #test code that pits two random players against one another
    newGame = connect4.Connect4Game(True)
    player1 = Connect4PlayerRandom(newGame)
    player2 = Connect4PlayerRandom(newGame)
    player1.start()
    player2.start()
    
    while newGame.winner == None:
        pass
    

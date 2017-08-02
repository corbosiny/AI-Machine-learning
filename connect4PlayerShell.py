import connect4
import threading

class Connect4PlayerShell(threading.Thread):
    def __init__(self):
        self.wins = 0
        self.game = None
        super(Connect4PlayerShell, self).__init__()    #calling thread constructor

    
    def run(self):                                      
        while True:
            self.prepareForNewGame()
            self.waitToBePutInANewGame()
            self.playGame()
            self.checkIfWinner()
            self.leaveGame()


    def prepareForNewGame(self):                        
        self.playerNum = None
        self.playerSymbol = None        
    

    def waitToBePutInANewGame(self):
        while self.game == None:
                pass


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
        pass                #decendant classes will fill this in


    def checkIfWinner(self):
        if self.game.winner == self.playerNum:
            self.wins += 1

    def leaveGame(self):
        self.game = None


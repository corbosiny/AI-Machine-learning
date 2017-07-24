import random
import Connect4Game()
class GameMaster():


    def __init__(self, gamePool, players):
        this.openGamePool = gamePool
        this.closedGamePool = []
        this.waitingPlayers = players
        this.playersInGame = []
        self.startAllGames()
        self.spectatingGame = None
        self.runGames = True
        manageGames()
        
    def manageGames(self):
        while self.runGames:
            self.waitForOpenGame()
            self.pickTwoPlayers()
            self.startGame()

    def startAllGames(self):
        while len(this.gamePool) != 0 and len(this.waitingPlayers) > 2:
            player1, player2 = self.pickTwoPlayers()            
            self.startGame(gamePool[0], player1, player2)
            player1.start()
            player2.start()
            
    def waitForOpenGame(self):
        self.spectateRandomGame()
        while len(this.openGamePool) == 0 or len(this.waitingPlayers) < 2:
            pass
        
    def pickTwoPlayers(self):
        tempPlayerList = [x for x in self.waitingPlayers]
        choiceOne = random.randint(0, len(self.tempPlayerList) - 1)
        player1 = tempPlayerList.pop(choiceOne)
        choiceTwo = random.randint(0, len(self.tempPlayerList) - 1)
        player2 = tempPlayerList.pop(choiceTwo)
        return player1, player2

    def startGame(self, game, player1, player2):
        self.setGameToClosed(game)
        self.addPlayerToGame(game, player1)
        self.addPlayerToGame(game, player2)
        
        self.setPlayerStatusToInGame(player1)
        self.setPlayerStatusToInGame(player2)
        
    def addPlayerToGame(self, game, player):
        self.setPlayerStatusToInGame(player)
        game.addPlayer(player)
    
        
    def setGameToClosed(self, game):
        self.closedGamePool.append(game)
        self.openGamePool.remove(game)
        game.prepareForNewGame()

    def setPlayerStatusToInGame(self, player):
        self.playersInGame.append(player)
        self.waitingPlayers.remove(player)
        

    def spectateRandomGame(self):
        if self.spectatingGame is None:
            length = len(self.closedGamePool)
            self.spectatingGame = self.closedGamePool[random.randint(0, length - 1)]
            self.spectatingGame.viewGame = True
        else:
            if self.spectatingGame.winner != None:
                self.spectatingGame = None
    
    def addNewPlayer(self, newPlayer):
        self.waitingPlayers.append(newPlayer)
        
    def removePlayer(self, player):
        if player in self.waitingPlayers:
            self.waitingPlayers.remove(player)

        else:
            game = findGameThePlayerIsIn(player)
            stopGameInProgress(game)
            

    def resetFinishedGames(self):
        for game in self.closedGamePool:
            if game.winner != None:
                self.resetFinishedGame(game)

    def resetFinishedGame(self, game):
        self.closedGamePool.remove(game)
        self.openGamePool.append(game)
        game.prepareForNewGame()
        
    
if __name__ == "__main__":
    

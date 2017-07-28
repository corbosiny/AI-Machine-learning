import random
from connect4GameViewer import Connect4GameViewer
from connect4 import Connect4Game
from connect4PlayerRandom import Connect4PlayerRandom

class GameMaster():


    def __init__(self, gamePool, players, spectateGames = False):
        self.games = gamePool
        self.openGamePool = gamePool
        self.closedGamePool = []
        self.waitingPlayers = players
        self.playersInGame = []
        self.startAllGames()
        
        self.spectateGames = spectateGames
        self.initTournamentViewer()
        self.runGames = True
        self.manageGames()
        
    def manageGames(self):
        while self.runGames:
            self.waitForOpenGame()
            player1, player2 = self.pickTwoPlayers() 
            self.startGame(self.openGamePool[0], player1, player2)

    def startAllGames(self):
        while len(self.openGamePool) != 0 and len(self.waitingPlayers) > 2:
            player1, player2 = self.pickTwoPlayers()            
            self.startGame(self.openGamePool[0], player1, player2)

            
    def waitForOpenGame(self):
        while len(self.openGamePool) == 0 or len(self.waitingPlayers) < 2:
            self.tournamentViewer.updateGames()
            self.resetFinishedGames()

    def pickTwoPlayers(self):
        tempPlayerList = [x for x in self.waitingPlayers]
        choiceOne = random.randint(0, len(tempPlayerList) - 1)
        player1 = tempPlayerList.pop(choiceOne)
        choiceTwo = random.randint(0, len(tempPlayerList) - 1)
        player2 = tempPlayerList.pop(choiceTwo)
        return player1, player2

    def startGame(self, game, player1, player2):
        self.setGameToClosed(game)
        self.addPlayerToGame(game, player1)
        self.addPlayerToGame(game, player2)

    def setGameToClosed(self, game):
        self.closedGamePool.append(game)
        self.openGamePool.remove(game)
        
    def addPlayerToGame(self, game, player):
        self.setPlayerStatusToInGame(player)
        game.addPlayer(player)


    def setPlayerStatusToInGame(self, player):
        self.playersInGame.append(player)
        self.waitingPlayers.remove(player)
        


    def initTournamentViewer(self):
        self.tournamentViewer = Connect4GameViewer(self)
        self.tournamentViewer.start()
        while len(self.tournamentViewer.textBoxes) != len(self.games):
            pass


    def addNewPlayerToPool(self, newPlayer):
        self.waitingPlayers.append(newPlayer)

    def removePlayerFromPool(self, player):
        while player not in self.waitingPlayers:
            pass
        self.waitingPlayers.remove(player)
    

    def resetFinishedGames(self):
        for game in self.closedGamePool:
            if not game.gameIsNotOver():
                self.resetFinishedGame(game)

    def resetFinishedGame(self, game):
        self.closedGamePool.remove(game)
        self.openGamePool.append(game)
        players = game.players
        game.prepareForNewGame()
        self.setPlayerStatusToWaiting(players[0])
        self.setPlayerStatusToWaiting(players[1])
        

    def setPlayerStatusToWaiting(self, player):
        self.waitingPlayers.append(player)
        self.playersInGame.remove(player)
    
if __name__ == "__main__":
    players = [Connect4PlayerRandom() for x in range(10)]
    games = [Connect4Game() for x in range(5)]
    master = GameMaster(games, players)
    

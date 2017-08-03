import random
import threading
from connect4GameViewer import Connect4GameViewer
from connect4 import Connect4Game
from connect4PlayerRandom import Connect4PlayerRandom

class GameMaster(threading.Thread):


    def __init__(self, gamePool, players, continueTournament = True):
        self.openGamePool = gamePool
        self.closedGamePool = []
        
        self.waitingPlayers = players
        self.playersInGame = []

        self.continueTournament = continueTournament
        super(GameMaster, self).__init__()
        
    def run(self):
        self.initTournamentViewer()
        while True:
            while self.continueTournament:
                self.startAllGames()
                self.waitForAllGamesToFinish()

            while not self.continueTournament:
                pass


    def startAllGames(self):
        while len(self.openGamePool) != 0 and len(self.waitingPlayers) >= 2:
            player1, player2 = self.pickTwoWaitingPlayers()            
            self.startGame(self.openGamePool[0], player1, player2)

            
    def waitForAllGamesToFinish(self):
        while len(self.closedGamePool) != 0:
            self.resetFinishedGames()

    def pickTwoWaitingPlayers(self):
        tempPlayerList = [player for player in self.waitingPlayers]
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
        self.gameViewers = [Connect4GameViewer(x) for x in self.openGamePool]
        for viewer in self.gameViewers:
            viewer.start()

    def shutOffTournamentViewer(self):
        for viewer in self.gameViewers:
            viewer.close()

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
    players = [Connect4PlayerRandom(x) for x in range(12)]
    games = [Connect4Game() for x in range(6)]
    master = GameMaster(games, players)
    master.start()

    while True:
        command = input(str(">>"))
        if command == "pause":
            print('pausing tournament after this round')
            master.continueTournament = False
        elif command == "start":
            print('resuming tournament, staring next round')
            master.continueTournament = True
        elif command == "view wins":
            for player in master.waitingPlayers + master.playersInGame:
                print("Player %d: " % player.playerID, player.wins)
    
        

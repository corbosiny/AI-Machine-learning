import random
import threading
from connect4GameViewer import Connect4GameViewer
from connect4 import Connect4Game
from connect4PlayerRandom import Connect4PlayerRandom
from connect4ProbabilityPlayer import Connect4ProbabilityPlayer

class GameMaster(threading.Thread):


    def __init__(self, gamePool, players, continueTournament = True):
        self.openGamePool = [game for game in gamePool]
        self.closedGamePool = []
        
        self.waitingPlayers = [player for player in players]
        self.playersInGame = []

        self.continueTournament = continueTournament
        self.roundsRun = 0
        super(GameMaster, self).__init__()
        
    def run(self):
        self.initTournamentViewer()
        while True:
            while self.continueTournament:
                self.startAllGames()
                self.waitForAllGamesToFinish()

            while not self.continueTournament:
                pass


    def initTournamentViewer(self):
        self.gameViewers = [Connect4GameViewer(x) for x in self.openGamePool]
        for viewer in self.gameViewers:
            viewer.start()


    def startAllGames(self):
        self.roundsRun += 1
        while len(self.openGamePool) != 0 and len(self.waitingPlayers) >= 2:
            player1, player2 = self.pickTwoWaitingPlayers()            
            self.startGame(self.openGamePool[0], player1, player2)


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
        player.joinGame(game)


    def setPlayerStatusToInGame(self, player):
        self.playersInGame.append(player)
        self.waitingPlayers.remove(player)
     
            
    def waitForAllGamesToFinish(self):
        while len(self.closedGamePool) != 0:
            self.resetFinishedGames()

        



    def shutOffTournamentViewer(self):
        for viewer in self.gameViewers:
            viewer.close()

    def addNewPlayerToPool(self, newPlayer):
        self.waitingPlayers.append(newPlayer)


    

    def resetFinishedGames(self):
        for game in self.closedGamePool:
            if not game.gameIsNotOver():
                self.resetFinishedGame(game)
        
    def resetFinishedGame(self, game):
        players = [player for player in game.players]
        self.setGameStatusToOpen(game)
        self.setPlayersStatusToWaiting(players)


    def setGameStatusToOpen(self, game):
        self.closedGamePool.remove(game)
        self.openGamePool.append(game)
        game.prepareForNewGame()
        
    def setPlayersStatusToWaiting(self, players):
        for player in players:
            self.setPlayerStatusToWaiting(player)

    def setPlayerStatusToWaiting(self, player):
        self.waitingPlayers.append(player)
        self.playersInGame.remove(player)
        player.prepareForNewGame()


        
if __name__ == "__main__":
    players = [Connect4PlayerRandom(x) for x in range(16)]
    players.append(Connect4ProbabilityPlayer(16))
    
    games = [Connect4Game(False, 10, 10) for x in range(8)]

    for game in games:
        game.start()
    
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
            playerIDs = [player.playerID for player in players]
            currentNumberOfWins = [player.wins for player in players]
            for playerID, numberOfWins in zip(playerIDs, currentNumberOfWins):
                print("Player %d: %d" % (playerID, numberOfWins))
        elif command == "view rounds":
            print("Rounds Run: %d" % master.roundsRun)
    
        

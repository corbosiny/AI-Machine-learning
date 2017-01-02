import connect4
import threading
import random

class Connect4PlayerRandom(threading.Thread):

    def __init__(self, game, playerNum):
        self.game = game
        self.playerNum = playerNum
        self.wins = 0
        super(Connect4PlayerRandom, self).__init__()

    def makeMove(self):
        while self.game.turn != self.playerNum:
            pass

        move = random.randint(0, 5)
        while self.game.board[0][move] != '-':
            move = random.randint(0, 5)
        
        if self.game.winner != None:
            return None
        else:
            self.game.makeMove(move)

    def run(self):
        while True:
            while self.game.winner == None:
                self.makeMove()

            if self.game.winner == self.playerNum:
                self.wins += 1        

            self.game = None
            while self.game == None:
                pass
            
if __name__ == "__main__":
    newGame = connect4.Connect4Game()
    player1 = Connect4Player(newGame, 0)
    player2 = Connect4Player(newGame, 1)
    player1.start()
    player2.start()
    
    while newGame.winner == None:
        pass
    print("Winner: Player %d" % newGame.winner)

import connect4
import threading
import random

class Connect4Player(threading.Thread):

    def __init__(self, game, playerNum):
        self.game = game
        self.playerNum = playerNum
        self.wins = 0
        super(Connect4Player, self).__init__()

    def makeMove(self):
        move = random.randint(0, 5)
        while self.game.board[0][move] != '-':
            move = random.randint(0, 5)
            
        while self.game.turn != self.playerNum:
            pass
        
        if self.game.winner != None:
            return None
        else:
            self.game.makeMove(move)

    def run(self):
        while self.game.winner == None:
            self.makeMove()

        if self.game.winner == self.playerNum:
            self.wins += 1        
    
if __name__ == "__main__":
    newGame = connect4.Connect4Game()
    player1 = Connect4Player(newGame, 0)
    player2 = Connect4Player(newGame, 1)
    player1.start()
    player2.start()
    
    while newGame.winner == None:
        pass
    print("Winner: Player %d" % newGame.winner)
    

from connect4PlayerShell import Connect4PlayerShell

class Connect4HumanPlayer(Connect4PlayerShell):

    def __init__(self):
        super(Connect4HumanPlayer, self).__init__()
        self.start()


    def generateMove(self):
        move = int(input(">>")) - 1
        return move

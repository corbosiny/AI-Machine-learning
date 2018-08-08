import connect4 #Only for testing purposes
from connect4PlayerShell import Connect4PlayerShell

class Connect4HumanPlayer(Connect4PlayerShell):

    def __init__(self, playerID):
        super(Connect4HumanPlayer, self).__init__(playerID)


    def generateMove(self, board):
        try:
            move = int(input(">>")) - 1
            return move
        except:
            return self.generateMove()              #if they enter an invalid move, we ask again


if __name__ == "__main__":
    import connect4PlayerTester
    tester = connect4PlayerTester.PlayerTester(Connect4HumanPlayer)
    assert(tester.testPlayers() == True)
    print("Initial Diagnostics Passed!\n\n")
    
    newGame = connect4.Connect4Game(True)
    newGame.start()
    player1 = Connect4HumanPlayer()
    player2 = Connect4HumanPlayer()

    while True:
        player1.joinGame(newGame)
        player2.joinGame(newGame)

        while newGame.gameIsNotOver():
            pass
            

        newGame.prepareForNewGame()

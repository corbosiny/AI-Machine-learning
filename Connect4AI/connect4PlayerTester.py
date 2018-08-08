from connect4 import Connect4Game #Only for testing purposes

DEFAULT_BOARD_LENGTH = 7
DEFAULT_BOARD_HEIGHT = 6

class PlayerTester():

    def __init__(self, ClassToTest, playerSymbols= ['X', 'O'], playerIDs = [1, 2], boardDimensions= [DEFAULT_BOARD_LENGTH, DEFAULT_BOARD_HEIGHT]):
        self.ClassToTest = ClassToTest
        self.playerSymbols = playerSymbols
        self.playerIDs = playerIDs
        self.boardDimensions = boardDimensions
        
    def checkPlayerVariablesAreValid(self, player, playerNum):
        assert(player.playerSymbol == self.playerSymbols[playerNum])
        assert(player.playerID == self.playerIDs[playerNum])
        assert(player.wins == 0)
        return True

    def checkIfValidMoves(self, player):
        for i in range(1000):
            move = player.generateMove(self.testGame.board)
            assert(move < self.boardDimensions[0] and move >= 0)
        return True

    def resetIsCorrect(self, player):
        player.prepareForNewGame()
        assert(player.playerSymbol == None)

        return True

    def trainingIsDone(self, player):
        assert(player.doneTraining == True)
        player.train()
        while player.doneTraining == False:
            pass

        assert(player.doneTraining == True)
        
        return True

    def testPlayers(self):
        self.testGame = Connect4Game(True, self.boardDimensions[0], self.boardDimensions[1])
        self.testGame.playerSymbols = self.playerSymbols
        player1 = self.ClassToTest(self.playerIDs[0])
        player2 = self.ClassToTest(self.playerIDs[1])
        player1.joinGame(self.testGame)
        player2.joinGame(self.testGame)

        assert(self.checkPlayerVariablesAreValid(player1, 0) == True)
        assert(self.checkPlayerVariablesAreValid(player2, 1) == True)

        assert(self.checkIfValidMoves(player1) == True)
        assert(self.checkIfValidMoves(player2) == True)

        assert(self.resetIsCorrect(player1) == True)
        assert(self.resetIsCorrect(player2) == True)


        assert(self.trainingIsDone(player1) == True)
        assert(self.trainingIsDone(player2) == True)
        
        return True
    
if __name__ == "__main__":
    ##Import and replace this line with the desired class to test

    import connect4PlayerShell
    tester = PlayerTester(connect4PlayerShell.Connect4PlayerShell)
    assert(tester.testPlayers() == True)
    print("Diagnostics Passed!")

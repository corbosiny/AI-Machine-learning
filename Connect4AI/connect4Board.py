defaultBoardLength = 7
defaultBoardHeight = 6

class Connect4Board():
    
    def __init__(self, length= defaultBoardLength, height= defaultBoardHeight):
        self.boardLength = length
        self.boardHeight = height
        self.clearBoard()
        
    def clearBoard(self):
        self.rows = [['-' for x in range(self.boardLength)] for y in range(self.boardHeight)]
        self.lastMove = []

    def updateBoard(self, column, sym):
        self.checkIfInvalidMove(column)
        row = self.calculateLastMovesRow(column)
        self.rows[row][column] = sym
        self.lastMove = [row, column]

    def checkIfInvalidMove(self, column):
        if column > self.boardLength - 1 or column < 0:                     
            raise InvalidMoveError('Invalid move %d, not in column range' % (column))
            return True

        if self.rows[0][column] != '-':
            raise InvalidMoveError('Invalid move %d, not an open column' % (column))
            return True
        
        return False

    def calculateLastMovesRow(self, column):
        row = self.boardHeight - 1
        while self.rows[row][column] != '-':
            row -= 1
        return row

    def checkWin(self):
        if self.checkHorizontal():
            return True
        if self.checkVertical():
            return True
        if self.checkDiagnols():
            return True
        return False


    def checkHorizontal(self):                                                 
        results = []
        currentColumn = self.lastMove[1]
        if currentColumn < self.boardLength - 3:
            results.append(self.checkThreeInARow(0, 1))

        if currentColumn > 2:
            results.append(self.checkThreeInARow(0, -1))

        if currentColumn < self.boardLength - 2 and currentColumn != 0:
            results.append(self.checkIfInMiddleOfFour(0, 1))

        if currentColumn > 1 and currentColumn != self.boardLength - 1:
            results.append(self.checkIfInMiddleOfFour(0, -1))	

        return max(results)

    
    def checkVertical(self):                       
        if self.lastMove[0] > 2:
            return False
        else:
            return self.checkThreeInARow(1, 0)
        

    def checkDiagnols(self):
        return max(self.checkLeftDiagnols(), self.checkRightDiagnols())
    
    def checkRightDiagnols(self):              
        return max(self.checkUpperRightDiagnol(), self.checkLowerRightDiagnol())

    def checkUpperRightDiagnol(self):
        results = [False]
        currentRow, currentColumn = self.lastMove
    
        if currentRow > 2 and currentColumn < self.boardLength - 3:
            results.append(self.checkThreeInARow(-1, 1))

        if (currentRow > 1 and currentRow != self.boardHeight - 1) and (currentColumn < self.boardLength - 2 and currentColumn != 0):
            results.append(self.checkIfInMiddleOfFour(-1, 1))
        
        return max(results)

    def checkLowerRightDiagnol(self):
        results = [False]
        currentRow, currentColumn = self.lastMove
        
        if currentRow < self.boardHeight - 3 and currentColumn < self.boardLength - 3:
            results.append(self.checkThreeInARow(1, 1))

        if (currentRow < self.boardHeight - 2 and currentRow != 0) and (currentColumn < self.boardLength - 2 and currentColumn != 0):
            results.append(self.checkIfInMiddleOfFour(1, 1))

        return max(results)
        
    def checkLeftDiagnols(self):                
        return max(self.checkUpperLeftDiagnol(), self.checkLowerLeftDiagnol())

    def checkUpperLeftDiagnol(self):
        results = [False]
        currentRow, currentColumn = self.lastMove
        if currentRow > 2 and currentColumn > 2:
            results.append(self.checkThreeInARow(-1, -1))
            
        if (currentRow > 1 and currentRow != self.boardHeight - 1) and (currentColumn > 1 and currentColumn != self.boardLength - 1):
            results.append(self.checkIfInMiddleOfFour(-1, -1))

        return max(results)
    
    def checkLowerLeftDiagnol(self):
        results = [False]
        currentRow, currentColumn = self.lastMove
        if currentRow < self.boardHeight - 3 and currentColumn > 2:
            results.append(self.checkThreeInARow(1, -1))

        if (currentRow < self.boardHeight - 2 and currentRow != 0) and (currentColumn > 1 and currentColumn != self.boardLength - 1):
            results.append(self.checkIfInMiddleOfFour(1, -1))
            
        return max(results)


    def checkThreeInARow(self, rowOffset, columnOffset):
        sym = self.rows[self.lastMove[0]][self.lastMove[1]]
        for i in range(1, 4):
            if self.rows[self.lastMove[0] + rowOffset * i][self.lastMove[1] + columnOffset * i] != sym or sym == '-':
                return False
        return True
            
    
    def checkIfInMiddleOfFour(self, rowOffset, columnOffset):
        sym = self.rows[self.lastMove[0]][self.lastMove[1]]
        for i in range(-1, 3):
            if self.rows[self.lastMove[0] + rowOffset * i][self.lastMove[1] + columnOffset * i] != sym or sym == '-':
                return False
        return True

    def __getitem__(self, key):
        return self.rows[key]

    def __setitem__(self, key, item):
        self.rows[key] = item

    def __iter__(self):
        for row in self.rows:
            yield row

    def __len__(self):
        return len(self.rows)
    
    def __str__(self):         
        boardStr = ''
        for row in self.rows:           #printing out rows
            boardStr += str(row)
            boardStr += '\n'
        boardStr += "[ 1"
        for col in range(1, self.boardLength): #adding in column nums
            boardStr += "    " + str(col + 1) 
        boardStr += ' ]\n\n'
        return boardStr 


class InvalidMoveError(Exception):

    def __init__(self, message):
        super(InvalidMoveError, self).__init__(message)

def checkBoardWorking(board):
    checkHorizontalWorking(board)
    checkVerticalWorking(board)
    checkDiagnolsWorking(board)
    checkInvalidMoves(board)
    
def checkHorizontalWorking(board):
    for row in range(board.boardHeight):
        for column in range(board.boardLength - 3):
            for i in range(column, column + 4):
                board.rows[row][i] = 'X'
            for j in range(column, column + 4):
                board.lastMove = [row, j]
                assert(board.checkWin() == True)
            board.clearBoard()        

def checkVerticalWorking(board):
    for column in range(board.boardLength):
        for row in range(board.boardHeight):
            board.updateBoard(column, 'X')
            if(row > 2):
                assert(board.checkWin() == True)
        board.clearBoard()
    
def checkDiagnolsWorking(board):
    checkLeftDiagnolWorking(board)
    checkRightDiagnolWorking(board)

def checkLeftDiagnolWorking(board):
    for column in range(board.boardLength - 3):
        for row in range(board.boardHeight - 1, 2, -1):
            for i in range(0, 4):
                board.rows[row - i][column + i] = 'X'
            for j in range(0, 4):
                board.lastMove = [row - j, column + j]
                assert(board.checkWin() == True)
            board.clearBoard()
                
    board.clearBoard()
    
def checkRightDiagnolWorking(board):
    for column in range(board.boardLength - 3):
        for row in range(board.boardHeight - 3):
            for i in range(0, 4):
                board.rows[row + i][column + i] = 'X'
            for j in range(0, 4):
                board.lastMove = [row + j, column + j]
                assert(board.checkWin() == True)
            board.clearBoard()
    board.clearBoard()

def checkInvalidMoves(board):
    try:
        board.checkWin()
        raise('Check win did not return error with empty board')
    except:
        pass
    assert(checkInvalidMove(board, board.boardLength) == True)
    board.clearBoard()
    assert(checkInvalidMove(board, -1) == True)
    board.clearBoard()
    for column in range(board.boardLength):
        for row in range(board.boardHeight):
            assert(checkInvalidMove(board, column) == False)
        assert(checkInvalidMove(board, column) == True)
        
    board.clearBoard()

def checkInvalidMove(board, move):
    try:
        board.updateBoard(move, 'X')
        return False
    except:
        return True
    

if __name__ == "__main__":
    newBoard = Connect4Board()
    checkBoardWorking(newBoard)
    print("Board diagnostics passed!")

class Connect4Board():
    
    def __init__(self):
        self.clearBoard()
        
    def clearBoard(self):
        self.rows = [['-' for x in range(6)] for y in range(6)]
        self.lastMove = []

    def updateBoard(self, column, sym):
        self.checkIfInvalidMove(column)
        row = self.calculateLastMovesRow(column)
        self.rows[row][column] = sym
        self.lastMove = [row, column]

    def checkIfInvalidMove(self, column):
        if column > 5 or column < 0 or not isinstance(column, int):                     
            raise InvalidMoveError('Invalid move: %d by current player, not in column range' % (column))
            return True

        if self.rows[0][column] != '-':
            raise InvalidMoveError('Invalid move %d by current player, not an open column' % (column))
            return True
        
        return False

    def calculateLastMovesRow(self, column):
        row = 5
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
        if currentColumn < 3:
            results.append(self.checkThreeInARow(0, 1))

        if currentColumn > 2:
            results.append(self.checkThreeInARow(0, -1))

        if currentColumn < 4 and currentColumn != 0:
            results.append(self.checkIfInMiddleOfFour(0, 1))

        if currentColumn > 1 and currentColumn != 5:
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
    
        if currentRow > 2 and currentColumn < 3:
            results.append(self.checkThreeInARow(-1, 1))

        if (currentRow > 1 and currentRow != 5) and (currentColumn < 4 and currentColumn != 0):
            results.append(self.checkIfInMiddleOfFour(-1, 1))
        
        return max(results)

    def checkLowerRightDiagnol(self):
        results = [False]
        currentRow, currentColumn = self.lastMove
        
        if currentRow < 3 and currentColumn < 3:
            results.append(self.checkThreeInARow(1, 1))

        if (currentRow < 4 and currentRow != 0) and (currentColumn < 4 and currentColumn != 0):
            results.append(self.checkIfInMiddleOfFour(1, 1))

        return max(results)
        
    def checkLeftDiagnols(self):                
        return max(self.checkUpperLeftDiagnol(), self.checkLowerLeftDiagnol())

    def checkUpperLeftDiagnol(self):
        results = [False]
        currentRow, currentColumn = self.lastMove
        if currentRow > 2 and currentColumn > 2:
            results.append(self.checkThreeInARow(-1, -1))
            
        if (currentRow > 1 and currentRow != 5) and (currentColumn > 1 and currentColumn != 5):
            results.append(self.checkIfInMiddleOfFour(-1, -1))

        return max(results)
    
    def checkLowerLeftDiagnol(self):
        results = [False]
        currentRow, currentColumn = self.lastMove
        if currentRow < 3 and currentColumn > 2:
            results.append(self.checkThreeInARow(1, -1))

        if (currentRow < 4 and currentRow != 0) and (currentColumn > 1 and currentColumn != 5):
            results.append(self.checkIfInMiddleOfFour(1, -1))
            
        return max(results)


    def checkThreeInARow(self, rowOffset, columnOffset):
        if sym is None:
            sym = self.rows[self.lastMove[0]][self.lastMove[1]]

        for i in range(1, 4):
            if self.rows[self.lastMove[0] + rowOffset * i][self.lastMove[1] + columnOffset * i] != sym or sym == '-':
                return False
        return True
            
    
    def checkIfInMiddleOfFour(self, rowOffset, columnOffset):
        if sym is None:
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
        for row in self.rows:
            boardStr += str(row)
            boardStr += '\n'
        boardStr += "[ 1    2    3    4    5    6 ]\n\n"
        return boardStr 


class InvalidMoveError(Exception):

    def __init__(self, message):
        super(InvalidMoveError, self).__init__(message)

if __name__ == "__main__":
    newBoard = Connect4Board()
    print(newBoard)
    newBoard.rows[2][0] = 'X'
    newBoard.rows[3][1] = 'X'
    newBoard.rows[4][2] = 'X'
    newBoard.rows[5][3] = 'X'
    print(newBoard)
    newBoard.lastMove = [5,3]
    print(newBoard.checkWin())

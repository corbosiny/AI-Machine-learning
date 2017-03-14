import matrix

class SudokuPlayer():

    def __init__(self, board, solution):
        self.board = board
        self.solution = solution
        self.ideas = board.makeCopy()
        self.changes = True
        self.guesses = []
        self.badGuesses = []
        for i in range(board.rows):
            for j in range(board.columns):
                if board[i][j] == 0:
                    self.ideas[i][j] = []

    def play(self):
        while not self.checkSolution():
            if self.changes == True:
                self.changes = False
            else:
                return 'COULD NOT SOLVE'

            self.subMatrices = []
            self.allIdeas = []
            self.rowIdeas = self.analyzeRows()
            self.allIdeas.append(self.rowIdeas)
            self.colIdeas = self.analyzeColumns()
            self.allIdeas.append(self.colIdeas)
            self.squareIdeas = self.analyzeSubMatrices()
            self.allIdeas.append(self.squareIdeas)
            #print()
            #print('Ideas:')
            #for idea in self.allIdeas:
            #    print(idea ,end = '\n\n')

            for num in self.badGuesses:
                i, j = num[:2]
                try:
                    for idea in self.ideas:
                        try:
                            if isinstance(idea[i][j], list):
                                idea[i][j].remove(num[-1])
                        except:
                            pass
                    if isinstance(ideas[i][j], list):
                        self.ideas[i][j].remove(num[-1])
                except:
                    pass

            #print()
            self.combineIdeas()
            #print()
            #print('Combined Ideas:')
            #print(self.ideas)
            #print()
            self.cleanUpRows()
            self.cleanUpColumns()
            self.cleanUpSubMatrices()
            #print()
            #print('Cleaned Up Ideas:')
            #print(self.ideas)
            #print()
            self.guess()
            #print('_' * 30)
            #input('')

        return self.checkSolution()

    def clearRow(self, i, num, ideas):
        for j in range(ideas.columns):
            if isinstance(ideas[i][j], list):
                try:
                    values = []
                    for elem in ideas[i][j]:
                        values.append(elem)
                    values.remove(num)
                    ideas[i][j] = values
                except:
                    pass

        return ideas

    def clearColumn(self, j, num, ideas):
        for i in range(ideas.rows):
            if isinstance(ideas[i][j], list):
                try:
                    values = []
                    for elem in ideas[i][j]:
                        values.append(elem)
                    values.remove(num)
                    ideas[i][j] = values
                except:
                    pass

        return ideas

    def clearSubMatrix(self, i, j, num, ideas):
        subMatrixRow = int(i / 3)
        subMatrixColumn = int(j / 3)
        subMatrix = ideas.subMatrix([subMatrixRow * 3, subMatrixRow * 3 + 2],[subMatrixColumn * 3, subMatrixColumn * 3 + 2])
        for i in range(3):
            for j in range(3):
                if isinstance(subMatrix[i][j], list):
                    try:
                        values = []
                        for elem in ideas[i + subMatrixRow * 3][j + subMatrixColumn * 3]:
                            values.append(elem)
                        values.remove(num)
                        subMatrix[i][j] = values
                        ideas[i + subMatrixRow * 3][j + subMatrixColumn * 3] = values
                    except:
                        pass
        return ideas

    def analyzeRows(self):
        ideaCopy = self.ideas.makeCopy()
        for i, row in enumerate(ideaCopy.matrix):
            leftOver = [1,2,3,4,5,6,7,8,9]
            for elem in row:
                if isinstance(elem, int):
                    try:
                        leftOver.remove(elem)
                    except:
                        pass

            for j, elem in enumerate(row):
                if isinstance(elem, list):
                    ideaCopy[i][j] = leftOver
                    if len(leftOver) == 1:
                        ideaCopy[i][j] = leftOver[0]
                        self.ideas[i][j] = leftOver[0]
                        self.board[i][j] = leftOver[0]
                        self.guesses.append([i, j, leftOver[0], 0])
                        #print('found one!')
                        self.changes = True
                        #if self.board[i][j] != self.solution[i][j]:
                        #  print('FALSE ANSWER HERE ROWS!!!!!!!!')
                        #print(i, j, leftOver[0])
                        ideaCopy = self.clearColumn(j, leftOver[0], ideaCopy)
                        ideaCopy = self.clearSubMatrix(i, j, leftOver[0], ideaCopy)

        return ideaCopy

    def analyzeColumns(self):
        ideaCopy = self.ideas.makeCopy()
        for j in range(self.ideas.columns):
            leftOver = [1,2,3,4,5,6,7,8,9]
            for i in range(self.ideas.rows):
                if isinstance(self.ideas[i][j], int):
                    try:
                        leftOver.remove(self.ideas.matrix[i][j])
                    except:
                        pass

            for i in range(self.ideas.rows):
                if isinstance(self.ideas.matrix[i][j], list):
                    ideaCopy[i][j] = leftOver
                    if len(leftOver) == 1:
                        ideaCopy[i][j] = leftOver[0]
                        self.ideas[i][j] = leftOver[0]
                        self.board[i][j] = leftOver[0]
                        self.guesses.append([i, j, leftOver[0], 0])
                        #self.rowIdeas[i][j] = leftOver[0]
                        ideaCopy = self.clearRow(i, leftOver[0], ideaCopy)
                        ideaCopy = self.clearSubMatrix(i, j, leftOver[0], ideaCopy)
                        #if self.board[i][j] != self.solution[i][j]:
                        #    print('FALSE ANSWER HERE COLUMNS!!!!!!!!!')
                        #print('found one!')
                        self.changes = True
                        #print(i, j, leftOver[0])

        return ideaCopy

    def analyzeSubMatrices(self):
        ideaCopy = self.ideas.makeCopy()
        for rows in range(0, self.board.rows - 2, 3):
            for columns in range(0, self.board.columns - 2, 3):
                subMatrix = self.ideas.subMatrix([rows, rows + 2],[columns, columns + 2])
                self.subMatrices.append(subMatrix)
                leftOver = [1,2,3,4,5,6,7,8,9]
                for row in subMatrix.matrix:
                    for elem in row:
                        if isinstance(elem, int):
                            try:
                                leftOver.remove(elem)
                            except:
                                pass
                for i, row in enumerate(subMatrix.matrix):
                    for j, elem in enumerate(row):
                        if isinstance(elem, list):
                            ideaCopy[i + rows][j + columns] = leftOver
                            if len(leftOver) == 1:
                                ideaCopy[i + rows][j + columns] = leftOver[0]
                                self.ideas[i + rows][j + columns] = leftOver[0]
                                self.board[i + rows][j + columns] = leftOver[0]
                                self.guesses.append([i + rows, j + columns, leftOver[0], 0])
                                #print('found one!')
                                self.changes = True
                                #if self.board[i + rows][j + columns] != self.solution[i + rows][j + columns]:
                                #    print('FALSE ANSWER HERE Matrices!!!!!!!!')
                                #print(i + rows, j + columns, leftOver[0])
                                ideaCopy = self.clearRow(i + rows, leftOver[0], ideaCopy)
                                ideaCopy = self.clearColumn(j + columns, leftOver[0], ideaCopy)

        return ideaCopy

    def cleanUpRows(self):
        for i in range(self.ideas.rows):
            for j in range(self.ideas.columns):
                if isinstance(self.ideas[i][j], list):
                    for elem in self.ideas[i][j]:
                        onlySpot = True
                        for k in range(self.ideas.columns):
                            if k == j:
                                continue
                            if isinstance(self.ideas[i][k], list) and elem in self.ideas[i][k]:
                                onlySpot = False
                                break
                        if onlySpot:
                            self.changes = True
                            #print('found one!')
                            #print(i,j, elem)
                            self.ideas[i][j] = elem
                            self.board[i][j] = elem
                            self.guesses.append([i, j, elem, 0])
                            self.ideas = self.clearRow(i, elem, self.ideas)
                            self.ideas = self.clearColumn(j, elem, self.ideas)
                            #if self.board[i][j] != self.solution[i][j]:
                             #   print('FALSE ANSWER HERE CLEANING ROWS!!!!!!!!')

    def cleanUpColumns(self):
        for j in range(self.ideas.columns):
            for i in range(self.ideas.rows):
                if isinstance(self.ideas[i][j], list):
                    for elem in self.ideas[i][j]:
                        onlySpot = True
                        for k in range(self.ideas.rows):
                            if k == i:
                                continue
                            if isinstance(self.ideas[k][j], list) and elem in self.ideas[k][j]:
                                onlySpot = False
                                break
                        if onlySpot:
                            self.changes = True
                            #print('found one!')
                            #print(i,j, elem)
                            self.ideas[i][j] = elem
                            self.board[i][j] = elem
                            self.guesses.append([i, j, elem, 0])
                            self.ideas = self.clearRow(i, elem, self.ideas)
                            self.ideas = self.clearColumn(j, elem, self.ideas)
                            #if self.board[i][j] != self.solution[i][j]:
                            #    print('FALSE ANSWER HERE CLEANING COLUMNS!!!!!!!!')

    def cleanUpSubMatrices(self):
        for i in range(0, self.ideas.rows - 3, 3):
            for j in range(0, self.ideas.columns - 3, 3):
                subMatrix = self.ideas.subMatrix([i, i+2], [j, j+2])
                for row in range(0, 3):
                    for column in range(0, 3):
                        if isinstance(subMatrix[row][column], list):
                            for elem in subMatrix[row][column]:
                                onlySpot = True
                                for x in range(0, 3):
                                    for y in range(0, 3):
                                        if x == row and y == column:
                                            continue
                                        if isinstance(subMatrix[x][y], list) and elem in subMatrix[x][y]:
                                            onlySpot = False
                                            break
                                    if not onlySpot:
                                        break

                                if onlySpot:
                                    self.changes = True
                                    #print('found one!')
                                    #print(i + row,j + column, elem)
                                    self.ideas[i + row][j + column] = elem
                                    self.board[i + row][j + column] = elem
                                    self.guesses.append([i + row, j + column, elem, 0])
                                    self.ideas = self.clearRow(i + row, elem, self.ideas)
                                    self.ideas = self.clearColumn(j + column, elem, self.ideas)
                                    #if self.board[i + row][j + column] != self.solution[i + row][j + column]:
                                     #   print('FALSE ANSWER HERE CLEANING SUBMATRIX!!!!!!!!')

    def guess(self):
        if self.changes == False:
                for i in range(self.ideas.rows):
                    for j in range(self.ideas.columns):
                        noGuessesLeft = True
                        if isinstance(self.ideas[i][j], list) and len(self.ideas[i][j]) > 0:
                            noGuessesLeft = False
                            break
                        
                if not noGuessesLeft:
                    guess = self.ideas[i][j][0]
                    self.ideas[i][j] = guess
                    self.board[i][j] = guess
                    self.changes = True
                    self.guesses.append([i, j, guess, 1])
                    
                else:
                    checkingFailure = [x[-1] for x in self.guesses]
                    if 1 not in checkingFailure:
                        return None
                    try:
                        lastGuess = [0]
                        while lastGuess[-1] != 1:
                            lastGuess = self.guesses.pop()
                            self.board[lastGuess[0]][lastGuess[1]] = 0
                            self.ideas[lastGuess[0]][lastGuess[1]] = []
                        self.badGuesses.append(lastGuess[:3])
                        self.changes = True
                    except:
                        pass #will allow the cant be solved flag to trigger

    def combineIdeas(self):
        for i in range(len(self.board.matrix)):
            for j in range(len(self.board.matrix[0])):
                if self.board[i][j] == 0:
                    found = False
                    for num, idea in enumerate(self.allIdeas):
                        if isinstance(idea[i][j], int):
                            self.ideas[i][j] = idea[i][j]
                          #  print('FOUND!')
                            break
                    if found:
                        self.rowIdeas[i][j] = idea[i][j]
                        self.colIdeas[i][j] = idea[i][j]
                        self.squareIdeas[i][j] = idea[i][j]
                        self.changes = True
                        continue

                    leftOver = [x for x in range(1,10)]
                    for x in range(1, 10):
                        for idea in self.allIdeas:
                            if x not in idea[i][j]:
                                leftOver.remove(x)
                                break
                    self.ideas[i][j] = leftOver

        for i in range(self.ideas.rows):
            for j in range(self.ideas.columns):
                if self.board[i][j] == 0:
                    change = False
                    if len(self.ideas[i][j]) == 1:
                        self.guesses.append([i, j, self.ideas[i][j][0], 0])
                        self.board[i][j] = self.ideas[i][j][0]
                        self.ideas[i][j] = self.ideas[i][j][0]
                        #print('found one!')
                        #if self.board[i][j] != self.solution[i][j]:
                        #    print('FALSE ANSWER HERE COMBINING!!!!!!!!')
                        #    print(self.rowIdeas[i][j], self.colIdeas[i][j], self.squareIdeas[i][j])
                        self.changes = True
                        change = True
                        #print(i, j, self.ideas[i][j])
                        #print()

                    if change:
                        self.ideas = self.clearRow(i, self.ideas[i][j], self.ideas)
                        self.ideas = self.clearColumn(j, self.ideas[i][j], self.ideas)
                        self.ideas = self.clearSubMatrix(i, j, self.ideas[i][j], self.ideas)
                        #print()
                        for y in range(len(self.allIdeas)):
                            self.allIdeas[y][i][j] = self.ideas[i][j]
                            self.allIdeas[y] = self.clearRow(i, self.ideas[i][j], self.allIdeas[y])
                            self.allIdeas[y] = self.clearColumn(j, self.ideas[i][j], self.allIdeas[y])
                            self.allIdeas[y] = self.clearSubMatrix(i, j, self.ideas[i][j], self.allIdeas[y])

    def checkSolution(self):
        for i in range(self.board.rows):
            for j in range(self.board.columns):
                if self.board[i][j] != self.solution[i][j]:
                    return False
        return True

if __name__ == "__main__":
    #board = matrix.Matrix([[0,0,8,0,0,0,6,0,0],[0,2,0,7,0,6,0,1,0],[9,0,0,0,0,0,0,0,4],[0,9,0,3,0,2,0,5,0], [0,0,0,0,9,0,0,0,0],[0,8,0,4,0,1,0,9,0], [8,0,0,0,0,0,0,0,5], [0,3,0,9,0,7,0,2,0], [0,0,6,0,0,0,3,0,0]])
    #boardCopy = board.makeCopy()
    #solut = matrix.Matrix([[7,5,8,1,4,9,6,3,2], [4,2,3,7,5,6,9,1,8], [9,6,1,8,2,3,5,7,4], [1,9,7,3,8,2,4,5,6], [3,4,2,6,9,5,1,8,7], [6,8,5,4,7,1,2,9,3], [8,1,9,2,3,4,7,6,5], [5,3,4,9,6,7,8,2,1], [2,7,6,5,1,8,3,4,9]])
    board = matrix.Matrix([[0,2,5,6,0,0,3,7,0],[0,4,0,0,5,3,0,6,2],[0,8,3,2,0,4,0,0,9],[8,0,0,7,0,5,9,2,0],[5,0,2,0,3,0,0,8,7],[3,7,0,4,8,0,0,0,1], [0,0,0,3,9,7,1,0,6],[4,9,0,0,2,0,7,0,0],[7,0,6,5,0,1,2,9,0]])
    boardCopy = board.makeCopy()
    solut = matrix.Matrix([[9,2,5,6,1,8,3,7,4],[1,4,7,9,5,3,8,6,2],[6,8,3,2,7,4,5,1,9],[8,1,4,7,6,5,9,2,3],[5,6,2,1,3,9,4,8,7],[3,7,9,4,8,2,6,5,1],[2,5,8,3,9,7,1,4,6],[4,9,1,8,2,6,7,3,5],[7,3,6,5,4,1,2,9,8]])
    player = SudokuPlayer(board, solut)
    result = player.play()
    print('My Guess:')
    print(player.ideas)
    print()
    print("The solution:")
    print(solut)
    print()
    print(result)

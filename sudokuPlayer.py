import matrix

class SudokuPlayer():

    def __init__(self, board, solution):
        self.board = board
        self.solution = solution
        self.ideas = board.makeCopy()
        for i in range(board.rows):
            for j in range(board.columns):
                if board[i][j] == 0:
                    self.ideas[i][j] = []
        
    def play(self):
        while not self.checkSolution():
            self.subMatrices = []
            print('analyzing rows...')
            self.rowIdeas = self.analyzeRows()
            print('analyzing columns...')
            self.colIdeas = self.analyzeColumns()
            print('analyzing squares...')
            self.squareIdeas = self.analyzeSubMatrices()
            print()
            print('Ideas:')
            print(self.rowIdeas)
            print()
            print(self.colIdeas)
            print()
            print(self.squareIdeas)
            print()
            print("Guesses:")
            print(self.ideas)
            print()
            print("Solution:")
            print(self.solution)
            print()
            
            ideas = [self.rowIdeas, self.colIdeas, self.squareIdeas]
            for i in range(len(self.board.matrix)):
                for j in range(len(self.board.matrix[0])):
                    if isinstance(self.ideas[i][j], list):
                        try:
                            found = False
                            for num, idea in enumerate(ideas):
                                if isinstance(idea[i][j], int):
                                    self.ideas[i][j] = idea[i][j]
                                    found = True
                                    break
                            if found:
                                self.rowIdeas[i][j] = idea[i][j] 
                                self.colIdeas[i][j] = idea[i][j]
                                self.squareIdeas[i][j] = idea[i][j]
                                continue
                            leftOver = [x for x in range(1,10) if x in self.rowIdeas[i][j] and x in self.colIdeas[i][j] and x in self.squareIdeas[i][j]]
                        except:
                            print(i, j)
                            print(self.rowIdeas[i][j])
                            print(self.colIdeas[i][j])
                            print(self.squareIdeas[i][j])
                            print(self.ideas[i][j])
                            raise Exception('FIX THIS')
                        if len(leftOver) == 1:
                            self.board[i][j] = leftOver[0]
                            self.ideas[i][j] = leftOver[0]
                            print('found one!')
                            print(i, j, leftOver[0])
                        else:
                            self.ideas[i][j] = leftOver
##            print(self.ideas)
##            print()
            print('________________________')
        return self.checkSolution()

    def analyzeRows(self):
        ideaCopy = self.ideas.makeCopy()
        for i, row in enumerate(self.ideas.matrix):
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
                        print('found one!')
                        print(i, j, leftOver[0])
        
            
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
                        self.rowIdeas[i][j] = leftOver[0]
                        print('found one!')
                        print(i, j, leftOver[0])
                            
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
                                self.rowIdeas[i + rows][j + columns] = leftOver[0]
                                self.colIdeas[i + rows][j + columns] = leftOver[0]
                                print('found one!')
                                print(i, j, leftOver[0])
        return ideaCopy

    def checkSolution(self):
        for i in range(self.ideas.rows):
            for j in range(self.ideas.columns):
                if self.ideas[i][j] != self.solution[i][j]:
                    return False
        return True
    
if __name__ == "__main__":
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

import matrix

delta = [[-1,0],[0,1],[1, 0],[0,-1]]
deltaMoves = ['^','>','v','<']

class Pather():

    def __init__(self, board, start, goal, cost= 1):
        self.board = board
        self.start = start
        self.goal = goal
        self.cost = cost
        self.bounds = [len(self.board), len(self.board[0])]

    def expandedMap(self, start = None):
        if start == None:
            start = self.start
        return self.valueMap(start, expanding = True)

    def costMap(self, start = None):
        if start == None:
            start = self.start
        return self.valueMap(start, self.cost)
    
    def valueMap(self, start = None, cost= 1, expanding= False):
        if start == None:
            start = self.goal
            
        self.explored = self.board.makeCopy()
        
        for i in range(self.explored.rows):
            for j in range(self.explored.columns):
                if self.explored[i][j] == 0:
                    self.explored[i][j] = ' '
                elif self.explored[i][j] == 1:
                    self.explored[i][j] = -1
        
        self.explored[start[0]][start[1]] = 0        
        frontier = [[0] + start]
        closed = []
        expansionNum = 1
        while len(frontier) > 0:
            frontier.sort()
            baseNode = frontier.pop(0)
            x = baseNode[1]
            y = baseNode[2]
            for num, move in enumerate(delta):
                x2 = x + move[0] 
                y2 = y + move[1]

                if (x2 < self.bounds[0] and x2 >= 0) and (y2 < self.bounds[1] and y2 >= 0):
                    if self.explored[x2][y2] != ' ':
                        pass
                    else:
                        if isinstance(cost, int):
                            newCost = cost
                        elif isinstance(cost, list):
                            newCost = cost[num]
                        else:
                            newCost = cost(x2, y2)
                            
                        frontier.append([baseNode[0] + newCost, x2, y2])
                        if not expanding:
                            self.explored[x2][y2] = baseNode[0] + newCost
                        else:
                            self.explored[x2][y2] = expansionNum
                            expansionNum += 1
                        
            closed.append(baseNode)

        return self.explored

        
    def __str__(self):
        return str(self.board)
    
class BreadthFirst(Pather):
            
        return self.explored
    
##class A*(Pather):
##
##    def __init__():
##
##
##class OptimumPolicy(Pather):
##
##    def __init__():


if __name__ == "__main__":
    maze = matrix.Matrix([[0,1,1,1],[0,1,0,1],[0,0,0,0],[0,0,1,0]])
    start = [0,0]
    goal = [len(maze) - 1, len(maze[0]) - 1]
    pather = BreadthFirst(maze, start, goal)
    print(pather.valueMap(start))

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
        self.valueMap(start)
        return self.expanding

    def costMap(self, start = None):
        if start == None:
            start = self.start
        return self.valueMap(start, self.cost)
    
    def valueMap(self, start = None, cost= 1):
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
        self.expanding = self.explored.makeCopy()
        frontier = [[0] + start]
        closed = []
        expansionNum = 1
        while len(frontier) > 0:
            frontier.sort()
            baseNode = frontier.pop(0)
            x,y = baseNode[1:]
            for num, move in enumerate(delta):
                x2 = x + move[0] 
                y2 = y + move[1]

                if (x2 < self.bounds[0] and x2 >= 0) and (y2 < self.bounds[1] and y2 >= 0):
                    if self.explored[x2][y2] != ' ':
                        pass
                    else:
                        if isinstance(cost, int) or isinstance(cost, float):
                            newCost = cost
                        elif isinstance(cost, list):
                            newCost = cost[num]
                        else:
                            newCost = cost(x2, y2)
                            
                        frontier.append([baseNode[0] + newCost, x2, y2])
                        self.explored[x2][y2] = baseNode[0] + newCost
                        self.expanding[x2][y2] = expansionNum
                        expansionNum += 1
                        
            closed.append(baseNode)

        return self.explored


    def bestMove(self, values, currentNode):
        moves = []
        mins = []
        x,y = currentNode
        if currentNode == self.goal:
            return '*', [x,y]
        for num, move in enumerate(delta):
            if x == 3 and y == 1:
                print("Move: ", move)
            x2 = x + move[0]
            y2 = y + move[1]
            if x2 >= 0 and x2 < len(values) and y2 >= 0 and y2 < len(values[0]):
                value = values[x2][y2]
                if x == 3 and y == 1:
                    print('Value: ', value)
                if (isinstance(value, int) or isinstance(value, float)) and value >= 0:
                    mins.append(value)
                    moves.append(deltaMoves[num])
        if len(mins) == 0:
            return "NO PATH", None
        bestMove = moves[mins.index(min(mins))]
        #values[x][y] = bestMove
        bestDelta = delta[deltaMoves.index(bestMove)]
        return bestMove, [x + bestDelta[0], y + bestDelta[1]]
    
    def __str__(self):
        return str(self.board)
    
class BreadthFirst(Pather):
       def __init__(self, board, start, goal, cost= 1):
           if not isinstance(cost, int) and not isinstance(cost, float):
               raise ValueError('Cost function for breadth first search must be a uniform int')
           super(BreadthFirst, self).__init__(board, start, goal, cost)
       
       def search(self, start = None):
           if start == None:
               start = self.start
           values = self.valueMap(self.goal)
           currentNode = start
           x,y = currentNode
           while currentNode != self.goal and currentNode != None:
               bestMove, currentNode = self.bestMove(values, currentNode)
               if bestMove != 'NO PATH':
                   values[x][y] = bestMove
               else:
                   values[x][y] = "X"
               x,y = currentNode
           values[x][y] = '*'
           for i in range(values.rows):
               for j in range(values.columns):
                   if (i != self.goal[0] or j != self.goal[1]) and isinstance(values[i][j], int):
                       if values[i][j] > 0:
                           values[i][j] = ' '
                   values[i][j]
           return values
        
       def policyMap(self):
           values = self.valueMap(self.goal)
           values2 = values.makeCopy()
           for i in range(values.rows):
               for j in range(values.columns):
                   if isinstance(values[i][j], int) and values[i][j] > 0:
                       values2[i][j] = self.bestMove(values, [i,j])[0]

           return values2

##class DepthFirst(self, board, start, goal, cost= 1):
##
##  
##  def __init__(self, board, start, goal, cost= 1):
##       if not isinstance(cost, int) and not isinstance(cost, float):
##           raise ValueError('Cost function for breadth first search must be a uniform int')
##       super(BreadthFirst, self).__init__(board, start, goal, cost)
##
##  def search(self):
##      pass
##
##  def policyMap(self):
##      pass
        
##class A*(Pather):
##
##    def __init__(self, board, start, goal, cost= 1):
##         if not callable(obj):
##             raise ValueError('Cost function for A* must be a heuristic function')
##         super(BreadthFirst, self).__init__(board, start, goal, cost)
##
##    def search():
##      pass
##
##    def policyMap(self):
##      pass


if __name__ == "__main__":
    maze = matrix.Matrix([[0,1,1,1],[0,1,0,1],[0,0,0,0],[0,0,1,0]])
    start = [0,0]
    goal = [len(maze) - 1, len(maze[0]) - 1]
    pather = BreadthFirst(maze, start, goal)
    print(maze)
    print()
    print(pather.expandedMap(start))
    print()
    print(pather.valueMap())
    print()
    print(pather.search())
    print()
    print(pather.policyMap())

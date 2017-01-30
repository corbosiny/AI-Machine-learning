import matrix
from math import sqrt

delta = [[-1,0],[0,1],[1, 0],[0,-1]]        #movements through the maze
deltaMoves = ['^','>','v','<']              #symbols of each movement for relaying path to user

class Pather():

    def __init__(self, board, start, goal, cost= 1, realMaze = None):
        self.board = board
        self.start = start
        self.goal = goal
        self.cost = cost
        self.realMaze = realMaze
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
    
    def valueMap(self, start = None, cost= 1, index = 0, stopEarly = False):
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
            baseNode = frontier.pop(index)
            x,y = baseNode[1:]
            if callable(cost) and [x,y] != self.start:
                baseNode[0] -= cost([x,y], self.goal)
                self.explored[x][y] = baseNode[0]
            for num, move in enumerate(delta):
                x2 = x + move[0] 
                y2 = y + move[1]

                if (x2 < self.bounds[0] and x2 >= 0) and (y2 < self.bounds[1] and y2 >= 0):
                    if self.realMaze and self.realMaze[x2][y2] == 1:
                        self.board[x2][y2] = -1
                        self.explored[x2][y2] = -1
                        self.expanding[x2][y2] = -1
                        
                    if self.explored[x2][y2] == -1:
                        pass
                    else:
                        if isinstance(cost, int) or isinstance(cost, float):
                            newCost = cost
                        elif isinstance(cost, list):
                            newCost = cost[num]
                        else:
                            newCost = cost([x2, y2], self.goal) + 1
                        if isinstance(self.explored[x2][y2], str) or baseNode[0] + newCost < self.explored[x2][y2]:
                            if x2 != self.goal[0] or y2 != self.goal[1]:
                                frontier.append([baseNode[0] + newCost, x2, y2])
                            self.explored[x2][y2] = baseNode[0] + newCost
                            self.expanding[x2][y2] = expansionNum
                            expansionNum += 1
                        else:
                            pass
                if stopEarly and (x2 == self.goal[0] and y2 == self.goal[1]):
                    return self.explored
            closed.append(baseNode)

        return self.explored


    def search(self, start = None, stopE = True, indi = 0, newCost = 1):
        if start == None:
            start = self.start
        
        values = self.valueMap(start, stopEarly = stopE, index = indi, cost= newCost)
        print(values)
        print()
        currentNode = self.goal
        while currentNode != self.start:
            x,y = currentNode
            bestMove, currentNode = self.bestMove(values, currentNode)
            if bestMove == "NO PATH":
                if x == self.goal[0] and y == self.goal[1]:
                    values[start[0]][start[1]] = "X"
                    return values
                values = self.valueMap(start, stopEarly = stopE)
                values[x][y] = 'X'
                currentNode = self.goal
            else:
                values[currentNode[0]][currentNode[1]] = deltaMoves[(deltaMoves.index(bestMove) + 2) % len(deltaMoves)]
        values[self.goal[0]][self.goal[1]] = '*'
        bestMove, currentNode = self.bestMove(values, currentNode)
        for i in range(values.rows):
            for j in range(values.columns):
                value = values[i][j]
                if (isinstance(value, int) or isinstance(value, float)):
                    if value > 0:
                        values[i][j] = ' '
                    else:
                        values[i][j] = 1
                elif value == 'X':
                    values[i][j] = ' '
                  
        return values


    def bestMove(self, values, currentNode):
        moves = []
        mins = []
        x,y = currentNode
        for num, move in enumerate(delta):
            x2 = x + move[0]
            y2 = y + move[1]
            if x2 >= 0 and x2 < len(values) and y2 >= 0 and y2 < len(values[0]):
                value = values[x2][y2]
                if (isinstance(value, int) or isinstance(value, float)) and value >= 0:
                    mins.append(value)
                    moves.append(deltaMoves[num])
        if len(mins) == 0:
            return "NO PATH", None
        bestMove = moves[mins.index(min(mins))]
        bestDelta = delta[deltaMoves.index(bestMove)]
        return bestMove, [x + bestDelta[0], y + bestDelta[1]]

    def policyMap(self, indi = 0, newCost= 1):
        
        values = self.valueMap(self.goal, cost= newCost, index = indi)
        values2 = values.makeCopy()
     
        for i in range(values.rows):
            for j in range(values.columns):
                if (isinstance(values[i][j], int) or isinstance(values[i][j], float)) and values[i][j] > 0:
                    values2[i][j] = self.bestMove(values, [i,j])[0]
        values2[self.goal[0]][self.goal[1]] = "*"
        return values2
    
    def __str__(self):
        return str(self.board)
    
class BreadthFirst(Pather):
       def __init__(self, board, start, goal, cost= 1, realMaze = None):
           if not isinstance(cost, int) and not isinstance(cost, float):
               raise ValueError('Cost function for breadth first search must be a uniform int')
           super(BreadthFirst, self).__init__(board, start, goal, cost, realMaze)

       def find(self, stop = True):
           return self.search(stopE = stop)

       def pMap(self):
           return self.policyMap()
        

class DepthFirst(Pather):
    def __init__(self, board, start, goal, cost= 1, realMaze = None):
        if not isinstance(cost, int) and not isinstance(cost, float):
            raise ValueError('Cost function for breadth first search must be a uniform int')
        super(DepthFirst, self).__init__(board, start, goal, cost, realMaze)

    def find(self, stop = True):
        return self.search(stopE = stop, indi = -1)

    def pMap(self):
        return self.policyMap(-1)
        
class Astar(Pather):

    def __init__(self, board, start, goal, cost, realMaze = None):
         if not callable(cost):
             raise ValueError('Cost function for A* must be a heuristic function')
         super(Astar, self).__init__(board, start, goal, cost, realMaze)

    def find(self, stop = True):
        cost = self.cost
        return self.search(stopE = stop, newCost = cost)

    def pMap(self):
        cost = self.cost
        return self.policyMap(newCost = cost)


def costEstimate(location, goal):
    return int(sqrt(sum([pow(x - y, 2) for x,y in zip(location, goal)])))
    
if __name__ == "__main__":
##    maze = matrix.Matrix([[0,1,0,0,1],[0,1,0,0,1],[0,0,0,0,1],[0,0,1,0,0], [0,1,1,0,0],[0,0,0,0,1]])
##    start = [0,0]
##    goal = [3, 3]
##    pather = BreadthFirst(maze, start, goal)
##    pather2 = DepthFirst(maze, start, goal)
##    pather3 = Astar(maze,start,goal, costEstimate)
##    print("Maze:")
##    print(maze)
##    print()
##    #print(pather.expandedMap(start))
##    print("--------------------")
##    #print(pather.valueMap())
##    print('\nBreadth First:')
##    print(pather.find())
##    print()
##    print(pather.find(False))
##    print()
##    print(pather.pMap())
##    print('\nDepth First:')
##    print(pather2.find())
##    print()
##    print(pather2.find(False))
##    print()
##    print(pather2.pMap())
##    print("\nA*:")
##    print()
##    print(pather3.find())
##    print()
##    print(pather3.find(False))
##    print()
##    print(pather3.pMap())
##    print()
    maze = matrix.Matrix([[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]])
    realMaze = matrix.Matrix([[0,0,1,0,0],[0,0,1,0,0],[0,1,1,0,0],[0,0,0,0,0],[0,0,0,0,0]])
    start = [0,0]
    goal = [0,4]
    pather = Astar(maze, start, goal, costEstimate, realMaze)
    print(pather.find())
    print()
    print(pather.expandedMap())
    

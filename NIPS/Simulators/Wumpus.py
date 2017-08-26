from random import randint
class Grid(object):
    '''represents the 2D wumpus world'''

    def __init__(self,N):
        '''class constructor'''
        self.size = N
        self.grid = [[0 for i in range(N)] for j in range(N)]
        self.goal_x,self.goal_y = 0,self.size-1
        self.obsMap = [[[] for i in range(N)] for j in range(N)]
        self.actions = ["left","right","top","down"]
        self.grid[int(N/float(2))][int(N/float(2))] = 1
        self.start = (randint(0,N-1),randint(0,N-1))
        self.features = ["row","column","stench","breeze"]
        self.getObs()

    def valid(self,x,y):
        '''checks if (x,y) is a valid position'''
        if x < 0 or x == self.size or y < 0 or y == self.size:
            return False
        return True

    def takeAction(self,state,action):
        '''takes an action and returns new state'''
        x,y = state[0],state[1]
        if self.grid[x][y] == 1:
            return "loser"
        if x == self.goal_x and y == self.goal_y:
            return "winner"
        ts = None
        if action in self.actions:
            if action == "left":
                if self.valid(x-1,y):
                    ts = (x-1,y)
                else:
                    ts = (x,y)
            elif action == "right":
                if self.valid(x+1,y):
                    ts = (x+1,y)
                else:
                    ts = (x,y)
            elif action == "top":
                if self.valid(x,y+1):
                    ts = (x,y+1)
                else:
                    ts = (x,y)
            elif action == "down":
                if self.valid(x,y-1):
                    ts = (x,y-1)
                else:
                    ts = (x,y)
        else:
            ts = (x,y)
        x,y = ts[0],ts[1]
        if self.grid[x][y] == 1:
            return "loser"
        if x == self.goal_x and y == self.goal_y:
            return "winner"
        return ts

    def getObs(self):
        '''generates observations of stench
           and breeze, based on wumpus pos
        '''
        valid = self.valid
        for x in range(self.size):
            for y in range(self.size):
                if valid(x+1,y) and self.grid[x+1][y] == 1:
                    self.obsMap[x][y].append("stench")
                if valid(x-1,y) and self.grid[x-1][y] == 1:
                    self.obsMap[x][y].append("stench")
                if valid(x,y+1) and self.grid[x][y+1] == 1:
                    self.obsMap[x][y].append("stench")
                if valid(x,y-1) and self.grid[x][y-1] == 1:
                    self.obsMap[x][y].append("stench")
                if self.grid[x][y]!=1:
                    self.obsMap[x][y].append("breeze")

    def factored(self,state):
        '''returns a factored state of
           x,y,I(stench),I(breeze)
        '''
        x,y = state[0],state[1]
        if not self.valid(x,y):
            print "In valid grid cell"
            exit()
        state = [x]+[y]
        state += [1 if "stench" in self.obsMap[x][y] else 0]
        state += [1 if "breeze" in self.obsMap[x][y] else 0]
        return state

    def __repr__(self):
        '''defines the representation of the grid
           that will be output on call to print
        '''
        string = "Wumpus map: \n"
        for i in range(self.size):
            for j in range(self.size):
                string += [str(self.grid[i][j])+", " if j!=self.size-1 else str(self.grid[i][j])+"\n"][0]
        string += "\nObservation map: \n"
        for i in range(self.size):
            for j in range(self.size):
                string += [str(self.obsMap[i][j])+", " if j!=self.size-1 else str(self.obsMap[i][j])+"\n"][0]
        return string+"\nGoal Position: ("+str(self.goal_x)+","+str(self.goal_y)+")"+"\n"

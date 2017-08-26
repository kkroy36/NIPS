import numpy as np
class Signal(object):
    '''class the represents a singlet agent in the
       traffic signal domain comprising 4 signals
    '''

    def __init__(self,avg):
        '''class constructor'''
        self.avg = avg
        self.density = np.random.poisson(avg,4)
        #east is 0, west is 1, north is 2, south is 3

class TrafficSignal(object):
    '''class for traffic signals of 4 signal objects'''

    def __init__(self,N=4):
        '''class constructor'''
        self.signals = []
        #0 is 1st signal, 1 is 2nd signal , 2 is 3rd signal, ..
        for i in range(N):
            self.signals.append(Signal(5))
        self.actions = []
        for signalID in ["one","two","three","four"]:
            for direction in ["east","west","north","south"]:
                self.actions.append((signalID,direction))
        '''
        for i in range(4):
            for j in range(4):
                self.actions.append((i,j))
        '''
        self.start = self

    def getMaxDensityDirection(self,signalID):
        '''returns the most crowded direction
           pertaining to the signal
        '''
        maxDensityDirection = 0
        for i in range(4):
            if self.signals[signalID].density[i] > self.signals[signalID].density[maxDensityDirection]:
                maxDensityDirection = i
        return maxDensityDirection

    def takeAction(self,state,action):
        '''releases traffic in the direction desired'''
        #action description = ("signal id","direction")
        signalID,direction = None,None
        if action[0] == "one":
            signalID = 0
        elif action[0] == "two":
            signalID = 1
        elif action[0] == "three":
            signalID = 2
        elif action[0] == "four":
            signalID = 3
        if action[1] == "east":
            direction = 0
        elif action[1] == "west":
            direction = 1
        elif action[1] == "north":
            direction = 2
        elif action[1] == "south":
            direction = 3
        maxDensityDirection = state.getMaxDensityDirection(signalID)
        #print("max density direction: "+str(maxDensityDirection))
        state.signals[signalID].density[direction] = np.random.poisson(state.signals[signalID].avg,1)
        if direction == maxDensityDirection:
            return "winner"
        else:
            return "loser"

    def factored(self,state):
        '''returns factored representation of state'''
        if state == "winner" or state == "loser":
            return state
        factoredState = []
        factoredState.append(self.signals[0].density[0])
        factoredState.append(self.signals[0].density[1])
        factoredState.append(self.signals[0].density[2])
        factoredState.append(self.signals[0].density[3])
        factoredState.append(self.signals[1].density[0])
        factoredState.append(self.signals[1].density[1])
        factoredState.append(self.signals[1].density[2])
        factoredState.append(self.signals[1].density[3])
        factoredState.append(self.signals[2].density[0])
        factoredState.append(self.signals[2].density[1])
        factoredState.append(self.signals[2].density[2])
        factoredState.append(self.signals[2].density[3])
        factoredState.append(self.signals[3].density[0])
        factoredState.append(self.signals[3].density[1])
        factoredState.append(self.signals[3].density[2])
        factoredState.append(self.signals[3].density[3])
        return factoredState
        

    def __repr__(self):
        '''call to print will output this'''
        rStr = ""
        rStr += "Number of cars going east in signal "+str(1)+" is " + str(self.signals[0].density[0])
        rStr += "\n Number of cars going west in signal " + str(1) + " is " + str(self.signals[0].density[1])
        rStr += "\nNumber of cars going north in signal " + str(1) + " is " + str(self.signals[0].density[2])
        rStr += "\nNumber of cars going south in signal " + str(1) + " is " + str(self.signals[0].density[3])
        rStr += "\nNumber of cars going east in signal " + str(2) + " is " + str(self.signals[1].density[0])
        rStr += "\nNumber of cars going west in signal " + str(2) + " is " + str(self.signals[1].density[1])
        rStr += "\nNumber of cars going north in signal " + str(2) + " is " + str(self.signals[1].density[2])
        rStr += "\nNumber of cars going south in signal " + str(2) + " is " + str(self.signals[1].density[3])
        rStr += "\nNumber of cars going east in signal " + str(3) + " is " + str(self.signals[2].density[0])
        rStr += "\nNumber of cars going west in signal " + str(3) + " is " + str(self.signals[2].density[1])
        rStr += "\nNumber of cars going north in signal " + str(3) + " is " + str(self.signals[2].density[2])
        rStr += "\nNumber of cars going south in signal " + str(3) + " is " + str(self.signals[2].density[3])
        rStr += "\nNumber of cars going east in signal " + str(4) + " is " + str(self.signals[3].density[0])
        rStr += "\nNumber of cars going west in signal " + str(4) + " is " + str(self.signals[3].density[1])
        rStr += "\nNumber of cars going north in signal " + str(4) + " is " + str(self.signals[3].density[2])
        rStr += "\nNumber of cars going south in signal " + str(4) + " is " + str(self.signals[3].density[3])
        return rStr+"\n"

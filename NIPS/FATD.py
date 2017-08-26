from FuncApprox import NeuralNetwork,GradientBooster,LSReg
from Chain import Chain
from BlackJack import Game
from Wumpus import Grid
from BW import BW
from traffic import TrafficSignal
from pong import Pong
from random import randint
from copy import deepcopy
from Matrix import matrix
class TD(object):
    '''class for TD learning'''

    def __init__(self,FA="LSReg",domain="50chain",N=100,loss="ls",trees=500,type="max",depth=2):
        '''class constructor'''
        self.domain = domain
        if domain == "50chain":
            self.domObj = Chain()
        elif domain == "blackjack":
            self.domObj = Game()
        elif domain == "wumpus":
            self.domObj = Grid(4)
        elif domain == "blocksworld":
            self.domObj = BW(4)
        elif domain == "traffic":
            self.domObj = TrafficSignal()
        elif domain == "pong":
            self.domObj = Pong()
        if FA == "LSReg":
            self.FA = LSReg()
        elif FA == "NN":
            self.FA = NeuralNetwork()
        elif FA == "GB":
            self.FA = GradientBooster(loss=loss,trees=trees,depth=depth)
        self.value,self.count = {},{}
        self.values = [{} for i in range(N)]
        self.approxValues = [{} for i in range(N)]
        self.BE = []
        self.type = type
        self.TD(self.FA,N)

    def getSample(self):
        '''gets a sample trajectory from
           the specified domain
        '''
        d = Chain()
        if self.domain == "blackjack":
            d = Game()
        elif self.domain == "wumpus":
            d = Grid(4)
        elif self.domain == "blocksworld":
            d = BW(4)
        elif self.domain == "traffic":
            d = TrafficSignal()
        elif self.domain == "pong":
            d = Pong()
        #elif wumpus
        sample = []
        state = d.start
        actions = d.actions
        while True:
            if state == "winner" or state == "loser":
                sample += [deepcopy(state)]
                break
            sample += [deepcopy(state)]
            action = actions[randint(0,len(actions)-1)]
            state = d.takeAction(state,action)
        return sample

    def getValue(self,state):
        '''returns the current estimate of the value'''
        if state == "winner":
            return 100
        elif state == "loser":
            return -50
        else:
            if state in self.value.keys():
                return self.value[state]
            else:
                return 0

    def setValue(self,state,value):
        '''gradient update to value of the state'''
        if state in self.value.keys():
            alpha = 1/float(self.count[state])
            self.value[state] += alpha*(value-self.value[state])
        elif state not in self.value.keys():
            self.value[state] = value

    def setCount(self,state):
        '''updated the count of the state'''
        if state in self.count.keys():
            self.count[state] += 1
        elif state not in self.count.keys():
            self.count[state] = 1

    def applyBellmanOperator(self,s):
        '''calculates value using bellman equation'''
        N = len(s)
        for i in range(N-2,-1,-1):
            R = -1
            self.setCount(str(s[i]))
            V_st = self.getValue(str(s[i+1]))
            self.setValue(str(s[i]),R+V_st) #put str here

    def applyProjection(self,s,FA):
        '''projects to span of basis
           using the function approximator
        '''
        d = self.domObj
        X = []
        Y = []
        for state in s[:-1]:
            X.append(d.factored(state))
            Y.append([self.getValue(str(state))])
        X = matrix(X)
        Y = matrix(Y)
        FA.setXY(X,Y)
        Y_hat = FA.predict()
        if Y_hat:
            nY = len(Y_hat)
            for i in range(nY):
                self.value[str(s[i])] = Y_hat[i]

    def bellmanError(self,true,approx,type="max"):
        '''gets average or max bellman error'''
        maxi = float("-inf")
        tot = 0
        c = 0
        for key in true:
            if key in approx:
                be = abs(true[key]-approx[key])
                tot += be
                c += 1
                if be > maxi:
                    maxi = be
        if type=="max":
            return maxi
        elif type=="avg":
            return tot/float(c)

    def TD(self,FA,N):
        '''carries out ADP'''
        for i in range(N):
            print "-"*80
            s = self.getSample()
            self.applyBellmanOperator(s)
            self.values[i] = deepcopy(self.value)
            self.applyProjection(s,FA)
            self.approxValues[i] = deepcopy(self.value)
            bellmanError = deepcopy(self.bellmanError(self.values[i],self.approxValues[i],type=self.type))
            self.BE.append(bellmanError)
            print "bellman error for iteration "+str(i)+": "+str(bellmanError)
            #raw_input("press key to continue")

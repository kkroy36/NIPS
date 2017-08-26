from itertools import permutations
import re
import itertools
from random import random
class BW(object):
    '''represents the blocks world simulator'''
    
    def __init__(self,N=4):
        '''class constructor'''
        if N == 4:
            self.blockList = ['A','B','C','D']
            self.start = tuple(sorted(['TABLE(A)','TABLE(B)','TABLE(D)','CLEAR(A)','CLEAR(C)','CLEAR(D)','ON(B,C)']))
            self.goal = tuple(sorted(['TABLE(A)','TABLE(B)','TABLE(C)','TABLE(D)','CLEAR(A)','CLEAR(B)','CLEAR(C)','CLEAR(D)']))
        elif N == 6:
            self.blockList = ['A','B','C','D','E','F']
            self.start = tuple(sorted(['TABLE(A)','TABLE(B)','TABLE(D)','CLEAR(A)','CLEAR(C)','CLEAR(F)','ON(B,C)','ON(D,E)','ON(E,F)']))
            self.goal = tuple(sorted(['TABLE(A)','TABLE(B)','TABLE(C)','TABLE(D)','TABLE(E)','TABLE(F)','CLEAR(A)','CLEAR(B)','CLEAR(C)','CLEAR(D)','CLEAR(E)','CLEAR(F)']))
        elif N == 5:
            self.blockList = ['A','B','C','D','E']
            self.start = tuple(sorted(['TABLE(A)','TABLE(C)','TABLE(D)','CLEAR(B)','CLEAR(C)','CLEAR(E)','ON(A,B)','ON(D,E)']))
            self.goal = tuple(sorted(['TABLE(A)','TABLE(B)','TABLE(C)','TABLE(D)','TABLE(E)','CLEAR(A)','CLEAR(B)','CLEAR(C)','CLEAR(D)','CLEAR(E)']))
        self.actions = ["stackBlock","unstackBlock"]

    def permutationsList(self,blocksList):
        permsBlockList = []
        for perms in permutations(blocksList, 2):
            permsBlockList.append(perms)
        return permsBlockList

    def checkArguments(self,configList):
        '''checks validity of state'''
        argDict = {}
        tableArgList = []
        clearArgList = []
        onArgList = []
        for eachState in configList:
            splitEachState = re.compile("(.*?)\s*\((.*?)\)")
            if splitEachState.match(eachState).group(1) == 'TABLE':
                tableArgList.append(splitEachState.match(eachState).group(2))
                argDict[splitEachState.match(eachState).group(1)] = tableArgList
            elif splitEachState.match(eachState).group(1) == 'CLEAR':
                clearArgList.append(splitEachState.match(eachState).group(2))
                argDict[splitEachState.match(eachState).group(1)] = clearArgList
            else:
                argTuple = [item for item in list(splitEachState.match(eachState).group(2)) if item != ","]
                onArgList.append(tuple(argTuple))
                argDict[splitEachState.match(eachState).group(1)] = onArgList
        return argDict

    def stackBlock(self,baseBlock, aboveBlock, configList):
        stateChange = False
        argDict = self.checkArguments(configList)
        if baseBlock in argDict['CLEAR'] and aboveBlock in argDict['CLEAR']:
            stateChange = True
            if ("ON" + "(" + baseBlock + "," + aboveBlock + ")") not in configList:
                configList.append("ON" + "(" + baseBlock + "," + aboveBlock + ")")
            configList.remove("CLEAR" + "(" + baseBlock + ")")

            if baseBlock in argDict['TABLE'] and aboveBlock in argDict['TABLE']:
                stateChange = True
                configList.remove("TABLE" + "(" + aboveBlock + ")")
            else:
                if aboveBlock in argDict['TABLE']:
                    configList.remove("TABLE" + "(" + aboveBlock + ")")
                for eachTuple in argDict['ON']:
                    if aboveBlock in eachTuple:
                        for item in eachTuple:
                            if item != aboveBlock:
                                stateChange = True
                                if ("CLEAR" + "(" + item + ")") not in configList:
                                    configList.append("CLEAR" + "(" + item + ")")
                                configList.remove("ON" + "(" + item + "," + aboveBlock + ")")
        if stateChange:
            return configList
        else:
            return stateChange

    def unstackBlock(self,baseBlock, aboveBlock, configList):
        stateChange = False
        argDict = self.checkArguments(configList)
        if 'ON' not in argDict.keys():
            self.stackBlock(baseBlock, aboveBlock, configList)
        elif (baseBlock, aboveBlock) in argDict['ON'] and aboveBlock in argDict['CLEAR']:
            configList.remove("ON" + "(" + baseBlock + "," + aboveBlock + ")")
            if ("CLEAR" + "(" + baseBlock + ")") not in configList:
                configList.append("CLEAR" + "(" + baseBlock + ")")
            if ("CLEAR" + "(" + aboveBlock + ")") not in configList:
                configList.append("CLEAR" + "(" + aboveBlock + ")")
            if ("TABLE" + "(" + aboveBlock + ")") not in configList:
                configList.append("TABLE" + "(" + aboveBlock + ")")
            stateChange = True
        if stateChange:
            return configList
        else:
            return stateChange

    def takeAction(self,state,action):
        perms = self.permutationsList(self.blockList)
        state = list(state)
        N = len(perms)
        initState = False
        while not initState:
            perm = perms[int(random() * len(perms))]
            if action == "stackBlock":
                possible = ["CLEAR" in item for item in state]
                if possible.count(True) < 2:
                    return tuple(sorted(state))
                initState = self.stackBlock(perm[0], perm[1], list(state))
            else:
                possible = ["ON" in item for item in state]
                if True not in  possible:
                    return tuple(sorted(state))
                initState = self.unstackBlock(perm[0], perm[1], list(state))
        if tuple(sorted(initState)) == self.goal:
            return "winner"
        return tuple(sorted(initState))

    def factored(self,state):
        '''returns factored state'''
        factors = []
        for block in self.blockList:
            factors.append("CLEAR("+block+")")
            factors.append("TABLE("+block+")")
        perms = self.permutationsList(self.blockList)
        for item in perms:
            factors.append("ON("+item[0]+","+item[1]+")")
        factors = sorted(factors)
        N = len(factors)
        factored = [0 for i in range(N)]
        for i in range(N):
            if factors[i] in state:
                factored[i] = 1
        return factored

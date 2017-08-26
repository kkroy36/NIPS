from math import exp
from random import randint
class Chain(object):
    '''class to represent the 50-chain'''
    
    def __init__(self):
        '''class constructor'''
        self.chain = [0 for i in range(50)]
        self.chain[13],self.chain[38] = 1,1
        self.actions = ["left","right"]
        self.start = randint(0,49)
        self.features = ["kernel1dens","kernel2dens"]

    def goldPositions(self):
        '''returns the gold positions on the chain'''
        return [13,38]

    def valid(self,cell):
        '''check if chain cell is valid'''
        if cell < 0 or cell > 49:
            return False
        return True

    def takeAction(self,cell,action):
        '''returns new state
           invalid action does nothing
        '''
        if cell == 13 or cell == 38:
            return "winner"
        if action not in self.actions:
            return cell
        elif action in self.actions:
            if action == "left":
                if self.valid(cell-1):
                    if cell-1 == 13 or cell-1 == 38:
                        return "winner"
                    else:
                        return cell-1
                elif not self.valid(cell-1):
                    return cell
            elif action == "right":
                if self.valid(cell+1):
                    if cell+1 == 13 or cell+1 == 38:
                        return "winner"
                    else:
                        return cell+1
                elif not self.valid(cell+1):
                    return cell

    def kernelProb(self,cell,kernel,std):
        '''gaussian kernel'''
        distance = (cell-kernel)**2
        factor = exp((-1*distance)/float(std))
        return factor

    def factored(self,cell):
        '''returns probabilities of RBF kernels'''
        kernels = self.goldPositions()
        Z = 0
        factoredCell = []
        for kernel in kernels: 
            prob = self.kernelProb(cell,kernel,4)
            factoredCell += [prob]
            Z += prob
        factoredCell = [prob/float(Z) for prob in factoredCell]
        return factoredCell

    def __repr__(self):
        '''printing the chain
           will output this content
        '''
        return "gold positions: "+" ".join([str(i) for i in self.goldPositions()])+"\n"     

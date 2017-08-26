from Matrix import matrix
import numpy as np
from sklearn.neural_network import MLPRegressor
from sklearn import ensemble
from sklearn.tree import DecisionTreeRegressor,export_graphviz
from os import system

class NeuralNetwork(object):
    '''class for a neural network function approximator'''
    
    def __init__(self,hiddenLayers=25,hiddenLayerSize=2,solver="lbfgs",activation="logistic"):
        self.hiddenLayers = hiddenLayers
        self.hiddenLayerSize = hiddenLayerSize
        self.solver = solver
        self.activation = activation
        self.X,self.Y = [],[]

    def setXY(self,X,Y):
        '''sets X and Y for regression'''
        self.X,self.Y = [],[]
        for item in X.value:
            self.X.append(item)
            self.Y.append(Y.value[X.value.index(item)][0])

    def dumpTree(self,tree,features,name):
        '''create tree png file'''
        with open(name+".dot",'w') as f:
            export_graphviz(tree,out_file=f,feature_names=features)
        system("dot -Tpng "+name+".dot "+"-o "+name+".png")

    def predict(self,dumpTree=False,features=False):
        '''predicts regression values'''
        npX = np.array(self.X)
        npY = np.array(self.Y)
        model = MLPRegressor(solver=self.solver,
                             activation=self.activation,
                             alpha=1e-5,
                             hidden_layer_sizes=(self.hiddenLayers,self.hiddenLayerSize),
                             random_state=1)
        model.fit(npX,npY)
        output = model.predict(npX)
        if dumpTree:
            if not features:
                print """please enter state features for tree node
                         in call to predict, do FA.predict(dumpTree=True,features=<feature_names>)
                      """
                exit()
            dt = DecisionTreeRegressor(random_state=0)
            dt.fit(npX,output)
            self.dumpTree(dt,features,"basisFunction")
        return [item for item in output]  

    def __repr__(self):
        '''returns this on call to print'''
        rStr = ""
        rStr += "Number of hidden layers: "+str(self.hiddenLayers)
        rStr += "\nHidden layer size: "+str(self.hiddenLayerSize)
        rStr += "\nactivation function: "+self.activation
        if self.solver == "lbfgs":
            rStr += "\nUsing batch gradients"
        elif self.solver == "sgd":
            rStr += "\nUsing stochastic gradients"
        return rStr

class GradientBooster(object):
    '''gradient boosting function approximator'''

    def __init__(self,trees=25,depth=2,loss="ls"):
        '''class constructor'''
        self.trees = trees
        self.depth = depth
        self.loss = loss
        self.X,self.Y = [],[]

    def setXY(self,X,Y):
        '''sets X and Y for regression'''
        self.X,self.Y = [],[]
        for item in X.value:
            self.X.append(item)
            self.Y.append(Y.value[X.value.index(item)][0])

    def dumpTree(self,tree,features,name):
        '''create tree png file'''
        with open(name+".dot",'w') as f:
            export_graphviz(tree,out_file=f,feature_names=features)
        system("dot -Tpng "+name+".dot "+"-o "+name+".png")

    def predict(self,dumpTree=False,features=False):
        '''predicts regression values'''
        npX = np.array(self.X)
        npY = np.array(self.Y)
        params = {'n_estimators':self.trees,
                  'max_depth':self.depth,
                  'min_samples_split':2,
                  'learning_rate':0.01,
                  'loss':self.loss}
        model = ensemble.GradientBoostingRegressor(**params)
        model.fit(npX,npY)
        output = model.predict(npX)
        if dumpTree:
            if not features:
                print """please enter state features for tree node
                         in call to predict, do FA.predict(dumpTree=True,features=<feature_names>)
                      """
                exit()
            dt = DecisionTreeRegressor(random_state=0)
            dt.fit(npX,output)
            self.dumpTree(dt,features,"basisFunction")
        return [item for item in output]

    def __repr__(self):
        '''returns this on call to print'''
        rStr = ""
        rStr += "Number of trees: "+str(self.trees)
        rStr += "\nMax depth of each tree: "+str(self.depth)
        rStr += "\nLoss function used: "+str(self.loss)
        return rStr

class LSReg(object):
    '''class for least squares regression'''
    
    def __init__(self):
        '''constructor'''
        self.X = []
        self.Y = []

    def setXY(self,X,Y):
        '''sets the value of X and Y'''
        self.X = X
        self.Y = Y

    @staticmethod
    def getWeight(X,Y):
        '''returns weight vector'''
        XtXinverse,XtY = None,None
        try:
            XtXinverse = (X.transpose()*X).inverse()
        except:
            print "Matrix not invertible"
            return False
        try:
            XtY = (X.transpose()*Y)
        except:
            print "Matrix operation failure"
            return False
        return XtXinverse*XtY

    def predict(self):
        '''predicts regression values'''
        W = LSReg.getWeight(self.X,self.Y) 
        if W:
            Y_hat = (W.transpose()*self.X.transpose())
            return [item for item in Y_hat.value[0]]
        else:
            return False

    def __repr__(self):
        '''returns this on call to print'''
        rStr = ""
        rStr += "least squares regression approximator"
        return rStr              

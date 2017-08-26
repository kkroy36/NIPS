import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import os

matplotlib.rcParams.update({'font.size':22})
def smooth(y, box_pts):
    box = np.ones(box_pts)/box_pts
    y_smooth = np.convolve(y, box, mode='same')
    return [i for i in y_smooth]

def difference(l1,l2):
    '''returns the difference between the lists'''
    N = len(l1)
    return [abs(l1[i]-l2[i]) for i in range(N)]

Xhuber,Yhuber = [],[]
domain = ((str(os.getcwd()).split("/"))[-1])[:-2]
with open("huber5000"+domain+".txt") as fp:
    lines = fp.read().splitlines()
for line in lines:
    Xhuber += [float(line.split(',')[0])]
    Yhuber += [float(line.split(',')[1])]

XNN,YNN = [],[]
with open("NN5000"+domain+".txt") as fp:
    lines = fp.read().splitlines()
for line in lines:
   XNN += [float(line.split(',')[0])]
   YNN += [float(line.split(',')[1])]

XLS,YLS = [],[]
with open("LS5000"+domain+".txt") as fp:
    lines = fp.read().splitlines()
for line in lines:
   XLS += [float(line.split(',')[0])]
   YLS += [float(line.split(',')[1])]

domain = ((str(os.getcwd()).split("/"))[-1])[:-2]
#Ynew = [(Y[i]-max(Y)) if max(Y)-1.8<Y[i]<max(Y)+1.8 else Y[i] for i in range(5000)]
#print max(X)
#print max(Ynew)
Yhuber = Yhuber[:2000]
YNN = YNN[:2000]
YLS = YLS[:2000]
plt.plot(range(2000),difference(Yhuber,YNN),label="NN",color='red')
plt.plot(range(2000),difference(Yhuber,YLS),label="LS",color='green')
plt.plot(range(2000),[0 for i in range(2000)],color='black')
#plt.plot(range(5000),smooth(Y,5000),label="without transfer")
#plt.plot(range(5000),smooth(Ynew,5000),label="with transfer")
plt.xlabel("iterations")
plt.ylabel("Bellman error(avg)")
plt.ylim(ymin=-0.5,ymax=3)#max(difference(Yhuber,YNN))+0.5)
plt.title("50-state chain")
plt.legend()
plt.show()  

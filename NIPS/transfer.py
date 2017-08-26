import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import os

matplotlib.rcParams.update({'font.size':26})
def smooth(y, box_pts):
    box = np.ones(box_pts)/box_pts
    y_smooth = np.convolve(y, box, mode='same')
    return [i for i in y_smooth]

def difference(l1,l2):
    '''returns the difference between the lists'''
    N = len(l1)
    return [abs(l1[i]-l2[i]) for i in range(N)]

XRRT,YRRT = [],[]
domain = "blackjack"
with open("RRT2000"+domain+".txt") as fp:
    lines = fp.read().splitlines()
for line in lines:
    XRRT += [float(line.split(',')[0])]
    YRRT += [float(line.split(',')[1])]

Xhuber,Yhuber = [],[]
with open("huber2000"+domain+".txt") as fp:
    lines = fp.read().splitlines()
for line in lines:
    Xhuber += [float(line.split(',')[0])]
    Yhuber += [float(line.split(',')[1])]

XNN,YNN = [],[]
with open("Deep Network2000"+domain+".txt") as fp:
    lines = fp.read().splitlines()
for line in lines:
   XNN += [float(line.split(',')[0])]
   YNN += [float(line.split(',')[1])]

XLS,YLS = [],[]
with open("Least Squares2000"+domain+".txt") as fp:
    lines = fp.read().splitlines()
for line in lines:
   XLS += [float(line.split(',')[0])]
   YLS += [float(line.split(',')[1])]

#Ynew = [(Y[i]-max(Y)) if max(Y)-1.8<Y[i]<max(Y)+1.8 else Y[i] for i in range(5000)]
#print max(X)
#print max(Ynew)
plt.plot(range(2000),difference(Yhuber,YRRT),label="RRT",color='blue',linewidth=3)
plt.plot(range(2000),difference(Yhuber,YNN),label="Deep Network",color='red',linewidth=3)
plt.plot(range(2000),difference(Yhuber,YLS),label="Least Squares",color='green',linewidth=3)
plt.plot(range(2000),[0 for i in range(2000)],color='black')
#plt.plot(range(5000),smooth(Y,5000),label="without transfer")
#plt.plot(range(5000),smooth(Ynew,5000),label="with transfer")
plt.xlabel("iterations")
plt.ylabel("Bellman error(avg)")
plt.ylim(ymin=-0.5,ymax=2)#max(difference(Yhuber,YNN))+0.5)
plt.title("Blackjack")
plt.legend()
plt.show()  

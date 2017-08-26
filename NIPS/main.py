from FATD import TD
import matplotlib.pyplot as plt
import numpy as np
import matplotlib
from math import log

matplotlib.rcParams.update({'font.size':26})

def smooth(y, box_pts):
    box = np.ones(box_pts)/box_pts
    y_smooth = np.convolve(y, box, mode='same')
    return [i for i in y_smooth]

def difference(l1,l2):
    '''returns the difference between the lists'''
    N = len(l1)
    return [abs(l1[i]-l2[i]) for i in range(N)]

def writeToFile(l,N,name):
    '''writes values to file'''
    with open(name,"a") as fp:
        for i in range(N):
            fp.write(str(i)+","+str(l[i])+"\n")

def main():
    '''main method
       default N=100
    '''
    N = 10
    type = "avg"
    domain = "tetris"
    tdGB = TD(FA="GB",domain=domain,N=N,type=type,loss="ls")
    #tdGBlad = TD(FA="GB",domain=domain,N=N,type=type,loss="lad")
    #tdGBhuber = TD(FA="GB",domain=domain,N=N,type=type,loss="huber")
    #tdNN = TD(FA="NN",domain=domain,N=N,type=type)
    #tdLS = TD(FA="LSReg",domain=domain,N=N,type=type)
    #writeToFile(tdGB.BE,N,"RRT"+str(N)+domain+".txt")
    #writeToFile(tdGBhuber.BE,N,"huber"+str(N)+domain+".txt")
    #writeToFile(tdNN.BE,N,"Deep Network"+str(N)+domain+".txt")
    #writeToFile(tdLS.BE,N,"Least Squares"+str(N)+domain+".txt")
    plt.ylim(ymin=-0.1,ymax=0.1)
    #plt.plot(range(N),difference(tdGBhuber.BE,tdGBlad.BE),label="LAD",color='red',linewidth=3)
    #plt.plot(range(N),difference(tdGBhuber.BE,tdGB.BE),label="LS",color='green',linewidth=3)
    #plt.plot(range(N),difference(tdGBhuber.BE,tdLS.BE),label="Least Squares",color='green',linewidth=3)
    plt.plot(range(N),tdGB.BE,label="GB")
    #plt.plot(range(N),tdLS.BE,label="LS")
    plt.xlabel("iterations")
    plt.ylabel("Bellman error("+type+")")
    plt.title(domain)
    plt.legend()
    plt.show() 

main()        

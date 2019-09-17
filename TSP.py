import math
import matplotlib.pyplot as plt
import random
import time
import copy
import sys
import tkinter
from matplotlib import style
style.use('fivethirtyeight')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

m=tkinter.Tk()
figure = plt.Figure()
ax = figure.add_subplot(111)
chart_type = FigureCanvasTkAgg(figure, m)
chart_type.get_tk_widget().pack()
ax.plot()

start_time = time.time()
results = []
problemDimension = 0

def update(x,y):
    ax.clear()
    ax.plot(x, y)
    figure.canvas.draw()
    figure.canvas.flush_events()

def run(inX,inY,maxtime,dimention):
    global problemDimension
    problemDimension = dimention
    x = inX
    y = inY
    update(x,y)
    x.append(x[0])
    y.append(y[0])
    #print(len(x),"len")
    solve = annealing(x,y)
    solve.simulate(int(maxtime),x,y)
    #print(results)
    plt.show()
    m.mainloop()
    return(results)


def calculateDistance(x1,y1,x2,y2):
     dist = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
     return dist

class tour:
    def __init__(self,ax,ay):
        global problemDimension
        self.x = ax
        self.y = ay
        self.tour = list(range(0,problemDimension))
        #makes 2 for run
        self.tour.append(self.tour[0])

    def nn(self,x,y):
        xList = []
        yList = []

        myTour = []
        distances = [0 for i in range(len(self.tour))]

        newX = []
        newY = []

        for i in range(0,len(self.tour)):
            tourPos = self.tour[i]
            xList.append(self.x[tourPos])
            yList.append(self.y[tourPos])

        newX.append(xList[0])
        newY.append(yList[0])
        xList.pop(0)
        yList.pop(0)

        for i in range(len(xList)):
            distances = []
            for j in range(len(xList)):
                distances.append(calculateDistance(newX[-1],newY[-1],xList[j],yList[j]))
                #distances.append((tsplib95.distances.euclidean((newX[-1],newY[-1]),(xList[j],yList[j]))))
            lowest = distances.index(min(distances))

            newX.append(xList[lowest])
            newY.append(yList[lowest])
            xList.pop(lowest)
            yList.pop(lowest)


        for i in range(len(newX)):
            for j in range(problemDimension-2):
                if (self.x[j]) == newX[i]:
                    if (self.y[j]) == newY[i]:
                        myTour.append(j+1)

        myTour.append(myTour[0])
        myTour.pop(0)


        newY.append(newY[0])
        newX.append(newX[0])
        self.tour = myTour

    def retTour(self):
        return self.tour

    def get_len(self):
        return len(self.tour)

    def makeSwap(self, a, b):
        temp = self.tour[a]
        self.tour[a] = self.tour[b]
        self.tour[b] = temp

    def findPathLength(self,x,y):
        pathDistance = 0
        for i in range(0,len(self.tour)-1):
            tourPos = self.tour[i]
            tourPos2 = self.tour[i+1]

            pathDistance += calculateDistance(x[tourPos],y[tourPos],x[tourPos2],y[tourPos2])
        return pathDistance

class annealing:
    def __init__(self,thisx,thisy):
        self.x = thisx
        self.y = thisy
        self.finalPath = None

    def acceptProbability(self, t, e, ne):
        if ne < e:
            return 1
        return math.exp((e - ne) / t)

    def retFinal(self):
        return self.finalPath

    def simulate(self,maxtime,x,y):
        self.x = x
        self.y = y


        t = 1000000000000000000000000
        cr = 0.000000000000000000001
        currentTour = tour(self.x,self.y)
        self.currentBest = currentTour
        self.currentBest.nn(self.x,self.y)

        # cooling
        while t > 0 and (time.time() - start_time)<maxtime:
            newtour = tour(self.x,self.y)
            newtour.tour = copy.deepcopy(self.currentBest.tour)

            touri = random.randint(1, len(newtour.tour)-3)
            tourj = random.randint(1, len(newtour.tour)-3)
            while tourj == touri:
                tourj = random.randint(1, problemDimension-3)

            newtour.makeSwap(touri, tourj)

            ce = self.currentBest.findPathLength(self.x,self.y)
            ne = newtour.findPathLength(self.x,self.y)

            if self.acceptProbability(t, ce, ne) > random.uniform(0,1):
                currentTour = newtour

            if currentTour.findPathLength(self.x,self.y) < self.currentBest.findPathLength(self.x,self.y):
                self.currentBest = currentTour
                print("Path length:",self.currentBest.findPathLength(self.x,self.y))

            t *= 1 - cr


        results.append(self.currentBest.findPathLength(self.x,self.y))
        self.currentBest.tour.append(-1)
        results.append(self.currentBest.retTour())

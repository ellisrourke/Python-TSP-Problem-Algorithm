import math
import matplotlib.pyplot as plt
import random
import time
import copy
import sys
import tsplib95



start_time = time.time()
input = "files/"+sys.argv[1]+".tsp"
results = []
problemDimension = 51

def calculateDistance(x1,y1,x2,y2):
     dist = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
     return dist

class tour:
    def __init__(self,ax,ay):
        self.x = ax
        self.y = ay
        self.tour = list(range(0, problemDimension-2))
        #makes 2 for run
        self.tour.append(self.tour[0])

    def nn(self,x,y):
        xList = []
        yList = []

        myTour = []
        distances = [0 for i in range(len(self.tour))]

        newX = []
        newY = []

        for i in range(0,problemDimension-1):
            #print(i)
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
        #print(a,b)
        temp = self.tour[a]
        self.tour[a] = self.tour[b]
        self.tour[b] = temp

    def findPathLength(self,x,y):
        #print(x[50])
        pathDistance = 0
        for i in range(0,len(self.tour)):
            tourPos = self.tour[i]
            print(tourPos,i)
            #print(len(x),len(y))
            #print(x[tourPos],y[tourPos])
            #print(tourPos, i)
            pathDistance += calculateDistance(x[tourPos],y[tourPos],x[tourPos+1],y[tourPos+1])
            #pathDistance = 0

            #pathDistance = 0
        print(pathDistance)
        #return pathDistance

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

            touri = random.randint(0, (len(newtour.tour)) )
            tourj = random.randint(0, (len(newtour.tour)) )
            while tourj == touri:
                tourj = random.randint(0, (problemDimension) )

            newtour.makeSwap(touri, tourj)

            ce = self.currentBest.findPathLength(self.x,self.y)
            ne = newtour.findPathLength(self.x,self.y)

            if self.acceptProbability(t, ce, ne) > random.uniform(0,1):
                currentTour = newtour

            if currentTour.findPathLength(self.x,self.y) < self.currentBest.findPathLength(self.x,self.y):
                self.currentBest = currentTour
                print("Path length:",self.currentBest.findPathLength(self.x,self.y))

            t *= 1 - cr


        print("final length: ", self.currentBest.findPathLength(self.x,self.y))
        self.finalPath = self.currentBest
        #self.finalPath.tour.append(-1)
        #for i in range(self.problem.dimension+2):
            #print(self.finalPath.retTour()[i])

        results.append(self.finalPath.findPathLength(self.x,self.y))
        self.finalPath.tour.append(-1)
        results.append(self.finalPath.retTour())
class Graph:
    def __init__(self, tour):
        self.xList = []
        self.yList = []
        # Populate axes
        for i in range(0, len(tour)):
            self.xList.append(prob.get_display(tour[i])[0])
            self.yList.append(prob.get_display(tour[i])[1])

    def display_graph(self):
        plt.close()
        plt.plot(self.xList, self.yList)
        plt.scatter(self.xList, self.yList)
        plt.show()



def run(inX,inY,maxtime):
    x = inX;
    y = inY;
    #print(len(x))
    #print(len(y))
    #x.append(x[0])
    #y.append(y[0])
    #print(x)
    #print(y)
    #print(len(x),"len")
    solve = annealing(x,y)
    solve.simulate(int(maxtime),x,y)
    #print(results)
    return(results)

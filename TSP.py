import math
import matplotlib.pyplot as plt
import random
import time
import copy
import sys
import tsplib95



start_time = time.time()
input = "files/"+sys.argv[1]+".tsp"
prob = tsplib95.load_problem(input)
results = []

class tour:
    def __init__(self):
        self.problem = prob = tsplib95.load_problem(input)
        self.tour = list(range(1, self.problem.dimension + 1))
        self.tour.append(self.tour[0])

    def nn(self):
        xList = []
        yList = []

        myTour = []
        distances = [0 for i in range(len(self.tour))]

        newX = []
        newY = []

        for i in range(0, len(self.tour)):
            xList.append(self.problem.get_display(self.tour[i])[0])
            yList.append(self.problem.get_display(self.tour[i])[1])

        newX.append(xList[0])
        newY.append(yList[0])
        xList.pop(0)
        yList.pop(0)

        for i in range(len(xList)):
            distances = []
            for j in range(len(xList)):
                distances.append((tsplib95.distances.euclidean((newX[-1],newY[-1]),(xList[j],yList[j]))))
            lowest = distances.index(min(distances))

            newX.append(xList[lowest])
            newY.append(yList[lowest])
            xList.pop(lowest)
            yList.pop(lowest)


        for i in range(len(newX)):
            for j in range(self.problem.dimension):
                if (self.problem.get_display(self.tour[j])[0]) == newX[i]:
                    if (self.problem.get_display(self.tour[j])[1]) == newY[i]:
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

    def findPathLength(self):
        pathDistance = 0
        for i in range(len(self.tour) - 1):
            pathDistance += self.problem.wfunc(self.tour[i], self.tour[i + 1])
        return pathDistance


class annealing:
    def __init__(self, prob):
        self.problem = prob
        self.finalPath = None

    def acceptProbability(self, t, e, ne):
        if ne < e:
            return 1
        return math.exp((e - ne) / t)

    def retFinal(self):
        return self.finalPath

    def simulate(self,maxtime):
        t = 1000000000000000000000000
        cr = 0.000000000000000000001
        currentTour = tour()
        self.currentBest = currentTour
        self.currentBest.nn()

        # cooling
        while t > 0 and (time.time() - start_time)<maxtime:
            newtour = tour()
            newtour.tour = copy.deepcopy(self.currentBest.tour)

            touri = random.randint(1, (self.problem.dimension) -1)
            tourj = random.randint(1, (self.problem.dimension) -1)
            while tourj == touri:
                tourj = random.randint(1, (self.problem.dimension) -1)

            newtour.makeSwap(touri, tourj)

            ce = self.currentBest.findPathLength()
            ne = newtour.findPathLength()

            if self.acceptProbability(t, ce, ne) > random.uniform(0,1):
                currentTour = newtour

            if currentTour.findPathLength() < self.currentBest.findPathLength():
                self.currentBest = currentTour
                print("Path length:",self.currentBest.findPathLength())

            t *= 1 - cr


        print("final length: ", self.currentBest.findPathLength())
        self.finalPath = self.currentBest
        #self.finalPath.tour.append(-1)
        #for i in range(self.problem.dimension+2):
            #print(self.finalPath.retTour()[i])

        results.append(self.finalPath.findPathLength())
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


def run(maxtime):
    solve = annealing(prob)
    solve.simulate(int(maxtime))
    return(results)

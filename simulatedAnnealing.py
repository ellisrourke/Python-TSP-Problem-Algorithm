import math
import tsplib95
import matplotlib.pyplot as plt
import random
import time
import copy

maxtime = int(input('enter amount of time: '))
start_time = time.time()



prob = tsplib95.load_problem("files/st70.tsp")
class tour:
    def __init__(self):
        self.problem = prob = tsplib95.load_problem("files/st70.tsp")
        self.tour = list(range(1, self.problem.dimension + 1))
        #random.shuffle(self.tour)
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
        #print(xList,yList)
        xList.pop(0)
        yList.pop(0)

        for i in range(len(xList)):
            distances = []
            for j in range(len(xList)):
                '''find distances to each node'''
                distances.append((tsplib95.distances.euclidean((newX[-1],newY[-1]),(xList[j],yList[j]))))
            lowest = distances.index(min(distances))

            newX.append(xList[lowest])
            newY.append(yList[lowest])
            xList.pop(lowest)
            yList.pop(lowest)
            #print(distances)


        for i in range(len(newX)):
            for j in range(self.problem.dimension):
                if (self.problem.get_display(self.tour[j])[0]) == newX[i]:
                    if (self.problem.get_display(self.tour[j])[1]) == newY[i]:
                        myTour.append(j+1)

        myTour.append(myTour[0])
        myTour.pop(0)


        newY.append(newY[0])
        newX.append(newX[0])

        #print(newX,newY)
        plt.plot(newX,newY)
        plt.scatter(newX,newY)
        plt.show()



        #print(myTour)
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

    def simulate(self):
        t = 1000000000000000000000000
        cr = 0.00000000000000000000000000000000001
        currentTour = tour()
        print(currentTour.retTour())
        self.currentBest = currentTour

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
                #print(currentTour.retTour())
                #plot = Graph(currentTour.retTour())
                #plot.display_graph()

            if currentTour.findPathLength() < self.currentBest.findPathLength():
                self.currentBest = currentTour
                print("Path length:",self.currentBest.findPathLength())
                plot = Graph(self.currentBest.retTour())
                plot.display_graph()

            t *= 1 - cr
            #print("temp", t)


        print("final length: ", self.currentBest.findPathLength())
        self.finalPath = self.currentBest
        plot = Graph(self.currentBest.retTour())
        plot.display_graph()


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



solve = annealing(prob)
solve.simulate()

# List of best tour
solutionTour = solve.retFinal().retTour()

#print('Final Route: ', solutionTour)
#plot = Graph(solutionTour)
#plot.display_graph()

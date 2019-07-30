import tsplib95 as tsplib
import math
import random
import networkx as nx
import matplotlib.pyplot as plt

class tspSolver():
    def __init__(self):
        self.problem = tsplib.load_problem("in_data/eil51.tsp", special="euclidean_2d_jitter")
        #self.tour = list(range(1, self.problem.dimension + 1))
        self.tour = list(range(1,15))
        self.shortestPathLength = 1000000

    def findPathLength(self):
        pathDistance = 0
        xList = []
        yList = []
        for i in range(0, len(self.tour)):
            xList.append(self.problem.get_display(self.tour[i])[0])
            yList.append(self.problem.get_display(self.tour[i])[1])

        #for i in range(self.problem.dimension-1):
        for i in range(13):
            pathDistance += tsplib.distances.euclidean((xList[i], yList[i]), (xList[i + 1], yList[i + 1]))

        return pathDistance

    def findShortestRandom(self):
        for i in range(2000000):
            random.shuffle(self.tour)
            xList = []
            yList = []
            for i in range(0, len(self.tour)):
                xList.append(self.problem.get_display(self.tour[i])[0])
                yList.append(self.problem.get_display(self.tour[i])[1])

            newDist = self.findPathLength()
            if newDist<self.shortestPathLength:
                self.shortestPathLength = newDist
                print("new shortest =",self.shortestPathLength)
                plt.plot(xList, yList)
                plt.scatter(xList, yList)
                plt.show()

'''
    def nearestNeighbour(self):
        xList = []
        yList = []
        for i in range(0, len(self.tour)):
            xList.append(self.problem.get_display(self.tour[i])[0])
            yList.append(self.problem.get_display(self.tour[i])[1])
        #for i in range(len(self.tour)):
        #    print(xList[i],"|",yList[i])


        x = []
        y = []

        x.append(self.problem.get_display(self.tour[0])[0])
        y.append(self.problem.get_display(self.tour[0])[1])
        dist = 10000000
        for i in range(len(self.tour)):
            j = i
            for j in range(len(self.tour)):
                if(math.sqrt(self.problem.get_display(self.tour[i][0])))
                
        #sqrt((x2-x1)^2+(y2-y1)^2)
        plt.plot(x,y)
        plt.scatter(x,y)
        plt.show()

'''








#---------------------------------------------------------------------------------------------------------------------------

'''
problem = tsp.load_problem('in_data/eil51.tsp',special="euclidean_2d_jitter")
#tour = list(range(1, problem.dimension + 1))
tour = list(range(1,6))

'''
x = tspSolver()
x.findShortestRandom()
#x.nearestNeighbour()

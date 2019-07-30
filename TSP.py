import tsplib95 as tsplib
import math
import random
import networkx as nx
import matplotlib.pyplot as plt

class tspSolver():
    def __init__(self):
        self.problem = tsplib.load_problem("in_data/eil51.tsp", special="euclidean_2d_jitter")
        self.tour = list(range(1, self.problem.dimension + 1))
        self.shortestPathLength = 1000000

    def findPathLength(self):
        pathDistance = 0
        xList = []
        yList = []
        for i in range(0, len(self.tour)):
            xList.append(self.problem.get_display(self.tour[i])[0])
            yList.append(self.problem.get_display(self.tour[i])[1])

        for i in range(self.problem.dimension-1):
            pathDistance += tsplib.distances.euclidean((xList[i], yList[i]), (xList[i + 1], yList[i + 1]))

        return pathDistance

    def findShortest(self):
        for i in range(10000):
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










#---------------------------------------------------------------------------------------------------------------------------

'''
problem = tsp.load_problem('in_data/eil51.tsp',special="euclidean_2d_jitter")
#tour = list(range(1, problem.dimension + 1))
tour = list(range(1,6))

'''
x = tspSolver()
x.findShortest()


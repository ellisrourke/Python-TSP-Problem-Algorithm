import tsplib95 as tsplib
import math
import random
import networkx as nx
import matplotlib.pyplot as plt
import numpy

class tspSolver():
    def __init__(self):
        self.problem = tsplib.load_problem("files/berlin52.tsp", special="euclidean_2d_jitter")
        self.tour = list(range(1, self.problem.dimension + 1))
        self.shortestPathLength = 1000000

    def findPathLength(self,xList,yList):
        pathDistance = 0
        for i in range(0, len(self.tour)):
            xList.append(self.problem.get_display(self.tour[i])[0])
            yList.append(self.problem.get_display(self.tour[i])[1])
        for i in range(self.problem.dimension-1):
        #for i in range(8):
            pathDistance += tsplib.distances.euclidean((xList[i], yList[i]), (xList[i + 1], yList[i + 1]))
        return pathDistance

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
        print(xList,yList)
        xList.pop(0)
        yList.pop(0)

        for i in range(len(xList)):
            distances = []
            for j in range(len(xList)):
                '''find distances to each node'''
                distances.append((tsplib.distances.euclidean((newX[-1],newY[-1]),(xList[j],yList[j]))))
            lowest = distances.index(min(distances))

            newX.append(xList[lowest])
            newY.append(yList[lowest])
            xList.pop(lowest)
            yList.pop(lowest)
            print(distances)


        for i in range(len(newX)):
            for j in range(self.problem.dimension):
                if (self.problem.get_display(self.tour[j])[0]) == newX[i]:
                    if (self.problem.get_display(self.tour[j])[1]) == newY[i]:
                        myTour.append(j)

        myTour.append(myTour[0])


        newY.append(newY[0])
        newX.append(newX[0])
        print(newX,newY)
        plt.plot(newX,newY)
        plt.scatter(newX,newY)
        plt.show()


        print(myTour)
        print("path length found",self.findPathLength(newX,newY))



#---------------------------------------------------------------------------------------------------------------------------


x = tspSolver()
x.nn()
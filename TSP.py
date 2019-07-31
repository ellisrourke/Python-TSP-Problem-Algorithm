import tsplib95 as tsplib
import math
import random
import networkx as nx
import matplotlib.pyplot as plt
import numpy

class tspSolver():
    def __init__(self):
        self.problem = tsplib.load_problem("in_data/eil51.tsp", special="euclidean_2d_jitter")
        #self.tour = list(range(1, self.problem.dimension + 1))
        self.tour = list(range(1,20))
        self.shortestPathLength = 1000000

    def findPathLength(self):
        pathDistance = 0
        xList = []
        yList = []
        for i in range(0, len(self.tour)):
            xList.append(self.problem.get_display(self.tour[i])[0])
            yList.append(self.problem.get_display(self.tour[i])[1])
        #for i in range(self.problem.dimension-1):
        for i in range(18):
            pathDistance += tsplib.distances.euclidean((xList[i], yList[i]), (xList[i + 1], yList[i + 1]))
        return pathDistance


    '''
    def nearestNeighbour(self):
        for i in range(0, len(self.tour)):
            xList.append(self.problem.get_display(self.tour[i])[0])
            yList.append(self.problem.get_display(self.tour[i])[1])

        for i in range(0,len(x)):
            minDist = 9999
            keep = [0,0]
            for j in range(i,len(x)):
                keep = [0, 0]
                dist = tsplib.distances.euclidean((x[i],y[i]),(x[j],y[j]))
                if dist < minDist:
                    minDist = dist
                    if x[j] not in pathx and y[j] not in pathy:
                        minDist = dist
                        keep[0] = x[j]
                        keep[1] = y[j]
            pathx.append(keep[0])
            pathy.append(keep[1])
        plt.plot(pathx, pathy)
        plt.scatter(pathx, pathy)
        plt.show()


    '''
    def findShortestRandom(self):
        for i in range(9999999):
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



    def nn(self):
        xList = []
        yList = []
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

        print(newX,newY)


        plt.plot(newX,newY)
        plt.scatter(newX,newY)
        plt.show()



#---------------------------------------------------------------------------------------------------------------------------

'''
problem = tsp.load_problem('in_data/eil51.tsp',special="euclidean_2d_jitter")
#tour = list(range(1, problem.dimension + 1))
tour = list(range(1,6))

'''
x = tspSolver()
#x.findShortestRandom()
#x.nearestNeighbour()
x.nn()
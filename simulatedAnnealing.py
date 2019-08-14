import random
import math
import tsplib95
import matplotlib.pyplot as plt


prob = tsplib95.load_problem("files/berlin52.tsp")



class tour:
    def __init__(self):
        self.problem = prob = tsplib95.load_problem("files/berlin52.tsp")
        self.tour = list(range(1,self.problem.dimension + 1))
        #random.shuffle(self.tour)
        #self.tour.append(self.tour[0])
        #print(self.tour)

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
        print(xList, yList)
        xList.pop(0)
        yList.pop(0)

        for i in range(len(xList)):
            distances = []
            for j in range(len(xList)):
                '''find distances to each node'''
                distances.append((tsplib95.distances.euclidean((newX[-1], newY[-1]), (xList[j], yList[j]))))
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
                        myTour.append(j+1)

        myTour.append(myTour[0])
        self.tour=myTour


    def retTour(self):
        return self.tour

    def makeSwap(self,a,b):
        temp = self.tour[a]
        self.tour[b]=self.tour[a]
        self.tour[a] = temp


    def findPathLength(self):
        pathDistance = 0
        for i in range(len(self.tour)-1):
            pathDistance += self.problem.wfunc(self.tour[i],self.tour[i+1])
        return pathDistance

class annealing:
    def __init__(self,prob):
        self.problem = prob
        self.finalPath = None


    def acceptProbability(self,t,e,ne):
        if ne < e:
            return 1
        else:
            return math.exp((e-ne)/t)

    def retFinal(self):
        return self.finalPath


    def simulate(self):
        t = 10000
        cr = 0.001
        currentTour = tour()
        currentTour.nn()
        print(currentTour.findPathLength())
        plot = Graph(currentTour.retTour())
        plot.display_graph()



        self.currentBest = currentTour
        #cooling
        while t > 1:
            newTour = tour()

            touri = random.randint(0,(self.problem.dimension)-1)
            tourj = 0
            while tourj != touri:
                tourj = random.randint(0,(self.problem.dimension)-1)
            newTour.makeSwap(touri,tourj)
            print(newTour.retTour())

            ce = currentTour.findPathLength()
            ne = newTour.findPathLength()


            if self.acceptProbability(t,ce,ne) > random.uniform(0,1):
                currentTour = newTour

            if currentTour.findPathLength() < self.currentBest.findPathLength():
                self.currentBest = currentTour
                print(self.currentBest.findPathLength())

                plot=Graph(newTour.retTour())
                plot.display_graph()

            t = t*(1-cr)
            #print("temp",t)

        print("final length: ",self.currentBest.findPathLength())

        self.finalPath = self.currentBest


class Graph:

    def __init__(self, tour):
        self.xList = []
        self.yList = []
        # Populate axes
        for i in range(0, len(tour)):
            self.xList.append(prob.get_display(tour[i])[0])
            self.yList.append(prob.get_display(tour[i])[1])

    def display_graph(self):
        plt.plot(self.xList, self.yList, 'black')
        plt.scatter(self.xList, self.yList)
        plt.xlabel('Node x Position')
        plt.ylabel('Node y Position')
        plt.show()



solution = annealing(prob)

solution.simulate()

# List of best tour
solutionTour = solution.retFinal().retTour()

#print('Final Route: ', solutionTour)

import random
import math
import tsplib95
import matplotlib.pyplot as plt


prob = tsplib95.load_problem("files/eil51.tsp")

class tour:
    def __init__(self):
        self.problem = prob = tsplib95.load_problem("files/eil51.tsp")
        self.tour = list(range(1,self.problem.dimension + 1))
        random.shuffle(self.tour)
        self.tour.append(self.tour[0])

    def retTour(self):
        return self.tour

    def get_len(self):
        return len(self.tour)

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
            return  1

        return math.exp((-(e-ne))/t)

    def retFinal(self):
        return self.finalPath


    def simulate(self):
        t = 100000.0
        cr = 0.00001
        currentTour = tour()

        self.currentBest = currentTour


        #cooling
        while t > 1:
            newTour = tour()

            touri = random.randint(0,(self.problem.dimension)-1)
            tourj = 0
            while tourj != touri:
                tourj = random.randint(0,(self.problem.dimension)-1)

            newTour.makeSwap(touri,tourj)

            ce = currentTour.findPathLength()
            ne = newTour.findPathLength()

            if self.acceptProbability(t,ce,ne) > random.uniform(0,1):
                currentTour = newTour

            if currentTour.findPathLength() < self.currentBest.findPathLength():
                self.currentBest = currentTour
                #print(self.currentBest.findPathLength())
                plot=Graph(self.currentBest.retTour())
                plot.display_graph()

            t *= 1-cr
            print("temp",t)

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
        plt.plot(self.xList, self.yList)
        plt.scatter(self.xList, self.yList)
        plt.title('TSP ')
        plt.xlabel('Node x Position')
        plt.ylabel('Node y Position')
        plt.show()



solution = annealing(prob)
solution.simulate()

# List of best tour
solutionTour = solution.retFinal().retTour()

print('Final Route: ', solutionTour)
print('Start: ', prob.get_display(solutionTour[0]), 'End: ', prob.get_display(solutionTour[-1]))
plot = Graph(solutionTour)
plot.display_graph()
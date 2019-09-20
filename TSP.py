import TSP_db
import math
import matplotlib.pyplot as plt
import random
import time
import copy
import sys
import tkinter
from tkinter import ttk
from tkinter import messagebox
plt.ion()

from matplotlib import style
#style.use('seaborn-dark')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
m=tkinter.Tk()
m.configure(background='#ECECEC')
m.minsize(1000,800)
m.maxsize(1000,800)
figure = plt.Figure( figsize=(4, 4) )
ax = figure.add_subplot(111)
figure.set_facecolor('#ECECEC')
plt.show()
plots = tkinter.Frame(m)

chart_type = FigureCanvasTkAgg(figure, plots)
chart_type2 = FigureCanvasTkAgg(figure,plots)
start_time = 0
results = []
problemDimension = 0
sa = tkinter.IntVar()
nn = tkinter.IntVar()
timeIn = tkinter.StringVar()

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

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def nn(self,x,y):
        xList = []
        yList = []

        myTour = []
        distances = [0 for i in range(len(self.tour))]

        newX = []
        newY = []

        for i in range(0,len(self.tour)):
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
        update(newX,newY)


    def get_len(self):
        return len(self.tour)

    def makeSwap(self, a, b):
        #print(a,b)
        temp = self.tour[a]
        self.tour[a] = self.tour[b]
        self.tour[b] = temp

    def retTour(self,x,y):
        newX,newY = [],[]
        for i in range(0,len(self.tour)-1):
            tourPos = self.tour[i]
            newX.append(x[tourPos])
            newY.append(y[tourPos])

        newX.append(newX[0])
        newY.append(newY[0])
        return (newX,newY)

    def findPathLength(self,x,y):
        #print(x[50])
        pathDistance = 0
        for i in range(0,len(self.tour)-1):
            tourPos = self.tour[i]
            tourPos2 = self.tour[i+1]
            #print(tourPos,i)
            #print(len(x),len(y))
            #print(x[tourPos],y[tourPos])
            #print(tourPos, i)
            pathDistance += calculateDistance(x[tourPos],y[tourPos],x[tourPos2],y[tourPos2])
            #pathDistance = 0

            #pathDistance = 0
        #print(pathDistance)
        return pathDistance

class annealing:
    def __init__(self,thisx,thisy):
        self.x = thisx
        self.y = thisy
        self.finalPath = None
        resetTime()


    def acceptProbability(self, t, e, ne):
        if ne < e:
            return 1
        return math.exp((e - ne) / t)

    def simulate(self,x,y,maxtime):

        self.x = x
        self.y = y
        t = 99999999999999999
        cr = 0.00000000000000001
        currentTour = tour(self.x,self.y)
        self.currentBest = currentTour

        if(nn.get()):
            #print("NN RUNNING")
            self.currentBest.nn(self.x,self.y)

        # cooling
        if(sa.get()):
            #print("SA RUNNING")
            while t > 0 and (time.time() - start_time)<maxtime:
                newtour = tour(self.x,self.y)
                newtour.tour = copy.deepcopy(self.currentBest.tour)

                touri = random.randint(1, len(newtour.tour)-2)
                tourj = random.randint(1, len(newtour.tour)-2)
                while tourj == touri:
                    tourj = random.randint(1, problemDimension-2)

                newtour.makeSwap(touri, tourj)
                ce = self.currentBest.findPathLength(self.x,self.y)
                ne = newtour.findPathLength(self.x,self.y)

                if self.acceptProbability(t, ce, ne) > random.uniform(0,1):
                    currentTour = newtour

                if currentTour.findPathLength(self.x,self.y) < self.currentBest.findPathLength(self.x,self.y):
                    self.currentBest = currentTour
                    data = self.currentBest.retTour(x,y)
                    update(data[0],data[1])
                    solveProblem_currentLength.config(text=self.currentBest.findPathLength(self.x,self.y))
                    #print("Path length:",self.currentBest.findPathLength(self.x,self.y))
                    #print(self.currentBest.x)

                t *= 1 - cr


            #print("final length: ", self.currentBest.findPathLength(self.x,self.y))
            self.finalPath = self.currentBest
            #self.finalPath.tour.append(-1)
            #for i in range(self.problem.dimension+2):
                #print(self.finalPath.retTour()[i])

            #self.finalPath.tour.append(-1)

            return(self.currentBest.findPathLength(self.x,self.y),self.finalPath.tour)


def resetTime():
    global start_time
    start_time = time.time()

def update(x,y,plotBool=1):
    ax.clear()
    if plotBool == 1:
        ax.plot(x,y)
    ax.scatter(x,y)
    figure.canvas.draw()
    figure.canvas.flush_events()



def showProblem():
    try:
        data = TSP_db.getCities(problemName.get())
        update(data[0],data[1],0)

    except:
        messagebox.showerror("Error","problem may not exist in database")

def fetchBest():
    try:
        data = TSP_db.fetch(problemName.get())
        #print(data)
        probN.config(text=data[0])
        dist.config(text=data[1])
        timeLabel.config(text=data[2])
    except:
        messagebox.showerror("Error","Unable to fetch solution")

def run():
    try:
        global problemDimension
        data = TSP_db.getCities(problemName.get())
        problemDimension = data[2]
        x = data[0]
        y = data[1]
        x.append(x[0])
        y.append(y[0])
        #print(len(x),"len")
        solve = annealing(x,y)
        data = solve.simulate(x,y,int(solveProblem_timeAllowed.get()))
        #print(data)

        datastr =  (str(data[1])).replace(",","")
        datastr  = datastr.strip('[]')
        datastr = datastr + " -1"
        #print(datastr)
        if(messagebox.askyesno("Process complete","The solver has completed...\nPush solution to database?")):
            print("test")
            #problem,tourLength,calculationTime,algorithm,tour,solvedBy
            #return(self.finalPath.findPathLength(x,y),self.finalPath.tour)
            TSP_db.submitSolution(problemName.get(),data[0],solveProblem_timeAllowed.get(),"ALG",datastr)
        else:
            print()
    except:
        messagebox.showerror("Error","Unable to solve")


def addProblem():
    TSP_db.addToDatabase(problemName.get())

#prompt and packing for taking the prolem name
probNameFrame = tkinter.Frame(m,pady=15,bg='#ECECEC')
problemNamePrompt = tkinter.Label(probNameFrame,text="Enter problem name",padx=10,font='Laksaman 18 bold',bg='#ECECEC')
problemName = tkinter.Entry(probNameFrame)
problemNamePrompt.pack(side = tkinter.LEFT)
problemName.pack(side = tkinter.LEFT)

#create frames for each button set
#addProbFrame = tkinter.Frame(m, pady=10,padx=10)

optionsFrame = tkinter.Frame(m,borderwidth=5,relief='groove')
addProbFrame = tkinter.Frame(optionsFrame,bd=5,relief='groove')
fetchSolutionFrame = tkinter.Frame(optionsFrame, pady=10,padx=10)
solveProblemFrame = tkinter.Frame(optionsFrame, pady=10,padx=10)

#pack the frames into the root frame
chart_type2.get_tk_widget().pack(side=tkinter.RIGHT)
chart_type.get_tk_widget().pack(side=tkinter.LEFT)



plots.pack(side=tkinter.TOP)
probNameFrame.pack(side = tkinter.TOP)
optionsFrame.pack(side = tkinter.TOP)
addProbFrame.pack(side = tkinter.LEFT,padx=30)
fetchSolutionFrame.pack(side = tkinter.LEFT,padx=30)
solveProblemFrame.pack(side = tkinter.LEFT,padx=30)

#add and pack addProblem buttons
addProb_title = tkinter.Label(addProbFrame,text="Add a problem to the database")
addProb_btn = ttk.Button(addProbFrame,text="Add to database",command=addProblem)
addProb_title.pack( side = tkinter.TOP,pady = 10)
addProb_btn.pack( side = tkinter.TOP ,pady = 10)

w = ttk.Separator(m,orient=tkinter.HORIZONTAL)
w.pack()

#add and pack fetchSolution buttons
fetchSolution_title = tkinter.Label(fetchSolutionFrame,text="Fetch the best solution from the database")
fetchSolution_btn = tkinter.Button(fetchSolutionFrame,text="fetch",command=fetchBest)
probN = tkinter.Label(fetchSolutionFrame)
dist = tkinter.Label(fetchSolutionFrame)
timeLabel = tkinter.Label(fetchSolutionFrame)
fetchSolution_title.pack( side = tkinter.TOP,pady = 10)
fetchSolution_btn.pack( side = tkinter.TOP,pady=10)
probN.pack()
dist.pack()
timeLabel.pack()


#add and pack solveProblem buttons
solveProblem_title = tkinter.Label(solveProblemFrame,text="Solve problem").pack(side = tkinter.TOP,pady = 5)
solveProblem_plotPoints = tkinter.Button(solveProblemFrame,text="plot cities",command=showProblem).pack()

solveProblem_timeAllowedLabel = tkinter.Label(solveProblemFrame,text="time allowed").pack()
solveProblem_timeAllowed = tkinter.Entry(solveProblemFrame,textvariable=timeIn)
solveProblem_timeAllowed.insert(0,"10")
solveProblem_timeAllowed.pack()
nn_option = tkinter.Checkbutton(solveProblemFrame, text="Nearest Neighbour",variable=nn,onvalue = 1, offvalue = 0)
sa_option = tkinter.Checkbutton(solveProblemFrame, text="Simulated Annealing",variable=sa,onvalue = 1, offvalue = 0)
nn_option.pack()
sa_option.pack()
nn_option.toggle()
sa_option.toggle()


solveProblem_btn = tkinter.Button(solveProblemFrame,text="Solve",command=run).pack(side = tkinter.TOP ,pady = 10)
solveProblem_currentLength_title = tkinter.Label(solveProblemFrame,text="Current path Length").pack()
solveProblem_currentLength = tkinter.Label(solveProblemFrame,text="NULL")
solveProblem_currentLength.pack()

plt.show()
m.mainloop()
import tkinter
import random
import math
import time
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
style.use('fivethirtyeight')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def calculateDistance(x1,y1,x2,y2):
     dist = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
     return dist


cities = [0,1,2,3,4,5,6]
x = [5,8,12,34,22,26,19]
y = [8,2,22,6,12,11,15]
oldE = 0


x.append(x[0])
y.append(y[0])
for i in range(7):
    oldE += calculateDistance(x[i],y[i],x[i+1],y[i+1])

m=tkinter.Tk()
figure = plt.Figure()
ax = figure.add_subplot(1,1,1)
chart_type = FigureCanvasTkAgg(figure, m)
chart_type.get_tk_widget().pack()


def makeSwap(lst,a, b):
    print(a,b)
    temp = lst[a]
    lst[a] = lst[b]
    lst[b] = temp

def animate(i):
    global oldE
    newE = 0

    a=random.randint(1,6)
    b=random.randint(1,6)
    while b == a:
        b=random.randint(1,6)
    makeSwap(x,a,b)
    makeSwap(y,a,b)
    print(x)
    print(y)

    for i in range(7):
        newE += calculateDistance(x[i],y[i],x[i+1],y[i+1])
    print(oldE)
    print(newE)
    if newE<=oldE:
        newE = oldE
        ax.clear()
        ax.plot(x,y)
        ax.scatter(x,y)


ani = animation.FuncAnimation(figure,animate,interval=100)

m.mainloop()

#ax.plot(x,y)
#ax.scatter(x,y)



print("hello")

import mysql.connector

connection = mysql.connector.connect(
    host = 'mysql.ict.griffith.edu.au',
    user = 's5057468',
    password = 'ZXGvz7ra',
    database = '1810ICTdb'
)

mycursor = connection.cursor()

def addToDatabase(prob):

    import tsplib95
    problem = tsplib95.load_problem(prob+".tsp")
    dim = problem.dimension
    tour = list(range(0,dim+1))
    sql = "INSERT IGNORE INTO Problem (Name, Size, Comment) VALUES (%s, %s, %s)"
    val = (prob,dim,"NULL")
    try:
        mycursor.execute(sql, val)
    except:
        print()

#add all cities to city table
    for i in range(1,dim+1):
        sql = "INSERT INTO Cities (Name,ID, x, y) VALUES (%s, %s, %s, %s)"
        val = (prob,i,(problem.get_display(tour[i])[0]),(problem.get_display(tour[i])[1]))
        try:
            mycursor.execute(sql, val)
            #print("record inserted.")
        except:
            messagebox.showerror("Error","Problem already exists in database")

            break
        connection.commit()

def fetch(problem):
    sql = "SELECT * FROM Solution WHERE ProblemName = %s AND TourLength = (SELECT min(TourLength) FROM Solution WHERE ProblemName = %s)"
    val = (problem, problem)
    mycursor.execute(sql,val)
    data = mycursor.fetchone()
    return(data)


    connection.commit()

def getCities(problem):
    x = []
    y = []
    sql = """SELECT * from Cities WHERE Name = %s"""
    val = (problem,)

    mycursor.execute(sql, val)
    ret = mycursor.fetchall()

    sql = "SELECT Size FROM Problem WHERE Name = %s"
    val = (problem,)
    mycursor.execute(sql, val)
    dim = mycursor.fetchone()
    dim = dim[0]

    for i in range(0, dim):
        x.append(ret[i][2])
        y.append(ret[i][3])
    return(x,y,dim,)

def submitSolution(prob,tourLen,time,alg,tour):
    sql = "INSERT INTO Solution (ProblemName,TourLength,RunningTime,Algorithm,Tour,Author) VALUES (%s, %s, %s, %s, %s, %s)"
    val = (prob, tourLen, time, 'simulatedAnnealing', tour, 'Ellis Rourke')
    try:
        mycursor.execute(sql, val)
    except:
        print()
    connection.commit()

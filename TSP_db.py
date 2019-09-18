import sys
import mysql.connector
#import TSP

connection = mysql.connector.connect(
    host = 'mysql.ict.griffith.edu.au',
    user = 's5057468',
    password = 'ZXGvz7ra',
    database = 's5057468db'
)

mycursor = connection.cursor()


def add(prob):
    import tsplib95
    problem = tsplib95.load_problem(prob)
    dim = problem.dimension
    print(dim)
    tour = list(range(0,dim+1))
    #print(prob.get_display(tour[0])[i])
    sql = "INSERT IGNORE INTO problem (name, dimention, description) VALUES (%s, %s, %s)"
    val = (sys.argv[1],dim,"NULL")
    try:
        mycursor.execute(sql, val)
    except:
        print("Problem already exists in database")
        exit()

#add all cities to city table
    for i in range(1,dim+1):
        sql = "INSERT INTO cities (name,ID, x, y) VALUES (%s, %s, %s, %s)"
        val = (sys.argv[1],i,(problem.get_display(tour[i])[0]),(problem.get_display(tour[i])[1]))
        try:
            mycursor.execute(sql, val)
            print("record inserted.")
        except:
            print("Problem already exists in database")
            break
    connection.commit()

def fetch(problem):
    sql = "SELECT * from solution WHERE problem = %s AND tourLength = (SELECT min(tourLength) FROM solution WHERE problem = %s)"
    val = (problem,problem)
    try:
        mycursor.execute(sql,val)
        ret = mycursor.fetchone()
        print("\nProblem:",ret[1])
        print("Tour Length:",ret[2])
        print("Calculation Time:",ret[3])
        print("Algorithm:",ret[4],"\n")

    except:
        print("error finding record")
    connection.commit()

'''
def solve(problem):
    x = []
    y = []
    sql = """SELECT * from cities WHERE name = %s"""
    val = (problem,)

    try:
        mycursor.execute(sql,val)
        ret = mycursor.fetchall()
        #print(ret[2][2],ret[2][3])
        sql = "SELECT dimention FROM problem WHERE name = %s"
        val = (sys.argv[1],)
        mycursor.execute(sql,val)
        dim = mycursor.fetchone()
        dim = dim[0]
        print(dim)

        for i in range(0,dim):
            x.append(ret[i][2])
            y.append(ret[i][3])
    except:
        print("problem may not exist in database")
        exit()

    data = TSP.run(x,y,sys.argv[3],dim)
    #print(data[0],data[1])

    datastr = (str(data[1])).replace(",", "")
    datastr = datastr.strip('[]')
    print(datastr)


    sql = "INSERT INTO solution (problem,tourLength,calculationTime,algorithm,tour,solvedBy) VALUES (%s, %s, %s, %s, %s, %s)"
    val = (sys.argv[1],data[0],sys.argv[3],'simulatedAnnealing',datastr,'Ellis Rourke')
    try:
        mycursor.execute(sql, val)
    except:
        print("error occured")
    connection.commit()
'''

def getCities(problem):
    print(problem)
    x = []
    y = []
    sql = """SELECT * from cities WHERE name = %s"""
    val = problem

    try:
            mycursor.execute(sql,val)
            ret = mycursor.fetchall()

            #print(ret[2][2],ret[2][3])
            sql = "SELECT dimention FROM problem WHERE name = %s"
            val = problem
            mycursor.execute(sql,val)
            dim = mycursor.fetchone()
            dim = dim[0]
            print(dim)

            for i in range(0,dim):
                x.append(ret[i][2])
                y.append(ret[i][3])

            return (x, y)

    except:
            print("problem may not exist in database")


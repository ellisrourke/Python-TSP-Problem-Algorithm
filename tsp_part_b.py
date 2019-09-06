import mysql.connector
import tsplib95
import tsp
import sys

connection = mysql.connector.connect(
    host = 'mysql.ict.griffith.edu.au',
    user = 's5057468',
    password = 'ZXGvz7ra',
    database = 's5057468db'
)
mycursor = connection.cursor()
prob = tsplib95.load_problem("files/"+sys.argv[1]+".tsp")

if sys.argv[2] == "ADD":
    tour = list(range(0,52))

    #print(prob.get_display(tour[0])[i])

    sql = "INSERT IGNORE INTO problem (name, dimention, description) VALUES (%s, %s, %s)";

    #WHERE NOT EXISTS (SELECT name FROM problem WHERE name = %s)
    val = (sys.argv[1],51,"NULL")
    try:
        mycursor.execute(sql, val)
    except:
        print("error occured")



#add all cities to city table
    for i in range(1,52):
        sql = "INSERT INTO cities (name,ID, x, y) VALUES (%s, %s, %s, %s)"
        val = (sys.argv[1],i,(prob.get_display(tour[i])[0]),(prob.get_display(tour[i])[1]))
        try:
            mycursor.execute(sql, val)
            print("record inserted.")
        except:
            print("error inserting record")
    connection.commit()







elif sys.argv[2] == "FETCH":
    sql = "SELECT * from solution WHERE problem = %s AND tourLength = (SELECT min(tourLength) FROM solution WHERE problem = %s)"
    val = (sys.argv[1],sys.argv[1])
    try:
        mycursor.execute(sql,val)
        ret = mycursor.fetchall()
        print(ret)
    except:
        print("error finding record")
    connection.commit()
elif sys.argv[2] == "SOLVE":
    x = []
    y = []
    sql = "SELECT * from cities WHERE name = 'eil51'"
    val = (sys.argv[1])
    print(val)
    try:
        mycursor.execute(sql)
        ret = mycursor.fetchall()
        #print(ret[2][2],ret[2][3])
    except:
        print("error")
    for i in range(0,51):
        x.append(ret[i][2])
        y.append(ret[i][3])

    print(x)
    print(y)

    #for i in range(50):
        #print(x[i],y[i])

    data = tsp.run(x,y,sys.argv[3])
'''
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

#execfile('tsp.py')
#tsp.run()

#if sys.argv[2] == FETCH; get the best known solution from the database  python3 TSP_db.py a280 FETCH
#if sys.argv[2] == ADD; add a new problem to the database > python3 TSP_db.py a280 ADD a280.tsp
#is sys.argv[2] == SOLVE; solve the given problem > python3 TSP_db.py a280 SOLVE 300

import mysql.connector
import tsplib95
#import tsp
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
    tour = list(range(1,prob.dimension + 1))
    tour.append(tour[0])
    #print(prob.get_display(tour[0])[i])
    '''
    sql = "INSERT INTO problem (name, dimention, description) VALUES (%s, %s, %s)"
    val = (sys.argv[1],prob.dimension,"NULL")
    mycursor.execute(sql, val)
    '''
#add all cities to city table
    for i in range(1,prob.dimension+1):
        sql = "INSERT INTO cities (name,ID, x, y) VALUES (%s, %s, %s, %s)"
        val = (sys.argv[1],i,prob.get_display(tour[i])[0],prob.get_display(tour[i])[1])
        mycursor.execute(sql, val)

    connection.commit()
    print("record(s) inserted.")


#execfile('tsp.py')
#tsp.run()

#if sys.argv[2] == FETCH; get the best known solution from the database  python3 TSP_db.py a280 FETCH
#if sys.argv[2] == ADD; add a new problem to the database > python3 TSP_db.py a280 ADD a280.tsp
#is sys.argv[2] == SOLVE; solve the given problem > python3 TSP_db.py a280 SOLVE 300

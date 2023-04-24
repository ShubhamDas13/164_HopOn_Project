import mysql.connector
from mysql.connector import Error

# host = "localhost"
# user = "root"
# password = "Shubham1310@"
# db = "HOPON_DB"

def ConnectMySQL(host_name, user_id, Password,db):
    connection = None
    try:
        connection = mysql.connector.connect(
            host = host_name,
            user = user_id,
            password = Password,
            database = db
        )
        print("MySQL Database connection successful")
    except Error as err:
        print(f"Error: '{err}'")
    return connection

def giveQuery(connection, quer):
    curr = connection.cursor()
    curr.execute(quer)
    data = curr.fetchall()
    return data

def insertQuerry(connection, quer):
    curr = connection.cursor()
    curr.execute(quer)
    
# con = ConnectMySQL(host,user,password,db)

# # print("Query 1: Give the Model and registration of the car whose Driver is of age less than and equal to 20")
# print("Output:")
# query1 = "select * from NOTIFICATIONS;"
# data = giveQuery(con, query1)
# for i in data:
#     print(i)


# print("Output:")
# query1 = "Select * from TRANSACTIONS where DriverID_tran = 35912337;"
# data = giveQuery(con, query1)
# for i in data:
#     print(i)


# print("Output:")
# query1 = "DELETE FROM DRIVER  where Driver_ID = 35912337;"
# data = giveQuery(con, query1)
# for i in data:
#     print(i)

# print("Output:")
# query1 = "Select * from TRANSACTIONS where DriverID_tran = 35912337;"
# data = giveQuery(con, query1)
# for i in data:
#     print(i)
# print("Query 1 Done")
# print("")

# print("Query 2: Give the Transaction ID of all the Trip whose starting location is China")
# print("Output:")
# query2 = "SELECT Transaction_ID FROM TRANSACTIONS WHERE TripID_tran in (SELECT Trip_ID FROM TRIP WHERE Pickup_Location = 'China')"
# data = giveQuery(con, query2)
# for i in data:
#     print(i)
# print("Query 2 Done")
# print("")


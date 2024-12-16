import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="Restaurant"
)   

mycursor = mydb.cursor()

def seePlates():
    mycursor.execute("SELECT * FROM plates")
    myresult = mycursor.fetchall()
    return myresult

def selectPlateByName(plate_name):
    mycursor.execute("SELECT * FROM plates WHERE name = %s", (plate_name,))
    myresult = mycursor.fetchall()
    return myresult

def selectPlateById(id):
    mycursor.execute("SELECT * FROM plates WHERE id = %s", (id,))
    myresult = mycursor.fetchall()
    return myresult

def seeOrders():
    mycursor.execute("SELECT * FROM orders")
    myresult = mycursor.fetchall()
    return myresult

def seeTables():
    mycursor.execute("SELECT * FROM tables")
    myresult = mycursor.fetchall()
    return myresult
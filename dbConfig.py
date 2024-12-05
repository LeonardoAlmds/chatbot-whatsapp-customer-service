import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="whatsappPy"
)

mycursor = mydb.cursor()

# Users

def insertUser(username):
    sql = "INSERT INTO users (username) VALUES (%s)"
    val = (username)
    mycursor.execute(sql, val)
    mydb.commit()
    return mycursor.rowcount

def selectUserByUsername(username):
    mycursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    myresult = mycursor.fetchall()
    return myresult

def seeUserLastMessage(username):
    mycursor.execute("SELECT last_message FROM users WHERE username = %s", (username,))
    myresult = mycursor.fetchall()
    return myresult

# Products

def selectAllProduts():
    mycursor.execute("SELECT * FROM products")
    myresult = mycursor.fetchall()
    return myresult

def selectProductById(id):
    mycursor.execute("SELECT * FROM products WHERE id = %s", (id,))
    myresult = mycursor.fetchall()
    return myresult

# Categories

def selectAllCategories():
    mycursor.execute("SELECT * FROM categories")
    myresult = mycursor.fetchall()
    return myresult

def selectCategoryById(id):
    mycursor.execute("SELECT * FROM categories WHERE id = %s", (id,))
    myresult = mycursor.fetchall()
    return myresult

# Brands

def selectAllBrands():
    mycursor.execute("SELECT * FROM brands")
    myresult = mycursor.fetchall()
    return myresult

def selectBrandById(id):
    mycursor.execute("SELECT * FROM brands WHERE id = %s", (id,))
    myresult = mycursor.fetchall()
    return myresult
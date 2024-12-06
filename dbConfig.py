import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="whatsappPy"
)

mycursor = mydb.cursor()

def selectAllProduts():
    mycursor.execute("SELECT * FROM products")
    myresult = mycursor.fetchall()
    return myresult

def selectAllProductsByCategory(category):
    mycursor.execute("SELECT * FROM products WHERE category = %s", (category,))
    myresult = mycursor.fetchall()
    return myresult

def selectAllProductsByBrand(brand):
    mycursor.execute("SELECT * FROM products WHERE brand = %s", (brand,))
    myresult = mycursor.fetchall()
    return myresult

def selectProductById(id):
    mycursor.execute("SELECT * FROM products WHERE id = %s", (id,))
    myresult = mycursor.fetchall()
    return myresult

def selectAllCategories():
    mycursor.execute("SELECT * FROM categories")
    myresult = mycursor.fetchall()
    return myresult

def selectCategoryById(id):
    mycursor.execute("SELECT * FROM categories WHERE id = %s", (id,))
    myresult = mycursor.fetchall()
    return myresult

def selectAllBrands():
    mycursor.execute("SELECT * FROM brands")
    myresult = mycursor.fetchall()
    return myresult

def selectBrandById(id):
    mycursor.execute("SELECT * FROM brands WHERE id = %s", (id,))
    myresult = mycursor.fetchall()
    return myresult
# Need to test if the new parameters are working

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from time import sleep
import dbConfig

options = webdriver.EdgeOptions()
options.add_argument("user-data-dir=C:/caminho/para/pasta/de/perfil")

browser = webdriver.Edge(options=options)
wait = WebDriverWait(browser, 10)
browser.get("https://web.whatsapp.com/")
print("Waiting for you scan your QRcode")
sleep(30)

input_box_xpath = '/html/body/div[1]/div/div/div[3]/div[4]/div/footer/div[1]/div/span/div/div[2]/div[1]/div/div[1]/p'
body = browser.find_element(By.XPATH, '/html/body')
def openUnread():
    unreadMessage = wait.until(
        EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div/div[3]/div[3]/div/div[2]/button[2]'))
    )
    unreadMessage.click()

def firstMessage(input_box):
    messages = [
        "Hello! Welcome to our service.",
        "How can I help you?",
        "",
        "Select one of the options below:"
    ]
    
    
    for message in messages:
        input_box.send_keys(message)
        input_box.send_keys(Keys.SHIFT, Keys.ENTER)

    menu(input_box)
        
    input_box.send_keys(Keys.ENTER)
    

def menu(input_box):
    messages = [
        "Options:",
        "",
        "1 - SEE ALL PRODUCTS",
        "2 - SEE ALL CATEGORIES",
        "3 - SEE ALL BRANDS",
        "4 - EXIT",
        "",
        "Type the number of the option you want to choose:"
    ]

    for message in messages:
        input_box.send_keys(message)
        input_box.send_keys(Keys.SHIFT, Keys.ENTER)

    input_box.send_keys(Keys.ENTER)
    
def productMenu(input_box):
    messages = [
        "Options:",
        "",
        "1 - SEE ALL PRODUCTS",
        "2 - SEE ALL PRODUCTS BY CATEGORY",
        "3 - SEE ALL PRODUCTS BY BRAND",
        "4 - EXIT",
        "",
        "Type the number of the option you want to choose:"
    ]

    for message in messages:
        input_box.send_keys(message)
        input_box.send_keys(Keys.SHIFT, Keys.ENTER)

    input_box.send_keys(Keys.ENTER)

def goodbye(input_box):
    messages = [
        "Thank you for using our service.",
        "Goodbye!",
        "",
        "If you want to use our service again, just send a message."
    ]

    for message in messages:
        input_box.send_keys(message)
        input_box.send_keys(Keys.SHIFT, Keys.ENTER)

    input_box.send_keys(Keys.ENTER)

def readMessage():
    try:

        clientChats = wait.until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, '_akbu'))
        )
        if clientChats:
            return clientChats[-1].text
        else:
            print("Nenhuma mensagem encontrada.")
            return None
    except Exception as e:
        print(f"Erro inesperado: {e}")
        return None

def seeAllProducts(input_box):
    products = dbConfig.selectAllProduts()
    for product in products:
        message = f"Product: {product[1]} - Price: {product[2]}"
        input_box.send_keys(message)
        input_box.send_keys(Keys.SHIFT, Keys.ENTER)
    
    input_box.send_keys(Keys.ENTER)
    
def seeAllProductsByCategory(input_box, category):
    products = dbConfig.selectAllProductsByCategory(category)
    for product in products:
        message = f"Product: {product[1]} - Price: {product[2]}"
        input_box.send_keys(message)
        input_box.send_keys(Keys.SHIFT, Keys.ENTER)
    
    input_box.send_keys(Keys.ENTER)
    
def seeAllProductsByBrand(input_box, brand):
    products = dbConfig.selectAllProductsByBrand(brand)
    for product in products:
        message = f"Product: {product[1]} - Price: {product[2]}"
        input_box.send_keys(message)
        input_box.send_keys(Keys.SHIFT, Keys.ENTER)
    
    input_box.send_keys(Keys.ENTER)

def seeAllCategories(input_box):
    categories = dbConfig.selectAllCategories()
    for category in categories:
        message = f"Category: {category[1]}"
        input_box.send_keys(message)
        input_box.send_keys(Keys.SHIFT, Keys.ENTER)
    
    input_box.send_keys(Keys.ENTER)

def seeAllBrands(input_box):
    brands = dbConfig.selectAllBrands()
    for brand in brands:
        message = f"Brand: {brand[1]}"
        input_box.send_keys(message)
        input_box.send_keys(Keys.SHIFT, Keys.ENTER)
    
    input_box.send_keys(Keys.ENTER)

def getNumber():
    number = wait.until(
        EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div/div[3]/div[4]/div/header/div[2]/div[1]/div/div/span'))
    )
    return number.text

currentService = []

def validationList(phone):
    if phone in currentService:
        return False
    currentService.append(phone)
    print(currentService)
    return True

def removeNumber(phone):
    if phone in currentService:
        currentService.remove(phone)
        print(currentService)

def choices(lastMessage, phone, input_box):
    if lastMessage == "1":
        seeAllProducts(input_box)
    elif lastMessage == "2":
        seeAllCategories(input_box)
    elif lastMessage == "3":
        seeAllBrands(input_box)
    elif lastMessage == "4":
        print("Option4 chosen, removing number")
        goodbye(input_box)
        removeNumber(phone)

def main():
    message = True
    c = True
    while c:
        try:
            openUnread()
            c = False
        except Exception as e:
            print(f"error {e}, trying again")
            openUnread()
    i = 0
    while True:
        while message:
            try:
                bubbleNotifications = browser.find_elements(By.CLASS_NAME, "_ahlk")
                for i in range(len(bubbleNotifications)):
                    notification = bubbleNotifications[i]
                    notification.click()

                    phone = getNumber()
                    valid = validationList(phone)
                    
                    input_box = browser.find_element(By.XPATH, input_box_xpath)
                    body.send_keys(Keys.PAGE_DOWN)
                    
                    if valid:
                        firstMessage(input_box)
                        body.send_keys(Keys.ESCAPE)
                    elif valid != True:
                        lastMessage = readMessage()
                        choices(lastMessage, phone, input_box)
                        menu(input_box)
                        body.send_keys(Keys.ESCAPE)
                    message = False
            except Exception as e:
                print(f"error {e}")
        
        
        message = True

main()
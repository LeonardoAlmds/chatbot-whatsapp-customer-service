from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from time import sleep
from collections import defaultdict

import dbConfig

options = webdriver.ChromeOptions()
options.add_argument("user-data-dir=C:/caminho/para/pasta/de/perfil")

browser = webdriver.Chrome(options=options)
wait = WebDriverWait(browser, 10)
browser.get("https://web.whatsapp.com/")
print("Waiting for you scan your QRcode")
sleep(30)

input_box_xpath = '/html/body/div[1]/div/div/div[3]/div[4]/div/footer/div[1]/div/span/div/div[2]/div[1]/div/div[1]/p'
body = browser.find_element(By.XPATH, '/html/body')
user_budgets = defaultdict(list)

def openUnread():
    unreadMessage = wait.until(
        EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div/div[3]/div[3]/div/div[2]/button[2]'))
    )
    unreadMessage.click()

def paste_content(browser, el, content):
    browser.execute_script(
      f'''
    const text = `{content}`;
    const dataTransfer = new DataTransfer();
    dataTransfer.setData('text', text);
    const event = new ClipboardEvent('paste', {{
    clipboardData: dataTransfer,
    bubbles: true
    }});
    arguments[0].dispatchEvent(event)
    ''',
        el)

def firstMessage(input_box):
    messages = [
        "Olá! Bem-vindo ao nosso serviço! 😄",
        "Como posso ajudar você?",
        "",
        "Selecione uma das opções abaixo: 📝"
    ]

    for message in messages:
        if message:
            paste_content(browser, input_box, message)
            input_box.send_keys(Keys.SHIFT, Keys.ENTER)
            sleep(0.5)
    menu(input_box)

def menu(input_box):
    messages = [
        "📋 *Opções:*",
        "",
        "[1] - VER TODOS OS PRODUTOS",
        "[2] - VER TODAS AS CATEGORIAS",
        "[3] - VER TODAS AS MARCAS",
        "[4] - SAIR 🚪",
        "",
        "✏️ *Digite o número da opção que você deseja escolher:*"
    ]

    for message in messages:
        if message:
            paste_content(browser, input_box, message)
            input_box.send_keys(Keys.SHIFT, Keys.ENTER)

    input_box.send_keys(Keys.ENTER)


def failMenu(input_box):
    failMessage = "❌ Não entendi sua resposta, desculpe! Por favor, escolha uma das opções abaixo:"
    paste_content(browser, input_box, failMessage)
    input_box.send_keys(Keys.SHIFT, Keys.ENTER)
    menu(input_box)
    input_box.send_keys(Keys.ENTER)
    
def productMenu(input_box):
    messages = 'Type the name of the product you want to see:'
    
    input_box.send_keys(messages)

    input_box.send_keys(Keys.ENTER)
    
def goodbye(input_box):
    messages = [
        "🙏 Obrigado por usar o nosso serviço.",
        "👋 Até logo!",
        "",
        "Se quiser usar nosso serviço novamente, basta enviar uma mensagem."
    ]

    for message in messages:
        if message:
            paste_content(browser, input_box, message)
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
    input_box.send_keys("Produtos:")
    input_box.send_keys(Keys.SHIFT, Keys.ENTER)
    for product in products:
        message = f"[{product[0]}] {product[1]} - R${product[2]}"
        input_box.send_keys(message)
        input_box.send_keys(Keys.SHIFT, Keys.ENTER)
    
    input_box.send_keys(Keys.ENTER)

'''def seeAllProductsByCategory(input_box, category):
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
'''

def budget(phone, input_box):
    try:
        input_box.send_keys("Please type the name of the product you want to add to your budget:")
        input_box.send_keys(Keys.ENTER)
        sleep(2)

        product_name = readMessage()

        input_box.send_keys(f"How many units of {product_name} would you like to add?")
        input_box.send_keys(Keys.ENTER)
        sleep(2)

        quantity_message = readMessage()
        try:
            quantity = int(quantity_message)
        except ValueError:
            input_box.send_keys("Invalid quantity. Please enter a valid number.")
            input_box.send_keys(Keys.ENTER)
            return

        product = dbConfig.selectProductByName(product_name)
        if not product:
            input_box.send_keys(f"Sorry, the product '{product_name}' was not found in our inventory.")
            input_box.send_keys(Keys.ENTER)
            return

        product_price = product[2]

        total_price = product_price * quantity

        user_budgets[phone].append({
            "product_name": product_name,
            "product_price": product_price,
            "quantity": quantity,
            "total_price": total_price
        })

        input_box.send_keys(f"{quantity} units of {product_name} added to your budget.")
        input_box.send_keys(Keys.ENTER)

        input_box.send_keys("Would you like to finalize your budget? Type 'yes' to finalize or 'no' to continue adding items.")
        input_box.send_keys(Keys.ENTER)
        sleep(2)

        finalize_message = readMessage().lower()
        if finalize_message == "yes":
            input_box.send_keys("Here is your budget:")
            input_box.send_keys(Keys.ENTER)

            total_budget = 0
            for item in user_budgets[phone]:
                message = f"Product: {item['product_name']}, Unit Price: {item['product_price']}, Quantity: {item['quantity']}, Total: {item['total_price']}"
                input_box.send_keys(message)
                input_box.send_keys(Keys.SHIFT, Keys.ENTER)
                total_budget += item['total_price']

            input_box.send_keys(f"Total Budget: {total_budget}")
            input_box.send_keys(Keys.ENTER)

            user_budgets.pop(phone, None)
        else:
            input_box.send_keys("You can continue adding items to your budget.")
            input_box.send_keys(Keys.ENTER)

    except Exception as e:
        input_box.send_keys(f"An error occurred: {e}")
        input_box.send_keys(Keys.ENTER)

def seeAllCategories(input_box):
    categories = dbConfig.selectAllCategories()
    input_box.send_keys("Categorias:")
    input_box.send_keys(Keys.SHIFT, Keys.ENTER)
    for category in categories:
        message = f"{category[1]}"
        input_box.send_keys(message)
        input_box.send_keys(Keys.SHIFT, Keys.ENTER)
    
    input_box.send_keys(Keys.ENTER)

def seeAllBrands(input_box):
    brands = dbConfig.selectAllBrands()
    input_box.send_keys("Marcas:")
    input_box.send_keys(Keys.SHIFT, Keys.ENTER)
    for brand in brands:
        message = f"{brand[1]}"
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
        print("Option 4 chosen, removing number")
        sleep(0.2)
        goodbye(input_box)
        removeNumber(phone)
    else:
        print("Invalid option")
        sleep(0.2)
        failMenu(input_box)
    
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
            body.send_keys(Keys.ESCAPE)
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
                    elif valid != True:
                        lastMessage = readMessage()
                        choices(lastMessage, phone, input_box)
                    message = False
            except Exception as e:
                print(f"error {e}")
        
        
        message = True

main()
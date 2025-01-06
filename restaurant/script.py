from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

from time import sleep
from collections import defaultdict

import restDbConfig
import payloadPix
import menus

options = webdriver.ChromeOptions()
options.add_argument("--log-level=3") # >> when we go debug this code remove this line <<
options.add_argument("user-data-dir=C:/caminho/para/pasta/de/perfil")

browser = webdriver.Chrome(options=options)
wait = WebDriverWait(browser, 10)
browser.get("https://web.whatsapp.com/")
print("Waiting for you scan your QRcode")
sleep(15)

current_service = []
budget_service = []

input_box_xpath = '//*[@id="main"]/footer/div[1]/div/span/div/div[2]/div[1]/div[2]/div[1]/p'
body = browser.find_element(By.XPATH, '/html/body')

def openUnread():
    unreadMessage = wait.until(
        EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div/div[3]/div/div[3]/div/div[2]/button[2]'))
    )
    unreadMessage.click()

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

def seeAllPlates(input_box):
    plates = restDbConfig.seePlates()
    
    menus.paste_content(browser, input_box, "🍔 *Cardápio:*")
    input_box.send_keys(Keys.SHIFT, Keys.ENTER)
    input_box.send_keys(Keys.SHIFT, Keys.ENTER)
    
    for plate in plates:
        message = f"[{plate[0]}] {plate[1]} - Preço: {plate[2]}"
        input_box.send_keys(message)
        input_box.send_keys(Keys.SHIFT, Keys.ENTER)
    
    input_box.send_keys(Keys.ENTER)

def seeOrders(input_box):
    orders = restDbConfig.seeOrders()
    for order in orders:
        message = f"Pedido: {order[1]} - Mesa: {order[2]}"
        input_box.send_keys(message)
        input_box.send_keys(Keys.SHIFT, Keys.ENTER)
    
    input_box.send_keys(Keys.ENTER)
    
def seeTables(input_box):
    tables = restDbConfig.seeTables()
    for table in tables:
        message = f"Mesa: {table[1]}"
        input_box.send_keys(message)
        input_box.send_keys(Keys.SHIFT, Keys.ENTER)
    
    input_box.send_keys(Keys.ENTER)     

def budgetFailMenu(input_box):
    failMessage = "❌ Não entendi sua resposta, desculpe! Por favor, envie o número do prato ou fim para concluir."
    menus.paste_content(browser, input_box, failMessage)
    input_box.send_keys(Keys.ENTER)

def getNumber():
    print("chegou aqui")
    number = wait.until(
        EC.presence_of_element_located((By.CLASS_NAME, "_amig"))
    )
    print(number.text)
    return number.text

def validationList(phone):
    if phone in current_service:
        return False
    current_service.append(phone)
    print(current_service)
    return True

def budgetList(phone): 
    if phone in budget_service:
        return False
    budget_service.append(phone)
    print(f"Entrei {budget_service}")
    return budget_service

def removeNumberBudget(phone): 
    if phone in budget_service:
        budget_service.remove(phone)
        print(f"Removi o {phone} do budget")

def removeNumber(phone):
    if phone in current_service:
        current_service.remove(phone)
        print(current_service)

def sendPayload(input_box):
    p = payloadPix.Payload("vinicius miguel", "+5581989945697", "10.00", "bezerros", "loja01")
    menus.paste_content(browser, input_box, "📲 *QR Code PIX:*")
    input_box.send_keys(Keys.SHIFT, Keys.ENTER)

    p.generatePayload()
    input_box.send_keys(Keys.CONTROL, 'v')
    sleep(2)
    input_box_img = browser.find_element(By.XPATH, "/html/body/div[1]/div/div/div[3]/div/div[2]/div[2]/span/div/div/div/div[2]/div/div[1]/div[3]/div/div/div[2]/div[1]/div[1]/p")
    input_box_img.send_keys(p.payload)
    input_box_img.send_keys(Keys.ENTER)

def removeValidListInsertBudgetList(phone):
    removeNumber(phone)
    budgetList(phone)

def budgetItems(input_box, phone):
    print(f"Entrei no budgetItems {input_box}, {phone}")

def choices(lastMessage, phone, input_box, browser):
    if lastMessage == "1":
        seeAllPlates(input_box)
    elif lastMessage == "2":
        seeTables(input_box)
    elif lastMessage == "3":
        removeValidListInsertBudgetList(phone)
    elif lastMessage == "4":
        menus.workingHours(input_box, browser)
    elif lastMessage == "5":
        menus.socialMedia(input_box, browser)
    elif lastMessage == "6":
        sleep(0.2)
        menus.goodbye(input_box, browser)
        removeNumber(phone)
    elif lastMessage == "7":
        sendPayload(input_box)
    else:
        print("Invalid option")
        sleep(0.2)
        menus.failMenu(input_box, browser)
    
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

                    if phone in budget_service:
                        budgetItems(input_box, phone)
                    elif valid:
                        menus.firstMessage(input_box, browser)
                    elif valid != True:
                        lastMessage = readMessage()
                        choices(lastMessage, phone, input_box, browser)
                    message = False

                    
            except Exception as e:
                print(f"error {e}")
        
        message = True

main()
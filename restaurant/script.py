from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from time import sleep
from collections import defaultdict

import restDbConfig

options = webdriver.ChromeOptions()
options.add_argument("--log-level=3") # >> when we go debug this code remove this line <<
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
        "Olá! Bem vindo ao nosso atendente virtual! 😄",
        "Como posso ajudar você hoje?",
        "",
        "A promoção de hoje é: 🎉",
        "",
        "🍔 *Hamburguer* - R$ 10,00",
        "🍟 *Batata Frita* - R$ 5,00",
        "Para mais informações, digite *MENU*.",
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
        "[1] - VER CARDÁPIO 🍔",
        "[2] - LUGARES DISPONÍVEIS 📍",
        "[3] - FAZER PEDIDO 🛒",
        "[4] - HORÁRIO DE FUNCIONAMENTO ⏰",
        "[5] - REDES SOCIAIS 📱",
        "[6] - SAIR 🚪",
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

def inProgress(input_box):
    inProgressMessage = "🔄 Essa função está em desenvolvimento, aguarde..."
    paste_content(browser, input_box, inProgressMessage)
    input_box.send_keys(Keys.ENTER)
    
def workingHours(input_box):
    workingHoursMessage = "🕒 Nosso horário de funcionamento é de segunda a sábado, das 11h às 22h."
    paste_content(browser, input_box, workingHoursMessage)
    input_box.send_keys(Keys.ENTER)
    
def socialMedia(input_box):
    messages = [
        "📱 *Redes Sociais:*"
        "",
        "📸 *Instagram:* @restaurante",
        "👍 *Facebook:* /restaurante",
        "🐦 *Twitter:* @restaurante"
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

def seeAllPlates(input_box):
    plates = restDbConfig.seePlates()
    
    paste_content(browser, input_box, "🍔 *Cardápio:*")
    input_box.send_keys(Keys.SHIFT, Keys.ENTER)
    input_box.send_keys(Keys.SHIFT, Keys.ENTER)
    
    for plate in plates:
        message = f"{plate[1]} - Preço: {plate[2]}"
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
        seeAllPlates(input_box)
    elif lastMessage == "2":
        seeTables(input_box)
    elif lastMessage == "3":
        inProgress(input_box)
    elif lastMessage == "4":
        workingHours(input_box)
    elif lastMessage == "5":
        socialMedia(input_box)
    elif lastMessage == "6":
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
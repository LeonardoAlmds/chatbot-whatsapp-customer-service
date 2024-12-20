from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from time import sleep
from collections import defaultdict
import payloadPix
import pyautogui as py

import restDbConfig

options = webdriver.ChromeOptions()
options.add_argument("--log-level=3") # >> when we go debug this code remove this line <<
options.add_argument("user-data-dir=C:/caminho/para/pasta/de/perfil")

browser = webdriver.Chrome(options=options)
wait = WebDriverWait(browser, 10)
browser.get("https://web.whatsapp.com/")
print("Waiting for you scan your QRcode")
sleep(30)

input_box_xpath = '//*[@id="main"]/footer/div[1]/div/span/div/div[2]/div[1]/div[2]/div[1]/p'
body = browser.find_element(By.XPATH, '/html/body')
user_budgets = defaultdict(list)

def openUnread():
    unreadMessage = wait.until(
        EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div/div[3]/div/div[3]/div/div[2]/button[2]'))
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
    
user_budgets = defaultdict(list)  # To store user selections

currentRequest = []
def budgetFailMenu(input_box):
    failMessage = "❌ Não entendi sua resposta, desculpe! Por favor, envie o número do prato ou fim para concluir."
    paste_content(browser, input_box, failMessage)
    input_box.send_keys(Keys.ENTER)

def arrayBudget(phone):
    if phone in currentRequest:
        return False
    currentRequest.append(phone)
    print(currentRequest)
    return True
def removeBudget(phone):
    if phone in currentRequest:
        currentRequest.remove()
        print("number removed")

def budget(phone, input_box):
    request = {}  
    arrayBudget(phone) 
    
    paste_content(browser, input_box, "🛒 *Montagem do Pedido*")
    input_box.send_keys(Keys.ENTER)
    paste_content(browser, input_box, "Escolha os itens do cardápio pelo número (ou digite 'fim' para concluir):")
    input_box.send_keys(Keys.ENTER)

    while True:
        user_message = readMessage().strip().lower()
        print(f"Mensagem recebida: {user_message}")  # Debug

        if user_message == "fim":
            paste_content(browser, input_box, "✅ Pedido concluído!")
            input_box.send_keys(Keys.ENTER)
            break 
        if user_message == "1":
            request["pizza"] = 10
        elif user_message == "2":
            request["pasta"] = 8
        elif user_message == "3":
            request["salad"] = 5
        elif user_message == "4":
            request["bread"] = 2
        elif user_message == "5":
            request["water"] = 1
        elif user_message == "6":
            request["soda"] = 2
        else:
            budgetFailMenu(input_box) 
            continue
        paste_content(browser, input_box, f"📝 *Resumo Atual:* {request}")
        input_box.send_keys(Keys.ENTER)

    total_price = sum(request.values())
    save_to_file(phone, [{"name": k, "price": v} for k, v in request.items()], total_price)
    paste_content(browser, input_box, f"💰 *Valor Total:* R$ {total_price:.2f}")
    input_box.send_keys(Keys.ENTER)



def calculate_total_price(plates):
    """
    Calculate the total price of the plates in the user's budget.
    """
    total = sum(plate["price"] for plate in plates)
    return total

def save_to_file(phone, plates, total_price):
    """
    Save the user's budget to a text file.
    """
    filename = f"budget_{phone}.txt"
    with open(filename, "w", encoding="utf-8") as file:
        file.write(f"Pedido do usuário: {phone}\n")
        file.write("Pratos selecionados:\n")
        for plate in plates:
            file.write(f"- {plate['name']} - R$ {plate['price']:.2f}\n")
        file.write(f"\nValor Total: R$ {total_price:.2f}")

def getNumber():
    print("chegou aqui")
    number = wait.until(
        EC.presence_of_element_located((By.CLASS_NAME, "_amig"))
    )
    print(number.text)
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

def sendPayload(input_box):
    p = payloadPix.Payload("vinicius miguel", "+5581989945697", "10.00", "bezerros", "loja01")
    paste_content(browser, input_box, "📲 *QR Code PIX:*")
    input_box.send_keys(Keys.SHIFT, Keys.ENTER)

    p.generatePayload()
    input_box.send_keys(Keys.CONTROL, 'v')
    sleep(2)
    input_box_img = browser.find_element(By.XPATH, "/html/body/div[1]/div/div/div[3]/div/div[2]/div[2]/span/div/div/div/div[2]/div/div[1]/div[3]/div/div/div[2]/div[1]/div[1]/p")
    input_box_img.send_keys(p.payload)
    input_box_img.send_keys(Keys.ENTER)

def choices(lastMessage, phone, input_box):
    if lastMessage == "1":
        seeAllPlates(input_box)
    elif lastMessage == "2":
        seeTables(input_box)
    elif lastMessage == "3":
        budget(input_box, phone)  # Start the budget process
    elif lastMessage == "4":
        workingHours(input_box)
    elif lastMessage == "5":
        socialMedia(input_box)
    elif lastMessage == "6":
        sleep(0.2)
        goodbye(input_box)
        removeNumber(phone)
    elif lastMessage == "7":
        sendPayload(input_box)
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
            #body.send_keys(Keys.ESCAPE)
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
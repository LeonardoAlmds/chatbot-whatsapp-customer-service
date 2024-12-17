from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from time import sleep
from collections import defaultdict

import restDbConfig

options = webdriver.EdgeOptions()
options.add_argument("--log-level=3") # >> when we go debug this code remove this line <<
options.add_argument("user-data-dir=C:/caminho/para/pasta/de/perfil")

browser = webdriver.Edge(options=options)
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

def budget(input_box, phone):
    """
    Function to handle user selections for plates and calculate the total budget.
    """
    paste_content(browser, input_box, "🛒 *Vamos montar seu pedido!*")
    input_box.send_keys(Keys.ENTER)
    sleep(1)

    paste_content(browser, input_box, "Envie o número do prato desejado ou digite *fim* para finalizar o pedido.")
    input_box.send_keys(Keys.ENTER)

    while True:
        lastMessage = readMessage()  # Read the last message sent by the user
        if lastMessage.lower() == "fim":
            total_price = calculate_total_price(user_budgets[phone])
            save_to_file(phone, user_budgets[phone], total_price)
            paste_content(browser, input_box, f"✅ Pedido finalizado! Valor total: R$ {total_price:.2f}")
            input_box.send_keys(Keys.ENTER)
            return

        if lastMessage.isdigit():
            plate_id = int(lastMessage)
            plate = restDbConfig.selectPlateById(plate_id)
            if plate:
                plate_name = plate[0][1]
                plate_price = plate[0][2]
                user_budgets[phone].append({"id": plate_id, "name": plate_name, "price": plate_price})
                
                paste_content(browser, input_box, f"📝 *{plate_name}* adicionado ao pedido. Preço: R$ {plate_price:.2f}")
                input_box.send_keys(Keys.ENTER)
                sleep(0.5)
                paste_content(browser, input_box, "Digite outro número ou *fim* para finalizar.")
                input_box.send_keys(Keys.ENTER)
            else:
                paste_content(browser, input_box, "❌ Prato não encontrado. Por favor, envie um ID válido.")
                input_box.send_keys(Keys.ENTER)
        else:
            paste_content(browser, input_box, "⚠️ Por favor, envie apenas o número do prato ou *fim* para concluir.")
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
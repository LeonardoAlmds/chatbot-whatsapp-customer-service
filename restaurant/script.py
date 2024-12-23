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

from menus import paste_content

options = webdriver.ChromeOptions()
options.add_argument("--log-level=3") # >> when we go debug this code remove this line <<
options.add_argument("user-data-dir=C:/caminho/para/pasta/de/perfil")

browser = webdriver.Chrome(options=options)
wait = WebDriverWait(browser, 10)
browser.get("https://web.whatsapp.com/")
print("Waiting for you scan your QRcode")
sleep(15)

input_box_xpath = '//*[@id="main"]/footer/div[1]/div/span/div/div[2]/div[1]/div[2]/div[1]/p'
body = browser.find_element(By.XPATH, '/html/body')
user_budgets = defaultdict(list)

cart = {}

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
    
user_budgets = defaultdict(list)  # To store user selections1

currentRequest = []
def budgetFailMenu(input_box):
    failMessage = "❌ Não entendi sua resposta, desculpe! Por favor, envie o número do prato ou fim para concluir."
    menus.paste_content(browser, input_box, failMessage)
    input_box.send_keys(Keys.ENTER)

def budget(input_box, phone):
    removeNumber(phone)
    budgetList(phone)
    
    paste_content(browser, input_box, "🛒 *Montagem do Pedido*")
    input_box.send_keys(Keys.SHIFT, Keys.ENTER)
    input_box.send_keys(Keys.SHIFT, Keys.ENTER)
    seeAllPlates(input_box)

import time  # Para adicionar delays e facilitar o debugging

def add(lastMessage, phone, input_box):
    # Inicializando o carrinho como um dicionário
    budget(input_box, phone)  # Envia orçamento inicial

    # Obtendo os pratos disponíveis
    plates = restDbConfig.seePlates()

    while True:
        input_box = browser.find_element(By.XPATH, input_box_xpath)
        print("Recebendo mensagem:", lastMessage)  # Log de entrada
        time.sleep(1)  # Tempo para visualização

        # Se a mensagem for "fim", sair do loop
        if lastMessage.lower() == "fim":
            removeBudget(phone)
            validationList(phone)

            print("Finalizando o processo.")
            time.sleep(1)  # Tempo para visualização
            break

        # Procurando o prato correspondente
        matching_plate = next((plate for plate in plates if str(lastMessage) == str(plate[0])), None)

        if matching_plate:
            input_box = browser.find_element(By.XPATH, input_box_xpath)
            print(f"Prato encontrado: {matching_plate[1]}")  # Log do prato encontrado
            time.sleep(1)  # Tempo para visualização

            # Adiciona o telefone ao dicionário se não existir
            if phone not in cart:
                cart[phone] = []
                print(f"Novo carrinho criado para {phone}")  # Log para novo carrinho
                time.sleep(1)  # Tempo para visualização

            # Perguntar quantos itens o cliente deseja
            input_box.send_keys(f"Quantos itens do prato {matching_plate[1]} você gostaria de adicionar?")
            input_box.send_keys(Keys.ENTER)
            print("Perguntando quantidade...")  # Log de pergunta de quantidade
            time.sleep(1)  # Tempo para visualização

            # Espera pela resposta com a quantidade
            quantity = int(lastMessage)  # Obtém a quantidade fornecida pelo cliente
            print(f"Quantidade recebida: {quantity}")  # Log da quantidade
            time.sleep(1)  # Tempo para visualização

            # Verifica se o prato já não está no carrinho antes de adicionar
            plate_in_cart = next((item for item in cart[phone] if item[0] == matching_plate[0]), None)

            if plate_in_cart:
                print(f"Prato {matching_plate[1]} já está no carrinho, atualizando a quantidade.")  # Log de atualização
                plate_in_cart[3] += quantity  # Atualiza a quantidade no carrinho
                input_box.send_keys(f"Atualizado: {quantity} unidades de {matching_plate[1]} no seu carrinho.")
                input_box.send_keys(Keys.ENTER)
                time.sleep(1)  # Tempo para visualização
            else:
                input_box = browser.find_element(By.XPATH, input_box_xpath)

                print(f"Adicionando {quantity} unidades de {matching_plate[1]} ao carrinho.")  # Log de adição
                cart[phone].append([matching_plate[0], matching_plate[1], matching_plate[2], quantity])
                input_box.send_keys(f"Adicionado: {quantity} unidades de {matching_plate[1]} ao seu carrinho.")
                input_box.send_keys(Keys.ENTER)
                time.sleep(1)  # Tempo para visualização



            input_box = browser.find_element(By.XPATH, input_box_xpath)

            # Montar a mensagem do carrinho completo
            cart_message = "Seu carrinho atual:\n"
            for item in cart[phone]:
                cart_message += f"- {item[1]} (ID: {item[0]}, Preço: {item[2]}, Quantidade: {item[3]})\n"

            print("Exibindo o carrinho:")  # Log de exibição do carrinho
            print(cart_message)  # Exibe o carrinho no console para debug
            
            
            # Envia a mensagem completa de uma vez
            input_box.send_keys(cart_message)
            input_box.send_keys(Keys.ENTER)
            time.sleep(1)  # Tempo para visualização

        else:
            input_box = browser.find_element(By.XPATH, input_box_xpath)
            input_box.send_keys(phone, "Desculpe, prato não encontrado. Por favor, tente novamente com um ID válido.")
            input_box.send_keys(Keys.ENTER)
            print("Prato não encontrado. Solicitando ao usuário que tente novamente.")  # Log de erro
            time.sleep(1)  # Tempo para visualização

        # Exibe o carrinho atual no console (debug)
        print("Estado do carrinho:", cart)
        time.sleep(1)  # Tempo para visualização


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
budget_service = []

def validationList(phone):
    if phone in currentService:
        return False
    currentService.append(phone)
    print(currentService)
    return True

def budgetList(phone): 
    if phone in budget_service:
        return False
    budget_service.append(phone)
    print(budget_service)
    return True

def removeBudget(phone):
    if phone in budget_service:
        budget_service.remove(phone)
        print(budget_service)

def removeNumber(phone):
    if phone in currentService:
        currentService.remove(phone)
        print(currentService)

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

def choices(lastMessage, phone, input_box, browser):
    if lastMessage == "1":
        seeAllPlates(input_box)
    elif lastMessage == "2":
        seeTables(input_box)
    elif lastMessage == "3":
        budget(input_box, phone)  # Start the budget process
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
                    budget_service = budgetList(phone)
                    
                    input_box = browser.find_element(By.XPATH, input_box_xpath)
                    body.send_keys(Keys.PAGE_DOWN)
                    
                    if budget_service == True:
                        menus.firstMessage(input_box, browser)
                    elif valid:
                        lastMessage = readMessage()
                        add(lastMessage, phone, input_box)
                    elif valid != True:
                        lastMessage = readMessage()
                        choices(lastMessage, phone, input_box, browser)
                    message = False
                    
            except Exception as e:
                print(f"error {e}")
        
        message = True

main()
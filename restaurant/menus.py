from selenium.webdriver.common.keys import Keys
from time import sleep

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

def firstMessage(input_box, browser):
    messages = [
        "Olá! Bem vindo ao nosso atendente virtual! 😄",
        "Como posso ajudar você hoje?",
        "",
        "A promoção do dia é: 🎉",
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
    menu(input_box, browser)

# Make less options, to make the menu more intuitive
def menu(input_box, browser):
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

def failMenu(input_box, browser):
    failMessage = "❌ Não entendi sua resposta, desculpe! Por favor, escolha uma das opções abaixo:"
    paste_content(browser, input_box, failMessage)
    input_box.send_keys(Keys.SHIFT, Keys.ENTER)
    menu(input_box, browser)
    input_box.send_keys(Keys.ENTER)
    input_box.send_keys(Keys.ESCAPE)

def goodbye(input_box, browser):
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

def inProgress(input_box, browser):
    inProgressMessage = "🔄 Essa função está em desenvolvimento, aguarde..."
    paste_content(browser, input_box, inProgressMessage)
    input_box.send_keys(Keys.ENTER)
    
def workingHours(input_box, browser):
    workingHoursMessage = "🕒 Nosso horário de funcionamento é de segunda a sábado, das 11h às 22h."
    paste_content(browser, input_box, workingHoursMessage)
    input_box.send_keys(Keys.ENTER)
    
def socialMedia(input_box, browser):
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


from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
import time
from time import sleep

import dbConfig

service = Service()
option = webdriver.EdgeOptions()
option.add_argument("user-data-dir=C:/caminho/para/pasta/de/perfil")
driver = webdriver.Edge(service=service, options=option)

wait = WebDriverWait(driver, 10)
whatsapp_url = "https://web.whatsapp.com/"
driver.get(whatsapp_url)
print("Scan the QR code and wait for login")

coxinha = True

def menu():
    input_message = wait.until(
        EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div/div[3]/div[4]/div/footer/div[1]/div/span/div/div[2]/div[1]/div/div[1]/p'))
    )

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
        input_message.send_keys(message)
        input_message.send_keys(Keys.SHIFT, Keys.ENTER)

    #input_message.send_keys(Keys.ENTER)

def openUnread():
    unreadMessage = wait.until(
        EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div/div[3]/div[3]/div/div[2]/button[2]'))
    )
    unreadMessage.click()

def seeAllProducts():
    products = dbConfig.selectAllProduts()
    input_message = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div[3]/div[4]/div/footer/div[1]/div/span/div/div[2]/div[1]/div/div[1]/p')
    for product in products:
        message = f"Product: {product[1]} - Price: {product[2]}"
        input_message.send_keys(message)
        input_message.send_keys(Keys.SHIFT, Keys.ENTER)
    
    #input_message.send_keys(Keys.ENTER)

def seeAllCategories():
    categories = dbConfig.selectAllCategories()
    input_message = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div[3]/div[4]/div/footer/div[1]/div/span/div/div[2]/div[1]/div/div[1]/p')
    for category in categories:
        message = f"Category: {category[1]}"
        input_message.send_keys(message)
        input_message.send_keys(Keys.SHIFT, Keys.ENTER)
    
    #input_message.send_keys(Keys.ENTER)

def seeAllBrands():
    brands = dbConfig.selectAllBrands()
    input_message = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div[3]/div[4]/div/footer/div[1]/div/span/div/div[2]/div[1]/div/div[1]/p')
    for brand in brands:
        message = f"Brand: {brand[1]}"
        input_message.send_keys(message)
        input_message.send_keys(Keys.SHIFT, Keys.ENTER)
    
    #input_message.send_keys(Keys.ENTER)

def main():
    global coxinha
    c = True
    while c:
        try:
            openUnread()
            c = False
        except Exception as e:
            print(f"error {e}, trying again")
            openUnread()
    
    while True:
        sleep(1)
        while coxinha:
            sleep(2)
            try:
                bubbleNotifications = driver.find_elements(By.CLASS_NAME, "_ahlk")
                for i in range(len(bubbleNotifications)):
                    notification = bubbleNotifications[i]
                    notification.click()
                    
                    print("Reading received messages...")
                    
                    message_hour = driver.find_elements(By.CLASS_NAME, 'x1rg5ohu.x16dsc37')
                    last_hour = message_hour[-1].text
                    
                    boolean = True
                    
                    start_time = time.time()
                    while boolean:
                        sleep(5)

                        received_messages = driver.find_elements(By.CSS_SELECTOR, 'div.message-in span.selectable-text')
                        
                        print(received_messages[-1].text)
                                
                        last_message = received_messages[-1].text
                                
                        print(f"New message received: {last_message}" + " at " + last_hour)

                        if last_message == "1":
                            print("Seeing all products...")
                            seeAllProducts()
                            menu()
                        elif last_message == "2":
                            print("Seeing all categories...")
                            seeAllCategories()
                            menu()
                        elif last_message == "3":
                            print("Seeing all brands...")
                            seeAllBrands()
                            menu()
                        elif last_message == "4":
                            print("Exiting...")
                            boolean = False
                            break
                        else:
                            print("Invalid option. Try again.")
                            menu()

                        if time.time() - start_time > 30:
                            print("No new messages received in the last 30 seconds.")
                            boolean = False
                    
                    coxinha = False
                sleep(2)
            except Exception as e:
                print(f"error {e}")
        coxinha = True
        
main()
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
import time

import dbConfig

service = Service()
option = webdriver.EdgeOptions()
driver = webdriver.Edge(service=service, options=option)


def menu():
    input_message = wait.until(
        EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div/div[3]/div[4]/div/footer/div[1]/div/span/div/div[2]/div[1]/div/div[1]/p'))
    )

    message = "Options: "
    input_message.send_keys(message)
    input_message.send_keys(Keys.SHIFT, Keys.ENTER)
    input_message.send_keys(Keys.SHIFT, Keys.ENTER)

    message = "1 - SEE ALL PRODUCTS"
    input_message.send_keys(message)
    input_message.send_keys(Keys.SHIFT, Keys.ENTER)

    message = "2 - SEE ALL CATEGORIES"
    input_message.send_keys(message)
    input_message.send_keys(Keys.SHIFT, Keys.ENTER)

    message = "3 - SEE ALL BRANDS"
    input_message.send_keys(message)
    input_message.send_keys(Keys.SHIFT, Keys.ENTER)

    message = "4 - EXIT"
    input_message.send_keys(message)
    input_message.send_keys(Keys.SHIFT, Keys.ENTER)
    input_message.send_keys(Keys.SHIFT, Keys.ENTER)

        
    message = "Type the number of the option you want to choose: "
    input_message.send_keys(message)
    input_message.send_keys(Keys.ENTER)

def seeAllProducts():
    products = dbConfig.selectAllProduts()
    input_message = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div[3]/div[4]/div/footer/div[1]/div/span/div/div[2]/div[1]/div/div[1]/p')
    for product in products:
        message = f"Product: {product[1]} - Price: {product[2]}"
        input_message.send_keys(message)
        input_message.send_keys(Keys.SHIFT, Keys.ENTER)
    
    input_message.send_keys(Keys.ENTER)
    
def seeAllCategories():
    categories = dbConfig.selectAllCategories()
    input_message = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div[3]/div[4]/div/footer/div[1]/div/span/div/div[2]/div[1]/div/div[1]/p')
    for category in categories:
        message = f"Category: {category[1]}"
        input_message.send_keys(message)
        input_message.send_keys(Keys.SHIFT, Keys.ENTER)
    
    input_message.send_keys(Keys.ENTER)
    
def seeAllBrands():
    brands = dbConfig.selectAllBrands()
    input_message = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div[3]/div[4]/div/footer/div[1]/div/span/div/div[2]/div[1]/div/div[1]/p')
    for brand in brands:
        message = f"Brand: {brand[1]}"
        input_message.send_keys(message)
        input_message.send_keys(Keys.SHIFT, Keys.ENTER)
    
    input_message.send_keys(Keys.ENTER)

try:
    whatsapp_url = "https://web.whatsapp.com/"
    driver.get(whatsapp_url)
    print("Scan the QR code and wait for login")

    wait = WebDriverWait(driver, 600)
    search_bar = wait.until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="side"]/div[1]/div/div[2]/div[2]/div/div[1]/p'))
    )
    print("Logged in successfully")

    contact_name = "+55 81 9569-0977"
    search_bar.send_keys(contact_name)
    search_bar.send_keys(Keys.ENTER)

    input_message = wait.until(
        EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div/div[3]/div[4]/div/footer/div[1]/div/span/div/div[2]/div[1]/div/div[1]/p'))
    )

    message = "Hello, this is an automated message using Python and Selenium."
    input_message.send_keys(message)
    input_message.send_keys(Keys.SHIFT, Keys.ENTER)
    input_message.send_keys(Keys.SHIFT, Keys.ENTER)
    
    message2 = "How can I help you today?"
    input_message.send_keys(message2)
    input_message.send_keys(Keys.ENTER)
    
    menu()

    print("Messages sent successfully")
    print("Reading received messages...")

    last_message_count = len(driver.find_elements(By.CSS_SELECTOR, 'div.message-in span.selectable-text'))
    
    message_hour = driver.find_elements(By.CLASS_NAME, 'x1rg5ohu.x16dsc37')
    last_hour = message_hour[-1].text
    
    while True:
        time.sleep(5)

        received_messages = driver.find_elements(By.CSS_SELECTOR, 'div.message-in span.selectable-text')
        current_message_count = len(received_messages)

        if current_message_count > last_message_count:
            new_messages = received_messages[last_message_count:]
            for message_element in new_messages:
                last_message = message_element.text
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
                    break
                else:
                    print("Invalid option. Try again.")
                    menu()

            last_message_count = current_message_count

except Exception as e:
    print(f"An error occurred: {e}")
finally:
    driver.quit()

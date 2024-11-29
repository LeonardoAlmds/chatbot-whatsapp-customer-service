from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
import time

service = Service()
option = webdriver.EdgeOptions()
driver = webdriver.Edge(service=service, options=option)

try:
    whatsapp_url = "https://web.whatsapp.com/"
    driver.get(whatsapp_url)
    print("Scan the QR code and wait for login")

    wait = WebDriverWait(driver, 600)
    search_bar = wait.until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="side"]/div[1]/div/div[2]/div[2]/div/div[1]/p'))
    )
    print("Logged in successfully")

    contact_name = "+55 81 8994-5697"
    search_bar.send_keys(contact_name)
    search_bar.send_keys(Keys.ENTER)

    input_message = wait.until(
        EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div/div[3]/div[4]/div/footer/div[1]/div/span/div/div[2]/div[1]/div/div[1]/p'))
    )
    
    username = wait.until(
        EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div/div[3]/div[4]/div/header/div[2]/div/div/div/span'))
    )
    print("Contact found successfully:", username.text)

    message = "Hello, this is an automated message using Python and Selenium."
    input_message.send_keys(message)
    input_message.send_keys(Keys.SHIFT, Keys.ENTER)
    input_message.send_keys(Keys.SHIFT, Keys.ENTER)
    
    message2 = "How can I help you today?"
    input_message.send_keys(message2)
    input_message.send_keys(Keys.ENTER)

    print("Messages sent successfully")
    
finally:
    time.sleep(5)
    driver.quit()

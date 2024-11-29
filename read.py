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

whatsapp_url = "https://web.whatsapp.com/"
driver.get(whatsapp_url)
print("Scan the QR code and wait for login")

try:
    wait = WebDriverWait(driver, 600)
    search_bar = wait.until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="side"]/div[1]/div/div[2]/div[2]/div/div[1]/p'))
    )
    print("Logged in successfully")

    contact_name = "+55 81 8994-5697"
    search_bar.send_keys(contact_name)
    search_bar.send_keys(Keys.ENTER)
    
    username = wait.until(
        EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div/div[3]/div[4]/div/header/div[2]/div/div/div/span'))
    )
    print("Contact found successfully:", username.text)
    
    print("Reading messages...")
    
    chatMessage = driver.find_elements(By.CLASS_NAME, "_akbu")
    
    for message in chatMessage:
        print("Message from:", username.text + "on: " + time.strftime("%d/%m/%Y %H:%M:%S"))
        print(message.text + "\n")
    
    print("Messages read successfully")
    
finally:
    time.sleep(5)
    driver.quit()
        

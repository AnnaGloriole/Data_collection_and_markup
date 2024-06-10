import selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
import pandas as pd
import csv

options = Options()
options.add_argument('start-maximized')
driver = webdriver.Chrome(options=options)
driver.get('https://wildberries.ru/')

time.sleep(0.5)
input = driver.find_element(By.ID, "searchInput")
input.send_keys('сервиз фарфор 6 персон синий')
input.send_keys(Keys.ENTER)

time.sleep(20)

while True:

    while True:
        wait = WebDriverWait(driver, 30)
        cards = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//article[@id]')))
        # cards = driver.find.element(By.XPATH, '//article[@id]')
        print(len(cards))
        count = len(cards)    
        driver.execute_script("window.scrollBy(0, 2000)")
        time.sleep(2)
        cards = driver.find_elements(By.XPATH, '//article[@id]')
        if len(cards) == count:
            break
    
    # Парсим данные
    goods = []
    try:
        for card in cards:
            price = card.find_element(By.CLASS_NAME, "price__lower-price").text
            name = card.find_element(By.XPATH, "./div/a").get_attribute('aria-label')
            url = card.find_element(By.XPATH, "./div/a").get_attribute('href')
            goods.append({price, name, url})
            print(name, price, url)
    except Exception as e:
        print(f"Ошибка: {e}")
        break
        
    # Переходим по кнопке дальше
    try:
        button = driver.find_element(By.CLASS_NAME, "pagination-next")
        button.click()
        # actions = ActionChains(driver)
        # actions.move_to_element(button).click() #key_down(Keys.CONTROL)
        # actions.perform()
        
    except Exception as e:
        print(f"Ошибка: {e}")
        break
print(goods)

print(f'Обработано {count} страниц')

# Сохраняем в файл
with open('dish.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['name', 'price', 'url'])
    writer.writerows(goods)
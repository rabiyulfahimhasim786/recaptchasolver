

#-------------------------------------------------------------------------------
# Imports

import csv
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.ui import Select

#-------------------------------------------------------------------------------
# Setup
Username = 0
Email = 1
URL = 2

with open('data.csv', 'r') as csv_file:

    csv_reader = csv.reader(csv_file)

#-------------------------------------------------------------------------------
# Web Automation

    for line in csv_reader:


        driver = webdriver.Chrome()
        driver.get('http://prdirectory.com.ar/submit.php')
        driver.maximize_window()
        #time.sleep(5)

        element=driver.find_elements(By.NAME, ('CATEGORY_ID'))
        print('ok')
        drp=Select(element[0])
        drp.select_by_visible_text("|   |___Web Development")
        time.sleep(4)

        goto = driver.find_elements(By.XPATH, '//*[@id="ok"]')
        goto[0].click()

        freelink = driver.find_element("xpath", '//*[@id="submitForm"]/table/tbody/tr/td/div/div[1]/table/tbody/tr[3]/td[1]/input')
        freelink.click()
        time.sleep(5)

        goto = driver.find_elements(By.XPATH, '//*[@id="submitForm"]/table/tbody/tr/td/div/div[1]/table/tbody/tr[4]/td/center/input')
        goto[0].click()

        Title_field = driver.find_element("xpath", '//*[@id="TITLE"]')
        Title_field.send_keys(line[3])
        time.sleep(3)


        Description_field = driver.find_element("xpath", '//*[@id="DESCRIPTION"]')
        Description_field.send_keys(line[4])
        time.sleep(3)

        Ownername_field = driver.find_element("xpath", '//*[@id="OWNER_NAME"]')
        Ownername_field.send_keys(line[0])
        time.sleep(3)

        Email_field = driver.find_element("xpath", '//*[@id="OWNER_EMAIL"]')
        Email_field.send_keys(line[1])
        time.sleep(3)



        agree = driver.find_elements(By.NAME, 'AGREERULES')
        agree[0].click()
        time.sleep(10)

        submit = driver.find_elements(By.XPATH, '//*[@id="submitForm"]/table/tbody/tr[12]/td/input')
        submit[0].click()



#-------------------------------------------------------------------------------

    
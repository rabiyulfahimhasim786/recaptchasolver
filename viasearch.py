

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
        driver.get('https://viesearch.com/submit')
        driver.maximize_window()
        #time.sleep(5)



        OWNER_NAME = driver.find_element("xpath", '/html/body/center/div/div[2]/div/div[4]/form/div[1]/div[2]/input')
        OWNER_NAME.send_keys(line[0])
        time.sleep(3)

        Email_field = driver.find_element("xpath", '/html/body/center/div/div[2]/div/div[4]/form/div[2]/div[2]/input')
        Email_field.send_keys(line[1])
        time.sleep(3)

        Website_Title = driver.find_element("xpath", '/html/body/center/div/div[2]/div/div[4]/form/div[3]/div[2]/input')
        Website_Title.send_keys(line[3])
        time.sleep(3)


        Website_Description = driver.find_element("xpath", '//*[@id="DESCRIPTION"]')
        Website_Description.send_keys(line[4])
        time.sleep(3)

        Website_Url = driver.find_element("xpath", '/html/body/center/div/div[2]/div/div[4]/form/div[5]/div[2]/input')
        Website_Url.send_keys(line[2])
        time.sleep(3)

        Website_Category=driver.find_elements(By.NAME, ('CATEGORY_ID'))
        print('ok')
        drp=Select(Website_Category[0])
        drp.select_by_visible_text("- - Directors")
        time.sleep(4)

        freelink = driver.find_element("xpath", '/html/body/center/div/div[2]/div/div[4]/form/div[7]/div[2]/div[7]/input')
        freelink.click()
        time.sleep(5)

        submit = driver.find_elements(By.XPATH, '/html/body/center/div/div[2]/div/div[4]/form/div[10]/div[2]/button')
        submit[0].click()



#-------------------------------------------------------------------------------
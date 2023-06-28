

#-------------------------------------------------------------------------------
# Imports

import csv
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.ui import Select
import os
import sys
import urllib
import pydub
import speech_recognition as sr
import re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import random
import time
from datetime import datetime
import requests
import json
import stem.process
from stem import Signal
from stem.control import Controller

# custom patch libraries
# from patch import download_latest_chromedriver, webdriver_folder_name


def delay(waiting_time=5):
    driver.implicitly_wait(waiting_time)

def create_tor_proxy(socks_port,control_port):
    TOR_PATH = os.path.normpath(os.getcwd()+"\\tor\\tor.exe")
    try:
        tor_process = stem.process.launch_tor_with_config(
          config = {
            'SocksPort': str(socks_port),
            'ControlPort' : str(control_port),
            'MaxCircuitDirtiness' : '300',
          },
          init_msg_handler = lambda line: print(line) if re.search('Bootstrapped', line) else False,
          tor_cmd = TOR_PATH
        )
        print("[INFO] Tor connection created.")
    except:
        tor_process = None
        print("[INFO] Using existing tor connection.")
    
    return tor_process

def renew_ip(control_port):
    print("[INFO] Renewing TOR ip address.")
    with Controller.from_port(port=control_port) as controller:
        controller.authenticate()
        controller.signal(Signal.NEWNYM)
        controller.close()
    print("[INFO] IP address has been renewed! Better luck next try~")  
    
if __name__ == "__main__":
    SOCKS_PORT = 41293
    CONTROL_PORT = 41294
    USER_AGENT_LIST = ['Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15',
                    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0',
                    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
                    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0',
                    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
                    ]
    activate_tor = False
    tor_process = None
    user_agent = random.choice(USER_AGENT_LIST)
    if activate_tor:
        print('[INFO] TOR has been activated. Using this option will change your IP address every 60 secs.')
        print('[INFO] Depending on your luck you might still see: Your Computer or Network May Be Sending Automated Queries.')
        tor_process = create_tor_proxy(SOCKS_PORT,CONTROL_PORT)
        PROXIES = {
            "http": f"socks5://127.0.0.1:{SOCKS_PORT}",
            "https": f"socks5://127.0.0.1:{SOCKS_PORT}"
        }
        response = requests.get("http://ip-api.com/json/", proxies=PROXIES)
    else:
        response = requests.get("http://ip-api.com/json/")
    result = json.loads(response.content)
    print('[INFO] IP Address [%s]: %s %s'%(datetime.now().strftime("%d-%m-%Y %H:%M:%S"), result["query"], result["country"]))
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
        driver.get('https://www.angelsdirectory.com/submit.php')
        driver.maximize_window()
        #time.sleep(5)

        username_field = driver.find_element("xpath", '/html/body/div[3]/div/div[1]/div/form/table/tbody/tr[4]/td[2]/input')
        username_field.send_keys(line[0])
        time.sleep(3)

        Email_field = driver.find_element("xpath", '/html/body/div[3]/div/div[1]/div/form/table/tbody/tr[5]/td[2]/input')
        Email_field.send_keys(line[1])
        time.sleep(3)

        URL_field = driver.find_element("xpath", '/html/body/div[3]/div/div[1]/div/form/table/tbody/tr[2]/td[2]/input')
        URL_field.send_keys(line[2])
        time.sleep(3)

        Title_field = driver.find_element("xpath", '/html/body/div[3]/div/div[1]/div/form/table/tbody/tr[1]/td[2]/input')
        Title_field.send_keys(line[3])
        time.sleep(3)

        Description_field = driver.find_element("xpath", '/html/body/div[3]/div/div[1]/div/form/table/tbody/tr[3]/td[2]/textarea')
        Description_field.send_keys(line[4])
        time.sleep(3)

        # Category_field = driver.find_element("xpath", '//*[@id="container"]/table/tbody/tr/td/form/table[2]/tbody/tr/td/table/tbody/tr[6]/td[2]/select')
        # Category_field.send_keys(line[7])
        

        element=driver.find_elements(By.NAME, ('CATEGORY_ID'))
        print('ok')
        drp=Select(element[0])
        drp.select_by_visible_text("|   |   |___Internet and Web Skills")
        time.sleep(4)

            
    # main program
    # auto locate recaptcha frames
        try:
            delay()
            frames = driver.find_elements_by_tag_name("iframe")
            recaptcha_control_frame = None
            recaptcha_challenge_frame = None
            for index, frame in enumerate(frames):
                if re.search('reCAPTCHA', frame.get_attribute("title")):
                    recaptcha_control_frame = frame
                    
                if re.search('recaptcha challenge', frame.get_attribute("title")):
                    recaptcha_challenge_frame = frame
            if not (recaptcha_control_frame and recaptcha_challenge_frame):
                print("[ERR] Unable to find recaptcha. Abort solver.")
                sys.exit()
            # switch to recaptcha frame
            delay()
            frames = driver.find_elements_by_tag_name("iframe")
            driver.switch_to.frame(recaptcha_control_frame)
            # click on checkbox to activate recaptcha
            driver.find_element_by_class_name("recaptcha-checkbox-border").click()
        
            # switch to recaptcha audio control frame
            delay()
            driver.switch_to.default_content()
            frames = driver.find_elements_by_tag_name("iframe")
            driver.switch_to.frame(recaptcha_challenge_frame)
        
            # click on audio challenge
            time.sleep(10)
            driver.find_element_by_id("recaptcha-audio-button").click()
        
            # switch to recaptcha audio challenge frame
            driver.switch_to.default_content()
            frames = driver.find_elements_by_tag_name("iframe")
            driver.switch_to.frame(recaptcha_challenge_frame)
        
            # get the mp3 audio file
            delay()
            src = driver.find_element_by_id("audio-source").get_attribute("src")
            print(f"[INFO] Audio src: {src}")
        
            path_to_mp3 = os.path.normpath(os.path.join(os.getcwd(), "sample.mp3"))
            path_to_wav = os.path.normpath(os.path.join(os.getcwd(), "sample.wav"))
        
            # download the mp3 audio file from the source
            urllib.request.urlretrieve(src, path_to_mp3)
        except:
            # if ip is blocked.. renew tor ip
            print("[INFO] IP address has been blocked for recaptcha.")
            if activate_tor:
                renew_ip(CONTROL_PORT)
            sys.exit()    

        # load downloaded mp3 audio file as .wav
        try:
            sound = pydub.AudioSegment.from_mp3(path_to_mp3)
            sound.export(path_to_wav, format="wav")
            sample_audio = sr.AudioFile(path_to_wav)
        except Exception:
            sys.exit(
                "[ERR] Please run program as administrator or download ffmpeg manually, "
                "https://blog.gregzaal.com/how-to-install-ffmpeg-on-windows/"
            )

        # translate audio to text with google voice recognition
        delay()
        r = sr.Recognizer()
        with sample_audio as source:
            audio = r.record(source)
        key = r.recognize_google(audio)
        print(f"[INFO] Recaptcha Passcode: {key}")

        # key in results and submit
        delay()
        driver.find_element_by_id("audio-response").send_keys(key.lower())
        driver.find_element_by_id("audio-response").send_keys(Keys.ENTER)
        time.sleep(5)
        driver.switch_to.default_content()
        time.sleep(5)
        #driver.find_element_by_id("recaptcha-demo-submit").click()
        if (tor_process):
            tor_process.kill()

        agree = driver.find_elements(By.NAME, 'agree')
        agree[0].click()
        time.sleep(10)

        submit = driver.find_elements(By.XPATH, '/html/body/div[3]/div/div[1]/div/form/table/tbody/tr[8]/td/input[2]')
        submit[0].click()



#-------------------------------------------------------------------------------

    
from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import os
from random import randint

class BrowserInteractions:
    def __init__(self, url,browser,driver_path, wait="0", scrolldownfor=10):
        self.wait = wait
        self.scrolldownfor = scrolldownfor
        if browser=="firefox":
            self.driver = webdriver.Firefox(executable_path=driver_path)
        elif browser=="chrome":
            self.driver = webdriver.Chrome(executable_path=driver_path)
        elif browser=="safari":
            self.driver = webdriver.Safari(executable_path=driver_path)
        elif browser == "ie":
            self.driver = webdriver.Ie(executable_path=driver_path)
        elif browser=="edge":
            self.driver = webdriver.Edge(executable_path=driver_path)
        elif browser=="opera":
            self.driver = webdriver.Opera(executable_path=driver_path)
        self.driver.implicitly_wait(wait)
        self.driver.get(url)

    def set_url(self, url):
        print(url)
        self.driver.implicitly_wait(self.wait)
        self.driver.get(url)        
        if int(self.scrolldownfor) > 0:
            SCROLL_PAUSE_TIME = 0.05
            # Get scroll height
            last_height = 400
            try:
                last_height = self.driver.execute_script("return document.body.scrollHeight")
            except:
                print("Height error - 400")
            
            x=0
            while x < self.scrolldownfor:
                son = self.driver.execute_script("return document.body.scrollHeight")
                self.driver.execute_script("window.scrollBy(0, 100);")
                time.sleep(SCROLL_PAUSE_TIME)
                self.driver.execute_script("window.scrollBy(0, 100);")
                time.sleep(SCROLL_PAUSE_TIME/2)
                self.driver.execute_script("window.scrollBy(0, 100);")
                time.sleep(SCROLL_PAUSE_TIME)
                self.driver.execute_script("window.scrollBy(0, 100);")
                time.sleep(SCROLL_PAUSE_TIME/2)
                self.driver.execute_script("window.scrollBy(0, 100);")
                time.sleep(SCROLL_PAUSE_TIME)
                self.driver.execute_script("window.scrollBy(0, 100);")
                time.sleep(SCROLL_PAUSE_TIME/2)
                self.driver.execute_script("window.scrollBy(0, 100);")
                time.sleep(SCROLL_PAUSE_TIME)

                # if son >= 2000: son = 2000  #haber siteleri için

                for i in range(0, son, 20):
                    self.driver.execute_script("window.scrollBy(0, 20);")
                    if i % 400 == 0:
                        time.sleep(SCROLL_PAUSE_TIME)
                    elif i % 200 == 0:
                        time.sleep(SCROLL_PAUSE_TIME / 2)

                
                # Wait to load page
                # time.sleep(SCROLL_PAUSE_TIME)

                new_height = self.driver.execute_script("return document.body.scrollHeight")
                if new_height == last_height: 
                    break
                last_height = new_height
                x=x+1


    def return_html(self):
        time.sleep(2)
        html = self.driver.execute_script("return document.documentElement.outerHTML;")
        return html
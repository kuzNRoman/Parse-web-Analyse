import time
import random

from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
import re
import pandas as pd
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import numpy as np

class finvizParser():

    def __init__(self):
        options = Options()
        options.add_argument("--no-sandbox")
        #options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-extensions")
        ua = UserAgent()
        uAgent = ua.random
        options.add_argument(f'user-agent={uAgent}')
        window_size = '2500,2500'
        options.add_argument(f'--window-size={window_size}')
        s = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=s, options=options) 

    def driver_close(self):
        self.driver.close()
        self.driver.quit()

    def existable_path(self, link):
        driver = self.driver
        try: 
            driver.find_element_by_xpath(link)
            existable = True
        except Exception:
            existable = False
        return existable

    def getDataFinviz(self):
        driver = self.driver
        driver.get('https://finviz.com/crypto.ashx')
        time.sleep(2)

        if self.existable_path('/html/body/div[8]/div/div[1]'):
            try:
                driver.find_element_by_xpath('/html/body/div[8]/div/div[1]').click()
            except:pass
        time.sleep(2)
        if self.existable_path('/html/body/div[8]/div[2]/div[2]'):
            try:
                driver.find_element_by_xpath('/html/body/div[8]/div[2]/div[2]').click()
            except:pass
        time.sleep(2)
        if self.existable_path('/html/body/div[2]/div/div[1]/div/div[2]'):
            try:
                with open(f"fig/fig_finviz.jpg", 'wb') as file:
                    file.write(driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div/div[2]').screenshot_as_png)
            except:pass

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

class investingParser():

    def __init__(self):
        options = Options()
        options.add_argument("--no-sandbox")
        #options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-extensions")
        ua = UserAgent()
        uAgent = ua.random
        options.add_argument(f'user-agent={uAgent}')
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

    def getDataInvesting(self, url_data):
        driver = self.driver
        driver.get(url_data)
        time.sleep(2)

        if self.existable_path('/html/body/div[5]/section/div[9]/table[1]'):
            tab_tab = driver.find_element_by_xpath('/html/body/div[5]/section/div[9]/table[1]').get_attribute('outerHTML')
            soup = BeautifulSoup(tab_tab, 'html.parser')
            df = pd.read_html(str(soup))[0]
            df = df.rename(columns={'Дата': 'Date', 'Цена': 'Price','Откр.':'Open', 'Макс.':'Max', 'Мин.':'Min', 'Объём':'Size', 'Изм. %':'Change'})
            df['Price'] = df['Price'].str.replace('.','',regex=True)
            df['Price'] = df['Price'].str.replace(',','.',regex=True)
            df['Price'] = pd.to_numeric(df['Price'])
            df['Open'] = df['Open'].str.replace('.','',regex=True)
            df['Open'] = df['Open'].str.replace(',','.',regex=True)
            df['Open'] = pd.to_numeric(df['Open'])
            df['Max'] = df['Max'].str.replace('.','',regex=True)
            df['Max'] = df['Max'].str.replace(',','.',regex=True)
            df['Max'] = pd.to_numeric(df['Max'])
            df['Min'] = df['Min'].str.replace('.','',regex=True)
            df['Min'] = df['Min'].str.replace(',','.',regex=True)
            df['Min'] = pd.to_numeric(df['Min'])
            df['Size'] = df['Size'].str.replace(',','',regex=True)
            df['Size'] = df['Size'].str.replace('K','0',regex=True)
            df['Size'] = df['Size'].str.replace('M','0000',regex=True)
            df['Size'] = pd.to_numeric(df['Size'])

            return df
        else:
            return None
            

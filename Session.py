import time
from selenium.webdriver.common.keys import Keys
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from enum import Enum

class TransType(Enum):
    BUY_YES = 0
    BUY_NO = 1
    SELL_YES = 2
    SELL_NO = 3

class Session(object):

    def __init__(self):
        self.loggedIn = False
        self.driver = webdriver.Firefox()

    def logon(self):
        self.driver.get('https://www.predictit.org/Profile/MyShares')
        self.driver.find_element_by_link_text('Sign In').click()
        self.driver.implicitly_wait(1)
        self.driver.find_element_by_id('Email').send_keys('skoltrading@gmail.com')
        pwElem = self.driver.find_element_by_id('Password')
        pwElem.send_keys('')
        pwElem.submit()
        self.loggedIn = True

    def logout(self):
        self.driver.get('https://www.predictit.org/Profile/MyShares')
        self.loggedIn = False

    def executeSingleTrade(self, transType, contractId, amount=1, marketId=-1):
        # go to correct web page
        self.driver.get('https://www.predictit.org/Home/SingleOption?contractId=' + str(contractId))
        # click buy/sell button
        buttonName = ''
        previewName = ''
        if transType == TransType.BUY_YES:
            buttonName = 'simpleYes'
            previewName = 'submitBuy'
        elif transType == TransType.BUY_NO:
            buttonName = 'simpleNo'
            previewName = 'submitBuy'
        elif transType == TransType.SELL_YES:
            buttonName = 'simpleNo'
            previewName = 'submitSell'
        elif transType == TransType.SELL_NO:
            buttonName = 'simpleYes'
            previewName = 'submitSell'
        print(buttonName)
        self.driver.find_element_by_id(buttonName).click()
        self.driver.implicitly_wait(1)
        # fill in quantity
        if (amount != 1):
            self.driver.find_element_by_id('Quantity').send_keys(str(amount))
        # execute trade
        self.driver.find_element_by_id(previewName).click() # preview
        # self.driver.implicitly_wait(1)
        self.driver.find_element(By.XPATH, '//button[text()="Submit Offer"]').click()  # WHEN TESTING EXECUTION COMMENT OUT THIS LINE SO YOU DON'T ACCIDENTALLY COMPLETE THE TRADE
        # self.driver.implicitly_wait(1)

    def begin(self):
    # Mikey: double check that the contractId (869) still exists before testing this
        try:
            self.logon()
            time.sleep(5)
            self.executeSingleTrade(TransType.BUY_NO, 558)
        except TimeoutException:
            print('Timeout Error')
        except NoSuchElementException:
            print('NoSuchElement Error')

def main():
    session = Session()
    session.begin()

if __name__ == "__main__":
    main()

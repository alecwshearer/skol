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

class ExecutionReport(object):

    def __init__(self):
        # self.symbol = 'empty'
        # self.marketType = 'empty'
        # self.startDate = 'empty'
        # self.endDate = 'empty'
        # self.sharesTraded = 'empty'
        # self.todaysVolume = 'empty'
        # self.totalShares = 'empty'
        self.tradedShares = 'empty'
        self.tradedPrice = 'empty'
        self.pnl = 'empty'
        self.riskAdjustment = 'empty'
        self.credit = 'empty'
        self.question = 'empty'

class Session(object):

    def __init__(self):
        self.loggedIn = False
        self.driver = webdriver.Firefox()

    def logon(self):
        self.driver.get('https://www.predictit.org/Profile/MyShares')
        self.driver.find_element_by_link_text('Sign In').click()
        time.sleep(1)
        self.driver.find_element_by_id('Email').send_keys('skoltrading@gmail.com')
        time.sleep(1)
        pwElem = self.driver.find_element_by_id('Password')
        time.sleep(1)
        pwElem.send_keys('')
        time.sleep(1)
        pwElem.submit()
        time.sleep(1)
        self.loggedIn = True

    def logout(self):
        self.driver.get('https://www.predictit.org/Profile/MyShares')
        self.loggedIn = False

    def executeSingleTrade(self, transType, contractId, amount=1, marketId='empty'):
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
            buttonName = 'sellYes-' + str(contractId)
            previewName = 'submitSell'
        elif transType == TransType.SELL_NO:
            buttonName = 'sellNo-' + str(contractId)
            previewName = 'submitSell'

        time.sleep(1)
        self.driver.find_element_by_id(buttonName).click()

        # fill in quantity
        if (amount != 1):
            self.driver.find_element_by_id('Quantity').send_keys(str(amount))
            time.sleep(1)

        # execute trade
        time.sleep(1)
        self.driver.find_element_by_id(previewName).click()

        time.sleep(1)
        self.driver.find_element(By.XPATH, '//button[text()="Submit Offer"]').click()  # WHEN TESTING EXECUTION COMMENT OUT THIS LINE SO YOU DON'T ACCIDENTALLY COMPLETE THE TRADE

        time.sleep(1)
        return self.buildExecutionReport(transType, contractId, marketId)

    def buildExecutionReport(self, transType, contractId, marketId):
        report = ExecutionReport()
        report.transType = transType
        report.contractId = contractId
        report.marketId = marketId
        tds = self.driver.find_elements(By.TAG_NAME, "td")

        # don' think we need this info, but these are their indices if we do.
        # report.symbol = tds[7]
        # report.marketType = tds[9]
        # report.startDate = tds[11]
        # report.endDate = tds[13]
        # report.sharesTraded = tds[15]
        # report.todaysVolume = tds[17]
        # report.totalShares = tds[19]
        report.tradedShares = tds[132]
        report.tradedPrice = tds[133]
        report.pnl = tds[135]
        report.riskAdjustment = tds[137]
        report.credit = tds[139]
        report.question = self.driver.find_element_by_class_name('confirm-question').text
        return report

    def begin(self):
        self.logon()

def main():
    session = Session()
    try:
        session.begin()
        report = session.executeSingleTrade(TransType.SELL_YES, 558)
        print report.__dict__  # print execution report
    except Exception,e: print str(e)

if __name__ == "__main__":
    main()

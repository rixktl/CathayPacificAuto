#!/usr/bin/env python3

from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
import time

class BrowserDriver:
    def __init__(self, headless = True):
        # Locate browser binary
        binary = FirefoxBinary('/Applications/Firefox.app/Contents/MacOS/firefox-bin')

        # Enable headless mode
        options = webdriver.FirefoxOptions()
        if (headless):
            options.add_argument('--headless')

        # Init driver
        self.__driver = webdriver.Firefox(firefox_binary=binary, options=options)

    def __del__(self):
        self.__driver.quit()

    def getDriver(self):
        return self.__driver


class CathayPacificBrowserDriver(BrowserDriver):
    months = dict(January=1, Febuary=2, March=3, April=4, May=5, June=6, \
    July=7, August=8, September=9, October=10, November=11, December=12)

    def __init__(self, headless = True):
        super().__init__(headless)
        self.__driver = super().getDriver()
        self.__URL = 'https://www.cathaypacific.com/cx/en_US.html'

    def __del__(self):
        super().__del__()

    @property
    def depart(self):
        return self.__depart

    @property
    def departDate(self):
        return self.__departDate

    @property
    def dest(self):
        return self.__dest

    @depart.setter
    def depart(self, val):
        self.__depart = val

    # Assume to be in form of {"month": "04", "day": "08"}
    @departDate.setter
    def departDate(self, val):
        self.__departDate = val

    @dest.setter
    def dest(self, val):
        self.__dest = val

    def fillLocations(self):
        departLabel = self.__driver.find_element_by_id('depart-label')
        departLabel.clear()
        departLabel.send_keys(self.__depart)

        destLabel = self.__driver.find_element_by_id('destination-label')
        destLabel.click()
        destLabel.send_keys(self.__dest)

    def selectDepartDates(self):
        # Start the datepicker
        departIdent = "//span[contains(text(), 'Departing on')]/following-sibling::button"
        departBtnList = self.__driver.find_elements_by_xpath(departIdent)
        departBtnList[1].click() # First button is fake, only the second one is real

        # Select month
        monthIdent = "//span[@class='ui-datepicker-month']"
        monthList = self.__driver.find_elements_by_xpath(monthIdent)
        currentMonth = CathayPacificBrowserDriver.months[(monthList[2].text)]
        diff = int(self.__departDate['month']) - currentMonth # Only second text is visible
        if (diff < 0): raise Exception('Month of departer has passed. You can\'t go back in time')

        # Jump to correct month
        if (diff > 1):
            for i in range(0, diff):
                nextBtnIdent = "//a[@data-handler='next']"
                nextBtnList = self.__driver.find_elements_by_xpath(nextBtnIdent)
                nextBtnList[1].click() # First button is fake, only the second one is real

        # Select day
        monthCalendarIdent = "//div[@class='ui-datepicker-group ui-datepicker-group-first']"
        monthCalendarList = self.__driver.find_elements_by_xpath(nextBtnIdent)
        dayIdent = "//td[.//a[contains(text(), '" + str(self.__departDate['day']) + "')]]"
        dayList = monthCalendarList[1].find_elements_by_xpath(dayIdent) # Second one is valid
        dayList[2].click() # Third one is valid

    def request(self):
        self.__driver.get(self.__URL)
        self.fillLocations()
        self.selectDepartDates()
        input('waiting for you to press any key...')


def main():
    CPBDriver = CathayPacificBrowserDriver(headless = False)
    CPBDriver.depart = 'San Diego, (SAN)'
    CPBDriver.departDate = {'month': '12', 'day': '11'}
    CPBDriver.dest = 'Hong Kong, (HKG)'
    CPBDriver.request()


if __name__ == '__main__':
    main()

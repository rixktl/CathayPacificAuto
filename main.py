#!/usr/bin/env python3

from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

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
    def dest(self):
        return self.__dest

    @depart.setter
    def depart(self, val):
        self.__depart = val

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

    def selectDates(self):
        # TODO: WIP
        # divs = self.__driver.find_elements_by_xpath("//div[@class='button-date-picker-wrapper field-group cx-inputfield']")
        departIdent = "//span[contains(text(), 'Departing on')]/following-sibling::button"
        departBtnList = self.__driver.find_elements_by_xpath(departIdent)
        departBtnList[1].click() # First button is fake, only the second one is real
        input('waiting for you to press any key...')

    def request(self):
        self.__driver.get(self.__URL)
        self.fillLocations()
        self.selectDates()


def main():
    CPBDriver = CathayPacificBrowserDriver(headless = False)
    CPBDriver.depart = 'San Diego, (SAN)'
    CPBDriver.dest = 'Hong Kong, (HKG)'
    CPBDriver.request()


if __name__ == '__main__':
    main()

import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import csv
import urllib
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time

mobile_emulation = {
    "userAgent": "Mozilla/5.0 (Linux; Android 4.2.1; en-us; Nexus 5 Build/JOP40D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Mobile Safari/535.19" }
option = Options()

# option.add_argument('--headless')

option.add_argument('--no-sandbox')
option.add_argument("--incognito")
option.add_argument("--disable-extensions")

# Pass the argument 1 to allow and 2 to block
option.add_experimental_option("prefs", { 
    "profile.default_content_setting_values.notifications": 1
})



# START_URL = "https://www.justdial.com/Delhi/Gift-Shops/nct-10231352/page-1"

START_URL = 'https://www.justdial.com/Delhi/Car-Repair-Services-in-Noida' #input('Past Your Link here and press ENTER? \n')

count = (int(input('Please Enter how much data do you want to scrape? Example: 10, 20, 30, 40.....more \n')))

class CatalogsScrapper:
    def __init__(self, browser, filename):

        if not isinstance(browser, webdriver.Chrome):
            raise TypeError("browser must be a instance of webdriver.Chrome")

        if os.path.exists(filename):
            os.remove(filename)
        self.filename = filename
        self.browser = browser

    # scrapping data from link one by one
    def scrappDataFromLink(self):
        
        if os.path.exists(self.filename):
            Data = []
            f = open("links.txt", "r")
            self.browser.get('ttps://www.justdial.com/')
            for x in f:
                chrome_options = Options()
                
                chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)

                chrome_options.add_argument("--headless")

                driver = webdriver.Chrome(chrome_options = chrome_options)
                print ('opening Link....')
                driver.get(x)



                First = driver.find_element_by_xpath('//*[@id="common_font_size"]/tbody/tr[2]')
                first = First.text
                Company = driver.find_element_by_xpath('//*[@id="common_font_size"]/tbody/tr[3]')
                company = Company.text
                Position = driver.find_element_by_xpath('//*[@id="common_font_size"]/tbody/tr[4]')
                position = Position.text
                Country = driver.find_element_by_xpath('//*[@id="common_font_size"]/tbody/tr[9]')
                country = Country.text


                Obj = {
                    "first": first,
                    "company": company,
                    "position": position,
                    "country": country
                }
                print (Obj)
                Data.append(Obj)
                driver.close()

            print (Data)
            

    def getArrayLinksAndScrapData(self):
        if os.path.exists(self.filename):
            num_lines = sum(1 for line in open('links.txt'))
            if num_lines >= count:
                print('links almost done now it getting data from link')
                self.scrappDataFromLink()


    def storeLink(self, Links):
        # open file with mode a
        f = open(self.filename, "a")
        # Looping on each catalog links on per page
        for Link in Links:
            f.write(Link + 'a')
        f.close()
        self.getArrayLinksAndScrapData()

    def getNextPageLink(self):
        next_button = self.browser.find_element_by_partial_link_text('Next')
        next_page_link = next_button.get_attribute('href')
        return next_page_link

    def scrape_justdial_Link(self):
        links = []
        elems = self.browser.find_elements_by_xpath('//*[@id="dg_Main"]/tbody/tr[2]/td[1]')

        for elem in elems:
            print (elem.get_attribute('href'))
            links.append(elem.get_attribute('href'))
        return links

    def getLinksData(self, pageUrl):
        print('Page Loading....')

        self.browser.get(pageUrl)

        links = self.scrape_justdial_Link()
        self.storeLink(links)
        # trying to get next page links
        try:
            next_page_link = self.getNextPageLink()
            print ('Starting crwaling from next page..')
            self.getLinksData(next_page_link)
        except NoSuchElementException as error:
            print('Crowling Done..')

        

def main():
    browser = webdriver.Chrome(chrome_options=option)
    catalogs_scrapper = CatalogsScrapper(browser, 'links.txt')
    catalogs_scrapper.getLinksData(START_URL)


if __name__ == "__main__":
    main()

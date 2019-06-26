#!/usr/bin/env python3
from MongoShopee import MongoDB
from OmniCrawler import Selenium
from datetime import datetime
from DataStructure.StringManipulator import Concatenate, Enumerate, Manipulate
import traceback
import time
import os
import datetime

class Run:
    Merchant_html_path = ''
    Merchant_name = ""
    Merchant_rate = ""
    Merchant_product = 0
    Merchant_established = ""
    Merchant_followers = 0
    Merchant_location = ''
    product_page = 0
    max_product_page = 100
    number_item = 0
    Date_Crawling = 0
    word_separator = "%2520"
    link = ""
    Selenium = Selenium()
    page_ordinal = 100
    def Crawling(self,Link_Merchant,Code_City):
        MongoDB().updateRunning(Link_Merchant)
        MongoDB().updateStatusCityRun(Link_Merchant,Code_City)
        while self.product_page == 0 or (self.product_page < self.page_ordinal and self.product_page < self.max_product_page):
            self.product_page = MongoDB().lastPage(Link_Merchant)
            self.Selenium.link = Link_Merchant+"?locations="+Code_City.replace(" ",self.word_separator)+"&page="+str(self.product_page)+"&sortBy=sales"
            self.Selenium.Load(self.Selenium.link)
            time.sleep(4)
            self.page_ordinal = int(self.Selenium.ExtractElementText("//*[@id='main']/div/div[2]/div[2]/div/div/div[@class='container _1EofO_']/div[2]/div/div/div[1]/div[2]/div/span[2]"))-1
            self.product_page+=1
            print("jumlah page ;" + str(self.page_ordinal))
            item_count = 0
            print('item :'+str(item_count))
            item_ordinal = self.Selenium.ExtractElements("//*[@id='main']/div/div[2]/div[2]/div/div/div[@class='container _1EofO_']/div[2]/div/div/div[2]/div")
            print("jumlah item : "+ str(len(item_ordinal)))
            while item_count < len(item_ordinal):
                item_count +=1
                checkstarseller = self.Selenium.ExtractElementText("[@id='main']/div/div[2]/div[2]/div/div/div[@class='container _1EofO_']/div[2]/div/div/div[2]/div["+str(item_count)+"]/div/a/div/div[1]/div[2]/div/span")
                print(checkstarseller)                                         
                if checkstarseller == "Star Seller" :
                    if item_count <11:
                        product_link = self.Selenium.ExtractElementAttribute('href',''.join(["//*[@id='main']/div/div[2]/div[2]/div/div/div[@class='container _1EofO_']/div[2]/div/div/div[2]/div["+str(item_count)+"]/div/a"]))
                        self.Merchant_location = self.Selenium.ExtractElementText("//*[@id='main']/div/div[2]/div[2]/div/div/div[@class='container _1EofO_']/div[2]/div/div/div[2]/div["+str(item_count)+"]/div/a/div/div[2]/div[5]")
                    elif item_count<21:
                        self.Selenium.scrollDown(3)
                        product_link = self.Selenium.ExtractElementAttribute('href',''.join(["//*[@id='main']/div/div[2]/div[2]/div/div/div[@class='container _1EofO_']/div[2]/div/div/div[2]/div["+str(item_count)+"]/div/a"]))
                        self.Merchant_location = self.Selenium.ExtractElementText("//*[@id='main']/div/div[2]/div[2]/div/div/div[@class='container _1EofO_']/div[2]/div/div/div[2]/div["+str(item_count)+"]/div/a/div/div[2]/div[5]")
                    elif item_count<31:
                        self.Selenium.scrollDown(4)
                        product_link = self.Selenium.ExtractElementAttribute('href',''.join(["//*[@id='main']/div/div[2]/div[2]/div/div/div[@class='container _1EofO_']/div[2]/div/div/div[2]/div["+str(item_count)+"]/div/a"]))
                        self.Merchant_location = self.Selenium.ExtractElementText("//*[@id='main']/div/div[2]/div[2]/div/div/div[@class='container _1EofO_']/div[2]/div/div/div[2]/div["+str(item_count)+"]/div/a/div/div[2]/div[5]")
                    elif item_count<41:
                        self.Selenium.scrollDown(5)
                        product_link = self.Selenium.ExtractElementAttribute('href',''.join(["//*[@id='main']/div/div[2]/div[2]/div/div/div[@class='container _1EofO_']/div[2]/div/div/div[2]/div["+str(item_count)+"]/div/a"]))
                        self.Merchant_location = self.Selenium.ExtractElementText("//*[@id='main']/div/div[2]/div[2]/div/div/div[@class='container _1EofO_']/div[2]/div/div/div[2]/div["+str(item_count)+"]/div/a/div/div[2]/div[5]")
                    elif item_count<51:
                        self.Selenium.scrollDown(6)
                        product_link = self.Selenium.ExtractElementAttribute('href',''.join(["//*[@id='main']/div/div[2]/div[2]/div/div/div[@class='container _1EofO_']/div[2]/div/div/div[2]/div["+str(item_count)+"]/div/a"]))
                        self.Merchant_location = self.Selenium.ExtractElementText("//*[@id='main']/div/div[2]/div[2]/div/div/div[@class='container _1EofO_']/div[2]/div/div/div[2]/div["+str(item_count)+"]/div/a/div/div[2]/div[5]")
                    else:
                        self.Selenium.scrollUp(3)
                    print('item :'+str(item_count))
                    if product_link is not None :
                        self.Selenium.Load(product_link)
                        time.sleep(3)
                        checkformat = len(self.Selenium.ExtractElements("//*[@id='main']/div/div[2]/div[2]/div[2]/div[3]/div"))
                        if checkformat == 3:
                            self.Merchant_html_path = self.Selenium.ExtractElementAttribute('href',"//*[@id='main']/div/div[2]/div[2]/div[2]/div[3]/div[2]/div[1]/div/div[3]/a")
                            checkformat = 0
                        elif checkformat == 2:
                            checkformat = 0
                            self.Merchant_html_path = self.Selenium.ExtractElementAttribute('href',"//*[@id='main']/div/div[2]/div[2]/div[2]/div[3]/div[1]/div[1]/div/div[3]/a")
                        else :
                            print(product_link)
                        if MongoDB().checkMerchant(self.Merchant_html_path) is None :
                            self.Selenium.Load(self.Merchant_html_path)
                            time.sleep(3)
                            self.Merchant_name = self.Selenium.ExtractElementText("//*[@id='main']/div/div[2]/div[2]/div[2]/div/div[1]/div/div[1]/div[3]/div[1]/div/h1")
                            self.Merchant_rate = self.Selenium.ExtractElementText("//*[@id='main']/div/div[2]/div[2]/div[2]/div/div[1]/div/div[2]/div[6]/div[2]/div[2]")
                            self.Merchant_product = self.Selenium.ExtractElementText("//*[@id='main']/div/div[2]/div[2]/div[2]/div/div[1]/div/div[2]/div[1]/div[2]/div[2]")
                            self.Merchant_established = self.Selenium.ExtractElementText("//*[@id='main']/div/div[2]/div[2]/div[2]/div/div[1]/div/div[2]/div[7]/div[2]/div[2]")
                            self.Merchant_followers =self.Selenium.ExtractElementText("//*[@id='main']/div/div[2]/div[2]/div[2]/div/div[1]/div/div[2]/div[5]/div[2]/div[2]")
                            self.Selenium.BackPage()

                            try:

                                MongoDB().insert_Shopee(self.Merchant_html_path, self.Merchant_name, self.Merchant_rate, self.Merchant_product, self.Merchant_established, self.Merchant_followers, self.Merchant_location)
                                self.Merchant_html_path = ''
                                self.Merchant_name = ""
                                self.Merchant_rate = ""
                                self.Merchant_product = 0
                                self.Merchant_established = ""
                                self.Merchant_followers = 0
                                self.Merchant_location = ''
                            except Exception as e:
                                print("skip")
                        self.Selenium.BackPage();time.sleep(2)
                else:
                    print('skipped')



            MongoDB().updatePages(Link_Merchant,self.product_page)
        self.product_page = 0
        self.number_item = 0
        self.Date_Crawling = 0
        self.max_product_page = 100
        MongoDB().updateStatusCityDone(Link_Merchant,Code_City)
        MongoDB().updatePages(Link_Merchant)
        #MongoDB().updateDoneStatus(Link_Merchant)
        self.Selenium.clear_cache()

    def main(self):
        Link_Merchant_count = MongoDB().countCategory()
        while Link_Merchant_count != 0:
            try:
                self.Crawling(MongoDB().getLinkToCrawling()[0],MongoDB().getLinkToCrawling()[1])
                self.product_page = 0
                self.number_item = 0
                self.Date_Crawling = 0
                self.max_product_page = 100
                print(MongoDB().getLinkToCrawling()[1])
                MongoDB().updateStatusCityDone(MongoDB().getLinkToCrawling()[0],MongoDB().getLinkToCrawling()[1])
                MongoDB().updatedStatusCategory(MongoDB().getLinkToCrawling()[0])
            except Exception as e:
                print(e)
                MongoDB().timeTrackError(e)
                self.Crawling(MongoDB().getLinkToCrawling()[0],MongoDB().getLinkToCrawling()[1])
            Link_Merchant_count = MongoDB().countCategory()
        MongoDB().updateMerchantTimeEnd()
try:
    Run().main()
except Exception as e:
    print(Run().product_page)
    MongoDB().timeTrackError(e)
    Run().main()

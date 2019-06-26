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
    idProduct = ""
    namaProduct = ""
    jumlahTerjual = ""
    hargaAsli = ""
    hargaDiskon = ""
    hargaRangeAtas = ""
    hargaRangeBawah = ""
    hargaDisRangeAtas = ""
    hargaDisRangeBawah = ""
    word_separator = "+"
    link = ""
    Selenium = Selenium()
    db = MongoDB()

    max_merchant = db.countMerchant()
    #print(max_merchant)#;input()
    page_ordinal = 100
    def Crawling(self):
        while self.max_merchant != 0:
            page_product = 0
            link = self.db.checkMerchantToCrawl()
            #print('link '+str(link));input()
            last = self.db.checkLastCrawling(link)
            #print(last)
            if last is not None:
                page_product = last
            if link is not None:
                self.db.updateStatus(link)
                self.Selenium.Load(link)
                time.sleep(4)
                max_page = int(self.Selenium.ExtractElementText("//*[@id='main']/div/div[2]/div[2]/div[2]/div/div[3]/div[@class='shop-page__all-products-section']/div[2]/div/div[1]/div[2]/div/span[2]"))

                while page_product < max_page:
                    self.db.writeLog(link, page_product)
                    page_product +=1
                    if page_product != 1:
                        self.Selenium.Load("".join([link,"?page=",str(page_product-1),"&sortBy=pop"]))
                        time.sleep(4)
                    item_count = 0
                    item_ordinal = len(self.Selenium.ExtractElements("//*[@id='main']/div/div[2]/div[2]/div[2]/div/div[3]/div[@class='shop-page__all-products-section']/div[2]/div/div[2]/div/div"))
                    #print(item_ordinal);input()
                    while item_count < item_ordinal:
                        if item_count < 30:
                            self.Selenium.scrollDown(5)
                        item_count +=1
                        try:
                            self.idProduct = self.Selenium.ExtractElementAttribute("href",''.join(["//*[@id='main']/div/div[2]/div[2]/div[2]/div/div[3]/div[@class='shop-page__all-products-section']/div[2]/div/div[2]/div/div[",str(item_count),"]/div/a"]))
                        except Exception as e:
                            self.Selenium.scrollDown(3)
                            try:
                                self.idProduct = self.Selenium.ExtractElementAttribute("href",''.join(["//*[@id='main']/div/div[2]/div[2]/div[2]/div/div[3]/div[@class='shop-page__all-products-section']/div[2]/div/div[2]/div/div[",str(item_count),"]/div/a"]))
                            except Exception as e:
                                self.Selenium.scrollUp(2)
                                self.idProduct = self.Selenium.ExtractElementAttribute("href",''.join(["//*[@id='main']/div/div[2]/div[2]/div[2]/div/div[3]/div[@class='shop-page__all-products-section']/div[2]/div/div[2]/div/div[",str(item_count),"]/div/a"]))
                        if self.idProduct is not None:
                            k = self.idProduct.split("-i")
                            l = k[0].split('id/')
                            self.namaProduct= l[1].replace('-',' ')
                            #print(self.namaProduct)
                            self.jumlahTerjual = self.Selenium.ExtractElementText(''.join(["//*[@id='main']/div/div[2]/div[2]/div[2]/div/div[3]/div[@class='shop-page__all-products-section']/div[2]/div/div[2]/div/div[",str(item_count),"]/div/a/div/div[2]/div[4]/div[3]"]))
                            check = self.Selenium.ExtractElements(''.join(["//*[@id='main']/div/div[2]/div[2]/div[2]/div/div[3]/div[@class='shop-page__all-products-section']/div[2]/div/div[2]/div/div[",str(item_count),"]/div/a/div/div[2]/div[2]/div"]))
                            if  len(check) == 2:
                                check2 = self.Selenium.ExtractElements(''.join(["//*[@id='main']/div/div[2]/div[2]/div[2]/div/div[3]/div[@class='shop-page__all-products-section']/div[2]/div/div[2]/div/div[",str(item_count),"]/div/a/div/div[2]/div[2]/div[1]/span"]))
                                if len(check2) == 2:
                                    self.hargaAsli = self.Selenium.ExtractElementText(''.join(["//*[@id='main']/div/div[2]/div[2]/div[2]/div/div[3]/div[@class='shop-page__all-products-section']/div[2]/div/div[2]/div/div[",str(item_count),"]/div/a/div/div[2]/div[2]/div[1]/span[2]"]))
                                    self.hargaDiskon = None
                                    self.hargaRangeAtas = None
                                    self.hargaRangeBawah = None
                                    self.hargaDisRangeAtas = None
                                    self.hargaDisRangeBawah = None
                                elif len(check2) == 4:
                                    self.Selenium.Load(self.idProduct)
                                    time.sleep(4)
                                    self.hargaAsli = None
                                    self.hargaDiskon = None
                                    check3 = self.Selenium.ExtractElements("//*[@id='main']/div/div[2]/div[2]/div[2]/div[2]/div[3]/div/div[3]/div/div/div/div")
                                    if len(check3) == 1:
                                        a = self.Selenium.ExtractElementText("//*[@id='main']/div/div[2]/div[2]/div[2]/div[2]/div[3]/div/div[3]/div/div/div/div/div/div").replace('Rp','').split(' - ')
                                        self.hargaRangeAtas = a[0].replace('.','')
                                        self.hargaRangeBawah = a[1].replace('.','')
                                        self.hargaDisRangeAtas = None
                                        self.hargaDisRangeBawah = None
                                    elif len(check3)==2:
                                        a = self.Selenium.ExtractElementText("//*[@id='main']/div/div[2]/div[2]/div[2]/div[2]/div[3]/div/div[3]/div/div/div/div/div[1]").replace('Rp','').split(' - ')
                                        b = self.Selenium.ExtractElementText("//*[@id='main']/div/div[2]/div[2]/div[2]/div[2]/div[3]/div/div[3]/div/div/div/div/div[2]/div[1]").replace('Rp','').split(' - ')
                                        self.hargaRangeAtas = a[0].replace('.','')
                                        self.hargaRangeBawah =  a[1].replace('.','')
                                        self.hargaDisRangeAtas =  b[0].replace('.','')
                                        self.hargaDisRangeBawah =  b[1].replace('.','')
                                    self.Selenium.BackPage()
                            elif len(check) == 3:

                                check2 = self.Selenium.ExtractElements(''.join(["//*[@id='main']/div/div[2]/div[2]/div[2]/div/div[3]/div[@class='shop-page__all-products-section']/div[2]/div/div[2]/div/div[",str(item_count),"]/div/a/div/div[2]/div[2]/div[1]/span"]))
                                if len(check2) == 2:
                                    self.hargaAsli = self.Selenium.ExtractElementText(''.join(["//*[@id='main']/div/div[2]/div[2]/div[2]/div/div[3]/div[@class='shop-page__all-products-section']/div[2]/div/div[2]/div/div[",str(item_count),"]/div/a/div/div[2]/div[2]/div[1]/span[2]"]))
                                    self.hargaDiskon = None
                                    self.hargaRangeAtas = None
                                    self.hargaRangeBawah = None
                                    self.hargaDisRangeAtas = None
                                    self.hargaDisRangeBawah = None
                                elif len(check2) == 4:
                                    self.Selenium.Load(self.idProduct)
                                    time.sleep(4)
                                    self.hargaAsli = None
                                    self.hargaDiskon = None
                                    check3 = self.Selenium.ExtractElements("//*[@id='main']/div/div[2]/div[2]/div[2]/div[2]/div[3]/div/div[3]/div/div/div/div")
                                    if len(check3) == 1:
                                        a = self.Selenium.ExtractElementText("//*[@id='main']/div/div[2]/div[2]/div[2]/div[2]/div[3]/div/div[3]/div/div/div/div/div/div").replace('Rp','').split(' - ')
                                        self.hargaRangeAtas = a[0].replace('.','')
                                        self.hargaRangeBawah = a[1].replace('.','')
                                        self.hargaDisRangeAtas = None
                                        self.hargaDisRangeBawah = None
                                    elif len(check3)==2:
                                        a = self.Selenium.ExtractElementText("//*[@id='main']/div/div[2]/div[2]/div[2]/div[2]/div[3]/div/div[3]/div/div/div/div/div[1]").replace('Rp','').split(' - ')
                                        b = self.Selenium.ExtractElementText("//*[@id='main']/div/div[2]/div[2]/div[2]/div[2]/div[3]/div/div[3]/div/div/div/div/div[2]/div[1]").replace('Rp','').split(' - ')
                                        self.hargaRangeAtas = a[0].replace('.','')
                                        self.hargaRangeBawah =  a[1].replace('.','')
                                        self.hargaDisRangeAtas =  b[0].replace('.','')
                                        self.hargaDisRangeBawah =  b[1].replace('.','')
                                    self.Selenium.BackPage()
                                #self.hargaAsli = self.Selenium.ExtractElementText(''.join(["//*[@id='main']/div/div[2]/div[2]/div[2]/div/div[3]/div[@class='shop-page__all-products-section']/div[2]/div/div[2]/div/div[",str(item_count),"]/div/a/div/div[2]/div[2]/div[1]"])).replace('Rp','').replace('-','').replace('.','')
                                #self.hargaDiskon = self.Selenium.ExtractElementText(''.join(["//*[@id='main']/div/div[2]/div[2]/div[2]/div/div[3]/div[@class='shop-page__all-products-section']/div[2]/div/div[2]/div/div[",str(item_count),"]/div/a/div/div[2]/div[2]/div[2]/span[2]"])).replace('.','')
                                #self.hargaRangeAtas = None
                                #self.hargaRangeBawah = None
                                #self.hargaDisRangeAtas = None
                                #self.hargaDisRangeBawah = None
                            #print(1)
                            if item_count != 1:
                                #print(2)
                                if self.db.checkProduct(link, self.idProduct) is None:
                                    #print(3)
                                    #print(self.db.checkProduct(link, self.idProduct))
                                    self.db.insertProduct(self.idProduct, link, self.namaProduct, self.jumlahTerjual, self.hargaAsli, self.hargaDiskon, self.hargaRangeAtas, self.hargaRangeBawah, self.hargaDisRangeAtas, self.hargaDisRangeBawah)
                            else:
                                #print(4)
                                self.db.insertProduct(self.idProduct, link, self.namaProduct, self.jumlahTerjual, self.hargaAsli, self.hargaDiskon, self.hargaRangeAtas, self.hargaRangeBawah, self.hargaDisRangeAtas, self.hargaDisRangeBawah)
                self.db.updateStatusEnd(link)
                self.max_merchant -=1
try:
    Run().Crawling()
except Exception as e:
    Run().Crawling()

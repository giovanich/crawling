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
    checkCategory = ""
    arraySubCategory = ["Perawatan Tubuh","Alat Kecantikan","Alat Rambut","Kecantikan Lainnya","Kosmetik Mata","Perawatan Kuku","Perawatan Pria","Kosmetik Wajah","Perawatan Rambut","Parfum","Kosmetik Bibir","Perawatan Wajah","Paket Kecantikan"]
    jumlahTerjual = 0
    hargaAsli = 0
    hargaAsliTDAtas = 0
    hargaAsliTDBawah = 0
    hargaTanpaDiskonFix = 0
    hargaAsliDisRangeAtas = 0
    hargaAsliDisRangeBawah = 0
    hargaDiskon = 0
    hargaRangeAtas = 0
    hargaRangeBawah = 0
    hargaDisRangeAtas = 0
    hargaDisRangeBawah = 0
    variasi = ""
    variasiFix = ""
    productTerjual = 0
    productRating = ""
    productUlasan = 0
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
            linkadd = link
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
                    page_product +=1
                    self.db.writeLog(link, page_product)
                    self.Selenium.Load("".join([link,"?page=",str(page_product-1),"&sortBy=sales"]))
                    time.sleep(4)
                    item_count = 0
                    item_ordinal = len(self.Selenium.ExtractElements("//*[@id='main']/div/div[2]/div[2]/div[2]/div/div[3]/div[@class='shop-page__all-products-section']/div[2]/div/div[2]/div/div"))
                    #print(item_ordinal);input()
                    while item_count < item_ordinal:
                        item_count +=1
                        self.idProduct = self.Selenium.ExtractElementAttribute("href",''.join(["//*[@id='main']/div/div[2]/div[2]/div[2]/div/div[3]/div[@class='shop-page__all-products-section']/div[2]/div/div[2]/div/div[",str(item_count),"]/div/a"]))
                        if self.idProduct is not None:
                            k = self.idProduct.split("-i")
                            l = k[0].split('id/')
                            self.namaProduct= l[1].replace('-',' ').replace(',',' ')
                            self.Selenium.Load(self.idProduct)
                            self.checkCategory = self.Selenium.ExtractElementText("//*[@id='main']/div/div[2]/div[2]/div[2]/div[3]/div[2]/div[1]/div[1]/div[1]/div[2]/div[1]/div/a[3]")
                            for i in self.arraySubCategory:
                                # print('test')
                                if i == self.checkCategory:
                                    print("category match")
                                    #ini untuk dapatin harga tanpa diskon yang ada range dan tidak ataupun tidak ada
                                    self.hargaTanpaDiskon = self.Selenium.ExtractElementText("//*[@id='main']/div/div[2]/div[2]/div[2]/div[2]/div[3]/div/div[3]/div/div/div/div/div/div").replace("Rp",'').replace(".",'').split(' - ')
                                    if len(self.hargaTanpaDiskon)==1:
                                        self.hargaTanpaDiskonFix = int(self.hargaTanpaDiskon[0])
                                    elif len(self.hargaTanpaDiskon)==2:
                                        self.hargaAsliTDAtas = int(self.hargaTanpaDiskon[1])
                                        self.hargaAsliTDBawah = int(self.hargaTanpaDiskon[0])
                                    else:
                                        self.hargaTanpaDiskonFix = 0
                                    # print(self.hargaTanpaDiskon,self.hargaAsliTDAtas,self.hargaAsliTDBawah)
                                    #ini untuk dapatin harga asli diskon
                                    self.hargaAsliDiskon = self.Selenium.ExtractElementText("//*[@id='main']/div/div[2]/div[2]/div[2]/div[2]/div[3]/div/div[3]/div/div/div/div/div[1]").replace("Rp",'').replace(".",'').split(' - ')
                                    if len(self.hargaAsliDiskon)==1:
                                        self.hargaAsliDiskon = int(self.hargaAsliDiskon[0])
                                    elif len(self.hargaAsliDiskon)==2:
                                        self.hargaAsliDisRangeAtas = int(self.hargaAsliDiskon[1])
                                        self.hargaAsliDisRangeBawah = int(self.hargaAsliDiskon[0])
                                    else:
                                        self.hargaAsliDiskon = 0

                                    # print(self.hargaAsliDiskon,self.hargaAsliDisRangeAtas,self.hargaAsliDisRangeBawah)
                                    #ini untuk dapatin harga range setelah diskon

                                    self.hargaDiskon = self.Selenium.ExtractElementText("//*[@id='main']/div/div[2]/div[2]/div[2]/div[2]/div[3]/div/div[3]/div/div/div/div/div[2]/div[1]")
                                    if(self.hargaDiskon == None):
                                        self.hargaDiskon = 0
                                    else:
                                        self.hargaDiskon = self.hargaDiskon.replace("Rp",'').replace(".",'').split(' - ')
                                        if len(self.hargaDiskon)==1:
                                            self.hargaDiskon = int(self.hargaDiskon[0])
                                        elif len(self.hargaDiskon)==2:
                                            self.hargaDisRangeAtas = int(self.hargaDiskon[1])
                                            self.hargaDisRangeBawah = int(self.hargaDiskon[0])
                                        else:
                                            self.hargaDiskon = 0

                                    # print(self.hargaDiskon,self.hargaDisRangeAtas,self.hargaDisRangeBawah)
                                    #self.hargaTanpaDiskonFix, self.hargaAsliTDAtas, self.hargaAsliTDBawah, hargaAsliDiskon, hargaAsliDisRangeAtas,hargaAsliDisRangeBawah, hargaDiskon, hargaDisRangeAtas, hargaDisRangeBawah
                                    try :
                                        self.jmlvariasi = len(self.Selenium.ExtractElements("//*[@id='main']/div/div[2]/div[2]/div[2]/div[2]/div[3]/div/div[4]/div/div[2]/div/div[1]/div/button"))
                                        self.jmlvariasi2 = len(self.Selenium.ExtractElements("//*[@id='main']/div/div[2]/div[2]/div[2]/div[2]/div[3]/div/div[4]/div/div[3]/div/div[1]/div/button"))
                                        if(self.jmlvariasi!=0):
                                            print(self.jmlvariasi)
                                            item_variasi = 0
                                            while item_variasi < self.jmlvariasi:
                                                item_variasi +=1
                                                self.variasi = self.Selenium.ExtractElementText("//*[@id='main']/div/div[2]/div[2]/div[2]/div[2]/div[3]/div/div[4]/div/div[2]/div/div[1]/div/button["+str(item_variasi)+"]")
                                                self.variasiFix = self.variasiFix + "|" +self.variasi
                                        elif(self.jmlvariasi2!=0):
                                            print(self.jmlvariasi2)
                                            item_variasi = 0
                                            while item_variasi < self.jmlvariasi2:
                                                item_variasi +=1
                                                self.variasi = self.Selenium.ExtractElementText("//*[@id='main']/div/div[2]/div[2]/div[2]/div[2]/div[3]/div/div[4]/div/div[2]/div/div[1]/div/button["+str(item_variasi)+"]")
                                                self.variasiFix = self.variasiFix + "|" +self.variasi
                                        else:
                                            self.variasi=""

                                        self.variasi= self.variasi.replace(',',' ')
                                    except Exception as e:
                                        self.variasi = ""
                                    # print(self.variasiFix)
                                    self.productTerjual = self.Selenium.ExtractElementText("//*[@id='main']/div/div[2]/div[2]/div[2]/div[2]/div[3]/div/div[2]/div[3]/div[1]")
                                    if (self.productTerjual == None):
                                        self.productTerjual = 0
                                    else:
                                        self.productTerjual = int(self.productTerjual)
                                    self.productRating = self.Selenium.ExtractElementText("//*[@id='main']/div/div[2]/div[2]/div[2]/div[2]/div[3]/div/div[2]/div[1]/div[1]")
                                    self.productUlasan = int(self.Selenium.ExtractElementText("//*[@id='main']/div/div[2]/div[2]/div[2]/div[2]/div[3]/div/div[2]/div[2]/div[1]"))
                                    self.db.insertProductVerse2(linkadd,self.idProduct, self.checkCategory,self.namaProduct, self.productTerjual, self.productRating, self.productUlasan,self.variasiFix, self.hargaTanpaDiskonFix, self.hargaAsliTDAtas, self.hargaAsliTDBawah,self.hargaDiskon,self.hargaDisRangeAtas,self.hargaDisRangeBawah, self.hargaAsliDiskon,self.hargaAsliDisRangeAtas,self.hargaAsliDisRangeBawah)
                                    self.jumlahTerjual = 0
                                    self.hargaAsli = 0
                                    self.hargaAsliTDAtas = 0
                                    self.hargaAsliTDBawah = 0
                                    self.hargaTanpaDiskonFix = 0
                                    self.hargaAsliDisRangeAtas = 0
                                    self.hargaAsliDisRangeBawah = 0
                                    self.hargaDiskon = 0
                                    self.hargaRangeAtas = 0
                                    self.hargaRangeBawah = 0
                                    self.hargaDisRangeAtas = 0
                                    self.hargaDisRangeBawah = 0
                                    self.variasi = ""
                                    self.variasiFix = ""
                                    self.productTerjual = 0
                                    self.productRating = ""
                                    self.productUlasan = 0
                                elif i!= self.checkCategory:
                                    print("category not match")
                            self.Selenium.BackPage()
                            self.variasiFix = ""
            self.db.updateStatusEnd(linkadd)

try:
    Run().Crawling()
except Exception as e:
    Run().Crawling()

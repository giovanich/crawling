#!/usr/bin/env python3
import pymongo
from pymongo import MongoClient
import datetime
client = MongoClient('localhost', 27017)
db = client.shopee_co_id


class MongoDB:
    def insert_Shopee(self,Merchant_html_path, Merchant_name, Merchant_rate, Merchant_product, Merchant_established, Merchant_followers, Merchant_location ):
        detail = {
                    '_id' : Merchant_html_path,
                    'Merchant_name' : Merchant_name,
                    'Merchant_rate' : Merchant_rate,
                    'Merchant_location' : Merchant_location,
                    'Merchant_established' : Merchant_established,
                    'Merchant_product' : Merchant_product,
                    'Merchant_followers' : Merchant_followers,
                    'Merchant_crawlingTime' : datetime.datetime.now(),
                    'status' : 1
                }
        result=db.MerchantJuni.insert_one(detail)
    def checkMerchant(self, Merchant_html_path):
        result= db.MerchantJuni.find({'_id' : Merchant_html_path},{'_id':1})
        for i in result:
            return str(i)

    def updateStatus(self, x):
            db.MerchantJuni.update(
                  {"_id": x},
                  { "$set": {"status": 2} }
                )
    def updateStatusEnd(self, x):
            db.MerchantJuni.update(
                  {"_id": x},
                  { "$set": {"status": 0} }
                )
    def checkMerchantToCrawl(self):
        #print("start")
        a = ''
        check = db.MerchantJuni.find({'status':1},{'_id':1}).limit(1).collation({'locale': "en_US", 'numericOrdering': True}).sort('Merchant_followers', pymongo.DESCENDING)
        count = db.MerchantJuni.find({'status':1},{'_id':1}).limit(1).collation({'locale': "en_US", 'numericOrdering': True}).sort('Merchant_followers', pymongo.DESCENDING).count()
        #print(count);input()
        if count >= 1:
            for k in check:
                a = str(k).replace('{\'_id\': \'','').replace('\'}','')
                #print("nilai "+a)
        else:
            result = db.MerchantJuni.find({'status':2},{'_id':1}).limit(1).collation({'locale': "en_US", 'numericOrdering': True}).sort('Merchant_followers', pymongo.DESCENDING)
            for j in result:
                a = str(j).replace('{\'_id\': \'','').replace('\'}','')

        return str(a)

    def insertProduct(self, idProduct, merchant_link, namaProduct, jumlahTerjual, hargaAsli, hargaDiskon, hargaRangeAtas, hargaRangeBawah, hargaDisRangeAtas, hargaDisRangeBawah):
        product_info ={"idProduct":idProduct,
            "namaProduct":namaProduct,
            "jumlahTerjual":jumlahTerjual,
            "hargaAsli":hargaAsli,
            "hargaDiskon":hargaDiskon,
            "hargaRangeAtas":hargaRangeAtas,
            "hargaRangeBawah":hargaRangeBawah,
            "hargaDisRangeAtas":hargaDisRangeAtas,
            "hargaDisRangeBawah":hargaDisRangeBawah}
        db.MerchantJuni.update({'_id': merchant_link }, { "$addToSet": { "ProductInfo": product_info } })
    def insertProductVerse2(self, merchant_link,idProduct,kategory, namaProduct, jumlahTerjual, ratingProduct, ulasanProduct, variasiProduct,hargaAsli, hargaAsliTDAtas, hargaAsliTDBawah,hargaDiskon, hargaDisRangeAtas, hargaDisRangeBawah, hargaAsliDiskon, hargaAsliDiskonAtas, hargaAsliDiskonBawah):
        product_info ={"idProduct":idProduct,
            "namaProduct":namaProduct,
            "jumlahTerjual":jumlahTerjual,
            "ratingProduct":ratingProduct,
            "jumlahUlasan" :ulasanProduct,
            "kategory": kategory,
            "variasi" : variasiProduct,
            "hargaAsli":hargaAsli,
            "hargaAsliTDAtas": hargaAsliTDAtas,
            "hargaAsliTDBawah": hargaAsliTDBawah,
            "hargaDiskon":hargaDiskon,
            "hargaDisRangeAtas":hargaDisRangeAtas,
            "hargaDisRangeBawah":hargaDisRangeBawah,
            "hargaAsliDiskon": hargaAsliDiskon,
            "hargaAsliDiskonAtas": hargaAsliDiskonAtas,
            "hargaAsliDiskonBawah": hargaAsliDiskonBawah}
        db.MerchantJuni.update({'_id': merchant_link }, { "$addToSet": { "ProductInfo": product_info } })
        db.MerchantJuni.update({'_id' : merchant_link},{'$set' :{'Merchant_crawlingTime' : datetime.datetime.now()}})


    def setStatus(self,Merchant_link):
        db.MerchantJuni.update({'_id': Merchant_link},{'$set':{'status':2}})

    def checkProduct(self, merchant_link, idProduct):

        result = db.MerchantJuni.find({ "_id" : merchant_link ,'ProductInfo' : {'$elemMatch':{'idProduct':idProduct}}},{'_id':1})
        for i in result:
            return str(i)
    def countMerchant(self):
        return db.MerchantJuni.find({'status':1}).count()

    def writeLog(self,Merchant_link, page_product):
        check = db.Log.find({'_id' : Merchant_link}).count()
        #print(count);input()
        if check == 1:
            db.Log.update({'_id' : Merchant_link},{'$set' : {'Product_page' : page_product,'crawltime' : datetime.datetime.now()}})
        else:
            db.Log.insert({'_id' : Merchant_link,'Product_page' : page_product,'crawltime' : datetime.datetime.now()})


    def checkLastCrawling(self,Merchant_link):
        check = db.Log.find({'_id' : Merchant_link}).count()
        if check == 0:
            db.Log.insert({'_id': Merchant_link, 'Product_page':0,'crawltime' : datetime.datetime.now()})
            return 0
        else:
            searchPage = db.Log.find({'_id' : Merchant_link},{'_id':0, 'Product_page':1 })
            for i in searchPage:
                b = str(i)
                return int(b.replace('{\'Product_page\': ','').replace('}',''))

    def updateMerchantPageLog(self,page_count):
        #untuktrycatch error
        db.Log.update({'_id': 'crawlmerchant' },{"$set": { 'page': page_count}})

    def timeTrackError(self, errormsg):
        db.Log.update({'_id': 'crawlmerchant' },{'$addToSet': { 'timeError': datetime.datetime.now(), 'errorMessage': errormsg}})

    def updateMerchantTimeEnd(self):
        db.Log.update({'_id': 'crawlmerchant' },{"$set": { 'timeEnd':  datetime.datetime.now()}})

    def checkMerchantPage(self,yesno):
        if yesno is True:
            db.Log.update({'_id': 'crawlmerchant'},{'$set' :{'timeStart' : datetime.datetime.now()}})
            check = db.Log.find({'_id' : 'crawlmerchant'},{'page' : 1,'_id' : 0})
            for i in check:
                a = str(i).replace("{\'page\': ",'').replace(" }",'')
                return int(a)
        else:
            check = db.Log.find({'_id' : 'crawlmerchant'},{'page' : 1,'_id' : 0})
            for i in check:
                a = str(i).replace("{\'page\': ",'').replace(" }",'')
                return int(a)

    def lastPage(self,Merchant):
        result = db.CategoryEdit.find({'_id':Merchant},{'last_page':1,'_id':0})
        for i in result:
            a = str(i).replace("{\'last_page\': ",'').replace("}",'')
            return int(a)

    def updatePages(self,Merchant,pages=0):
        db.CategoryEdit.update({'_id':Merchant},{'$set':{'last_page':pages}})



    def updateRunning(self,x):
        db.CategoryEdit.update(
              {"_id": x},
              { "$set": {"status": 2} }
            )
    def updateDoneStatus(self,x):
        db.CategoryEdit.update(
                  {"_id": x},
                  { "$set": {"status": 0} }
                )
    def updloop(self,x):
        db.MerchantJuni.update(
                  {"_id": x},
                  { "$set": {"status": 1} }
                )
    def updlopon(self,x):
        db.MerchantJuni.update(
              {"_id": x},
              { "$set": {"status": 2} }
            )
    def updloopend(self,x):
        db.MerchantJuni.update(
                  {"_id": x},
                  { "$set": {"status": 0} }
                )
    def updateDoneStatus1(self,x):
        db.MerchantJuni.update(
                  {"_id": x},
                  { "$set": {"status": 1} }
                )
    def count_status(self):
        return db.MerchantJuni.find({'statusloop':2}).count()

    def updateStatusCategoryAll(self,status = 1):
        db.CategoryEdit.update_many({},{ "$set": {"status": status} })

    def checkCityStatus(self,Category):
        a = ''
        result = db.CategoryEdit.find({ "_id" : Category ,'Region' : {'$elemMatch':{'status': 2}}},{'_id':0,'Region.$.City':1})
        print(result.count())
        if result.count()==1:
            for i in result:
                a = str(i).replace("{'Region': [{'City': '","").replace("', 'status': 2.0}]}","").replace("', 'status': 2}]}","")
        else:
            result = db.CategoryEdit.find({ "_id" : Category ,'Region' : {'$elemMatch':{'status': 1}}},{'_id':0,'Region.$.City':1})
            for i in result:
                a = str(i).replace("{'Region': [{'City': '","").replace("', 'status': 1.0}]}","").replace("', 'status': 1}]}","")
        return a

    def updatedStatusCategory(self,Category):
        if self.checkCityStatus(Category) == '':
            self.updateDoneStatus(Category)
        else:
            self.updateRunning(Category)

    def updateStatusCityRun(self,Category,city):
        result = db.CategoryEdit.update({ "_id" : Category ,'Region' : {'$elemMatch':{'City': city}}},{"$set": {"Region.$.status": 2}})

    def updateStatusCityDone(self,Category,city):
        result = db.CategoryEdit.update({ "_id" : Category ,'Region' : {'$elemMatch':{'City': city}}},{"$set": {"Region.$.status": 0}})

    def updateStatusCity(self,Category,city):
        result = db.CategoryEdit.update({ "_id" : Category ,'Region' : {'$elemMatch':{'City': city}}},{"$set": {"Region.$.status": 1}})

    def getLinkToCrawling(self):
        a = ''
        b = []
        check = db.CategoryEdit.find({'status' : 2},{'_id' : 1}).limit(1).count()
        if check == 1:
            result = db.CategoryEdit.find({'status' : 2},{'_id' : 1})
            for i in result:
                a = str(i).replace('{\'_id\': \'','').replace('\'}','')
                b.append(a)
                b.append(self.checkCityStatus(a))
        else:
            result = db.CategoryEdit.find({'status':1},{'_id':1}).limit(1)
            for i in result:
                a = str(i).replace('{\'_id\': \'','').replace('\'}','')
                b.append(a)
                b.append(self.checkCityStatus(a))
        return b
    def updateStatusCityAll(self,status = 1):
        db.CategoryEdit.update_many({ "_id" : '$exists','Region' : '$exists'},{"$set": {"Region.$.status": status}})
    def countCategory(self):
        a = db.CategoryEdit.find({'status':1}).count()
        b = db.CategoryEdit.find({'status':2}).count()
        return a+b



    #def parseIntAtt(self):
    #    db.MerchantJuni.find({Merchant_followers :{$exists: true}}).forEach(function(obj){obj.Merchant_followers = new NumberInt(obj.Merchant_followers); db.MerchantJuni.save(obj); } );
    #    db.MerchantJuni.find({Merchant_product :{$exists: true}}).forEach(function(obj){obj.Merchant_product = new NumberInt(obj.Merchant_followers); db.MerchantJuni.save(obj); } );

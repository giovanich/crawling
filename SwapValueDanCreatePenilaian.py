#!/usr/bin/env python3
import pymongo
from pymongo import MongoClient
import datetime
client = MongoClient('localhost', 27017)
db = client.shopee_co_id

db.MerchantPerawatanWajah.delete_many({'_id' : None})
db.MerchantPerawatanWajah.delete_many({'Merchant_followers' : {'$regex': '/%$/'}}})
db.MerchantPerawatanTubuh.update_many({'Merchant_rate' : '0 Penilaian'},{'$set' : {'Merchant_rate' : '0.0 (0 Penilaian)'}})
#swap nilai toko baru yang tempat fieldnya tertukar
a = db.MerchantPerawatanWajah.find({'Merchant_established' : None},{'_id' : 1,'Merchant_rate' : 1,'Merchant_followers' :1})
for i in a:
    x = str(i).replace("{\'_id\': \'",'').replace("\', \'Merchant_rate\': \'",'#').replace("\', \'Merchant_followers\': \'",'#').replace("\'}",'')

    z = x.split('#')
    db.MerchantPerawatanWajah.update({'_id' : z[0]},{'$set' :{'Merchant_established' : z[1] , 'Merchant_rate' : z[2], 'Merchant_followers' : 0}})

#hapus merchant yang tidak mempunyai followers, biasanya karena toko baru
db.MerchantPerawatanWajah.remove({'$or' :[{'Merchant_followers' : None},{'Merchant_followers' : ''}]})

#memisahkan rate antara persentase rate dengan jumlah penilaian
j = ""
b = db.MerchantPerawatanWajah.find({'Penilaian' : {'$exists': False}},{'_id':1,'Merchant_rate':1})
for i in b:
    b = str(i).replace("{\'_id\': \'",'').replace("\',",'|').replace(" \'Merchant_rate\': \'",'').replace(" (",' - ').replace(" Penilaian)\'}",'')
    j = b.split('|')
    print(j)
    k = j[1].split(' - ')
    l = int(k[1])
    print(k)
    db.MerchantPerawatanWajah.update({'_id': j[0]}, {'$set':{'Merchant_rate' : k[0],'Penilaian':l }})
#hapus merchant yang memiliki jumlah penilaian tidak sampai 5rb
db.MerchantPerawatanWajah.remove({'Penilaian':{'$lt' : 5000}})

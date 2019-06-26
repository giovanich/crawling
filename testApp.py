#!/usr/bin/env python3
import pymongo
from pymongo import MongoClient
import datetime
client = MongoClient('localhost', 27017)
db = client.shopee_co_id

v = ['']
a = db.MerchantPerawatanTubuh.find({},{'_id':0,'Merchant_rate':1})
for i in a:
    p = str(i).replace("\', \'Penilaian\': \'",'')

def takeFirst(elem):
    return elem[0]

a = [{1,'a'},{7,'b'}, {4, 'd'}]
a.append({8, 'c'})
a.sort(key=takeFirst)
print(a)
if len(a)>=21:
    del a[20:len(a)]
print(a)

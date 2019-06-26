#!/usr/bin/env python3
import pymongo
from pymongo import MongoClient
import datetime
client = MongoClient('localhost', 27017)
db = client.shopee_co_id


a = db.Category.find({'Region' : {'$elemMatch' : {'status' : 1}}},{'_id' :0,'Region.$.City':1})
for s in a:
    print (s)

#!/usr/bin/env python3
import pymongo
from pymongo import MongoClient
import datetime
client = MongoClient('localhost', 27017)
db = client.shopee_co_id


db.MerchantJuni.update_many({'status' : 1},{'$set' : {'statusloop' : 1}})

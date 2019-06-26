import pymongo
from pymongo import MongoClient
import datetime
client = MongoClient(
client = pymongo.MongoClient("mongodb+srv://DNA-1:User01@clusterawscrawling-sd7jc.mongodb.net/test?retryWrites=true&w=majority")
db = client.test

#!/usr/bin/env python3
import time
from timeloop import Timeloop
from datetime import timedelta
import os
from MongoShopee import MongoDB
tl = Timeloop()

@tl.job(interval=timedelta(seconds=1))
def startpoint():
    if MongoDB().count_status() !=5 :
        print('a')
        os.system('screen ./shopeeProduct2.py &')
@tl.job(interval=timedelta(hours=1))
def sample_job_every_1h():
    if MongoDB().count_status() !=5:
        print("Repeat")
        os.system('screen ./shopeeProduct2.py &')
if __name__ == "__main__":
    tl.start(block=True)

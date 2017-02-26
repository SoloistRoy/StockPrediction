import datetime
import time as T

from yahoo_finance import Share
from pymongo import MongoClient

def get_realtimeData(cName, collection):
    stock = Share(cName)
    post = {'datetime':stock.get_trade_datetime(), 'price':stock.get_price(),
            'Volume':stock.get_volume()}
    post_id = collection.insert_one(post).inserted_id


dbClient = MongoClient()
db = dbClient.StockRealtime

now = datetime.datetime.now()

# beginTime = now.replace(hour=9, minute=0, second=0, microsecond=0)
# endTime = now.replace(hour=16, minute=0, second=0, microsecond=0)
stockList = ['YHOO', 'GOOG']
# while now > beginTime and now < endTime:
while 1:
    for stock in stockList:
        get_realtimeData(stock, db[stock])
    T.sleep(60)
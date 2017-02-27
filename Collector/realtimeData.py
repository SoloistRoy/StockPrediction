import datetime
import time as T

from yahoo_finance import Share
from pymongo import MongoClient
from pymongo import errors

def get_realtimeData(cName, collection):
    stock = Share(cName)
    collection.create_index('datetime', unique = True)
    post = {'datetime':stock.get_trade_datetime(), 'price':stock.get_price(),
            'Volume':stock.get_volume()}
    try:
    	collection.insert_one(post)
    except errors.DuplicateKeyError:
    	print datetime.datetime.now()


dbClient = MongoClient()
db = dbClient.StockRealtime

now = datetime.datetime.now()

# beginTime = now.replace(hour=9, minute=0, second=0, microsecond=0)
# endTime = now.replace(hour=16, minute=0, second=0, microsecond=0)
stockList = ['YHOO', 'GOOG', 'AAPL', 'BIDU', 'BABA']
# while now > beginTime and now < endTime:
for i in stockList:
	db[i].remove()
while 1:
    for stock in stockList:
        get_realtimeData(stock, db[stock])
    print ++1
    T.sleep(59.30)
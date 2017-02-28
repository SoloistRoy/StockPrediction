from iqfeed import historicData
from pymongo import MongoClient

import datetime

dateStart = datetime.datetime(2017,2,27)
dateEnd = datetime.datetime(2017,2,27)     

iq = historicData(dateStart, dateEnd, 60)

dbClient = MongoClient()
db = dbClient.StockRealtime

stockList = ['YHOO', 'GOOG', 'AAPL', 'BIDU', 'BABA']

for stock in stockList:
    db[stock].remove()
    stockData = iq.download_symbol(stock)
    # stockData = stockData.to_dict()
    stockData = stockData.split(',')
    transData = []
    while stockData:
        temp = []
        for i in range(7):
            temp.append(stockData.pop(0))
        transData.append(temp)
    for item in transData:
        post = {'datetime':item[0], 'price':float(item[4]), 'Volume':int(item[5])}
        db[stock].insert_one(post)
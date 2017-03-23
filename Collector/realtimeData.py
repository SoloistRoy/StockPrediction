from iqfeed import historicData
from pymongo import MongoClient

import datetime

dateStart = datetime.datetime(2017,2,27)
dateEnd = datetime.datetime(2017,3,2)     

iq = historicData(dateStart, dateEnd, 60) #last parameter is the time gap between 2 reads

dbClient = MongoClient()
dbClient.drop_database('StockRealtime')
db = dbClient.StockRealtime

stockList = ['YHOO', 'GOOG', 'AAPL', 'BIDU', 'BABA']
for stock in stockList:
    stockData = iq.download_symbol(stock)
    stockData = stockData.split(',')
    transData = []
    while stockData:
        temp = []
        for i in range(7):
            temp.append(stockData.pop(0))
        transData.append(temp)
    for item in transData:
        dt = item[0].split(' ')
        post = {'time':dt[1], 'price':float(item[4]), 'volume':int(item[5])}
        dt = dt[0].split('-')
        db[stock+dt[2]+dt[1]+dt[0]].insert_one(post)
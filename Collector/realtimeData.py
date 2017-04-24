# written by: Yiran Sun
# assisted by:
# debugged by: Yiran Sun
from iqfeed import historicData
from pymongo import MongoClient
import datetime

dateStart = datetime.datetime(2017,2,1)
dateEnd = datetime.datetime(2017,4,23)     

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
        dt[0] = dt[0].split('-')
        dt[1] = dt[1].split(':')
        dt = datetime.datetime(int(dt[0][0]),int(dt[0][1]),int(dt[0][2]),int(dt[1][0]),int(dt[1][1]),int(dt[1][2]))
        post = {'time':dt, 'price':float(item[4]), 'volume':int(item[5])}
        db[stock].insert_one(post)
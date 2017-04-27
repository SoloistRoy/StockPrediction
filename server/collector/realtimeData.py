# written by: Yiran Sun
# assisted by:
# debugged by: Yiran Sun
from iqfeed import historicData
from pymongo import MongoClient
import pymongo
import datetime

def getRealtime():
    dbClient = MongoClient()
    db = dbClient.StockRealtime
    stockList = ['YHOO', 'GOOG', 'AAPL', 'CCF', 'BAC', 'FB', 'TWTR', 'BIDU', 'BABA', 'EDU']

    pricceList = {}
    resPriceList = []

    dateEnd = datetime.datetime.now()

    for stock in stockList:
        t = list(db[stock].find().sort([('time', pymongo.DESCENDING)]))
        dateStart = t[0]['time'] + datetime.timedelta(minutes=1)
        iq = historicData(dateStart, dateEnd, 60)

        stockData = iq.download_symbol(stock)
        if stockData == 'E,!NO_DATA!,':
            pricceList[stock] = t[0]
            continue
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
    #         post = {'name':stock, 'price': post['price']}
    #     resPriceList.append(post)
    # return resPriceList
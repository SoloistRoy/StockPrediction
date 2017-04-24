# written by: Yiran Sun
# assisted by:
# debugged by: Yiran Sun
from yahoo_finance import Share
from pymongo import MongoClient
import datetime

def get_annualData(cName, collection):
	collection.remove()
	stock = Share(cName)
	dataSet = stock.get_historical('2016-1-1','2017-4-23')
	for item in dataSet:
		item['Date'] = item['Date'].split('-')
		item['Date'] = datetime.datetime(int(item['Date'][0]),int(item['Date'][1]),int(item['Date'][2]))
		post = {'date':item['Date'], 'open':float(item['Open']),
				'close':float(item['Close']), 'high':float(item['High']),
				'low':float(item['Low']), 'volume':int(item['Volume'])}
		collection.insert_one(post)

dbClient = MongoClient()
db = dbClient.StockAnnual

stockList = ['YHOO', 'GOOG', 'AAPL', 'BIDU', 'BABA']
for stock in stockList:
	get_annualData(stock, db[stock])
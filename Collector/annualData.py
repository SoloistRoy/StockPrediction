from yahoo_finance import Share
from pymongo import MongoClient

def get_annualData(cName, collection):
	stock = Share(cName)
	dataSet = stock.get_historical('2016-2-1','2017-2-1')
	for item in dataSet:
		post = {'date':item['Date'], 'open':float(item['Open']),
				'close':float(item['Close']), 'high':float(item['High']),
				'low':float(item['Low']), 'volume':int(item['Volume'])}
		post_id = collection.insert_one(post).inserted_id

dbClient = MongoClient()
db = dbClient.StockAnnual

stockList = ['YHOO', 'GOOG']
for stock in stockList:
	get_annualData(stock, db[stock])
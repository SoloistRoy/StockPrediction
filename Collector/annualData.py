from yahoo_finance import Share
from pymongo import MongoClient

def getStockData(cName, collection):
	stock = Share(cName)
	dataSet = stock.get_historical('2016-12-1','2017-2-1')
	for item in dataSet:
		post = {'datet':item['Date'], 'open':float(item['Open']),
				'close':float(item['Close']), 'high':float(item['High']),
				'low':float(item['Low']), 'volume':int(item['Volume'])}
		# posts = db.posts
		post_id = collection.insert_one(post).inserted_id
		print post_id
	return dataSet

dbClient = MongoClient()
db = dbClient.StockAnnual

stockList = ['YHOO', 'GOOG']
for i in stockList:
	collection = db[i]
	getStockData(i, collection)

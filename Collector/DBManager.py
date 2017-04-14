from yahoo_finance import Share
from pymongo import MongoClient
import pymongo
def insert_stock_annualData(cName, collection, startTime = '2015-3-1', endTime = '2017-3-1'):
	collection.remove()
	stock = Share(cName)
	dataSet = stock.get_historical(startTime,endTime)
	for item in dataSet:
		post = {'date':item['Date'], 'open':float(item['Open']),
				'close':float(item['Close']), 'high':float(item['High']),
				'low':float(item['Low']), 'volume':int(item['Volume'])}
		collection.insert_one(post)
def get_stock_raw_data(stock):
	dbClient = MongoClient()
	db = dbClient.StockAnnual
	cursor = db[stock].find().sort([('date', pymongo.ASCENDING)])
	return cursor

def get_stock_atrributes_data(stock, attrList):
	dbClient = MongoClient()
	db = dbClient.StockAnnual
	#only query the data we need
	query = {attr: 1 for attr in attrList}
	#exclude id
	query['_id'] = 0
	cursor = db[stock].find({}, query).sort([('date', pymongo.ASCENDING)])
	#tranform cursor to list so it becomes iterative
	l = list(cursor)
	res = []
	for attr in attrList:
		res.append([d[attr] for d in l])
	return tuple(res)
def update_all_annualdata():
	dbClient = MongoClient()
	db = dbClient.StockAnnual

	stockList = ['YHOO', 'GOOG', 'AAPL', 'BIDU', 'BABA']
	for stock in stockList:
		insert_stock_annualData(stock, db[stock])
#update_all_annualdata()
# close, = get_stock_atrributes_data('BABA', ['close'])
# print close

#print get_stock_atrributes_data('BABA', ['close', 'high'])
# dbClient = MongoClient()
# db = dbClient.StockAnnual
#
# stockList = ['YHOO', 'GOOG', 'AAPL', 'BIDU', 'BABA']
# for stock in stockList:
# 	get_annualData(stock, db[stock])
# for stock in stockList:
# 	cursor = db[stock].find().sort([('date', pymongo.ASCENDING)])
# 	for sInfo in cursor:
# 		print sInfo
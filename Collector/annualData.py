# written by: Yiran Sun
# assisted by:
# debugged by: Yiran Sun
from yahoo_finance import Share
from pymongo import MongoClient
import pymongo
import datetime

def getAnnual():
	dateEnd = str(datetime.datetime.now().date())
	dateEnd = '%s-%s-%s' % (dateEnd[:4],dateEnd[5:7],dateEnd[-2:])
	dateStart = '2016-01-01'

	def get_annualData(cName, collection):
		t = list(db[cName].find().sort([('date', pymongo.DESCENDING)]))
		# dateStart = str(t[0]['date'].date())
		# dateStart = '%s-%s-%s' % (dateStart[:4],dateStart[5:7],dateStart[-2:])
		stock = Share(cName)
		dataSet = stock.get_historical(dateStart,dateEnd)
		for item in dataSet:
			item['Date'] = item['Date'].split('-')
			item['Date'] = datetime.datetime(int(item['Date'][0]),int(item['Date'][1]),int(item['Date'][2]))
			post = {'date':item['Date'], 'open':float(item['Open']),
					'close':float(item['Close']), 'high':float(item['High']),
					'low':float(item['Low']), 'volume':int(item['Volume'])}
			collection.insert_one(post)

	dbClient = MongoClient()
	db = dbClient.StockAnnual

	stockList = ['YHOO', 'GOOG', 'AAPL', 'CCF', 'BAC', 'FB', 'TWTR', 'BIDU', 'BABA', 'EDU']
	for stock in stockList:
		get_annualData(stock, db[stock])

getAnnual()
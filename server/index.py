# written by: Yiran Sun
# assisted by: Jingyuan Li
# debugged by: Yiran Sun, Jingyuan Li
# import sys
# sys.path.append('../Collector')
from flask import Flask, render_template, url_for, request, session, redirect, jsonify
from flask_pymongo import PyMongo
from bson import json_util
import json
import datetime
import pymongo
import predictor
from collector import realtimeData
from collector import annualData
from collector import Indicator as idc
from collector import DBManager as dbm

app = Flask('StockAnnual', template_folder = 'G:\Python\Web\StockPrediction',static_folder='G:\Python\Web\StockPrediction')
# app = Flask('StockAnnual', template_folder = '/Users/jingyuan/WorkSpace/SEProject/StockPrediction',static_folder='/Users/jingyuan/WorkSpace/SEProject/StockPrediction')
app.config['MONGO_DBNAME'] = 'StockAnnual'
app.config['MONGO_URI'] = 'mongodb://localhost/StockAnnual'
app.config['SECRET_KEY'] = 'super secret key'

app.config['MONGO2_DBNAME'] = 'StockRealtime'

mongo = PyMongo(app)
mongo2 = PyMongo(app, config_prefix='MONGO2')
# dbClient = MongoClient()
# db = dbClient.StockRealtime
priceList = realtimeData.getRealtime() # test: comment these 2 lines
annualData.getAnnual()
# priceList = {'AAPL':{'price':100.00},'BIDU':{'price':100.00},'BABA':{'price':100.00},'YHOO':{'price':100.00},'GOOG':{'price':100.00}}

@app.route('/home')
@app.route('/')
def index():
	if 'piece' in session:
		m = session['piece']
		print m
		session.clear()
		# return str(m)

	# online_users = mongo.db.GOOG.find({'date': '2017-02-01'})
	return render_template('index.html')

@app.route('/query', methods=['POST'])
def query():
	# stockName = request.form['stockName']
	print(request.json)
	stockName = request.json['stockName']
	# stock = mongo.db[stockName]
	# m = stock.find({})
	# session['piece'] = m[0]['high']
	# mClone = json_util.dumps(m.clone())
	# s = copy.deepcopy(mClone)
	# print 's: ', type(mClone)
	stock = priceList[stockName]
	print stock
	return jsonify(0, stock['price'])

@app.route('/hisData', methods=['POST'])
def hisQuery():
	data = request.data
	dataDict = json.loads(data)
	stockName = dataDict['stockName']
	dateRange = dataDict['dateRange']
	print stockName, type(dateRange)
	dtsmall = datetime.datetime(int(dateRange[6:10]),int(dateRange[:2]),int(dateRange[3:5]))
	dtlarge = datetime.datetime(int(dateRange[19:]),int(dateRange[13:15]),int(dateRange[16:18]))
	print dtlarge,dtsmall
	stock = mongo.db[stockName]
	historicalData = stock.find({'date':{'$gte':dtsmall, '$lte':dtlarge}}).sort([('date', pymongo.ASCENDING)])
	historicalResult  = []
	for i in historicalData:
		temp = str(i['date']).split(' ')
		i['date'] = temp[0]
		historicalResult.append(i)
	historicalData = json_util.dumps(historicalResult)
	# print idc.RSI(stockName), idc.MACD(stockName)
	return historicalData

@app.route('/getPre', methods=['POST'])
def predict():
	stockName = str(request.json['stockName'])
	stock = mongo.db[stockName]
	latest = stock.find().sort([('date', pymongo.DESCENDING)])[:5]
	latest = [[one['high'],one['low'],one['open'],one['close'],one['volume']] for one in latest]
	
	prePriceJson = []
	#period = datePicker -- add module in JS
	period = int(request.json['datePicker'])
	method = str(request.json['method'])

	mPredictor = predictor.annualPredict()
	prePrice = mPredictor.load(stockName, period, latest, method)
	for i in range(period):
		dataJson = {}
		dataJson['high'] = prePrice[2*i][0]
		dataJson['low'] = prePrice[2*i][1]
		dataJson['open'] = prePrice[2*i][2]
		dataJson['close'] = prePrice[2*i][3]
		dataJson['volume'] = prePrice[2*i][4]
		dataJson['date'] = prePrice[2*i+1]
		prePriceJson.append(dataJson)
	prePriceJson = json_util.dumps(prePriceJson)
	print "----------------------------------"
	# print prePriceJson #Result of 5 days prediction
	return prePriceJson

@app.route('/indData', methods=['POST'])
def indQuery():
	# Get query data
	stockName = str(request.json['stockName'])
	method = str(request.json['method'])
	indName = str(request.json['indicatorName'])
	dateRange = str(request.json['dateRange'])
	print stockName, indName, dateRange
	stock = mongo.db[stockName]
	# Calculate date range
	dtsmall = datetime.datetime(int(dateRange[6:10]),int(dateRange[:2]),int(dateRange[3:5]))
	dtlarge = datetime.datetime(int(dateRange[19:]),int(dateRange[13:15]),int(dateRange[16:18]))
	print dtlarge,dtsmall
	indResult = []
	indDate  = []
	indData = stock.find({'date':{'$gte':dtsmall, '$lte':dtlarge}}).sort([('date', pymongo.ASCENDING)])
	# Get close price list (indResult) and date list (indDate)
	for i in indData:
		temp = float(i['close'])
		temp1 = str(i['date']).split(' ')
		indDate.append(temp1[0])
		indResult.append(temp)
	# Get indicator data
	N = 10
	print "stock======----------==================="
	print len(indResult)
	print len(indDate)
	if indName == 'SMA':
		indDateResult = indDate[N:len(indDate)]
		idcData = idc.SMA(indResult, N)
	elif indName == 'EMA':
		indDateResult = indDate
		idcData = idc.EMA(indResult, N)
	elif indName == 'RSI':
		indDateResult = indDate[N:len(indDate)]
		idcData = idc.RSI(indResult)
	# elif indName == 'MACD':
	# 	idcData = idc.MACD(indResult)
	print "INDICATOR DATA CALCULATED-----------------------"
	print len(indDateResult)
	print len(idcData)
	idcJson = []
	for i in range(len(idcData)):
		dataJson = {}
		dataJson['date'] = indDateResult[i]
		dataJson['close'] = idcData[i]
		idcJson.append(dataJson)
	idcJson = json_util.dumps(idcJson)
	print "idcJson-------------------"
	return idcJson

@app.route('/dateQuery', methods=['POST'])
def dateQuery():
	stockName = str(request.json['stockName'])
	stockDate = str(request.json['stockDate'])
	print stockName, stockDate
	stockDate = stockDate.split('-')
	dtsmall = datetime.datetime(int(stockDate[0]), int(stockDate[1]), int(stockDate[2]), 0, 0,)
	dtlarge = dtsmall+datetime.timedelta(1)
	print dtsmall, dtlarge
	stock = mongo2.db[stockName]
	dateData = list(stock.find({'time':{'$gt':dtsmall, '$lt':dtlarge}}).sort([('time', pymongo.ASCENDING)]))
	if len(dateData) == 0:
		return 'VOID'
	for i in dateData:
		i['time'] = i['time'].time().strftime('%H:%M')
	# dateData = [{'time': '12:00','price':128.9,'volume': 11223344},{'time': '12:00','price':128.9,'volume': 11223344},{'time': '12:00','price':128.9,'volume': 11223344},{'time': '12:00','price':128.9,'volume': 11223344}]
	dateData = json_util.dumps(dateData)
	return dateData

@app.route('/Query', methods=['POST'])
def queQuery():
	stockName = str(request.json['stockName'])
	print stockName
	highest = dbm.get_highest_price_last_ten_days(stockName)
	average = dbm.get_ave_price_last_one_year(stockName)
	lowest = dbm.get_lowest_price_last_one_year(stockName)
	companies = dbm.get_stock_ave_price_lower_than_lowest_price_selected_stock(stockName)
	print companies
	data = [highest,average,lowest]
	eve = ['Highest stock price in the last ten days','Average stock price in the last one year','Lowest stock price in the last ten days']
	
	resData = []
	for i in range(3):
		dataJson = {}
		dataJson['event'] = eve[i]
		dataJson['value'] = data[i]
		resData.append(dataJson)
	# resData = [{'event': 'Highest stock price in the last ten days','value': highest},{'event': 'Average stock price in the last one year','value': average},{{'event': 'Lowest stock price in the last ten days','value': lowest}}]
	# less = dbm.get_stock_ave_price_lower_than_lowest_price_selected_stock()
	resData = json_util.dumps(resData)
	return resData


if __name__ == '__main__':
	app.debug = True
	app.run()

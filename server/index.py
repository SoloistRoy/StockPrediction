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

app = Flask('StockAnnual', template_folder = 'G:\Python\Web\StockPrediction',static_folder='G:\Python\Web\StockPrediction')
# app = Flask('StockAnnual', template_folder = '/Users/jingyuan/WorkSpace/SEProject/StockPrediction',static_folder='/Users/jingyuan/WorkSpace/SEProject/StockPrediction')
app.config['MONGO_DBNAME'] = 'StockAnnual'
app.config['MONGO_URI'] = 'mongodb://localhost/StockAnnual'
app.config['SECRET_KEY'] = 'super secret key'

mongo = PyMongo(app)
# dbClient = MongoClient()
# db = dbClient.StockRealtime
# priceList = realtimeData.getRealtime()
priceList = {'AAPL':{'price':100.00},'BIDU':{'price':100.00},'BABA':{'price':100.00},'YHOO':{'price':100.00},'GOOG':{'price':100.00}}
# annualData.getAnnual()


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
	# print stock.find({})
	historicalData = stock.find({'date':{'$gte':dtsmall, '$lte':dtlarge}}).sort([('date', pymongo.ASCENDING)])
	historicalResult  = []
	for i in historicalData:
		temp = str(i['date']).split(' ')
		i['date'] = temp[0]
		historicalResult.append(i)
	historicalData = json_util.dumps(historicalResult)
	# historicalData = historical.getHisData(stockName, dateRange, stock)
	print idc.RSI(stockName), idc.MACD(stockName)
	return historicalData

@app.route('/getPre', methods=['POST'])
def predict():
	stockName = str(request.json['stockName'])
	stock = mongo.db[stockName]
	latest = stock.find().sort([('date', pymongo.DESCENDING)])[0]
	latest = [latest['high'],latest['low'],latest['open'],latest['close'],latest['volume']]
	
	prePriceJson = []
	#period = datePicker -- add module in JS
	period = int(request.json['datePicker'])

	mPredictor = predictor.annualPredict()
	prePrice = mPredictor.load(stockName, period, latest)
	for i in range(period):
		dataJson = {}
		dataJson['high'] = prePrice[2*i][0]
		dataJson['low'] = prePrice[2*i][1]
		dataJson['open'] = prePrice[2*i][2]
		dataJson['close'] = prePrice[2*i][3]
		dataJson['volume'] = prePrice[2*i][4]
		dataJson['date'] = prePrice[2*i+1]
		prePriceJson.append(dataJson)
		print "===================="
		print dataJson
	prePriceJson = json_util.dumps(prePriceJson)
	print "----------------------------------"
	print prePriceJson #Result of 5 days prediction
	return prePriceJson

if __name__ == '__main__':
	app.debug = True
	app.run()

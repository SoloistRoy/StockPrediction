from flask import Flask, render_template, url_for, request, session, redirect, jsonify
from flask_pymongo import PyMongo
from bson import json_util
import json
import historicalServer as historical

app = Flask('StockAnnual', template_folder = 'G:\Python\Web\StockPrediction',static_folder='G:\Python\Web\StockPrediction')
# app = Flask('StockAnnual', template_folder = '/Users/jingyuan/WorkSpace/SEProject/StockPrediction',static_folder='/Users/jingyuan/WorkSpace/SEProject/StockPrediction')
app.config['MONGO_DBNAME'] = 'StockAnnual'
app.config['MONGO_URI'] = 'mongodb://localhost/StockAnnual'
app.config['SECRET_KEY'] = 'super secret key'

mongo = PyMongo(app)
# dbClient = MongoClient()
# db = dbClient.StockRealtime

@app.route('/home')
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
	stock = mongo.db[stockName]
	m = stock.find({})
	session['piece'] = m[0]['high']
	mClone = json_util.dumps(m.clone())
	# s = copy.deepcopy(mClone)
	print 's: ', type(mClone)
	return jsonify(str(m[0]['high']), mClone)

if __name__ == '__main__':
	app.debug = True
	app.run()

@app.route('/hisData', methods=['POST'])
def hisQuery():
	data = request.data
	dataDict = json.loads(data)
	stockName = dataDict['stockName']
	dateRange = dataDict['dateRange']
	print stockName, dateRange
	stock = mongo.db[stockName]
	print stock.find({})
	
	historicalData = historical.getHisData(stockName, dateRange, stock)
	return str(historicalData)